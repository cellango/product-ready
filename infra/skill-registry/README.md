# product-ready

**AI-native Spec-Driven Development for Product Owners.**

> Invoke with `/product-ready` — or let Claude detect intent automatically from your message.

---

## What this skill does

Product Ready guides Product Owners through a structured workflow from a vague idea to a complete, AI-ready BDD Spec — then helps generate tests and code from that spec.

The development chain:

```
PRD → BDD Spec (THE SPEC) → [AI: Tests + Code] → Acceptance
```

The BDD Spec is the canonical source of truth. It is scored for quality before any AI generation is allowed. Each scenario becomes a self-contained, copy-paste-ready AI prompt.

---

## When Claude loads this skill

Claude loads `/product-ready` automatically when you mention:

- PRD, product requirements, user stories, acceptance criteria
- BDD spec, behavior spec, Given/When/Then
- Backlog review, feature design, readiness review
- Generate tests, generate code from spec, score my spec
- Spec-driven development

Or invoke it directly: `/product-ready [your input]`

---

## What you get

### 13-step adaptive workflow

| Depth | When | Output |
|-------|------|--------|
| Lightweight | Bug fixes, small changes | Acceptance criteria |
| Standard | Most product work | PRD + BDD Spec |
| Full | Compliance, financial, AI systems | Complete lifecycle + Spec Quality Score |

Auto-escalates on financial, security, compliance, or multi-system signals.

### 8 enforced guardrails

1. **No Missing Decisions** — TBDs flagged before they reach engineering
2. **Testability** — untestable requirements blocked
3. **No Duplicates or Conflicts** — conflicting rules normalised to BR-* format
4. **Metric Integrity** — every metric needs baseline, target, timeframe, decision rule
5. **Security & Compliance** — SOC2, NIST, PCI, HIPAA mapped automatically
6. **UI is First-Class** — all UI states, transitions, accessibility included
7. **Evidence Over Assumption** — evidence labelled Strong / Medium / Weak
8. **Spec Integrity** — BDD Spec scored Complete / Partial / Incomplete before AI generation

### Spec Quality Score (Guardrail #8)

Before generating tests or code, the skill scores the BDD Spec across 5 dimensions:

| Dimension | Level |
|-----------|-------|
| Coverage — happy/edge/failure paths | Critical |
| Clarity — no vague Then clauses | Critical |
| Linkage — every scenario linked to REQ-* | Required |
| Decisions — no open decisions | Required |
| UI states (if UI involved) | Conditional |

**Complete** → generate. **Partial** → fix first. **Incomplete** → STOP.

### Generate from Spec (Step 5b)

Say "generate tests from this spec" or "generate code". The skill:
1. Scores the spec
2. Formats each BDD scenario as a self-contained AI prompt
3. Outputs one ready-to-paste block per scenario

### Three-tier First Interaction

1. **Intent clear** ("write a PRD for X") → proceeds directly, no intro
2. **Domain known, task unclear** ("I need to improve checkout") → asks what the specific problem is
3. **No signal** ("I have an idea") → one sentence + one focused question

---

## Example interactions

**Write a PRD:**
```
You: Write a PRD for a CSV export feature
Product Ready: [asks 3 minimum questions, then produces PRD with REQ-*, BR-*, metrics]
```

**Score and generate from a BDD Spec:**
```
You: Generate tests from this spec [paste BS-* scenarios]
Product Ready: Spec Quality Score — Coverage: Pass, Clarity: Fail (BS-003 Then clause uses "should")
              Fix BS-003 Then clause before generating.
```

**Backlog review:**
```
You: Review my backlog for missing decisions
Product Ready: [applies all 8 guardrails, surfaces MPDs, flags untestable stories]
```

---

## Artifact numbering convention

| Prefix | Artifact |
|--------|----------|
| REQ-* | Requirements |
| BR-* | Business rules |
| BS-* | BDD scenarios |
| TS-* | Test cases |
| MPD | Missing Product Decision |

---

## Source & license

- **Repository:** https://github.com/cellango/product-ready
- **License:** Apache 2.0
- **Version:** 1.2.0
- **Tests:** 135 passing (structural integrity + unit tests)
