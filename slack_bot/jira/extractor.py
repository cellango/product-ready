"""
Structured data extractor for Jira export.

Makes a lightweight second LLM call to extract a structured JSON payload
from the product-ready conversation history. This is more reliable than
regex parsing against varied LLM output formats.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

from slack_bot.llm.client import LLMClient, Message

logger = logging.getLogger(__name__)

_EXTRACTION_PROMPT = """\
You are a data extractor. Given a product-ready conversation, extract the \
following as valid JSON — no markdown, no explanation, only the JSON object.

{
  "title": "short feature title (max 10 words)",
  "summary": "2-3 sentence description of what is being built and why",
  "requirements": ["REQ-001: ...", "REQ-002: ..."],
  "stories": [
    {
      "title": "story title (max 12 words)",
      "description": "what the story delivers",
      "acceptance_criteria": "bullet list of acceptance criteria"
    }
  ],
  "metrics": ["success metric 1", "success metric 2"]
}

Rules:
- Extract only what is explicitly in the conversation — do not invent.
- If the conversation has no PRD or stories yet, return:
  {"error": "insufficient_data", "message": "No PRD or stories found in conversation."}
- requirements: include REQ-* and BR-* items if present, otherwise leave empty list.
- stories: include Issue/story breakdowns if present, otherwise leave empty list.
- metrics: include SMART metrics if present, otherwise leave empty list.
"""


@dataclass
class ExtractedPRD:
    title: str
    summary: str
    requirements: list[str] = field(default_factory=list)
    stories: list[dict] = field(default_factory=list)
    metrics: list[str] = field(default_factory=list)

    @property
    def has_stories(self) -> bool:
        return len(self.stories) > 0


def extract_from_conversation(
    messages: list[Message],
    llm: LLMClient,
) -> ExtractedPRD | None:
    """
    Call the LLM to extract structured PRD data from a conversation history.
    Returns None if the conversation has insufficient data.
    """
    if not messages:
        return None

    extraction_messages = list(messages) + [
        {"role": "user", "content": _EXTRACTION_PROMPT}
    ]

    try:
        raw = llm.complete(extraction_messages)
    except Exception as exc:
        logger.exception("LLM extraction failed: %s", exc)
        return None

    # Strip markdown code fences if the model wrapped the JSON
    clean = raw.strip()
    if clean.startswith("```"):
        lines = clean.splitlines()
        clean = "\n".join(
            line for line in lines
            if not line.startswith("```")
        ).strip()

    try:
        data = json.loads(clean)
    except json.JSONDecodeError:
        logger.warning("LLM extraction returned non-JSON: %s", raw[:200])
        return None

    if "error" in data:
        logger.info("Extraction returned insufficient_data: %s", data.get("message"))
        return None

    return ExtractedPRD(
        title=data.get("title", "Untitled Feature"),
        summary=data.get("summary", ""),
        requirements=data.get("requirements", []),
        stories=data.get("stories", []),
        metrics=data.get("metrics", []),
    )
