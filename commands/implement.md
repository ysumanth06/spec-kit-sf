---
description: "Implement a story file with auto-heal loop and scoring gates."
---

# Implement a Developer Story

## User Input

$ARGUMENTS

# Implement a Developer Story

## User Input

$ARGUMENTS

## Prerequisites

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Story file exists and status is **READY** (approved by `/speckit.sf.review`)
- Constitution exists: `.specify/memory/constitution.md`
- Plan exists in the same feature directory
- Dependencies are met (Story-000 must be DONE for non-foundation stories)
- Developer has authenticated to Dev Sandbox: `sf org login web --alias dev`
- Salesforce Code Analyzer plugin installed: `sf plugins install @salesforce/sfdx-scanner`

## Instructions

### Step 1: Read All Context

1. Read the story file provided as input
2. Read the constitution from `.specify/memory/constitution.md`
3. Read the plan from the same feature directory (`plan.md`)
4. Read the data model (`data-model.md`) for object/field definitions
5. Read `sfdx-project.json` for API version

### Step 2: Validate Prerequisites

1. **Story status**: Must be READY (not DRAFT or already IMPLEMENTING)
2. **Dependencies**: Check each REQUIRES dependency — verify its status is DONE or IMPLEMENTING
3. **Constitution**: Verify constitution.md exists
4. **Environment**: Confirm target org is Dev Sandbox (`--target-org dev`)

### Step 3: Update Story Status

Update the story file:
- Set **State** to `IMPLEMENTING`
- Set **Started** to today's date

### Step 4: Create Story Branch

Create the story branch from the feature branch. If the feature branch exists and Story-000 has been merged, branch from the updated feature branch.

### Step 5: Check Code Analyzer

1. Verify if `sf scanner run` is available.
2. If NOT available:
   - Prompt: "Salesforce Code Analyzer is not installed. Would you like to install it now?"
   - **WARNING: Proceeding without the Code Analyzer is a SECURITY RISK.**

### Step 6: Implement Layers in Deployment Order

Read the **SF Implementation Layers** table from the story file. Execute each layer in order:

#### Phase 1: Metadata (if applicable)
- Create/modify custom objects, fields, validation rules, permission sets
- Mark `[ ]` → `[x]` in the story's layer table
- **Scoring gate**: Must meet metadata minimum threshold

#### Phase 2: Apex (if applicable)
- Create classes in order: Selector → Service → TriggerAction → Controller
- Follow Separation of Concerns (Article VI)
- Create test classes following PNB pattern (Article V)
- Mark `[ ]` → `[x]` in the story's layer table
- **Scoring gate**: Must meet Apex minimum threshold
- **Scanner gate**: Run `sf scanner run --target "force-app/main/default/classes/*.cls" --engine pmd`
  - Requirement: **Zero Severity 1 (Critical)** violations.

#### Phase 3: Flow (if applicable)
- Create flow definition files
- Deploy as Draft first, then activate after validation
- Mark `[ ]` → `[x]` in the story's layer table

#### Phase 4: LWC (if applicable)
- Follow component architecture best practices (PICKLES if available)
- Create component files: .html, .js, .css, .js-meta.xml
- Create Jest test files in `__tests__/` directory
- Ensure SLDS 2 compliance, keyboard accessibility
- Mark `[ ]` → `[x]` in the story's layer table
- **Scanner gate**: Run `sf scanner run --target "force-app/main/default/lwc/" --engine eslint-lwc`

### Step 7: Run Full Story Tests

After all layers are implemented:

1. Run Apex tests:
   ```bash
   sf apex run test --class-names [TestClass1,TestClass2] --code-coverage --result-format json --target-org dev
   ```
2. Run Jest tests (if LWC present):
   ```bash
   npx lwc-jest -- --testPathPattern [componentName]
   ```
3. Verify coverage meets story's scoring gates
4. Update the story's **Scoring Gates** section with actual scores

### Step 8: Scoring Gate Validation & Auto-Heal

Compare actual scores with the story's required thresholds:

1. **Initial Check**: If ALL gates pass → proceed. If any gate FAILS → Enter **Auto-Heal Mode**.
2. **Auto-Heal Loop (Agentic)**:
   - **Analyze**: Review the score report. Identify specific checklist failures by following the rubric in `docs/scoring.md`.
   - **Refactor**: Automatically modify the code to address issues.
   - **Re-score**: Rerun evaluation against the `docs/scoring.md` checklist.
   - **Retry Limit**: Up to **3 times** per layer.
3. **Final Validation**: If score achieved within 3 retries → proceed. Otherwise STOP and report blockers.

### Step 9: Update Story File

- Mark all implementation layer checkboxes as `[x]`
- Update **Scoring Gates** with actual scores
- Set **State** to `IMPLEMENTED`
- Set **Completed** to today's date

### Step 10: Summary

Inform the developer:
- Layers completed: X/Y
- All scoring gates: PASS/FAIL
- Files created: [list]

## Next Step

Run `/speckit.sf.verify` to generate your Verification Evidence document before creating the PR.

## Output

- **Files created**: All force-app/ files listed in the story's implementation layers
- **Story file updated**: Status → IMPLEMENTED, all layers marked complete, scores recorded

## Error Handling

- **Dependency not met**: Stop with clear message about which story needs to complete first
- **Scoring gate failure**: Stop, report score gap, suggest fixes, allow re-run
- **Git branch conflict**: Warn and suggest resolving before continuing
- **Compilation error**: Report error, suggest fix, allow retry
