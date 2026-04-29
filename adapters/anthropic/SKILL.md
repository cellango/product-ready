---
name: product-ready
version: 1.3.0
description: Use this skill when working on product ideas, PRDs, requirements, user stories, acceptance criteria, backlog items, behavior specs, test plans, readiness reviews, spec-driven development, generating tests and code from a BDD Spec, or checking requirement coverage and traceability. Helps Product Owners clarify ideas, write PRDs, define AI-ready BDD Specs, score spec quality, generate AI prompts from scenarios, detect missing decisions, enforce bidirectional traceability (RTM-lite), and prepare work for engineering.
---

# Product Ready Core

## Purpose

Product Ready ensures that all product work is:
- clear
- testable
- measurable
- non-duplicative
- secure and compliant
- usable (UI/UX included)
- ready for engineering and acceptance

If it is not testable and measurable, it is not Product Ready.

## Core Principle

Do not move forward until the work is:
- understood
- decision-complete
- testable
- aligned to a product goal

## Adaptive Workflow Model

Product Ready uses **one workflow with adaptive depth**, not multiple workflows.

### Depth Levels

- **Lightweight** → small changes, bugs, simple features
- **Standard** → most product work
- **Full** → high-risk, compliance-heavy, AI, financial, or complex systems

### Escalation Rules

Increase rigor if:
- ambiguity increases
- risk increases
- compliance/security applies
- multiple systems or workflows are involved
- user impact is high

## Spec-Driven Development Model

Product Ready is AI-native Spec-Driven Development, built on BDD.

The development chain:

```
PRD → BDD Spec (THE SPEC) → [AI: Tests + Code] → Acceptance
```

The BDD Spec is the canonical source of truth for all downstream work:
- Test cases are **derived** from the BDD Spec, not invented separately
- Code is **generated** from the BDD Spec, not guessed at
- Acceptance is **validated** against the BDD Spec, not developer assumptions

**Do not generate tests or code without a complete, unambiguous, decision-resolved BDD Spec.**

The BDD Spec is earned — it is produced by validated discovery (Step 2), challenged assumptions (Step 3), and a complete PRD (Step 4). It is never written first.

## Workflow (Canonical)

### 1. Product Strategy / Goal

Define:
- business objective
- customer problem
- success metric (SMART)
- priority vs other work

If unclear → ask questions.

### 2. Discovery / Validation

Clarify:
- problem
- user
- current workflow
- desired outcome

Validate:
- assumptions
- cheapest test
- success/failure criteria

### 3. Challenge (Drill-Me)

Critically evaluate:
- assumptions
- risks (value, usability, feasibility, viability)
- missing decisions
- simpler alternatives

### 4. PRD

Produce structured product definition:
- requirements (REQ-*)
- business rules (BR-*)
- goals and non-goals
- metrics (SMART + integrity)
- dependencies

### 5. BDD Spec (THE SPEC)

Define:
- scenarios (BS-*)
- Given / When / Then
- edge cases
- failure cases
- UI states
- observable outputs

All scenarios must be testable.

Before proceeding to Step 6, apply Spec Integrity guardrail:
every scenario must be complete, unambiguous, decision-resolved, and linked to a REQ-*.
If any condition is unmet → STOP. Do not proceed to test or code generation.

### 5b. Generate from Spec (optional)

Activates when the user asks to generate tests or code from the BDD Spec.

