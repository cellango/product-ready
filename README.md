# Product Ready

**The AI-native Spec-Driven Development system for Product Owners.**

[![Version](https://img.shields.io/badge/version-1.2.0-blue)](adapters/anthropic/SKILL.md)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/cellango/product-ready/actions/workflows/ci.yml/badge.svg)](https://github.com/cellango/product-ready/actions)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Positioning

> **Product Ready is AI-native Spec-Driven Development, built on BDD.**

The development chain is explicit:

```
PRD → BDD Spec (THE SPEC) → [AI: Tests + Code] → Acceptance
```

- **PRD** — what must exist, why it matters, how success is measured
- **BDD Spec** — how the system must behave, expressed in Given/When/Then scenarios; this *is* the spec
- **[AI: Tests + Code]** — generated from the BDD Spec, not invented alongside it
- **Acceptance** — validated against the BDD Spec, not developer assumptions

The BDD Spec is the canonical source of truth. It is not written upfront — it is derived from validated discovery, a challenged PRD, and resolved decisions. **Do not generate tests or code from a spec that is ambiguous, incomplete, or not yet challenged.**

---

## What it is

Product Ready is an AI skill for Product Owners. It guides you through a structured workflow — from vague idea to a complete BDD Spec that AI tools can use to generate tests and code — enforcing non-negotiable quality guardrails at every step.

**If it is not testable and measurable, it is not Product Ready.**

It works as a Claude Code skill, an OpenAI system prompt, or a Slack bot with Jira integration.

---

## The problem it solves

Product teams lose weeks to:
- Requirements that can't be tested
- Decisions left as "TBD" until mid-sprint
- Features shipped without success metrics
- Compliance gaps caught too late
- Engineering asking the same clarification questions every cycle

Product Ready catches all of these before work reaches engineering.

---

## How it works

Product Ready uses a single 13-step canonical workflow with **adaptive depth**:

| Depth | When | What you get |
|-------|------|-------------|
| Lightweight | Bug fixes, small changes | Acceptance criteria, no PRD |
| Standard | Most product work | PRD + BDD Spec |
| Full | Compliance, financial, AI, multi-system | Complete lifecycle with Spec Quality Score, security/compliance scenarios |

It auto-escalates when it detects financial, security, compliance, or multi-system signals — no configuration needed.

### 8 non-negotiable guardrails

Every output is checked against:
1. **No Missing Decisions** — flags TBDs before they reach engineering
2. **Testability** — untestable requirements are blocked
3. **No Duplicates or Conflicts** — normalizes conflicting rules to BR-* format
4. **Metric Integrity** — every metric needs baseline, target, timeframe, decision rule
5. **Security & Compliance** — SOC2, NIST, PCI, HIPAA frameworks mapped automatically
6. **UI is First-Class** — all UI states, transitions, and accessibility included
7. **Evidence Over Assumption** — claims are labelled Strong / Medium / Weak
8. **Spec Integrity** — BDD Spec scored Complete / Partial / Incomplete before any AI generation

---

## Quick start: Claude Code

```bash
mkdir -p ~/.claude/skills/product-ready
cp adapters/anthropic/SKILL.md ~/.claude/skills/product-ready/SKILL.md
```

Then type `/product-ready` in Claude Code. The skill detects intent automatically.

### Example inputs

```
"Write a PRD for user login"                 → standard mode, questions before PRD
"Build a payment processing system"          → full mode, compliance questions
"Generate tests from this spec"              → Spec Quality Score + AI prompt blocks
"Review my backlog"                          → guardrails applied, missing decisions flagged
"Score my spec"                              → Spec Quality Score across 5 dimensions
```

---

## Quick start: OpenAI

Use `adapters/openai/system_prompt.txt` as the system prompt for any OpenAI-compatible model (GPT-4o, etc.) or Custom GPT.

---

## Quick start: Slack bot

The Slack bot (`slack_bot/`) is a production implementation with:
- Intent routing across all workflow modes
- Multi-turn conversation context per thread
- **Send to Jira** — exports BDD Spec and stories directly to your Jira project
- Supports Claude (Anthropic) and GPT-4o (OpenAI) — model-agnostic

```bash
# Local dev (Socket Mode — no public URL needed)
cp .env.example .env   # fill in SLACK_BOT_TOKEN, ANTHROPIC_API_KEY, SLACK_APP_TOKEN
make dev

# Production (Hetzner + Ansible)
make provision         # first-time server setup
make deploy            # every push
```

See `infra/` for the full Ansible IaC setup (Nginx, Let's Encrypt, Docker, gunicorn).

---

## Building adapters

All adapter files are generated from `core/`. Do not edit adapter files directly.

```bash
python3 scripts/build.py --validate
```

### Running tests

```bash
pip install pytest pyyaml
python3 -m pytest tests/ -v
```

135 tests across two suites:
- **`tests/test_skill.py`** — 52 structural integrity tests: frontmatter, version, no duplicate sections, three-tier First Interaction rule, all 8 guardrails, Spec-Driven Development model, AI-native extensions, build idempotency
- **`tests/slack/`** — 83 unit tests: LLM client, intent router, thread context, Block Kit renderer, Jira client, Jira extractor, Jira export handler

---

## Repository structure

```
core/
  product-ready-core.md     ← canonical workflow + SDD model (source of truth)
  guardrails.md             ← 8 core guardrails including Spec Integrity
  templates/
    prd-template.md         ← PRD template
    behavior-spec-template.md ← BDD scenario template
    bdd-spec-ai.md          ← AI-optimised BDD Spec template (v1.2.0)

adapters/
  anthropic/SKILL.md        ← Claude Code skill (v1.2.0)
  openai/system_prompt.txt  ← OpenAI system prompt
  slack/PRODUCT_READY.md    ← Reference architecture doc

slack_bot/                  ← Production Slack bot
  handlers/                 ← slash commands, mentions, Jira export
  jira/                     ← Jira REST client + LLM extractor
  blocks/                   ← Block Kit renderer
  context/                  ← Thread context (TTL-based, in-memory)
  llm/                      ← Model-agnostic LLM client

infra/                      ← Ansible IaC for Hetzner
  provision.yml             ← first-time server setup
  deploy.yml                ← rolling deploy
  roles/                    ← common / docker / nginx / product_ready

scripts/
  build.py                  ← generates adapters from core

tests/
  test_skill.py             ← 52 structural integrity tests
  slack/                    ← 83 Slack bot unit tests
```

---

## Current status

| Component | Status | Version / Notes |
|-----------|--------|----------------|
| Claude Code skill (SKILL.md) | ✅ Production | v1.2.0 — AI-native SDD, Spec Quality Score |
| OpenAI system prompt | ✅ Production | Matches Claude Code feature set |
| Slack bot (`slack_bot/`) | ✅ Production | Intent routing, Jira export, multi-turn context |
| Jira integration | ✅ Production | Epic + Story export, BDD Spec → Jira |
| Hetzner deployment (Ansible) | ✅ Production | Nginx, Let's Encrypt, Docker, gunicorn |
| Slack adapter doc (`adapters/slack/`) | 📄 Reference | Architecture reference — see `slack_bot/` for working code |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

The guardrails, escalation triggers, testability rule, Spec Integrity gate, and three-tier First Interaction logic are **protected by policy** — PRs that weaken them will be closed. Everything else is open for contribution.

---

## License

Apache 2.0 — see [LICENSE](LICENSE).
