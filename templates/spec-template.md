# Feature Specification: $FEATURE_NAME

**Feature Branch**: `$FEATURE_NUMBER-$FEATURE_SLUG`
**Created**: $DATE
**Status**: Draft
**Author**: $AUTHOR
**Input**: User description: "$ARGUMENTS"

---

## Salesforce Platform Context

<!--
  REQUIRED: Define the Salesforce platform context for this feature.
  This section ensures all stakeholders understand the target environment.
-->

**Target Org Type**: [Production / Sandbox / Scratch / Developer]
**Target Clouds**: [Sales Cloud, Service Cloud, Experience Cloud, Marketing Cloud, etc.]
**Target Editions**: [Enterprise, Unlimited, Developer]
**API Version**: $API_VERSION <!-- auto-detected from sfdx-project.json -->
**sf CLI Version**: v2.x
**Existing Packages**: [List managed packages that may affect behavior, e.g., TAF, CPQ, DocGen]
**Org Constraints**: [Any org-specific limits, e.g., "sandbox has 200MB storage remaining"]

---

## User Stories

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story must be INDEPENDENTLY TESTABLE — meaning if you implement just ONE,
  you should still have a viable MVP that delivers value.

  Each story will become a separate task_story_NN.md file during the /speckit.sf.stories phase,
  assigned to an individual developer via Jira.

  Focus on WHAT users need and WHY.
  ❌ Avoid HOW to implement (no Apex code, no LWC snippets, no Flow steps).
-->

### User Story 1 — [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the business value]

**Independent Test**: [How this can be tested standalone — e.g., "Can be verified by navigating to Account page and clicking New Invoice"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 — [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the business value]

**Independent Test**: [How this can be tested standalone]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 — [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the business value]

**Independent Test**: [How this can be tested standalone]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed]

---

## Automation Approach Decision

<!--
  REQUIRED: For each behavior in this feature, explicitly choose the automation approach.
  This prevents costly reversals between declarative and imperative solutions.
  Reference Constitution Article III: Declarative-First Mandate.
-->

| Behavior | Approach | Justification |
|----------|----------|---------------|
| [e.g., Default field values on create] | Flow / Validation Rule / Formula | [Why declarative is sufficient] |
| [e.g., Complex multi-object calculation] | Apex Service | [Why Apex is needed — Flow can't handle X] |
| [e.g., External notification] | Platform Event + Apex | [Why async is required] |
| [e.g., User-facing data entry] | LWC Component | [Why screen flow is insufficient] |

---

## Salesforce Object Map

<!--
  High-level entity map — detailed data model comes in the /speckit.sf.plan phase.
  List all objects this feature creates, modifies, or reads from.
-->

| Object | Type | Relationship | Notes |
|--------|------|-------------|-------|
| [Object Name] | Standard / Custom | [Lookup / Master-Detail / Junction] | [Key fields, purpose] |
| [Object Name] | Standard / Custom | [Lookup / Master-Detail / Junction] | [Key fields, purpose] |

---

## Data Volume & Governor Limit Considerations

<!--
  REQUIRED: Estimate data volumes and identify governor limit risks.
  Reference Constitution Article II: Governor-Limit Awareness.
-->

- **Expected record volume**: [e.g., 10k Accounts, 500k Activities, 1M records total]
- **Bulk operation scenarios**: [e.g., daily data loads of 10k records via Data Loader]
- **Peak concurrent users**: [e.g., 50 users creating records simultaneously]
- **Limits to monitor**: [SOQL queries, DML statements, CPU time, heap size]
- **Large data volume (LDV) concerns**: [Any objects expected to exceed 1M records]

---

## Security & Sharing Model

<!--
  REQUIRED: Define the record-level and field-level security approach.
  Reference Constitution Article IV: Security-by-Default.
-->

- **Record-level access (OWD)**: [Private / Public Read / Public Read-Write for each object]
- **Field-level security**: [Permission Set approach — which perm sets for which profiles/roles]
- **Sharing rules**: [Criteria-based / Owner-based sharing rules needed]
- **Record ownership**: [Who owns records by default? Assignment rules?]
- **Guest user access**: [If Experience Cloud — what do unauthenticated users see?]

---

## Edge Cases

<!--
  Include both general edge cases AND Salesforce-specific governor limit scenarios.
-->

### General Edge Cases
- What happens when [boundary condition]?
- How does the system handle [error scenario]?
- What if [concurrent modification scenario]?

### Governor Limit Edge Cases
- What happens when a data load inserts 10,000 records at once? (trigger bulkification)
- What happens when a user's transaction hits 100 SOQL queries? (query optimization)
- What happens when an external callout times out? (retry/error handling)
- What happens when a Flow runs > 2,000 elements? (Flow bulkification)

---

## Functional Requirements

<!--
  Use MUST for requirements, SHOULD for nice-to-haves, MAY for optional.
  Mark unclear items with [NEEDS CLARIFICATION: specific question].
-->

- **FR-001**: System MUST [specific capability]
- **FR-002**: System MUST [specific capability]
- **FR-003**: Users MUST be able to [key interaction]
- **FR-004**: System SHOULD [desirable behavior]
- **FR-005**: System MAY [optional enhancement]

*Unclear requirements:*
- **FR-006**: System MUST [behavior] [NEEDS CLARIFICATION: how should X work when Y?]
- **FR-007**: System MUST [behavior] [NEEDS CLARIFICATION: what is the business rule for Z?]

---

## Non-Functional Requirements

- **NFR-001**: Page load time MUST be < [X] seconds
- **NFR-002**: Apex transactions MUST complete within [X]ms CPU time
- **NFR-003**: System MUST handle [X] concurrent users without degradation
- **NFR-004**: Code coverage MUST exceed 90%

---

## Success Criteria

<!--
  Measurable, technology-agnostic success metrics.
-->

- **SC-001**: [Measurable metric, e.g., "Users can complete invoice creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 200+ record bulk operations without errors"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce manual data entry time by 50%"]

---

## Assumptions & Dependencies

<!--
  Document assumptions made when the feature description didn't specify details.
  These become clarification targets for /speckit.sf.clarify.
-->

- [Assumption about target users]
- [Assumption about scope boundaries]
- [Assumption about existing data/objects]
- [Dependency on existing Apex/Flow/LWC]
- [Dependency on external system or API]

---

## Out of Scope

<!--
  Explicitly list what this feature does NOT include.
  Prevents scope creep during implementation.
-->

- [Feature/behavior explicitly excluded from this release]
- [Future enhancement deferred to a later spec]

---

## Clarification Status

| # | Question | Status | Answer |
|---|----------|--------|--------|
| 1 | [Question from NEEDS CLARIFICATION markers] | ⏳ Pending | — |
| 2 | [Question] | ✅ Answered | [Answer from /speckit.sf.clarify] |

---

## Change Log

| Date | Author | Change |
|------|--------|--------|
| $DATE | $AUTHOR | Initial specification created |
