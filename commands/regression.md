---
description: "Full feature regression before release."
---

# Feature Regression Testing

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- All stories merged to the feature branch
- QA Sandbox available (`--target-org qa`)
- Feature branch is deployable

## Instructions

### Step 1: Identify Feature Context

1. Determine which feature is being tested (read from current branch or user input)
2. Read all story files in `.specify/specs/NNN-feature-name/`
3. Collect all Apex test classes across all stories
4. Collect all LWC test files across all stories

### Step 2: Deploy Full Feature Branch to QA

Deploy the entire feature branch to the QA sandbox:

```bash
sf project deploy start \
  --source-dir force-app \
  --target-org qa \
  --test-level RunLocalTests \
  --dry-run
```

If dry-run succeeds:
```bash
sf project deploy start \
  --source-dir force-app \
  --target-org qa \
  --test-level RunLocalTests
```

If dry-run fails: report compilation errors and identify which story likely introduced them.

### Step 3: Run ALL Apex Tests

Run all local tests (not just story-specific ones):

```bash
sf apex run test \
  --test-level RunLocalTests \
  --code-coverage \
  --result-format json \
  --target-org qa \
  --wait 15
```

### Step 4: Run ALL Jest Tests

```bash
npx lwc-jest --json
```

### Step 5: Compare Results

For each test:
1. Check if this test was reported as PASS in any individual story's QA results
2. If a previously-passing test now FAILS → this is a **REGRESSION**
3. Map the regression to which story likely introduced it:
   - Check which story's files the failing test references
   - Check Git blame to see which story branch last modified the relevant code

### Step 6: Generate Regression Report

```markdown

## Regression Report: Feature NNN-feature-name

### Overall Results
- Total Apex tests: XX
- Passed: XX
- Failed: XX
- Regressions detected: XX

### Code Coverage
| Class | Coverage | Per-Story Coverage | Delta |
|-------|----------|-------------------|-------|
| InvoiceService | 88% | 95% (story-01) | -7% ⚠️ |
| InvoiceProcessor | 92% | 92% (story-02) | 0% ✅ |

### Regressions Detected
| Test | Was | Now | Likely Cause |
|------|-----|-----|-------------|
| InvoiceServiceTest.testCreate | ✅ PASS (story-01) | ❌ FAIL | story-02 modified InvoiceService |

### No Regressions
[List tests that continue to pass]

### New Tests (not in individual stories)
[List any tests that only exist in the merged branch]
```

### Step 7: Determine Verdict

- If **zero regressions** → PASS: "Feature is regression-free. Ready for `/speckit.sf.score`."
- If **regressions found** → FAIL: 
  - List specific regressions with likely causing story
  - Recommend: "Return to developer of story-02 to fix regression before proceeding"

## Error Handling

- **Prerequisite Missing**: STOP and inform the user of the missing context.

## Notes

- This should be run AFTER all story PRs are merged to the feature branch
- Regressions are often caused by shared objects: triggers, utility classes, permission sets
- If a regression is found, the developer of the causing story should fix it, not the QA tester
- After fix, re-run `/speckit.sf.regression` to confirm

## Next Step

If PASS: Run `/speckit.sf.score` for the full quality dashboard.
