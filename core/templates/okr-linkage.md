# OKR Linkage Template

Use this template at Step 1 (Strategy/Goal) and Step 4 (PRD) to declare how a piece of product
work connects to the company or product OKRs. See Guardrail #14 (OKR Alignment Rule).

Every PRD must complete this template before proceeding to Step 5 (BDD Spec).

---

## OKR Linkage

**Objective:** OBJ-[N] — [Full objective text, e.g. "Become the go-to platform for SMB inventory teams by Q3"]

**Key Result:** KR-[N] — [Full KR text with current value and target]
- Current value: [e.g. 41%]
- Target value: [e.g. 60%]
- Deadline: [e.g. end of Q3 2026]
- Gap to close: [e.g. 19 percentage points]

**Feature / PRD:** [Feature name]
**Team:** [Team name or owner]
**Quarter:** [e.g. Q2 2026]

---

## Contribution Hypothesis

*Complete all three before proceeding. Vague answers = OKR decoration — rewrite.*

**1. Behaviour change hypothesis**
What specific behaviour change in the user does this feature drive?
> [e.g. "Teams that use CSV export will re-engage with the platform on a weekly cadence because
> they integrate the data into their existing workflows, reducing their reason to churn."]

**2. KR movement hypothesis**
How does that behaviour change translate into KR movement?
> [e.g. "Export-adopting teams show 23% lower 30-day churn in our pilot cohort (n=47).
> If export adoption reaches 40% of active teams, we model a 12–15 point retention lift."]

**Evidence strength:** Strong / Medium / Weak
**Evidence source:** [e.g. pilot data, support ticket analysis, user interviews, assumption]

**3. Falsifiability**
What data at 30/60/90 days would prove OR disprove the hypothesis?
> [e.g. "If export adoption ≥ 40% AND 30-day retention does not increase by ≥ 8 points
> within 60 days of GA, the causal link is broken and we must revise the hypothesis."]

---

## Validation Plan

**Leading indicator (feature metric):**
[The metric tracked within the feature that predicts KR movement]
- Metric: [e.g. export adoption rate]
- Target: [e.g. ≥ 40% of active teams within 60 days of GA]
- Measurement method: [e.g. event tracking: `export.completed` event per team]

**Lagging indicator (KR metric):**
[The KR metric tracked at 30/60/90 days post-ship]
- Metric: [e.g. 30-day team retention]
- Measurement points: 30d / 60d / 90d post-GA
- Baseline snapshot date: [date the baseline was captured]

**Attribution approach:**
[How KR movement will be isolated from other concurrent changes]
> [e.g. "Holdout group: 10% of teams will not see the export feature for 60 days.
> Compare retention between export-exposed and holdout cohorts."]

**Concurrent work that may affect the same KR:**
| Initiative | Expected KR impact | How to separate |
|------------|--------------------|-----------------|
| [e.g. Onboarding redesign] | [e.g. +5 points retention] | [e.g. different user cohort] |

---

## Non-OKR Declaration *(complete only if this work does not serve a current OKR)*

**Reason:** [ ] Regulatory / legal  [ ] Technical debt  [ ] Security  [ ] Incident response  [ ] Infrastructure

**Explanation:**
> [e.g. "SOC2 Type II requires audit logging for all admin actions. This is a compliance
> requirement with a hard deadline, not an OKR initiative."]

**Work owner approval:** [name / role]

---

## OKR Decoration Check

Before finalising, confirm the contribution hypothesis passes all three:

| Check | Status | Notes |
|-------|--------|-------|
| Behaviour change is specific and named | [ ] Pass / [ ] Fail | |
| KR movement is quantified with evidence | [ ] Pass / [ ] Fail | |
| Hypothesis is falsifiable (clear disproof condition) | [ ] Pass / [ ] Fail | |
| Attribution plan handles concurrent initiatives | [ ] Pass / [ ] Fail | |

**All four must pass before proceeding to BDD Spec.**
If any fail: the OKR linkage is decoration — rewrite before continuing.

---

## Measure Checkpoint *(complete at Step 12, post-ship)*

**Date:** [measurement date]
**Days since GA:** [30 / 60 / 90]

| Level | Metric | Before | After | Delta | Target | Status |
|-------|--------|--------|-------|-------|--------|--------|
| Feature | [export adoption] | — | [47%] | — | 40% | ✅ Met |
| KR | [30-day retention] | [41%] | [54%] | +13pp | 60% | ⚠️ Partial |

**KR remaining gap:** [54% vs 60% target — 6 points remaining]

**Attribution note:**
> [e.g. "Export feature contributed ~8pp of the 13pp lift. Onboarding redesign contributed ~5pp
> (based on holdout cohort comparison). Total gap to KR target: 6 points."]

**Hypothesis verdict:**
- [ ] ✅ Confirmed — feature moved KR as predicted
- [ ] ⚠️ Partial — feature moved KR but less than predicted — refine hypothesis
- [ ] ❌ Disproved — feature did not move KR — causal chain was wrong, revisit

**Next lever (if gap remains):**
> [e.g. "Export adoption explains ~65% of the retention model. The remaining gap likely
> requires improving the onboarding flow for teams who never reach the export feature."]
