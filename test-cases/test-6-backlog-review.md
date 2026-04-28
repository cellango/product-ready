# Test Case 6: Backlog Review (Standard)

## User Input
"Review these stories"

## Expected Behavior
- **Trigger:** Yes (matches "review", "backlog")
- **Mode:** Standard
- **First Response:** Apply guardrails: duplicate detection, INVEST review, missing decisions
- **Output:** Review feedback with gaps identified
- **Workflow Steps:** Guardrails → Issues (if needed)

## Validation Notes
- Detect missing decisions
- Check testability
- Flag duplicates/conflicts