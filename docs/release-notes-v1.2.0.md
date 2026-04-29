# Release Notes — v1.2.0

**Release date:** 2026-04-28
**Tag:** `v1.2.0`
**Repository:** https://github.com/cellango/product-ready

---

## What's in this release

v1.2.0 completes the Spec-Driven Development pivot started in v1.1.0. Product Ready is now a full AI-native SDD system: the BDD Spec is the canonical source of truth, spec quality is scored before generation, and each scenario produces a ready-to-paste AI prompt.

This release also ships a production Slack bot with Jira integration and full Hetzner deployment infrastructure.

---

## New in v1.2.0

### Spec Quality Score (Guardrail #8 upgraded)

Guardrail #8 is now a structured scoring rubric with five dimensions:

| Dimension | Level |
|-----------|-------|
| Coverage — happy/edge/failure paths present | Critical |
| Clarity — no "should/may/typically" in Then clauses | Critical |
| Linkage — every BS-* linked to REQ-* | Required |
| Decisions — no open [MPD] markers | Required |
| UI states — (if UI involved) | Conditional |

Scores: **Complete** → proceed | **Partial** → fix and re-score | **Incomplete** → STOP.

### Step 5b: Generate from Spec

New optional workflow step that activates on "generate tests", "generate code from spec", or "score my spec":
1. Runs the Spec Quality Score
2. If Complete: formats each BS-* scenario as a self-contained AI generation prompt
3. Outputs one ready-to-paste block per scenario

### BDD Spec → AI Prompt Mapping

New section in the core workflow with three rules and before/after examples:
- Then clauses must be exact and observable (not "should", "may", "typically")
- One behaviour per scenario — never bundle multiple assertions
- State all preconditions explicitly — AI tools have no knowledge of your system

### AI-optimised BDD Spec template (`core/templates/bdd-spec-ai.md`)

New template covering all five scenario types (happy path, edge case, failure, security, UI state) with:
- Embedded AI generation prompt blocks (copy-paste ready)
- Spec Quality Score checklist built in

### New trigger phrases

The skill now activates on: `generate tests`, `generate code from spec`, `score my spec`, `spec quality`, `BDD spec`, `spec-driven development`.

---

## New in v1.1.0 (included in this release)

- **Guardrail #8: Spec Integrity** — explicit STOP gate before test/code generation
- **Step 5 renamed** from "Behavior Spec (BDD)" to "BDD Spec (THE SPEC)" — BDD implicit in the name
- **Spec-Driven Development Model section** added to core workflow
- **Version bumped** 1.0.0 → 1.1.0
- **10 new structural tests**

---

## Production infrastructure (Phase 2–3)

This release includes the full Slack + Jira production stack:

### Slack bot (`slack_bot/`)
- Model-agnostic LLM client (Anthropic / OpenAI)
- Intent router with three-tier First Interaction logic
- Thread-aware conversation context (TTL=30min, in-memory)
- Block Kit renderer with structured artifact display
- Slash commands: `/product-ready`, `/prd`, `/behavior`, `/backlog`

### Jira integration
- LLM-based PRD extraction from Slack thread history
- Jira REST API v3 client (Atlassian Document Format)
- Epic + Story creation linked to parent
- "Send to Jira" button on PRD/backlog/behavior responses

### Hetzner deployment (`infra/`)
- Ansible provision + deploy playbooks (4 roles: common / docker / nginx / product_ready)
- Nginx TLS proxy with Let's Encrypt (auto-renew daily)
- gunicorn production server with `/health` endpoint
- Ansible Vault for secrets
- `make dev` / `make provision` / `make deploy` / `make logs`

---

## Test coverage

| Suite | Tests | Coverage |
|-------|-------|---------|
| `tests/test_skill.py` | 52 | Structural integrity: frontmatter, guardrails, SDD model, AI-native extensions, build idempotency |
| `tests/slack/` | 83 | LLM client, router, thread context, Block Kit, Jira client, extractor, export handler |
| **Total** | **135** | **All passing** |

---

## Breaking changes

None. All changes are additive.

---

## Upgrade from v1.0.0

```bash
# Update installed Claude Code skill
cp adapters/anthropic/SKILL.md ~/.claude/skills/product-ready/SKILL.md
```

---

## What's next (v1.3.0 candidates)

- Redis-backed thread context (survives restarts, enables horizontal scaling)
- Linear integration alongside Jira
- Multi-workspace Slack support
- Spec completeness reports exported as PDF
