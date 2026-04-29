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
    "Spec Integrity",
    "Acceptance Coverage Rule",
    "Bidirectional Traceability Rule",
    "Scenario Completeness Rule",
    "No Ambiguity Rule",
    "Automation Readiness Rule",
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
# Spec-Driven Development model integrity
# ---------------------------------------------------------------------------

class TestSpecDrivenDevelopment:
    def test_sdd_model_section_in_core(self):
        text = CORE_MD.read_text()
        assert "Spec-Driven Development Model" in text, \
            "core/product-ready-core.md missing 'Spec-Driven Development Model' section"

    def test_bdd_spec_the_spec_in_core(self):
        text = CORE_MD.read_text()
        assert "BDD Spec (THE SPEC)" in text, \
            "core/product-ready-core.md must name Step 5 'BDD Spec (THE SPEC)'"

    def test_sdd_chain_in_core(self):
        text = CORE_MD.read_text()
        assert "PRD → BDD Spec (THE SPEC)" in text, \
            "core/product-ready-core.md missing the SDD chain"

    def test_spec_integrity_stop_instruction_in_core(self):
        text = CORE_MD.read_text()
        assert "STOP" in text, \
            "Spec Integrity guardrail must contain explicit STOP instruction"

    def test_bdd_spec_the_spec_in_skill_md(self):
        text = SKILL_MD.read_text()
        assert "BDD Spec (THE SPEC)" in text, \
            "SKILL.md must reference 'BDD Spec (THE SPEC)'"

    def test_spec_driven_trigger_phrase_in_skill_md(self):
        text = SKILL_MD.read_text()
        assert "spec-driven development" in text.lower(), \
            "SKILL.md trigger phrases missing 'spec-driven development'"

    def test_spec_integrity_in_openai_prompt(self):
        text = OPENAI_PROMPT.read_text()
        assert "Spec Integrity" in text, \
            "OpenAI system_prompt.txt missing 'Spec Integrity' guardrail"

    def test_sdd_chain_in_openai_prompt(self):
        text = OPENAI_PROMPT.read_text()
        assert "BDD Spec (THE SPEC)" in text, \
            "OpenAI system_prompt.txt missing the SDD chain"

    def test_version_bumped_to_1_3_0(self):
        fm = parse_frontmatter(SKILL_MD)
        assert str(fm.get("version")) == "1.3.0", \
            f"Expected version 1.3.0 for Phase 4 release, got {fm.get('version')}"


# ---------------------------------------------------------------------------
# Phase 3 — AI-native extensions integrity
# ---------------------------------------------------------------------------

AI_TEMPLATE = ROOT / "core/templates/bdd-spec-ai.md"


class TestAINativeExtensions:
    def test_bdd_ai_prompt_mapping_section_in_core(self):
        assert "BDD Spec → AI Prompt Mapping" in CORE_MD.read_text(), \
            "core/product-ready-core.md missing 'BDD Spec → AI Prompt Mapping' section"

    def test_then_clause_rules_in_core(self):
        text = CORE_MD.read_text()
        # Rules forbid "should", "may", "typically" in Then clauses
        assert "should" in text and "may" in text and "typically" in text, \
            "core/product-ready-core.md missing Then clause vague-language rules"

    def test_generate_from_spec_step_in_core(self):
        assert "Generate from Spec" in CORE_MD.read_text(), \
            "core/product-ready-core.md missing 'Generate from Spec' step (5b)"

    def test_spec_quality_score_in_guardrails(self):
        assert "Spec Quality Score" in (ROOT / "core/guardrails.md").read_text(), \
            "core/guardrails.md missing 'Spec Quality Score' rubric"

    def test_quality_score_dimensions_in_guardrails(self):
        text = (ROOT / "core/guardrails.md").read_text()
        for dimension in ["Coverage", "Clarity", "Linkage", "Decisions"]:
            assert dimension in text, \
                f"core/guardrails.md Spec Quality Score missing dimension: '{dimension}'"

    def test_complete_partial_incomplete_scoring_in_guardrails(self):
        text = (ROOT / "core/guardrails.md").read_text()
        for score in ["Complete", "Partial", "Incomplete"]:
            assert score in text, \
                f"core/guardrails.md Spec Quality Score missing score level: '{score}'"

    def test_ai_template_file_exists(self):
        assert AI_TEMPLATE.exists(), \
            "core/templates/bdd-spec-ai.md does not exist"

    def test_ai_template_has_quality_score_checklist(self):
        assert "Spec Quality Score" in AI_TEMPLATE.read_text(), \
            "bdd-spec-ai.md must embed the Spec Quality Score checklist"

    def test_generate_trigger_phrase_in_skill_md(self):
        text = SKILL_MD.read_text()
        assert "generate tests" in text.lower() or "generate from spec" in text.lower(), \
            "SKILL.md trigger phrases missing generation intent triggers"

    def test_spec_quality_score_in_openai_prompt(self):
        assert "Spec Quality Score" in OPENAI_PROMPT.read_text(), \
            "OpenAI system_prompt.txt missing 'Spec Quality Score'"

    def test_bdd_ai_prompt_rules_in_openai_prompt(self):
        text = OPENAI_PROMPT.read_text()
        assert "BDD SPEC" in text.upper() and "AI PROMPT" in text.upper(), \
            "OpenAI system_prompt.txt missing BDD→AI Prompt rules section"


