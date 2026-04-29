# Spec-Driven Development — Implementation Plan

## Strategic direction

Product Ready is already built on the right chain. The workflow is correct. The framing is not yet explicit, and one critical guardrail is missing. This plan makes the Spec-Driven Development model explicit without breaking anything that already works.

**The target chain:**
```
Discovery → Challenge → PRD → BDD Spec (THE SPEC) → [AI: Tests + Code] → Acceptance
```

**The principle:**
BDD Spec is not a BDD exercise. It is THE canonical source of truth that drives AI code generation, AI test generation, and human acceptance validation.

---

## Phase 1 — Positioning (Now, no skill changes)

**Goal:** Establish the SDD narrative externally before changing the skill internals.

**Why first:** Positioning shapes how contributors, users, and reviewers interpret the upcoming skill changes. If they understand the SDD frame before Phase 2 lands, the guardrail additions and terminology changes feel like evolution, not disruption.

### Deliverables

- [x] **README.md** — Add positioning statement and `PRD → BDD Spec (THE SPEC) → [AI: Tests + Code] → Acceptance` chain front and centre
- [x] **docs/product-ready-positioning.md** — Full marketing and positioning document
- [ ] **docs/spec-driven-implementation-plan.md** — This document (in progress)

### Not changing in Phase 1

- SKILL.md
- core/ files
- Tests
- Version number

---

## Phase 2 — Skill Evolution: Spec Integrity (Week 1–2)

**Goal:** Make the BDD Spec THE SPEC inside the skill — not just by positioning, but by enforcement.

**The single highest-value change:** Add Guardrail #8 — Spec Integrity Rule. This is the guardrail missing from the current system. Without it, AI tools and developers proceed on incomplete specs and produce confidently wrong output.

### Core changes

#### 2a. Add Guardrail #8 to `core/guardrails.md`

```markdown
### 8. Spec Integrity
Before generating tests or code:
- BDD Spec must be complete (all scenarios written)
- BDD Spec must be unambiguous (no open interpretations)
- All edge cases and failure paths must be covered
- All Missing Product Decisions must be resolved

→ If any condition is unmet: STOP. Do not proceed to test or code generation.
```

#### 2b. Rename "Behavior Spec (BDD)" → "BDD Spec" in `core/product-ready-core.md`

The step is already correct. The name change signals its elevated role. BDD becomes implicit in the name — the chain reads naturally without needing a parenthetical explanation.

Before: `Step 5: Behavior Spec (BDD)`
After: `Step 5: BDD Spec (THE SPEC)`

#### 2c. Add Spec-Driven Development Model section to `core/product-ready-core.md`

```markdown
## Spec-Driven Development Model

The BDD Spec is the canonical source of truth for all downstream work.

From the BDD Spec:
- Test cases are derived (not invented)
- Code is generated (not guessed)
- Acceptance is validated (not interpreted)

Do not generate tests or code without a validated BDD Spec.
The spec must be complete, unambiguous, and decision-resolved before proceeding.
```

#### 2d. Add "spec-driven development" to trigger phrases in `adapters/anthropic/SKILL.md`

Ensures the skill activates when teams frame their work in SDD language.

#### 2e. Rebuild all adapters

```bash
python3 scripts/build.py --validate
```

#### 2f. Update tests in `tests/test_skill.py`

Add structural tests for:
- Guardrail #8 present in SKILL.md and core
- "BDD Spec" terminology present
- Spec-Driven Development Model section present
- "spec-driven development" in trigger phrases

#### 2g. Version bump

`1.0.0` → `1.1.0` (minor — additive guardrail + positioning, no breaking changes)

### Success criteria for Phase 2

- All 114 existing tests pass
- New structural tests pass
- Spec Integrity guardrail blocks test/code generation on incomplete specs (manual verification)
- SKILL.md reflects the full SDD chain explicitly

---

## Phase 3 — AI-Native Extensions (Month 1–2)

**Goal:** Make the BDD Spec directly usable by AI coding tools — not just conceptually, but practically.

This phase adds guidance inside the skill on *how* to use the BDD Spec with AI tools, and adds templates that produce spec output in the right format for AI consumption.

### 3a. BDD Spec → AI Prompt guidance

Add a section to the skill that explains how to translate a BDD Spec into an AI code generation prompt:

```
Scenario: [BS-001 title]
Given: [preconditions]
When: [action]
Then: [observable outcome]

Constraints:
- REQ-001: [linked requirement]
- BR-003: [relevant business rule]

Generate: [test function / implementation stub / both]
```

