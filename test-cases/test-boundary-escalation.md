# Test Case: Boundary Escalation - Simple to Complex

## User Input
"Add a search button" (initial)
Follow-up context reveals: "Actually it needs to search across 5 databases with real-time sync"

## Expected Behavior
- **Trigger:** Yes (matches "add", "feature")
- **Mode:** Fast initially, then escalate to Full when complexity revealed
- **First Response:** Simple clarification questions
- **Escalation Point:** When multi-database complexity discovered
- **Output:** Escalate to full workflow with data integration requirements
- **Workflow Steps:** Start Fast → Escalate to Full → Discovery → Challenge → PRD → Behavior → Test

## Validation Notes
- Start with minimal mode
- Dynamically escalate based on revealed complexity
- Include data consistency and performance requirements