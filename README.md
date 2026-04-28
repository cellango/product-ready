# Product-Ready

**Make Product Work Clear, Testable, Measurable, and Ready for Engineering**

*An AI-powered skill that eliminates ambiguity and rework in product development. If it's not testable and measurable, it's not Product Ready.*

[![Phase](https://img.shields.io/badge/Phase-3%20Validated-green)](https://github.com/your-repo/product-ready)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🚀 The Problem

Product teams waste weeks on:
- **Ambiguous requirements** that lead to wrong implementations
- **Missing decisions** discovered mid-development
- **Untestable features** that can't be validated
- **Unmeasurable success** with no clear metrics
- **Compliance gaps** in regulated industries
- **UI/UX oversights** that hurt usability

Traditional tools focus on documentation, not readiness.

## ✅ The Solution

Product-Ready is an intelligent workflow that ensures every product idea becomes **clear, testable, measurable, non-duplicative, secure, compliant, usable, and engineering-ready**.

### Key Differentiators
- **Adaptive Depth**: Scales from quick bug fixes to enterprise compliance systems
- **Full Lifecycle Coverage**: Strategy → Discovery → Build → Test → Release → Measure → Learn
- **Industry-Grade Guardrails**: Detects duplicates, enforces testability, ensures metric integrity
- **BDD-Style Behavior Specs**: Generates testable Given/When/Then scenarios
- **Compliance Integration**: Built-in SOC2, NIST, PCI support

## 🎯 Who It's For

- **Product Owners** clarifying ideas and writing PRDs
- **Product Managers** defining behavior and acceptance criteria
- **Business Analysts** reviewing backlogs and detecting gaps
- **Delivery Leads** ensuring work is ready for engineering
- **Engineering Teams** getting clear, testable handoffs

## ✨ Features

### Adaptive Workflow Engine
- **Lightweight Mode**: Quick fixes and small features
- **Standard Mode**: Most product work
- **Full Mode**: High-risk, compliance, AI, or complex systems

### Intelligent Guardrails
- Missing Product Decision detection
- Duplicate/conflict identification
- Testability enforcement
- Metric integrity (SMART + baselines + decision rules)
- Security & compliance mapping
- UI/UX state coverage

### Complete Product Lifecycle
1. **Strategy/Goal**: Business objectives and success metrics
2. **Discovery/Validation**: Problem clarification and assumption testing
3. **Challenge**: Risk assessment and alternative evaluation
4. **PRD**: Structured requirements and business rules
5. **Behavior Spec**: BDD scenarios with edge cases
6. **Test Spec**: Test cases with automation levels
7. **Prioritization**: Impact/effort/risk evaluation
8. **Issues**: Independent, testable stories
9. **Build**: Implementation guidance
10. **Acceptance**: Readiness validation
11. **Release**: Go-live criteria
12. **Measure**: Success tracking
13. **Learn/Iterate**: Feedback loop

## 🛠 How It Works

Product-Ready activates on natural language triggers like:
- "Write a PRD for login"
- "Define acceptance criteria"
- "Review these user stories"
- "Add export to CSV"

It adapts its depth automatically:
- Vague requests → Discovery mode
- Risky/complex → Full workflow
- Simple tasks → Lightweight output

**No configuration needed** - just mention product work and it engages.

## 📋 Use Cases

### Startup MVP Development
*"We want to build a marketplace"* → Clarifies problem, validates assumptions, produces testable roadmap

### Enterprise Compliance
*"Need SOC2 audit logs"* → Maps controls, generates security scenarios, ensures compliance readiness

### Bug Fixes & Tweaks
*"Fix payment failures"* → Defines reproduction, success metrics, acceptance criteria

### Feature Requests
*"Build invoice approval"* → Full PRD → Behavior specs → Test cases → Engineering stories

### Backlog Reviews
*"Review these stories"* → Detects duplicates, missing decisions, prioritization guidance

## 🚀 Getting Started

### Prerequisites
- Claude/Anthropic access
- VS Code with Copilot Chat (recommended)

### Installation

1. **Workspace Installation** (recommended for teams):
   ```bash
   # Clone or download the repository
   git clone https://github.com/your-repo/product-ready.git

   # Copy the skill to your workspace
   cp product-ready/.github/skills/product-ready/SKILL.md .github/skills/product-ready/
   ```

2. **User-Level Installation** (personal use):
   - Copy `SKILL.md` to your VS Code user prompts folder
   - Location: `~/Library/Application Support/Code/User/prompts/` (macOS)

### Usage

Simply mention product-related tasks in natural language:

```
"Write acceptance criteria for user registration"
"Review this PRD for gaps"
"Clarify this feature idea"
```

Product-Ready will activate automatically and guide you through the appropriate workflow.

## 📖 Examples

See [examples/](./examples/) for complete workflow outputs:
- [Discovery](./examples/example-discovery.md)
- [PRD](./examples/example-prd.md)
- [Behavior Spec](./examples/example-behavior-spec.md)
- [Test Spec](./examples/example-test-spec.md)
- [Acceptance](./examples/example-acceptance.md)

## 🧪 Validation

18 comprehensive test cases validate reliability:
- ✅ Triggers on product language
- ✅ Adapts depth appropriately
- ✅ Prevents over-generation
- ✅ Handles edge cases

See [test-cases/](./test-cases/) for details.

## 🗺 Roadmap

- **Phase 4** (Current): Expand capabilities - UI/UX, enterprise compliance, AI workflows
- **Phase 5**: Launch and adoption - documentation, pilot programs
- **Phase 6**: Continuous improvement - user feedback, integrations

### Recent Milestones
- ✅ Phase 1: Product foundation and vision
- ✅ Phase 2: Core workflow engine with examples
- ✅ Phase 3: Validation with 18 test cases

## 🤝 Contributing

We welcome contributions! This is an open-source project for better product development.

### Ways to Contribute
- Test the skill and report issues
- Suggest improvements or new features
- Add examples or test cases
- Help with documentation

### Development Setup
1. Fork the repository
2. Make changes to `SKILL.md` or examples
3. Test with simulated conversations
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with insights from modern product management practices, BDD, and agile methodologies. Special thanks to the product community for inspiration.

---

**Ready to make your product work actually ready?** Start with Product-Ready today.