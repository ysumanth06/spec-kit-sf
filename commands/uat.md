---
description: "Generate UAT scripts and manage business sign-offs."
---

# Business UAT Generation

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Story status is **QA** (technical verification passed via `/speckit.sf.qa`)
- Story code is deployed to UAT Sandbox (if applicable) or QA Sandbox
- Constitution exists: `.specify/memory/constitution.md`

## Instructions

### Step 1: Read Story Context

1. Read the story file provided as input
2. Read the feature spec (`spec.md`) in the same directory
3. Extract:
   - User Stories (As a... I want to... So that...)
   - Acceptance Criteria (Given/When/Then)
   - Feature Context (Process flow, constraints)

### Step 2: Generate Business Walkthrough

Generate a script that translates technical ACs into business steps.

**Guidelines for Business Language:**
- **NO technical jargon**: Avoid "Apex", "Trigger", "SOQL", "LWC", "DML".
- **Action-Oriented**: Use "Log in as...", "Navigate to...", "Click...", "Verify that...".
- **Business Outcomes**: Focus on what the user sees and achieves, not how it happens.

### Step 3: Create UAT Script File

Save the generated script to:
`.specify/specs/NNN-feature-name/uat_story_NN.md`

### Step 4: Present to BPO

Show the generated UAT script to the BPO. Highlight:
- The specific business process being tested
- The data needed for testing
- How to record Pass/Fail

### Step 5: Manage Sign-Off (Interactive)

If the BPO provides feedback or sign-off:
1. Update the `uat_story_NN.md` file with the BPO's name, date, and verdict.
2. If verdict is **PASS**:
   - Update the story file status to **READY FOR PROD** or **DONE**.
3. If verdict is **FAIL**:
   - Record the observation in the story file
   - Set story status back to **IMPLEMENTING** (for rework)

## Next Step

After UAT sign-off, run `/speckit.sf.deploy prod` to promote to production.

## Output

- **File created**: `.specify/specs/NNN-feature-name/uat_story_NN.md`
- **Story file updated**: Status updated based on sign-off (if provided)

## Error Handling

- **Story not ready**: If story status is not QA/REVIEW, warn that UAT might be premature.
- **Missing Spec**: If `spec.md` is missing, use story ACs only but warn about limited context.

## Notes

- This command focuses on **BUSINESS** validation. For technical QA, use `/speckit.sf.qa`.
- UAT should ideally be performed in a separate UAT Sandbox with production-like data.
