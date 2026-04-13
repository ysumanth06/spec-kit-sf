# SFSpeckit Workflow Guide

The complete Salesforce Spec-Driven Development lifecycle, from project setup to production release.

## Lifecycle Overview

```
/speckit.sf.constitution   ─── Run once per project
        │
/speckit.sf.specify        ─── Create feature spec
        │
/speckit.sf.clarify        ─── Gap analysis + org drift
        │
/speckit.sf.plan           ─── Technical architecture + blast radius
        │
/speckit.sf.stories        ─── Decompose into developer stories
        │
/speckit.sf.review         ─── TPO + Architect approval gate
        │
/speckit.sf.implement      ─── Build each story (auto-heal loop)
        │
/speckit.sf.verify         ─── Generate verification evidence
        │
/speckit.sf.pr             ─── PR with scoring + security scan
        │
/speckit.sf.qa             ─── Technical QA + persona coverage
        │
/speckit.sf.uat            ─── Business sign-off
        │
/speckit.sf.regression     ─── Cross-story regression testing
        │
/speckit.sf.score          ─── 555-point quality dashboard
        │
/speckit.sf.deploy         ─── Multi-environment promotion
        │
/speckit.sf.release-notes  ─── Auto-generated release docs
```

## Phase 1: Foundation

### `/speckit.sf.constitution`

Run **once per project**. Creates the constitution document with 9 Salesforce-specific articles that govern all development:

1. Metadata-First
2. Governor-Limit Awareness
3. Declarative-First (Flow vs. Apex)
4. Security-by-Default
5. PNB Test-First
6. Separation of Concerns
7. Deployment Safety
8. Agent Architecture
9. Cross-Skill Orchestration

Includes **Environmental Discovery** — CLI scans your org to detect installed packages, existing Flows vs. Apex ratio, and integration endpoints.

## Phase 2: Specification

### `/speckit.sf.specify <feature description>`

Creates a numbered feature directory (`.specify/specs/NNN-feature-slug/`) with a full specification including:
- User stories with P1/P2/P3 priorities
- Acceptance criteria (Given/When/Then)
- Salesforce Platform Context
- Automation Approach decisions (Flow vs. Apex per behavior)
- Object Map and Security Model

### `/speckit.sf.clarify`

Two-mode gap analysis:
- **Draft Mode**: Generates a Clarification Report for business stakeholders
- **Interactive Mode**: Resolves questions in real-time and updates the spec

Includes **Org Drift Detection** — CLI compares your spec's object map against the actual org to catch manual changes.

## Phase 3: Technical Design

### `/speckit.sf.plan`

Creates the technical implementation plan with:
- Complete `force-app/` file structure
- Data model (objects, fields, relationships)
- Apex/Flow/LWC architecture
- 7-phase deployment order
- Scoring gate thresholds
- **Blast Radius Analysis** — queries the Tooling API to detect dependent components

**Gate**: Plan requires Architect Sign-Off before stories can be generated.

## Phase 4: Story Generation

### `/speckit.sf.stories`

Decomposes the plan into self-contained, Jira-ready developer stories:
- Story-000 (Foundation) always generated first — blocks all others
- Each story includes security matrix, test cases, file paths, effort estimates
- Dependency graph shows parallel vs. sequential work

### `/speckit.sf.review`

Two-part review gate:
- **Architect**: Validates dependency graph, deployment order, merge conflict risks
- **TPO**: Validates coverage, sprint fit, scope boundaries

Stories move from DRAFT → READY after approval.

## Phase 5: Implementation

### `/speckit.sf.implement <story_file>`

Builds each story in Salesforce deployment order:
1. Metadata (objects, fields, permissions)
2. Apex (Selector → Service → TriggerAction → Controller)
3. Flow (deploy as Draft, then activate)
4. LWC (SLDS 2, accessibility, Jest tests)

**Auto-Heal Loop**: If a scoring gate fails, the AI automatically analyzes the deduction, refactors the code, and re-scores (up to 3 retries).

### `/speckit.sf.verify`

Generates formal Verification Evidence with:
- Test execution summary
- Code coverage heatmap
- Runtime telemetry (SOQL count, CPU time, DML rows)
- Security scanner snapshot

## Phase 6: Code Review & QA

### `/speckit.sf.pr`

Creates a PR with:
- Full scoring results (Metadata, Apex, LWC, Coverage)
- Security scan (PMD + DFA)
- Structured review checklist

### `/speckit.sf.qa`

Technical QA verification:
- Manual test scripts generated from acceptance criteria
- Automated Apex/Jest test execution
- Persona Coverage Matrix (verifies access for each profile/permission set)
- Traceability Matrix (maps every AC to test coverage)

### `/speckit.sf.uat`

Business UAT scripts in **non-technical language** for BPO sign-off.

## Phase 7: Quality & Release

### `/speckit.sf.regression`

After all stories merge: deploys full feature to QA, runs all tests, detects regressions with attribution to causing story.

### `/speckit.sf.score`

555-point quality dashboard showing per-story and per-layer scores with an overall grade (A/B/C/D/F).

### `/speckit.sf.deploy <target>`

Multi-environment promotion with dry-run gates, phased deployment fallback, and post-deploy verification.

### `/speckit.sf.release-notes`

Auto-generates release documentation aggregating all story results, scoring, and quality metrics.

## Emergency: `/speckit.sf.hotfix`

Bypasses the full SDD cycle for critical production bugs. Minimal workflow: assess → fix → test → deploy → backport.

## Mid-Sprint: `/speckit.sf.change`

Handles requirement changes during active development. Generates impact report showing affected stories and effort delta.
