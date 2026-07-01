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
    help="Offline K-CII vulnerability assessment helper. Not an official KISA tool and not a remote collector.",
    no_args_is_help=True,
)
questionnaire_app = typer.Typer(help="Offline questionnaire template export and import commands.")
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
            raise typer.BadParameter(f"invalid evidence JSONL at line {line_number}: {exc}") from exc
    return records


def _load_results(path: Path) -> list[EvaluationResult]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("results", payload if isinstance(payload, list) else None)
    if not isinstance(items, list):
        raise typer.BadParameter("results file must contain a JSON list or a {'results': [...]} object")
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
    target: str = typer.Option("local", "--target", help="Local lab target. Stub supports local only."),
    profile: str = typer.Option("linux", "--profile", help="Local lab profile. Stub supports linux only."),
    output: Path = typer.Option(Path("out"), "--output", "-o", help="Output directory."),
    no_color: bool = typer.Option(False, "--no-color", help="Disable color output for future rich UI."),
    no_advisory: bool = typer.Option(False, "--no-advisory", help="Do not create security advisory files."),
    include_good_advisory: bool = typer.Option(False, "--include-good-advisory", help="Include GOOD items as maintenance advisories."),
) -> None:
    """Create local lab placeholder outputs; not an operational or remote collector."""
    _ = no_color
    if target != "local":
        typer.echo("Only --target local is supported in the scaffold.", err=True)
        raise typer.Exit(code=2)
    if profile != "linux":
        typer.echo("Only --profile linux is supported in the scaffold.", err=True)
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

    typer.echo(f"Created scaffold outputs in {output}")


@questionnaire_app.command("export")
def questionnaire_export(
    profile: str = typer.Option(..., "--profile", help="Questionnaire profile. Supports security-appliance."),
    output: Path = typer.Option(..., "--output", "-o", help="Output questionnaire workbook path."),
) -> None:
    """Export an offline questionnaire workbook template for manual/interview evidence."""
    if _normalize_profile(profile) != "security-appliance":
        typer.echo("Only --profile security-appliance is supported for questionnaire export.", err=True)
        raise typer.Exit(code=2)
    write_security_appliance_questionnaire(output)
    typer.echo(f"Wrote security appliance questionnaire to {output}")


@questionnaire_app.command("import")
def questionnaire_import(
    profile: str = typer.Option(..., "--profile", help="Questionnaire profile. Supports security-appliance."),
    input_path: Path = typer.Option(..., "--input", "-i", help="Completed questionnaire workbook."),
    output: Path = typer.Option(Path("out"), "--output", "-o", help="Output directory."),
    appliance_type: str = typer.Option("firewall", "--appliance-type", help="Security appliance type."),
    asset_id: str = typer.Option("security-appliance-questionnaire", "--asset-id", help="Asset identifier used in outputs."),
    no_advisory: bool = typer.Option(False, "--no-advisory", help="Do not create security advisory files."),
    include_good_advisory: bool = typer.Option(False, "--include-good-advisory", help="Include GOOD items as maintenance advisories."),
) -> None:
    """Import a completed offline questionnaire and create the seven-file output bundle."""
    if _normalize_profile(profile) != "security-appliance":
        typer.echo("Only --profile security-appliance is supported for questionnaire import.", err=True)
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
    typer.echo(f"Imported security appliance questionnaire into {output}")


@app.command("classify-paste")
def classify_paste(
    input_path: Path | None = typer.Option(
        None,
        "--input",
        "-i",
        help="Target server/device result file. Omit to read pasted evidence from standard input.",
    ),
    profile: str = typer.Option("windows", "--profile", help="Offline evidence profile. Supports windows, linux, unix, network, dbms, and security-appliance."),
    vendor: str | None = typer.Option(None, "--vendor", help="Network vendor parser. Required for --profile network; supports cisco_ios."),
    dbms: str | None = typer.Option(None, "--dbms", help="DBMS parser. Required for --profile dbms; supports postgresql, mysql, mariadb."),
    unix: str | None = typer.Option(None, "--unix", help="Unix parser. Required for --profile unix; supports aix, solaris, hpux, linux."),
    appliance_type: str | None = typer.Option(None, "--appliance-type", help="Security appliance type. Supports firewall, ips, ids, waf, vpn, anti-ddos, fortigate, paloalto, cisco-asa, f5."),
    asset_id: str = typer.Option("windows-paste", "--asset-id", help="Asset identifier used in outputs."),
    output: Path = typer.Option(Path("out"), "--output", "-o", help="Output directory."),
    no_advisory: bool = typer.Option(False, "--no-advisory", help="Do not create security advisory files."),
    include_good_advisory: bool = typer.Option(False, "--include-good-advisory", help="Include GOOD items as maintenance advisories."),
) -> None:
    """Classify pasted/copied offline evidence with rulepack decisions."""
    _classify_text(input_path, profile, vendor, dbms, unix, appliance_type, asset_id, output, no_advisory, include_good_advisory)


