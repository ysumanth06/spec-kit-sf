# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-07-21

### Added
- **New Command**: `/speckit.sf.analyze` — pre-implementation analysis with mother story lineage, component scope mapping, and org drift detection via `sf project retrieve preview`.
- **Bundled Templates**: Shipped 9 Salesforce SDD templates in `templates/` (constitution, spec, plan, story, clarify, clarification report, QA test scripts, UAT scripts, hotfix).
- **Sync Tooling**: Added `scripts/sync_skills_to_commands.py` to convert Cursor skills from the standalone SFSpeckit toolkit into Spec Kit extension command format.
- **Setup Enhancements**: `/speckit.sf.setup` now initializes `.specify/` directories and copies bundled templates on first run.

### Changed
- **Full Skill Sync**: All 18 lifecycle commands updated from the latest standalone SFSpeckit skills (v1.1.0), adapted for the Spec Kit extension format (`.specify/` paths, `/speckit.sf.*` commands, optional accelerator discovery).
- **Code Analyzer v5**: Migrated all scanner references from legacy `@salesforce/sfdx-scanner` / `sf scanner run` to `code-analyzer` plugin and `sf code-analyzer run`.
- **Implement Workflow**: Deploy-before-commit guardrail, standardized branch naming, API limit kill switch in auto-heal loop, and expanded scoring gate validation.
- **Verify Workflow**: Pre-verification deployment guardrails, runtime telemetry analysis, and formal evidence document template.
- **Deploy Workflow**: Destructive changes human-in-the-loop gate and automated rollback strategy for phased deployments.
- **PR Workflow**: Code Analyzer v5 security scan, DFA analysis, and scanner penalty scoring.
- **Clarify Workflow**: Expanded stakeholder sign-off report with org drift audit and deep business gap analysis.
- **Plan Workflow**: CLI-driven blast radius / impact analysis via Tooling API dependency queries.
- **Extension Manifest**: Bumped to 19 commands; updated command descriptions to match latest skill capabilities.
- **README**: Updated lifecycle diagram and command table to include `/speckit.sf.analyze` in the build phase.

### Fixed
- **Template Paths**: Corrected template references from `.agents/skills/` to `.specify/templates/` across all commands.
- **Legacy References**: Removed Spectrum Engine and `sfspeckit-data/` path references from extension commands.

## [1.0.0] - 2026-04-13

### Added
- **Extension Identity**: Formally registered as `sf` extension for Spec-Kit.
- **Hybrid AI Architecture**: Implemented a "Self-Contained but Aware" model. The extension works with zero dependencies but can leverage existing Salesforce agent skills as optional accelerators.
- **Unified Scoring Rubric**: Created `docs/scoring.md` featuring a 555-point expert rubric for Metadata, Apex, Flow, and LWC.
- **Automated Setup**: Added `/speckit.sf.setup` command to automatically install Salesforce CLI, GitHub CLI, and Code Analyzer v5.
- **Salesforce Code Analyzer v5 Support**: Full integration with PMD 7 and DFA scanner engines.
- **Auto-Heal Implementation Loop**: Added automated remediation logic to `/speckit.sf.implement` (up to 3 retries).
- **Blast Radius Analysis**: Integrated CLI-driven dependency mapping in `/speckit.sf.plan` to prevent architectural regressions.
- **17 Lifecycle Commands**: Complete coverage from Project Constitution to Multi-org Deployment.
- **Zero-Dependency Mode**: Removed requirement for external foundational skills; all best-practice knowledge is now embedded in the extension documentation.

### Fixed
- **Manifest**: Registered `/speckit.sf.setup` in `extension.yml` to enable CLI discovery.
- **Documentation**: Standardized official homepage link to GitHub Pages across manifest and README.
- **Branding**: Completed final audit and removal of legacy agentskills.io references.

### Removed
- Deleted standalone migration guides in favor of a clean, unified workflow.
- Removed hard dependencies on external agent skills.

---
© 2026 Sumanth Yanamala
