# Test Case: Escalation - High User Impact

## User Input
"Change the login flow for all 100k users"

## Expected Behavior
- **Trigger:** Yes (matches "change", "workflow")
- **Mode:** Full (escalate due to high user impact)
- **First Response:** Assess user impact, identify rollback needs
- **Output:** Full workflow with migration plan and monitoring
- **Workflow Steps:** Discovery → Challenge (impact assessment) → PRD → Behavior → Test → Release

## Validation Notes
- Recognize high user impact (100k users)
- Include migration and rollback planning
- Add monitoring and success metrics