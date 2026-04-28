"""Tests for the workflow router — intent detection and tier classification."""

import pytest

from slack_bot.workflows.router import Intent, route


class TestTier1ClearIntent:
    def test_prd_keyword(self):
        r = route("write a PRD for the login feature")
        assert r.intent == Intent.PRD
        assert r.tier == 1

    def test_product_requirements(self):
        r = route("product requirements document for onboarding")
        assert r.intent == Intent.PRD
        assert r.tier == 1

    def test_acceptance_criteria(self):
        r = route("define acceptance criteria for checkout")
        assert r.intent == Intent.BEHAVIOR
        assert r.tier == 1

    def test_user_stories(self):
        r = route("write user stories for the notification system")
        assert r.intent == Intent.BEHAVIOR
        assert r.tier == 1

    def test_backlog(self):
        r = route("review my backlog")
        assert r.intent == Intent.BACKLOG
        assert r.tier == 1

    def test_challenge(self):
        r = route("drill me on this feature — what are the risks?")
        assert r.intent == Intent.CHALLENGE
        assert r.tier == 1

    def test_test_spec(self):
        r = route("write test cases for the payment flow")
        assert r.intent == Intent.TEST_SPEC
        assert r.tier == 1

    def test_readiness_check(self):
        r = route("is this feature ready to ship?")
        assert r.intent == Intent.ACCEPTANCE
        assert r.tier == 1

    def test_action_verb_triggers_discovery(self):
        r = route("add export to CSV")
        assert r.intent == Intent.DISCOVERY
        assert r.tier == 1

    def test_build_verb(self):
        r = route("build a search feature")
        assert r.intent == Intent.DISCOVERY
        assert r.tier == 1


class TestTier2DomainKnownTaskUnclear:
    def test_ux_domain(self):
        r = route("I want to improve user experience")
        assert r.tier == 2
        assert r.intent == Intent.DISCOVERY
        assert "UX problem" in r.hint or "problem" in r.hint.lower()

    def test_payment_domain(self):
        r = route("we have issues with payment")
        assert r.tier == 2

    def test_onboarding_domain(self):
        r = route("thinking about our onboarding")
        assert r.tier == 2

    def test_auth_domain(self):
        r = route("something about authentication")
        assert r.tier == 2


class TestTier3NoSignal:
    def test_completely_vague(self):
        r = route("I have an idea")
        assert r.tier == 3
        assert r.intent == Intent.UNKNOWN

    def test_i_need_help(self):
        r = route("I need help")
        assert r.tier == 3

    def test_empty_string(self):
        r = route("")
        assert r.tier == 3

    def test_hello(self):
        r = route("hello")
        assert r.tier == 3


class TestHintContent:
    def test_prd_hint_mentions_questions_first(self):
        r = route("write a PRD")
        assert "question" in r.hint.lower() or "clarif" in r.hint.lower()

    def test_backlog_hint_mentions_guardrails(self):
        r = route("review my backlog")
        assert "guardrail" in r.hint.lower() or "MPD" in r.hint

    def test_tier3_hint_mentions_intro(self):
        r = route("I have an idea")
        assert "Product Ready" in r.hint
