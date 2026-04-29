# BDD Spec — AI-Optimised Scenario Template

Use this template when the BDD Spec will be used to drive AI code or test generation.
Each scenario becomes a self-contained AI prompt. See `core/product-ready-core.md`
→ "BDD Spec → AI Prompt Mapping" for the rules that make scenarios AI-ready.

**Before writing scenarios, confirm:**
- Guardrail #11: you will write at least 1 happy path + 1 failure + 1 edge case per REQ-*
- Guardrail #12: no banned ambiguous terms ("should", "user-friendly", "fast", etc.)
- Guardrail #8: all Then clauses will be exact, observable, and include concrete values

---

## Feature: [Feature name from PRD]

**Linked PRD:** [REQ-NNN title]
**Spec status:** [ ] Draft  [ ] Under review  [ ] Complete

---

## Scenario [BS-001]: [Happy path title]

**Type:** Happy path
**Priority:** Must / Should / Could

**Given** [system state — specific entities, roles, named values; no assumed context]
**When** [one user action or system event — one trigger only]
**Then** [exact, observable outcome — HTTP status + body, UI element + text, DB record + field values, log entry, or event name]

**Test data:**
- Input: [exact value(s) used in this scenario, e.g. `username: "alice@example.com"`, `amount: 99.99`]
- Precondition state: [e.g. `orders table has 0 rows for user_id=42`]
- Expected output: [e.g. `{"status": "created", "order_id": "ord-123"}`]

**Pass condition:** [exact assertion that must be true — mirrors the Then clause]
**Fail condition:** [what would make this test fail — wrong status, missing field, wrong value]

**Requirements:** REQ-[NNN] — [one-line requirement text]
**Business Rules:** BR-[NNN] — [one-line rule text]
**Automation:** Automatable — Unit / Integration / E2E / Manual only / Partially automatable

**AI generation prompt** (copy-paste ready):

    Scenario BS-001: [title]
    Type: Happy path

    Given [preconditions — exact entities and values]
    When [one action]
    Then [exact assertion]

    Test data: [input values, precondition state, expected output]
    Pass condition: [exact assertion]
    Fail condition: [what breaks it]

    Requirements: REQ-[NNN] — [text]
    Business Rules: BR-[NNN] — [text]
    Automation: [level]
    Context: [any API endpoints, data schemas, or technical constraints]

    Generate: test function

---

## Scenario [BS-002]: [Edge case title]

**Type:** Edge case
**Priority:** Must / Should / Could

**Given** [edge condition — explicit boundary value or unusual but valid state]
**When** [action]
**Then** [exact behaviour at the boundary]

**Test data:**
- Input: [boundary value, e.g. `quantity: 0`, `filename: ""`, `amount: 10000.00` (limit)]
- Precondition state: [system state at the boundary]
- Expected output: [exact output at boundary]

**Pass condition:** [assertion that confirms boundary is handled correctly]
**Fail condition:** [what would indicate the boundary is NOT handled — e.g. 500 error, wrong truncation]

**Requirements:** REQ-[NNN]
**Business Rules:** BR-[NNN]
**Automation:** Automatable — Unit / Integration / E2E

**AI generation prompt:**

    Scenario BS-002: [title]
    Type: Edge case

    Given [edge condition — exact boundary value]
    When [action]
    Then [exact boundary behaviour]

    Test data: [boundary value, precondition state, expected output]
    Pass condition: [assertion]
    Fail condition: [what breaks it]

    Requirements: REQ-[NNN] — [text]
    Automation: [level]
    Context: [boundary value, constraint, data type]

    Generate: test function

---

## Scenario [BS-003]: [Failure / error title]

**Type:** Failure
**Priority:** Must / Should / Could

**Given** [failure precondition — missing data, invalid input, expired token, system unavailable]
**When** [action]
**Then** [exact error response — status code, error message text, fallback behaviour, audit log entry]

**Test data:**
- Input: [exact invalid or missing value, e.g. `token: "expired-jwt"`, `email: "notanemail"`]
- Precondition state: [what makes this a failure — e.g. `payment_service returns 503`]
- Expected output: [exact error format, e.g. `HTTP 422 {"error": "invalid_email"}`]

**Pass condition:** [exact assertion confirming error is handled correctly]
**Fail condition:** [what would indicate the failure is NOT handled — e.g. 200 returned, no error message, no rollback]

**Requirements:** REQ-[NNN]
**Business Rules:** BR-[NNN]
**Automation:** Automatable — Unit / Integration

