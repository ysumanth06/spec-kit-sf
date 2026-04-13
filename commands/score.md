---
description: "555-point quality scoring dashboard across all stories in a feature."
---

# Quality Scoring Dashboard

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.
Use `scoring.*` thresholds if configured.

## Prerequisites

- Feature directory exists: `.specify/specs/NNN-feature-name/`
- At least one story file exists with scoring data
- Constitution exists: `.specify/memory/constitution.md`

## Instructions

### Step 1: Read All Feature Stories

1. Read all `task_story_*.md` files in the feature directory
2. Read the plan for scoring gate thresholds
3. Read the constitution for scoring standards

### Step 2: Collect Scoring Data

For each story, extract scores from the **Scoring Gates** section:

- **Metadata score** (X/120)
- **Apex score** (X/150)
- **Flow score** (X/110)
- **LWC score** (X/165)
- **Testing coverage** (X%)
- **Security scanner** (violations count)

### Step 3: Calculate Feature-Level Scores

Aggregate across all stories:

```markdown
## Feature Quality Dashboard: NNN-feature-name

### Per-Story Breakdown

| Story | Metadata | Apex | Flow | LWC | Coverage | Scanner | Total |
|-------|----------|------|------|-----|----------|---------|-------|
| 00 | 98/120 | — | — | — | 95% | 0 Sev1 | 98 |
| 01 | 105/120 | 135/150 | — | 148/165 | 92% | 0 Sev1 | 388 |
| 02 | — | 128/150 | 95/110 | — | 88% | 0 Sev1 | 223 |

### Feature Summary

| Layer | Average Score | Threshold | Status |
|-------|--------------|-----------|--------|
| Metadata | 102/120 (85%) | 84 (70%) | ✅ |
| Apex | 132/150 (88%) | 90 (60%) | ✅ |
| Flow | 95/110 (86%) | — | ✅ |
| LWC | 148/165 (90%) | 125 (76%) | ✅ |
| Coverage | 91% | 90% | ✅ |
| Security | 0 Critical | 0 | ✅ |

### Overall Feature Score: XXX/555

### Quality Grade
- **A (90-100%)**: Production-ready, exemplary quality
- **B (80-89%)**: Production-ready, minor improvements possible
- **C (70-79%)**: Acceptable, review recommended before production
- **D (60-69%)**: Below standard, remediation required
- **F (<60%)**: Not deployable, significant rework needed
```

### Step 4: Identify Weak Areas

For each layer below threshold:
- List specific stories causing the drag
- List specific deductions (from the scoring skill reports)
- Suggest remediation actions

### Step 5: Constitution Compliance Check

Verify all stories comply with key articles:
- Article I: Metadata-first approach followed?
- Article IV: All classes use `with sharing`?
- Article V: PNB test pattern in all test classes?
- Article VI: Separation of Concerns maintained?

### Step 6: Generate Recommendations

Based on the dashboard:
- **Ready for promotion**: If all gates pass, recommend `/speckit.sf.deploy`
- **Needs work**: If gates fail, list specific stories and layers to fix
- **Partial promotion**: If some stories pass, recommend partial deployment

## Next Step

If all scoring gates pass: Run `/speckit.sf.deploy qa` to promote to QA environment.

## Output

- **Dashboard**: Per-story and feature-level scoring breakdown
- **Grade**: Overall quality grade (A/B/C/D/F)
- **Recommendations**: Promotion readiness or remediation actions
