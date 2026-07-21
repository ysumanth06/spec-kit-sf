# Salesforce Clarification Checklist

**Feature**: $FEATURE_NAME
**Spec**: [spec.md](./spec.md)
**Status**: In Progress

---

<!--
  Walk through each question with the TPO/BPO.
  Record answers in the Answer column.
  Update spec.md with clarifications and remove [NEEDS CLARIFICATION] markers.
-->

## 10-Point Salesforce Clarification Checklist

### 1. Org Architecture

**Question**: Is this feature for a single org or multi-org architecture (parent/child, hub-spoke)?

**Why it matters**: Multi-org requires data sync strategy, cross-org APIs, or Salesforce Connect.

**Answer**: [Record answer here]

**Impact on spec**: [How this changes the spec, if at all]

---

### 2. Data Migration

**Question**: Does existing data need to be migrated or transformed for this feature? If yes, what's the source, volume, and format?

**Why it matters**: Data migration may require Batch Apex, ETL tools, or custom import scripts. Affects Story-000 scope.

**Answer**: [Record answer here]

---

### 3. External Integrations

**Question**: Are there callouts to external systems? If yes, what protocols (REST/SOAP), authentication (OAuth/API Key), and what are the external system SLAs?

**Why it matters**: Requires Named Credentials, HttpCalloutMock for tests, retry logic, and circuit breaker patterns. Affects governor limit budget (max 100 callouts per transaction).

**Answer**: [Record answer here]

---

### 4. Sharing Model

**Question**: What are the Organization-Wide Default (OWD) settings for the objects involved? Who should see what records?

**Why it matters**: Incorrect OWD settings cause users to see too much or too little data. Sharing rules, manual sharing, and Apex managed sharing have different complexity levels.

**Answer**: [Record answer here]

---

### 5. Managed Package Interactions

**Question**: Are there installed managed packages (e.g., CPQ, DocGen, Financial Force) that interact with the objects in this feature? Do they have triggers, flows, or validation rules on these objects?

**Why it matters**: Package triggers can conflict with custom triggers, exceed governor limits, or lock records. Need to understand the full automation landscape.

**Answer**: [Record answer here]

---

### 6. Flow vs. Apex Decisions

**Question**: For each automation identified in the spec, has the team confirmed whether Flow or Apex is the right approach? Are there any automations where the choice is unclear?

**Why it matters**: Constitution Article III mandates Declarative-First. Switching from Flow to Apex (or vice versa) mid-implementation is expensive.

**Answer**: [Record answer here]

---

### 7. Experience Cloud

**Question**: Does this feature need to be accessible in a Community/Portal (Experience Cloud site)? If yes, which user profiles (Customer Community, Partner, etc.)?

**Why it matters**: Experience Cloud has different security contexts (guest vs. authenticated), LWC target configs, and sharing model implications. Components need `isExposed: true` and correct targets in meta.xml.

**Answer**: [Record answer here]

---

### 8. Mobile Compatibility

**Question**: Does this feature need to work on the Salesforce Mobile App? Are there specific mobile-only behaviors (camera, geolocation, offline)?

**Why it matters**: Mobile has smaller screens, different navigation patterns, and some LWC features aren't supported. Lightning App Builder layouts differ between desktop and mobile.

**Answer**: [Record answer here]

---

### 9. Agentforce Integration

**Question**: Should this feature be accessible to Agentforce AI agents? If yes, which actions should agents be able to perform?

**Why it matters**: Agent-accessible features need `@InvocableMethod` Apex or Autolaunched Flows. Topic/action architecture must be planned. Affects Story decomposition (may add Agent story).

**Answer**: [Record answer here]

---

### 10. Multi-Currency / Multi-Language

**Question**: Does this feature need to support multiple currencies or multiple languages (Translation Workbench)?

**Why it matters**: Multi-currency requires CurrencyIsoCode fields on custom objects, dated exchange rates, and special handling in formulas/reports. Multi-language requires custom labels and translated picklist values.

**Answer**: [Record answer here]

---

## Summary of Clarifications

| # | Topic | Decision | Spec Section Updated |
|---|-------|----------|---------------------|
| 1 | Org Architecture | [Single/Multi] | Platform Context |
| 2 | Data Migration | [Yes/No — details] | Assumptions |
| 3 | External Integrations | [Yes/No — systems] | Object Map, NFRs |
| 4 | Sharing Model | [OWD settings] | Security & Sharing Model |
| 5 | Managed Packages | [List] | Assumptions |
| 6 | Flow vs. Apex | [Confirmed/Changed] | Automation Approach |
| 7 | Experience Cloud | [Yes/No] | Platform Context |
| 8 | Mobile | [Yes/No] | NFRs |
| 9 | Agentforce | [Yes/No] | User Stories |
| 10 | Multi-Currency/Language | [Yes/No] | Platform Context |

---

## Remaining Clarifications

<!--
  List any [NEEDS CLARIFICATION] markers still unresolved after this session.
  These must be resolved before /speckit.sf.plan can generate an approved plan.
-->

- [ ] [Outstanding question 1]
- [ ] [Outstanding question 2]
