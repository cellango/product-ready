# Contributing to Product Ready

Thank you for your interest in contributing. This document explains how the project works, what contributions are welcome, and what is protected by policy.

## How it works

Product Ready has a single source of truth in `core/` and a build system that generates platform-specific adapters:

```
core/
  product-ready-core.md   ← canonical workflow (13 steps)
  guardrails.md           ← 7 core guardrails
  examples/               ← reference outputs per workflow step
  templates/              ← PRD and behavior spec templates

scripts/
  build.py                ← generates adapters from core

adapters/
  anthropic/SKILL.md      ← generated: Claude Code skill
  openai/system_prompt.txt← generated: OpenAI system prompt
  slack/PRODUCT_READY.md  ← generated: Slack reference architecture (not yet implemented)
```

**Never edit adapter files directly.** Edit `core/` and then run the build:

```bash
python3 scripts/build.py --validate
```

Run tests before opening a PR:

```bash
pip install pytest pyyaml
python3 -m pytest tests/test_skill.py -v
```

## What contributions are welcome

- **New examples** in `core/examples/` — real-world inputs and expected outputs for specific industries or use cases
- **New templates** in `core/templates/` — domain-specific PRD or behavior spec templates (healthcare, fintech, etc.)
- **New adapters** — ports to other platforms (e.g., a working Slack bot, a VS Code extension, a Linear integration)
- **Test cases** in `test-cases/` — new scenarios that expose gaps in skill behavior
- **Bug reports** — incorrect skill behavior against a documented test case

## Protected: what contributors cannot change

The following are non-negotiable and PRs that weaken them will be rejected:

### 1. The 7 guardrails (`core/guardrails.md`)

All seven guardrails must remain intact:
- No Missing Decisions
- Testability Rule
- No Duplicates or Conflicts
- Metric Integrity
- Security & Compliance
- UI is First-Class
- Evidence Over Assumption

PRs that remove, merge, or soften any guardrail will be closed. These are the quality gates that differentiate Product Ready from generic prompt wrappers.

### 2. Escalation triggers

The five escalation triggers that promote work to Full mode must remain:
- Risk level increases
- Compliance requirements apply
- Multiple systems involved
- High user impact
- Ambiguity detected

PRs that make escalation opt-in, add bypass flags, or remove triggers will be closed.

### 3. The Testability Rule

A core invariant: **if it cannot be tested, it is not Product Ready.** PRs that allow untestable requirements to pass through as acceptable will be rejected.

### 4. Output discipline

The Minimal First Response Rule ("do not generate full artifacts unless asked") must be preserved. PRs that default to full PRD generation on first message violate the skill's design contract.

### 5. The three-tier First Interaction rule

The intent-detection tiers in `core/product-ready-core.md` must stay as three distinct tiers. Collapsing them back to a single generic menu is a known regression (it was the original bug that caused 3 of 5 baseline tests to fail).

## Opening a PR

1. Fork the repo and create a branch from `main`
2. Make changes to `core/` — not adapter files
3. Run `python3 scripts/build.py --validate` to regenerate adapters
4. Run `python3 -m pytest tests/test_skill.py -v` — all 31 tests must pass
5. If you are adding a new scenario, add it to `test-cases/` with expected behavior documented
6. Open the PR with a description of what changed and why

## Versioning

Product Ready uses semantic versioning in `SKILL.md` frontmatter. The maintainer bumps the version. Contributions do not need to update the version number.

- **Patch** (1.0.x): bug fixes, wording improvements, new examples
- **Minor** (1.x.0): new workflow steps, new adapters, new templates
- **Major** (x.0.0): breaking changes to the canonical workflow or guardrail structure

## Questions

Open an issue before starting large contributions. The fastest way to get a PR merged is to discuss intent first.
