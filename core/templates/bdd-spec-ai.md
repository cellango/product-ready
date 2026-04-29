# BDD Spec — AI-Optimised Scenario Template

Use this template when the BDD Spec will be used to drive AI code or test generation.
Each scenario becomes a self-contained AI prompt. See `core/product-ready-core.md`
→ "BDD Spec → AI Prompt Mapping" for the rules that make scenarios AI-ready.

---

## Feature: [Feature name from PRD]

**Linked PRD:** [REQ-NNN title]
**Spec status:** [ ] Draft  [ ] Under review  [ ] Complete

---

## Scenario [BS-001]: [Happy path title]

**Type:** Happy path
**Priority:** Must / Should / Could

**Given** [system state — specific entities, roles, values; no assumed context]
**When** [one user action or system event — one trigger only]
**Then** [exact, observable outcome — HTTP status, UI message, database record, etc.]

**Requirements:** REQ-[NNN] — [one-line requirement text]
**Business Rules:** BR-[NNN] — [one-line rule text]
**Automation:** Unit / Integration / E2E / Manual

**AI generation prompt** (copy-paste ready):

    Scenario BS-001: [title]
    Type: Happy path

    Given [preconditions]
    When [action]
    Then [exact assertion]

    Requirements: REQ-[NNN] — [text]
    Business Rules: BR-[NNN] — [text]
    Automation: [level]
    Context: [any API endpoints, data schemas, or technical constraints]

    Generate: test function

---

## Scenario [BS-002]: [Edge case title]

**Type:** Edge case
**Priority:** Must / Should / Could

**Given** [edge condition — explicit boundary value or unusual state]
**When** [action]
**Then** [exact behaviour at the boundary]

**Requirements:** REQ-[NNN]
**Business Rules:** BR-[NNN]
**Automation:** Unit / Integration / E2E / Manual

**AI generation prompt:**

    Scenario BS-002: [title]
    Type: Edge case

    Given [edge condition]
    When [action]
    Then [exact boundary behaviour]

    Requirements: REQ-[NNN] — [text]
    Automation: [level]
    Context: [boundary value, constraint]

    Generate: test function

---

## Scenario [BS-003]: [Failure / error title]

**Type:** Failure
**Priority:** Must / Should / Could

**Given** [failure precondition — missing data, invalid input, system down, etc.]
**When** [action]
**Then** [exact error response — status code, message text, fallback behaviour]

**Requirements:** REQ-[NNN]
**Business Rules:** BR-[NNN]
**Automation:** Unit / Integration / E2E / Manual

**AI generation prompt:**

    Scenario BS-003: [title]
    Type: Failure

    Given [failure condition]
    When [action]
    Then [exact error handling]

    Requirements: REQ-[NNN] — [text]
    Automation: [level]
    Context: [error type, expected response format]

    Generate: test function

---

## Scenario [BS-004]: [UI state title] *(include only if UI involved)*

**Type:** UI state
**Priority:** Must / Should / Could

**Given** [system state affecting UI]
**When** [user action or system event]
**Then** [exact UI change — element visible/hidden, text content, disabled state, etc.]

**Accessibility:** [tab order, ARIA label, screen reader text]

**Requirements:** REQ-[NNN]
**Automation:** E2E / Manual

**AI generation prompt:**

    Scenario BS-004: [title]
    Type: UI state

    Given [system state]
    When [trigger]
    Then [exact UI assertion — element, text, state]

    Requirements: REQ-[NNN] — [text]
    Automation: E2E
    Context: [component name, selector, framework]

    Generate: E2E test

---

## Scenario [BS-005]: [Security / compliance title] *(include if security applies)*

**Type:** Security
**Priority:** Must

**Given** [actor without authorisation, or attack precondition]
**When** [action that should be blocked]
**Then** [exact rejection response — HTTP 401/403, redirect, audit log entry]

**Compliance:** [SOC2 / NIST / PCI / HIPAA control reference]
**Automation:** Unit / Integration

**AI generation prompt:**

    Scenario BS-005: [title]
    Type: Security

    Given [unauthorised actor or attack precondition]
    When [action]
    Then [exact rejection — status, message, audit entry]

    Requirements: REQ-[NNN] — [text]
    Compliance: [framework + control]
    Automation: [level]

    Generate: test function

---

## Spec Quality Score

Run before generating tests or code (Guardrail #8):

| Dimension | Status | Notes |
|-----------|--------|-------|
| Coverage — happy paths present | [ ] Pass / [ ] Fail | |
| Coverage — edge cases present | [ ] Pass / [ ] Fail | |
| Coverage — failure paths present | [ ] Pass / [ ] Fail | |
| Clarity — no "should/may/typically" in Then | [ ] Pass / [ ] Fail | |
| Linkage — every BS-* linked to REQ-* | [ ] Pass / [ ] Fail | |
| Decisions — no open [MPD] markers | [ ] Pass / [ ] Fail | |
| UI states — all defined (if UI involved) | [ ] Pass / [ ] N/A | |

**Score:** [ ] Complete — proceed  [ ] Partial — fix listed items  [ ] Incomplete — STOP
