---
description: "Generate Jira-ready developer stories with security matrices."
---

# Generate Developer Story Files

## User Input

$ARGUMENTS

## Skill Discovery

Before executing, search the project for any installed agent skills related to:

- **Metadata/Objects** — field types, relationships, permission sets
- **Apex development** — Separation of Concerns, TAF patterns
- **Testing** — PNB patterns, test data factories

Search locations: `.agents/skills/`, `.specify/extensions/`, `.claude/commands/`
If found, load and apply their best practices. If not found, use built-in knowledge.

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

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

### Step 2: Validate Architect Sign-Off

Check plan.md for the Architect Sign-Off section:
- If "Overall Sign-Off: [x] APPROVED" → proceed
- If not approved → warn: "⚠️ Architect has not signed off on this plan. Story generation may need revision after sign-off."
- Ask user whether to proceed or wait

### Step 3: Generate Story-000 (Foundation Story)

**ALWAYS generate this story first.** It contains shared infrastructure that blocks all other stories.

Create `.specify/specs/NNN-feature-name/task_story_00.md` containing:

- **Type**: FULL
- **What it covers**:
  - All Custom Objects and Custom Fields referenced by ANY user story
  - Permission Sets with FLS for all new fields
  - Trigger files (one per object, with TAF MetadataTriggerHandler dispatch)
  - Test Data Factory class(es)
  - Custom Metadata for Trigger Action configuration
  - Base utility/selector classes shared across stories
- **Dependencies**: NONE (this is the root)
- **Blocks**: ALL other stories (task_story_01..NN)

### Step 4: Decompose User Stories into Developer Stories

For each user story in the spec (US-1, US-2, US-3...):

1. **Jira-Ready Description**: Format as "As a [Persona], I want to [Action] so that [Business Benefit]".
2. **Determine story type**: `FULL` (has Apex/Flow/LWC) or `DECLARATIVE` (metadata-only)
3. **Security & Access Matrix**: Which Permission Sets/Profiles require access to which objects/fields.
4. **Map to SF implementation layers**: Apex classes, Flows, LWC components, test classes with exact file paths.
5. **Detailed Acceptance Criteria**: At least 3-5 Given/When/Then scenarios from the spec.
6. **Generate test cases**: Positive, Negative, and Bulk (251+ records).
7. **Determine dependencies**: Every story REQUIRES task_story_00.md.
8. **Estimate effort**: Hours for Human Developer Effort per layer.

### Step 5: Create Story Files

For each story (01, 02, 03, ...):

Create `.specify/specs/NNN-feature-name/task_story_NN.md`:

1. Set **Status** to DRAFT
2. Set **Story Type** to FULL or DECLARATIVE
3. Populate **SF Implementation Layers** table with exact file paths
4. Populate **Security & Access Matrix** with detailed profile/permset configs
5. Populate **Dependencies** based on Step 4 analysis
6. Populate **Scoring Gates** with thresholds from the plan
7. Populate **Estimation** table (Human Effort in hours)
8. Add TPO/Architect guidance in **Developer Notes**

### Step 6: Build Dependency Graph

Create a summary showing the story dependency structure:

```
task_story_00.md (Foundation) ⛔ BLOCKS ALL
├── task_story_01.md (US-1: ...) [P]
├── task_story_02.md (US-2: ...) [P]
│   └── task_story_04.md (US-4: ...) — depends on 02
└── task_story_03.md (US-3: ...) [P]

[P] = Can work in parallel after Story-000 completes
```

### Step 7: Present to User

Show the user:
- Number of stories generated (including Story-000)
- Dependency graph
- Which stories can be worked in parallel
- Total estimated effort (Human Hours)
- Recommendation for sprint planning

## Next Step

Run `/speckit.sf.review` to have the Architect validate the story decomposition before creating Jira tickets.

## Output

- **Files created**: `task_story_00.md` through `task_story_NN.md`
- **Location**: `.specify/specs/NNN-feature-name/`
- **Status**: All stories in DRAFT state

## Notes

- Story-000 is ALWAYS generated and ALWAYS blocks other stories
- DECLARATIVE stories skip Apex/LWC layers and only include metadata scoring
- Mark parallel stories with `[P]` in the dependency graph
- **Estimations represent Human Developer Effort in hours.**
