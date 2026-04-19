"""
CLI memory commands for the two-file public memory system (SUMMARY/PROFILE).
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from deeptutor.services.memory import get_memory_service

console = Console()


def register(app: typer.Typer) -> None:
    @app.command("show")
    def memory_show(
        file: str = typer.Argument(
            "all", help="File to show: summary, profile, or all.",
        ),
    ) -> None:
        """Display memory file content."""
        svc = get_memory_service()
        if file == "all":
            snap = svc.read_snapshot()
            for label, content in [
                ("SUMMARY", snap.summary),
                ("PROFILE", snap.profile),
            ]:
                if content:
                    console.print(Panel(Markdown(content), title=f"[bold]{label}.md[/]"))
                else:
                    console.print(f"[dim]{label}.md: (empty)[/]")
        elif file in ("summary", "profile"):
            content = svc.read_file(file)
            if content:
                console.print(Panel(Markdown(content), title=f"[bold]{file.upper()}.md[/]"))
            else:
                console.print(f"[dim]{file.upper()}.md: (empty)[/]")
        else:
            console.print(f"[red]Unknown file: {file}. Use summary, profile, or all.[/]")

    @app.command("clear")
    def memory_clear(
        file: str = typer.Argument(
            "all", help="File to clear: summary, profile, or all.",
        ),
        force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation."),
    ) -> None:
        """Clear memory file(s)."""
        svc = get_memory_service()
        if file not in ("summary", "profile", "all"):
            console.print(f"[red]Unknown file: {file}[/]")
            raise typer.Exit(1)

        if not force:
            target = "all memory files" if file == "all" else f"{file.upper()}.md"
            if not typer.confirm(f"Clear {target}?"):
                raise typer.Abort()

        if file == "all":
            svc.clear_memory()
            console.print("[green]Cleared all memory files.[/]")
        else:
            svc.clear_file(file)
            console.print(f"[green]Cleared {file.upper()}.md.[/]")
