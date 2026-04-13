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

## Prerequisites

- Story status is **REVIEW** or higher (code review completed)
- Story code is deployed to QA Sandbox (`--target-org qa`)
- QA tester authenticated to QA org

## Instructions

### Step 1: Read Story Context

1. Read the story file
2. Extract: Acceptance criteria, Security & Access Matrix, Test cases, Implementation layers, Scoring gates

### Step 2: Analyze Persona Coverage Requirements

1. For each Profile or Permission Set in the story's **Security & Access Matrix**:
   - Identify which functional ACs it must be tested against.
   - Identify "Negative" personas (those who should NOT have access).
2. Ensure generated test scripts set the persona context (e.g., "Log in as Sales Rep").

### Step 3: Generate Manual Test Scripts

For each acceptance criterion:
1. Convert Given/When/Then into step-by-step clickpath instructions.
2. **Assign a Persona** from the Security Matrix.
3. Create a table: Step | Action | Expected Result | Pass/Fail | Notes.
4. Add preconditions and cleanup instructions.

### Step 4: Run Automated Apex Tests

```bash
sf apex run test \
  --class-names [TestClass1,TestClass2,...] \
  --code-coverage \
  --result-format json \
  --target-org qa \
  --wait 10
```

### Step 5: Run Jest Tests (if LWC)

```bash
npx lwc-jest -- --testPathPattern [componentName] --json
```

### Step 6: Build Persona Coverage Matrix

| Persona | Object Access | Field Security | Result | Method |
|---------|---------------|----------------|--------|--------|
| [Name] | [✅/❌] | [✅/❌] | PASS/FAIL | Automated (runAs) |
| [Name] | [✅/❌] | [✅/❌] | PASS/FAIL | Manual (TC-XXX) |

### Step 7: Build Traceability Matrix

| AC # | Description | Automated Test | Manual Script | Status |
|------|-------------|---------------|---------------|--------|
| AC-1 | [Brief] | TestClass.method ✅ | TC-001 ⏳ | Partial |

### Step 8: Write Test Scripts File

Save results to: `.specify/specs/NNN-feature-name/task_story_NN_test_scripts.md`

### Step 9: Update Story File

- **Technical Tests**: X/Y passed
- **Persona Coverage**: X/Y confirmed
- **State** to `QA` (passed technical QA, ready for UAT)

## Next Step

Technical QA PASSED. Run `/speckit.sf.uat` to begin the business sign-off process.

## Output

- **Content**: Manual test scripts, automated results, traceability matrix
- **Story file updated**: Status → QA, QA results section populated

## Notes

- Manual test scripts require QA to EXECUTE them in the org and record Pass/Fail
- If automated tests fail, story should be returned to developer before manual testing
