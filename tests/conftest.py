import pytest
import os


@pytest.fixture(scope="session", autouse=True)
def env_setup():
    os.environ["JIRA_SERVER"] = "https://jira.example.com"
    os.environ["JIRA_PAT"] = "1234567890"
