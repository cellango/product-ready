# Product Ready - Slack Integration

> **Status: Reference Architecture — Not Yet Implemented**
> This document describes the intended Slack integration design. The slash commands, API handlers, and integrations shown below are design specifications, not working code. A functional implementation is planned for a future release. Do not deploy this as-is.

## Overview
Product Ready brings structured product development workflows directly into Slack, enabling teams to clarify requirements, define behaviors, and ensure readiness without leaving their conversation flow.

## Features
- **Inline Workflow Execution**: Run product workflows in Slack threads
- **Adaptive Assistance**: Scales from quick checks to full PRD generation
- **Team Collaboration**: Share and review work items in channels
- **Integration Ready**: Connects with Jira, Linear, Notion for seamless handoff

## Usage

### Basic Commands
- `/product-ready clarify "user login issue"` - Start discovery
- `/product-ready prd "new feature idea"` - Generate PRD
- `/product-ready behavior "login flow"` - Define acceptance criteria
- `/product-ready review @thread` - Review existing discussion

### Workflow Integration
1. **Discovery Mode**: Ask clarifying questions in thread
2. **PRD Generation**: Output structured requirements
3. **Behavior Specs**: Generate Given/When/Then scenarios
4. **Test Cases**: Create acceptance criteria
5. **Readiness Check**: Validate work completeness

## Core Logic
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

## Multi-Level Prioritization Model

Prioritization is not a single step — it is a continuous decision system that runs at three levels throughout the workflow.

**The critical insight:** Prioritization placed only after the PRD is too late. By the time a full spec is written, teams have invested effort, anchored on a solution, and created sunk-cost pressure. Prioritization must happen *before* that investment is made.

| Level | When | Question it answers |
|-------|------|-------------------|
| **Strategic** | Before Discovery | Should we work on this problem at all? |
| **Solution** | Before PRD | Which approach and scope should we pursue? |
| **Delivery** | Before Issues | What do we build first within this initiative? |

Each level requires: scoring + justification + explicit trade-offs. Ranking without reasoning is not prioritization.

### Anti-Pattern: Specification Before Prioritization

Do not fully specify work that has not been prioritized. Writing a complete PRD for a low-priority initiative creates:
- wasted effort
- sunk-cost pressure to build it anyway
- over-engineering of the wrong thing

**If priority is unclear → stop and prioritize first. Then spec.**

### Context-Aware Prioritization

Prioritization criteria shift with company stage:

| Stage | Optimize for | De-emphasize |
|-------|-------------|--------------|
| **Startup** | Learning speed, validated assumptions | Polish, scalability |
| **Growth** | User impact, reach, retention | Internal tooling |
| **Enterprise** | Risk reduction, compliance, stakeholder alignment | Speed alone |

Declare the stage at the start of each prioritization session.

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

**OKR linkage** — for every piece of product work, establish:
- **Objective** (OBJ-*): the qualitative, time-bound goal this work serves
- **Key Result** (KR-*): the specific measurable outcome this work is expected to move, with current value and target
- **Contribution hypothesis**: why this work is the right lever for this KR
- **Non-OKR declaration**: if this work does not serve a current OKR (e.g. technical debt, regulatory requirement), declare it explicitly — do not leave it implied

If OKR linkage is unclear → ask before proceeding.

If unclear → ask questions.

### 1b. Strategic Prioritization

Before moving to Discovery, confirm this initiative deserves investment at all.

**Score against portfolio:**

| Criterion | Score (1–5) | Notes |
|-----------|-------------|-------|
| Strategic alignment — does this serve an active OBJ-*/KR-*? | | |
| Customer impact — how many users, how severely affected? | | |
| Business value — revenue, retention, risk reduction, compliance | | |
| Confidence — how well do we understand the problem? | | |
| Opportunity cost — what are we NOT doing by choosing this? | | |

