# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-13

### Added

- Initial release as a Spec Kit community extension
- 17 commands covering the full Salesforce SDD lifecycle:
  - **Foundation**: `constitution`
  - **Core SDD Cycle**: `specify`, `clarify`, `plan`, `stories`, `implement`
  - **Extended Lifecycle**: `review`, `change`, `qa`, `pr`, `verify`, `deploy`, `score`, `hotfix`, `regression`, `release-notes`, `uat`
- 2 lifecycle hooks: `after_tasks` → review, `after_implement` → verify
- Config template for org aliases, scoring thresholds, and deployment settings
- Dynamic skill discovery — auto-detects and uses installed Salesforce domain skills
- Documentation: workflow guide, scoring system, migration guide from standalone SFSpeckit
