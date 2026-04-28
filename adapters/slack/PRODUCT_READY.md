# Product Ready - Slack Integration

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
- Include security scenarios in behavior specs
- Generate compliance test cases

### 6. UI is First-Class
- Define all UI states and transitions
- Ensure usability and accessibility standards
- Include UI scenarios in behavior specs
- Validate with user testing criteria

### 7. Evidence Over Assumption
For all claims and assumptions:
- Label evidence strength: Strong / Medium / Weak
- Prefer data-driven decisions
- Validate assumptions with cheapest tests

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

## Implementation Notes
- Use Slack's block kit for rich formatting
- Store conversation context in thread
- Support file uploads for PRDs/behavior specs
- Integrate with Slack's reminder system for follow-ups
