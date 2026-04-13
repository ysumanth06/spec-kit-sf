---
description: "Promote Salesforce code across environments (Dev to QA to UAT to Prod)."
---

# Environment Promotion

## User Input

$ARGUMENTS

## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Salesforce Deployment** (`sf-deploy`, `sf-metadata`)
- **Environment Management** (`sf-connected-apps`, `sf-data`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in promoting code across environments. However, the standards in `docs/scoring.md` are the **primary source of truth**.

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
- [ ] BPO UAT sign-off received
- [ ] Architect final sign-off
- [ ] Release notes prepared

If any prerequisite fails → STOP and report what's missing.

### Step 2: Read Deployment Context

1. Read the plan: `.specify/specs/NNN-feature-name/plan.md`
2. Read `sfdx-project.json` for source paths
3. Confirm target org:
   ```bash
   sf org display --target-org $TARGET_ENV
   ```

### Step 3: Dry-Run Validation

ALWAYS run dry-run first:

```bash
sf project deploy start \
  --source-dir force-app \
  --target-org $TARGET_ENV \
  --test-level RunLocalTests \
  --dry-run \
  --wait 15
```

If dry-run fails: Parse errors, categorize them, report with suggested fixes, STOP.

### Step 4: Deploy (if dry-run passes)

```bash
sf project deploy start \
  --source-dir force-app \
  --target-org $TARGET_ENV \
  --test-level RunLocalTests \
  --wait 15
```

If metadata dependencies cause issues, deploy in phases:
1. Objects + Fields (NoTestRun)
2. Permission Sets (NoTestRun)
3. Apex Classes + Tests (RunLocalTests)
4. Flows as Draft (NoTestRun)
5. Activate Flows
6. LWC Components (NoTestRun)

### Step 5: Post-Deployment Verification

```bash
sf apex run test \
  --test-level RunLocalTests \
  --code-coverage \
  --result-format json \
  --target-org $TARGET_ENV
```

### Step 6: Update Story Statuses

- **QA**: Update statuses to QA-READY
- **UAT**: Inform BPO that UAT environment is ready
- **Production**: Update all statuses to DONE, record deployment date 🎉

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

## Output

- **Deployment**: Code promoted to target environment
- **Story files updated**: Status updated based on target
- **Test results**: Post-deployment verification results

## Production Safety

For production deployments:
1. ALWAYS dry-run first
2. Deploy during maintenance window if possible
3. Have rollback plan ready (previous Git tag)
4. Monitor for 30 minutes post-deploy
5. Verify with smoke tests in production

## Error Handling

- **Dry-run failure**: Report errors, suggest fixes, do NOT proceed
- **Deployment failure**: Report error, check for locking/conflicts, suggest rollback
- **Test failure post-deploy**: Report failing tests, recommend investigation
