# Product Ready — Positioning & Messaging

## The one-line positioning

**Product Ready is the AI-native Spec-Driven Development system for Product Owners.**

---

## The shift happening right now

AI coding tools — Copilot, Cursor, Claude Code — have made writing code faster than ever. But they have exposed a problem that was already there:

> **Garbage in, garbage out.**
> AI generates code confidently from whatever spec it is given — including a bad one.

The bottleneck is no longer how fast developers can write code. The bottleneck is how clearly Product Owners can define what to build.

Teams that understand this are converging on a model:

```
PRD → BDD Spec (THE SPEC) → [AI: Tests + Code] → Acceptance
```

This is **Spec-Driven Development** — and Product Ready is the system that makes it work.

---

## The problem in concrete terms

A Product Owner describes a feature. A developer prompts an AI tool. The AI writes 400 lines of code in 3 minutes.

Then the questions begin:
- What happens when the session expires mid-checkout?
- Does this need to work for guest users?
- What does "success" look like — is it the click, the confirmation, or the backend record?
- Who approved the edge case where the user has two accounts?

These are not coding questions. They are **missing product decisions**. And they don't surface until the code is already written.

**Product Ready catches them before the spec is written.**

---

## How it works

Product Ready is not a template. It is a structured workflow with adaptive depth, enforced guardrails, and a clear chain of accountability:

### The chain

```
Discovery → Challenge → PRD → BDD Spec (THE SPEC) → [AI: Tests + Code] → Acceptance
```

Each step feeds the next. Nothing is generated without what comes before it being complete.

| Step | What it produces | Why it matters |
|------|-----------------|----------------|
| Discovery | Validated problem definition | Ensures you're solving the right thing |
| Challenge | Tested assumptions, identified risks | Stops you building on a wrong premise |
| PRD | Requirements (REQ-*), business rules (BR-*), success metrics | The "what" and "why" |
| **BDD Spec** | Given/When/Then scenarios (BS-*) | **THE SPEC — drives everything downstream** |
| Test Spec | Test cases (TS-*) derived from BDD Spec | AI-generated tests anchored to real behaviour |
| Build | Implementation guided by BDD Spec | Code aligned to intent, not assumption |
| Acceptance | Scenarios pass, behaviour matches intent | Done means done |

### The BDD Spec is not optional

The BDD Spec (Behavior-Driven Development, Given/When/Then) is the canonical source of truth. It is:
- **What AI test generators use** — each scenario maps directly to a test case
- **What AI code generators use** — the spec is a precise prompt, not a vague description
- **What QA validates against** — acceptance is defined by the spec, not by memory
- **What engineering builds to** — no interpretation required

**Without a complete BDD Spec, you are guessing. With one, you are building.**

---

## The guardrails

Product Ready enforces 8 non-negotiable quality rules on every output:

| # | Guardrail | What it prevents |
|---|-----------|-----------------|
| 1 | No Missing Decisions | TBDs reaching engineering |
| 2 | Testability | Untestable requirements becoming accepted |
| 3 | No Duplicates or Conflicts | Contradictory rules surviving to implementation |
| 4 | Metric Integrity | Success metrics without baselines or targets |
| 5 | Security & Compliance | SOC2, NIST, PCI, HIPAA gaps caught late |
| 6 | UI is First-Class | UI states and accessibility as afterthoughts |
| 7 | Evidence Over Assumption | Guesses shipped as facts |
| 8 | Spec Integrity | Code or tests generated from an incomplete BDD Spec |

Guardrail #8 is the AI-era addition. It exists because AI tools are honest executors — they will generate code from a broken spec without complaint.

---

## Who it is for

### Primary: Product Owners and Product Managers

You are responsible for the spec. If the spec is wrong, the product is wrong — regardless of how cleanly the code was written.

Product Ready gives you a structured process and a validated output (the BDD Spec) that your AI tools and your engineering team can use directly.

### Secondary: Engineering leads

You receive the BDD Spec. Every scenario in it maps to a test case. Every test case is anchored to a business requirement. When something is ambiguous, you can point to the spec — not to a Slack message from three weeks ago.

### Tertiary: QA and test engineers

Acceptance is defined by the BDD Spec, not by individual judgment. You don't have to interpret what "done" means — the scenarios tell you.

---

## What makes Product Ready different

### Not just BDD
BDD alone tells you how to write scenarios. Product Ready tells you how to derive the right scenarios from validated discovery and a challenged PRD. The BDD Spec is the output of a complete thinking process — not the starting point.

### Not just a template
Templates produce completed fields, not correct decisions. Product Ready asks questions, challenges assumptions, flags missing decisions, and enforces quality before anything is written.

### Not just an AI prompt
Product Ready is a workflow with teeth. The guardrails are non-negotiable. The chain is enforced. You cannot reach the BDD Spec step with unresolved decisions — the skill will stop you.

### AI-native by design
The BDD Spec format is optimized for AI consumption. Given/When/Then scenarios are precise, unambiguous, and directly usable as AI prompts for test and code generation. Teams using Product Ready spend less time prompting AI tools because their specs are already structured correctly.

---

## The competitive framing

| Approach | What it produces | What it misses |
|----------|-----------------|----------------|
| TDD only | Correct code | Correct product |
| BDD only | Correct intent | Correct implementation |
| Spec-Driven without BDD | Fast generation | Verified correctness of the spec |
| **Product Ready** | **Correct intent + correct implementation + verified spec** | Nothing |

---

## Adapters: where it works

| Platform | Status |
|----------|--------|
| Claude Code (SKILL.md) | Production — `/product-ready` slash command |
| OpenAI (system prompt) | Production — paste into any GPT-4o model |
| Slack + Jira | Production — bot with BDD Spec → Jira export |

---

## The tagline options (for consideration)

1. **"Spec first. Code second. Acceptance always."**
2. **"The spec is the product. Everything else is execution."**
3. **"BDD Spec → AI Code → Shipped right."**
4. **"Stop prompting. Start speccing."**

---

## Call to action

**For individuals:** Install the Claude Code skill in 60 seconds.
```bash
mkdir -p ~/.claude/skills/product-ready
cp adapters/anthropic/SKILL.md ~/.claude/skills/product-ready/SKILL.md
```
Then type `/product-ready` in Claude Code.

**For teams:** Deploy the Slack bot — your Product Owners write specs in Slack, stories land in Jira automatically.

**For contributors:** The system is open source (Apache 2.0). The workflow is the moat — the guardrails, escalation triggers, and testability rule are protected invariants. Everything else is open for improvement.

→ [GitHub Repository](https://github.com/YOUR_ORG/product-ready)
→ [CONTRIBUTING.md](../CONTRIBUTING.md)
