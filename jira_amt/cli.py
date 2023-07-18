"""This module provides the Jira CLI."""

import json
from pathlib import Path

import tomlkit as toml
from tomlkit import document, table, comment as cm, nl
from typing import Optional
import typer

from jira_amt import (
    __app_name__, __version__, __author__, config, jira
)

app = typer.Typer()


@app.command()
def init() -> None:
    """Initialize Jira CLI."""
    typer.secho("Initializing Jira CLI ...", fg=typer.colors.GREEN)

    # Create work directory
    Path(config.WORK_DIR).mkdir(parents=True, exist_ok=True)

    # Create schemas file
    schema_list = document()
    typer.secho("  -> Fetching schemas", fg=typer.colors.BRIGHT_GREEN)
    schema_list.add(
        cm(f"Jira Asset Management - Status list - v{__version__}")
    )
    schemas = json.loads(get_jira().get_schema().text)
    for schema in schemas['objectschemas']:
        title = f"{schema['id']}:{schema['name']}"
        schema_list.add(title, table())
        objects = json.loads(get_jira().get_objecttypes(schema['id']).text)
        for object in objects:
            schema_list[title].add(object['name'].lower(), object['id'])
    with open(
        config.WORK_DIR+"/schemas.toml",
        mode="w",
        encoding="utf-8"
    ) as file:
        toml.dump(schema_list, file)

    # Create attributes file
    typer.secho("  -> Fetching attributes", fg=typer.colors.BRIGHT_GREEN)
    attr_list = document()
    attr_list.add(
        cm(f"Jira Asset Management - Status list - v{__version__}")
    )
    for object in objects:
        result = json.loads(get_jira().get_attributes(object['id']).text)
        attributes = table()
        for attribute in result:
            attributes.add(
                attribute['name'].lower() + "." + str(attribute['type']),
                attribute['id']
            )
        attr_list.add(object['name'].lower(), attributes)
    with open(
        config.WORK_DIR+"/attributes.toml",
        mode="w",
        encoding="utf-8"
    ) as file:
        toml.dump(attr_list, file)

    # Create statuses file
    typer.secho("  -> Fetching statuses", fg=typer.colors.BRIGHT_GREEN)
    status_list = document()
    status_list.add(
        cm(f"Jira Asset Management - Status list - v{__version__}")
    )
    status_list.add(nl())
    globals = json.loads(get_jira().get_global_statustypes().text)
    for status in globals:
        status_list.add(status['name'].lower(), status['id'])
    for schema in schemas['objectschemas']:
        locals = json.loads(
            get_jira().get_statustypes(schema['id']).text
        )
        temp = table()
        for status in locals:
            temp.add(status['name'].lower(), status['id'])
        status_list.add(schema['name'], temp)

    with open(
        config.WORK_DIR+"/status.toml",
        mode="w",
        encoding="utf-8"
    ) as file:
        toml.dump(status_list, file)

    typer.secho("Done!", fg=typer.colors.GREEN)


@app.command()
def comment(
    schema: str = typer.Argument(
        help="Your schema name"
    ),
    object: str = typer.Argument(
        help="Your object name"
    ),
    asset: str = typer.Argument(
        help="Asset's name"
    ),
    body: str = typer.Argument(
        help="Comment's body"
    )
) -> None:
    """Set a comment for your asset."""
    result = get_jira().add_comment(schema, object, asset, body)
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
    schema: str = typer.Argument(
        help="Your schema name"
    ),
    object: str = typer.Argument(
        help="Your object name"
    ),
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
    result = get_jira().update_asset(schema, object, asset, name, value)
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
