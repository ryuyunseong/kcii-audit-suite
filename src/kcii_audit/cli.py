from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

from kcii_audit.ai.redactor import redact_record
from kcii_audit.collectors.os.linux import LinuxCollector
from kcii_audit.engine.evaluator import evaluate_evidence
from kcii_audit.parsers.linux_server import records_from_linux_paste
from kcii_audit.parsers.dbms_mariadb import records_from_mariadb_paste
from kcii_audit.parsers.dbms_mysql import records_from_mysql_paste
from kcii_audit.parsers.dbms_postgresql import records_from_postgresql_paste
from kcii_audit.parsers.network_cisco_ios import records_from_cisco_ios_paste
from kcii_audit.parsers.network_junos import records_from_junos_paste
from kcii_audit.parsers.security_appliance_common import records_from_security_appliance_paste
from kcii_audit.parsers.security_appliance_questionnaire import records_from_security_appliance_questionnaire
from kcii_audit.parsers.unix_server import records_from_unix_paste
from kcii_audit.parsers.windows_server import records_from_windows_paste
from kcii_audit.reports.excel_writer import write_detail_workbook, write_summary_workbook
from kcii_audit.reports.advisory_writer import write_security_advisory_markdown, write_security_advisory_workbook
from kcii_audit.reports.questionnaire_writer import write_security_appliance_questionnaire
from kcii_audit.reports.report_writer import write_markdown_report
from kcii_audit.schemas.evidence import EvidenceRecord
from kcii_audit.schemas.result import EvaluationResult

app = typer.Typer(
    help="K-CII 오프라인 취약점 분석·평가 보조 도구입니다. KISA 공식 도구나 원격 수집기가 아닙니다.",
    no_args_is_help=True,
)
questionnaire_app = typer.Typer(help="오프라인 보안장비 질의서 내보내기·가져오기 명령입니다.")
app.add_typer(questionnaire_app, name="questionnaire")


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    path.write_text(content, encoding="utf-8")


def _load_evidence_jsonl(path: Path) -> list[EvidenceRecord]:
    records: list[EvidenceRecord] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(EvidenceRecord.model_validate_json(line))
        except Exception as exc:  # pragma: no cover - pydantic message shape can change
            raise typer.BadParameter(f"증적 JSONL {line_number}번째 줄이 올바르지 않습니다: {exc}") from exc
    return records


def _load_results(path: Path) -> list[EvaluationResult]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("results", payload if isinstance(payload, list) else None)
    if not isinstance(items, list):
        raise typer.BadParameter("결과 파일에는 JSON 목록 또는 {'results': [...]} 객체가 있어야 합니다")
    return [EvaluationResult.model_validate(item) for item in items]


