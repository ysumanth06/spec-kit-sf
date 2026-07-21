# Implementation Plan: $FEATURE_NAME

**Branch**: `$FEATURE_NUMBER-$FEATURE_SLUG` | **Date**: $DATE | **Spec**: [spec.md](./spec.md)
**Constitution**: [constitution.md](../../memory/constitution.md)

---

## Summary

[Extract from spec: primary requirement + technical approach. 2-3 sentences max.]

---

## Technical Context

<!--
  Auto-populated from sfdx-project.json where possible.
  Fill remaining fields based on spec requirements.
-->

**Platform**: Salesforce [Edition] with [Cloud1, Cloud2]
**API Version**: $API_VERSION <!-- from sfdx-project.json sourceApiVersion -->
**CLI Version**: sf v2.x (NOT legacy sfdx)
**Primary Languages**: Apex (server-side), JavaScript (LWC client-side)
**Testing Framework**: Apex Test Framework (`sf apex run test`), Jest (LWC)
**UI Framework**: Lightning Web Components with SLDS 2
**Automation**: Flow Builder + Apex Triggers (TAF pattern)
**Deployment**: `sf project deploy start` with `--dry-run` validation
**Source Format**: SFDX Source Format (decomposed metadata)

---

## Constitution Check

*GATE: Must pass before implementation begins. Reference: .sfspeckit/memory/constitution.md*

### Pre-Implementation Gates

#### Metadata-First Gate (Article I)
- [ ] All objects/fields defined before any code references them?
- [ ] Permission Sets planned for all new fields?
- [ ] Story-000 (Foundation) covers all shared metadata?

#### Governor-Limit Gate (Article II)
- [ ] Data volume estimates documented in spec?
- [ ] Bulk scenarios identified (251+ records)?
- [ ] No SOQL/DML in loops in any design?

#### Declarative-First Gate (Article III)
- [ ] Automation Approach Decision table completed in spec?
- [ ] Apex justified only where Flow/Validation Rules insufficient?

#### Security Gate (Article IV)
- [ ] `with sharing` default for all Apex classes?
- [ ] `WITH USER_MODE` for all SOQL?
- [ ] No hardcoded Salesforce IDs in design?

#### Test-First Gate (Article V)
- [ ] PNB test pattern planned for all Apex?
- [ ] Test Data Factory designed?
- [ ] 90%+ coverage target set?

#### Separation of Concerns Gate (Article VI)
- [ ] Service/Selector/Domain layers identified?
- [ ] No business logic in triggers or controllers?

---

## Salesforce Project Structure

```text
force-app/
└── main/
    └── default/
        ├── objects/                          # Custom Objects & Fields
        │   └── $OBJECT_NAME__c/
        │       ├── $OBJECT_NAME__c.object-meta.xml
        │       ├── fields/
        │       │   ├── $FIELD_1__c.field-meta.xml
        │       │   └── $FIELD_2__c.field-meta.xml
        │       └── validationRules/
        │           └── $RULE_NAME.validationRule-meta.xml
        ├── classes/                          # Apex Classes
        │   ├── $FeatureService.cls
        │   ├── $FeatureService.cls-meta.xml
        │   ├── $ObjectSelector.cls
        │   ├── $ObjectSelector.cls-meta.xml
        │   ├── TA_$Object_$Behavior.cls      # Trigger Action handlers
        │   ├── TestDataFactory.cls
        │   ├── $FeatureServiceTest.cls
        │   └── ...
        ├── triggers/                         # Trigger files (one per object)
        │   ├── $ObjectTrigger.trigger
        │   └── $ObjectTrigger.trigger-meta.xml
        ├── lwc/                              # Lightning Web Components
        │   └── $componentName/
        │       ├── $componentName.html
        │       ├── $componentName.js
        │       ├── $componentName.css
        │       ├── $componentName.js-meta.xml
        │       └── __tests__/
        │           └── $componentName.test.js
        ├── flows/                            # Flow definitions
        │   └── $FlowName.flow-meta.xml
        ├── permissionsets/                   # Permission Sets
        │   └── $FeatureAccess.permissionset-meta.xml
        ├── customMetadata/                   # CMDT records (TAF config)
        │   └── Trigger_Action__mdt/
        └── messageChannels/                  # Lightning Message Service
```

---

## Deployment Order

<!--
  CRITICAL: Salesforce metadata has strict dependency ordering.
  Deploying out of order causes compilation failures.
-->

| Phase | What | SF Skill | Why This Order |
|-------|------|----------|----------------|
| 1 | Custom Objects + Fields | sf-metadata | All code references these |
| 2 | Permission Sets | sf-metadata | FLS requires fields to exist |
| 3 | Apex Classes + Tests | sf-apex | `@InvocableMethod` needed before Flows |
| 4 | Flows (deploy as Draft) | sf-flow | Flows reference fields and Apex |
| 5 | Activate Flows | sf-deploy | Safe to activate after validation |
| 6 | LWC Components | sf-lwc | UI depends on all backend layers |
| 7 | Agent Configs (if applicable) | sf-ai-agentforce | Agents invoke Flows & Apex |

