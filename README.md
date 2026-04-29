# Product Ready

**The AI-native Spec-Driven Development system for Product Owners.**

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](adapters/anthropic/SKILL.md)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/YOUR_GITHUB_USERNAME/product-ready/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/product-ready/actions)
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
| Standard | Most product work | PRD + behavior spec |
| Full | Compliance, financial, AI, multi-system | Complete lifecycle with security/compliance scenarios |

It auto-escalates when it detects financial, security, compliance, or multi-system signals — no configuration needed.

### 7 non-negotiable guardrails

Every output is checked against:
1. **No Missing Decisions** — flags TBDs before they reach engineering
2. **Testability** — untestable requirements are blocked
3. **No Duplicates or Conflicts** — normalizes conflicting rules to BR-* format
4. **Metric Integrity** — every metric needs baseline, target, timeframe, decision rule
5. **Security & Compliance** — SOC2, NIST, PCI, HIPAA frameworks mapped automatically
6. **UI is First-Class** — all UI states, transitions, and accessibility included
7. **Evidence Over Assumption** — claims are labelled Strong / Medium / Weak

---

## Quick start: Claude Code

1. Copy `adapters/anthropic/SKILL.md` to your Claude Code skills directory
2. Activate it with `/product-ready` in Claude Code
3. Start with any product-related input — the skill detects intent automatically

### Example inputs that trigger the skill

```
"Add export to CSV"                          → fast mode, clarifying questions
"Build a payment processing system"          → full mode, compliance questions
"Write a PRD for user login"                 → standard mode, questions before PRD
"Review my backlog"                          → guardrails applied, missing decisions flagged
```

---

## Quick start: OpenAI

Use `adapters/openai/system_prompt.txt` as the system prompt for any OpenAI-compatible model (GPT-4o, etc.) or Custom GPT.

---

## Slack adapter

The Slack adapter (`adapters/slack/PRODUCT_READY.md`) is a **reference architecture** — it documents the intended design for a future working implementation. It is not deployable as-is. See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to help build it.

---

## Building adapters

All adapter files are generated from `core/`. Do not edit adapter files directly.

```bash
python3 scripts/build.py --validate
```

### Running tests

```bash
pip install pytest pyyaml
python3 -m pytest tests/test_skill.py -v
```

31 structural tests cover: frontmatter validity, version, no duplicate sections, three-tier First Interaction rule in all adapters, all 7 guardrails present, all 5 escalation triggers present, and build idempotency.

---

## Repository structure

```
core/
  product-ready-core.md     ← canonical 13-step workflow (source of truth)
  guardrails.md             ← 7 core guardrails
  examples/                 ← reference outputs per workflow step
  templates/                ← PRD and behavior spec templates

adapters/
  anthropic/SKILL.md        ← Claude Code skill (v1.0.0)
  openai/system_prompt.txt  ← OpenAI system prompt
  slack/PRODUCT_READY.md    ← Reference architecture (not yet implemented)

scripts/
  build.py                  ← generates adapters from core

tests/
  test_skill.py             ← 31 structural integrity tests

test-cases/                 ← 22 scenario specs (lightweight → enterprise)
```

---

## Adapters: current status

| Adapter | Status | Notes |
|---------|--------|-------|
| Claude Code (SKILL.md) | Production | v1.0.0, tested, CI-validated |
| OpenAI (system_prompt.txt) | Production | Matches Claude Code behavior |
| Slack | Reference only | Design spec — functional implementation planned |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

The guardrails, escalation triggers, testability rule, and three-tier First Interaction logic are **protected by policy** — PRs that weaken them will be closed. Everything else is open for contribution.

---

## License

Apache 2.0 — see [LICENSE](LICENSE).
