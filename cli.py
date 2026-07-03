from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from frauddefctl.core.config import load_config
from frauddefctl.core.models import AssessmentRecord
from frauddefctl.core.parsing import parse_many
from frauddefctl.core.reports import export_csv, export_json, export_markdown, timestamp
from frauddefctl.core.risk import classify_score, score_to_bucket
from frauddefctl.modules.safe_risk import summarize_safe_risk
from frauddefctl.modules.search import detect_search_type, normalize_search_value
from frauddefctl.ui.menu import run_interactive_menu

app = typer.Typer(help="frauddefctl - terminal administrativo para Google Cloud Fraud Defense")
config_app = typer.Typer(help="Configuração")
utils_app = typer.Typer(help="Utilidades")
risk_app = typer.Typer(help="Classificação SAFE/RISK")
report_app = typer.Typer(help="Relatórios")
search_app = typer.Typer(help="Busca e normalização")

app.add_typer(config_app, name="config")
app.add_typer(utils_app, name="utils")
app.add_typer(risk_app, name="risk")
app.add_typer(report_app, name="report")
app.add_typer(search_app, name="search")

console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Abrir menu interativo estilo ATM"),
):
    if ctx.invoked_subcommand is None and interactive:
        run_interactive_menu()
    elif ctx.invoked_subcommand is None:
        console.print("Use --help para ver comandos ou --interactive para abrir o menu.")


@config_app.command("validate")
def validate_config(
    config_path: Path = typer.Option(Path("config/config.example.yaml"), "--config", help="Arquivo YAML de configuração"),
):
    config = load_config(config_path)
    table = Table(title="Projetos configurados")
    table.add_column("Project ID")
    table.add_column("Alias")
    table.add_column("Environment")
    table.add_column("Enabled")
    for project in config.projects:
        table.add_row(project.project_id, project.alias or "", project.environment or "", str(project.enabled))
    console.print(table)
    console.print(f"Threshold SAFE/RISK: {config.defaults.score_safe_threshold}")


@utils_app.command("parse-values")
def parse_values(
    values: Optional[str] = typer.Option(None, "--values", "-v", help="Valores colados"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Arquivo com valores"),
    output_json: bool = typer.Option(False, "--json", help="Saída JSON"),
):
    parsed = parse_many(values, file)
    if output_json:
        console.print(json.dumps(parsed, ensure_ascii=False, indent=2))
        return
    for idx, item in enumerate(parsed, start=1):
        console.print(f"{idx}. {item}")


@risk_app.command("classify")
def classify(
    score: Optional[float] = typer.Option(None, "--score", help="Score decimal 0.0 a 1.0"),
    threshold: float = typer.Option(0.5, "--threshold", help="Threshold SAFE/RISK"),
):
    verdict = classify_score(score, threshold)
    bucket = score_to_bucket(score)
    console.print(f"score_decimal: {score}")
    console.print(f"score_bucket : {bucket}")
    console.print(f"threshold    : {threshold}")
    console.print(f"risk_status  : {verdict.value}")


@search_app.command("detect")
def search_detect(value: str = typer.Argument(..., help="Nome, URL, domínio, IP/CIDR ou site key")):
    console.print({
        "input": value,
        "detected_type": detect_search_type(value),
        "normalized": normalize_search_value(value),
    })


def _read_assessments_csv(input_path: Path) -> list[AssessmentRecord]:
    with input_path.open("r", encoding="utf-8-sig", newline="") as fp:
        sample = fp.read(4096)
        fp.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t") if sample else csv.excel
        reader = csv.DictReader(fp, dialect=dialect)
        records = []
        for index, row in enumerate(reader, start=1):
            score_raw = row.get("score_decimal") or row.get("score") or ""
            score = float(score_raw.replace(",", ".")) if score_raw else None
            records.append(
                AssessmentRecord(
                    assessment_id=row.get("assessment_id") or f"row-{index}",
                    project_id=row.get("project_id") or None,
                    site_key_id=row.get("site_key_id") or None,
                    display_name=row.get("display_name") or None,
                    score_decimal=score,
                    action_expected=row.get("action_expected") or None,
                    action_returned=row.get("action_returned") or None,
                    hostname=row.get("hostname") or None,
                )
            )
    return records


@report_app.command("safe-risk")
def report_safe_risk(
    input_path: Path = typer.Option(..., "--input", "-i", help="CSV com assessments e coluna score_decimal"),
    output_dir: Path = typer.Option(Path("reports/metrics"), "--output-dir", help="Diretório de saída"),
    threshold: float = typer.Option(0.5, "--threshold", help="Threshold SAFE/RISK"),
    formats: str = typer.Option("csv,json,markdown", "--formats", help="csv,json,markdown"),
    csv_separator: str = typer.Option(";", "--csv-separator", help="Separador CSV"),
):
    records = _read_assessments_csv(input_path)
    summary = summarize_safe_risk(records, threshold)
    now = timestamp()
    output_dir.mkdir(parents=True, exist_ok=True)

    table = Table(title="Relatório SAFE x RISK")
    table.add_column("Métrica")
    table.add_column("Valor")
    for key, value in summary.items():
        table.add_row(key, str(value))
    console.print(table)

    rows = [summary]
    generated: list[Path] = []
    requested = {item.strip().lower() for item in formats.split(",") if item.strip()}
    if "csv" in requested:
        generated.append(export_csv(rows, output_dir / f"safe_risk_summary_{now}.csv", separator=csv_separator))
    if "json" in requested:
        generated.append(export_json(rows, output_dir / f"safe_risk_summary_{now}.json"))
    if "markdown" in requested or "md" in requested:
        generated.append(export_markdown(rows, output_dir / f"safe_risk_summary_{now}.md", "Relatório SAFE x RISK"))

    console.print("Arquivos gerados:")
    for path in generated:
        console.print(f"- {path}")


if __name__ == "__main__":
    app()
