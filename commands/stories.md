---
description: "Generate Jira-ready developer stories with security matrices."
---

# Generate Developer Story Files

## User Input

$ARGUMENTS

## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Metadata/Story Analysis** (`sf-metadata`, `sf-data`)
- **Developer Workload Estimation** (if specialized skills exist)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in decomposing features and identifying implementation layers. However, the standards in `docs/scoring.md` are the **primary source of truth**.

## Prerequisites

- Plan exists: `.specify/specs/NNN-feature-name/plan.md`
- Data model exists: `.specify/specs/NNN-feature-name/data-model.md`
- Spec exists: `.specify/specs/NNN-feature-name/spec.md`
- **Architect Sign-Off is completed** in plan.md (check the sign-off section)
  - If sign-off is incomplete, WARN the user and ask if they want to proceed anyway

## Instructions

### Step 1: Read All Context

1. Read the plan from `.specify/specs/NNN-feature-name/plan.md`
2. Read the data model from `.specify/specs/NNN-feature-name/data-model.md`
3. Read the spec from `.specify/specs/NNN-feature-name/spec.md`
4. Read the constitution from `.specify/memory/constitution.md`
5. Read the story template from `.specify/templates/story-template.md`

### Step 2: Validate Architect Sign-Off

Check plan.md for the Architect Sign-Off section:
- If "Overall Sign-Off: [x] APPROVED" → proceed
- If not approved → warn: "⚠️ Architect has not signed off on this plan. Story generation may need revision after sign-off."
- Ask user whether to proceed or wait

### Step 3: Generate Story-000 (Foundation Story)

**ALWAYS generate this story first.** It contains shared infrastructure that blocks all other stories.

Create `.specify/specs/NNN-feature-name/task_story_00.md` containing:

- **Type**: FULL
- **Requirements**: All custom objects, fields, validation rules from data-model.md
- **What it covers**:
  - All Custom Objects and Custom Fields referenced by ANY user story
  - Permission Sets with FLS for all new fields
  - Trigger files (one per object, with TAF MetadataTriggerHandler dispatch)
  - Test Data Factory class(es)
  - Custom Metadata for Trigger Action configuration
  - Base utility/selector classes shared across stories
- **Dependencies**: NONE (this is the root)
- **Blocks**: ALL other stories (task_story_01..NN)
- **Implementation Layers**: Metadata only (Objects, Fields, PermSets, Triggers, TestDataFactory)
- **Story Type**: FULL (even though mostly metadata, includes TestDataFactory Apex)

### Step 4: Decompose User Stories into Developer Stories

For each user story in the spec (US-1, US-2, US-3...):

1. **Jira-Ready Description**: Format the requirement as "As a [Persona], I want to [Action] so that [Business Benefit]".
2. **Determine story type**:
   - `FULL` — Has Apex, Flow, LWC, or multiple layers
   - `DECLARATIVE` — Metadata-only (picklist values, validation rules, config)
3. **Security & Access Matrix**: Identify exactly which Permission Sets and Profiles require access to which objects and fields. Detail Read/Edit access requirements.
4. **Map to SF implementation layers**:
   - Which Apex classes does this story need? (Service, Selector, Controller, TriggerAction)
   - Which Flows? (Record-Triggered, Screen, Autolaunched)
   - Which LWC components?
   - Which test classes?
5. **Determine exact file paths** using the plan's project structure
6. **Detailed Acceptance Criteria**: Extract at least 3-5 Given/When/Then scenarios from the spec.
7. **Generate test cases**:
   - **Positive**: Happy path scenarios from acceptance criteria
   - **Negative**: Error handling, validation failures, permission denials
   - **Bulk**: 251+ record scenarios for trigger/batch code
8. **Determine dependencies**:
   - Every story REQUIRES task_story_00.md (Foundation)
   - If Story-02's Apex calls Story-01's Service class → Story-02 REQUIRES Story-01
   - If stories are independent → mark as INDEPENDENT OF (can work in parallel)
9. **Estimate effort**: Estimate hours for **Human Developer Effort** per layer. Use story points as a secondary measure if requested.

### Step 5: Create Story Files

For each story (01, 02, 03, ...):

Create `.specify/specs/NNN-feature-name/task_story_NN.md` using the story template:

1. Replace all `$` placeholders with actual values
2. Set **Status** to DRAFT
3. Set **Story Type** to FULL or DECLARATIVE
4. Populate the **SF Implementation Layers** table with exact file paths
5. Populate the **Security & Access Matrix** with detailed profile/permset configs
6. Populate **Dependencies** based on Step 4 analysis
7. Populate **Scoring Gates** with thresholds from the plan
8. Populate **Estimation** table (clearly labeled as Human Effort)
9. Add TPO/Architect guidance in **Developer Notes**

### Step 6: Build Dependency Graph

Create a summary showing the story dependency structure:

```
task_story_00.md (Foundation) ⛔ BLOCKS ALL
├── task_story_01.md (US-1: Invoice UI) [P]
├── task_story_02.md (US-2: Invoice Logic) [P]  
│   └── task_story_04.md (US-4: Invoice Reports) — depends on 02
└── task_story_03.md (US-3: Dashboard) [P]

[P] = Can work in parallel after Story-000 completes
```

### Step 7: Present to User

Show the user:
- Number of stories generated (including Story-000)
- Dependency graph
- Which stories can be worked in parallel
- Total estimated effort (Human Hours)
- Recommendation for sprint planning (which stories fit in one sprint?)

Suggest: "Run `/speckit.sf.review` to have the Architect validate the story decomposition before creating Jira tickets."

## Error Handling

- **Prerequisite Missing**: STOP and inform the user of the missing context.

## Story File Format

Each story file follows `.specify/templates/story-template.md` and includes:
- Feature context (links to spec, plan, constitution)
- Detailed Description (As a/I want to/So that)
- Detailed Acceptance criteria (Given/When/Then)
- Security & Access Matrix (Profiles/Permission Sets)
- Test cases (Positive, Negative, Bulk)
- Dependencies (REQUIRES / INDEPENDENT OF)
- SF Implementation Layers table (Layer → Skill → File Path → Status)
- Scoring gates
- Estimation (Human Developer Effort per layer + total)
- Status section (state, assignee, Jira, branch)
- Code review checklist
- QA results section

## Notes

- Story-000 is ALWAYS generated and ALWAYS blocks other stories
- DECLARATIVE stories skip Apex/LWC layers and only include metadata scoring
- Mark parallel stories with `[P]` in the dependency graph
- Map each story to its originating user story with `[US-N]`
- **Estimations represent Human Developer Effort in hours.**

## Next Step

Run `/speckit.sf.review` to have the Architect validate the story decomposition before creating Jira tickets.
