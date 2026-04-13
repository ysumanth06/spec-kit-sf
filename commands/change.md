---
description: "Handle mid-sprint requirement changes with impact analysis."
---

# Mid-Sprint Change Management

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Active feature exists: `.specify/specs/NNN-feature-name/`
- At least one story file exists: `.specify/specs/NNN-feature-name/task_story_*.md`
- Spec and plan exist in the feature directory

## Instructions

### Step 1: Read Current State

1. Read all files in the feature directory:
   - `spec.md` — current specification
   - `plan.md` — current technical plan
   - All `task_story_*.md` — current stories with their statuses
2. Read the constitution from `.specify/memory/constitution.md`
3. Note which stories are: DRAFT, READY, IMPLEMENTING, IMPLEMENTED, DONE

### Step 2: Understand the Change Request

Ask the user to describe the change. Collect:
- **What changed**: New requirement, modified requirement, or removed requirement
- **Why it changed**: Business priority shift, regulatory, user feedback, technical discovery
- **Urgency**: Must-have this sprint or can defer?

### Step 3: Generate Impact Report

Analyze the change against every existing story:

```markdown
## Change Impact Report

### Change Request
[Description of the change]

### Impact Analysis

| Story | Status | Impact | Action Required |
|-------|--------|--------|----------------|
| task_story_00 | DONE | ⚠️ New field needed | Add field to Foundation story |
| task_story_01 | IMPLEMENTING | 🔴 Major rework | Modify logic, update tests |
| task_story_02 | READY | ✅ No impact | None |
| task_story_03 | DRAFT | ⚠️ New AC needed | Add acceptance criterion |

### New Stories Required
- task_story_05.md — [New requirement description]

### Effort Delta
- Original estimate: X hours
- Revised estimate: Y hours
- Delta: +Z hours

### Risk Assessment
- Stories already IMPLEMENTING that need rework: [list]
- Deployment order changes: [yes/no]
- New dependencies introduced: [yes/no]
```

### Step 4: Present Options

Present the TPO with options:

**Option A: Full Integration**
- Modify affected stories in-place
- Update spec and plan
- Re-run `/speckit.sf.review`

**Option B: New Story Only**
- Create a new story (task_story_NN.md) for the change
- Minimal disruption to in-progress work
- May require coordination with existing stories

**Option C: Defer**
- Log the change request but don't act on it
- Create a follow-up spec for next sprint/release

### Step 5: Execute Chosen Option

Based on the TPO's choice:
- Update the spec with the change
- Update the plan if architecture is affected
- Create or modify story files
- Update dependency graph

### Step 6: Update Affected Artifacts

- Update `spec.md` with change log entry
- Update `plan.md` if architecture changed
- Update affected `task_story_*.md` files
- Add change tracking entry to each modified file

## Output

- **Impact Report**: Analysis of how the change affects every story
- **Updated Files**: Spec, plan, and/or stories modified based on chosen option
- **New Stories**: Any new task_story files created for the change
