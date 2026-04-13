---
description: "Emergency production bug fix workflow with fast-track deployment."
---

# Emergency Production Fix

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Production access configured: `sf org login web --alias prod`
- Developer authenticated to Dev Sandbox
- Constitution exists at `.specify/memory/constitution.md` (for reference)

## Instructions

### Step 1: Assess the Bug

Gather critical information:
1. **Severity**: Is this a P0 (system down) or P1 (major feature broken)?
2. **Impact**: How many users are affected?
3. **Root cause**: What is the suspected cause?
4. **Reproduction steps**: How to reproduce the bug?

### Step 2: Create Hotfix Branch

```bash
git checkout main
git pull origin main
git checkout -b hotfix/YYYYMMDD-brief-description
```

### Step 3: Create Minimal Hotfix Story

Create a lightweight story file:
- **Location**: `.specify/specs/hotfix/hotfix-YYYYMMDD-description.md`
- **Content**: Minimal — just the bug description, fix approach, and test plan
- **Skip**: Full scoring gates, full Constitution check (speed over ceremony)

### Step 4: Implement the Fix

1. Make the minimal code change to fix the bug
2. Write a focused test that reproduces the bug and verifies the fix
3. Run the test:
   ```bash
   sf apex run test --class-names [HotfixTestClass] --code-coverage --target-org dev
   ```

### Step 5: Security Quick-Check

Even for hotfixes, verify:
- [ ] No hardcoded IDs introduced
- [ ] `with sharing` maintained
- [ ] `WITH USER_MODE` on new SOQL (if any)
- [ ] No credentials exposed

```bash
sf scanner run --target "force-app/main/default/classes/[ChangedFile].cls" --engine pmd
```

### Step 6: Deploy to Production

```bash
# Dry-run first (ALWAYS)
sf project deploy start \
  --source-dir force-app \
  --target-org prod \
  --test-level RunSpecifiedTests \
  --tests [HotfixTestClass] \
  --dry-run

# If dry-run passes, deploy
sf project deploy start \
  --source-dir force-app \
  --target-org prod \
  --test-level RunSpecifiedTests \
  --tests [HotfixTestClass]
```

### Step 7: Verify in Production

1. Confirm the bug is fixed in production
2. Run smoke tests
3. Monitor for 30 minutes

### Step 8: Backport

After production is stable:
1. Merge hotfix branch to main: `git checkout main && git merge hotfix/...`
2. Merge to any active feature branches that need the fix
3. Update any affected story files if in progress

### Step 9: Post-Mortem

Create a brief incident report:
- What broke and when
- Root cause
- Fix applied
- Prevention measures

## Next Step

After hotfix is deployed, run `/speckit.sf.release-notes` to update release documentation.

## Output

- **Hotfix deployed**: Code deployed to production
- **Hotfix story**: `.specify/specs/hotfix/hotfix-YYYYMMDD-description.md`
- **Test results**: Hotfix test verification

## Error Handling

- **Dry-run failure**: STOP. Do not deploy a hot fix that doesn't pass validation.
- **Test failure**: STOP. Fix the test or the code before deploying.
- **Deployment failure**: Escalate immediately. Check for locking, permissions, or compilation errors.

## Notes

- Hotfixes bypass the full SDD cycle (no full specification, no story decomposition)
- Minimum required: bug description, fix, test, deploy
- Always backport to main and active feature branches after deployment
