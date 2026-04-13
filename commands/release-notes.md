---
description: "Auto-generate release notes from completed stories and test results."
---

# Generate Feature Release Notes

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- All stories in the feature directory must be in `DONE` or `QA` state.
- Documentation directory exists: `.specify/specs/NNN-feature-name/test-logs/`

## Instructions

### Step 1: Inventory Feature Assets

1. Read the feature directory `.specify/specs/NNN-feature-name/`
2. Collect:
   - All `task_story_NN.md` files
   - All `test-logs/story-NN-verify.md` evidence files
   - The original `spec.md` for context
   - The implementation `plan.md` for scoring gate thresholds

### Step 2: Aggregate Statistics

Calculate cumulative stats:
- **Total Stories**: X
- **Development Hours**: Total (from story estimation tables)
- **Test Coverage**: Weighted average across all classes/components
- **Scoring Quality**: Average scores for Apex, LWC, and Metadata

### Step 3: Extract Feature Highlights

Generate a bulleted list of functional changes by reading the "Summary" section of each story file.

### Step 4: Generate Release Notes Document

Create `.specify/specs/NNN-feature-name/RELEASE_NOTES.md`:

```markdown
# 🚀 Release Notes: $FEATURE_NAME (NNN)

**Release Date**: $DATE
**Lead Developer**: $LIST
**TPO Approval**: [ ]

## 1. Executive Summary
Brief summary of the feature's business impact.

## 2. Functional Highlights (What's New)
- **$STORY_TITLE**: $STORY_DESCRIPTION
- ... (repeat for all DONE stories)

## 3. Quality & Assurance Snapshot
| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Unit Test Coverage | XX% | 75% | ✅ |
| Avg. Apex Quality | 142/150 | 90 | ✅ |
| Avg. LWC Quality | 158/165 | 125 | ✅ |
| Security Scanner | 0 Critical | 0 | ✅ |

## 4. Technical Inventory
### New Objects/Fields
- [List from Story-000]

### New/Modified Code
- [Class List]
- [LWC List]

## 5. Verification & Testing
Links to all unit test evidence documents.

## 6. Known Issues / Deferred Items
(Extracted from plan.md "Out of Scope")
```

### Step 5: Present to User

Show the location of the `RELEASE_NOTES.md` and suggest: "Release notes generated. Review and commit to the main branch before final deployment."

## Output

- **File created**: `.specify/specs/NNN-feature-name/RELEASE_NOTES.md`
- **Summary**: Concise stats on coverage, quality, and story completion
