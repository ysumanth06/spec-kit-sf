---
description: "Create a technical plan with force-app structure and blast radius analysis."
---

# Create Technical Implementation Plan

## User Input

$ARGUMENTS

## Skill Discovery

Before executing, search the project for any installed agent skills related to:

- **Metadata/Objects** — field types, relationships, permissions, naming conventions
- **Apex development** — Separation of Concerns, layer patterns, bulkification
- **LWC development** — PICKLES methodology, component architecture
- **Flow development** — flow type selection, bulkification patterns
- **SOQL** — query optimization, relationship traversal
- **Permissions** — Permission Set architecture
- **Integration** — Named Credential patterns, External Services
- **Diagramming** — ERD and architecture diagram generation

Search locations: `.agents/skills/`, `.specify/extensions/`, `.claude/commands/`
If found, load and apply their best practices. If not found, use built-in knowledge.

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Spec exists: `.specify/specs/NNN-feature-name/spec.md` (status: Clarified or Draft)
- Constitution exists: `.specify/memory/constitution.md`
- `sfdx-project.json` exists

## Instructions

### Step 1: Read All Context

1. Read constitution from `.specify/memory/constitution.md`
2. Read spec from `.specify/specs/NNN-feature-name/spec.md`
3. Read `sfdx-project.json` for API version, package directories
4. Scan `force-app/main/default/` for existing objects, classes, LWC components
5. Check for existing data model patterns (naming conventions, trigger patterns)
6. Read user's tech stack guidance (if provided)

### Step 2: Run Constitution Check

Validate the spec against Constitution Articles I–IX:
- Article I: Are all objects/fields defined before code references?
- Article II: Are data volume estimates present?
- Article III: Is the automation approach decision table complete?
- Article IV: Is the security model defined?
- Article V: Is the PNB test pattern planned?
- Article VI: Are service/selector/domain layers identified?

If any checks fail, note them in the plan's "Constitution Check" section with specific remediation guidance.

### Step 3: Read Plan Template

Read `.specify/templates/plan-template.md` if it exists — this defines the plan structure.

### Step 4: Design the Technical Architecture

Based on the spec, determine:

1. **Data Model**: Define all custom objects, fields, relationships, and validation rules.
2. **Apex Architecture**: Map to Separation of Concerns layers (Trigger + Trigger Actions, Service, Selector, Domain, Controller, Batch/Schedulable).
3. **Flow Architecture**: Identify Record-triggered, Screen, Autolaunched, and Subflows.
4. **LWC Architecture**: Identify components, target configs, wire vs. imperative, communication patterns.
5. **File Paths**: Map every artifact to its exact `force-app/` path.

### Step 4.5: Calculate Architectural Impact (CLI-Driven)

**PREVENTS PRODUCTION REGRESSIONS.** Before finalizing the plan, use the SF CLI to determine the "Blast Radius" of these changes.

1. **Query Tooling API**:
   For each existing class, object, or flow being modified:
   ```bash
   sf query --tooling --query "SELECT MetadataComponentName, MetadataComponentType FROM MetadataComponentDependency WHERE RefMetadataComponentName = '[TargetName]'"
   ```
2. **Identify Consuming Teams**: Look for dependencies that belong to other features or team namespaces.
3. **Assess Risk**:
   - **High**: Shared utility classes, base objects (Account, Case), or widely used triggers.
   - **Medium**: Domain-specific services with internal dependencies.
   - **Low**: New components or isolated leaf nodes.

Record findings in the **Impact Analysis** section of the `plan.md`.

### Step 5: Generate Plan Files

Create the following files:

#### `.specify/specs/NNN-feature-name/plan.md`
- Populate from the plan template
- Include Impact Analysis Matrix
- Include deployment order (7 phases)
- Include scoring gates table
- Include Architect Sign-Off section (blank — architect fills this)
- Include environment strategy and estimation summary

#### `.specify/specs/NNN-feature-name/data-model.md`
- Detailed object/field definitions
- Field-level metadata XML examples
- Relationship diagrams

#### `.specify/specs/NNN-feature-name/research.md` (optional)
- Only if technical research was needed

### Step 6: Present Plan for Architect Review

Present the plan to the user with clear indication of:
- ⚠️ The **Architect Sign-Off** section is empty and MUST be completed
- **Impact Analysis**: Highlight high-risk dependencies found in Step 4.5.
- The deployment order and scoring gates
- Any constitution violations or exceptions noted

## Next Step

This plan requires Architect review. The Architect Sign-Off section must be completed before `/speckit.sf.stories` can generate story files.

## Output

- **File created**: `.specify/specs/NNN-feature-name/plan.md` (includes Impact Matrix)
- **File created**: `.specify/specs/NNN-feature-name/data-model.md`
- **File created**: `.specify/specs/NNN-feature-name/research.md` (optional)
- **Status**: Pending Architect Review

## GATE

**The plan is NOT approved until the Architect Sign-Off section in plan.md is completed.** The `/speckit.sf.stories` command will check for this and warn if sign-off is missing.
