"""
Workflow router.

Maps user input to a workflow intent using the same three-tier logic as the
SKILL.md First Interaction rule. Returns an intent label and an optional
pre-filled system hint to steer the LLM toward the right workflow step.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class Intent(str, Enum):
    DISCOVERY = "discovery"
    PRD = "prd"
    BEHAVIOR = "behavior"
    BACKLOG = "backlog"
    CHALLENGE = "challenge"
    TEST_SPEC = "test_spec"
    ACCEPTANCE = "acceptance"
    UNKNOWN = "unknown"


# --- keyword maps ---------------------------------------------------------- #

_PRD_PATTERNS = re.compile(
    r"\b(prd|product requirements? doc(ument)?|write (a |the )?requirements?|"
    r"spec(ification)?|document (the )?feature)\b",
    re.I,
)
_BEHAVIOR_PATTERNS = re.compile(
    r"\b(acceptance criteria|behavior spec|given.when.then|bdd|"
    r"user stor(y|ies)|scenarios?)\b",
    re.I,
)
_BACKLOG_PATTERNS = re.compile(
    r"\b(backlog|review (my |these |the )?stories|prioriti[sz]e|"
    r"rank (the )?work|sprint planning)\b",
    re.I,
)
_CHALLENGE_PATTERNS = re.compile(
    r"\b(challenge|drill.?me|critique|poke holes?|what.s wrong|risk(s)?|"
    r"assumptions?|push.?back)\b",
    re.I,
)
_TEST_PATTERNS = re.compile(
    r"\b(test (cases?|spec|plan)|TS-\d+|automated? tests?|qa plan)\b",
    re.I,
)
_ACCEPTANCE_PATTERNS = re.compile(
    r"\b(is (this |it |the \w+ )?ready|ready to (ship|launch|release|deploy)|"
    r"readiness (check|review)|done criteria|definition of done)\b",
    re.I,
)

# domain words that signal "domain known, task unclear" (Tier 2)
_DOMAIN_WORDS = re.compile(
    r"\b(ux|user experience|performance|onboarding|search|checkout|"
    r"login|auth(entication)?|payment|notification|dashboard|report|"
    r"mobile|api|integration|workflow|approval|compliance)\b",
    re.I,
)

# explicit task words — if present the intent is clear (Tier 1)
# "improve" is intentionally excluded: "improve X" names a domain, not a task
_TASK_WORDS = re.compile(
    r"\b(add|build|create|write|define|review|fix|generate|"
    r"export|design|implement|show|list|explain)\b",
    re.I,
)


@dataclass
class RouteResult:
    intent: Intent
    tier: int          # 1=clear, 2=domain known, 3=no signal
    hint: str          # prepended to user message for the LLM


def route(text: str) -> RouteResult:
    """
    Determine the workflow intent and interaction tier from raw user text.
    Mirrors the three-tier First Interaction rule in core/product-ready-core.md.
    """
    t = text.strip()

    # --- Tier 1: explicit intent ------------------------------------------ #
    if _PRD_PATTERNS.search(t):
        return RouteResult(Intent.PRD, 1, "[Workflow: PRD] Start with clarifying questions before drafting.")
    if _BEHAVIOR_PATTERNS.search(t):
        return RouteResult(Intent.BEHAVIOR, 1, "[Workflow: Behavior Spec] Ask which feature before generating scenarios.")
    if _BACKLOG_PATTERNS.search(t):
        return RouteResult(Intent.BACKLOG, 1, "[Workflow: Backlog Review] Apply all 7 guardrails. Flag missing decisions with [MPD].")
    if _CHALLENGE_PATTERNS.search(t):
        return RouteResult(Intent.CHALLENGE, 1, "[Workflow: Challenge] Critically evaluate assumptions and risks.")
    if _TEST_PATTERNS.search(t):
        return RouteResult(Intent.TEST_SPEC, 1, "[Workflow: Test Spec] Convert behavior into test cases with automation levels.")
    if _ACCEPTANCE_PATTERNS.search(t):
        return RouteResult(Intent.ACCEPTANCE, 1, "[Workflow: Acceptance] Check all Must scenarios, tests, defects, and UI/UX.")
    if _TASK_WORDS.search(t):
        return RouteResult(Intent.DISCOVERY, 1, "[Workflow: Discovery] Start with fast-mode clarifying questions.")

    # --- Tier 2: domain known, task unclear -------------------------------- #
    if _DOMAIN_WORDS.search(t):
        domain = _DOMAIN_WORDS.search(t).group(0)
        return RouteResult(
            Intent.DISCOVERY,
            2,
            f"[Workflow: Discovery] The user mentioned '{domain}' but hasn't stated a task. "
            f"Ask what specific problem they're trying to solve — not which workflow step they want.",
        )

    # --- Tier 3: no signal ------------------------------------------------- #
    return RouteResult(
        Intent.UNKNOWN,
        3,
        "[Workflow: Unknown] Introduce Product Ready in one sentence, then ask one question: "
        "'What are you working on — an idea, a PRD, acceptance criteria, or a backlog review?'",
    )
