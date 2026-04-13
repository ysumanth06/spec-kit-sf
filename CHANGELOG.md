# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

### Changed
- Migrated from standalone SFSpeckit scripts to Spec-Kit native markdown command architecture.
- Replaced the custom Python/Bash CLI wrapper with the native `specify` engine.
- Refined the "Spectrum Engine" logic into agent-native instructions.

### Removed
- Deleted standalone migration guides in favor of a clean, unified workflow.
- Removed hard dependencies on external agent skills.

---
© 2026 Sumanth Yanamala
