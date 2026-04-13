# SFSpeckit — Salesforce Spec-Driven Development

> Enterprise-grade Salesforce SDLC extension for [Spec Kit](https://github.com/github/spec-kit). 17 commands covering the full development lifecycle with Zero-Dependency AI Architecture.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Spec Kit](https://img.shields.io/badge/spec--kit-extension-purple.svg)](https://github.com/github/spec-kit)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](CHANGELOG.md)

## Overview

SFSpeckit transforms Salesforce development from ad-hoc coding into a spec-driven, quality-gated process. It follows a deterministic lifecycle:

```
Constitution → Specify → Clarify → Plan → Stories → Implement → Verify → PR → QA → UAT → Deploy
```

**Hybrid AI Architecture:**
- **Self-Contained**: Works perfectly as a standalone extension with Zero-Dependency.
- **Smart-Aware**: Automatically checks for existing Salesforce foundational skills (`sf-apex`, `sf-lwc`, `sf-docs`) and uses them as **Optional Accelerators**.
- **Unified Rubric**: The **555-point quality scoring** in `docs/scoring.md` is the absolute Source of Truth, regardless of what supplemental skills are used.
- **Auto-heal loop** — AI automatically fixes code that fails scoring gates (up to 3 retries).
- **Blast radius analysis** — CLI-driven dependency impact detection before any changes.

## Installation

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
```

## Prerequisites

| Tool | Version | Required | Purpose |
|------|---------|----------|---------|
| [Spec Kit](https://github.com/github/spec-kit) | ≥ 0.4.0 | ✅ Yes | Core SDD framework |
| [Salesforce CLI (`sf`)](https://developer.salesforce.com/tools/salesforcecli) | ≥ 2.0.0 | ✅ Yes | Org operations, deployments, testing |
| Salesforce DX project | — | ✅ Yes | `sfdx-project.json` must exist |

## Configuration

```bash
# Copy config template
cp .specify/extensions/sf/sf-config.template.yml \
   .specify/extensions/sf/sf-config.yml
```

## Commands

### 🏗️ Foundation
- `/speckit.sf.constitution` — Establish project principles and environmental discovery.

### 🔄 Core SDD Cycle
- `/speckit.sf.specify` — Create a feature spec.
- `/speckit.sf.clarify` — Run gap analysis and business clarification.
- `/speckit.sf.plan` — Technical architecture and blast radius analysis.
- `/speckit.sf.stories` — Generate Jira-ready stories with effort estimates.
- `/speckit.sf.implement` — Build a story with auto-heal loop and scoring gates.

### 🔧 Extended Lifecycle
- `/speckit.sf.review` — TPO + Architect approval gate.
- `/speckit.sf.change` — Mid-sprint change management.
- `/speckit.sf.verify` — Generate formal Verification Evidence.
- `/speckit.sf.pr` — PR preparation with scoring and security scans.
- `/speckit.sf.qa` — QA verification and persona coverage.
- `/speckit.sf.uat` — Business sign-off management.
- `/speckit.sf.score` — 555-point quality dashboard aggregator.
- `/speckit.sf.deploy` — Multi-environment promotion (Dev → QA → UAT → Prod).
- `/speckit.sf.hotfix` — Emergency production fix workflow.
- `/speckit.sf.regression` — Full regression testing after branch merges.
- `/speckit.sf.release-notes` — Auto-generated release documentation.

## Success Architecture

SFSpeckit is designed to be **completely self-contained**. All Salesforce best practices (Bulkification, Security, SOLID) are encoded in `docs/scoring.md`, serving as the AI's internal source of truth.

## License

[MIT](LICENSE) — © 2026 Sumanth Yanamala