This formalises what Product Owners and engineers are already doing informally — turning scenarios into prompts. Making it explicit means the skill produces output that is immediately AI-ready without reformatting.

### 3b. Spec quality scoring

Before the Spec Integrity gate, the skill runs a quality check and scores the BDD Spec:

| Dimension | Check |
|-----------|-------|
| Coverage | All happy paths, edge cases, failure paths present |
| Clarity | No "should", "may", "typically" language in Then clauses |
| Linkage | Every scenario linked to at least one REQ-* |
| Decisions | No open MPD markers remaining |
| UI | All UI states defined if UI is involved |

Score: `Complete / Partial / Incomplete`
Only `Complete` specs pass the Spec Integrity gate.

### 3c. BDD Spec template (AI-optimised)

Add `core/templates/bdd-spec-ai.md` — a scenario template structured for direct use as an AI prompt:

```markdown
## Scenario [BS-NNN]: [title]

**Type:** Happy path / Edge case / Failure / Security / UI state

**Given** [system state / preconditions]
**When** [user action or system event]
**Then** [observable, testable outcome]

**Linked to:** REQ-NNN, BR-NNN
**Automation level:** Unit / Integration / E2E / Manual
**AI generation note:** [any context the AI tool needs that isn't in the scenario]
```

### 3d. "Generate from Spec" workflow step

Add an optional Step 5b: Generate, which activates when a user says "generate tests from this spec" or "create code from this spec":

1. Verify Spec Integrity gate passes
2. Format each BS-* scenario as an AI prompt
3. Specify automation level for each
4. Output ready-to-paste prompts for the AI tool of choice

---

## Phase 4 — Distribution & Community (Month 2)

**Goal:** Make the system publicly available and establish it as the reference SDD implementation for AI-era product teams.

### 4a. GitHub Release v1.1.0

Release notes frame the update explicitly as the SDD pivot:
- New: Spec-Driven Development positioning
- New: Guardrail #8 — Spec Integrity
- New: BDD Spec as THE SPEC (renamed, elevated)
- New: AI-native trigger phrases and prompting guidance

### 4b. Publish to Anthropic skill registry

Submit PR to `https://github.com/anthropics/skills`:
```
skills/product-ready/
├── SKILL.md
└── README.md   ← uses docs/product-ready-positioning.md as source
```

### 4c. Make repo public

Prerequisites before going public:
- [x] All phases complete and tested
- [x] `YOUR_GITHUB_USERNAME` replaced with `cellango` in README
- [x] `YOUR_ORG` replaced with `cellango` in docs
- [ ] Ansible vault.yml encrypted (user action required — see docs/launch-checklist.md)
- [x] No API keys in any committed file
- [x] License confirmed (Apache 2.0)

### 4d. Community engagement

- Post to Product Hunt (use docs/product-ready-positioning.md as source)
- Post to r/ProductManagement and r/artificial
- Share with Slack communities (Lenny's Newsletter, Mind the Product)
- See docs/launch-checklist.md for full post templates

---

## Phase summary

| Phase | Focus | Version | Status |
|-------|-------|---------|--------|
| 1 | Positioning & docs | 1.0.0 | ✅ Complete |
| 2 | Spec Integrity guardrail + BDD Spec rename | 1.1.0 | ✅ Complete |
| 3 | AI-native extensions (Spec Quality Score, Generate from Spec, templates) | 1.2.0 | ✅ Complete |
| 4 | Distribution, registry, public launch | 1.2.0 | ✅ Code complete — user actions in launch-checklist.md |

---

## Non-negotiable constraints across all phases

These do not change regardless of what else evolves:

1. The 8 guardrails are never weakened
2. The three-tier First Interaction rule is never replaced with a menu
3. Testability Rule: if it cannot be tested, it is not Product Ready
4. BDD Spec is always derived from a complete PRD — never written first
5. Discovery and Challenge steps are always upstream of the BDD Spec
6. All changes go through `core/` and are rebuilt into adapters via `build.py`
7. 100% test pass rate required before any version bump

---

## The risk to actively manage

**Risk:** "Spec-Driven Development" becomes a shortcut.

Teams hear SDD and conclude: write a spec, feed it to AI, ship. They skip Discovery and Challenge. They write specs for solutions they assumed, not problems they validated. The spec looks complete. The AI generates clean code. The product is wrong.

**Mitigation:** The chain in all documentation always starts from Discovery, not from the BDD Spec. Phase 2 training materials and the skill itself explicitly state: the BDD Spec is only as good as the thinking that produced it.
