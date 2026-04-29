# Product Ready

**The AI-native Spec-Driven Development system for Product Owners.**

[![Version](https://img.shields.io/badge/version-1.5.0-blue)](adapters/anthropic/SKILL.md)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/cellango/product-ready/actions/workflows/ci.yml/badge.svg)](https://github.com/cellango/product-ready/actions)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Positioning

> **Product Ready is AI-native Spec-Driven Development, built on BDD.**

The development chain is explicit:

```
OKR → PRD → BDD Spec (THE SPEC) → [AI: Tests + Code] → Acceptance
```

- **OKR** — the objective and key result this work must move; declared before the PRD is written
- **PRD** — what must exist, why it matters, how success is measured, linked to a Key Result
- **BDD Spec** — how the system must behave, expressed in Given/When/Then scenarios; this *is* the spec
- **[AI: Tests + Code]** — generated from the BDD Spec, not invented alongside it
- **Acceptance** — validated against the BDD Spec and the RTM-lite coverage matrix, not developer assumptions

The BDD Spec is the canonical source of truth. It is not written upfront — it is derived from validated discovery, a challenged PRD, and resolved decisions. **Do not generate tests or code from a spec that is ambiguous, incomplete, or not yet challenged.**

---

## What it is

Product Ready is an AI skill for Product Owners. It guides you through a structured workflow — from vague idea to a complete BDD Spec that AI tools can use to generate tests and code — enforcing non-negotiable quality guardrails at every step.

**If it is not testable, measurable, and linked to a Key Result, it is not Product Ready.**

It works as a Claude Code skill, an OpenAI system prompt, or a Slack bot with Jira integration.

---

## The problem it solves

Product teams lose weeks to:
- Requirements that can't be tested
- Decisions left as "TBD" until mid-sprint
- Features shipped without success metrics
- OKR linkage that is decorative, not causal
- Specs that are incomplete when handed to AI code generation tools
- Requirements with no linked test cases — gaps caught after build, not before
- Engineering asking the same clarification questions every cycle
- Compliance gaps caught too late

Product Ready catches all of these before work reaches engineering.

---

## How it works

Product Ready uses a single 13-step canonical workflow with **adaptive depth**:

| Depth | When | What you get |
|-------|------|-------------|
| Lightweight | Bug fixes, small changes | Acceptance criteria, no PRD |
| Standard | Most product work | PRD + BDD Spec |
| Full | Compliance, financial, AI, multi-system | Complete lifecycle with Spec Quality Score, RTM-lite, OKR linkage, security/compliance scenarios |

It auto-escalates when it detects financial, security, compliance, or multi-system signals — no configuration needed.

---

### 18 non-negotiable guardrails

Every output is checked against:

**Spec quality**
1. **No Missing Decisions** — flags TBDs before they reach engineering
2. **Testability** — untestable requirements are blocked
3. **No Duplicates or Conflicts** — normalizes conflicting rules to BR-* format
4. **Metric Integrity** — every metric needs baseline, target, timeframe, decision rule
5. **Security & Compliance** — SOC2, NIST, PCI, HIPAA frameworks mapped automatically
6. **UI is First-Class** — all UI states, transitions, and accessibility included
7. **Evidence Over Assumption** — claims are labelled Strong / Medium / Weak
8. **Spec Integrity** — BDD Spec scored across 7 dimensions before any AI generation is allowed

**Coverage & traceability**
9. **Acceptance Coverage Rule** — every REQ-* must link to at least one BS-* and one TS-*; blocks acceptance if any gap exists
10. **Bidirectional Traceability** — RTM-lite enforces REQ→BS→TS forward trace and TS→BS→REQ backward trace; orphan detection on every BS-* and TS-*
11. **Scenario Completeness** — each REQ-* must have a happy path, a failure scenario, and an edge case before the spec is considered complete

**BDD quality**
12. **No Ambiguity** — bans "should", "user-friendly", "fast", "seamless" and similar terms in requirements and Then clauses; requires measurable replacements
13. **Automation Readiness** — every scenario classified as Automatable / Partially automatable / Manual only; flags Automation Risk when <50% are automatable

**OKR alignment**
14. **OKR Alignment Rule** — every PRD must declare an Objective (OBJ-*) and Key Result (KR-*) with a falsifiable contribution hypothesis and validation plan before proceeding to the BDD Spec; OKR decoration is explicitly rejected

**Prioritization**
15. **Prioritization Justification Rule** — every prioritization decision must answer: why now, what value, what is NOT being done, and what is the consequence of delay; ranked lists without reasoning are blocked
16. **Trade-off Declaration** — every priority decision must document what was deprioritized, why, what risk is accepted, and what event would trigger re-prioritization
17. **Prioritization Gate** — Strategic prioritization must pass before a PRD is written; Delivery prioritization must pass before Issues are created; bypassing the gates is the most expensive anti-pattern in product development
18. **Re-prioritization Trigger** — priorities are not permanent; mandatory re-scoring when data changes, effort changes by >50%, a KR moves unexpectedly, a competitor ships, or a compliance risk is identified post-prioritization

---

### Spec Quality Score (Guardrail #8)

Before generating tests or code, the spec is scored across 7 dimensions:

| Dimension | What it checks | Level |
|-----------|----------------|-------|
| **Coverage** | Happy paths, edge cases, and failure paths all present | Critical |
| **Clarity** | No "should", "may", "typically" in Then clauses | Critical |
| **Observability** | Every Then clause names a system layer: UI / API / DB / log / event | Required |
| **Linkage** | Every BS-* linked to at least one REQ-* | Required |
| **Decisions** | No open [MPD] markers remaining | Required |
| **Example data** | Every scenario includes concrete values — not "a user", not placeholder X | Required |
| **UI** | All UI states defined (conditional — only if UI is involved) | Conditional |

**Complete** → all Critical + all Required pass → proceed to generation
**Partial** → one or more Required fail → fix and re-score
**Incomplete** → one or more Critical fail → STOP

---

### Multi-Level Prioritization (Guardrails #15–#18)

Prioritization runs at three gates — not as a single step at the end.

| Level | Gate | Question answered | Framework |
|-------|------|-------------------|-----------|
| **Strategic** | Before Discovery (Step 1b) | Should we work on this problem at all? | Weighted scoring: strategic alignment, customer impact, business value, confidence |
| **Solution** | Before PRD (Step 3b) | Which approach and scope should we pursue? | MoSCoW triage + option scoring |
| **Delivery** | Before Issues (Step 7) | What do we build first within confirmed scope? | RICE / WSJF / ICE scored backlog |

**The anti-pattern this prevents:** Writing a full PRD for work that hasn't been strategically approved — the most expensive anti-pattern in product development.

Every prioritization decision must produce:
1. A justification answering *why now, what value, what NOT doing, consequence of delay*
2. A trade-off declaration for everything that was deprioritized
3. A re-prioritization trigger — conditions under which the priority must be re-evaluated

See `core/templates/prioritization.md` for the complete three-level template.

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
"Score my spec"                              → Spec Quality Score across 7 dimensions
"Check coverage"                             → RTM-lite, coverage gaps, orphan detection
"Link this PRD to our OKR"                  → OKR Alignment Rule, contribution hypothesis
"Prioritize these features"                  → Strategic scoring, RICE, trade-off declaration
"Why are we building this first?"            → Prioritization Justification Rule applied
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

231 tests across two suites:
- **`tests/test_skill.py`** — 148 structural integrity tests: frontmatter, version, no duplicate sections, three-tier First Interaction rule, all 18 guardrails, Spec-Driven Development model, AI-native extensions, coverage & traceability, OKR alignment, multi-level prioritization, build idempotency
- **`tests/slack/`** — 83 unit tests: LLM client, intent router, thread context, Block Kit renderer, Jira client, Jira extractor, Jira export handler

---

## Repository structure

```
core/
  product-ready-core.md       ← canonical workflow + SDD model + OKR chain (source of truth)
  guardrails.md               ← 18 guardrails: Spec Integrity, Coverage, OKR Alignment, Prioritization
  templates/
    prd-template.md           ← PRD template
    behavior-spec-template.md ← BDD scenario template
    bdd-spec-ai.md            ← AI-optimised BDD Spec template with test data + automation readiness
    rtm-lite.md               ← Requirements Traceability Matrix template
    okr-linkage.md            ← OKR linkage, contribution hypothesis, and validation plan template
    prioritization.md         ← Three-level prioritization template (Strategic / Solution / Delivery)

adapters/
  anthropic/SKILL.md          ← Claude Code skill (v1.5.0)
  openai/system_prompt.txt    ← OpenAI system prompt
  slack/PRODUCT_READY.md      ← Reference architecture doc

docs/
  product-ready-workflow.html ← Self-contained HTML workflow reference (PDF-ready)

slack_bot/                    ← Production Slack bot
  handlers/                   ← slash commands, mentions, Jira export
  jira/                       ← Jira REST client + LLM extractor
  blocks/                     ← Block Kit renderer
  context/                    ← Thread context (TTL-based, in-memory)
  llm/                        ← Model-agnostic LLM client

infra/                        ← Ansible IaC for Hetzner
  provision.yml               ← first-time server setup
  deploy.yml                  ← rolling deploy
  roles/                      ← common / docker / nginx / product_ready

scripts/
  build.py                    ← generates adapters from core

tests/
  test_skill.py               ← 111 structural integrity tests
  slack/                      ← 83 Slack bot unit tests
```

---

## Artifact numbering

| Prefix | Artifact | Level |
|--------|----------|-------|
| OBJ-* | Objectives (OKR) | Company / Product |
| KR-* | Key Results (OKR) | Company / Product |
| REQ-* | Requirements | Feature |
| BR-* | Business rules | Feature |
| BS-* | BDD scenarios | Feature |
| TS-* | Test cases | Feature |
| MPD | Missing Product Decision | Any |

Every REQ-* is traceable upward to a KR-*, and every KR-* to an OBJ-*.
Every BS-* and TS-* must be traceable back to a REQ-* (enforced by Guardrail #10).

---

## Current status

| Component | Status | Version / Notes |
|-----------|--------|----------------|
| Claude Code skill (SKILL.md) | ✅ Production | v1.5.0 — 18 guardrails, OKR alignment, RTM-lite, multi-level prioritization |
| OpenAI system prompt | ✅ Production | Matches Claude Code feature set |
| Slack bot (`slack_bot/`) | ✅ Production | Intent routing, Jira export, multi-turn context |
| Jira integration | ✅ Production | Epic + Story export, BDD Spec → Jira |
| Hetzner deployment (Ansible) | ✅ Production | Nginx, Let's Encrypt, Docker, gunicorn |
| Workflow reference (`docs/`) | 📄 Reference | `product-ready-workflow.html` — PDF-ready, all 18 guardrails and 13 steps |
| Slack adapter doc (`adapters/slack/`) | 📄 Reference | Architecture reference — see `slack_bot/` for working code |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

The guardrails, escalation triggers, testability rule, Spec Integrity gate, three-tier First Interaction logic, OKR Alignment Rule, and Prioritization Gates are **protected by policy** — PRs that weaken them will be closed. Everything else is open for contribution.

---

## License

Apache 2.0 — see [LICENSE](LICENSE).