@app.command("classify-file")
def classify_file(
    input_path: Path = typer.Option(
        ...,
        "--input",
        "-i",
        help="Target server/device result file copied to the Windows work PC.",
    ),
    profile: str = typer.Option("windows", "--profile", help="Offline evidence profile. Supports windows, linux, unix, network, dbms, and security-appliance."),
    vendor: str | None = typer.Option(None, "--vendor", help="Network vendor parser. Required for --profile network; supports cisco_ios."),
    dbms: str | None = typer.Option(None, "--dbms", help="DBMS parser. Required for --profile dbms; supports postgresql, mysql, mariadb."),
    unix: str | None = typer.Option(None, "--unix", help="Unix parser. Required for --profile unix; supports aix, solaris, hpux, linux."),
    appliance_type: str | None = typer.Option(None, "--appliance-type", help="Security appliance type. Supports firewall, ips, ids, waf, vpn, anti-ddos, fortigate, paloalto, cisco-asa, f5."),
    asset_id: str = typer.Option("windows-paste", "--asset-id", help="Asset identifier used in outputs."),
    output: Path = typer.Option(Path("out"), "--output", "-o", help="Output directory."),
    no_advisory: bool = typer.Option(False, "--no-advisory", help="Do not create security advisory files."),
    include_good_advisory: bool = typer.Option(False, "--include-good-advisory", help="Include GOOD items as maintenance advisories."),
) -> None:
    """Classify an offline evidence file copied to the Windows work PC."""
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
        typer.echo("Only --profile windows, --profile linux, --profile unix, --profile network, --profile dbms, and --profile security-appliance are supported for offline classification.", err=True)
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
        typer.echo(f"Classified {len(results)} copied {normalized_profile} item(s) into {output}")
        return

    text = _read_text_input(input_path) if input_path else typer.get_text_stream("stdin").read()
    if not text.strip():
        typer.echo("Pasted output is empty.", err=True)
        raise typer.Exit(code=2)

    if normalized_profile == "windows":
        records = records_from_windows_paste(text, asset_id=asset_id)
    elif normalized_profile == "linux":
        records = records_from_linux_paste(text, asset_id=asset_id if asset_id != "windows-paste" else "linux-paste")
    elif normalized_profile == "unix":
        normalized_unix = (unix or "").strip().lower()
        if normalized_unix not in {"aix", "solaris", "hpux", "linux"}:
            typer.echo("Only --unix aix, --unix solaris, --unix hpux, and --unix linux are supported for --profile unix.", err=True)
            raise typer.Exit(code=2)
        records = records_from_unix_paste(
            text,
            unix_flavor=normalized_unix,
            asset_id=asset_id if asset_id != "windows-paste" else f"unix-{normalized_unix}-paste",
        )
    elif normalized_profile == "network":
        if vendor != "cisco_ios":
            typer.echo("Only --vendor cisco_ios is supported for --profile network.", err=True)
            raise typer.Exit(code=2)
        records = records_from_cisco_ios_paste(
            text,
            asset_id=asset_id if asset_id != "windows-paste" else "network-paste",
        )
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
            typer.echo("Only --dbms postgresql, --dbms mysql, and --dbms mariadb are supported for --profile dbms.", err=True)
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
    typer.echo(f"Classified {len(results)} copied {normalized_profile} item(s) into {output}")


@app.command()
def evaluate(
    evidence: Path = typer.Option(..., "--evidence", "-e", help="Input evidence JSONL file."),
    output: Path = typer.Option(Path("results.json"), "--output", "-o", help="Output results JSON file."),
) -> None:
    """Evaluate evidence with the placeholder deterministic engine."""
    records = _load_evidence_jsonl(evidence)
    results = evaluate_evidence(records)
    _write_json(output, {"results": [result.model_dump(mode="json") for result in results]})
    typer.echo(f"Wrote evaluation results to {output}")


@app.command()
def report(
    results: Path = typer.Option(..., "--results", "-r", help="Input results JSON file."),
    output: Path = typer.Option(Path("report.md"), "--output", "-o", help="Output Markdown report."),
) -> None:
    """Generate a placeholder Markdown report from evaluation results."""
    loaded_results = _load_results(results)
    guide_version = loaded_results[0].guide_version if loaded_results else "unknown"
    write_markdown_report(output, loaded_results, guide_version=guide_version)
    typer.echo(f"Wrote report to {output}")


@app.command()
def redact(
    input_path: Path = typer.Option(..., "--input", "-i", help="Input evidence JSONL file."),
    output: Path = typer.Option(Path("masked_evidence.jsonl"), "--output", "-o", help="Masked JSONL output."),
) -> None:
    """Mask sensitive values from JSONL records before AI-assisted review."""
    masked_rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise typer.BadParameter(f"invalid JSON at line {line_number}: {exc}") from exc
        masked_rows.append(redact_record(payload))
    _write_jsonl(output, masked_rows)
    typer.echo(f"Wrote masked evidence to {output}")


if __name__ == "__main__":
    app()
