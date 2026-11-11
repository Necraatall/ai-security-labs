"""Privacy-preserving standalone HTML and JSON reports."""

from __future__ import annotations

import html
import json
from pathlib import Path


def render_html(data: dict) -> str:
    """Render only structured non-secret evaluation fields."""
    metrics = data["metrics"]
    allowed = (
        "repeat", "case_id", "category", "status", "detections", "output_guard",
        "post_guard_leak", "error_type", "raw_response_length",
    )
    headers = "".join(f"<th>{html.escape(col)}</th>" for col in allowed)
    cells = []
    for row in data["observations"]:
        values = "".join(
            "<td>" + html.escape(str(row.get(col, "")), quote=True) + "</td>"
            for col in allowed
        )
        cells.append("<tr>" + values + "</tr>")
    summary = "".join(
        f"<li>{html.escape(k)}: {html.escape(str(v))}</li>"
        for k, v in metrics.items()
    )
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>AI Security Labs — experiment report</title>"
        "<style>body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:1rem}"
        "table{border-collapse:collapse;width:100%;font-size:13px}td,th{border:1px solid #bbb;"
        "padding:7px;text-align:left}th{background:#eee}</style></head><body>"
        "<h1>AI Security Labs: repeated local model probe</h1>"
        f"<p>Model: {html.escape(data['model_name'])}; "
        f"gate: <strong>{html.escape(data['gate'])}</strong></p>"
        "<p>The protected variant is a deterministic OUTPUT FILTER over the SAME model response. "
        "It is not proof of secure model behavior; unrecognized leaks can pass.</p>"
        f"<ul>{summary}</ul><table><thead><tr>{headers}</tr></thead>"
        f"<tbody>{''.join(cells)}</tbody></table>"
        "<p>No marker, system prompt or raw model output is included in this report.</p>"
        "</body></html>"
    )


def write_reports(data: dict, json_path: Path, html_path: Path) -> None:
    if json_path.resolve() == html_path.resolve():
        raise ValueError("JSON and HTML paths must differ")
    for path in (json_path, html_path):
        path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    html_path.write_text(render_html(data), encoding="utf-8")
