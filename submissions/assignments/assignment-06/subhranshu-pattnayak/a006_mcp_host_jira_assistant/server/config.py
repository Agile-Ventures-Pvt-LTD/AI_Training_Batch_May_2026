"""Main Configuration file for Jira MCP Server."""

import os
from dotenv import load_dotenv

load_dotenv()

JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")


if not JIRA_API_TOKEN:
    raise ValueError("JIRA_API_TOKEN not in .env")

if not JIRA_BASE_URL:
    raise ValueError("JIRA_BASE_URL not in .env")

if not JIRA_EMAIL:
    raise ValueError("JIRA_EMAIL not in .env")