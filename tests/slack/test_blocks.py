"""Tests for the Block Kit renderer."""

import pytest

from slack_bot.blocks.renderer import render_response, _chunk
from slack_bot.workflows.router import Intent


class TestPlainText:
    def test_short_text_returns_single_section(self):
        blocks = render_response("Here is a quick answer.", Intent.UNKNOWN)
        assert len(blocks) == 1
        assert blocks[0]["type"] == "section"
        assert "quick answer" in blocks[0]["text"]["text"]

    def test_long_text_is_chunked(self):
        long_text = "word " * 700  # ~3500 chars > 3000 limit
        blocks = render_response(long_text, Intent.UNKNOWN)
        assert len(blocks) >= 2
        for b in blocks:
            assert len(b["text"]["text"]) <= 3000


class TestQuestionBlocks:
    def test_numbered_questions_render_as_clean_list(self):
        text = "Before I write this, a few questions:\n1. Who are the users?\n2. What does success look like?\n3. Any compliance constraints?"
        blocks = render_response(text, Intent.PRD)
        full_text = " ".join(
            b["text"]["text"] for b in blocks if b.get("type") == "section"
        )
        assert "Who are the users" in full_text
        assert "success" in full_text

    def test_preamble_is_preserved(self):
        text = "Before I write this, a few questions:\n1. Who uses this?\n2. What's the goal?"
        blocks = render_response(text, Intent.PRD)
        texts = [b["text"]["text"] for b in blocks if b.get("type") == "section"]
        combined = " ".join(texts)
        assert "Before I write" in combined


class TestMPDBlocks:
    def test_mpd_flags_appear_as_red_circles(self):
        text = "[MPD] Who approves the invoice?\n[MPD] What happens on timeout?\nHere is the rest of the analysis."
        blocks = render_response(text, Intent.BACKLOG)
        mpd_block = next((b for b in blocks if "MPD" in b.get("text", {}).get("text", "")), None)
        assert mpd_block is not None
        assert ":red_circle:" in mpd_block["text"]["text"]
        assert "Who approves" in mpd_block["text"]["text"]
        assert "timeout" in mpd_block["text"]["text"]

    def test_non_mpd_text_still_rendered(self):
        text = "[MPD] Missing decision.\nHere is the backlog review."
        blocks = render_response(text, Intent.BACKLOG)
        all_text = " ".join(
            b.get("text", {}).get("text", "") for b in blocks
        )
        assert "backlog review" in all_text

    def test_divider_follows_mpd_block(self):
        text = "[MPD] Something missing.\nRest of response."
        blocks = render_response(text, Intent.BACKLOG)
        mpd_idx = next(
            i for i, b in enumerate(blocks)
            if "MPD" in b.get("text", {}).get("text", "")
        )
        assert blocks[mpd_idx + 1]["type"] == "divider"


class TestStructuredArtifacts:
    def test_markdown_headers_become_header_blocks(self):
        text = "## Goals\nIncrease adoption.\n## Requirements\nREQ-001: Users can export."
        blocks = render_response(text, Intent.PRD)
        header_blocks = [b for b in blocks if b["type"] == "header"]
        assert len(header_blocks) == 2
        header_texts = [b["text"]["text"] for b in header_blocks]
        assert "Goals" in header_texts
        assert "Requirements" in header_texts

    def test_req_reference_triggers_structured_render(self):
        text = "REQ-001: The user can log in.\nREQ-002: Session expires after 30 minutes."
        blocks = render_response(text, Intent.PRD)
        all_text = " ".join(b.get("text", {}).get("text", "") for b in blocks)
        assert "REQ-001" in all_text


class TestChunk:
    def test_short_text_not_chunked(self):
        assert _chunk("hello", 3000) == ["hello"]

    def test_splits_at_paragraph_boundary(self):
        text = "A" * 1500 + "\n\n" + "B" * 1500
        chunks = _chunk(text, 3000)
        assert len(chunks) == 2

    def test_all_content_preserved(self):
        text = "word " * 1000
        chunks = _chunk(text, 500)
        combined = " ".join(chunks).replace("  ", " ")
        assert len(combined) >= len(text) - 10  # allow minimal whitespace loss
