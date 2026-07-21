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

- Story status is **IMPLEMENTED** (completed by /speckit.sf.implement)
- Story branch exists: `story/$FEATURE_NUMBER-$STORY_NUMBER-$STORY_SLUG`
- All implementation layers are marked `[x]` in the story file
- Salesforce Code Analyzer (v5) installed: `sf plugins install code-analyzer`
- **Verification Evidence** exists: `.specify/specs/[feature]/test-logs/story-$ID-verify.md`

## Instructions

### Step 1.5: Check Code Analyzer

1. Verify if `sf code-analyzer run` is available.
2. If NOT available:
   - Prompt: "Salesforce Code Analyzer (v5) is not installed. Would you like to install it now? (`sf plugins install code-analyzer`)"
   - If user declines:
     - **WARNING: Proceeding without the Code Analyzer is a SECURITY RISK. The automated PR will not include a Security Score, forcing a manual and much slower review by the Architect.**
     - Ask: "Are you sure you want to proceed without static analysis? (y/n)"
   - If user agrees to install: Install and rerun this command.

### Step 2: Run All Scoring Gates

Execute scoring for every artifact layer in this story:

**Security Scan (Code Analyzer v5)**:
- Run full scan on story files: `sf code-analyzer run --path "force-app/" --engine pmd,eslint`
- **Mandatory Gate**: ZERO Severity 1 (Critical) or Severity 2 (High) violations allowed.
- If violations exist → STOP and inform developer they must fix them before PR creation.

**Metadata scoring** (if story has metadata):
- Invoke sf-metadata scoring logic against objects/fields created
- Target: ≥ 84/120

**Apex scoring** (if story has Apex):
- Invoke sf-apex scoring logic against all Apex classes
- **Scanner Penalty**: -10 points for every Severity 3 (Moderate) violation found by PMD.
- Check for:
  - Bulkification compliance (no SOQL/DML in loops)
  - Security (`with sharing`, `WITH USER_MODE`)
  - No hardcoded IDs
  - Proper error handling
  - SOLID principles adherence
- Target: ≥ 90/150

**LWC scoring** (if story has LWC):
- Invoke sf-lwc scoring logic (PICKLES methodology)
- **Scanner Penalty**: -5 points for every ESLint violation found.
- Check for:
  - SLDS 2 compliance
  - Accessibility (keyboard nav, ARIA labels)
  - Performance (wire service, lazy loading)
- Target: ≥ 125/165

- Target: ≥ 90% coverage

**Data Flow Analysis (Architect-Ready Scan)**:
- Run Unified Scan: `sf code-analyzer run --path "force-app/main/default/classes" --engine pmd-dfa`
- Record any findings. Any high-risk DFA finding (Injection, FLS bypass) must be documented in the PR description.

### Step 3: Generate PR Description

Create a PR description from the story file content:

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
| sf-metadata | X/120 | 84 | ✅/❌ |
| sf-apex | X/150 | 90 | ✅/❌ |
| sf-lwc | X/165 | 125 | ✅/❌ |
| Coverage | X% | 90% | ✅/❌ |

### Test Results
- **Evidence Document**: [story-$STORY_ID-verify.md](file:///abs/path/to/evidence)
- Apex tests: X/Y passed
- Jest tests: X/Y passed
- Coverage: X%

### Dependencies
[Extract from story's Dependencies section]
```

### Step 4: Generate Code Review Checklist

Create the review checklist for the PR:

```markdown

## Code Review Checklist

### Apex Review (Peer + Architect)
- [ ] **Bulkification**: No SOQL or DML inside loops
- [ ] **Sharing**: `with sharing` used on all classes (or exception documented)
- [ ] **SOQL Security**: `WITH USER_MODE` or `WITH SECURITY_ENFORCED` on all queries
- [ ] **No Hardcoded IDs**: No 15/18-char record IDs in code
- [ ] **No Hardcoded URLs**: Using NavigationMixin or custom settings
- [ ] **Error Handling**: Try-catch with meaningful error messages
- [ ] **Layer Separation**: Service ≠ Selector ≠ Controller ≠ Trigger
- [ ] **Naming Conventions**: Match team standards from constitution

### LWC Review (Peer + Architect)
- [ ] **SLDS 2**: Using Lightning Design System tokens and components
- [ ] **Accessibility**: Keyboard navigation, ARIA labels, screen reader compatible
- [ ] **Performance**: Wire service for reads, imperative for writes
- [ ] **No Direct DML**: LWC never calls DML directly (always via Apex controller)
- [ ] **Error Handling**: Toast messages for user-facing errors

### Test Review (Peer)
- [ ] **PNB Pattern**: Positive, Negative, and Bulk tests present
- [ ] **Bulk Test**: 251+ records tested (crosses batch boundary)
- [ ] **TestDataFactory**: No inline test data creation
- [ ] **Assert Class**: Using `Assert.areEqual()` with descriptive messages
- [ ] **Coverage**: ≥ 90% on all production classes
- [ ] **SeeAllData**: `@IsTest(SeeAllData=false)` on all test classes

### General Review (Architect)
- [ ] **Constitution Compliance**: No violations of Articles I–IX
- [ ] **Scope**: Changes don't exceed story boundaries
- [ ] **Performance**: No N+1 query patterns, efficient Apex collections
- [ ] **Deployment Safety**: Safe to deploy in the defined deployment order
```

### Step 5: Push Branch

Before creating the PR, ensure all local changes are pushed to the remote repository:

```bash
# Push current story branch to origin
git push origin story/$FEATURE_NUMBER-$STORY_NUMBER-$STORY_SLUG
```

### Step 6: Create Remote Pull Request

Target branch: The **feature branch** for this project (e.g., `feature/001-smart-grid`).

#### Option A: Automated (GitHub CLI)
If `gh` is installed and authenticated:

```bash
gh pr create \
  --title "Story: $STORY_ID — $STORY_TITLE" \
  --body-file [path_to_generated_description_markdown] \
  --base feature/$FEATURE_NUMBER-$FEATURE_SLUG \
  --head story/$FEATURE_NUMBER-$STORY_NUMBER-$STORY_SLUG
```

#### Option B: Manual (Fallback)
If `gh` is NOT installed:
1. Inform the user: "GitHub CLI (`gh`) is missing. Install it with `brew install gh` for full automation."
2. Provide the generated **PR Description** and **Checklist** from Step 3 and 4.
3. Provide the direct link to create the PR manually: `https://github.com/ysumanth06/Salesforce-Smart-Grid/compare/feature/$FEATURE_SLUG...story/$STORY_SLUG`

### Step 7: Update Story File

Update the story file:
- Set **State** to `REVIEW`
- Record the **PR Link** in the story's `Links` or `State` section.
- Update **Scoring Gates** section with actual scores.

### Step 8: Final Summary

Show the developer:
- ✅ Scoring results (pass/fail per gate)
- ✅ Branch pushed to origin
- ✅ PR Created (Link: $PR_URL) or Instructions for manual creation
- ✅ Story status updated to REVIEW

## Error Handling

- **Prerequisite Missing**: STOP and inform the user of the missing context.

## GATE

**PR must be approved by BOTH a Peer Developer AND the Architect before merging to the feature branch.** This ensures code quality, security compliance, and architectural consistency.

## Next Step

PR must be approved by BOTH a Peer Developer AND the Architect before merging. After merge, run `/speckit.sf.qa` for QA verification.
