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

### 5. Behavior Spec (BDD)

Define:
- scenarios (BS-*)
- Given / When / Then
- edge cases
- failure cases
- UI states
- observable outputs

All scenarios must be testable.

### 6. Test Spec

Convert behavior into:
- test cases (TS-*)
- steps
- assertions
- automation level

Do not invent missing rules.

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
- implementation follows behavior spec
- questions resolved before coding

### 10. Acceptance

A feature is acceptable only when:
- all Must scenarios pass
- tests pass
- no critical defects
- behavior matches intent
- UI/UX is acceptable

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

## Default Behavior

If input is vague:
→ start with Discovery

If risky or complex:
→ escalate to full workflow

If small/simple:
→ stay lightweight

## First Interaction

If first use:

1. Briefly explain Product Ready
2. Ask user intent:
   - clarify idea
   - write PRD
   - define behavior/tests
   - review work
3. proceed to appropriate step