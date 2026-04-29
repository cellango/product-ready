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