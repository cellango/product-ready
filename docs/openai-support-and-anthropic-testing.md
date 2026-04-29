# OpenAI Support Plan And Anthropic Skill Testing

## Current Priority

Focus now: validate the Anthropic skill generated at `adapters/anthropic/SKILL.md`.

Later priority: add OpenAI support as a first-class equivalent artifact, not only a plain system prompt.

## OpenAI Support Implementation Plan

### Goal

Build OpenAI artifacts from the same Product Ready core workflow and guardrails used by the Anthropic skill.

The first OpenAI release should support:

- Codex agent skill usage.
- Responses API prompt usage.
- Manual Custom GPT setup guidance.
- Validation that prevents Anthropic and OpenAI behavior from drifting.

### Target Artifacts

Create these generated files under `adapters/openai/`:

- `codex-skill/product-ready/SKILL.md`
- `codex-skill/product-ready/agents/openai.yaml`
- `api/system_prompt.txt`
- `api/responses-request.json`
- `custom-gpt/instructions.md`
- `custom-gpt/setup.md`

### Phase 1: Shared Source Rendering

- Move shared skill content generation into reusable functions in `scripts/build.py`.
- Generate Anthropic and OpenAI artifacts from `core/product-ready-core.md` and `core/guardrails.md`.
- Keep platform-specific behavior in small adapter templates.
- Make Anthropic `SKILL.md` and OpenAI Codex `SKILL.md` structurally comparable.

Acceptance criteria:

- One core content change updates both Anthropic and OpenAI generated artifacts.
- OpenAI output no longer duplicates a hardcoded copy of the workflow.
- Existing Anthropic output remains behaviorally unchanged.

### Phase 2: OpenAI Codex Skill Artifact

- Generate `adapters/openai/codex-skill/product-ready/SKILL.md`.
- Include required frontmatter: `name` and `description`.
- Add OpenAI/Codex-specific usage notes for invocation, scope, and when not to use.
- Add `agents/openai.yaml` with display metadata and default invocation behavior.

Acceptance criteria:

- The OpenAI Codex skill can be copied into `.agents/skills/product-ready/`.
- The skill description clearly triggers on PRDs, requirements, acceptance criteria, behavior specs, test plans, and readiness reviews.
- The skill remains instruction-only unless deterministic scripts become necessary.

### Phase 3: OpenAI API Artifact

- Generate `adapters/openai/api/system_prompt.txt`.
- Generate `adapters/openai/api/responses-request.json`.
- Use the Responses API shape with model, instructions, and example input.
- Keep provider-specific fields isolated so future model changes are easy.

Acceptance criteria:

- The JSON file parses successfully.
- The instructions content matches the generated OpenAI system prompt.
- The example request can be copied into API tests with only API key/model changes.

### Phase 4: Custom GPT Package

- Generate `adapters/openai/custom-gpt/instructions.md`.
- Generate `adapters/openai/custom-gpt/setup.md`.
- Document what to paste into Custom GPT instructions.
- Document that no GPT Action is required for the initial instruction-only release.
- Add an optional future section for GPT Actions if external APIs are introduced.

Acceptance criteria:

- A user can create a Custom GPT manually from the generated docs.
- The setup doc explains what is supported now and what is intentionally deferred.
- No claims imply a hosted API or GPT Action exists before it does.

### Phase 5: Validation And CI

- Add validation for all required OpenAI files.
- Validate YAML frontmatter for OpenAI Codex `SKILL.md`.
- Validate `agents/openai.yaml` as YAML.
- Validate `responses-request.json` as JSON.
- Check required sections exist in Anthropic and OpenAI artifacts.
- Update CI to fail if OpenAI artifacts are missing or malformed.

Acceptance criteria:

- `python3 scripts/build.py --validate` checks Anthropic and OpenAI artifacts.
- CI verifies both platform outputs.
- Markdown lint passes for all generated Markdown.

### Phase 6: Documentation

