# Test Case: Default Behavior - Vague Input

## User Input
"I want to improve user experience"

## Expected Behavior
- **Trigger:** Yes (matches "improve", "user experience")
- **Mode:** Standard (default for vague but relevant)
- **First Response:** Start with Discovery: What specific problems? What users? What success looks like?
- **Output:** Discovery questions, then proceed based on answers
- **Workflow Steps:** Discovery → Challenge → appropriate depth

## Validation Notes
- Default to Discovery for vague inputs
- Ask clarifying questions before generating artifacts
- Adapt based on discovery answers