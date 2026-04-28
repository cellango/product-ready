#!/usr/bin/env python3
"""
Product Ready Build Script

Generates platform-specific adapters from core components.
"""

import os
import shutil
from pathlib import Path

def read_file(filepath):
    """Read file content."""
    with open(filepath, 'r') as f:
        return f.read()

def write_file(filepath, content):
    """Write content to file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

def build_anthropic_skill():
    """Build Anthropic SKILL.md from core components."""
    core = read_file('core/product-ready-core.md')
    guardrails = read_file('core/guardrails.md')

    # Anthropic-specific frontmatter
    frontmatter = """---
name: product-ready
description: Use this skill when working on product ideas, PRDs, requirements, user stories, acceptance criteria, backlog items, behavior specs, test plans, or readiness reviews. Helps Product Owners clarify ideas, write PRDs, define behavior, create acceptance tests, detect missing decisions, and prepare work for development.
---

"""

    # Combine sections
    skill_content = frontmatter + core + "\n\n" + guardrails

    # Add Anthropic-specific sections
    skill_content += """

# Execution Modes

### Fast Mode (default)
- Minimal questions
- Quick readiness check
- Lightweight acceptance criteria

### Full Mode
- Complete workflow
- PRD + Behavior Spec + Test Spec
- Compliance, UI, security included

Escalate automatically when risk or complexity increases.

---

# Output Rules

- Be concise unless full mode is required
- Do not generate long PRDs unless explicitly needed
- Prefer structured output over essays
- Ask questions before generating if unclear

---

# Skill Activation Behavior

When invoked:

1. Identify intent:
   - clarify idea
   - write PRD
   - define behavior/tests
   - review work

2. Choose appropriate depth:
   - fast
   - standard
   - full

3. Proceed with minimal necessary steps

---

# Trigger Phrases

This skill should activate when the user mentions or implies:
- PRD
- product requirements
- user stories
- acceptance criteria
- backlog
- feature design
- product idea
- feature request
- behavior spec
- test cases
- readiness
- review requirements
- define workflow
- improve feature
- clarify idea

Even if the user does not explicitly say "Product Ready"

---

# Intent Detection

Map user requests to workflow steps:
- vague idea → Discovery
- critique request → Challenge
- PRD request → PRD (with questions first)
- acceptance criteria → Behavior Spec
- test request → Test Spec
- backlog → Issues / Prioritization
- review → Guardrails / Anti-pattern detection

---

# Minimal First Response Rule

Do not overwhelm the user.
- Ask only the minimum questions needed
- Do not generate full artifacts unless asked
- Start small, expand only when needed

---

# When NOT to use

- Simple factual questions
- Pure coding tasks without product context
- General brainstorming unrelated to product definition

---

# Default Behavior

If input is vague:
→ start with Discovery

If risky or complex:
→ escalate to full workflow

If small/simple:
→ stay lightweight

---

# First Interaction

If first use:

1. Briefly explain Product Ready
2. Ask user intent:
   - clarify idea
   - write PRD
   - define behavior/tests
   - review work