# ---------------------------------------------------------------------------
# Phase 4 — Coverage, Traceability, and BDD Quality guardrails
# ---------------------------------------------------------------------------

RTM_TEMPLATE = ROOT / "core/templates/rtm-lite.md"
GUARDRAILS_MD = ROOT / "core/guardrails.md"


class TestCoverageAndTraceability:
    # --- Guardrail #9: Acceptance Coverage Rule ---

    def test_acceptance_coverage_rule_in_guardrails(self):
        assert "Acceptance Coverage Rule" in GUARDRAILS_MD.read_text(), \
            "core/guardrails.md missing Guardrail #9: Acceptance Coverage Rule"

    def test_acceptance_coverage_requires_bs_and_ts(self):
        text = GUARDRAILS_MD.read_text()
        assert "BS-*" in text and "TS-*" in text, \
            "Acceptance Coverage Rule must reference both BS-* and TS-* linkage"

    def test_acceptance_coverage_rule_in_skill_md(self):
        assert "Acceptance Coverage Rule" in SKILL_MD.read_text(), \
            "SKILL.md missing Acceptance Coverage Rule (Guardrail #9)"

    # --- Guardrail #10: Bidirectional Traceability ---

    def test_bidirectional_traceability_in_guardrails(self):
        assert "Bidirectional Traceability Rule" in GUARDRAILS_MD.read_text(), \
            "core/guardrails.md missing Guardrail #10: Bidirectional Traceability Rule"

    def test_rtm_lite_mentioned_in_guardrails(self):
        assert "RTM-lite" in GUARDRAILS_MD.read_text(), \
            "core/guardrails.md missing RTM-lite matrix in Guardrail #10"

    def test_orphan_detection_in_guardrails(self):
        assert "orphan" in GUARDRAILS_MD.read_text().lower(), \
            "Bidirectional Traceability Rule must include orphan detection"

    def test_rtm_template_exists(self):
        assert RTM_TEMPLATE.exists(), \
            "core/templates/rtm-lite.md does not exist"

    def test_rtm_template_has_coverage_matrix(self):
        text = RTM_TEMPLATE.read_text()
        assert "REQ-*" in text and "BS-*" in text and "TS-*" in text, \
            "rtm-lite.md must contain REQ-*/BS-*/TS-* traceability table"

    def test_rtm_template_has_orphan_detection(self):
        assert "Orphan" in RTM_TEMPLATE.read_text(), \
            "rtm-lite.md must include an Orphan Detection section"

    def test_rtm_template_has_coverage_summary(self):
        assert "Coverage Summary" in RTM_TEMPLATE.read_text(), \
            "rtm-lite.md must include a Coverage Summary section"

    def test_coverage_validation_step_in_core(self):
        assert "Coverage Validation" in CORE_MD.read_text(), \
            "core/product-ready-core.md missing Coverage Validation step"

    def test_rtm_trigger_phrases_in_skill_md(self):
        text = SKILL_MD.read_text().lower()
        assert "check coverage" in text or "traceability matrix" in text or "rtm" in text, \
            "SKILL.md trigger phrases missing coverage/RTM intent triggers"

    def test_coverage_validation_in_openai_prompt(self):
        text = OPENAI_PROMPT.read_text()
        assert "RTM" in text or "traceability" in text.lower(), \
            "OpenAI system_prompt.txt missing RTM/traceability guidance"

    # --- Guardrail #11: Scenario Completeness Rule ---

    def test_scenario_completeness_rule_in_guardrails(self):
        assert "Scenario Completeness Rule" in GUARDRAILS_MD.read_text(), \
            "core/guardrails.md missing Guardrail #11: Scenario Completeness Rule"

    def test_scenario_completeness_requires_three_types(self):
        text = GUARDRAILS_MD.read_text()
        # All three scenario types must be required per REQ-*
        assert "happy path" in text.lower() and "failure" in text.lower() and "edge case" in text.lower(), \
            "Scenario Completeness Rule must require happy path, failure, and edge case per REQ-*"

    # --- Guardrail #12: No Ambiguity Rule ---

    def test_no_ambiguity_rule_in_guardrails(self):
        assert "No Ambiguity Rule" in GUARDRAILS_MD.read_text(), \
            "core/guardrails.md missing Guardrail #12: No Ambiguity Rule"

    def test_no_ambiguity_banned_terms_listed(self):
        text = GUARDRAILS_MD.read_text()
        # Must list banned vague terms
        assert "user-friendly" in text and "seamless" in text, \
            "No Ambiguity Rule must list banned vague terms (user-friendly, seamless, etc.)"

    def test_no_ambiguity_in_openai_prompt(self):
        text = OPENAI_PROMPT.read_text()
        assert "user-friendly" in text or "No Ambiguity" in text, \
            "OpenAI system_prompt.txt missing No Ambiguity Rule content"

    # --- Guardrail #13: Automation Readiness Rule ---

    def test_automation_readiness_rule_in_guardrails(self):
        assert "Automation Readiness Rule" in GUARDRAILS_MD.read_text(), \
            "core/guardrails.md missing Guardrail #13: Automation Readiness Rule"

    def test_automation_readiness_has_classifications(self):
        text = GUARDRAILS_MD.read_text()
        assert "Automatable" in text and "Manual only" in text, \
            "Automation Readiness Rule must define Automatable and Manual only classifications"

    def test_automation_readiness_threshold_defined(self):
        text = GUARDRAILS_MD.read_text()
        # Must define the 80% threshold
        assert "80%" in text, \
            "Automation Readiness Rule must define the ≥80% Automation Ready threshold"

    def test_automation_readiness_in_bdd_template(self):
        text = (ROOT / "core/templates/bdd-spec-ai.md").read_text()
        assert "Automation Readiness" in text or "Automation Ready" in text, \
            "bdd-spec-ai.md must include Automation Readiness classification"

    # --- Guardrail #8 extended — new dimensions ---

    def test_observability_dimension_in_guardrails(self):
        assert "Observability" in GUARDRAILS_MD.read_text(), \
            "core/guardrails.md Guardrail #8 missing Observability dimension"

    def test_example_data_dimension_in_guardrails(self):
        text = GUARDRAILS_MD.read_text()
        assert "Example data" in text or "example data" in text, \
            "core/guardrails.md Guardrail #8 missing Example data dimension"

    def test_observability_dimension_in_bdd_template(self):
        text = (ROOT / "core/templates/bdd-spec-ai.md").read_text()
        assert "Observability" in text, \
            "bdd-spec-ai.md Spec Quality Score missing Observability dimension"

    def test_bdd_template_has_test_data_field(self):
        text = (ROOT / "core/templates/bdd-spec-ai.md").read_text()
        assert "Test data" in text, \
            "bdd-spec-ai.md must include Test data field in each scenario"

    def test_bdd_template_has_pass_fail_conditions(self):
        text = (ROOT / "core/templates/bdd-spec-ai.md").read_text()
        assert "Pass condition" in text and "Fail condition" in text, \
            "bdd-spec-ai.md must include explicit Pass condition and Fail condition fields"

    def test_acceptance_gate_references_coverage_in_core(self):
        text = CORE_MD.read_text()
        # Step 10 (Acceptance) must reference the coverage/RTM guardrails
        assert "RTM-lite" in text or "Coverage Gap" in text or "Acceptance Coverage" in text, \
            "core/product-ready-core.md Step 10 (Acceptance) must reference coverage requirements"


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