def _read_text_input(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-16"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def _normalize_profile(profile: str) -> str:
    return profile.strip().lower().replace("_", "-")


def _is_excel_input(path: Path | None) -> bool:
    return path is not None and path.suffix.lower() in {".xlsx", ".xlsm"}


def _write_output_bundle(
    output: Path,
    records: list[EvidenceRecord],
    results: list[EvaluationResult],
    *,
    write_advisory: bool = True,
    include_good_advisory: bool = False,
) -> None:
    output.mkdir(parents=True, exist_ok=True)
    evidence_rows = [record.model_dump(mode="json") for record in records]
    result_rows = [result.model_dump(mode="json") for result in results]

    _write_jsonl(output / "evidence.jsonl", evidence_rows)
    _write_json(output / "results.json", {"results": result_rows})
    write_detail_workbook(output / "detail.xlsx", results, include_good_advisory=include_good_advisory)
    write_summary_workbook(output / "summary.xlsx", results, include_good_advisory=include_good_advisory)
    guide_version = records[0].guide_version if records else "unknown"
    write_markdown_report(
        output / "report.md",
        results,
        guide_version=guide_version,
        include_good_advisory=include_good_advisory,
    )
    if write_advisory:
        write_security_advisory_markdown(
            output / "security_advisory.md",
            results,
            include_good=include_good_advisory,
        )
        write_security_advisory_workbook(
            output / "security_advisory.xlsx",
            results,
            include_good=include_good_advisory,
        )


@app.command()
def scan(
    target: str = typer.Option("local", "--target", help="로컬 검증 대상입니다. 현재 local만 지원합니다."),
    profile: str = typer.Option("linux", "--profile", help="로컬 검증 프로파일입니다. 현재 linux만 지원합니다."),
    output: Path = typer.Option(Path("out"), "--output", "-o", help="산출물 디렉터리입니다."),
    no_color: bool = typer.Option(False, "--no-color", help="향후 컬러 UI 출력을 사용하지 않습니다."),
    no_advisory: bool = typer.Option(False, "--no-advisory", help="보안 권고문 파일을 생성하지 않습니다."),
    include_good_advisory: bool = typer.Option(False, "--include-good-advisory", help="양호 항목도 유지관리 권고문에 포함합니다."),
) -> None:
    """운영 수집이 아닌 로컬 검증용 예시 산출물을 생성합니다."""
    _ = no_color
    if target != "local":
        typer.echo("현재 --target local만 지원합니다.", err=True)
        raise typer.Exit(code=2)
    if profile != "linux":
        typer.echo("현재 로컬 검증에서는 --profile linux만 지원합니다.", err=True)
        raise typer.Exit(code=2)

    records = LinuxCollector().collect(asset_id=target)
    results = evaluate_evidence(records)

    _write_output_bundle(
        output,
        records,
        results,
        write_advisory=not no_advisory,
        include_good_advisory=include_good_advisory,
    )

    typer.echo(f"로컬 검증 산출물을 생성했습니다: {output}")


@questionnaire_app.command("export")
def questionnaire_export(
    profile: str = typer.Option(..., "--profile", help="질의서 프로파일입니다. security-appliance를 지원합니다."),
    output: Path = typer.Option(..., "--output", "-o", help="질의서 Excel 저장 경로입니다."),
) -> None:
    """수동확인·인터뷰 증적용 보안장비 질의서 Excel을 생성합니다."""
    if _normalize_profile(profile) != "security-appliance":
        typer.echo("질의서 내보내기는 --profile security-appliance만 지원합니다.", err=True)
        raise typer.Exit(code=2)
    write_security_appliance_questionnaire(output)
    typer.echo(f"보안장비 질의서를 생성했습니다: {output}")


@questionnaire_app.command("import")
def questionnaire_import(
    profile: str = typer.Option(..., "--profile", help="질의서 프로파일입니다. security-appliance를 지원합니다."),
    input_path: Path = typer.Option(..., "--input", "-i", help="답변을 작성한 질의서 Excel입니다."),
    output: Path = typer.Option(Path("out"), "--output", "-o", help="산출물 디렉터리입니다."),
    appliance_type: str = typer.Option("firewall", "--appliance-type", help="보안장비 유형입니다."),
    asset_id: str = typer.Option("security-appliance-questionnaire", "--asset-id", help="산출물에 사용할 비식별 자산 ID입니다."),
    no_advisory: bool = typer.Option(False, "--no-advisory", help="보안 권고문 파일을 생성하지 않습니다."),
    include_good_advisory: bool = typer.Option(False, "--include-good-advisory", help="양호 항목도 유지관리 권고문에 포함합니다."),
) -> None:
    """작성된 보안장비 질의서를 가져와 기본 7개 산출물을 생성합니다."""
    if _normalize_profile(profile) != "security-appliance":
        typer.echo("질의서 가져오기는 --profile security-appliance만 지원합니다.", err=True)
        raise typer.Exit(code=2)
    try:
        records = records_from_security_appliance_questionnaire(
            input_path,
            appliance_type=appliance_type,
            asset_id=asset_id,
        )
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc

    results = evaluate_evidence(records)
    _write_output_bundle(
        output,
        records,
        results,
        write_advisory=not no_advisory,
        include_good_advisory=include_good_advisory,
    )
    typer.echo(f"보안장비 질의서를 분석해 산출물을 생성했습니다: {output}")


@app.command("classify-paste")
def classify_paste(
    input_path: Path | None = typer.Option(
        None,
        "--input",
        "-i",
        help="대상 서버·장비의 결과 파일입니다. 생략하면 표준 입력의 붙여넣기 증적을 읽습니다.",
    ),
    profile: str = typer.Option("windows", "--profile", help="오프라인 증적 프로파일입니다: windows, linux, unix, network, dbms, security-appliance."),
    vendor: str | None = typer.Option(None, "--vendor", help="네트워크 벤더입니다. network에서 필수이며 cisco_ios, junos를 지원합니다."),
    dbms: str | None = typer.Option(None, "--dbms", help="DBMS 종류입니다. dbms에서 필수이며 postgresql, mysql, mariadb를 지원합니다."),
    unix: str | None = typer.Option(None, "--unix", help="Unix 종류입니다. unix에서 필수이며 aix, solaris, hpux, linux를 지원합니다."),
    appliance_type: str | None = typer.Option(None, "--appliance-type", help="보안장비 유형입니다: firewall, ips, ids, waf, vpn, anti-ddos, fortigate, paloalto, cisco-asa, f5."),
    asset_id: str = typer.Option("windows-paste", "--asset-id", help="산출물에 사용할 비식별 자산 ID입니다."),
    output: Path = typer.Option(Path("out"), "--output", "-o", help="산출물 디렉터리입니다."),
    no_advisory: bool = typer.Option(False, "--no-advisory", help="보안 권고문 파일을 생성하지 않습니다."),
    include_good_advisory: bool = typer.Option(False, "--include-good-advisory", help="양호 항목도 유지관리 권고문에 포함합니다."),
) -> None:
    """복사하거나 붙여넣은 오프라인 증적을 rulepack 기준으로 판정합니다."""
    _classify_text(input_path, profile, vendor, dbms, unix, appliance_type, asset_id, output, no_advisory, include_good_advisory)


@app.command("classify-file")
def classify_file(
    input_path: Path = typer.Option(
        ...,
        "--input",
        "-i",
        help="Windows 작업 PC로 가져온 대상 서버·장비 결과 파일입니다.",
    ),
    profile: str = typer.Option("windows", "--profile", help="오프라인 증적 프로파일입니다: windows, linux, unix, network, dbms, security-appliance."),
    vendor: str | None = typer.Option(None, "--vendor", help="네트워크 벤더입니다. network에서 필수이며 cisco_ios, junos를 지원합니다."),
    dbms: str | None = typer.Option(None, "--dbms", help="DBMS 종류입니다. dbms에서 필수이며 postgresql, mysql, mariadb를 지원합니다."),
    unix: str | None = typer.Option(None, "--unix", help="Unix 종류입니다. unix에서 필수이며 aix, solaris, hpux, linux를 지원합니다."),
    appliance_type: str | None = typer.Option(None, "--appliance-type", help="보안장비 유형입니다: firewall, ips, ids, waf, vpn, anti-ddos, fortigate, paloalto, cisco-asa, f5."),
    asset_id: str = typer.Option("windows-paste", "--asset-id", help="산출물에 사용할 비식별 자산 ID입니다."),
    output: Path = typer.Option(Path("out"), "--output", "-o", help="산출물 디렉터리입니다."),
    no_advisory: bool = typer.Option(False, "--no-advisory", help="보안 권고문 파일을 생성하지 않습니다."),
    include_good_advisory: bool = typer.Option(False, "--include-good-advisory", help="양호 항목도 유지관리 권고문에 포함합니다."),
) -> None:
    """Windows 작업 PC로 가져온 오프라인 증적 파일을 판정합니다."""
    _classify_text(input_path, profile, vendor, dbms, unix, appliance_type, asset_id, output, no_advisory, include_good_advisory)


def _classify_text(
    input_path: Path | None,
    profile: str,
    vendor: str | None,
    dbms: str | None,
    unix: str | None,
    appliance_type: str | None,
    asset_id: str,
    output: Path,
    no_advisory: bool,
    include_good_advisory: bool,
) -> None:
    normalized_profile = _normalize_profile(profile)
    if normalized_profile not in {"windows", "linux", "unix", "network", "dbms", "security-appliance"}:
        typer.echo("오프라인 판정은 --profile windows, linux, unix, network, dbms, security-appliance만 지원합니다.", err=True)
        raise typer.Exit(code=2)

    if normalized_profile == "security-appliance" and _is_excel_input(input_path):
        try:
            records = records_from_security_appliance_questionnaire(
                input_path,
                appliance_type=appliance_type or "firewall",
                asset_id=asset_id if asset_id != "windows-paste" else "security-appliance-questionnaire",
            )
        except ValueError as exc:
            typer.echo(str(exc), err=True)
            raise typer.Exit(code=2) from exc
        results = evaluate_evidence(records)
        _write_output_bundle(
            output,
            records,
            results,
            write_advisory=not no_advisory,
            include_good_advisory=include_good_advisory,
        )
        typer.echo(f"{normalized_profile} 항목 {len(results)}개를 판정해 산출물을 생성했습니다: {output}")
        return

    text = _read_text_input(input_path) if input_path else typer.get_text_stream("stdin").read()
    if not text.strip():
        typer.echo("입력한 증적이 비어 있습니다.", err=True)
        raise typer.Exit(code=2)

    if normalized_profile == "windows":
        records = records_from_windows_paste(text, asset_id=asset_id)
    elif normalized_profile == "linux":
        records = records_from_linux_paste(text, asset_id=asset_id if asset_id != "windows-paste" else "linux-paste")
    elif normalized_profile == "unix":
        normalized_unix = (unix or "").strip().lower()
        if normalized_unix not in {"aix", "solaris", "hpux", "linux"}:
            typer.echo("--profile unix에서는 --unix aix, solaris, hpux, linux만 지원합니다.", err=True)
            raise typer.Exit(code=2)
        records = records_from_unix_paste(
            text,
            unix_flavor=normalized_unix,
            asset_id=asset_id if asset_id != "windows-paste" else f"unix-{normalized_unix}-paste",
        )
    elif normalized_profile == "network":
        normalized_vendor = (vendor or "").strip().lower().replace("-", "_")
        if normalized_vendor == "cisco_ios":
            records = records_from_cisco_ios_paste(
                text,
                asset_id=asset_id if asset_id != "windows-paste" else "network-paste",
            )
        elif normalized_vendor in {"junos", "juniper_junos"}:
            records = records_from_junos_paste(
                text,
                asset_id=asset_id if asset_id != "windows-paste" else "network-junos-paste",
            )
        else:
            typer.echo("--profile network에서는 --vendor cisco_ios와 junos만 지원합니다.", err=True)
            raise typer.Exit(code=2)
    elif normalized_profile == "dbms":
        normalized_dbms = (dbms or "").strip().lower()
        if normalized_dbms == "postgresql":
            records = records_from_postgresql_paste(
                text,
                asset_id=asset_id if asset_id != "windows-paste" else "dbms-postgresql-paste",
            )
        elif normalized_dbms == "mysql":
            records = records_from_mysql_paste(
                text,
                asset_id=asset_id if asset_id != "windows-paste" else "dbms-mysql-paste",
            )
        elif normalized_dbms == "mariadb":
            records = records_from_mariadb_paste(
                text,
                asset_id=asset_id if asset_id != "windows-paste" else "dbms-mariadb-paste",
            )
        else:
            typer.echo("--profile dbms에서는 --dbms postgresql, mysql, mariadb만 지원합니다.", err=True)
            raise typer.Exit(code=2)
    else:
        try:
            records = records_from_security_appliance_paste(
                text,
                appliance_type=appliance_type or "firewall",
                asset_id=asset_id if asset_id != "windows-paste" else "security-appliance-paste",
            )
        except ValueError as exc:
            typer.echo(str(exc), err=True)
            raise typer.Exit(code=2) from exc
    results = evaluate_evidence(records)
    _write_output_bundle(
        output,
        records,
        results,
        write_advisory=not no_advisory,
        include_good_advisory=include_good_advisory,
    )
    typer.echo(f"{normalized_profile} 항목 {len(results)}개를 판정해 산출물을 생성했습니다: {output}")


@app.command()
def evaluate(
    evidence: Path = typer.Option(..., "--evidence", "-e", help="입력 증적 JSONL 파일입니다."),
    output: Path = typer.Option(Path("results.json"), "--output", "-o", help="판정 결과 JSON 파일입니다."),
) -> None:
    """정규화된 증적을 결정론적 rulepack 엔진으로 판정합니다."""
    records = _load_evidence_jsonl(evidence)
    results = evaluate_evidence(records)
    _write_json(output, {"results": [result.model_dump(mode="json") for result in results]})
    typer.echo(f"판정 결과를 저장했습니다: {output}")


@app.command()
def report(
    results: Path = typer.Option(..., "--results", "-r", help="입력 판정 결과 JSON 파일입니다."),
    output: Path = typer.Option(Path("report.md"), "--output", "-o", help="Markdown 결과 보고서 경로입니다."),
) -> None:
    """판정 결과로 Markdown 보고서를 생성합니다."""
    loaded_results = _load_results(results)
    guide_version = loaded_results[0].guide_version if loaded_results else "unknown"
    write_markdown_report(output, loaded_results, guide_version=guide_version)
    typer.echo(f"보고서를 생성했습니다: {output}")


@app.command()
def redact(
    input_path: Path = typer.Option(..., "--input", "-i", help="입력 증적 JSONL 파일입니다."),
    output: Path = typer.Option(Path("masked_evidence.jsonl"), "--output", "-o", help="마스킹된 JSONL 저장 경로입니다."),
) -> None:
    """AI 보조 검토 전에 JSONL 증적의 민감정보를 마스킹합니다."""
    masked_rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise typer.BadParameter(f"JSON {line_number}번째 줄이 올바르지 않습니다: {exc}") from exc
        masked_rows.append(redact_record(payload))
    _write_jsonl(output, masked_rows)
    typer.echo(f"마스킹된 증적을 저장했습니다: {output}")


if __name__ == "__main__":
    app()
