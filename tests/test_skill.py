"""
Structural and integrity tests for product-ready skill artifacts.

These tests verify that:
- The build system produces correct output from the core sources
- SKILL.md has required metadata (name, version, description)
- The three-tier First Interaction rule is present in all adapters
- No duplicate sections exist in SKILL.md
- The Slack adapter is clearly labelled as reference architecture
- The build is idempotent (running twice produces identical output)
"""

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
SKILL_MD = ROOT / "adapters/anthropic/SKILL.md"
OPENAI_PROMPT = ROOT / "adapters/openai/system_prompt.txt"
SLACK_MD = ROOT / "adapters/slack/PRODUCT_READY.md"
CORE_MD = ROOT / "core/product-ready-core.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(path: Path) -> dict:
    text = path.read_text()
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return {}
    end = next(i for i, l in enumerate(lines[1:], 1) if l.strip() == "---")
    return yaml.safe_load("\n".join(lines[1:end]))


def count_occurrences(path: Path, needle: str) -> int:
    return path.read_text().count(needle)


def run_build() -> str:
    result = subprocess.run(
        [sys.executable, "scripts/build.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Build failed:\n{result.stderr}"
    return result.stdout + result.stderr


# ---------------------------------------------------------------------------
# SKILL.md — frontmatter
# ---------------------------------------------------------------------------

class TestSkillFrontmatter:
    def test_has_name(self):
        fm = parse_frontmatter(SKILL_MD)
        assert fm.get("name") == "product-ready"

    def test_has_version(self):
        fm = parse_frontmatter(SKILL_MD)
        assert "version" in fm, "SKILL.md frontmatter must include 'version'"

    def test_version_is_semver(self):
        fm = parse_frontmatter(SKILL_MD)
        version = str(fm.get("version", ""))
        parts = version.split(".")
        assert len(parts) == 3 and all(p.isdigit() for p in parts), \
            f"version must be semver (e.g. 1.0.0), got: {version}"

    def test_has_description(self):
        fm = parse_frontmatter(SKILL_MD)
        assert fm.get("description"), "SKILL.md frontmatter must include 'description'"


# ---------------------------------------------------------------------------
# SKILL.md — no duplicate sections
# ---------------------------------------------------------------------------

class TestSkillNoDuplicates:
    def test_single_first_interaction(self):
        count = count_occurrences(SKILL_MD, "## First Interaction")
        assert count == 1, f"Expected 1 'First Interaction' section, found {count}"

    def test_single_default_behavior(self):
        count = count_occurrences(SKILL_MD, "## Default Behavior")
        assert count == 1, f"Expected 1 'Default Behavior' section, found {count}"

    def test_single_execution_modes_in_guardrails(self):
        count = count_occurrences(SKILL_MD, "## Execution Modes")
        assert count == 1, f"Expected 1 'Execution Modes' section, found {count}"


# ---------------------------------------------------------------------------
# Three-tier First Interaction rule — all adapters
# ---------------------------------------------------------------------------

THREE_TIER_MARKERS = [
    "Intent clear",
    "Domain known, task unclear",
    "No signal",
]


class TestThreeTierRule:
    @pytest.mark.parametrize("marker", THREE_TIER_MARKERS)
    def test_skill_md_has_marker(self, marker):
        assert marker in SKILL_MD.read_text(), \
            f"SKILL.md missing three-tier marker: '{marker}'"

    @pytest.mark.parametrize("marker", THREE_TIER_MARKERS)
    def test_openai_prompt_has_marker(self, marker):
        assert marker in OPENAI_PROMPT.read_text(), \
            f"OpenAI system_prompt.txt missing three-tier marker: '{marker}'"

    @pytest.mark.parametrize("marker", THREE_TIER_MARKERS)
    def test_core_has_marker(self, marker):
        assert marker in CORE_MD.read_text(), \
            f"core/product-ready-core.md missing three-tier marker: '{marker}'"


# ---------------------------------------------------------------------------
# Slack adapter — reference architecture label
# ---------------------------------------------------------------------------

class TestSlackAdapterLabel:
    def test_has_status_label(self):
        text = SLACK_MD.read_text()
        assert "Reference Architecture" in text or "Not Yet Implemented" in text, \
            "Slack adapter must carry a 'Reference Architecture / Not Yet Implemented' label"


# ---------------------------------------------------------------------------
# Core guardrails integrity
# ---------------------------------------------------------------------------

REQUIRED_GUARDRAILS = [
    "No Missing Decisions",
    "Testability Rule",
    "No Duplicates or Conflicts",
    "Metric Integrity",
    "Security & Compliance",
    "UI is First-Class",
    "Evidence Over Assumption",
]


class TestGuardrailsIntegrity:
    @pytest.mark.parametrize("guardrail", REQUIRED_GUARDRAILS)
    def test_guardrail_present_in_skill(self, guardrail):
        assert guardrail in SKILL_MD.read_text(), \
            f"SKILL.md missing guardrail: '{guardrail}'"


# ---------------------------------------------------------------------------
# Escalation triggers integrity
# ---------------------------------------------------------------------------

REQUIRED_ESCALATION_TRIGGERS = [
    "Risk level increases",
    "Compliance requirements apply",
    "Multiple systems involved",
    "High user impact",
    "Ambiguity detected",
]


class TestEscalationTriggers:
    @pytest.mark.parametrize("trigger", REQUIRED_ESCALATION_TRIGGERS)
    def test_escalation_trigger_present(self, trigger):
        assert trigger in SKILL_MD.read_text(), \
            f"SKILL.md missing escalation trigger: '{trigger}'"


# ---------------------------------------------------------------------------
# Build idempotency
# ---------------------------------------------------------------------------

class TestBuildIdempotency:
    def test_build_is_idempotent(self):
        run_build()
        snapshot_skill = SKILL_MD.read_text()
        snapshot_openai = OPENAI_PROMPT.read_text()

        run_build()
        assert SKILL_MD.read_text() == snapshot_skill, \
            "SKILL.md content changed between two consecutive builds (not idempotent)"
        assert OPENAI_PROMPT.read_text() == snapshot_openai, \
            "system_prompt.txt content changed between two consecutive builds (not idempotent)"

    def test_build_exits_zero(self):
        run_build()  # asserts returncode == 0 internally
