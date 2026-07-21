---
description: "Promote Salesforce code across environments (Dev to QA to UAT to Prod)."
---

# Environment Promotion

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

Depending on target environment:

| Target | Prerequisites |
|--------|--------------|
| `qa` | All stories merged to feature branch, code review completed |
| `uat` | QA verification passed, regression tests passed, scoring gates met |
| `prod` | BPO UAT sign-off completed, all stories DONE |

## Instructions

### Step 1: Validate Prerequisites

#### For QA deployment:
- [ ] All story PRs merged to feature branch
- [ ] All story statuses are REVIEW or higher
- [ ] No failing tests in dev sandbox

#### For UAT deployment:
- [ ] All stories passed QA verification (`/speckit.sf.qa`)
- [ ] Regression tests passed (`/speckit.sf.regression`)
- [ ] Feature scoring meets thresholds (`/speckit.sf.score`)

#### For Production deployment:
- [ ] All stories in DONE state
- [ ] BPO UAT sign-off received (documented in story files)
- [ ] Architect final sign-off
- [ ] Release notes prepared

If any prerequisite fails → STOP and report what's missing.

### Step 2: Read Deployment Context

1. Read the plan for deployment order: `.specify/specs/NNN-feature-name/plan.md`
2. Read `sfdx-project.json` for source paths
3. Confirm target org alias is configured:
   ```bash
   sf org display --target-org $TARGET_ENV
   ```

### Step 3: Destructive Changes & Dry-Run Validation

1. **Check for Destructive Changes**: Look for `force-app/main/default/destructiveChanges.xml` (or equivalent path).
2. **Human-in-the-Loop Gate**: If the file exists, STOP and output the contents to the console. Ask the Release Manager: "Destructive changes detected. Do you approve the execution of these deletions? (y/n)". Do NOT proceed without explicit typed approval.
3. **Dry-Run**: ALWAYS run dry-run first. If destructive changes exist and were approved, append `--post-destructive-changes destructiveChanges.xml`.

```bash
sf project deploy start \
  --source-dir force-app \
  --target-org $TARGET_ENV \
  --test-level RunLocalTests \
  --dry-run \
  --wait 15
```

If dry-run fails:
- Parse error output
- Categorize errors: compilation, test failure, missing dependency
- Report with suggested fixes
- STOP — do not proceed to actual deployment

### Step 4: Deploy (if dry-run passes)

If deploying the entire source directory at once works (most cases):

```bash
sf project deploy start \
  --source-dir force-app \
  --target-org $TARGET_ENV \
  --test-level RunLocalTests \
  --wait 15
```

If metadata dependencies cause issues, deploy in phases:

**Phase 1: Objects + Fields**
```bash
sf project deploy start \
  --source-dir force-app/main/default/objects \
  --target-org $TARGET_ENV \
  --test-level NoTestRun
```

**Phase 2: Permission Sets**
```bash
sf project deploy start \
  --source-dir force-app/main/default/permissionsets \
  --target-org $TARGET_ENV \
  --test-level NoTestRun
```

**Phase 3: Apex Classes + Tests**
```bash
sf project deploy start \
  --source-dir force-app/main/default/classes \
  --source-dir force-app/main/default/triggers \
  --target-org $TARGET_ENV \
  --test-level RunLocalTests
```

**Phase 4: Flows (as Draft)**
```bash
sf project deploy start \
  --source-dir force-app/main/default/flows \
  --target-org $TARGET_ENV \
  --test-level NoTestRun
```

**Phase 5: Activate Flows**
Activate flows using `sf project deploy start` after draft validation.

**Phase 6: LWC Components**
```bash
sf project deploy start \
  --source-dir force-app/main/default/lwc \
  --target-org $TARGET_ENV \
  --test-level NoTestRun
```

### Step 4.5: Automated Rollback Strategy

If a phased deployment fails mid-flight (e.g., Phase 3 fails after Phase 1 and 2 succeeded), the org may be in an inconsistent state.
1. **Halt and Alert**: Stop the deployment, report the specific errors, and alert the Release Manager.
2. **Identify Previous State**: Identify the Git commit SHA from immediately before the deployment started.
3. **Rollback Prompt**: Ask the user: "Deployment failed. Would you like to automatically rollback to the previous state (Commit SHA: $PREV_SHA)? (y/n)"
4. **Execute Rollback**: If approved, run `git checkout $PREV_SHA` and execute an atomic `sf project deploy start --source-dir force-app --target-org $TARGET_ENV --ignore-conflicts` to revert the org metadata, then run `git checkout -` to return to the current branch.

### Step 5: Post-Deployment Verification

After successful deployment:

```bash
# Run all tests in the target org
sf apex run test \
  --test-level RunLocalTests \
  --code-coverage \
  --result-format json \
  --target-org $TARGET_ENV
```

Verify:
- All tests pass
- Coverage meets thresholds
- No unexpected failures

### Step 6: Update Story Statuses

If deploying to QA:
- Update story statuses to QA-READY

If deploying to UAT:
- Inform BPO that UAT environment is ready for validation
- Reference UAT test scripts from `/speckit.sf.qa` output

If deploying to Production:
- Update all story statuses to DONE
- Record deployment date
- Congratulate the team 🎉

### Step 7: Report

```markdown

## Deployment Report

- **Target**: $TARGET_ENV
- **Status**: ✅ SUCCESS / ❌ FAILED
- **Dry-run**: Passed
- **Tests**: XX/YY passed
- **Coverage**: XX%
- **Duration**: X minutes
- **Components Deployed**: XX
```

## Error Handling

- **Prerequisite Missing**: STOP and inform the user of the missing context.

- **Dry-run failure**: Report errors, suggest fixes, do NOT proceed
- **Deployment failure**: Report error, check for locking/conflicts, suggest rollback
- **Test failure post-deploy**: Report failing tests, recommend investigation before promoting further

## Production Safety

For production deployments:
1. ALWAYS dry-run first
2. Deploy during maintenance window if possible
3. Have rollback plan ready (previous Git tag)
4. Monitor for 30 minutes post-deploy
5. Verify with smoke tests in production
