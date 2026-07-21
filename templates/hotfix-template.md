# HOTFIX: $HOTFIX_TITLE

**Branch**: hotfix/$HOTFIX_ID-$HOTFIX_SLUG
**Created**: $DATE
**Severity**: $SEVERITY <!-- Critical / High / Medium -->
**Author**: $AUTHOR
**Jira**: [PROJ-NNN]

---

## Bug Description

**Environment where discovered**: [Production / UAT / QA]
**Steps to reproduce**:
1. [Step 1]
2. [Step 2]
3. [Step 3 — error occurs]

**Expected behavior**: [What should happen]
**Actual behavior**: [What actually happens]
**Error message/log**: [Exact error, stack trace, or debug log excerpt]

---

## Root Cause Analysis

[What caused the bug — include file name, line number, logic flaw]

**Root cause file**: `force-app/main/default/classes/$FILE.cls` line $LINE
**Root cause**: [e.g., "Missing null check on Account.Industry before string comparison"]

---

## Fix Description

[Describe the fix in plain language — what changes and why]

**Files to modify**:

| File | Change |
|------|--------|
| `force-app/main/default/classes/$FILE.cls` | [Description of code change] |
| `force-app/main/default/classes/$FILETest.cls` | [New test for this scenario] |

---

## Test Case

### Positive Test
- [Verify the original functionality still works after fix]

### Regression Test
- [Verify the specific bug scenario is now handled correctly]

### Bulk Test (if applicable)
- [Verify fix works with 251+ records if trigger-related]

---

## Affected Environments

- [ ] Production (must deploy immediately)
- [ ] UAT Sandbox
- [ ] QA Sandbox
- [ ] Dev Sandbox

---

## Rollback Plan

**If the fix causes new issues**:
1. [Revert to previous version: `git revert $COMMIT`]
2. [Deploy previous version: `sf project deploy start --target-org prod`]
3. [Notify: $STAKEHOLDERS]

---

## Deployment

```bash
# 1. Deploy to production (dry-run first)
sf project deploy start --source-dir force-app --target-org prod --test-level RunLocalTests --dry-run

# 2. Deploy for real
sf project deploy start --source-dir force-app --target-org prod --test-level RunLocalTests

# 3. Back-port to feature branches
git checkout feature/$FEATURE_BRANCH
git merge hotfix/$HOTFIX_ID-$HOTFIX_SLUG
```

---

## Sign-Off

- **Developer**: [Name] — [ ] Fix implemented + tested
- **Architect**: [Name] — [ ] Code reviewed + approved
- **QA**: [Name] — [ ] Verified in staging
- **TPO**: [Name] — [ ] Approved for production deployment
