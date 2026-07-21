---
description: "Impact analysis for mid-sprint requirement changes."
---

# Handle Mid-Sprint Requirement Changes

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Feature spec, plan, and story files exist
- At least some stories are in READY or IMPLEMENTING state

## Instructions

### Step 1: Read Current State

1. Read the current spec: `.specify/specs/NNN-feature-name/spec.md`
2. Read the current plan: `.specify/specs/NNN-feature-name/plan.md`
3. Read ALL story files: `.specify/specs/NNN-feature-name/task_story_*.md`
4. Track each story's current status (DRAFT, READY, IMPLEMENTING, REVIEW, QA, DONE)

### Step 2: Analyze Impact

Evaluate the change request against each artifact:

**Spec impact**: Does this change add new user stories, modify existing acceptance criteria, or change the object map?

**Plan impact**: Does this change require new objects/fields, new Apex classes, new LWC components, or change the deployment order?

**Story impact**: For each existing story:
- Does this change add new requirements to an existing story?
- Does this change invalidate work already completed?
- Does this change create new dependencies?

**Destructive Impact**: Does this change obsolete any existing fields, objects, or classes? If yes, prepare to generate a `destructiveChanges.xml` containing these components.

### Step 3: Generate Impact Report

```markdown

## Change Impact Report

### Change Request
"$CHANGE_DESCRIPTION"

### Impact Summary
| Area | Impact Level | Details |
|------|-------------|---------|
| Spec | [None/Minor/Major] | [What changes in spec] |
| Plan | [None/Minor/Major] | [What changes in plan] |
| Data Model | [None/Minor/Major] | [New objects/fields needed] |
| Story-000 | [None/Minor/Major] | [Foundation changes needed] |

### Stories Affected

| Story | Status | Impact | Action Required |
|-------|--------|--------|----------------|
| task_story_00.md | DONE | 🔴 Major | Add CurrencyIsoCode field to Invoice__c, update PermSet |
| task_story_01.md | IMPLEMENTING | 🟡 Minor | Add currency picker to LWC form |
| task_story_02.md | READY | ⚪ None | No changes needed |
| task_story_03.md | READY | ⚪ None | No changes needed |

### New Stories Needed
- task_story_04.md — Currency Conversion Service (new Apex batch class)

### Destructive Changes Review
*(If applicable, list components slated for deletion. TPO MUST manually sign off.)*
| Component Type | Component Name | Action | TPO Approval Required |
|----------------|----------------|--------|-----------------------|
| CustomField | Invoice__c.OldCurrency__c | DELETE | [ ] Pending Sign-off |
> **WARNING**: Deletions will be executed during deployment. Ensure `destructiveChanges.xml` is generated and accurate before approving.

### Risk Assessment
- **Already-completed work**: Story-000 Foundation needs re-deployment (schema change)
- **In-progress work**: Story-01 developer needs to update LWC (minor rework)
- **Estimation impact**: +X hours / +Y story points

### Recommended Actions
1. [ ] Update spec.md with multi-currency requirements
2. [ ] Update plan.md with new data model fields
3. [ ] Update task_story_00.md to add CurrencyIsoCode field
4. [ ] Update task_story_01.md to add currency picker UI
5. [ ] Create task_story_04.md for currency conversion service
6. [ ] Re-deploy Story-000 to Dev Sandbox with schema change
7. [ ] Update Jira tickets: modify PROJ-100, PROJ-101; create PROJ-104
```

### Step 4: Present to TPO

Show the impact report. Ask:
- "Do you want to proceed with these changes?"
- "Should I update the affected files now?"

### Step 5: Apply Changes (if approved)

If the TPO approves:
1. Update spec.md with change log entry
2. Update plan.md if data model or architecture changes
3. Update affected story files
4. Create new story files
5. Update dependency graph
6. If destructive changes are approved, generate `destructiveChanges.xml` in the `force-app/main/default` directory.

### Step 6: Add Change Log Entry

Add to spec.md's Change Log:

```markdown
| $DATE | $TPO | Change: "$CHANGE_DESCRIPTION" — Stories affected: 00, 01; New story: 04 |
```

## Error Handling

- **Prerequisite Missing**: STOP and inform the user of the missing context.

## Notes

- Changes to DONE stories are the most expensive (require redeployment)
- Changes to DRAFT/READY stories are cheap (just file updates)
- Changes to IMPLEMENTING stories require developer communication
- Always update the spec first — it's the source of truth
