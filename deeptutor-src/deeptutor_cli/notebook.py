"""CLI commands for notebook record management."""

from __future__ import annotations

import json

import typer

from deeptutor.app import DeepTutorApp

from .common import console, print_notebook_table


def register(app: typer.Typer) -> None:
    @app.command("list")
    def list_notebooks() -> None:
        """List notebooks."""
        client = DeepTutorApp()
        print_notebook_table(client.list_notebooks())

    @app.command("create")
    def create_notebook(
        name: str = typer.Argument(..., help="Notebook name."),
        description: str = typer.Option("", "--description", help="Notebook description."),
    ) -> None:
        """Create a notebook."""
        client = DeepTutorApp()
        notebook = client.create_notebook(name=name, description=description)
        console.print(json.dumps(notebook, ensure_ascii=False, indent=2, default=str))

    @app.command("show")
    def show_notebook(
        notebook_id: str = typer.Argument(..., help="Notebook id."),
        fmt: str = typer.Option("rich", "--format", help="Output format: rich | json."),
    ) -> None:
        """Show a notebook and its records."""
        client = DeepTutorApp()
        notebook = client.get_notebook(notebook_id)
        if notebook is None:
            console.print(f"[red]Notebook not found:[/] {notebook_id}")
            raise typer.Exit(code=1)
        if fmt == "json":
            console.print(json.dumps(notebook, ensure_ascii=False, indent=2, default=str))
            return
        console.print(f"[bold]{notebook.get('name', '')}[/] ({notebook.get('id', '')})")
        console.print(str(notebook.get("description", "") or ""))
        for record in notebook.get("records", []):
            console.print(
                f"\n[cyan]{record.get('id', '')}[/] "
                f"{record.get('type', '')} "
                f"{record.get('title', '')}"
            )

    @app.command("remove-record")
    def remove_record(
        notebook_id: str = typer.Argument(..., help="Notebook id."),
        record_id: str = typer.Argument(..., help="Record id."),
    ) -> None:
        """Delete a notebook record."""
        client = DeepTutorApp()
        success = client.remove_record(notebook_id, record_id)
        if not success:
            console.print(f"[red]Record not found:[/] {record_id}")
            raise typer.Exit(code=1)
        console.print(f"Removed record {record_id} from notebook {notebook_id}")
