# Clarification Report: $FEATURE_NAME

**Project**: $PROJECT_NAME
**TPO**: $TPO_NAME
**Status**: Pending Business Decision
**Source Spec**: [spec.md](./spec.md)

---

## Executive Summary

This report identifies architectural and business logic gaps in the current feature specification. Decisions made in this document will directly impact the technical design, build cost, and security model of the $FEATURE_NAME feature.

---

## Section 1: Technical Foundation (Salesforce Baseline)

<!-- The 10-point Salesforce checklist goes here -->

### 1.1 Org Architecture
**Question**: $QUESTION
**Architect Impact**: $IMPACT
**Decision Options**:
- [ ] Option A: $DETAILS
- [ ] Option B: $DETAILS
**Final Decision**: 

---

## Section 2: Deep Business Analysis (Logic Gaps)

<!-- Dynamic questions generated from spec analysis -->

### 2.1 [Gap Title]
**Context from Spec**: "$SNIPPET_FROM_SPEC"
**The Question**: $CLEAR_LANGUAGE_QUESTION
**Architect Impact**: $WHY_THIS_MATTERS_FOR_CODE
**Decision Options**:
- [ ] Option A: $PROS_CONS
- [ ] Option B: $PROS_CONS
**Final Decision**: 

---

## Section 3: Stakeholder Sign-off

| Role | Name | Date | Signature / Method |
|------|------|------|--------------------|
| **TPO** (Technical) | | | |
| **BPO** (Business) | | | |
| **Architect** | | | |

---

## Next Steps

1.  **Review**: TPO reviews this report with Business Stakeholders.
2.  **Decide**: Record the "Final Decision" for each item above.
3.  **Approve**: TPO, BPO, and Architect sign off on the report.
4.  **Sync**: Re-run `/speckit.sf.clarify` to apply these decisions to the master `spec.md`.
