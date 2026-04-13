---
description: "Run the Salesforce gap analysis checklist against the specification."
---

# Fill Specification Gaps

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Specification exists in `.specify/specs/NNN-feature-name/spec.md`
- Constitution exists in `.specify/memory/constitution.md`

## Instructions

### Step 1: Read Current State

1. Read the feature spec from `.specify/specs/NNN-feature-name/spec.md`
2. Identify all `[NEEDS CLARIFICATION]` markers.
3. **Ask the TPO**: "Would you like to run in **Draft Mode** (generate report for business) or **Interactive Mode** (answer now and sync to spec immediately)?"

### Step 1.5: Environment Drift Audit (CLI-Driven)

**CRITICAL for Multi-Org Teams.** Before analyzing logic, verify the physical environment matches the spec baseline.

1. **Run Metadata Inventory**:
   ```bash
   sf metadata list -m CustomObject --target-org [org]
   sf object list --target-org [org]
   ```
2. **Run Deployment Preview**:
   ```bash
   sf project deploy preview --target-org [org]
   ```
3. **Analyze Results**:
   - **Manual Changes**: Identify components in the org that are NOT in source control (Local vs. Remote drift).
   - **Conflict Risk**: Identify if Team B has modified objects referenced in your `spec.md`.
   - **Base Assumption Failure**: Does the object map in the spec accurately reflect the actual org schema?

Record every deviation in the **Org Consistency** section of the report.

### Step 2: Perform Deep Gap Analysis

Act as a Business Analyst and Architect to identify gaps beyond the standard checklist. Analyze the spec for:
- **The "Unhappy Path"**: Missing error states or recovery logic.
- **Ambiguous Rules**: Non-specific logic like "standard discount" or "priority handling."
- **Boundary Cases**: What happens at the minimum/maximum values?
- **User Experience**: Ambiguities in desktop vs. mobile or guest vs. authenticated behavior.
- **Agentforce Readiness**: Gaps in data exposure for AI agents.

Generate as many specific questions as needed to cover every identified edge case.

### Step 3: Generate Clarification Report

Create a formal sign-off document:
- **Location**: `.specify/specs/[feature-dir]/clarification-report-[feature-name].md`
- **Content**:
    - **Section 1: Org Consistency & Drift**: Results from the Step 1.5 CLI Audit.
    - **Section 2: Technical Foundation**: The 10-point Salesforce checklist.
    - **Section 3: Deep Business Analysis**: All dynamic questions identified in Step 2.
    - **Section 4: Stakeholder Sign-off Table**: Fields for TPO and BPO approval.

For each question, provide:
- **Context**: Why this was flagged in the spec.
- **The Question**: Clear, non-technical language for the business.
- **Proposed Options**: Option A, Option B, etc., with pros/cons for each.
- **Architectural Impact**: How the decision affects the complexity/cost of the build.

### Step 4: Summary and Execution Guidance

Inform the TPO of the results. The guidance depends on the mode chosen in Step 1:

**If Draft Mode**:
- "Clarification report generated."
- "Next: Review with stakeholders (especially the **Drift Alert** section), record decisions, and re-run this command in **Interactive Mode** to sync."

**If Interactive Mode**:
- "Decisions gathered and recorded in the report."
- "Proceed to Step 5 (Update Specification) immediately."

### Step 5: Update the Specification

**Execute this if in Interactive Mode OR if the TPO confirms sign-off for a previous Draft.**

For each resolved question in the report:
1. Update relevant spec section (Platform Context, Security Model, Object Map, etc.).
2. Remove corresponding `[NEEDS CLARIFICATION]` markers.
3. Update the Clarification Status table in the spec.

## Next Step

Run `/speckit.sf.plan` to create the technical implementation plan.

## Output

- **Clarification Report Created**: `.specify/specs/NNN-feature-name/clarification-report-[feature-name].md`
- **Spec Updated (Optional)**: `.specify/specs/NNN-feature-name/spec.md` (only after TPO sign-off)

## Note on Drift

If drift is significant (e.g., destructive changes found), STOP and resolve source control conflicts before proceeding to `/speckit.sf.plan`.
