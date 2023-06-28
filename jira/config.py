import os

JIRA_SERVER = os.getenv('JIRA_SERVER')
JIRA_PAT = os.getenv('JIRA_PAT')
JIRA_OBJECT = os.getenv('JIRA_OBJECT')
WORK_DIR = os.path.expanduser('~') + '/.jira'
