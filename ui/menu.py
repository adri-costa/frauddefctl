from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

MAIN_MENU = [
    ("1", "Ambiente e autenticação"),
    ("2", "Chaves de site reCAPTCHA / Fraud Defense"),
    ("3", "Chaves de API Google Cloud"),
    ("4", "Inventário e governança"),
    ("5", "Métricas e uso"),
    ("6", "Troubleshooting de integração"),
    ("7", "Troubleshooting de Assessment ID"),
    ("8", "Annotations"),
    ("9", "Relatórios e evidências"),
    ("10", "Drift Detection"),
    ("0", "Sair"),
]

SUBMENU_FOOTER = [("0", "Voltar"), ("99", "Menu principal"), ("q", "Sair")]


def render_menu(title: str, items: list[tuple[str, str]]) -> str:
    lines = [f"[{key}] {label}" for key, label in items]
    console.print(Panel("\n".join(lines), title=title, expand=False))
    return Prompt.ask("Selecione uma opção")


def run_interactive_menu() -> None:
    while True:
        choice = render_menu("frauddefctl - Google Cloud Fraud Defense Terminal", MAIN_MENU)
        if choice in {"0", "q", "Q"}:
            console.print("Saindo.")
            return
        console.print(f"Opção {choice} selecionada. Módulo será plugado nas próximas fases.")
        console.print("Todo submenu terá [0] Voltar, [99] Menu principal e [q] Sair.")
