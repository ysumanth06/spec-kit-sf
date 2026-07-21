---
description: "Generate formal Verification Evidence documents with coverage metrics."
---

# Story Verification Evidence Generation

## User Input

$ARGUMENTS

## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Salesforce Verification & Testing** (`sf-testing`, `sf-apex`, `sf-lwc`)
- **Observability & Logs** (`sf-debug`, `sf-agentforce-observability`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in generating verification evidence. However, the standards in `docs/scoring.md` are the **primary source of truth**.

## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.

## Prerequisites

- Story status is **IMPLEMENTED** (completed by /speckit.sf.implement)
- Target org is Dev Sandbox (`--target-org dev`)
- Salesforce Code Analyzer (v5) installed (for security snapshot)

## Instructions

### Step 1: Identify Story Scope

1. Read the story file.
2. Identify all Apex classes, LWC components, and Triggers from the **SF Implementation Layers** table.
3. Identify relevant test classes (e.g., `MyClass_Test.cls`).

### Step 2: Pre-Verification Guardrails

1. **Deployment Check**: Confirm that the latest code has been successfully deployed to the target Salesforce Org. 
   - Ask: "Have you successfully deployed the latest changes to your Salesforce org via `sf project deploy start`?"
   - If NO: STOP and instruct the developer to deploy first. Verification MUST run against deployed code.
2. **Git Commit Guardrail**: Ensure no unverified code is pushed to remote. Do not run any `git commit` or `git push` commands until all tests pass in the following steps.

### Step 3: Run Apex Tests & Security Scans

```bash
sf apex run test \
  --class-names [Class1Test,Class2Test] \
  --code-coverage \
  --result-format json \
  --output-dir .specify/logs/tests \
  --target-org dev
```

Run Code Analyzer v5 security snapshot:
```bash
sf code-analyzer run --path "force-app/" --engine pmd,eslint
```

### Step 3.5: Runtime Telemetry Analysis (Log Observation)

**ENSURES SCALABILITY.** Don't just check IF it passed; check HOW it passed.

1. **Identify Slowest Test Methods**: From the JSON results in Step 3.
2. **Pull Debug Logs**:
   ```bash
   sf apex get log --log-id [LogId] --target-org dev
   ```
3. **Parse for Bottlenecks**:
   - **SOQL Count**: High number of queries (>60 per transaction).
   - **CPU Time**: Transactions taking >1000ms of CPU.
   - **DML Rows**: Large DML operations (>150 rows in unit tests).

Record these in the **Runtime Telemetry** section.

### Step 4: Run LWC Jest Tests (if applicable)

If the story has LWC layers:
```bash
npx lwc-jest -- --testPathPattern [componentName] --json --outputFile .specify/logs/tests/jest-results.json
```

### Step 5: Generate Unit Test Evidence Document

Check the auto-generated evidence:
- Location: `.specify/specs/[feature-dir]/test-logs/story-$ID-verify.md`
- Template:

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
| $COMP_NAME        | LWC  | 92%         | 80%       | ✅      |

## 3. Runtime Telemetry (Observability)

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Max SOQL | 42 | 60 | ✅ |
| Max CPU | 850ms | 1000ms | ⚠️ WARN |
| Max DML | 12 | 100 | ✅ |

### Bottleneck Analysis
- **$METHOD_NAME**: High CPU usage in `calculateTotal`. Consider caching.

## 4. Performance Metrics (Legacy)

List any test method taking longer than **1.0 second**:

| Test Method | Duration | Status |
|-------------|----------|--------|
| $METHOD_NAME | 1.45s    | ⚠️ SLOW |

## 5. Security Scan Snapshot (Code Analyzer v5)

Standard scan results (PMD/ESLint):
- **Severity 1 (Critical)**: 0
- **Severity 2 (High)**: 0
- **Severity 3 (Moderate)**: X

## 6. Bulk Verification (251+ Records)

- [ ] Bulk test scenario executed for $OBJECT_NAME
- [ ] No governor limit exceptions (SOQL/DML) detected
```

### Step 6: Update Story File

Update the story file:
- Update **QA Results** or **State** section to reference the new evidence document.
- Set **State** to `VERIFIED` (Internal dev verification complete).

## Error Handling

- **Prerequisite Missing**: STOP and inform the user of the missing context.

## Next Step

Run `/speckit.sf.pr` to prepare the pull request.
