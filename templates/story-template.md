# $STORY_ID — $STORY_TITLE

**Feature**: $FEATURE_NAME ([spec.md](../spec.md))
**Plan**: [plan.md](../plan.md)
**Constitution**: [constitution.md](../../../memory/constitution.md)
**Type**: $STORY_TYPE <!-- FULL | DECLARATIVE -->
**Priority**: $PRIORITY <!-- P1, P2, P3 -->

---

## Status

- **State**: DRAFT <!-- DRAFT | READY | IMPLEMENTING | REVIEW | QA | DONE -->
- **Assigned To**: [Developer Name]
- **Jira**: [PROJ-NNN]
- **Branch**: story/$FEATURE_NUMBER-$STORY_NUMBER-$STORY_SLUG
- **Started**: —
- **Completed**: —
- **Scores**: —

---

## Description

**As a** [Persona]  
**I want to** [Action]  
**So that** [Business Benefit]

---

## Acceptance Criteria

1. **Given** [initial state/precondition], **When** [action being tested], **Then** [business outcome]
2. **Given** [initial state/precondition], **When** [action being tested], **Then** [business outcome]
3. **Given** [initial state/precondition], **When** [action being tested], **Then** [business outcome]
4. **Given** [initial state/precondition], **When** [action being tested], **Then** [business outcome]
5. **Given** [initial state/precondition], **When** [action being tested], **Then** [business outcome]

---

## Security & Access Matrix

| Permission Set / Profile | Object | Field(s) | Access (R/E) | Rationale |
|--------------------------|--------|----------|--------------|-----------|
| [e.g. Sales User] | [e.g. Invoice__c] | [e.g. Base_Amount__c] | Read/Edit | Standard sales creation |
| [e.g. Finance Admin] | [e.g. Invoice__c] | [e.g. Status__c] | Read/Edit | Workflow management |
| [e.g. Manager] | [e.g. Invoice__c] | [e.g. Base_Amount__c] | Read Only | Visibility into sales |

---

## Test Cases

### Positive Tests ✅
- [Scenario 1] → [expected outcome]
- [Scenario 2] → [expected outcome]
- [Scenario 3] → [expected outcome]

### Negative Tests ❌
- [Scenario 1] → [expected error/log]
- [Scenario 2] → [expected error/log]
- [Scenario 3] → [expected error/log]

### Bulk Tests 📊
- [251+ records scenario] → [no governor failures]
- [Batch/Async scenario] → [successful processing]

---

## Dependencies

- **REQUIRES**: task_story_00.md (Foundation)
- **REQUIRES**: [task_story_0X.md — only if this story depends on another]
- **INDEPENDENT OF**: [task_story_0X.md]

---

## SF Implementation Layers

| Layer | What to Build | SF Skill | File Path | Status |
|-------|-------------|----------|-----------|--------|
| Metadata | [Object/Field/ValidationRule] | sf-metadata | `force-app/...` | [ ] |
| Apex | [Selector/Service/Action/Controller] | sf-apex | `force-app/...` | [ ] |
| Flow | [Requirement] | sf-flow | `force-app/...` | [ ] |
| LWC | [Component Name] | sf-lwc | `force-app/...` | [ ] |
| Tests | [Apex/Jest Test Classes] | sf-testing | `force-app/...` | [ ] |

---

## Scoring Gates

| Layer | SF Skill | Min Score | Target | Actual |
|-------|----------|-----------|--------|--------|
| Metadata | sf-metadata | 84/120 | 100/120 | — |
| Apex | sf-apex | 90/150 | 120/150 | — |
| LWC | sf-lwc | 125/165 | 145/165 | — |
| Coverage | sf-testing | 90% | 95% | — |

---

## Estimation (Human Developer Effort)

| Layer | Complexity | Estimated Effort (Hours) |
|-------|-----------|--------------------------|
| Metadata | [Low/Med/High] | [X] |
| Logic (Apex/Flow) | [Low/Med/High] | [X] |
| UI (LWC) | [Low/Med/High] | [X] |
| Testing | [Low/Med/High] | [X] |
| **Total** | | **[Total Hours]** |

> [!NOTE]
> All estimations are based on **manual developer hours** required to implement and verify the story.

---

## Developer Notes

<!--
  TPO and/or Architect can add implementation guidance, gotchas,
  or references to existing patterns in the codebase.
-->

- [e.g., Use @AuraEnabled(cacheable=false) for DML methods]
- [e.g., Follow TAF trigger pattern — see existing AccountTrigger for reference]
- [e.g., Reference InvoiceSelector from Story-000 for all Invoice__c queries]
- [e.g., This object has a validation rule blocking Status changes — test data must match criteria]

---

## Code Review Checklist

<!--
  Completed by peer reviewer + architect during /speckit.sf.pr.
-->

- [ ] Apex: Bulkification verified (no SOQL/DML in loops)
- [ ] Apex: `with sharing` used (or exception documented)
- [ ] Apex: `WITH USER_MODE` on all SOQL queries
- [ ] Apex: No hardcoded Salesforce IDs
- [ ] LWC: SLDS 2 compliant
- [ ] LWC: Keyboard accessible
- [ ] Tests: PNB pattern (Positive, Negative, Bulk 251+)
- [ ] Tests: Coverage ≥ 90%
- [ ] Tests: Test Data Factory used (no inline data creation)
- [ ] Tests: Assert class with descriptive messages
- [ ] Constitution: No violations (or justified in notes)

**Peer Reviewer**: [Name] — [ ] Approved
**Architect**: [Name] — [ ] Approved

---

## QA Results

<!--
  Completed by QA tester during /speckit.sf.qa.
-->

- **Test Scripts Generated**: [link to task_story_NN_test_scripts.md]
- **Automated Tests**: [X/Y passed]
- **Manual Tests**: [X/Y passed]
- **Coverage**: [X%]
- **QA Verdict**: [ ] PASS / [ ] FAIL
- **QA Tester**: [Name]
- **Date**: [Date]
