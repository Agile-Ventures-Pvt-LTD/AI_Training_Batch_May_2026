from jira import JIRA
from dotenv import load_dotenv
import os

load_dotenv()


def test_jira_connection():

    jira = JIRA(
        server=os.getenv("JIRA_BASE_URL"),
        basic_auth=(
            os.getenv("JIRA_EMAIL"),
            os.getenv("JIRA_API_TOKEN"),
        ),
    )

    projects = jira.projects()

    assert projects is not None

    assert len(projects) > 0