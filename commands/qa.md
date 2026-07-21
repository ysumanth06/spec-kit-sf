---
description: "Generate manual test scripts and run automated Apex/Jest tests."
---

# QA Story Verification

## User Input

$ARGUMENTS

## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Salesforce QA & Testing** (`sf-testing`, `sf-apex`, `sf-lwc`)
- **Persona/Access Auditing** (`sf-permissions`, `sf-data`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in generating test scripts and persona coverage. However, the standards in `docs/scoring.md` are the **primary source of truth**.

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Story status is **REVIEW** or higher (code review completed)
- Story code is deployed to QA Sandbox (`--target-org qa`)
- QA tester authenticated to QA org

## Instructions

### Step 1: Read Story Context

1. Read the story file
2. Extract:
   - Acceptance criteria (Given/When/Then)
   - **Security & Access Matrix** (the personas to be tested)
   - Test cases (Positive, Negative, Bulk)
   - Implementation layers (which Apex classes, LWC components, Flows)
   - Scoring gates

### Step 2: Analyze Persona Coverage Requirements

1. For each Profile or Permission Set listed in the story's **Security & Access Matrix**:
   - Identify which functional ACs it must be tested against.
   - Identify "Negative" personas (those who should NOT have access).
2. Ensure the generated test scripts (Step 3) explicitly set the persona context (e.g., "Log in as Sales Rep").

### Step 3: Generate Manual Test Scripts

Read `.specify/templates/test-scripts-template.md` (or the project's `.specify/templates/test-scripts-template.md` if customized) and generate test scripts for each acceptance criterion:

For each acceptance criterion:
1. Convert Given/When/Then into step-by-step clickpath instructions.
2. **Assign a Persona**: Explicitly state which Profile/Permission Set from the Security Matrix should be used for this specific test.
3. Create a table with columns: Step | Action | Expected Result | Pass/Fail | Notes.
4. Add preconditions (user permissions, test data requirements).
5. Add cleanup instructions.

### Step 4: Run Automated Apex Tests

Execute Apex tests for classes listed in the story:

```bash
sf apex run test \
  --class-names [TestClass1,TestClass2,...] \
  --code-coverage \
  --result-format json \
  --target-org qa \
  --wait 10
```

### Step 5: Run Jest Tests (if LWC)

If the story includes LWC components:

```bash
npx lwc-jest -- --testPathPattern [componentName] --json
```

### Step 6: Build Persona Coverage Matrix

Cross-reference every persona from the story's **Security & Access Matrix** with the tests performed:

| Persona | Object Access | Field Security | Result | Method |
|---------|---------------|----------------|--------|--------|
| [Name] | [✅/❌] | [✅/❌] | PASS/FAIL | Automated (runAs) |
| [Name] | [✅/❌] | [✅/❌] | PASS/FAIL | Manual (TC-XXX) |

Ensure every persona has at least one associated test result.

### Step 7: Build Traceability Matrix

Map every acceptance criterion to its test coverage:

| AC # | Description | Automated Test | Manual Script | Status |
|------|-------------|---------------|---------------|--------|
| AC-1 | [Brief] | TestClass.method ✅ | TC-001 ⏳ | Partial |

### Step 8: Prepare for UAT

**Next Step**: "Technical QA PASSED. Run `/speckit.sf.uat` to begin the business sign-off process."

### Step 9: Write Test Scripts File

Save technical results (Persona Matrix, Traceability Matrix, Manual Scripts) to:
`.specify/specs/NNN-feature-name/task_story_NN_test_scripts.md`

### Step 10: Update Story File

Update the story file's QA Results section:
- **Technical Tests**: X/Y passed
- **Persona Coverage**: X/Y confirmed
- **State**: If all tests pass, set to `QA_READY`.

### Step 11: QA Bug Remediation Flow

If a bug is discovered during testing:

1. **Do NOT create a new branch or story file**.
2. Set the Story State to `QA_FAILED`.
3. Document the bug details (Steps to Reproduce, Expected, Actual) in the **QA Results** section.
4. Return the story to the developer.
5. **Developer Action**: Check out the existing `story/` branch, fix the bug, deploy to the SF Dev org, verify with `/speckit.sf.verify`, and push to the existing PR.
6. Once the developer's fix is deployed to the QA Sandbox, run `/speckit.sf.qa` again.

## Error Handling

- **Prerequisite Missing**: STOP and inform the user of the missing context.

## Notes

- Manual test scripts require QA to EXECUTE them in the org and record Pass/Fail
- UAT scripts are for BPO reviewers in the UAT sandbox (separate phase)
- If automated tests fail, story should be returned to developer before manual testing

## Next Step

Technical QA PASSED. Run `/speckit.sf.uat` to begin the business sign-off process.
