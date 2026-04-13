# SFSpeckit Quality Scoring System

SFSpeckit enforces quality through a **555-point scoring system** across four dimensions.

## The Standalone Source of Truth

> [!IMPORTANT]
> This document is the **absolute Source of Truth** for all Salesforce quality gates in this extension. Even if external foundational skills (like `sf-apex`) are used as accelerators, the AI Agent must prioritize the standards and checklists below to ensure enterprise-grade SDLC compliance.

## Scoring Breakdown

| Layer | Max Score | Default Threshold | What's Scored |
|-------|-----------|-------------------|---------------|
| **Metadata** | 120 | 84 (70%) | Objects, fields, permissions, naming, relationships |
| **Apex** | 150 | 90 (60%) | Bulkification, security, SoC, error handling, SOLID |
| **Flow** | 110 | — | Bulkification, naming, fault paths, DML optimization |
| **LWC** | 165 | 125 (76%) | Component architecture, SLDS, accessibility, performance |
| **Total** | **555** | — | Weighted across all applicable layers |

---

## Authoritative Reference Logic

When evaluating complex architectural decisions, the AI Agent follows these routing principles to simulate official documentation lookup:

### 1. Identify the Doc Family
| Family | Typical Source | Use Case |
|--------|----------------|----------|
| **Developer Docs** | `developer.salesforce.com/docs/...` | Apex methods, APIs, LWC hooks, metadata XML |
| **Salesforce Help** | `help.salesforce.com/...` | Setup UI, feature limits, standard object behavior |
| **Platform Guides** | `developer.salesforce.com/docs/platform/...` | Modern guides (Agentforce, Enhanced Messaging) |

### 2. Best Practice Grounding
The AI must prioritize **Official Salesforce Release Notes** and **Architect Decision Guides** over third-party blogs or outdated stack-overflow answers.

---

## Technical Checklists (The AI Rubric)

### Metadata (120 points)
- **Naming (20pts)**: PascalCase for API names, clear labels, mandatory descriptions.
- **Relationships (15pts)**: Correct use of Master-Detail vs. Lookup. Junction objects for M:M.
- **Security (15pts)**: Permission Set-first approach. No FLS on Profiles. Field-level security covers all new fields.
- **Scalability (15pts)**: Minimal use of Formula fields on high-volume objects (index awareness).

### Apex (150 points)
- **Bulkification (25pts)**: Zero SOQL or DML inside loops. Collection-based processing (Set/List/Map).
- **Security (25pts)**: `with sharing` present. `WITH USER_MODE` or `Security.stripInaccessible()` on all queries. No hardcoded IDs.
- **Separation of Concerns (25pts)**: Logic separated into Service, Selector, Domain, and Controller layers (based on TAF/fflib standards).
- **Testing (20pts)**: PNB (Positive/Negative/Bulk) pattern. High coverage (90%+) and meaningful assertions.

### Flow (110 points)
- **Performance (20pts)**: No Get/Update elements inside loops. Fast field updates used where appropriate.
- **Resilience (20pts)**: Fault paths on every DML operation. Meaningful error handling.
- **Standards (15pts)**: Clear element labels, consistent naming, one record-triggered flow per object/event.

### LWC (165 points)
- **Architecture (25pts)**: Clear separation of props/state. Proper use of @wire vs. imperative Apex.
- **Accessibility (25pts)**: Keyboard navigation, ARIA labels, SLDS 2.0 design tokens.
- **Performance (20pts)**: Minimal DOM footprint, efficient event handling (no frequent `dispatch`), `@wire` caching used correctly.

---

## Auto-Heal Loop

When a score falls below threshold during `/speckit.sf.implement`:
1. **Analyze**: Agent identifies specific checklist failures.
2. **Refactor**: Agent modifies code to address the gap.
3. **Re-Score**: Agent re-evaluates the refactored code.
4. **Retry Limit**: The loop repeats up to 3 times before reporting a permanent quality failure.
