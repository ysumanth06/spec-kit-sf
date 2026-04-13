---
description: "Run full regression tests across all stories in a feature."
---

# Full Regression Testing

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

```bash
# Dry-run first
sf project deploy start \
  --source-dir force-app \
  --target-org qa \
  --test-level RunLocalTests \
  --dry-run

# If dry-run succeeds, deploy
sf project deploy start \
  --source-dir force-app \
  --target-org qa \
  --test-level RunLocalTests
```

If dry-run fails: report compilation errors and identify which story likely introduced them.

### Step 3: Run ALL Apex Tests

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
1. Check if it was PASS in any individual story's QA results
2. If a previously-passing test now FAILS → **REGRESSION**
3. Map the regression to which story likely introduced it via Git blame

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

### Regressions Detected
| Test | Was | Now | Likely Cause |
|------|-----|-----|-------------|
| InvoiceServiceTest.testCreate | ✅ PASS (story-01) | ❌ FAIL | story-02 modified InvoiceService |

### No Regressions
[List tests that continue to pass]
```

### Step 7: Determine Verdict

- **Zero regressions** → PASS: "Feature is regression-free."
- **Regressions found** → FAIL: List specific regressions with likely causing story. Recommend fix before proceeding.

## Next Step

If PASS: Run `/speckit.sf.score` for the full quality dashboard.

## Output

- **Regression report**: Detailed analysis with attribution
- **Verdict**: PASS (no regressions) or FAIL (regressions detected)

## Notes

- Run AFTER all story PRs are merged to the feature branch
- Regressions are often caused by shared objects: triggers, utility classes, permission sets
- After fix, re-run `/speckit.sf.regression` to confirm
