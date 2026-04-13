# SFSpeckit — Salesforce Spec-Driven Development

> Enterprise-grade Salesforce SDLC extension for [Spec Kit](https://github.com/github/spec-kit). 17 commands covering the full development lifecycle — from project constitution to production deployment.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Spec Kit](https://img.shields.io/badge/spec--kit-extension-purple.svg)](https://github.com/github/spec-kit)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](CHANGELOG.md)

## Overview

SFSpeckit transforms Salesforce development from ad-hoc coding into a spec-driven, quality-gated process. Every feature follows a deterministic lifecycle:

```
Constitution → Specify → Clarify → Plan → Stories → Implement → Verify → PR → QA → UAT → Deploy
```

**What makes this different:**
- **555-point quality scoring** across Metadata, Apex, LWC, and Testing
- **Auto-heal loop** — AI automatically fixes code that fails scoring gates (up to 3 retries)
- **Dynamic skill discovery** — auto-detects and uses installed Salesforce domain skills
- **Blast radius analysis** — CLI-driven dependency impact detection before any changes
- **Multi-environment promotion** — Dev → QA → UAT → Prod with dry-run gates

## Installation

### From Community Catalog (after catalog submission)
```bash
specify extension add sf
```

### From GitHub Release
```bash
specify extension add sf --from https://github.com/ysumanth06/spec-kit-sf/archive/refs/tags/v1.0.0.zip
```

### Local Development
```bash
git clone https://github.com/ysumanth06/spec-kit-sf.git
specify extension add --dev /path/to/spec-kit-sf
```

### Verify Installation
```bash
specify extension list
# Should show:
#  ✓ SFSpeckit — Salesforce Spec-Driven Development (v1.0.0)
#     Enterprise Salesforce SDLC with 17 commands for the full SDD lifecycle.
#     Commands: 17 | Hooks: 2 | Status: Enabled
```

## Prerequisites

| Tool | Version | Required | Purpose |
|------|---------|----------|---------|
| [Spec Kit](https://github.com/github/spec-kit) | ≥ 0.4.0 | ✅ Yes | Core SDD framework |
| [Salesforce CLI (`sf`)](https://developer.salesforce.com/tools/salesforcecli) | ≥ 2.0.0 | ✅ Yes | Org operations, deployments, testing |
| [GitHub CLI (`gh`)](https://cli.github.com/) | ≥ 2.0.0 | ❌ Optional | Automated PR creation |
| Salesforce DX project | — | ✅ Yes | `sfdx-project.json` must exist |

## Configuration

After installation, configure your project:

```bash
# Copy config template
cp .specify/extensions/sf/sf-config.template.yml \
   .specify/extensions/sf/sf-config.yml

# Edit with your settings
vim .specify/extensions/sf/sf-config.yml
```

### Configuration Layers (highest priority last)
1. Extension defaults (`extension.yml`)
2. Project config (`.specify/extensions/sf/sf-config.yml`)
3. Local overrides (`.specify/extensions/sf/sf-config.local.yml` — gitignored)
4. Environment variables (`SPECKIT_SF_*`)

### Key Config Options
```yaml
project:
  org_aliases:
    dev: "dev-sandbox"
    qa: "qa-sandbox"
    prod: "production"

scoring:
  metadata: 80  # Minimum passing % for metadata scoring
  apex: 80      # Minimum passing % for Apex scoring
  lwc: 80       # Minimum passing % for LWC scoring
```

## Commands

### 🏗️ Foundation (Run Once)

| Command | Description |
|---------|-------------|
| `/speckit.sf.constitution` | Establish project principles with 9 Salesforce articles, environmental discovery, and scoring gates |

### 🔄 Core SDD Cycle

| Command | Description |
|---------|-------------|
| `/speckit.sf.specify` | Create a feature spec with object maps, automation decisions, and security model |
| `/speckit.sf.clarify` | Run gap analysis with org drift detection and business clarification report |
| `/speckit.sf.plan` | Create technical plan with `force-app/` structure, blast radius, and Architect sign-off |
| `/speckit.sf.stories` | Generate Jira-ready stories with security matrices and effort estimates |
| `/speckit.sf.implement` | Build a story with auto-heal loop and scoring gates |

### 🔧 Extended Lifecycle

| Command | Description |
|---------|-------------|
| `/speckit.sf.review` | TPO + Architect review gate with dependency and merge conflict analysis |
| `/speckit.sf.change` | Mid-sprint change management with impact report |
| `/speckit.sf.verify` | Generate formal Verification Evidence with coverage and telemetry |
| `/speckit.sf.pr` | PR preparation with scoring gates, security scan, and review checklist |
| `/speckit.sf.qa` | QA verification with persona coverage and traceability matrix |
| `/speckit.sf.uat` | Business UAT scripts in non-technical language with sign-off management |
| `/speckit.sf.score` | 555-point quality dashboard across all stories |
| `/speckit.sf.deploy` | Multi-environment promotion (Dev → QA → UAT → Prod) |
| `/speckit.sf.hotfix` | Emergency production fix with fast-track deployment |
| `/speckit.sf.regression` | Full regression testing after story merges |
| `/speckit.sf.release-notes` | Auto-generated release notes from completed stories |

### Lifecycle Hooks

| Hook | Trigger | Action |
|------|---------|--------|
| `after_tasks` | After `/speckit.tasks` runs | Prompts to run `/speckit.sf.review` |
| `after_implement` | After `/speckit.implement` runs | Prompts to run `/speckit.sf.verify` |

## Dynamic Skill Discovery

SFSpeckit commands **do not hardcode** references to specific domain skills. Instead, they dynamically search for relevant installed skills at runtime:

```
Before executing, search for installed agent skills related to:
- Apex development, LWC development, Metadata/Objects, SOQL, Testing, etc.

Search: .agents/skills/, .specify/extensions/, .claude/commands/
If found → load and apply. If not found → use built-in knowledge.
```

This means the extension works with **any** combination of installed skills and **any** AI agent (Claude, Gemini, Copilot, Cursor, etc.).

## Troubleshooting

### sf CLI Not Found
```
Error: Tool 'sf' not found or version too low
```
**Fix**: Install Salesforce CLI: `npm install -g @salesforce/cli`

### Commands Not Appearing in Agent
**Check**:
1. Extension installed: `specify extension list`
2. Commands registered: `ls .claude/commands/speckit.sf.*`
3. Restart your AI agent

**Fix**: Reinstall: `specify extension remove sf && specify extension add --dev .`

### Config Not Loading
**Check**:
1. Config exists: `ls .specify/extensions/sf/sf-config.yml`
2. YAML valid: `python3 -c "import yaml; yaml.safe_load(open('.specify/extensions/sf/sf-config.yml'))"`

**Fix**: Copy template: `cp .specify/extensions/sf/sf-config.template.yml .specify/extensions/sf/sf-config.yml`

### Constitution Not Found
```
Error: Constitution not found at .specify/memory/constitution.md
```
**Fix**: Run `/speckit.sf.constitution` first — it must be run once before any other command.

## Contributing

Contributions are welcome! Please:

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/my-improvement`
3. Commit your changes: `git commit -m "Add improvement"`
4. Push: `git push origin feature/my-improvement`
5. Open a Pull Request

## Documentation

- [Full Workflow Guide](docs/workflow.md) — End-to-end lifecycle walkthrough
- [Scoring System](docs/scoring.md) — 555-point quality scoring explained
- [Migration Guide](docs/migration-from-standalone.md) — Upgrading from standalone SFSpeckit

## License

[MIT](LICENSE) — © 2026 Sumanth Yanamala