---

## Scoring Gates

<!--
  Every artifact must meet minimum scoring thresholds before proceeding.
  Scoring is run by the SF skills during implementation.
-->

| Artifact | SF Skill | Max Score | Min to Proceed | Block If Below |
|----------|----------|-----------|----------------|----------------|
| Metadata XML | sf-metadata | 120 | 84 (70%) | 72 |
| Apex Code | sf-apex | 150 | 90 (60%) | 75 |
| LWC Components | sf-lwc | 165 | 125 (76%) | 100 |
| Test Coverage | sf-testing | 120 | 108 (90%) | 84 |

---

## Environment Strategy

| Environment | sf CLI Alias | Purpose | Deployed By |
|------------|-------------|---------|-----------|
| Dev Sandbox | `dev` | Development + code review | Developers (via PR merge) |
| QA Sandbox | `qa` | Verification + regression | QA Lead (`sf project deploy start --target-org qa`) |
| UAT Sandbox | `uat` | Business validation | TPO (`sf project deploy start --target-org uat`) |
| Production | `prod` | Live release | TPO with dry-run (`sf project deploy start --target-org prod`) |

---

## Data Model

<!--
  Detailed entity definitions. Moves beyond the spec's high-level Object Map.
  For complex data models, extract to a separate data-model.md file.
-->

### $OBJECT_NAME__c

| Field API Name | Type | Required | Description |
|---------------|------|----------|-------------|
| Name | Auto Number / Text | Yes | [Format: e.g., INV-{0000}] |
| $Field1__c | Text(255) | Yes | [Description] |
| $Field2__c | Currency(16,2) | Yes | [Description] |
| $Field3__c | Lookup(Account) | No | [Relationship description] |
| $Field4__c | Picklist | Yes | [Values: Active, Inactive, Closed] |

**Sharing Model**: [OWD: Private / Public Read / Public Read-Write]
**Record Types**: [If applicable: Type1, Type2]

---

## 🏛️ Architect Sign-Off

<!--
  GATE: This plan is NOT approved for implementation until the Architect
  completes this section. The /speckit.sf.stories command will not generate
  story files until this section is filled.
-->

### Data Model Review
- [ ] Object relationships are correct (cardinality, cascade delete behavior)
- [ ] Field types are appropriate (no Text where Picklist is better)
- [ ] Naming conventions follow org standards
- **Reviewed by**: [Architect Name]
- **Notes**: [Any concerns or modifications required]

### Security Review
- [ ] OWD settings are correct for each object
- [ ] Sharing rules are sufficient for cross-team access
- [ ] FLS approach uses Permission Sets (not Profiles)
- [ ] No over-permissioning (least privilege principle)
- **Reviewed by**: [Architect Name]

### Governor Limit Assessment
- [ ] Bulk scenarios identified and accounted for
- [ ] Query patterns will scale to estimated data volumes
- [ ] Async processing identified where needed (Batch, Queueable, Future)
- [ ] No known limit risks
- **Reviewed by**: [Architect Name]

### Integration Review (if applicable)
- [ ] Named Credentials configured for external callouts
- [ ] Retry and error handling patterns defined
- [ ] Callout timeout thresholds set
- [ ] Mock patterns defined for testing
- **Reviewed by**: [Architect Name]

### Deployment Strategy
- [ ] Deployment order validated
- [ ] No circular dependencies
- [ ] Rollback plan documented
- **Reviewed by**: [Architect Name]

**Overall Sign-Off**: [ ] APPROVED / [ ] CHANGES REQUIRED
**Date**: [Date]

---

## Estimation Summary

| Layer | Complexity | Estimated Effort |
|-------|-----------|-----------------|
| Metadata (objects, fields, perm sets) | [Low/Med/High] | [X hours] |
| Apex (services, selectors, triggers) | [Low/Med/High] | [X hours] |
| Flow (automations) | [Low/Med/High] | [X hours] |
| LWC (components) | [Low/Med/High] | [X hours] |
| Testing (Apex + Jest) | [Low/Med/High] | [X hours] |
| Deployment + Verification | Low | [X hours] |
| **Total** | | **[X hours / Y story points]** |

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified.**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., `without sharing` on inner class] | [business reason] | [why `with sharing` insufficient] |
| [e.g., Apex over Flow for routing] | [complexity reason] | [why Flow can't handle conditionals] |

---

## Research Notes

<!--
  If technology research was needed (e.g., comparing libraries, evaluating
  platform features), document findings here or in a separate research.md file.
-->

[Research findings, if any. Otherwise delete this section.]

---

## Change Log

| Date | Author | Change |
|------|--------|--------|
| $DATE | $AUTHOR | Initial plan created |
