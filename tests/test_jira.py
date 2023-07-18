from typer.testing import CliRunner
from jira_amt import __app_name__, __version__, __author__, cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_author():
    result = runner.invoke(cli.app, ["--author"])
    assert result.exit_code == 0
    assert f"{__author__}\n" in result.stdout
