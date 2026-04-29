# Prioritization Template

Use this template at all three prioritization levels. See Guardrails #15–#18 and the
Multi-Level Prioritization Model in `core/product-ready-core.md`.

**Declare context before scoring:**
- Company stage: [ ] Startup  [ ] Growth  [ ] Enterprise
- Prioritization level: [ ] Strategic  [ ] Solution  [ ] Delivery
- Quarter / sprint: [e.g. Q3 2026 / Sprint 14]

---

## Level 1 — Strategic Prioritization

*Answers: Should we work on this problem at all?*
*Run before Discovery. Gate: do not proceed to Discovery if score is low.*

### Initiative scoring

| Criterion | Weight | Score (1–5) | Weighted | Notes |
|-----------|--------|-------------|----------|-------|
| Strategic alignment — serves active OBJ-*/KR-* | 30% | | | |
| Customer impact — users affected, severity | 25% | | | |
| Business value — revenue / retention / risk / compliance | 25% | | | |
| Confidence — how well do we understand the problem? | 20% | | | |
| **Weighted total** | 100% | | **/5.0** | |

**Threshold:** Score ≥ 3.5 to proceed. Score < 3.0 → deprioritize. 3.0–3.5 → revisit next quarter.

### Prioritization justification (Guardrail #15)

**Why this problem, why now:**
> [e.g. "CSV export is the #3 churn reason in support tickets. Q3 is our last window before
> enterprise renewal season. If we miss this, we risk 12 enterprise renewals in Q4."]

**What we are NOT doing to make room for this:**
> [e.g. "Deferring the mobile app redesign (was planned for Q3) and the Linear integration."]

**Consequence of delaying one quarter:**
> [e.g. "We enter enterprise renewal season without a capability competitors launched in June.
> Risk: 3–5 churned accounts = ~$180K ARR."]

### Trade-off declaration (Guardrail #16)

| Deprioritized initiative | Why ranked lower | Risk accepted | Re-prioritization trigger |
|--------------------------|-----------------|---------------|--------------------------|
| Mobile app redesign | Lower urgency, no churn signal | UX debt accumulates | NPS drops below 40 or churn spikes |
| Linear integration | No customer request volume | — | 3+ enterprise deals blocked by this |

---

## Level 2 — Solution Prioritization

*Answers: Which approach and scope should we pursue?*
*Run after Challenge, before PRD. Gate: PRD scope must reflect only Must + approved Should.*

### MoSCoW triage

| Capability | Must / Should / Could / Won't | Reason |
|------------|-------------------------------|--------|
| [e.g. CSV export of filtered view] | Must | Core ask from 12 churned accounts |
| [e.g. Scheduled export (email)] | Should | High value but not blocking adoption |
| [e.g. Excel format] | Could | Requested by 2 accounts, low churn signal |
| [e.g. PDF export] | Won't (this release) | Not in any support ticket |

### Solution option scoring (if multiple approaches exist)

| Option | Impact | Effort | Risk | Confidence | Recommendation |
|--------|--------|--------|------|------------|----------------|
| Option A: CSV only | H | M | L | H | **Proceed** |
| Option B: CSV + Excel + PDF | H | H | M | M | Defer Excel/PDF |

**Selected scope:** [Option A — CSV only]

**Non-goals (must appear in PRD):**
- [Excel and PDF formats — not this release]
- [Scheduled / automated export — next quarter]

---

## Level 3 — Delivery Prioritization

*Answers: What do we build first within confirmed scope?*
*Run after Test Spec, before Issues. Gate: every story must be scored and justified.*

### RICE scored backlog

| # | Story | Reach | Impact | Confidence | Effort | RICE | Cost of Delay | Justification |
|---|-------|-------|--------|------------|--------|------|---------------|---------------|
| 1 | Export button + CSV generation | 500/wk | H (3) | H (1.0) | M (2) | 750 | High | Core capability — nothing else works without it |
| 2 | Column selection UI | 500/wk | M (2) | H (1.0) | M (2) | 500 | Medium | Users need control; without it, exports are noisy |
| 3 | Export history / audit log | 200/wk | L (1) | M (0.8) | M (2) | 80 | Low | Compliance nice-to-have; not blocking adoption |

**RICE formula:** (Reach × Impact × Confidence) / Effort
**Cost of Delay:** High = blocks adoption or revenue / Medium = slows adoption / Low = minor inconvenience

### Trade-off declaration (Guardrail #16)

| Deprioritized story | Why ranked lower | Risk accepted by delaying | Re-prioritization trigger |
|---------------------|-----------------|--------------------------|--------------------------|
| Export history / audit log | Low reach, low urgency | Compliance gap if enterprise requires it | SOC2 audit requirement confirmed |
| Scheduled export | Out of scope this release | Power users must do manual export | 3+ enterprise deals request this |

### Re-prioritization conditions (Guardrail #18)

*What would change the order of this backlog?*

| Trigger | Action |
|---------|--------|
| Effort estimate for story #2 increases >50% | Re-score, consider deferring column selection |
| Compliance team confirms audit log is SOC2 required | Promote story #3 to #2 |
| Competitor ships scheduled export | Elevate scheduled export into this release |

---

## Prioritization Decision Log

*Record every prioritization decision. Provides audit trail for stakeholder questions.*

| Date | Level | Decision | Decider | Evidence | Trade-off accepted |
|------|-------|----------|---------|----------|--------------------|
| [date] | Strategic | Approved CSV export for Q3 | [name] | 12 churned accounts, $180K ARR risk | Deferred mobile redesign |
| [date] | Solution | Scoped to CSV only | [name] | Low signal for Excel/PDF | PDF deferred to Q4 |
| [date] | Delivery | Export button before column selection | [name] | Core path must work first | Column UI in sprint 2 |

---

## Prioritization Health Check

Run at the start of each sprint or quarter review:

| Check | Status | Notes |
|-------|--------|-------|
| Every item in backlog has a justification | [ ] Pass / [ ] Fail | |
| Trade-off Declaration is complete | [ ] Pass / [ ] Fail | |
| Re-prioritization triggers are defined | [ ] Pass / [ ] Fail | |
| No item was re-prioritized by opinion alone | [ ] Pass / [ ] Fail | |
| Deprioritized items have a review date | [ ] Pass / [ ] Fail | |
| Priority aligns to current OKR/KR status | [ ] Pass / [ ] Fail | |
