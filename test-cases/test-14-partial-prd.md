# Test Case 14: Partial PRD Review (Enterprise)

## User Input
"Here is my PRD" (provides partial PRD)

## Expected Behavior
- **Trigger:** Yes (matches "review", "PRD")
- **Mode:** Standard
- **First Response:** Review for missing decisions, weak metrics, missing behavior
- **Output:** Gap analysis with recommendations
- **Workflow Steps:** Guardrails → Challenge → fill gaps

## Validation Notes
- Surface missing elements
- Suggest improvements