# Salesforce Development Constitution

**Project**: $PROJECT_NAME
**Created**: $DATE
**Status**: Active
**Version**: 1.0

> This constitution establishes the immutable principles governing all Salesforce development in this project. Every specification, plan, and implementation must comply with these articles. Exceptions require documented justification in the Complexity Tracking section of the relevant plan.

---

## Article I: Metadata-First Principle

Every feature MUST begin with metadata definition. No Apex class, Flow, or LWC shall reference objects or fields that do not exist in `force-app/main/default/objects/`.

### Enforcement Rules
1. All Custom Objects and Fields must be defined in metadata XML before any code references them
2. Permission Sets must be created for every new object/field (fields are INVISIBLE without FLS)
3. The metadata foundation (Story-000) MUST deploy and verify before any code stories begin

### Orchestration Order
```
sf-metadata → sf-apex → sf-flow → sf-lwc → sf-deploy → sf-testing → sf-data
```

### Exception Process
If metadata cannot be pre-defined (e.g., dynamic schema scenarios), document the runtime metadata access pattern and ensure `Schema.describe()` calls are cached and bulkified.

---

## Article II: Governor-Limit Awareness

All Apex code MUST be designed for bulk execution. Specifications MUST include data volume estimates. Every trigger, service, and batch class must operate correctly with 200+ records in a single transaction.

### Enforcement Rules
1. No SOQL queries inside loops — use collections and maps
2. No DML statements inside loops — collect records, DML once
3. Minimum test scenario: 251 records (crosses 200-record batch boundary)
4. CPU time budget: design for < 5,000ms per transaction
5. SOQL query budget: design for < 50 queries per transaction
6. Heap size: design for < 6MB synchronous / 12MB asynchronous

### Limits to Track Per Feature

| Limit | Synchronous | Asynchronous |
|-------|------------|--------------|
| SOQL Queries | 100 | 200 |
| DML Statements | 150 | 150 |
| CPU Time | 10,000ms | 60,000ms |
| Heap Size | 6MB | 12MB |
| Callouts | 100 | 100 |

### Exception Process
If a feature requires governor limit exceptions (e.g., complex data transformations), use `@future`, Queueable, or Batch Apex. Document the async pattern choice and retry strategy.

---

## Article III: Declarative-First Mandate

Before writing Apex, validate whether the requirement can be met declaratively. Apex is reserved for scenarios that Flow, Validation Rules, or Formula Fields cannot handle.

### Apex is Justified When
- Complex business logic involving multiple objects with conditional branching Flow cannot express
- Callouts to external systems (Named Credentials + HttpCalloutMock)
- Batch processing > 50,000 records
- Custom UI interactions requiring `@AuraEnabled` methods
- Complex data transformations requiring Apex Collections (Maps, Sets)
- Platform Event publishing/subscribing with complex routing

### Automation Decision Matrix

| Requirement Type | First Choice | Fallback |
|-----------------|-------------|----------|
| Field defaults | Formula Field / Record-Triggered Flow | Apex Trigger Action |
| Field validation | Validation Rule | Apex Trigger Action |
| Record automation | Record-Triggered Flow | Apex Trigger Action |
| Scheduled work | Scheduled Flow | Apex Schedulable + Batch |
| Screen interaction | Screen Flow | LWC |
| External callout | — | Apex Service + Named Credential |
| Mass data processing | — | Apex Batch |

### Exception Process
Document the declarative alternative considered and why it was insufficient. Include this in the story file's Developer Notes section.

---

## Article IV: Security-by-Default

All code must enforce Salesforce's security model. No code bypasses sharing, FLS, or CRUD checks unless explicitly justified and approved by the Architect.

### Enforcement Rules
1. **Apex classes**: Always `with sharing` unless documented exception with Architect approval
2. **SOQL queries**: Always `WITH USER_MODE` or `WITH SECURITY_ENFORCED`
3. **LWC inputs**: Sanitize with `lightning-input` validators; never render unescaped HTML
4. **No hardcoded IDs**: No 15/18-character Salesforce record IDs in code — use Custom Settings, Custom Metadata, or queries
5. **No hardcoded URLs**: Use `NavigationMixin` or `{!$Api.Partner_Server_URL}` patterns
6. **Sensitive data**: Never log PII (email, phone, SSN) in debug statements

### `without sharing` Exception Process
1. Document the specific business reason (e.g., "system integration user needs cross-org access")
2. Architect must approve
3. Add `// SECURITY: without sharing justified — [reason] — approved by [Architect] on [date]` comment
4. Limit scope: use `without sharing` on the smallest possible inner class, not the entire service

---

## Article V: Test-First Imperative (PNB Pattern)

All test classes must follow the PNB pattern: Positive, Negative, Bulk. Tests must use Test Data Factory and achieve ≥90% code coverage.

### Enforcement Rules
1. All test classes: `@IsTest(SeeAllData=false)` — no exceptions
2. **P**ositive tests: Verify correct behavior with valid inputs
3. **N**egative tests: Verify error handling with invalid inputs
4. **B**ulk tests: Verify behavior with 251+ records (crosses 200-record batch boundary)
5. Test Data Factory pattern required — no inline test data creation
6. `Assert` class required (not legacy `System.assert`) with descriptive messages
7. 90%+ code coverage target (75% Salesforce minimum, 90% team standard)
8. `Test.startTest()` / `Test.stopTest()` always paired — never orphaned

