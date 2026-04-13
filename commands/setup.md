---
description: "Automated dependency checker and installer (sf, gh, sf-scanner)."
---

# Environment Setup

## User Input

$ARGUMENTS

## Instructions

Analyze the environment and install missing dependencies for SFSpeckit.

### Step 1: Detect Operating System

Identify whether the user is on **macOS**, **Windows**, or **Linux**.

### Step 2: Check Salesforce CLI (`sf`)

1. Run: `sf version`
2. If found: Report version.
3. If NOT found:
   - **macOS**: Suggest `brew install --cask salesforce-cli`
   - **Windows**: Suggest `winget install Salesforce.SalesforceCLI` or `npm install --global @salesforce/cli`
   - Ask for permission to run the install command.

### Step 3: Check GitHub CLI (`gh`)

1. Run: `gh --version`
2. If found: Report version.
3. If NOT found:
   - **macOS**: Suggest `brew install gh`
   - **Windows**: Suggest `winget install GitHub.cli`
   - Ask for permission to run the install command.

### Step 4: Check SF Code Analyzer (`sf-scanner`)

1. Run: `sf plugins inspect @salesforce/sfdx-scanner`
2. If found: Report version. Ensure version is ≥ 5.0.0 for PMD 7 support.
3. If NOT found or version is < 5.0.0:
   - Suggest: `sf plugins install @salesforce/sfdx-scanner@latest`
   - Ask for permission to run the install command.

### Step 5: Verify Permissions & Login

1. Check if user is authenticated to any org: `sf org list`
2. If no orgs found:
   - Provide instruction: `sf org login web --alias dev`

### Step 6: Summary Report

Generate a status table:

| Tool | Status | Version | Action Taken |
|------|--------|---------|--------------|
| Salesforce CLI | ✅ / ❌ | X.X.X | [Installed/None] |
| GitHub CLI | ✅ / ❌ | X.X.X | [Installed/None] |
| Code Analyzer | ✅ / ❌ | X.X.X | [Updated/None] |

## Next Step

Environment is ready. Run `/speckit.sf.constitution` to initialize your project principles.

## Output

- **Status Table**: Final state of all dependencies.
- **Confirmation**: Final readiness check for SFSpeckit commands.