- Update `README.md` with separate setup paths:
  - Anthropic skill.
  - OpenAI Codex skill.
  - OpenAI Responses API.
  - OpenAI Custom GPT.
- Remove or qualify claims that imply unsupported Slack/OpenAI features.
- Keep implementation notes in `docs/`.

Acceptance criteria:

- README setup steps match real generated files.
- Documentation distinguishes current support from planned support.
- Root still contains only `README.md` as Markdown.

## Anthropic Skill Testing

### Prerequisites

- You have the repository locally.
- You have access to Claude or an Anthropic environment that supports skills.
- You can run Python 3 locally.

### Step 1: Check The Generated Skill Exists

From the repository root, run:

```bash
ls -la adapters/anthropic/SKILL.md
```

Expected result:

- The file exists.
- The file is not empty.

### Step 2: Validate The Build Script

Run:

```bash
python3 scripts/build.py --validate
```

Expected result:

- Build completes successfully.
- Anthropic `SKILL.md` is regenerated.
- YAML frontmatter validation passes.

Note: this command regenerates adapter files. Review `git diff` afterward before committing.

### Step 3: Check Anthropic Skill Frontmatter

Run:

```bash
head -5 adapters/anthropic/SKILL.md
```

Expected result:

```yaml
---
name: product-ready
description: Use this skill when working on product ideas, PRDs, requirements, user stories, acceptance criteria, backlog items, behavior specs, test plans, or readiness reviews. Helps Product Owners clarify ideas, write PRDs, define behavior, create acceptance tests, detect missing decisions, and prepare work for development.
---
```

### Step 4: Install The Skill In Claude

Use the installation path required by your Anthropic/Claude environment.

At minimum, copy or upload:

```text
adapters/anthropic/SKILL.md
```

Use the skill name:

```text
product-ready
```

### Step 5: Smoke Test Triggering

Start a new Claude chat with the skill enabled and use this prompt:

```text
Write acceptance criteria for user registration.
```

Expected behavior:

- The skill recognizes product work.
- The response stays lightweight.
- The response includes testable acceptance criteria.
- The response should not generate a full PRD unless needed.

### Step 6: Test Discovery Mode

Use this prompt:

```text
We want to improve onboarding.
```

Expected behavior:

- The skill treats the input as vague.
- The response starts with discovery or clarifying questions.
- The response asks only the minimum useful questions.

### Step 7: Test Full Mode Escalation

Use this prompt:

```text
Create requirements for audit logging in a SOC2-regulated financial product.
```

Expected behavior:

- The skill escalates because compliance and risk apply.
- The response includes security/compliance considerations.
- The response mentions testability and measurable acceptance criteria.
- The response should identify missing product decisions if needed.

### Step 8: Test Review Behavior

Use this prompt:

```text
Review this user story for readiness:
As an admin, I want export, so I can report.
```

Expected behavior:

- The skill identifies ambiguity.
- The skill flags missing decisions.
- The skill asks for format, scope, permissions, success criteria, and test expectations.

### Step 9: Test Non-Trigger Boundary

Use this prompt:

```text
What is the capital of France?
```

Expected behavior:

- The skill should not force the Product Ready workflow.
- The response should answer directly or stay out of scope.

### Step 10: Record Results

For each test prompt, record:

- Prompt used.
- Whether the skill triggered.
- Mode selected: lightweight, standard, or full.
- Missing decisions found.
- Whether output was testable.
- Any behavior that felt too verbose or too shallow.

Use failed or weak responses to refine:

- `core/product-ready-core.md`
- `core/guardrails.md`
- Anthropic-specific sections in `scripts/build.py`

### Step 11: Run Local Verification Before Committing

Run:

```bash
flake8 scripts/build.py
python3 -m py_compile scripts/build.py
npx markdownlint-cli2 "**/*.md"
find . -maxdepth 1 -name "*.md" -print
```

Expected result:

- Python lint passes.
- Python compile check passes.
- Markdown lint passes.
- Root Markdown check only prints `./README.md`.