### Test Data Factory Pattern
```apex
@IsTest
public class TestDataFactory {
    public static List<Account> createAccounts(Integer count) {
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < count; i++) {
            accounts.add(new Account(Name = 'Test Account ' + i));
        }
        return accounts;
    }

    public static List<Account> createAndInsertAccounts(Integer count) {
        List<Account> accounts = createAccounts(count);
        insert accounts;
        return accounts;
    }
}
```

### Exception Process
If a test requires `SeeAllData=true` (e.g., testing against standard price book), document the reason and limit scope to the specific test method, not the class.

---

## Article VI: Separation of Concerns

Code must follow a layered architecture. No single class should mix triggers, business logic, data access, and UI concerns.

### Required Layers

| Layer | Naming Convention | Responsibility |
|-------|------------------|----------------|
| **Trigger** | `[Object]Trigger.trigger` | One trigger per object, dispatches to handler |
| **Trigger Action** | `TA_[Object]_[Behavior].cls` | Single trigger action handler (TAF pattern) |
| **Service** | `[Feature]Service.cls` | Business logic, orchestration |
| **Selector** | `[Object]Selector.cls` | All SOQL queries for an object |
| **Domain** | `[Object]Domain.cls` | Record validation, field calculation |
| **Controller** | `[Feature]Controller.cls` | `@AuraEnabled` methods only — no business logic |
| **Test** | `[ClassName]Test.cls` | Test class mirrors production class |

### Anti-Patterns (NEVER Do)
- ❌ Business logic in a trigger body
- ❌ SOQL queries in a controller class
- ❌ DML operations in an LWC JavaScript file
- ❌ Multiple triggers on the same object
- ❌ God classes with > 500 lines

### Exception Process
For small utilities (< 50 lines), a single helper class is acceptable. Document why the full layered pattern is unnecessary.

---

## Article VII: Deployment Safety

All deployments must be validated before execution. The deployment order must follow metadata dependency chains.

### Enforcement Rules
1. **Always `--dry-run` first** for QA, UAT, and Production deployments
2. **Deploy in dependency order**:
   - Phase 1: Custom Objects + Fields
   - Phase 2: Permission Sets (FLS)
   - Phase 3: Apex Classes + Test Classes
   - Phase 4: Flows (deploy as Draft)
   - Phase 5: Activate Flows
   - Phase 6: LWC Components
   - Phase 7: Agent Configurations (if applicable)
3. **Permission Sets over Profiles** for field-level security
4. **Always include a Permission Set** when creating new objects/fields
5. **Run all local tests** on deployment: `--test-level RunLocalTests`

### Environment Promotion Path
```
Dev Sandbox → QA Sandbox → UAT Sandbox → Production
(PR merge)    (sf deploy)   (sf deploy)    (sf deploy + dry-run)
```

### Rollback Strategy
- Apex: Deploy previous version from Git
- Flows: Deactivate current, activate previous version (Flows are versioned)
- Metadata: Deploy previous XML from Git
- **Destructive changes**: Require `destructiveChanges.xml` — Architect approval required

---

## Article VIII: Agent Architecture

When building Agentforce agents, follow topic-action patterns with clear boundaries.

### Enforcement Rules
1. **Topics** map 1:1 to business capabilities (e.g., "Order Management", "Case Resolution")
2. **Actions** are atomic and reusable across topics
3. **System instructions** encode persona and guardrails, NOT business logic
4. Actions invoke `@InvocableMethod` Apex or Flows — never raw SOQL/DML
5. **Lifecycle**: Deactivate → Modify → Re-publish → Re-activate (never edit live agents)
6. **Testing**: Use `sf agent test` for automated multi-turn conversation testing

### Exception Process
If a topic spans multiple capabilities (e.g., "Customer Service" covering orders + returns + complaints), document the topic boundary decision and get Architect approval.

---

## Article IX: Cross-Skill Orchestration

SF Spec-Kit skills must be invoked in the correct dependency order. Each skill's output feeds the next skill's input.

### Skill Dependency Chain
```
sf-metadata → sf-apex → sf-flow → sf-lwc → sf-deploy → sf-testing → sf-data
```

### Cross-Skill Rules
1. Never invoke sf-apex before sf-metadata has created the referenced objects
2. Never invoke sf-flow before sf-apex if the Flow calls `@InvocableMethod` classes
3. Never invoke sf-lwc before sf-apex if the LWC calls `@AuraEnabled` methods
4. Never invoke sf-data before sf-deploy has deployed the target objects to the org
5. Always invoke sf-testing after sf-deploy to validate in-org behavior

### Scoring Gates

| Skill | Scoring System | Minimum to Proceed | Block If Below |
|-------|---------------|-------------------|----------------|
| sf-metadata | 120 points / 6 categories | 84 (70%) | 72 |
| sf-apex | 150 points / 7 categories | 90 (60%) | 75 |
| sf-lwc | 165 points / PICKLES | 125 (76%) | 100 |
| sf-testing | 120 points / 6 categories | 108 (90%) | 84 |

---

## Amendment Process

Modifications to this constitution require:
1. Documented rationale for the change
2. Review and approval by Architect + TPO
3. Impact assessment on existing specifications and implementations
4. Version increment with dated changelog entry

### Changelog
| Date | Version | Change | Approved By |
|------|---------|--------|-------------|
| $DATE | 1.0 | Initial constitution | $AUTHOR |
