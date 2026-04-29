# RTM-lite — Requirements Traceability Matrix

Use this template to verify that every requirement is specified (BDD Spec) and tested (Test Spec)
before the feature is accepted. Generate this matrix at the end of Step 6 (Test Spec) and again
at Step 10 (Acceptance). See Guardrails #9 (Acceptance Coverage Rule) and #10 (Bidirectional
Traceability Rule).

---

## Feature: [Feature name from PRD]

**Generated:** [date]
**Author:** [name or role]
**Status:** [ ] In progress  [ ] Coverage gaps present  [ ] RTM complete

---

## Traceability Matrix

| REQ-* | Requirement | BS-* Scenarios | TS-* Test Cases | Coverage | Automation |
|-------|-------------|----------------|-----------------|----------|------------|
| REQ-001 | [Requirement text] | BS-001, BS-002, BS-003 | TS-001, TS-002, TS-003 | ✅ Full | Auto: 3/3 |
| REQ-002 | [Requirement text] | BS-004 | — | ⚠️ No TS-* | — |
| REQ-003 | [Requirement text] | — | — | ❌ Gap | — |

**Coverage key:**
- ✅ Full — at least one BS-* AND at least one TS-* present
- ⚠️ Partial — BS-* present but no TS-*, or TS-* present but no BS-*
- ❌ Gap — no BS-* and no TS-* linked

---

## Scenario Completeness Check

For each REQ-*, confirm all three scenario types are present (Guardrail #11):

| REQ-* | Happy Path | Failure | Edge Case | Complete? |
|-------|------------|---------|-----------|-----------|
| REQ-001 | BS-001 | BS-002 | BS-003 | ✅ Yes |
| REQ-002 | BS-004 | — | — | ❌ Missing failure + edge case |

---

## Orphan Detection

List any BS-* or TS-* that are not linked to any REQ-* (Guardrail #10):

| ID | Type | Linked to | Status |
|----|------|-----------|--------|
| BS-007 | BDD Scenario | — | ❌ Orphan — assign to a REQ-* or remove |
| TS-005 | Test Case | — | ❌ Orphan — assign to a REQ-* or remove |

*(Leave empty if no orphans found)*

---

## Coverage Summary

| Metric | Count |
|--------|-------|
| Total requirements (REQ-*) | N |
| Requirements with full coverage (BS-* + TS-*) | N |
| Requirements with partial coverage | N |
| Requirements with no coverage (gaps) | N |
| Total BDD scenarios (BS-*) | N |
| Total test cases (TS-*) | N |
| Orphan BS-* | N |
| Orphan TS-* | N |
| Automatable scenarios | N (N%) |
| Partially automatable | N (N%) |
| Manual only | N (N%) |

**RTM Status:**
- [ ] ✅ Complete — all REQ-* have BS-* and TS-*, no orphans, ≥80% automatable
- [ ] ⚠️ Partial — coverage gaps or automation risk present (list below)
- [ ] ❌ Blocked — one or more REQ-* have no coverage → cannot accept

---

## Gaps to resolve before acceptance

*(List each gap with owner and target date)*

| Gap | Type | Owner | Due |
|-----|------|-------|-----|
| REQ-002 has no TS-* | Missing test case | [name] | [date] |
| REQ-003 has no BS-* or TS-* | Missing spec and test | [name] | [date] |
| BS-007 is an orphan | No linked requirement | [name] | [date] |
