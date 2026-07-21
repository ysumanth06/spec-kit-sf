---
description: "Implement a story file with auto-heal loop and scoring gates."
---

# Implement a Developer Story

## User Input

$ARGUMENTS

## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Foundational Salesforce Layers** (`sf-apex`, `sf-lwc`, `sf-metadata`, `sf-flow`)
- **Utility Skills** (`sf-docs`, `sf-debug`, `sf-data`, `sf-integration`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist implementation and scoring. However, the standards in `docs/scoring.md` are the **primary source of truth**.

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Story file exists and status is **READY** (approved by /speckit.sf.review)
- Constitution exists: `.specify/memory/constitution.md`
- Plan exists in the same feature directory
- Dependencies are met (Story-000 must be DONE for non-foundation stories)
- Developer has authenticated to Dev Sandbox: `sf org login web --alias dev`
- Salesforce Code Analyzer (v5) installed: `sf plugins install code-analyzer`

## Instructions

### Step 1: Read All Context

1. Read the story file provided as input
2. Read the constitution from `.specify/memory/constitution.md`
3. Read the plan from the same feature directory (`plan.md`)
4. Read the data model (`data-model.md`) for object/field definitions
5. Read `sfdx-project.json` for API version

### Step 2: Validate Prerequisites

Check the following before starting:

1. **Story status**: Must be READY (not DRAFT or already IMPLEMENTING)
2. **Dependencies**: Check each REQUIRES dependency:
   - Read the required story file
   - Verify its status is DONE or IMPLEMENTING
   - If not met → STOP and inform: "Dependency task_story_00.md is not yet complete"
3. **Constitution**: Verify constitution.md exists
4. **Environment**: Confirm target org is Dev Sandbox (`--target-org dev`)

### Step 3: Update Story Status

Update the story file:
- Set **State** to `IMPLEMENTING`
- Set **Started** to today's date

### Step 4: Create Story Branch

Ensure branch naming consistency. The standard format is:
- Feature Branch: `feature/<feature-id>-<slug>`
- Story Branch: `story/<feature-id>-<story-id>-<slug>`

```bash
git checkout feature/$FEATURE_NUMBER-$FEATURE_SLUG
git pull origin feature/$FEATURE_NUMBER-$FEATURE_SLUG
git checkout -b story/$FEATURE_NUMBER-$STORY_NUMBER-$STORY_SLUG
```

If the feature branch exists and Story-000 has been merged, always branch from the updated feature branch.

### Step 5: Check Code Analyzer

1. Verify if `sf code-analyzer run` is available.
2. If NOT available:
   - Prompt: "Salesforce Code Analyzer (v5) is not installed. Would you like to install it now? (`sf plugins install code-analyzer`)"
   - If user declines:
     - **WARNING: Proceeding without the Code Analyzer is a SECURITY RISK. Vulnerabilities like SOQL Injection or CRUD/FLS holes may not be caught before deployment. This could cause significant problems during PR review or in Production.**
     - Ask: "Are you sure you want to proceed without static analysis? (y/n)"
   - If user agrees to install: Install and rerun this command.

### Step 6: Implement Layers in Deployment Order

Read the **SF Implementation Layers** table from the story file. Execute each layer in order:

#### Phase 1: Metadata (if applicable)
- Consult the **Metadata Best Practices Checklist** in `docs/scoring.md`
- Create/modify custom objects, fields, validation rules, permission sets
- File paths from the story's implementation layers table
- Check: mark `[ ]` → `[x]` in the story's layer table
- **Scoring gate**: Run sf-metadata scoring → must meet 84/120 minimum

#### Phase 2: Apex (if applicable)
- Consult the **Apex Best Practices Checklist** in `docs/scoring.md`
- Create classes in order: Selector → Service → TriggerAction → Controller
- Follow Separation of Concerns (Article VI):
  - Selector: All SOQL queries, `WITH USER_MODE`
  - Service: Business logic, no SOQL/DML directly
  - TriggerAction: TAF handler, dispatched from trigger
  - Controller: `@AuraEnabled` methods only, delegates to Service
- Create test classes following PNB pattern (Article V):
  - Positive tests: Valid inputs → success
  - Negative tests: Invalid inputs → proper error handling
  - Bulk tests: 251+ records → no governor limit exceptions
  - Use TestDataFactory (from Story-000)
- Check: mark `[ ]` → `[x]` in the story's layer table
- **Scoring gate**: Run sf-apex scoring → must meet 90/150 minimum
- **Scanner gate**: Run `sf code-analyzer run --path "force-app/main/default/classes/*.cls" --engine pmd`
  - Requirement: **Zero Severity 1 (Critical)** violations.
  - Fix any violations before proceeding to Phase 3.

#### Phase 3: Flow (if applicable)
- Consult the **Flow Best Practices Checklist** in `docs/scoring.md`
- Create flow definition files
- Deploy as Draft first, then activate after validation
- Check: mark `[ ]` → `[x]` in the story's layer table
- **Scoring gate**: Run sf-flow scoring → must meet minimum

#### Phase 4: LWC (if applicable)
- Consult the **LWC Best Practices Checklist** in `docs/scoring.md`
- Follow PICKLES methodology
- Create component files: .html, .js, .css, .js-meta.xml
- Create Jest test files in `__tests__/` directory
- Ensure SLDS 2 compliance, keyboard accessibility
- Check: mark `[ ]` → `[x]` in the story's layer table
- **Scoring gate**: Run sf-lwc scoring → must meet 125/165 minimum
- **Scanner gate**: Run `sf code-analyzer run --path "force-app/main/default/lwc/" --engine eslint`
  - Requirement: **Zero Severity 1 (Critical)** violations.
  - Fix any violations before proceeding to Step 6.

### Step 6: Run Full Story Tests

After all layers are implemented:

1. Consult the **Testing Best Practices Checklist** in `docs/scoring.md`
2. Run Apex tests for this story's classes:
   ```bash
   sf apex run test --class-names [TestClass1,TestClass2] --code-coverage --result-format json --target-org dev
   ```
3. Run Jest tests (if LWC present):
   ```bash
   npx lwc-jest -- --testPathPattern [componentName]
   ```
4. Verify coverage meets story's scoring gates
5. Update the story's **Scoring Gates** section with actual scores

### Step 7: Scoring Gate Validation & Auto-Heal

Compare actual scores with the story's required thresholds:

1. **Initial Check**:
   - If ALL gates pass → proceed to Step 8.
   - If any gate FAILS → Enter **Auto-Heal Mode**.

2. **Auto-Heal Loop (Agentic Logic)**:
   - **Analyze**: Review the score report from the failed `sf-*` skill. Identify the specific points deducted (e.g., "Missing CRUD/FLS check" or "Hardcoded ID").
   - **Refactor**: Automatically modify the code to address the identified issues.
   - **Re-score**: Rerun the scoring skill for that layer.
   - **Retry Limit**: Attempt this loop up to **3 times** per layer.
   - **API Limit Kill Switch**: After each retry, check the `LimitInfoHeader` or equivalent limits output. If `API Requests` or `CPU Time` exceeds 80% of the org limit, or shows a sudden massive spike, **IMMEDIATELY ABORT** the auto-heal loop to prevent sandbox lockout.

3. **Final Validation**:
   - If score is achieved within 3 retries (and limits are safe) → proceed to Step 8.
   - If all 3 retries fail, or the kill switch is triggered → STOP and inform the developer of the specific blockers, current score vs. threshold, and current API limit status.

### Step 8: Deploy to Salesforce Target Org

**CRITICAL GUARDRAIL**: You MUST deploy the code to the target Salesforce org *before* making any Git commits.

```bash
sf project deploy start --target-org dev
```

If the deployment fails, **STOP**. Resolve the deployment errors in the code before proceeding. Do NOT commit failing code to the repository.

### Step 9: Git Commit and Push

Only AFTER a successful Salesforce deployment, commit the changes to your story branch:

```bash
git add .
git commit -m "feat: implement $STORY_TITLE"
git push origin story/$FEATURE_NUMBER-$STORY_NUMBER-$STORY_SLUG
```

### Step 10: Update Story File

Update the story file:
- Mark all implementation layer checkboxes as `[x]`
- Update **Scoring Gates** with actual scores
- Set **State** to `IMPLEMENTED`
- Set **Completed** to today's date (implementation date, not QA date)

### Step 11: Summary

Inform the developer:
- Layers completed: X/Y
- All scoring gates: PASS/FAIL
- Files created: [list]
- Suggest: "Implementation complete. Run `/speckit.sf.verify` to generate your Verification Evidence document before creating the PR."

## Error Handling

- **Prerequisite Missing**: STOP and inform the user of the missing context.

- **Dependency not met**: Stop with clear message about which story needs to complete first
- **Scoring gate failure**: Stop, report score gap, suggest fixes, allow re-run
- **Git branch conflict**: Warn and suggest resolving before continuing
- **Compilation error**: Report error, suggest fix, allow retry

## Next Step

Run `/speckit.sf.verify` to generate your Verification Evidence document before creating the PR.
