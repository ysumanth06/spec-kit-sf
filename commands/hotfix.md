---
description: "Emergency production bug fix workflow with fast-track deployment."
---

# Emergency Production Hotfix

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Production access configured: `sf org login web --alias prod`
- Developer authenticated to Dev Sandbox for testing
- Constitution exists (for reference, not blocking)

## Instructions

### Step 1: Create Hotfix Branch

```bash
git checkout main
git pull origin main
git checkout -b hotfix/HOTFIX-$ID-$SLUG
```

### Step 2: Generate Minimal Story File

Read `.specify/templates/hotfix-template.md` and create a hotfix story:
- Location: `.specify/specs/hotfixes/hotfix-$ID.md`
- Auto-fill: bug description from user input, date, severity
- Ask user for:
  - Severity: Critical / High / Medium
  - Environment where discovered
  - Steps to reproduce

### Step 3: Root Cause Analysis

1. Analyze the bug description
2. Use optional `sf-debug` accelerator skill if available if debug logs are available
3. Identify the root cause file and line number
4. Document in the hotfix story

### Step 4: Implement Fix

1. Make the minimum code change to fix the bug
2. Follow constitution articles (with sharing, user mode) even in hotfix
3. Add/update the specific test for this bug scenario:
   - Test that reproduces the exact bug (fails before fix, passes after)
   - Bulk test if trigger-related

### Step 5: Run Tests

```bash
sf apex run test --class-names [AffectedTestClass] --code-coverage --target-org dev
```

Verify:
- New test passes
- Existing tests still pass
- Coverage not decreased

### Step 6: Architect Review

Hotfixes still require architect approval:
- Present the fix for review
- Show root cause and minimal change
- Show test results
- Get approval before production deployment

### Step 7: Deploy to Production

```bash
# Dry-run first
sf project deploy start --source-dir force-app --target-org prod --test-level RunLocalTests --dry-run

# Deploy
sf project deploy start --source-dir force-app --target-org prod --test-level RunLocalTests
```

### Step 8: Back-Port

After successful production deploy:
```bash
# Merge hotfix to main
git checkout main
git merge hotfix/HOTFIX-$ID-$SLUG

# Back-port to open feature branches
git checkout feature/$OPEN_FEATURE_BRANCH
git merge main
```

### Step 9: Update Hotfix Story

- Mark hotfix story as DONE
- Record deployment date and verified-by

## Error Handling

- **Prerequisite Missing**: STOP and inform the user of the missing context.

## Notes

- Hotfixes bypass specify/clarify/plan/tasks but NEVER bypass testing and architect review
- Keep changes minimal — this is not the place for refactoring
- Document the root cause for future reference (prevents recurrence)
