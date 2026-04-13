---
description: "Prepare a PR with scoring gates and code review checklist."
---

# Prepare Code Review

## User Input

$ARGUMENTS

## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Salesforce Quality & Deployment** (`sf-apex`, `sf-lwc`, `sf-testing`, `sf-deploy`)
- **Metadata Auditing** (`sf-metadata`, `sf-permissions`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in verification and scoring. However, the standards in `docs/scoring.md` are the **primary source of truth**.

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Story status is **IMPLEMENTED** (completed by `/speckit.sf.implement`)
- Story branch exists
- All implementation layers are marked `[x]` in the story file
- Salesforce Code Analyzer plugin installed: `sf plugins install @salesforce/sfdx-scanner`
- **Verification Evidence** exists: `.specify/specs/[feature]/test-logs/story-$ID-verify.md`

## Instructions

### Step 1: Check Code Analyzer

1. Verify if `sf scanner run` is available.
2. If NOT available:
   - Prompt: "Salesforce Code Analyzer is not installed. Would you like to install it now?"
   - **WARNING: Proceeding without the Code Analyzer is a SECURITY RISK.**

### Step 2: Run All Scoring Gates

Evaluate the implementation using the **Best Practices Checklist** in `docs/scoring.md`.

**Security Scan (Scanner)**:
- Run: `sf scanner run --target "force-app/" --engine pmd,eslint-lwc`
- **Mandatory Gate**: ZERO Severity 1 (Critical) or Severity 2 (High) violations.
- If violations exist → STOP and inform developer.

**Metadata scoring** (if story has metadata): Target ≥ 84/120

**Apex scoring** (if story has Apex):
- **Scanner Penalty**: -10 points for every Severity 3 (Moderate) PMD violation.
- Check: Bulkification, Security, No hardcoded IDs, Error handling, SOLID principles.
- Target: ≥ 90/150

**LWC scoring** (if story has LWC):
- **Scanner Penalty**: -5 points for every ESLint violation.
- Check: SLDS 2 compliance, Accessibility, Performance.
- Target: ≥ 125/165

**Data Flow Analysis (Architect-Ready Scan)**:
- Run: `sf scanner run dfa --target "force-app/main/default/classes" --projectdir "force-app/"`
- Any high-risk DFA finding must be documented in the PR description.

### Step 3: Generate PR Description

```markdown
## Story: $STORY_ID — $STORY_TITLE

**Jira**: $JIRA_LINK
**Type**: $STORY_TYPE (FULL / DECLARATIVE)
**Branch**: story/$BRANCH → feature/$FEATURE_BRANCH

### Requirements
[Extract from story's Requirements section]

### Acceptance Criteria
[Extract from story's Acceptance Criteria]

### Files Changed
| File | Type | Action |
|------|------|--------|
| [file path] | [Apex/LWC/Flow/Metadata] | [Created/Modified] |

### Scoring Results
| Layer | Score | Threshold | Status |
|-------|-------|-----------|--------|
| Metadata | X/120 | 84 | ✅/❌ |
| Apex | X/150 | 90 | ✅/❌ |
| LWC | X/165 | 125 | ✅/❌ |
| Coverage | X% | 90% | ✅/❌ |

### Test Results
- **Evidence Document**: `.specify/specs/[feature]/test-logs/story-$ID-verify.md`
- Apex tests: X/Y passed
- Jest tests: X/Y passed
- Coverage: X%
```

### Step 4: Generate Code Review Checklist

```markdown
## Code Review Checklist

### Apex Review (Peer + Architect)
- [ ] Bulkification: No SOQL or DML inside loops
- [ ] Sharing: `with sharing` on all classes
- [ ] SOQL Security: `WITH USER_MODE` on all queries
- [ ] No Hardcoded IDs
- [ ] Error Handling: Try-catch with meaningful messages
- [ ] Layer Separation: Service ≠ Selector ≠ Controller ≠ Trigger

### LWC Review (Peer + Architect)
- [ ] SLDS 2 compliance
- [ ] Accessibility: Keyboard nav, ARIA labels
- [ ] Performance: Wire service for reads, imperative for writes

### Test Review (Peer)
- [ ] PNB Pattern present
- [ ] Bulk Test: 251+ records
- [ ] TestDataFactory used (no inline test data)
- [ ] Coverage ≥ 90%

### General Review (Architect)
- [ ] Constitution Compliance
- [ ] Scope within story boundaries
- [ ] Deployment Safety
```

### Step 5: Push Branch & Create PR

```bash
git push origin story/$FEATURE_NUMBER-$STORY_NUMBER-$STORY_SLUG
```

#### Option A: Automated (GitHub CLI)
```bash
gh pr create \
  --title "Story: $STORY_ID — $STORY_TITLE" \
  --body-file [path_to_generated_description] \
  --base feature/$FEATURE_NUMBER-$FEATURE_SLUG \
  --head story/$FEATURE_NUMBER-$STORY_NUMBER-$STORY_SLUG
```

#### Option B: Manual (Fallback)
If `gh` is NOT installed, provide the PR description and a direct link to create it manually.

### Step 6: Update Story File

- Set **State** to `REVIEW`
- Record the **PR Link**
- Update **Scoring Gates** with actual scores

## Next Step

PR must be approved by BOTH a Peer Developer AND the Architect before merging. After merge, run `/speckit.sf.qa` for QA verification.

## Output

- **PR URL**: Direct link to the created Pull Request
- **Code review checklist**: Structured reviewer guide
- **Story file updated**: Status → REVIEW, scores and PR link recorded

## GATE

**PR must be approved by BOTH a Peer Developer AND the Architect before merging to the feature branch.**