Steps:
1. Run Spec Quality Score (Guardrail #8)
2. If score is **Incomplete** or **Partial** → list every failing dimension, STOP
3. If score is **Complete** → format each BS-* scenario as an AI generation prompt

For each scenario, produce one self-contained prompt block:

    Scenario [BS-NNN]: [title]
    Type: [Happy path / Edge case / Failure / Security / UI]

    Given [preconditions — specific, named entities and values]
    When [one action or event]
    Then [exact, observable assertion]

    Requirements: [REQ-NNN] — [brief text]
    Business Rules: [BR-NNN] — [brief text]
    Automation: [Unit / Integration / E2E / Manual]
    Context: [API endpoints, data types, constraints the AI needs]

    Generate: [test function / implementation stub / both]

Output one prompt block per scenario. Do not bundle multiple scenarios in one block.

### 6. Test Spec

Convert behavior into:
- test cases (TS-*) derived from BDD Spec scenarios
- steps
- assertions
- automation level (Automatable / Partially automatable / Manual only)

Do not invent missing rules.

After completing the Test Spec, apply **Guardrail #9 (Acceptance Coverage Rule)** and **Guardrail #10 (Bidirectional Traceability)**:
- Every REQ-* must now link to at least one BS-* and at least one TS-*
- Generate the RTM-lite (Requirements Traceability Matrix) — see `core/templates/rtm-lite.md`
- Flag any Coverage Gaps or orphan BS-*/TS-* before proceeding

### 7. Prioritization

Evaluate:
- impact
- effort
- risk
- confidence

Produce ranked backlog.

### 8. Issues

Break into:
- independent, testable stories
- linked to REQ / BS / TS

### 9. Build

Ensure:
- implementation follows BDD Spec
- questions resolved before coding

### 10. Acceptance

A feature is acceptable only when:
- all Must scenarios pass
- tests pass
- no critical defects
- behavior matches intent
- UI/UX is acceptable
- RTM-lite is complete: every REQ-* has at least one BS-* and one TS-* (Guardrail #9)
- No orphan BS-*/TS-* items (Guardrail #10)
- Automation Readiness ≥80% (Guardrail #13)

### 11. Release

Ensure:
- readiness criteria met
- stakeholders aligned
- rollback plan exists

### 12. Measure

Track:
- success metrics
- guardrail metrics
- adoption
- quality

### 13. Learn / Iterate

Evaluate:
- what worked
- what failed
- next iteration

Feed back into discovery.

## BDD Spec → AI Prompt Mapping

A BDD scenario is a complete AI generation prompt — no reformatting required when written correctly.

### Rules for AI-ready Then clauses

Then clauses must be **exact and observable**. Vague language breaks AI generation:

- ❌ "the system should process the request" — untestable
- ❌ "the user may see a confirmation" — ambiguous
- ❌ "the page typically loads within a few seconds" — non-deterministic
- ✅ "the API returns HTTP 200 with body `{"status": "created", "id": "<uuid>"}`"
- ✅ "the user sees the message 'Your order has been placed (Order #12345)'"
- ✅ "a record is inserted in the orders table with status='pending' and user_id matching the session"

### One behaviour per scenario

Do not combine multiple assertions in a single scenario. Split them:

- ❌ `Given X, When Y, Then A and B and C`
- ✅ `BS-001: Then A` | `BS-002: Then B` | `BS-003: Then C`

### State all preconditions explicitly

AI tools have no knowledge of your system. Given clauses must be self-contained:

- ❌ "Given the user is logged in"
- ✅ "Given a registered user with role=admin, account_status=active, and a valid session token"

### Standard AI prompt format

    Scenario [BS-NNN]: [title]
    Type: [Happy path / Edge case / Failure / Security / UI]

    Given [preconditions]
    When [action]
    Then [exact assertion]

    Requirements: [REQ-NNN] — [brief text]
    Business Rules: [BR-NNN] — [brief text]
    Automation: [Unit / Integration / E2E / Manual]
    Context: [technical constraints]

    Generate: [test function / implementation / both]

## Coverage Validation

Activates when the user asks to "check coverage", "run RTM", "generate traceability matrix", or "check acceptance coverage".

Steps:
1. List all REQ-* from the PRD
2. For each REQ-*, list linked BS-* and TS-*
3. Output the RTM-lite table (see `core/templates/rtm-lite.md`)
4. Flag: Coverage Gaps (REQ-* with no BS-* or no TS-*), orphans (BS-*/TS-* not linked to any REQ-*)
5. Report coverage summary: N covered / N total, orphan count, automation readiness %
6. If gaps exist: STOP. List what must be added before acceptance.

## Default Behavior

If input is vague:
→ start with Discovery

If risky or complex:
→ escalate to full workflow

If small/simple:
→ stay lightweight

## First Interaction

Three tiers — pick the first that matches:

**1. Intent clear** (user named a task: "write a PRD", "review my backlog", "add export to CSV"):
→ Skip any intro. Proceed directly to the appropriate workflow step.

**2. Domain known, task unclear** (user named an area — UX, performance, onboarding, search — but not what they want to do):
→ Skip the process menu. Ask what specific problem they're trying to solve.
→ Example: "What's the specific UX problem you're seeing — is it a flow, a friction point, or something users are failing to do?"

**3. No signal** (no domain, no task — e.g., "I have an idea", "I need help"):
→ One sentence: "Product Ready helps you define, spec, and validate product work before it reaches engineering."
→ One question: "What are you working on — an idea, a PRD, acceptance criteria, or a backlog review?"

# Product Ready Guardrails

## Purpose

Guardrails ensure quality, prevent common pitfalls, and enforce standards throughout the product development process.

## Core Guardrails

### 1. No Missing Decisions
If a decision is required but not made:
→ Mark as **Missing Product Decision**
→ Do not proceed until resolved

### 2. Testability Rule
If work cannot be tested:
→ It is not ready
→ Must have acceptance criteria and test cases

### 3. No Duplicates or Conflicts
- Detect duplicate requirements
- Detect contradictions between rules
- Normalize conflicting items into BR-* business rules
- Resolve before finalizing

### 4. Metric Integrity
Every success metric must include:
- **Baseline**: Current value
- **Target**: Desired value
- **Timeframe**: When to achieve
- **Decision Rule**: How to evaluate success/failure

### 5. Security & Compliance
- Identify applicable frameworks (SOC2, NIST, PCI, etc.)
- Map controls to requirements
- Include security scenarios in BDD Spec
- Generate compliance test cases

### 6. UI is First-Class
- Define all UI states and transitions
- Ensure usability and accessibility standards
- Include UI scenarios in BDD Spec
- Validate with user testing criteria

### 7. Evidence Over Assumption
For all claims and assumptions:
- Label evidence strength: Strong / Medium / Weak
- Prefer data-driven decisions
- Validate assumptions with cheapest tests

### 8. Spec Integrity

Before proceeding to test or code generation, run the **Spec Quality Score**:

| Dimension | Check | Level |
|-----------|-------|-------|
| **Coverage** | Happy paths, edge cases, and failure paths all present | Critical |
| **Clarity** | No "should", "may", "typically" in Then clauses — all assertions are exact and observable | Critical |
| **Observability** | Every Then clause names a specific system layer: UI element, API response, DB record, log entry, or event | Required |
| **Linkage** | Every BS-* scenario linked to at least one REQ-* | Required |
| **Decisions** | No open [MPD] markers remaining | Required |
| **Example data** | Every scenario includes at least one concrete value — not "a user", not "some input", not placeholder X | Required |
| **UI** | All UI states defined (conditional — only if UI is involved) | Conditional |

**Score:**
- **Complete** → all Critical pass + all Required pass → proceed to generation
- **Partial** → one or more Required dimensions fail → list what must be fixed, re-score before continuing
- **Incomplete** → one or more Critical dimensions fail → STOP immediately. Do not generate tests or code.

Report the score and list every failing dimension before stopping.

### 9. Acceptance Coverage Rule

Every REQ-* must be covered before a feature can be accepted:
- Every REQ-* must link to **at least one BS-*** (behavior scenario)
- Every REQ-* must link to **at least one TS-*** (test case)

If any REQ-* lacks either a BS-* or a TS-*: flag it as a **Coverage Gap**. Do not mark the feature as Product Ready or accepted.

Apply at: Step 6 completion (Test Spec), and again at Step 10 (Acceptance).

### 10. Bidirectional Traceability Rule

Traceability must be enforced in both directions:

1. **Forward trace** (REQ → BS → TS): every requirement is specified and tested
2. **Backward trace** (TS → BS → REQ): every test case has a validated reason to exist
3. **Orphan detection**: any BS-* or TS-* not linked to a REQ-* is an **orphan** — flag it and resolve before acceptance

Generate an **RTM-lite** (Requirements Traceability Matrix) before Step 10 (Acceptance):

| REQ-* | Requirement | BS-* Scenarios | TS-* Test Cases | Coverage |
|-------|-------------|----------------|-----------------|----------|
| REQ-001 | [text] | BS-001, BS-002 | TS-001, TS-002 | ✅ Full |
| REQ-002 | [text] | BS-003 | — | ⚠️ No TS-* |
| REQ-003 | [text] | — | — | ❌ Gap |

Report: requirements covered / total, orphan count, automation readiness percentage.

### 11. Scenario Completeness Rule

For each REQ-*, the BDD Spec must contain all three scenario types:
- At least **1 happy path** (BS-* Type: Happy path) — the core success behaviour
- At least **1 failure scenario** (BS-* Type: Failure) — system response to bad input or error condition
- At least **1 edge case** (BS-* Type: Edge case) — boundary values, unusual but valid states

If any type is missing for a REQ-*: report as **Partial Coverage** for that requirement.
Do not proceed to test generation until all three types are present.

### 12. No Ambiguity Rule

Requirements and Then clauses must not contain ambiguous terms. Reject and replace:

| ❌ Banned term | ✅ Required replacement |
|----------------|------------------------|
| "should", "might", "could" | a deterministic assertion |
| "user-friendly", "intuitive", "easy", "simple" | measurable usability metric (e.g. SUS > 80, task completion < 2 min) |
| "fast", "performant", "quick" | specific latency or throughput number (e.g. p95 < 200ms) |
| "better", "improve", "enhance" | baseline → target with timeframe |
| "seamless", "smooth" | named user flow with completion criterion |

If any banned term appears in a REQ-* or Then clause: flag and require rewrite before accepting.

### 13. Automation Readiness Rule

Every BS-*/TS-* must be classified for automation:

- **Automatable** — deterministic output, reproducible state, independent of other tests, executable in CI
  → Specify level: Unit / Integration / E2E
- **Partially automatable** — some steps automatable, some require human verification
  → Document which steps are manual and why
- **Manual only** — requires human judgment, subjective assessment, or cannot be reproduced in CI
  → Document the reason

A spec is **Automation Ready** when ≥80% of scenarios are Automatable.
Flag as **Automation Risk** when <50% of scenarios are Automatable — escalate before committing to delivery timeline.

## Execution Modes

### Fast Mode (Default)
- Minimal questions asked
- Quick readiness check
- Lightweight acceptance criteria
- For small changes and simple features

### Full Mode
- Complete workflow execution
- PRD + Behavior Spec + Test Spec
- Compliance, UI, security included
- For high-risk, complex, or regulated work

### Escalation Triggers
Automatically escalate to Full Mode when:
- Risk level increases
- Compliance requirements apply
- Multiple systems involved
- High user impact
- Ambiguity detected

# Output Rules

- Be concise unless full mode is required
- Do not generate long PRDs unless explicitly needed
- Prefer structured output over essays
- Ask questions before generating if unclear

---

# Skill Activation Behavior

When invoked:

1. Identify intent:
   - clarify idea
   - write PRD
   - define behavior/tests
   - review work

2. Choose appropriate depth:
   - fast
   - standard
   - full

3. Proceed with minimal necessary steps

---

# Trigger Phrases

This skill should activate when the user mentions or implies:
- PRD
- product requirements
- user stories
- acceptance criteria
- backlog
- feature design
- product idea
- feature request
- behavior spec
- test cases
- readiness
- review requirements
- define workflow
- improve feature
- clarify idea
- spec-driven development
- BDD spec
- generate from spec
- generate tests
- generate code from spec
- score my spec
- spec quality
- check coverage
- traceability matrix
- RTM
- requirement coverage
- acceptance coverage
- automation readiness

Even if the user does not explicitly say "Product Ready"

---

# Intent Detection

Map user requests to workflow steps:
- vague idea → Discovery
- critique request → Challenge
- PRD request → PRD (with questions first)
- acceptance criteria → BDD Spec
- test request → Test Spec
- backlog → Issues / Prioritization
- review → Guardrails / Anti-pattern detection
- generate tests / generate code → run Spec Quality Score first (Guardrail #8), then Generate from Spec (Step 5b)
- score my spec / check spec quality → run Spec Quality Score and report dimensions
- check coverage / run RTM / traceability matrix / acceptance coverage → run Coverage Validation, output RTM-lite, flag gaps

---

# Minimal First Response Rule

Do not overwhelm the user.
- Ask only the minimum questions needed
- Do not generate full artifacts unless asked
- Start small, expand only when needed

---

# When NOT to use

- Simple factual questions
- Pure coding tasks without product context
- General brainstorming unrelated to product definition