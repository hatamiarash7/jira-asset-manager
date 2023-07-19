import os
import tomlkit
import typer

JIRA_SERVER = os.getenv('JIRA_SERVER')
JIRA_PAT = os.getenv('JIRA_PAT')
JIRA_OBJECT = os.getenv('JIRA_OBJECT')
WORK_DIR = os.path.expanduser('~') + '/.jira'


def getConfig(type):
    with open(
        WORK_DIR+"/"+type+".toml",
        mode="r",
        encoding="utf-8"
    ) as file:
        return tomlkit.parse(file.read())


def getSchema(name: str) -> str:
    toml = getConfig('schemas')
    for schema in toml:
        if schema.split(':')[1] == name:
            return schema.split(':')[0]


def getObject(schema: str, name: str) -> str:
    toml = getConfig('schemas')
    return toml[schema][name.lower()]


def getAttributes(name: str) -> str:
    toml = getConfig('attributes')
    for attributes in toml:
        if attributes == name:
            return toml[attributes]


def getAttribute(object: str, name: str) -> str:
    toml = getConfig('attributes')

    for attributes in toml:
        if attributes == object.lower():
            for attribute in toml[attributes]:
                if attribute.split('.')[0] == name.lower():
                    return toml[attributes][attribute]


def getAttributeValue(schema: str, name: str, value: str) -> str:
    toml = getConfig('attributes')

    for attributes in toml:
        if attributes == schema.lower():
            for attribute in toml[attributes]:
                if attribute.split('.')[0] == name.lower():
                    if attribute.split('.')[1] == "7":
                        return getStatus(value)

    return value


def getStatus(name: str) -> str:
    toml = getConfig('status')

    for status in toml:
        if status == name.lower():
            return toml[status]
        if isinstance(toml[status], tomlkit.items.Table):
            for key in toml[status]:
                if key == name.lower():
                    return toml[status][key]

    typer.secho(f"Invalid Type: {name}", fg=typer.colors.RED)
    raise typer.Exit()
