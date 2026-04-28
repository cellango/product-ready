"""
Jira REST API v3 client.

Authentication: Jira Cloud API token (email + token → Basic auth).
All methods raise JiraError on non-2xx responses so callers don't need
to inspect status codes.

Required environment variables:
  JIRA_BASE_URL       https://your-company.atlassian.net
  JIRA_EMAIL          your-email@company.com
  JIRA_API_TOKEN      API token from id.atlassian.com/manage-profile/security
  JIRA_PROJECT_KEY    e.g. PROD
  JIRA_EPIC_TYPE      issue type name for epics   (default: Epic)
  JIRA_STORY_TYPE     issue type name for stories (default: Story)
"""

from __future__ import annotations

import os
from base64 import b64encode
from dataclasses import dataclass, field
from typing import Any

import urllib.request
import urllib.error
import json


class JiraError(Exception):
    def __init__(self, status: int, body: str) -> None:
        super().__init__(f"Jira API error {status}: {body}")
        self.status = status
        self.body = body


@dataclass
class JiraConfig:
    base_url: str
    email: str
    api_token: str
    project_key: str
    epic_type: str = "Epic"
    story_type: str = "Story"

    @classmethod
    def from_env(cls) -> "JiraConfig":
        missing = [
            k for k in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY")
            if not os.getenv(k)
        ]
        if missing:
            raise RuntimeError(f"Missing Jira config: {', '.join(missing)}")
        return cls(
            base_url=os.environ["JIRA_BASE_URL"].rstrip("/"),
            email=os.environ["JIRA_EMAIL"],
            api_token=os.environ["JIRA_API_TOKEN"],
            project_key=os.environ["JIRA_PROJECT_KEY"],
            epic_type=os.getenv("JIRA_EPIC_TYPE", "Epic"),
            story_type=os.getenv("JIRA_STORY_TYPE", "Story"),
        )


@dataclass
class CreatedIssue:
    key: str
    url: str
    summary: str


@dataclass
class ExportResult:
    epic: CreatedIssue | None = None
    stories: list[CreatedIssue] = field(default_factory=list)

    @property
    def all_issues(self) -> list[CreatedIssue]:
        result = []
        if self.epic:
            result.append(self.epic)
        result.extend(self.stories)
        return result


class JiraClient:
    def __init__(self, config: JiraConfig) -> None:
        self._config = config
        token = b64encode(f"{config.email}:{config.api_token}".encode()).decode()
        self._auth_header = f"Basic {token}"

    def _request(self, method: str, path: str, body: dict | None = None) -> Any:
        url = f"{self._config.base_url}/rest/api/3/{path.lstrip('/')}"
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": self._auth_header,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            raise JiraError(exc.code, exc.read().decode()) from exc

    def validate_project(self) -> bool:
        """Return True if the configured project key exists and is accessible."""
        try:
            self._request("GET", f"project/{self._config.project_key}")
            return True
        except JiraError:
            return False

    def create_epic(self, summary: str, description: str, metrics: list[str]) -> CreatedIssue:
        metrics_text = "\n".join(f"- {m}" for m in metrics) if metrics else ""
        full_description = description
        if metrics_text:
            full_description += f"\n\n**Success Metrics**\n{metrics_text}"

        payload = {
            "fields": {
                "project": {"key": self._config.project_key},
                "summary": summary[:255],
                "description": _adf_doc(full_description),
                "issuetype": {"name": self._config.epic_type},
            }
        }
        result = self._request("POST", "issue", payload)
        return self._to_issue(result, summary)

    def create_story(
        self,
        summary: str,
        description: str,
        acceptance_criteria: str,
        epic_key: str | None = None,
    ) -> CreatedIssue:
        body = description
        if acceptance_criteria:
            body += f"\n\n**Acceptance Criteria**\n{acceptance_criteria}"

        fields: dict[str, Any] = {
            "project": {"key": self._config.project_key},
            "summary": summary[:255],
            "description": _adf_doc(body),
            "issuetype": {"name": self._config.story_type},
        }
        if epic_key:
            # Jira Cloud: link to parent epic via the parent field
            fields["parent"] = {"key": epic_key}

        result = self._request("POST", "issue", {"fields": fields})
        return self._to_issue(result, summary)

    def add_comment(self, issue_key: str, comment: str) -> None:
        self._request(
            "POST",
            f"issue/{issue_key}/comment",
            {"body": _adf_doc(comment)},
        )

    def _to_issue(self, api_response: dict, summary: str) -> CreatedIssue:
        key = api_response["key"]
        url = f"{self._config.base_url}/browse/{key}"
        return CreatedIssue(key=key, url=url, summary=summary)


def _adf_doc(text: str) -> dict:
    """Wrap plain text in Atlassian Document Format (ADF) for Jira API v3."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    content = [
        {
            "type": "paragraph",
            "content": [{"type": "text", "text": para}],
        }
        for para in paragraphs
    ]
    return {"version": 1, "type": "doc", "content": content or [{"type": "paragraph", "content": [{"type": "text", "text": text}]}]}


def build_jira_client() -> JiraClient:
    return JiraClient(JiraConfig.from_env())
