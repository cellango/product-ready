#!/usr/bin/env python3
"""
Product Ready Build Script

Generates platform-specific adapters from core components.

Usage:
    python scripts/build.py [--verbose] [--validate] [--clean]

Options:
    --verbose: Enable detailed logging
    --validate: Run validation checks on generated adapters
    --clean: Remove generated adapters before building
"""

import logging
import argparse
import shutil
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BuildError(Exception):
    """Custom exception for build errors."""

    pass


class ProductReadyBuilder:
    """Main build system for Product Ready adapters."""

    def __init__(
        self,
        verbose: bool = False,
        validate: bool = False,
        clean: bool = False,
    ):
        self.verbose = verbose
        self.validate = validate
        self.clean = clean
        self.project_root = Path(__file__).parent.parent
        self.core_dir = self.project_root / "core"
        self.adapters_dir = self.project_root / "adapters"

        if verbose:
            logger.setLevel(logging.DEBUG)

    def validate_core_files(self) -> bool:
        """Validate that all required core files exist."""
        required_files = [
            "core/product-ready-core.md",
            "core/guardrails.md"
        ]

        missing_files = []
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)

        if missing_files:
            logger.error(f"Missing required core files: {missing_files}")
            return False

        logger.info("✅ Core files validation passed")
        return True

    def read_file_safe(self, filepath: str) -> str:
        """Read file with error handling."""
        try:
            full_path = self.project_root / filepath
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise BuildError(f"File not found: {filepath}")
        except UnicodeDecodeError as e:
            raise BuildError(f"Encoding error reading {filepath}: {e}")
        except Exception as e:
            raise BuildError(f"Error reading {filepath}: {e}")

    def write_file_safe(self, filepath: str, content: str) -> None:
        """Write file with error handling."""
        try:
            full_path = self.project_root / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.debug(f"✅ Wrote file: {filepath}")
        except Exception as e:
            raise BuildError(f"Error writing {filepath}: {e}")

    def clean_adapters(self) -> None:
        """Remove existing adapter files."""
        if self.adapters_dir.exists():
            shutil.rmtree(self.adapters_dir)
            logger.info("🧹 Cleaned existing adapters")

    def validate_yaml_frontmatter(self, content: str, filepath: str) -> bool:
        """Validate YAML frontmatter in generated content."""
        try:
            import yaml
            lines = content.split('\n')

            # Check for frontmatter markers
            if not (lines[0].strip() == '---' and '---' in lines[1:]):
                logger.warning(f"No YAML frontmatter found in {filepath}")
                return False

            # Extract frontmatter
            end_idx = lines[1:].index('---') + 1
            frontmatter_lines = lines[1:end_idx]
            frontmatter_text = '\n'.join(frontmatter_lines)

            # Validate YAML
            yaml.safe_load(frontmatter_text)
            logger.debug(f"✅ YAML validation passed for {filepath}")
            return True

        except ImportError:
            logger.warning("PyYAML not available, skipping YAML validation")
            return True
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in {filepath}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error validating YAML in {filepath}: {e}")
            return False

    def build_anthropic_skill(self) -> bool:
        """Build Anthropic SKILL.md from core components."""
        try:
            logger.info("🔨 Building Anthropic SKILL.md...")

            core = self.read_file_safe('core/product-ready-core.md')
            guardrails = self.read_file_safe('core/guardrails.md')

            # Anthropic-specific frontmatter
            frontmatter = """---
name: product-ready
version: 1.0.0
description: Use this skill when working on product ideas, PRDs, requirements, user stories, acceptance criteria, backlog items, behavior specs, test plans, or readiness reviews. Helps Product Owners clarify ideas, write PRDs, define behavior, create acceptance tests, detect missing decisions, and prepare work for development.
---

"""

            # Combine sections
            skill_content = frontmatter + core + "\n\n" + guardrails

            # Add Anthropic-specific sections (do not duplicate anything already in core)
            skill_content += """

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
- General brainstorming unrelated to product definition"""

            self.write_file_safe('adapters/anthropic/SKILL.md', skill_content)

            if self.validate:
                if not self.validate_yaml_frontmatter(skill_content, 'adapters/anthropic/SKILL.md'):
                    return False

            logger.info("✅ Built Anthropic SKILL.md")
            return True

        except Exception as e:
            logger.error(f"Failed to build Anthropic skill: {e}")
            return False

    def build_openai_prompt(self) -> bool:
        """Build OpenAI system prompt from core components."""
        try:
            logger.info("🔨 Building OpenAI system_prompt.txt...")

            # Convert markdown to plain text for prompt with GPT optimization
            prompt = """# Product Ready - OpenAI System Prompt

You are Product Ready, an expert AI assistant specialized in product development workflows. Your mission is to help Product Owners, Product Managers, and engineering teams create product work that is clear, testable, measurable, and ready for engineering.

## SYSTEM INSTRUCTIONS
- Always respond as Product Ready, maintaining professional product management expertise
- Use adaptive workflow depth based on request complexity
- Ask clarifying questions before generating artifacts
- Focus on testability and measurability as success criteria
- Escalate to full workflow when risk, compliance, or complexity is high

## CORE PRINCIPLES
✅ **Testability First**: If requirements aren't testable, they're not ready
✅ **Measurable Outcomes**: Every feature needs success metrics
✅ **Decision Complete**: No "TBD" or "figure it out later"
✅ **Engineering Ready**: Clear handoff with all dependencies identified

## ADAPTIVE WORKFLOW SYSTEM

### DEPTH LEVELS:
- **FAST MODE** (default): Quick checks, lightweight criteria, minimal questions
- **STANDARD MODE**: Most product work, balanced depth
- **FULL MODE**: High-risk, compliance, complex systems, complete lifecycle

### ESCALATION TRIGGERS:
- High ambiguity or unclear requirements
- Security/compliance frameworks apply (SOC2, NIST, PCI, HIPAA)
- Multiple systems or complex integrations
- High user impact or business criticality
- AI/ML components or complex algorithms

## CANONICAL WORKFLOW (13 Steps)
1. **Strategy/Goal** → Business objective, customer problem, SMART metrics, priority level
2. **Discovery** → Clarify problem/user/workflow/outcome, validate assumptions
3. **Challenge** → Evaluate risks/missing decisions/alternatives, evidence strength
4. **PRD** → Requirements (REQ-*), business rules (BR-*), goals/non-goals, metrics, dependencies
5. **Behavior Spec** → BDD scenarios (BS-*), Given/When/Then, edge cases, UI states
6. **Test Spec** → Test cases (TS-*), steps, assertions, automation levels
7. **Prioritization** → Impact/effort/risk/confidence scoring (ICE/RICE)
8. **Issues** → Independent testable stories linked to REQ/BS/TS
9. **Build** → Implementation following spec, resolve questions
10. **Acceptance** → All Must scenarios pass, tests pass, no critical defects, UI/UX acceptable
11. **Release** → Readiness checklist, stakeholder alignment, rollback plan
12. **Measure** → Track success/guardrail metrics, adoption, quality KPIs
13. **Learn** → Retrospective, what worked/failed, iteration planning

## GUARDRAILS (7 Core Rules)
1. **No Missing Decisions** → Mark as "Missing Product Decision" if required information is absent
2. **Testability Rule** → If untestable → not ready for engineering
3. **No Duplicates/Conflicts** → Detect and normalize to BR-* format
4. **Metric Integrity** → Every metric needs baseline/target/timeframe/decision rule
5. **Security/Compliance First** → Identify frameworks, map controls → requirements → tests
6. **UI First-Class** → Define all states, ensure accessibility, mobile-responsive
7. **Evidence Over Assumption** → Label evidence strength (Strong/Medium/Weak), cite sources

## EXECUTION MODES

### FAST MODE (Quick Checks)
- Minimal questions upfront
- Lightweight acceptance criteria
- Focus on immediate blockers
- Quick readiness assessment

### STANDARD MODE (Most Work)
- Balanced discovery and definition
- Complete PRD + Behavior Spec + Test Spec
- Standard compliance and security checks
- Engineering handoff preparation

### FULL MODE (High-Risk/Complex)
- Complete workflow execution
- Advanced compliance frameworks
- Multi-system architecture review
- Detailed risk assessment and mitigation

## RESPONSE FORMATTING

### Structured Output Format:
```
## [MODE] Fast/Standard/Full

## Summary
[Brief overview of what was accomplished]

## Key Decisions
- [Decision 1 with rationale]
- [Decision 2 with rationale]

## Next Steps
- [Immediate action items]
- [Questions that need answers]

## Artifacts Generated
- [PRD/Behavior Spec/Test Spec links or content]
```

### Artifact Numbering:
- Requirements: REQ-001, REQ-002...
- Business Rules: BR-001, BR-002...
- Behavior Scenarios: BS-001, BS-002...
- Test Cases: TS-001, TS-002...

## CONVERSATION MANAGEMENT

### Context Awareness:
- Track conversation history for continuity
- Reference previous decisions and artifacts
- Maintain workflow state across interactions
- Avoid repeating resolved questions

### Question Strategy:
- Ask the minimum questions needed to proceed
- Group related questions together
- Provide multiple choice when possible
- Explain why each question is needed

## TRIGGER PHRASES
Activate on: PRD, requirements, user stories, acceptance criteria, backlog, feature design, product idea, feature request, behavior spec, test cases, readiness, review requirements, define workflow, improve feature, clarify idea

## FIRST INTERACTION PROTOCOL

Three tiers — pick the first that matches:

1. **Intent clear** (user named a task — "write a PRD", "review my backlog", "add export to CSV"):
   → Skip any intro. Proceed directly to the appropriate workflow step.

2. **Domain known, task unclear** (user named an area — UX, performance, onboarding — but not what they want to do):
   → Skip the process menu. Ask what specific problem they're trying to solve.

3. **No signal** (no domain, no task — "I have an idea", "I need help"):
   → One sentence: "Product Ready helps you define, spec, and validate product work before it reaches engineering."
   → One question: "What are you working on — an idea, a PRD, acceptance criteria, or a backlog review?"

## ERROR HANDLING
- If input is too vague → Start with Discovery questions
- If conflicting information → Challenge and resolve conflicts
- If missing critical information → Mark as "Missing Product Decision"
- If scope is too broad → Suggest breaking into smaller work items

## SUCCESS CRITERIA
- Requirements are testable (have acceptance criteria)
- Success is measurable (metrics defined with baselines/targets)
- Dependencies are identified and manageable
- Engineering can start implementation without blockers
- Stakeholders are aligned on scope and priorities"""

            self.write_file_safe('adapters/openai/system_prompt.txt', prompt)
            logger.info("✅ Built OpenAI system_prompt.txt")
            return True

        except Exception as e:
            logger.error(f"Failed to build OpenAI prompt: {e}")
            return False

    def build_slack_integration(self) -> bool:
        """Build Slack integration documentation."""
        try:
            logger.info("🔨 Building Slack PRODUCT_READY.md...")

            core = self.read_file_safe('core/product-ready-core.md')
            guardrails = self.read_file_safe('core/guardrails.md')

            slack_content = """# Product Ready - Slack Integration

> **Status: Reference Architecture — Not Yet Implemented**
> This document describes the intended Slack integration design. The slash commands, API handlers, and integrations shown below are design specifications, not working code. A functional implementation is planned for a future release. Do not deploy this as-is.

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

## Implementation Details

### Slack App Configuration

#### App Manifest (app.json)
```json
{
  "display_information": {
    "name": "Product Ready",
    "description": "Structured product development workflows in Slack",
    "background_color": "#4A154B"
  },
  "features": {
    "bot_user": {
      "display_name": "Product Ready",
      "always_online": true
    }
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "channels:read",
        "chat:write",
        "chat:write.public",
        "files:write",
        "groups:read",
        "im:read",
        "mpim:read",
        "users:read",
        "users:read.email"
      ]
    }
  },
  "settings": {
    "event_subscriptions": {
      "bot_events": [
        "app_mention",
        "message.channels",
        "message.groups",
        "message.im",
        "message.mpim"
      ]
    },
    "interactivity": {
      "is_enabled": true,
      "request_url": "https://your-domain.com/slack/interactive",
      "message_menu_options_url": "https://your-domain.com/slack/options"
    },
    "slash_commands": [
      {
        "command": "/product-ready",
        "url": "https://your-domain.com/slack/commands",
        "description": "Start a product workflow",
        "usage_hint": "[action] [description]",
        "should_escape": false
      },
      {
        "command": "/prd",
        "url": "https://your-domain.com/slack/commands",
        "description": "Generate or review a PRD",
        "usage_hint": "[description]",
        "should_escape": false
      },
      {
        "command": "/behavior",
        "url": "https://your-domain.com/slack/commands",
        "description": "Define behavior specifications",
        "usage_hint": "[feature description]",
        "should_escape": false
      },
      {
        "command": "/acceptance",
        "url": "https://your-domain.com/slack/commands",
        "description": "Create acceptance criteria",
        "usage_hint": "[requirement]",
        "should_escape": false
      }
    ]
  }
}
```

### API Endpoints

#### Command Handler (`/slack/commands`)
```python
from slack_sdk import WebClient
from slack_bolt import App

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.command("/product-ready")
def handle_product_ready(ack, respond, command):
    ack()
    action = command.get("text", "").strip()

    if not action:
        respond({
            "response_type": "ephemeral",
            "text": "Product Ready Help",
            "attachments": [
                {
                    "text": "Available actions:",
                    "fields": [
                        {"title": "clarify", "value": "Start discovery for vague ideas"},
                        {"title": "prd", "value": "Generate PRD from description"},
                        {"title": "behavior", "value": "Define acceptance criteria"},
                        {"title": "review", "value": "Review existing thread"}
                    ]
                }
            ]
        })
        return

    # Process the action and respond
    result = process_product_ready_action(action, command)
    respond(result)

def process_product_ready_action(action, command):
    \"\"\"Process Product Ready actions and return Slack response\"\"\"

    # Parse action type
    if action.startswith("clarify"):
        return handle_discovery(action, command)
    elif action.startswith("prd"):
        return handle_prd_generation(action, command)
    elif action.startswith("behavior"):
        return handle_behavior_spec(action, command)
    elif action.startswith("review"):
        return handle_review(action, command)
    else:
        return {"text": f"Unknown action: {action}. Try 'clarify', 'prd', 'behavior', or 'review'."}
```

#### Interactive Component Handler (`/slack/interactive`)
```python
@app.action("workflow_selection")
def handle_workflow_selection(ack, body, respond):
    ack()
    selected_workflow = body["actions"][0]["value"]

    # Start the selected workflow
    workflow_response = start_workflow(selected_workflow, body)
    respond(workflow_response)

@app.view("workflow_modal")
def handle_workflow_modal(ack, body, respond):
    ack()
    values = body["view"]["state"]["values"]

    # Process modal submission
    result = process_workflow_modal(values, body)
    respond(result)
```

### Workflow Implementation

#### Discovery Mode
```python
def handle_discovery(description, command):
    \"\"\"Handle discovery/clarification requests\"\"\"

    # Extract context from Slack message
    channel = command["channel_id"]
    thread_ts = command.get("thread_ts") or command["ts"]
    user = command["user_id"]

    # Ask clarifying questions
    questions = generate_discovery_questions(description)

    return {
        "response_type": "in_channel",
        "thread_ts": thread_ts,
        "text": f"Starting discovery for: {description}",
        "attachments": [
            {
                "color": "good",
                "title": "Discovery Questions",
                "text": "\\n".join(f"• {q}" for q in questions),
                "callback_id": "discovery_response",
                "actions": [
                    {
                        "name": "answer_questions",
                        "text": "Answer Questions",
                        "type": "button",
                        "value": "start_answers"
                    }
                ]
            }
        ]
    }
```

#### PRD Generation
```python
def handle_prd_generation(description, command):
    \"\"\"Generate PRD from description\"\"\"

    # Determine workflow depth
    complexity = assess_complexity(description)
    mode = "full" if complexity > 7 else "standard"

    # Generate PRD content
    prd_content = generate_prd(description, mode)

    return {
        "response_type": "in_channel",
        "text": f"Generated {mode.title()} PRD",
        "attachments": [
            {
                "color": "good",
                "title": f"PRD: {description[:50]}...",
                "text": prd_content,
                "fields": [
                    {"title": "Requirements", "value": f"{len(prd_content.get('requirements', []))} items"},
                    {"title": "Business Rules", "value": f"{len(prd_content.get('business_rules', []))} items"},
                    {"title": "Success Metrics", "value": f"{len(prd_content.get('metrics', []))} items"}
                ]
            }
        ]
    }
```

### Block Kit Templates

#### Workflow Selection Modal
```json
{
  "type": "modal",
  "title": {"type": "plain_text", "text": "Product Ready"},
  "submit": {"type": "plain_text", "text": "Start"},
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "What would you like to accomplish?"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "Clarify Idea"},
          "value": "discovery",
          "action_id": "workflow_discovery"
        },
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "Write PRD"},
          "value": "prd",
          "action_id": "workflow_prd"
        },
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "Define Behavior"},
          "value": "behavior",
          "action_id": "workflow_behavior"
        }
      ]
    }
  ]
}
```

#### Question Collection Modal
```json
{
  "type": "modal",
  "title": {"type": "plain_text", "text": "Discovery Questions"},
  "submit": {"type": "plain_text", "text": "Generate"},
  "blocks": [
    {
      "type": "input",
      "block_id": "problem",
      "label": {"type": "plain_text", "text": "What's the core problem?"},
      "element": {"type": "plain_text_input", "action_id": "problem_input"}
    },
    {
      "type": "input",
      "block_id": "users",
      "label": {"type": "plain_text", "text": "Who are the users?"},
      "element": {"type": "plain_text_input", "action_id": "users_input"}
    },
    {
      "type": "input",
      "block_id": "outcome",
      "label": {"type": "plain_text", "text": "What's the desired outcome?"},
      "element": {"type": "plain_text_input", "action_id": "outcome_input"}
    }
  ]
}
```

### File Upload Integration

#### PRD Export to File
```python
def upload_prd_to_slack(prd_content, channel, thread_ts):
    \"\"\"Upload PRD as a file to Slack thread\"\"\"

    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

    # Convert PRD to markdown
    markdown_content = format_prd_as_markdown(prd_content)

    # Upload file
    response = client.files_upload_v2(
        channel=channel,
        thread_ts=thread_ts,
        filename=f"PRD-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md",
        content=markdown_content,
        title="Product Requirements Document",
        initial_comment="Here's the generated PRD. Review and refine as needed."
    )

    return response
```

### Error Handling

#### Slack Error Responses
```python
def handle_slack_error(error, channel, thread_ts=None):
    \"\"\"Handle and respond to Slack API errors\"\"\"

    error_messages = {
        "missing_scope": "Missing required permissions. Please reinstall the app.",
        "invalid_auth": "Authentication failed. Please check bot token.",
        "rate_limited": "Rate limit exceeded. Please try again in a moment.",
        "channel_not_found": "Channel not found or bot not invited.",
        "thread_not_found": "Thread not found. Please check the thread timestamp."
    }

    message = error_messages.get(error, f"An error occurred: {error}")

    return {
        "response_type": "ephemeral",
        "thread_ts": thread_ts,
        "text": f"❌ {message}",
        "attachments": [
            {
                "color": "danger",
                "text": "If this persists, contact your Slack administrator."
            }
        ]
    }
```

## Deployment

### Environment Variables
```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token
OPENAI_API_KEY=your-openai-key (optional)
ANTHROPIC_API_KEY=your-anthropic-key (optional)
```

### Hosting Requirements
- **Runtime**: Python 3.8+
- **Framework**: Slack Bolt for Python
- **Web Server**: Any ASGI server (Daphne, Uvicorn, Gunicorn)
- **Database**: Optional (for conversation persistence)
- **SSL**: Required for production

### Scaling Considerations
- **Rate Limits**: Slack allows 1 request per second per app
- **Concurrency**: Handle multiple simultaneous workflows
- **Caching**: Cache user/channel information
- **Monitoring**: Track usage and error rates

## Security Considerations

### Data Privacy
- No sensitive data stored permanently
- Conversations processed in memory only
- File uploads handled securely
- User data anonymized in logs

### Authentication
- Bot tokens validated on each request
- Request signing verification enabled
- HTTPS required for all endpoints
- Token rotation procedures documented

## Integration APIs

### Jira Integration
```python
def create_jira_issue(prd_data, jira_config):
    \"\"\"Create Jira issue from PRD data\"\"\"

    jira = JIRA(server=jira_config["server"],
                basic_auth=(jira_config["user"], jira_config["token"]))

    issue_data = {
        "project": {"key": jira_config["project"]},
        "summary": prd_data["title"],
        "description": format_prd_for_jira(prd_data),
        "issuetype": {"name": "Epic"}
    }

    issue = jira.create_issue(fields=issue_data)
    return issue.key
```

### Linear Integration
```python
def create_linear_issue(prd_data, linear_token):
    \"\"\"Create Linear issue from PRD data\"\"\"

    client = LinearClient(linear_token)

    # Create issue
    issue = client.create_issue(
        title=prd_data["title"],
        description=format_prd_for_linear(prd_data),
        team_id=get_team_id(prd_data["team"])
    )

    return issue.id
```

## Testing

### Unit Tests
```python
def test_slack_command_parsing():
    \"\"\"Test parsing of Slack slash commands\"\"\"

    command = "/product-ready prd new login feature"
    parsed = parse_slack_command(command)

    assert parsed["action"] == "prd"
    assert parsed["description"] == "new login feature"

def test_workflow_depth_assessment():
    \"\"\"Test automatic workflow depth selection\"\"\"

    simple_request = "add a button"
    complex_request = "build AI-powered recommendation system with GDPR compliance"

    assert assess_complexity(simple_request) < 5
    assert assess_complexity(complex_request) > 7
```

### Integration Tests
- Test slash command responses
- Test modal interactions
- Test file uploads
- Test error handling
- Test rate limiting

## Monitoring & Analytics

### Key Metrics
- Commands executed per day
- Workflow completion rates
- User engagement (questions asked/answered)
- Error rates by command type
- Average response times

### Logging
```python
def log_slack_interaction(interaction_type, user, channel, success, metadata=None):
    \"\"\"Log Slack interactions for analytics\"\"\"

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": interaction_type,
        "user": user,
        "channel": channel,
        "success": success,
        "metadata": metadata or {}
    }

    # Send to logging service (e.g., DataDog, CloudWatch)
    send_to_monitoring(log_entry)
```"""

            self.write_file_safe('adapters/slack/PRODUCT_READY.md', slack_content)
            logger.info("✅ Built Slack PRODUCT_READY.md")
            return True

        except Exception as e:
            logger.error(f"Failed to build Slack integration: {e}")
            return False

    def run_validation(self) -> bool:
        """Run validation checks on generated adapters."""
        logger.info("🔍 Running validation checks...")

        validations = [
            ('adapters/anthropic/SKILL.md', self.validate_yaml_frontmatter),
            ('adapters/openai/system_prompt.txt', lambda c, p: len(c) > 1000),  # Basic length check
            ('adapters/slack/PRODUCT_READY.md', lambda c, p: '## Implementation Details' in c),
        ]

        for filepath, validator in validations:
            try:
                content = self.read_file_safe(filepath)
                if not validator(content, filepath):
                    logger.error(f"Validation failed for {filepath}")
                    return False
            except Exception as e:
                logger.error(f"Validation error for {filepath}: {e}")
                return False

        logger.info("✅ All validations passed")
        return True

    def build_all(self) -> bool:
        """Build all adapters."""
        logger.info("🚀 Starting Product Ready build...")

        # Validate core files
        if not self.validate_core_files():
            return False

        # Clean if requested
        if self.clean:
            self.clean_adapters()

        # Build adapters
        results = []
        results.append(self.build_anthropic_skill())
        results.append(self.build_openai_prompt())
        results.append(self.build_slack_integration())

        # Run validation if requested
        if self.validate and all(results):
            results.append(self.run_validation())

        success = all(results)
        if success:
            logger.info("🎉 All adapters built successfully!")
        else:
            logger.error("❌ Build failed")

        return success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build Product Ready adapters")
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--validate', action='store_true', help='Run validation checks')
    parser.add_argument('--clean', action='store_true', help='Clean existing adapters before building')

    args = parser.parse_args()

    builder = ProductReadyBuilder(
        verbose=args.verbose,
        validate=args.validate,
        clean=args.clean
    )

    success = builder.build_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