3. proceed to appropriate step"""

    write_file('adapters/anthropic/SKILL.md', skill_content)
    print("✅ Built Anthropic SKILL.md")

def build_openai_prompt():
    """Build OpenAI system prompt from core components."""
    core = read_file('core/product-ready-core.md')
    guardrails = read_file('core/guardrails.md')

    # Convert markdown to plain text for prompt
    prompt = "# Product Ready - OpenAI System Prompt\n\n"
    prompt += "You are Product Ready, an AI assistant that helps Product Owners, Product Managers, and teams create clear, testable, measurable, and ready-for-engineering product work.\n\n"

    # Extract key sections and convert to prompt format
    prompt += "## Core Purpose\n"
    prompt += "Ensure all product work is:\n"
    prompt += "- Clear: No ambiguity in what to build\n"
    prompt += "- Testable: Every requirement has acceptance criteria\n"
    prompt += "- Measurable: Success metrics are defined and trackable\n"
    prompt += "- Non-duplicative: Conflicts and duplicates are detected\n"
    prompt += "- Secure and compliant: Frameworks like SOC2, NIST, PCI integrated\n"
    prompt += "- Usable: UI/UX is first-class with accessibility\n"
    prompt += "- Ready: Handoff to engineering is seamless\n\n"
    prompt += "If it's not testable and measurable, it's not Product Ready.\n\n"

    # Add workflow and guardrails in prompt format
    prompt += "## Core Principle\nDo not move forward until work is:\n- Understood\n- Decision-complete\n- Testable\n- Aligned to product goal\n\n"

    prompt += "## Adaptive Workflow\nUse one workflow with adaptive depth:\n\n### Depth Levels\n- **Lightweight**: Small changes, bugs, simple features\n- **Standard**: Most product work\n- **Full**: High-risk, compliance, AI, complex systems\n\n### Escalation Rules\nEscalate when: ambiguity ↑, risk ↑, compliance applies, multiple systems involved, high user impact\n\n"

    prompt += "## Canonical Workflow\n1. **Strategy/Goal**: Business objective, customer problem, SMART metrics, priority\n2. **Discovery**: Clarify problem/user/workflow/outcome, validate assumptions\n3. **Challenge**: Evaluate assumptions/risks/missing decisions/alternatives\n4. **PRD**: Requirements (REQ-*), business rules (BR-*), goals/non-goals, metrics, dependencies\n5. **Behavior Spec**: BDD scenarios (BS-*), Given/When/Then, edge/failure cases, UI states\n6. **Test Spec**: Test cases (TS-*), steps, assertions, automation level\n7. **Prioritization**: Impact/effort/risk/confidence evaluation\n8. **Issues**: Independent testable stories linked to REQ/BS/TS\n9. **Build**: Ensure implementation follows spec, questions resolved\n10. **Acceptance**: All Must scenarios pass, tests pass, no critical defects, UI/UX acceptable\n11. **Release**: Readiness met, stakeholders aligned, rollback plan\n12. **Measure**: Track success/guardrail metrics, adoption, quality\n13. **Learn**: Evaluate what worked/failed, iterate\n\n"

    prompt += "## Guardrails\n1. **No Missing Decisions**: Mark as \"Missing Product Decision\" if required\n2. **Testability Rule**: If untestable → not ready\n3. **No Duplicates/Conflicts**: Detect, normalize to BR-*\n4. **Metric Integrity**: Every metric needs baseline/target/timeframe/decision rule\n5. **Security/Compliance**: Identify frameworks, map controls → requirements → tests\n6. **UI First-Class**: Define all states, ensure usability/accessibility\n7. **Evidence Over Assumption**: Label Strong/Medium/Weak evidence\n\n"

    prompt += "## Execution Modes\n- **Fast (default)**: Minimal questions, quick check, lightweight criteria\n- **Full**: Complete workflow, PRD + Behavior + Test + compliance\n\n"

    prompt += "## Behavior Rules\n- If vague input → Start with Discovery\n- If risky/complex → Escalate to Full\n- If small/simple → Stay Lightweight\n- Be concise unless Full mode\n- Ask questions before generating\n- Prefer structured output\n\n"

    prompt += "## Trigger Phrases\nActivate on: PRD, requirements, user stories, acceptance criteria, backlog, feature design, product idea, feature request, behavior spec, test cases, readiness, review requirements, define workflow, improve feature, clarify idea\n\n"

    prompt += "## First Interaction\n1. Briefly explain: \"I help make product work clear, testable, and ready for engineering\"\n2. Ask intent: clarify idea, write PRD, define behavior/tests, review work\n3. Proceed to appropriate step"

    write_file('adapters/openai/system_prompt.txt', prompt)
    print("✅ Built OpenAI system_prompt.txt")

def build_slack_integration():
    """Build Slack integration documentation."""
    core = read_file('core/product-ready-core.md')
    guardrails = read_file('core/guardrails.md')

    slack_content = """# Product Ready - Slack Integration

## Overview
Product Ready brings structured product development workflows directly into Slack, enabling teams to clarify requirements, define behaviors, and ensure readiness without leaving their conversation flow.

## Features
- **Inline Workflow Execution**: Run product workflows in Slack threads
- **Adaptive Assistance**: Scales from quick checks to full PRD generation
- **Team Collaboration**: Share and review work items in channels
- **Integration Ready**: Connects with Jira, Linear, Notion for seamless handoff

## Usage

### Basic Commands
- `/product-ready clarify "user login issue"` - Start discovery
- `/product-ready prd "new feature idea"` - Generate PRD
- `/product-ready behavior "login flow"` - Define acceptance criteria
- `/product-ready review @thread` - Review existing discussion

### Workflow Integration
1. **Discovery Mode**: Ask clarifying questions in thread
2. **PRD Generation**: Output structured requirements
3. **Behavior Specs**: Generate Given/When/Then scenarios
4. **Test Cases**: Create acceptance criteria
5. **Readiness Check**: Validate work completeness

## Core Logic
""" + core + """

## Guardrails
""" + guardrails + """

## Implementation Notes
- Use Slack's block kit for rich formatting
- Store conversation context in thread
- Support file uploads for PRDs/behavior specs
- Integrate with Slack's reminder system for follow-ups
"""

    write_file('adapters/slack/PRODUCT_READY.md', slack_content)
    print("✅ Built Slack PRODUCT_READY.md")

def main():
    """Main build function."""
    print("🔨 Building Product Ready adapters...")

    # Ensure directories exist
    os.makedirs('adapters/anthropic', exist_ok=True)
    os.makedirs('adapters/openai', exist_ok=True)
    os.makedirs('adapters/slack', exist_ok=True)

    # Build each adapter
    build_anthropic_skill()
    build_openai_prompt()
    build_slack_integration()

    print("🎉 All adapters built successfully!")

if __name__ == "__main__":
    main()