**AI generation prompt:**

    Scenario BS-003: [title]
    Type: Failure

    Given [failure condition — exact invalid input or system state]
    When [action]
    Then [exact error handling — status, message, rollback, audit]

    Test data: [input, precondition state, expected error output]
    Pass condition: [assertion]
    Fail condition: [what breaks it]

    Requirements: REQ-[NNN] — [text]
    Automation: [level]
    Context: [error type, expected response format, logging behaviour]

    Generate: test function

---

## Scenario [BS-004]: [UI state title] *(include only if UI involved)*

**Type:** UI state
**Priority:** Must / Should / Could

**Given** [system state affecting UI — named component, data condition, user role]
**When** [user action or system event]
**Then** [exact UI change — element visible/hidden/disabled, text content, error banner, ARIA label]

**Test data:**
- Input: [user action or event that triggers state change]
- Precondition state: [UI state before the trigger]
- Expected output: [exact UI state after — element selector, text content, CSS state]

**Pass condition:** [exact assertion, e.g. `button[data-id="submit"] is disabled`, `#error-msg text == "Email is required"`]
**Fail condition:** [what would indicate the UI state is wrong — element missing, wrong text, wrong state]

**Accessibility:** [tab order, ARIA label, screen reader announcement]

**Requirements:** REQ-[NNN]
**Automation:** Automatable — E2E / Manual only (if subjective visual assessment required)

**AI generation prompt:**

    Scenario BS-004: [title]
    Type: UI state

    Given [system state — named component and data]
    When [trigger]
    Then [exact UI assertion — element, text, state]

    Test data: [trigger input, precondition UI state, expected post-trigger UI state]
    Pass condition: [assertion — selector, text, or state]
    Fail condition: [what breaks it]

    Requirements: REQ-[NNN] — [text]
    Automation: E2E
    Context: [component name, selector, framework, accessibility requirement]

    Generate: E2E test

---

## Scenario [BS-005]: [Security / compliance title] *(include if security applies)*

**Type:** Security
**Priority:** Must

**Given** [actor without authorisation, or attack precondition — e.g. valid user without admin role]
**When** [action that should be blocked — e.g. DELETE /admin/users/42]
**Then** [exact rejection response — HTTP 401/403, redirect URL, audit log entry, no data returned]

**Test data:**
- Input: [exact request, e.g. `DELETE /admin/users/42` with `role: "viewer"` JWT]
- Precondition state: [actor state — valid session, wrong role, expired token]
- Expected output: [exact rejection, e.g. `HTTP 403 {"error": "forbidden"}` + audit log: `"action": "unauthorized_delete"`]

**Pass condition:** [assertion confirming rejection — status, message, audit entry, no data leak]
**Fail condition:** [what would indicate a security failure — 200 returned, data exposed, no audit log]

**Compliance:** [SOC2 / NIST / PCI / HIPAA control reference]
**Automation:** Automatable — Unit / Integration

**AI generation prompt:**

    Scenario BS-005: [title]
    Type: Security

    Given [unauthorised actor or attack precondition — exact role, token, or request]
    When [action that should be blocked]
    Then [exact rejection — status, message, audit entry, no data leak]

    Test data: [exact request, actor state, expected rejection output]
    Pass condition: [assertion]
    Fail condition: [what indicates a security failure]

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
| Observability — Then clause names system layer (UI/API/DB/log/event) | [ ] Pass / [ ] Fail | |
| Linkage — every BS-* linked to REQ-* | [ ] Pass / [ ] Fail | |
| Decisions — no open [MPD] markers | [ ] Pass / [ ] Fail | |
| Example data — concrete values in every scenario | [ ] Pass / [ ] Fail | |
| UI states — all defined (if UI involved) | [ ] Pass / [ ] N/A | |

**Score:** [ ] Complete — proceed  [ ] Partial — fix listed items  [ ] Incomplete — STOP

---

## Automation Readiness Summary

(Guardrail #13 — complete after all scenarios are written)

| BS-* | Type | Automation | Level | Notes |
|------|------|------------|-------|-------|
| BS-001 | Happy path | Automatable | Unit | |
| BS-002 | Edge case | Automatable | Integration | |
| BS-003 | Failure | Automatable | Unit | |
| BS-004 | UI state | Automatable | E2E | |
| BS-005 | Security | Automatable | Integration | |

**Automatable: N/N (N%)** — [ ] ≥80% Automation Ready  [ ] <50% Automation Risk

---

## RTM-lite Row (add to `rtm-lite.md` when Test Spec is complete)

| REQ-* | Requirement | BS-* | TS-* | Coverage | Automation |
|-------|-------------|------|------|----------|------------|
| REQ-[NNN] | [text] | BS-001, BS-002, BS-003, BS-004, BS-005 | TS-[NNN], ... | ✅ Full | Auto: N/N |
