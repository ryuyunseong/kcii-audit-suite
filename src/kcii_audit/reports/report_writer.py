from __future__ import annotations

from collections import Counter
from pathlib import Path

from jinja2 import Template

from kcii_audit.reports.advisory_writer import generate_security_advisories
from kcii_audit.schemas.result import EvaluationResult

REPORT_TEMPLATE = """# K-CII 점검 결과 보고서

## 개요

- 기준 버전: {{ guide_version }}
- 산출 상태: scaffold placeholder
- 원본 민감정보 포함 여부: 포함하지 않음

## 종합 결과

| 판정 | 건수 |
| --- | ---: |
{% for status, count in status_counts.items() -%}
| {{ status }} | {{ count }} |
{% endfor %}

## 상세 결과

| 자산ID | 분야 | 항목ID | 항목명 | 판정 | 판정근거 |
| --- | --- | --- | --- | --- | --- |
{% for result in results -%}
| {{ result.asset_id }} | {{ result.platform }} | {{ result.item_id }} | {{ result.item_title }} | {{ result.status_label }} | {{ result.reason }} |
{% endfor %}

## 보안 권고문 요약

{% if advisory_counts -%}
| 판정 | 권고문 수 |
| --- | ---: |
{% for status, count in advisory_counts.items() -%}
| {{ status }} | {{ count }} |
{% endfor %}
{% else -%}
권고 대상 항목이 없습니다.
{% endif %}

## 상세 권고문

{% if advisories -%}
{% for advisory in advisories -%}
### {{ advisory.advisory_id }} {{ advisory.title }}

- 관련 항목: {{ advisory.item_id }}
- 영향도: {{ advisory.impact }}
- 대상: {{ advisory.masked_asset }}
- 판정: {{ advisory.status_label }}
- 취약 사유: {{ advisory.reason }}
- 권고 조치: {{ advisory.recommendation }}
- 재점검 방법: {{ advisory.retest_method }}

{% endfor -%}
{% else -%}
생성된 상세 권고문이 없습니다.
{% endif %}

## 조치 권고

취약 및 수동확인 항목은 보안 권고문에 따라 조치 또는 추가 확인을 진행합니다.

## 부록

원본 증적은 보고서에 포함하지 않고, 향후 local vault와 hash 기반 참조로 분리합니다.
"""


def write_markdown_report(
    path: Path,
    results: list[EvaluationResult],
    guide_version: str,
    *,
    include_good_advisory: bool = False,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    status_counts = Counter(result.status_label for result in results)
    advisories = generate_security_advisories(results, include_good=include_good_advisory)
    advisory_counts = Counter(advisory.status_label for advisory in advisories)
    rendered = Template(REPORT_TEMPLATE).render(
        guide_version=guide_version,
        results=results,
        status_counts=dict(status_counts),
        advisories=advisories,
        advisory_counts=dict(advisory_counts),
    )
    path.write_text(rendered, encoding="utf-8")
