# Product-Ready: Product Foundation

## Product Vision

Product-Ready is an AI-powered assistant that helps Product Owners, Product Managers, and delivery teams create clear, testable, measurable, and ready-for-engineering product work. It eliminates ambiguity, missing decisions, and rework by providing a structured, adaptive workflow that scales from simple bug fixes to complex enterprise systems.

### Target Users
- Product Owners
- Product Managers
- Business Analysts
- Delivery Leads
- Engineering Teams (for clarity on requirements)

### Core Outcomes
- Work is clear: no ambiguity in what to build
- Testable: every requirement has acceptance criteria
- Measurable: success metrics are defined and trackable
- Non-duplicative: conflicts and duplicates are detected
- Secure and compliant: frameworks like SOC2, NIST, PCI are integrated
- Usable: UI/UX is first-class, with accessibility
- Ready for engineering: handoff is seamless, acceptance is defined

### Primary Use Cases
- PRD creation and review
- Behavior specification (BDD-style scenarios)
- Acceptance criteria definition
- Readiness reviews for backlogs or features
- Missing decision detection
- Prioritization guidance

## Success Metrics

### Adoption Metrics
- Sessions started: number of times the skill is invoked
- Workflows completed: percentage of sessions that reach acceptance
- User retention: repeat usage over time

### Quality Metrics
- Reduction in missing decisions: fewer "Missing Product Decision" flags in reviews
- Testable stories: percentage of output stories that are INVEST-compliant and testable
- Review pass rate: how often reviewed work passes without major gaps

### Velocity Metrics
- Time-to-ready: average time from vague idea to engineering-ready work item
- Handoff efficiency: reduction in back-and-forth during development

## MVP Scope

The MVP focuses on the core workflow for standard product work, with adaptive depth.

### Core Workflow Stages
1. Discovery / Validation
2. Challenge (critical evaluation)
3. PRD (structured definition)
4. Behavior Spec (BDD scenarios)
5. Test Spec (test cases)
6. Prioritization
7. Issue Breakdown
8. Acceptance Readiness

### Guardrails
- Missing Product Decision detection
- Testability enforcement
- Duplicate/conflict detection
- Metric integrity checks
- UI state coverage

### Basic Trigger Logic
- Activation on relevant phrases (PRD, requirements, etc.)
- Intent detection to map to workflow steps
- Adaptive depth: Fast, Standard, Full modes

## Architecture and Delivery Model

Product-Ready is delivered as a Claude/Anthropic skill (SKILL.md) that integrates into AI-assisted product management workflows.

### Why a Skill?
- On-demand activation for specific product tasks
- Bundled workflow logic and guardrails
- No external dependencies; runs within Claude's context

### Minimum Integration Path
- Hosted in `.github/skills/product-ready/SKILL.md` for workspace-specific use
- Can be copied to user-level prompts folder for personal use
- Triggered via natural language matching the description and trigger phrases

### Future Extensions
- Integration with tools like Jira, Notion for backlog sync
- Web-based UI for non-Claude users
- API for automated workflows