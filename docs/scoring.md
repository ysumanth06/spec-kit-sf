# SFSpeckit Quality Scoring System

SFSpeckit enforces quality through a **555-point scoring system** across four dimensions.

## Scoring Breakdown

| Layer | Max Score | Default Threshold | What's Scored |
|-------|-----------|-------------------|---------------|
| **Metadata** | 120 | 84 (70%) | Objects, fields, permissions, naming, relationships |
| **Apex** | 150 | 90 (60%) | Bulkification, security, SoC, error handling, SOLID |
| **Flow** | 110 | — | Bulkification, naming, fault paths, DML optimization |
| **LWC** | 165 | 125 (76%) | PICKLES, SLDS 2, accessibility, performance, reactivity |
| **Total** | **555** | — | Weighted across all applicable layers |

> Not all layers apply to every story. A metadata-only (DECLARATIVE) story is scored on the 120-point Metadata scale only.

## When Scoring Happens

| Command | Scoring Event |
|---------|--------------|
| `/speckit.sf.implement` | Per-layer scoring during implementation |
| `/speckit.sf.pr` | Full scoring suite + security scanner |
| `/speckit.sf.score` | Feature-level dashboard across all stories |
| `/speckit.sf.verify` | Evidence document with coverage metrics |

## Metadata Scoring (120 points)

| Category | Points | Criteria |
|----------|--------|----------|
| Naming Conventions | 20 | API names, labels, descriptions |
| Field Types | 20 | Correct types (Picklist vs Text, Lookup vs MD) |
| Relationships | 15 | Proper cascade, junction objects |
| Validation Rules | 15 | Coverage, error messages |
| Permission Sets | 15 | FLS, object access, no Profile edits |
| Record Types | 10 | Business process separation |
| Indexes/Queries | 10 | Custom indexes for filtered lookups |
| Documentation | 15 | Help text, descriptions |

## Apex Scoring (150 points)

| Category | Points | Criteria |
|----------|--------|----------|
| Bulkification | 25 | No SOQL/DML in loops, collection-based processing |
| Security | 25 | `with sharing`, `WITH USER_MODE`, no hardcoded IDs |
| Separation of Concerns | 25 | Service/Selector/Domain/Controller layers |
| Error Handling | 20 | Try-catch, meaningful messages, custom exceptions |
| Test Quality | 20 | PNB pattern, TestDataFactory, Assert class |
| SOLID Principles | 15 | Single responsibility, loose coupling |
| Performance | 10 | Efficient collections, lazy loading, async where appropriate |
| Naming & Style | 10 | Consistent naming, comments on complex logic |

### Scanner Penalties
- **-10 points** per Severity 3 (Moderate) PMD violation
- **Automatic FAIL** for any Severity 1 (Critical) violation

## Flow Scoring (110 points)

| Category | Points | Criteria |
|----------|--------|----------|
| Bulkification | 20 | No DML/Get in loops |
| Naming | 15 | Clear element names, descriptions |
| Fault Paths | 20 | Error handling on every DML |
| DML Optimization | 15 | Batch DML operations |
| Flow Type | 15 | Correct type for use case |
| Documentation | 10 | Description, notes |
| Testing | 15 | Coverage via Apex tests |

## LWC Scoring (165 points)

| Category | Points | Criteria |
|----------|--------|----------|
| PICKLES Architecture | 25 | Props, Imports, Config, Keys, Lifecycle, Events, State |
| SLDS 2 Compliance | 20 | Design tokens, Lightning components |
| Accessibility | 25 | Keyboard nav, ARIA, screen reader |
| Performance | 20 | Wire service, lazy loading, caching |
| Reactivity | 20 | Tracked properties, immutable patterns |
| Jest Tests | 25 | Component rendering, event handling, mocks |
| Error Handling | 15 | Toast messages, loading states |
| Naming & Style | 15 | Consistent naming, CSS custom properties |

### Scanner Penalties
- **-5 points** per ESLint violation

## Quality Grades

| Grade | Score Range | Meaning |
|-------|------------|---------|
| **A** | 90–100% | Production-ready, exemplary quality |
| **B** | 80–89% | Production-ready, minor improvements possible |
| **C** | 70–79% | Acceptable, review recommended |
| **D** | 60–69% | Below standard, remediation required |
| **F** | < 60% | Not deployable, significant rework needed |

## Auto-Heal

When a score falls below threshold during `/speckit.sf.implement`:
1. The AI analyzes specific deductions
2. Automatically refactors the code
3. Re-runs scoring
4. Up to 3 retries per layer

If auto-heal fails after 3 attempts, the developer is notified with specific blockers.

## Customizing Thresholds

Override defaults in `.specify/extensions/sf/sf-config.yml`:

```yaml
scoring:
  metadata: 80   # Lower from default 84 (70%)
  apex: 100      # Raise from default 90 (67%)
  lwc: 80        # Lower from default 125 (76%)
  testing: 80    # Coverage threshold
```
