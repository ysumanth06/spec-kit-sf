# QA Test Scripts: $STORY_ID — $STORY_TITLE

**Story**: [task_story_$NN.md](./task_story_$NN.md)
**Feature**: $FEATURE_NAME
**QA Tester**: [Name]
**Environment**: QA Sandbox (`--target-org qa`)
**Date Generated**: $DATE

---

## Automated Test Results

<!--
  Auto-populated by /speckit.sf.qa from Apex test execution.
-->

| Test Class | Method | Result | Duration |
|-----------|--------|--------|----------|
| $TestClass | $testMethod1 | ✅ PASS / ❌ FAIL | Xms |
| $TestClass | $testMethod2 | ✅ PASS / ❌ FAIL | Xms |

**Coverage**: $X% (target: 90%)

## Persona Coverage Matrix

<!--
  Ensures that every persona defined in the story's Security & Access Matrix
  was explicitly tested (either via runAs in Apex or manual walkthrough).
-->

| Persona | Object Access Tested | Field Security Verified | Method | Result |
|---------|----------------------|-------------------------|--------|--------|
| [Name] | [✅/❌] | [✅/❌] | Automated (runAs) | PASS/FAIL |
| [Name] | [✅/❌] | [✅/❌] | Manual (TC-XXX) | PASS/FAIL |

---

## Manual Test Scripts

<!--
  Generated from acceptance criteria in the story file.
  QA tester executes these step-by-step in the org and records Pass/Fail.
-->

### TC-001: $TEST_TITLE

**Acceptance Criteria**: AC-$N
**Preconditions**: [User has $PERMISSION_SET assigned, $RECORD exists]
**Test Data**: [Specific data needed — use test accounts/contacts, not production data]

| Step | Action | Expected Result | Pass/Fail | Notes |
|------|--------|----------------|-----------|-------|
| 1 | [Navigate to / open / click] | [Page loads / element visible] | | |
| 2 | [Enter / select / modify] | [Field accepts input / dropdown shows values] | | |
| 3 | [Click save / submit / action] | [Success toast / record created / redirect] | | |
| 4 | [Verify result] | [Record shows correct values / related list updated] | | |

**Cleanup**: [Delete test record / revert changes]
**Screenshots**: [Attach if applicable]

---

### TC-002: $TEST_TITLE (Negative)

**Acceptance Criteria**: AC-$N
**Preconditions**: [Same as TC-001]

| Step | Action | Expected Result | Pass/Fail | Notes |
|------|--------|----------------|-----------|-------|
| 1 | [Navigate to form] | [Form loads] | | |
| 2 | [Leave required field blank / enter invalid data] | [Field shows validation] | | |
| 3 | [Click save] | [Error message: "$ERROR_MESSAGE"] | | |
| 4 | [Verify no record created] | [Related list unchanged] | | |

---

### TC-003: $TEST_TITLE (Bulk/Performance)

**Acceptance Criteria**: AC-$N
**Preconditions**: [251+ test records exist in org]

| Step | Action | Expected Result | Pass/Fail | Notes |
|------|--------|----------------|-----------|-------|
| 1 | [Trigger bulk operation / data load] | [Process begins] | | |
| 2 | [Wait for completion] | [All records processed] | | |
| 3 | [Verify no errors in debug log] | [No governor limit exceptions] | | |
| 4 | [Spot-check 5 random records] | [All have correct values] | | |

---

[Add more test scripts as needed — one per acceptance criterion]

---

## Acceptance Criteria Traceability Matrix

<!--
  Maps every acceptance criterion to its test coverage (automated + manual).
  Ensures no AC is untested.
-->

| AC # | Acceptance Criteria | Automated Test | Manual Test | Status |
|------|--------------------|-----------------|----|--------|
| AC-1 | [Brief description] | [TestClass.method or —] | TC-001 | ⏳ Pending |
| AC-2 | [Brief description] | [TestClass.method] | — | ✅ Auto Pass |
| AC-3 | [Brief description] | — | TC-002 | ⏳ Pending |
| AC-4 | [Brief description] | [TestClass.method] | TC-003 | ⏳ Pending |

---

## QA Summary

| Category | Result |
|----------|--------|
| Automated tests | $X / $Y passed |
| Persona Coverage | $X / $Y confirmed |
| Manual test scripts | $X / $Y passed |
| Code coverage | $X% |
| **Overall Verdict** | ✅ PASS / ❌ FAIL |

**QA Tester**: [Name]
**Sign-Off Date**: [Date]
