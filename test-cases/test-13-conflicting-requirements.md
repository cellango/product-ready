# Test Case 13: Conflicting Requirements (Enterprise)

## User Input
"Alert in 30 seconds" (later) "Alert in 60 seconds"

## Expected Behavior
- **Trigger:** Yes (matches "requirements")
- **Mode:** Standard
- **First Response:** Detect contradiction, trigger conflict resolution
- **Output:** Normalized BR-* with resolved conflict
- **Workflow Steps:** Guardrails (conflict detection) → Challenge → PRD

## Validation Notes
- Flag contradictions
- Require decision on which to use