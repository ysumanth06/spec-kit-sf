---
description: "Create a Salesforce feature spec with object maps and security model."
---

# Create Salesforce Feature Specification

## User Input

$ARGUMENTS

## Skill Discovery

Before executing, search the project for any installed agent skills related to:

- **Salesforce documentation** — official docs, feature references
- **Diagramming** — ERD, object relationship visualization

Search locations: `.agents/skills/`, `.specify/extensions/`, `.claude/commands/`
If found, load and apply their best practices. If not found, use built-in knowledge.

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Constitution exists: `.specify/memory/constitution.md` (run `/speckit.sf.constitution` first)
- Git repository initialized
- `sfdx-project.json` exists in project root

## Instructions

### Step 1: Read Context

1. Read the constitution from `.specify/memory/constitution.md`
2. Read `sfdx-project.json` to extract:
   - `sourceApiVersion` → API version
   - `packageDirectories[0].path` → source path
   - `name` → project name
3. Scan `force-app/main/default/objects/` to understand existing custom objects
4. Scan `.specify/specs/` to determine next feature number

### Step 2: Create Feature Branch & Directory

1. Determine next feature number (scan existing dirs in `.specify/specs/`)
2. Create slug from feature description (lowercase, hyphens)
3. Create directory: `.specify/specs/NNN-feature-slug/`
4. Create git branch: `feature/NNN-feature-slug`
   - If branch creation fails (not on main, uncommitted changes), warn but continue

### Step 3: Read Template

Read `.specify/templates/spec-template.md` if it exists — this is the structure to follow.

### Step 4: Gather Requirements

Have a conversation with the user to understand the feature. Focus on:

1. **User stories**: Who uses this feature? What do they need to accomplish? Break into P1/P2/P3 priorities.
2. **Acceptance scenarios**: For each user story, define Given/When/Then scenarios.
3. **Salesforce Platform Context**: Target org type, clouds, editions, packages.
4. **Automation Approach**: For each behavior, determine if Flow or Apex is appropriate (reference Article III).
5. **Object Map**: What standard/custom objects are involved? Relationships?
6. **Data Volume**: Expected record counts, bulk scenarios.
7. **Security Model**: OWD settings, FLS approach, sharing rules.

### Step 5: Generate the Specification

Create `.specify/specs/NNN-feature-slug/spec.md` by:

1. Populating the spec template with gathered requirements
2. Auto-filling:
   - `$FEATURE_NAME` = feature description
   - `$FEATURE_NUMBER` = next number (e.g., 001)
   - `$FEATURE_SLUG` = slugified description
   - `$API_VERSION` = from sfdx-project.json
   - `$DATE` = today
3. Writing user stories in P1→P2→P3 priority order
4. Marking any unclear items with `[NEEDS CLARIFICATION: specific question]`
5. Populating the Automation Approach Decision table
6. Listing functional and non-functional requirements

### Step 6: Identify Clarification Needs

Review the generated spec for:
- Any assumptions made (document in Assumptions section)
- Any ambiguous requirements (mark with `[NEEDS CLARIFICATION]`)
- Any missing information (add to Clarification Status table)

### Step 7: Present to User

Show the generated spec to the user. Highlight:
- Number of user stories created
- Any items marked `[NEEDS CLARIFICATION]`
- Automation approach decisions made

## Next Step

- **Requirement Audit**: Run `/speckit.sf.clarify` to execute the gap analysis and ensure the specification is complete.
- **Technical Design**: Once the spec is clarified, run `/speckit.sf.plan` to create the technical implementation plan.

## Output

- **Directory created**: `.specify/specs/NNN-feature-slug/`
- **File created**: `.specify/specs/NNN-feature-slug/spec.md`
- **Branch created**: `feature/NNN-feature-slug`
- **Status**: Draft (with clarification markers if applicable)
