---
description: "Create a technical plan with force-app structure and blast radius analysis."
---

# Create Technical Implementation Plan

## User Input

$ARGUMENTS

## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Metadata/Objects/Relationships** (`sf-metadata`, `sf-data`, `sf-diagram-mermaid`)
- **Apex/LWC Architectural Patterns** (`sf-apex`, `sf-lwc`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in architectural planning and blast radius analysis. However, the standards in `docs/scoring.md` are the **primary source of truth**.

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

Read `.specify/templates/plan-template.md` — this defines the plan structure.

### Step 4: Design the Technical Architecture

Based on the spec, determine:

1. **Data Model**: Define all custom objects, fields, relationships, and validation rules. Consider:
   - Field types (use Picklist over Text where values are constrained)
   - Lookup vs. Master-Detail relationships (cascade delete implications)
   - Auto Number vs. Name fields
   - Record types (if multiple business processes on same object)

2. **Apex Architecture**: Map to Separation of Concerns layers:
   - Trigger + Trigger Actions (TAF pattern) — one trigger per object
   - Service classes — business logic orchestration
   - Selector classes — all SOQL for an object
   - Domain classes — record validation, field calculation
   - Controller classes — `@AuraEnabled` methods only
   - Batch/Schedulable — async processing if needed

3. **Flow Architecture**: Identify:
   - Record-triggered flows (Before/After, on Create/Update/Delete)
   - Screen flows (user-facing wizards)
   - Autolaunched flows (background processing)
   - Flow interview callbacks

4. **LWC Architecture**: Identify:
   - Components with their target configs (Record Page, App Page, Home Page)
   - Wire vs. imperative Apex calls
   - Component communication patterns (events, LMS, parent-child)
   - SLDS 2 design tokens

5. **File Paths**: Map every artifact to its exact `force-app/` path.

### Step 4.5: Calculate Architectural Impact (CLI-Driven)

**PREVENTS PRODUCTION REGRESSIONS.** Before finalizing the plan, use the SF CLI to determine the "Blast Radius" of these changes.

1. **Query Tooling API**:
   For each existing class, object, or flow being modified:
   ```bash
   sf query --tooling --query "SELECT MetadataComponentName, MetadataComponentType FROM MetadataComponentDependency WHERE RefMetadataComponentName = '[TargetName]'"
   ```
2. **Identify Consuming Teams**:
   Look for dependencies that belong to other features or team namespaces.
3. **Assess Risk**:
   - **High**: Shared utility classes, base objects (Account, Case), or widely used triggers.
   - **Medium**: Domain-specific services with internal dependencies.
   - **Low**: New components or isolated leaf nodes.

Record findings in the **Impact Analysis** section of the `plan.md`.

### Step 5: Generate Plan Files

Create the following files:

#### `.specify/specs/NNN-feature-name/plan.md`
- Populate from the plan template
- Auto-fill technical context from `sfdx-project.json`
- **Impact Analysis Matrix**: List all components at risk of regression.
- Include deployment order (7 phases)
- Include scoring gates table
- Include Architect Sign-Off section (blank — architect fills this)
- Include environment strategy
- Include estimation summary

#### `.specify/specs/NNN-feature-name/data-model.md`
- Detailed object/field definitions
- Field-level metadata XML examples
- Relationship diagrams (consider using sf-diagram-mermaid)

#### `.specify/specs/NNN-feature-name/research.md` (optional)
- Only if technical research was needed
- Document findings, comparisons, decisions

### Step 6: Present Plan for Architect Review

Present the plan to the user with clear indication of:
- ⚠️ The **Architect Sign-Off** section is empty and MUST be completed
- **Impact Analysis**: Highlight high-risk dependencies found in Step 4.5.
- The deployment order
- The scoring gates
- Any constitution violations or exceptions noted

Remind: "This plan requires Architect review. The 🏛️ Architect Sign-Off section must be completed before `/speckit.sf.stories` can generate story files."

## Output

- **Primary Blueprint**: `.specify/specs/NNN-feature-name/plan.md`
- **Data Architecture**: `.specify/specs/NNN-feature-name/data-model.md`
- **Traceability**: Impact Matrix populated in `plan.md`
- **Status**: Updated to `Architect Review Required`

## Error Handling

- **Missing Spec**: STOP and run `/speckit.sf.specify` or `/speckit.sf.clarify` first.
- **Constitutional Conflict**: If the design violates an Article (e.g., Article VI: SoC), itemize the risk in the "Exceptions" section and require explicit Architect waiver.

## GATE

**The plan is NOT approved until the Architect Sign-Off section in plan.md is completed.** The `/speckit.sf.stories` skill will check for this and warn if sign-off is missing.

## Next Step

This plan requires Architect review. The Architect Sign-Off section must be completed before `/speckit.sf.stories` can generate story files.