**Mandatory outputs before proceeding:**
- Why this problem, why now (not in 3 months, not someone else's problem)
- What we are explicitly NOT pursuing to make room for this
- Consequence of delaying 1 quarter: what breaks or is missed?

**Gate:** If strategic score is low or the opportunity cost is unacceptable → deprioritize. Do not proceed to Discovery.

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

**OKR alignment challenge** — always ask:
- "Is this feature the right lever for KR-*? Or is there a higher-leverage intervention that would move the same KR faster?"
- "Is the contribution hypothesis falsifiable? Can you describe what data at 30/60/90 days would prove or disprove it?"
- "If this feature ships and the KR does not move, what is your fallback hypothesis?"
- "Is this work output (something shipped) or outcome (a KR moved)? Do not confuse the two."

### 3b. Solution Prioritization

Before writing the PRD, confirm which solution approach and feature scope to pursue.

**MoSCoW triage on candidate capabilities:**

| Capability | Must / Should / Could / Won't | Reason |
|------------|-------------------------------|--------|
| [capability A] | Must | [why non-negotiable] |
| [capability B] | Should | [why valuable but deferrable] |
| [capability C] | Won't (this release) | [why deprioritized] |

**Solution scoring (compare alternatives):**

| Option | Impact | Effort | Risk | Confidence | Score | Decision |
|--------|--------|--------|------|------------|-------|----------|
| Option A | H | M | L | H | | |
| Option B | H | H | M | M | | |

**Gate:** PRD scope must reflect only Must + approved Should items. Won't items must be documented in the PRD's non-goals — not left ambiguous.

### 4. PRD

Produce structured product definition:
- requirements (REQ-*)
- business rules (BR-*)
- goals and non-goals
- metrics (SMART + integrity)
- dependencies

**OKR section** — every PRD must include:

```
OKR linkage:
  Objective: OBJ-[N] — [objective text]
  Key Result: KR-[N] — [KR text] (current: [value], target: [value], by: [date])

Contribution hypothesis:
  [How and why this feature is expected to move this KR]
  [Causal chain: feature adoption → behaviour change → KR movement]

Validation plan:
  [How KR movement will be isolated from other concurrent changes]
  [Measurement points: 30d / 60d / 90d post-ship]
  [Leading indicator: the feature metric that predicts KR movement]
```

If the work does not serve a current OKR, declare:
```
Non-OKR declaration: [reason — e.g. regulatory requirement / technical debt / incident response]
```

Every REQ-* in the PRD is implicitly linked to the KR-* declared in the OKR section.
If individual requirements serve different KRs, declare per-requirement linkage explicitly.

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

### 7. Delivery Prioritization

Order implementation within the confirmed scope. This answers: "What do we build first?"

**Standard scoring model** (covers RICE, ICE, and WSJF in one pass):

| Item | Reach | Impact | Confidence | Effort | RICE Score | Cost of Delay | Priority | Justification |
|------|-------|--------|------------|--------|------------|---------------|----------|---------------|
| [story A] | [users/wk] | H/M/L | H/M/L | H/M/L | R×I×C/E | H/M/L | #1 | [reason] |
| [story B] | | | | | | | #2 | [reason] |

- **RICE** = (Reach × Impact × Confidence) / Effort — optimizes user value
- **Cost of Delay** — what is lost per sprint this is delayed? (from WSJF)
- **Confidence** — how certain are we about impact estimate? (0–100%)

**Every ranked item must include a Justification** — one sentence explaining why this is above the item below it.

**Trade-off Declaration** — for each item not in the top tier, state:
- Why it is ranked lower
- What risk is accepted by delaying it
- What would trigger re-prioritization (new data, metric change, escalation)

**Frameworks by context:**

| Situation | Use |
|-----------|-----|
| User-value focus | RICE |
| Deadline / urgency pressure | WSJF (Cost of Delay ÷ Job Size) |
| Simple backlog triage | ICE (Impact × Confidence × Ease) |
| Release scope decisions | MoSCoW |

Output: ranked backlog with score, justification, and trade-off note per item.

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

**OKR measurement** — at every measurement checkpoint, report both levels:

```
Feature metric:    [metric name] — [actual] vs [target] — [✅ Met / ⚠️ Partial / ❌ Missed]
KR movement:       KR-[N] — [before: value] → [after: value] (+/- delta)
KR remaining gap:  [current value] vs [KR target] — [gap remaining]
Attribution note:  [how much of the KR movement is attributable to this feature vs other work]
```

If the KR did not move despite the feature metric being met:
→ Revisit the contribution hypothesis — the causal chain was wrong
→ Identify what the next lever is
→ Feed back into Step 13 (Learn / Iterate)

### 13. Learn / Iterate

Evaluate:
- what worked
- what failed
- next iteration

Feed back into discovery.

## Artifact Numbering Convention

| Prefix | Artifact | Level |
|--------|----------|-------|
| OBJ-* | Objectives (OKR) | Company / Product |
| KR-* | Key Results (OKR) | Company / Product |
| REQ-* | Requirements | Feature |
| BR-* | Business rules | Feature |
| BS-* | BDD scenarios | Feature |
| TS-* | Test cases | Feature |
| MPD | Missing Product Decision | Any |

Every REQ-* should be traceable upward to a KR-*, and every KR-* to an OBJ-*.

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

## Guardrails
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

### 14. OKR Alignment Rule

Every PRD must declare its OKR linkage before the work proceeds to BDD Spec.

**Required fields:**
- Objective (OBJ-*) — which qualitative goal this work serves
- Key Result (KR-*) — the specific measurable outcome, with current value and target
- Contribution hypothesis — the causal chain from this feature to KR movement
- Validation plan — how KR movement will be measured and attributed post-ship

**Allowed exception:**
Work that does not serve a current OKR must carry an explicit Non-OKR declaration:
- Regulatory / legal requirement
- Technical debt / reliability / security
- Incident response
- Foundational infrastructure

Implied OKR alignment ("this obviously helps growth") is not accepted.
Undeclared OKR linkage = **Missing Product Decision** — apply Guardrail #1.

**OKR decoration check:**
If the contribution hypothesis cannot answer all three:
1. What specific behaviour change in the user does this feature drive?
2. How does that behaviour change translate into KR movement?
3. What data at 30/60/90 days proves or disproves the hypothesis?

→ The hypothesis is decoration, not a real linkage. Rewrite before proceeding.

**Accepted KR formats:**
- Quantitative: "Increase 30-day retention from 41% to 60% by end of Q3"
- Leading indicator acceptable as proxy: "Increase weekly active teams from 210 to 500 by Q3"
- Lagging KR with leading feature metric is the correct pattern — declare both

### 15. Prioritization Justification Rule

Every prioritization decision — at Strategic, Solution, or Delivery level — must include a written justification. Ranking without reasoning is not prioritization.

**Required for every prioritized item:**
- **Why now** — why this quarter, not next? What changes if delayed?
- **Value delivered** — which KR-* does this move, and by how much?
- **What we are NOT doing** — what is explicitly deprioritized to make room for this?
- **Consequence of delay** — what breaks or is missed if this slips one sprint / one quarter?

**Banned outputs:**
- A ranked list with no explanation (rank ≠ justification)
- "This is high priority" with no evidence
- Priority set by seniority or loudness of request

If any item cannot answer all four questions: flag as **Priority Decision Pending** and escalate before proceeding.

### 16. Trade-off Declaration

For every priority decision, the items NOT chosen must be documented.

**Required trade-off record:**

| Deprioritized item | Why ranked lower | Risk accepted by delaying | Re-prioritization trigger |
|-------------------|-----------------|--------------------------|--------------------------|
| [item] | [reason] | [what could go wrong] | [event that would change priority] |

**The Product Owner must be able to defend any deprioritization decision** to any stakeholder with the same evidence used to make it. "We'll get to it later" is not a trade-off declaration.

### 17. Prioritization Gate

Do not write a full PRD for work that has not passed Strategic Prioritization.
Do not create Issues for work that has not passed Delivery Prioritization.

**Gate 1 — Strategic (before Discovery):**
- Initiative must score above threshold on strategic alignment, customer impact, and confidence
- Opportunity cost must be explicitly accepted
- If strategic score is low → deprioritize or park in backlog. Do not proceed.

**Gate 2 — Solution (before PRD):**
- MoSCoW triage must be complete on candidate capabilities
- PRD scope must contain only Must + approved Should items
- Won't items must appear in PRD non-goals

**Gate 3 — Delivery (before Issues):**
- Every story must be scored and ranked
- Every story must have a justification
- Trade-off Declaration must be complete for deprioritized stories

Violation of any gate = **specification before prioritization** — the most expensive anti-pattern in product development.

### 18. Re-prioritization Trigger

Priorities are not permanent. A priority set without a review condition is a frozen assumption — not a decision.

**Mandatory re-prioritization when any of the following occur:**
- New data contradicts the contribution hypothesis
- A KR-* moves unexpectedly (positive or negative)
- Effort estimate changes by >50%
- A dependency is removed or added
- A competitor ships the same capability
- A compliance or security risk is identified post-prioritization
- A stakeholder escalates with new evidence (not new opinion)

**At each re-prioritization:**
1. Document what changed and why it changes the priority
2. Re-score affected items
3. Update the Trade-off Declaration
4. Notify affected teams before re-ordering their queue

Opinion-based re-prioritization (without new evidence) is not accepted. Apply Guardrail #7 (Evidence Over Assumption).

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

## Implementation Details

### Slack App Configuration

#### App Manifest (app.json)
```json
{
  "display_information": {
    "name": "Product Ready",
    "description": "Structured product development workflows in Slack",
    "background_color": "#4A154B"
  },
  "features": {
    "bot_user": {
      "display_name": "Product Ready",
      "always_online": true
    }
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "channels:read",
        "chat:write",
        "chat:write.public",
        "files:write",
        "groups:read",
        "im:read",
        "mpim:read",
        "users:read",
        "users:read.email"
      ]
    }
  },
  "settings": {
    "event_subscriptions": {
      "bot_events": [
        "app_mention",
        "message.channels",
        "message.groups",
        "message.im",
        "message.mpim"
      ]
    },
    "interactivity": {
      "is_enabled": true,
      "request_url": "https://your-domain.com/slack/interactive",
      "message_menu_options_url": "https://your-domain.com/slack/options"
    },
    "slash_commands": [
      {
        "command": "/product-ready",
        "url": "https://your-domain.com/slack/commands",
        "description": "Start a product workflow",
        "usage_hint": "[action] [description]",
        "should_escape": false
      },
      {
        "command": "/prd",
        "url": "https://your-domain.com/slack/commands",
        "description": "Generate or review a PRD",
        "usage_hint": "[description]",
        "should_escape": false
      },
      {
        "command": "/behavior",
        "url": "https://your-domain.com/slack/commands",
        "description": "Define behavior specifications",
        "usage_hint": "[feature description]",
        "should_escape": false
      },
      {
        "command": "/acceptance",
        "url": "https://your-domain.com/slack/commands",
        "description": "Create acceptance criteria",
        "usage_hint": "[requirement]",
        "should_escape": false
      }
    ]
  }
}
```

### API Endpoints

#### Command Handler (`/slack/commands`)
```python
from slack_sdk import WebClient
from slack_bolt import App

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.command("/product-ready")
def handle_product_ready(ack, respond, command):
    ack()
    action = command.get("text", "").strip()

    if not action:
        respond({
            "response_type": "ephemeral",
            "text": "Product Ready Help",
            "attachments": [
                {
                    "text": "Available actions:",
                    "fields": [
                        {"title": "clarify", "value": "Start discovery for vague ideas"},
                        {"title": "prd", "value": "Generate PRD from description"},
                        {"title": "behavior", "value": "Define acceptance criteria"},
                        {"title": "review", "value": "Review existing thread"}
                    ]
                }
            ]
        })
        return

    # Process the action and respond
    result = process_product_ready_action(action, command)
    respond(result)

def process_product_ready_action(action, command):
    """Process Product Ready actions and return Slack response"""

    # Parse action type
    if action.startswith("clarify"):
        return handle_discovery(action, command)
    elif action.startswith("prd"):
        return handle_prd_generation(action, command)
    elif action.startswith("behavior"):
        return handle_behavior_spec(action, command)
    elif action.startswith("review"):
        return handle_review(action, command)
    else:
        return {"text": f"Unknown action: {action}. Try 'clarify', 'prd', 'behavior', or 'review'."}
```

#### Interactive Component Handler (`/slack/interactive`)
```python
@app.action("workflow_selection")
def handle_workflow_selection(ack, body, respond):
    ack()
    selected_workflow = body["actions"][0]["value"]

    # Start the selected workflow
    workflow_response = start_workflow(selected_workflow, body)
    respond(workflow_response)

@app.view("workflow_modal")
def handle_workflow_modal(ack, body, respond):
    ack()
    values = body["view"]["state"]["values"]

    # Process modal submission
    result = process_workflow_modal(values, body)
    respond(result)
```

### Workflow Implementation

#### Discovery Mode
```python
def handle_discovery(description, command):
    """Handle discovery/clarification requests"""

    # Extract context from Slack message
    channel = command["channel_id"]
    thread_ts = command.get("thread_ts") or command["ts"]
    user = command["user_id"]

    # Ask clarifying questions
    questions = generate_discovery_questions(description)

    return {
        "response_type": "in_channel",
        "thread_ts": thread_ts,
        "text": f"Starting discovery for: {description}",
        "attachments": [
            {
                "color": "good",
                "title": "Discovery Questions",
                "text": "\n".join(f"• {q}" for q in questions),
                "callback_id": "discovery_response",
                "actions": [
                    {
                        "name": "answer_questions",
                        "text": "Answer Questions",
                        "type": "button",
                        "value": "start_answers"
                    }
                ]
            }
        ]
    }
```

#### PRD Generation
```python
def handle_prd_generation(description, command):
    """Generate PRD from description"""

    # Determine workflow depth
    complexity = assess_complexity(description)
    mode = "full" if complexity > 7 else "standard"

    # Generate PRD content
    prd_content = generate_prd(description, mode)

    return {
        "response_type": "in_channel",
        "text": f"Generated {mode.title()} PRD",
        "attachments": [
            {
                "color": "good",
                "title": f"PRD: {description[:50]}...",
                "text": prd_content,
                "fields": [
                    {"title": "Requirements", "value": f"{len(prd_content.get('requirements', []))} items"},
                    {"title": "Business Rules", "value": f"{len(prd_content.get('business_rules', []))} items"},
                    {"title": "Success Metrics", "value": f"{len(prd_content.get('metrics', []))} items"}
                ]
            }
        ]
    }
```

### Block Kit Templates

#### Workflow Selection Modal
```json
{
  "type": "modal",
  "title": {"type": "plain_text", "text": "Product Ready"},
  "submit": {"type": "plain_text", "text": "Start"},
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "What would you like to accomplish?"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "Clarify Idea"},
          "value": "discovery",
          "action_id": "workflow_discovery"
        },
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "Write PRD"},
          "value": "prd",
          "action_id": "workflow_prd"
        },
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "Define Behavior"},
          "value": "behavior",
          "action_id": "workflow_behavior"
        }
      ]
    }
  ]
}
```

#### Question Collection Modal
```json
{
  "type": "modal",
  "title": {"type": "plain_text", "text": "Discovery Questions"},
  "submit": {"type": "plain_text", "text": "Generate"},
  "blocks": [
    {
      "type": "input",
      "block_id": "problem",
      "label": {"type": "plain_text", "text": "What's the core problem?"},
      "element": {"type": "plain_text_input", "action_id": "problem_input"}
    },
    {
      "type": "input",
      "block_id": "users",
      "label": {"type": "plain_text", "text": "Who are the users?"},
      "element": {"type": "plain_text_input", "action_id": "users_input"}
    },
    {
      "type": "input",
      "block_id": "outcome",
      "label": {"type": "plain_text", "text": "What's the desired outcome?"},
      "element": {"type": "plain_text_input", "action_id": "outcome_input"}
    }
  ]
}
```

### File Upload Integration

#### PRD Export to File
```python
def upload_prd_to_slack(prd_content, channel, thread_ts):
    """Upload PRD as a file to Slack thread"""

    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

    # Convert PRD to markdown
    markdown_content = format_prd_as_markdown(prd_content)

    # Upload file
    response = client.files_upload_v2(
        channel=channel,
        thread_ts=thread_ts,
        filename=f"PRD-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md",
        content=markdown_content,
        title="Product Requirements Document",
        initial_comment="Here's the generated PRD. Review and refine as needed."
    )

    return response
```

### Error Handling

#### Slack Error Responses
```python
def handle_slack_error(error, channel, thread_ts=None):
    """Handle and respond to Slack API errors"""

    error_messages = {
        "missing_scope": "Missing required permissions. Please reinstall the app.",
        "invalid_auth": "Authentication failed. Please check bot token.",
        "rate_limited": "Rate limit exceeded. Please try again in a moment.",
        "channel_not_found": "Channel not found or bot not invited.",
        "thread_not_found": "Thread not found. Please check the thread timestamp."
    }

    message = error_messages.get(error, f"An error occurred: {error}")

    return {
        "response_type": "ephemeral",
        "thread_ts": thread_ts,
        "text": f"❌ {message}",
        "attachments": [
            {
                "color": "danger",
                "text": "If this persists, contact your Slack administrator."
            }
        ]
    }
```

## Deployment

### Environment Variables
```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token
OPENAI_API_KEY=your-openai-key (optional)
ANTHROPIC_API_KEY=your-anthropic-key (optional)
```

### Hosting Requirements
- **Runtime**: Python 3.8+
- **Framework**: Slack Bolt for Python
- **Web Server**: Any ASGI server (Daphne, Uvicorn, Gunicorn)
- **Database**: Optional (for conversation persistence)
- **SSL**: Required for production

### Scaling Considerations
- **Rate Limits**: Slack allows 1 request per second per app
- **Concurrency**: Handle multiple simultaneous workflows
- **Caching**: Cache user/channel information
- **Monitoring**: Track usage and error rates

## Security Considerations

### Data Privacy
- No sensitive data stored permanently
- Conversations processed in memory only
- File uploads handled securely
- User data anonymized in logs

### Authentication
- Bot tokens validated on each request
- Request signing verification enabled
- HTTPS required for all endpoints
- Token rotation procedures documented

## Integration APIs

### Jira Integration
```python
def create_jira_issue(prd_data, jira_config):
    """Create Jira issue from PRD data"""

    jira = JIRA(server=jira_config["server"],
                basic_auth=(jira_config["user"], jira_config["token"]))

    issue_data = {
        "project": {"key": jira_config["project"]},
        "summary": prd_data["title"],
        "description": format_prd_for_jira(prd_data),
        "issuetype": {"name": "Epic"}
    }

    issue = jira.create_issue(fields=issue_data)
    return issue.key
```

### Linear Integration
```python
def create_linear_issue(prd_data, linear_token):
    """Create Linear issue from PRD data"""

    client = LinearClient(linear_token)

    # Create issue
    issue = client.create_issue(
        title=prd_data["title"],
        description=format_prd_for_linear(prd_data),
        team_id=get_team_id(prd_data["team"])
    )

    return issue.id
```

## Testing

### Unit Tests
```python
def test_slack_command_parsing():
    """Test parsing of Slack slash commands"""

    command = "/product-ready prd new login feature"
    parsed = parse_slack_command(command)

    assert parsed["action"] == "prd"
    assert parsed["description"] == "new login feature"

def test_workflow_depth_assessment():
    """Test automatic workflow depth selection"""

    simple_request = "add a button"
    complex_request = "build AI-powered recommendation system with GDPR compliance"

    assert assess_complexity(simple_request) < 5
    assert assess_complexity(complex_request) > 7
```

### Integration Tests
- Test slash command responses
- Test modal interactions
- Test file uploads
- Test error handling
- Test rate limiting

## Monitoring & Analytics

### Key Metrics
- Commands executed per day
- Workflow completion rates
- User engagement (questions asked/answered)
- Error rates by command type
- Average response times

### Logging
```python
def log_slack_interaction(interaction_type, user, channel, success, metadata=None):
    """Log Slack interactions for analytics"""

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": interaction_type,
        "user": user,
        "channel": channel,
        "success": success,
        "metadata": metadata or {}
    }

    # Send to logging service (e.g., DataDog, CloudWatch)
    send_to_monitoring(log_entry)
```