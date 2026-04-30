"""Tests for the Jira REST client."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from slack_bot.jira.client import (
    JiraClient,
    JiraConfig,
    JiraError,
    _adf_doc,
    build_jira_client,
)


@pytest.fixture
def config():
    return JiraConfig(
        base_url="https://example.atlassian.net",
        email="user@example.com",
        api_token="token123",
        project_key="PROD",
    )


@pytest.fixture
def client(config):
    return JiraClient(config)


class TestJiraConfig:
    def test_from_env_raises_when_missing(self, monkeypatch):
        for k in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY"):
            monkeypatch.delenv(k, raising=False)
        with pytest.raises(RuntimeError, match="Missing Jira config"):
            JiraConfig.from_env()

    def test_from_env_reads_all_vars(self, monkeypatch):
        monkeypatch.setenv("JIRA_BASE_URL", "https://co.atlassian.net")
        monkeypatch.setenv("JIRA_EMAIL", "a@b.com")
        monkeypatch.setenv("JIRA_API_TOKEN", "tok")
        monkeypatch.setenv("JIRA_PROJECT_KEY", "ABC")
        cfg = JiraConfig.from_env()
        assert cfg.base_url == "https://co.atlassian.net"
        assert cfg.project_key == "ABC"

    def test_base_url_trailing_slash_stripped(self, monkeypatch):
        monkeypatch.setenv("JIRA_BASE_URL", "https://co.atlassian.net/")
        monkeypatch.setenv("JIRA_EMAIL", "a@b.com")
        monkeypatch.setenv("JIRA_API_TOKEN", "tok")
        monkeypatch.setenv("JIRA_PROJECT_KEY", "ABC")
        cfg = JiraConfig.from_env()
        assert not cfg.base_url.endswith("/")

    def test_defaults_for_issue_types(self, monkeypatch):
        monkeypatch.setenv("JIRA_BASE_URL", "https://x.atlassian.net")
        monkeypatch.setenv("JIRA_EMAIL", "a@b.com")
        monkeypatch.setenv("JIRA_API_TOKEN", "tok")
        monkeypatch.setenv("JIRA_PROJECT_KEY", "X")
        monkeypatch.delenv("JIRA_EPIC_TYPE", raising=False)
        monkeypatch.delenv("JIRA_STORY_TYPE", raising=False)
        cfg = JiraConfig.from_env()
        assert cfg.epic_type == "Epic"
        assert cfg.story_type == "Story"


class TestCreateEpic:
    def test_creates_epic_with_correct_fields(self, client):
        mock_response = {"key": "PROD-1", "id": "10001"}
        with patch.object(client, "_request", return_value=mock_response) as mock_req:
            issue = client.create_epic("Login Feature", "Users can log in", ["Reduce bounce by 10%"])
        mock_req.assert_called_once()
        _, path, payload = mock_req.call_args[0]
        assert path == "issue"
        assert payload["fields"]["summary"] == "Login Feature"
        assert payload["fields"]["issuetype"]["name"] == "Epic"

    def test_returns_created_issue_with_url(self, client, config):
        with patch.object(client, "_request", return_value={"key": "PROD-42"}):
            issue = client.create_epic("Feature", "desc", [])
        assert issue.key == "PROD-42"
        assert "PROD-42" in issue.url
        assert config.base_url in issue.url

    def test_summary_truncated_to_255(self, client):
        long_title = "A" * 300
        with patch.object(client, "_request", return_value={"key": "PROD-1"}) as mock_req:
            client.create_epic(long_title, "desc", [])
        _, _, payload = mock_req.call_args[0]
        assert len(payload["fields"]["summary"]) <= 255


class TestCreateStory:
    def test_creates_story_linked_to_epic(self, client):
        with patch.object(client, "_request", return_value={"key": "PROD-2"}) as mock_req:
            client.create_story("User can log in", "desc", "criteria", epic_key="PROD-1")
        _, _, payload = mock_req.call_args[0]
        assert payload["fields"]["parent"]["key"] == "PROD-1"
        assert payload["fields"]["issuetype"]["name"] == "Story"

    def test_story_without_epic_has_no_parent(self, client):
        with patch.object(client, "_request", return_value={"key": "PROD-3"}) as mock_req:
            client.create_story("Story", "desc", "ac", epic_key=None)
        _, _, payload = mock_req.call_args[0]
        assert "parent" not in payload["fields"]

    def test_acceptance_criteria_in_description(self, client):
        with patch.object(client, "_request", return_value={"key": "PROD-4"}) as mock_req:
            client.create_story("Title", "body", "Given I am logged in…", epic_key=None)
        _, _, payload = mock_req.call_args[0]
        desc_text = str(payload["fields"]["description"])
        assert "Given I am logged in" in desc_text


class TestJiraError:
    def test_request_raises_on_http_error(self, client):
        import urllib.error
        with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError(
            url="", code=403, msg="Forbidden", hdrs=None, fp=None
        )):
            with pytest.raises(JiraError) as exc_info:
                client._request("GET", "project/PROD")
            assert exc_info.value.status == 403

    def test_request_raises_jira_error_on_timeout(self, client):
        with patch("urllib.request.urlopen", side_effect=TimeoutError("timed out")):
            with pytest.raises(JiraError) as exc_info:
                client._request("GET", "project/PROD")
            assert exc_info.value.status == 0
            assert "timed out" in exc_info.value.body


class TestAdfDoc:
    def test_single_paragraph(self):
        doc = _adf_doc("Hello world")
        assert doc["type"] == "doc"
        assert doc["version"] == 1
        assert doc["content"][0]["type"] == "paragraph"
        assert doc["content"][0]["content"][0]["text"] == "Hello world"

    def test_multiple_paragraphs_split_on_blank_line(self):
        doc = _adf_doc("First paragraph.\n\nSecond paragraph.")
        assert len(doc["content"]) == 2
