---
description: "Generate formal Verification Evidence documents with coverage metrics."
---

# Story Verification Evidence Generation

## User Input

$ARGUMENTS

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Story status is **IMPLEMENTED** (completed by `/speckit.sf.implement`)
- Target org is Dev Sandbox (`--target-org dev`)
- Salesforce Code Analyzer plugin installed (for security snapshot)

## Instructions

### Step 1: Identify Story Scope

1. Read the story file.
2. Identify all Apex classes, LWC components, and Triggers from the **SF Implementation Layers** table.
3. Identify relevant test classes (e.g., `MyClass_Test.cls`).

### Step 2: Push Current Changes

Ensure the story branch is up-to-date:
```bash
git add .
git commit -m "chore: prepare for unit test verification"
```

### Step 3: Run Apex Tests & Performance Analysis

```bash
sf apex run test \
  --class-names [Class1Test,Class2Test] \
  --code-coverage \
  --result-format json \
  --output-dir .specify/logs/tests \
  --target-org dev
```

### Step 3.5: Runtime Telemetry Analysis (Log Observation)

**ENSURES SCALABILITY.** Don't just check IF it passed; check HOW it passed.

1. **Identify Slowest Test Methods** from the JSON results.
2. **Pull Debug Logs**:
   ```bash
   sf apex get log --log-id [LogId] --target-org dev
   ```
3. **Parse for Bottlenecks**:
   - **SOQL Count**: >60 per transaction = warning
   - **CPU Time**: >1000ms = warning
   - **DML Rows**: >150 rows in unit tests = warning

Record in the **Runtime Telemetry** section.

### Step 4: Run LWC Jest Tests (if applicable)

```bash
npx lwc-jest -- --testPathPattern [componentName] --json --outputFile .specify/logs/tests/jest-results.json
```

### Step 5: Generate Unit Test Evidence Document

Create: `.specify/specs/[feature-dir]/test-logs/story-$ID-verify.md`

```markdown
# Verification Evidence: Story $ID — $TITLE

**Date**: $DATE
**Developer**: $USER
**Status**: [PASS / FAIL]

## 1. Test Execution Summary

| Engine | Total Tests | Passed | Failed | Duration | Status |
|--------|-------------|--------|--------|----------|--------|
| Apex   | X           | X      | X      | X.XXs    | ✅/❌ |
| LWC    | X           | X      | X      | X.XXs    | ✅/❌ |

## 2. Code Coverage Heatmap

| Class / Component | Type | Covered (%) | Threshold | Status |
|-------------------|------|-------------|-----------|--------|
| $CLASS_NAME       | Apex | 94%         | 90%       | ✅      |

## 3. Runtime Telemetry (Observability)

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Max SOQL | 42 | 60 | ✅ |
| Max CPU | 850ms | 1000ms | ⚠️ WARN |
| Max DML | 12 | 100 | ✅ |

### Bottleneck Analysis
- List any optimization recommendations

## 4. Performance Metrics

List any test method taking longer than **1.0 second**.

## 5. Security Scanner Snapshot

- **Severity 1 (Critical)**: 0
- **Severity 2 (High)**: 0
- **Severity 3 (Moderate)**: X

## 6. Bulk Verification (251+ Records)

- [ ] Bulk test scenario executed
- [ ] No governor limit exceptions detected
```

### Step 6: Update Story File

- Reference the new evidence document
- Set **State** to `VERIFIED`

## Next Step

Run `/speckit.sf.pr` to prepare the pull request.

## Output

- **Evidence Document**: `.specify/specs/[feature]/test-logs/story-$ID-verify.md`
- **Story Update**: Status → VERIFIED, scores recorded
