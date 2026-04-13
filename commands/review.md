---
description: "TPO and Architect review of generated stories before Jira creation."
---

# Story Review Gate

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Story files exist: `.specify/specs/NNN-feature-name/task_story_*.md`
- Plan exists: `.specify/specs/NNN-feature-name/plan.md`

## Instructions

### Step 1: Read All Story Files

1. Read all `task_story_*.md` files in the feature directory
2. Read the plan for deployment order and scoring gates
3. Read the spec for completeness validation

### Step 2: Build and Validate Dependency Graph

1. Parse each story's Dependencies section
2. Build a dependency graph
3. Check for:
   - ❌ **Circular dependencies**: Story A requires Story B which requires Story A
   - ❌ **Missing dependencies**: Story references an artifact not created by any story
   - ❌ **Orphan stories**: Stories with no connection to the dependency chain
   - ✅ **Foundation story exists**: task_story_00.md is present and blocks all others

### Step 3: Validate Deployment Order Within Stories

For each story, verify:
- Metadata layers come before Apex layers
- Apex layers come before Flow layers (if Flow calls `@InvocableMethod`)
- Apex layers come before LWC layers (if LWC calls `@AuraEnabled`)
- All layers respect Constitution Article IX (Cross-Skill Orchestration)

### Step 4: Identify Merge Conflict Risks

Check for files that appear in MULTIPLE stories:
- ⚠️ Same trigger file modified by multiple stories → consolidate in Story-000
- ⚠️ Same Permission Set modified by multiple stories → suggest one Permission Set per feature
- ⚠️ Same utility class modified by multiple stories → move shared code to Story-000

### Step 5: Validate Story Completeness

For each story, check all required sections are populated:
- [ ] Requirements section is non-empty
- [ ] Acceptance criteria has at least 2 Given/When/Then scenarios
- [ ] Test cases has at least 1 Positive, 1 Negative, 1 Bulk test
- [ ] Dependencies are declared (REQUIRES and/or INDEPENDENT OF)
- [ ] SF Implementation Layers table has at least 1 row
- [ ] File paths use `force-app/main/default/` prefix
- [ ] Scoring gates match plan thresholds
- [ ] Estimation is present

### Step 6: Architect Validation Checklist

**Architect Review:**
- [ ] Dependency graph is correct (no circular deps, no missing refs)
- [ ] Deployment order within each story is safe
- [ ] No unresolved merge conflict risks
- [ ] Story boundaries are clean (no cross-story coupling beyond declared deps)
- [ ] Estimations are reasonable for the complexity
- [ ] Naming conventions are consistent across stories
- [ ] Shared infrastructure is properly consolidated in Story-000
- [ ] Security patterns (with sharing, user mode) are consistent

### Step 7: TPO Validation Checklist

**TPO Review:**
- [ ] All acceptance criteria from the spec are covered across stories
- [ ] Stories are independently testable
- [ ] Priority ordering matches business value (P1 stories first)
- [ ] Estimation total aligns with sprint capacity
- [ ] No scope creep (stories don't exceed spec boundaries)

### Step 8: Generate Review Report

```markdown
## Story Review Summary
- Total stories: X (including Story-000 Foundation)
- Parallel stories: Y (can be assigned simultaneously)
- Sequential stories: Z (have blocking dependencies)
- Total estimated effort: X hours / Y story points
- Merge conflict risks: [list or "none identified"]
- Deployment order issues: [list or "none identified"]

## Recommended Sprint Allocation
- Sprint 1: Story-000 + [parallel stories]
- Sprint 2: [sequential stories that depend on Sprint 1]
```

### Step 9: Finalize

Once both TPO and Architect provide approvals:
- Mark all story files' Status as **READY** (was DRAFT)
- Inform: "Stories are approved. Create Jira tickets from these story files and assign to developers."

## Next Step

Developers will use `/speckit.sf.implement <story_file>` to build their assigned story.

## Output

- **Files updated**: All `task_story_*.md` files → Status changed from DRAFT to READY
- **Review artifacts**: Dependency graph, risk assessment, sprint allocation recommendation
