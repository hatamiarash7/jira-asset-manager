"""This module provides the Jira CLI."""

from typing import Optional
import typer
from jira import (
    __app_name__, __version__, __author__, jira, config
)

app = typer.Typer()


@app.command()
def comment(
    asset: str = typer.Argument(
        help="Asset's name"
    ),
    body: str = typer.Argument(
        help="Comment's body"
    )
) -> None:
    """Set a comment for your asset."""
    result = get_jira().add_comment(asset, body)
    if result:
        typer.secho(
            f"Comment added to asset '{asset}' successfully.",
            fg=typer.colors.GREEN
        )
    else:
        typer.secho(
            f"Error adding comment to asset '{asset}'.",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)


@app.command()
def attr(
    asset: str = typer.Argument(
        help="Asset's name"
    ),
    name: str = typer.Argument(
        help="Attribute name"
    ),
    value: str = typer.Argument(
        help="Attribute value"
    )
) -> None:
    """Update an attribute of your asset."""
    result = get_jira().update_asset(asset, name, value)
    if result:
        typer.secho(
            f"Asset '{asset}' updated successfully.",
            fg=typer.colors.GREEN
        )
    else:
        typer.secho(
            f"Error updating asset '{asset}'.",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)


def get_jira() -> jira.JiraAssetHandler:
    if not config.JIRA_SERVER:
        typer.secho(
            "JIRA_SERVER environment variable not set.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    if not config.JIRA_PAT:
        typer.secho(
            "JIRA_PAT environment variable not set.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    return jira.JiraAssetHandler(
        config.JIRA_SERVER,
        config.JIRA_PAT
    )


def _version_callback(value: bool) -> None:
    if value:
        typer.secho(f"{__app_name__} v{__version__}", fg=typer.colors.CYAN)
        raise typer.Exit()


def _author_callback(value: bool) -> None:
    if value:
        typer.secho(f"{__author__}", fg=typer.colors.BRIGHT_MAGENTA)
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version.",
        callback=_version_callback,
        is_eager=True,
    ),
    author: Optional[bool] = typer.Option(
        None,
        "--author",
        "-a",
        help="Show the application's author information.",
        callback=_author_callback,
        is_eager=True,
    )
) -> None:
    return
