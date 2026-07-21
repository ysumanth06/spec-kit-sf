---
description: "555-point quality scoring dashboard across all stories in a feature."
---

# Feature Quality Scoring Dashboard

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.
Use `scoring.*` thresholds if configured.

## Prerequisites

- Feature code exists in `force-app/`
- Story files exist in `.specify/specs/NNN-feature-name/`

## Instructions

### Step 1: Identify Feature Scope

1. Read all story files in `.specify/specs/NNN-feature-name/`
2. Collect all artifacts per story (Apex classes, LWC components, metadata)
3. Build a complete file inventory for the feature

### Step 2: Run Metadata Scoring

For each custom object created/modified by this feature:
- Evaluate metadata quality using the rubric in `docs/scoring.md`
- Score across 6 categories (120 points max):
  - Field definitions (types, required, descriptions)
  - Relationship design (lookup vs. master-detail)
  - Permission Sets (FLS coverage)
  - Naming conventions
  - Validation rules
  - Documentation

### Step 3: Run Apex Scoring

For each Apex class created/modified:
- Evaluate Apex quality using the rubric in `docs/scoring.md`
- Score across 7 categories (150 points max):
  - Bulkification compliance
  - Security (sharing, user mode, no hardcoded IDs)
  - SOLID principles
  - Error handling
  - Naming conventions
  - Documentation/comments
  - Performance optimization

### Step 4: Run LWC Scoring

For each LWC component created/modified:
- Evaluate LWC quality using the rubric in `docs/scoring.md`
- Score using PICKLES methodology (165 points max):
  - Performance
  - Interoperability
  - Consistency
  - Knowledge (documentation)
  - Lifecycle management
  - Error handling
  - Security

### Step 5: Run Test Scoring

Evaluate test quality using the rubric in `docs/scoring.md`:
- Score across 6 categories (120 points max):
  - PNB pattern compliance
  - TestDataFactory usage
  - Assert class with messages
  - SeeAllData=false compliance
  - Coverage percentage
  - Bulk test presence (251+)

### Step 6: Generate Combined Dashboard

```markdown

## 📊 Quality Scoring Dashboard: Feature NNN-feature-name

### Overall Feature Score
| Category | Max | Actual | % | Status |
|----------|-----|--------|---|--------|
| Metadata | 120 | XX | XX% | ✅/❌ |
| Apex | 150 | XX | XX% | ✅/❌ |
| LWC | 165 | XX | XX% | ✅/❌ |
| Testing | 120 | XX | XX% | ✅/❌ |
| **Total** | **555** | **XX** | **XX%** | **✅/❌** |

### Per-Story Breakdown
| Story | Status | Metadata | Apex | LWC | Testing | Total |
|-------|--------|----------|------|-----|---------|-------|
| Story-000 | DONE ✅ | 98/120 | 85/150 | — | 110/120 | 293 |
| Story-001 | QA ⏳ | — | 125/150 | 142/165 | 108/120 | 375 |
| Story-002 | REVIEW ⏳ | — | 95/150 | — | 100/120 | 195 |

### Top Improvements Needed
1. [Story-002] Apex scoring: Add error handling to InvoiceProcessor (+15 pts)
2. [Story-001] LWC scoring: Add ARIA labels to invoiceCreator (+10 pts)
3. [Story-000] Metadata: Add field descriptions to Invoice__c fields (+8 pts)

### Code Coverage Summary
| Class | Coverage | Target | Status |
|-------|----------|--------|--------|
| InvoiceService | 95% | 90% | ✅ |
| InvoiceProcessor | 88% | 90% | ❌ |
| InvoiceController | 92% | 90% | ✅ |
| Overall | 91% | 90% | ✅ |

### Story Status Summary
| Status | Count |
|--------|-------|
| DONE | X |
| QA | X |
| REVIEW | X |
| IMPLEMENTING | X |
| READY | X |
| DRAFT | X |
```

### Step 7: Determine Feature Readiness

- If ALL scoring gates pass and ALL stories are DONE → "Feature is ready for `/speckit.sf.deploy qa`"
- If any gates fail → list specific improvements needed before deployment
- If any stories are not DONE → list pending stories

## Error Handling

- **Prerequisite Missing**: STOP and inform the user of the missing context.

## Next Step

If all scoring gates pass: Run `/speckit.sf.deploy qa` to promote to QA environment.
