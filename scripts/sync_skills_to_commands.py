#!/usr/bin/env python3
"""Sync Sf Spec Kit skills into Spec Kit SF extension command format."""

from __future__ import annotations

import re
from pathlib import Path

SOURCE_SKILLS = Path("/Users/ek6504/work/opensource/Sf Spec Kit/.cursor/skills")
TARGET_ROOT = Path("/Users/ek6504/work/opensource/Spec Kit SF")
TARGET_COMMANDS = TARGET_ROOT / "commands"
TARGET_TEMPLATES = TARGET_ROOT / "templates"

SKILL_TO_COMMAND = {
    "sfspeckit-constitution": "constitution",
    "sfspeckit-specify": "specify",
    "sfspeckit-clarify": "clarify",
    "sfspeckit-plan": "plan",
    "sfspeckit-stories": "stories",
    "sfspeckit-analyze": "analyze",
    "sfspeckit-implement": "implement",
    "sfspeckit-review": "review",
    "sfspeckit-verify": "verify",
    "sfspeckit-pr": "pr",
    "sfspeckit-qa": "qa",
    "sfspeckit-uat": "uat",
    "sfspeckit-score": "score",
    "sfspeckit-deploy": "deploy",
    "sfspeckit-change": "change",
    "sfspeckit-hotfix": "hotfix",
    "sfspeckit-regression": "regression",
    "sfspeckit-release-notes": "release-notes",
}

COMMAND_DESCRIPTIONS = {
    "constitution": "Establish Salesforce project principles with 9 articles and environmental discovery.",
    "specify": "Create a Salesforce feature spec with object maps and security model.",
    "clarify": "Analyze the feature specification for gaps and edge cases with stakeholder sign-off.",
    "plan": "Create a technical plan with force-app structure and blast radius analysis.",
    "stories": "Generate Jira-ready developer stories with security matrices.",
    "analyze": "Pre-implementation analysis with mother story context and org drift detection.",
    "implement": "Implement a story file with auto-heal loop and scoring gates.",
    "review": "TPO and Architect review of generated stories before Jira creation.",
    "verify": "Generate formal Verification Evidence documents with coverage metrics.",
    "pr": "Prepare a PR with scoring gates and code review checklist.",
    "qa": "Generate manual test scripts and run automated Apex/Jest tests.",
    "uat": "Generate UAT scripts and manage business sign-offs.",
    "score": "555-point quality scoring dashboard across all stories in a feature.",
    "deploy": "Promote Salesforce code across environments (Dev to QA to UAT to Prod).",
    "change": "Impact analysis for mid-sprint requirement changes.",
    "hotfix": "Emergency production bug fix workflow with fast-track deployment.",
    "regression": "Full feature regression before release.",
    "release-notes": "Business-ready delivery summary from completed stories.",
}

COMMAND_TITLES = {
    "constitution": "Establish Salesforce Project Principles",
    "specify": "Create Salesforce Feature Specification",
    "clarify": "Fill Specification Gaps",
    "plan": "Create Technical Implementation Plan",
    "stories": "Generate Developer Story Files",
    "analyze": "Pre-Implementation Analysis",
    "implement": "Implement a Developer Story",
    "review": "Review Generated Stories",
    "verify": "Story Verification Evidence Generation",
    "pr": "Prepare Code Review",
    "qa": "QA Story Verification",
    "uat": "Business UAT Scripts and Sign-Off",
    "score": "Feature Quality Scoring Dashboard",
    "deploy": "Environment Promotion",
    "change": "Handle Mid-Sprint Requirement Changes",
    "hotfix": "Emergency Production Hotfix",
    "regression": "Feature Regression Testing",
    "release-notes": "Generate Release Notes",
}

NEXT_STEPS = {
    "constitution": "Run `/speckit.sf.specify <feature description>` to create your first specification.",
    "specify": "- **Requirement Audit**: Run `/speckit.sf.clarify` to execute the gap analysis and ensure the specification is complete.\n- **Technical Design**: Once the spec is clarified, run `/speckit.sf.plan` to create the technical implementation plan.",
    "clarify": "Run `/speckit.sf.plan` to create the technical implementation plan.",
    "plan": "This plan requires Architect review. The Architect Sign-Off section must be completed before `/speckit.sf.stories` can generate story files.",
    "stories": "Run `/speckit.sf.review` to have the Architect validate the story decomposition before creating Jira tickets.",
    "review": "Developers should run `/speckit.sf.analyze <story_file>` before `/speckit.sf.implement <story_file>`.",
    "analyze": "Analysis complete and environment is clean. Run `/speckit.sf.implement <story_file>` to begin development.",
    "implement": "Run `/speckit.sf.verify` to generate your Verification Evidence document before creating the PR.",
    "verify": "Run `/speckit.sf.pr` to prepare the pull request.",
    "pr": "PR must be approved by BOTH a Peer Developer AND the Architect before merging. After merge, run `/speckit.sf.qa` for QA verification.",
    "qa": "Technical QA PASSED. Run `/speckit.sf.uat` to begin the business sign-off process.",
    "uat": "After UAT sign-off, run `/speckit.sf.deploy prod` to promote to production.",
    "score": "If all scoring gates pass: Run `/speckit.sf.deploy qa` to promote to QA environment.",
    "regression": "If PASS: Run `/speckit.sf.score` for the full quality dashboard.",
    "setup": "Environment is ready. Run `/speckit.sf.constitution` to initialize your project principles.",
}

SUPPLEMENTAL_SECTIONS = {
    "constitution": """## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Salesforce Governance & Principles** (constitutions, architectural standards)
- **Environment Discovery** (`sf-metadata`, `sf-data`, `sf-connected-apps`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in establishing the project constitution. However, the standards in `docs/scoring.md` are the **primary source of truth**.
""",
    "specify": """## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Salesforce documentation** — official docs, feature references
- **Diagramming** — ERD, object relationship visualization

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in defining the feature specification. However, the standards in `docs/scoring.md` are the **primary source of truth**.
""",
    "plan": """## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Metadata/Objects/Relationships** (`sf-metadata`, `sf-data`, `sf-diagram-mermaid`)
- **Apex/LWC Architectural Patterns** (`sf-apex`, `sf-lwc`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in architectural planning and blast radius analysis. However, the standards in `docs/scoring.md` are the **primary source of truth**.
""",
    "stories": """## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Metadata/Story Analysis** (`sf-metadata`, `sf-data`)
- **Developer Workload Estimation** (if specialized skills exist)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in decomposing features and identifying implementation layers. However, the standards in `docs/scoring.md` are the **primary source of truth**.
""",
    "analyze": """## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Metadata Drift & Retrieval** (`sf-metadata`, `sf-deploy`)
- **Org Comparison** (`sf-data`, `sf-debug`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist drift detection and lineage analysis. However, the standards in `docs/scoring.md` are the **primary source of truth**.
""",
    "implement": """## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Foundational Salesforce Layers** (`sf-apex`, `sf-lwc`, `sf-metadata`, `sf-flow`)
- **Utility Skills** (`sf-docs`, `sf-debug`, `sf-data`, `sf-integration`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist implementation and scoring. However, the standards in `docs/scoring.md` are the **primary source of truth**.
""",
    "verify": """## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Salesforce Verification & Testing** (`sf-testing`, `sf-apex`, `sf-lwc`)
- **Observability & Logs** (`sf-debug`, `sf-agentforce-observability`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in generating verification evidence. However, the standards in `docs/scoring.md` are the **primary source of truth**.
""",
    "pr": """## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Salesforce Quality & Deployment** (`sf-apex`, `sf-lwc`, `sf-testing`, `sf-deploy`)
- **Metadata Auditing** (`sf-metadata`, `sf-permissions`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in verification and scoring. However, the standards in `docs/scoring.md` are the **primary source of truth**.
""",
    "qa": """## Supplemental Skill Discovery (Optional)

Before executing, you may check for any installed agent skills related to:
- **Salesforce QA & Testing** (`sf-testing`, `sf-apex`, `sf-lwc`)
- **Persona/Access Auditing** (`sf-permissions`, `sf-data`)

> [!NOTE]
> These skills are **Optional Accelerators**. If found, use them to assist in generating test scripts and persona coverage. However, the standards in `docs/scoring.md` are the **primary source of truth**.
""",
}

EXTENSION_CONFIG_SECTION = """## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.
"""

EXTENSION_CONFIG_WITH_SCORING = """## Extension Configuration

Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.
Use `scoring.*` thresholds if configured.
"""

COMMANDS_WITH_EXTENSION_CONFIG = {
    "clarify",
    "review",
    "verify",
    "pr",
    "qa",
    "uat",
    "score",
    "deploy",
    "regression",
    "release-notes",
    "change",
    "hotfix",
}

COMMANDS_WITH_SCORING_CONFIG = {"score"}

SKIP_SECTIONS = {
    "overview",
    "who runs this",
    "input",
    "verification evidence",
    "cross-referenced skills",
}

COMMAND_REPLACEMENTS = [
    (r"\.agents/skills/[Ss][Ff][Ss]peckit-([a-z-]+)/([a-z0-9_-]+\.md)", r".specify/templates/\2"),
    (r"\.agents/skills/[Ss][Ff][Ss]peckit-([a-z-]+)/", ".specify/templates/"),
    (r"/[Ss][Ff][Ss]peckit-constitution", "/speckit.sf.constitution"),
    (r"/[Ss][Ff][Ss]peckit-specify", "/speckit.sf.specify"),
    (r"/[Ss][Ff][Ss]peckit-clarify", "/speckit.sf.clarify"),
    (r"/[Ss][Ff][Ss]peckit-plan", "/speckit.sf.plan"),
    (r"/[Ss][Ff][Ss]peckit-stories", "/speckit.sf.stories"),
    (r"/[Ss][Ff][Ss]peckit-analyze", "/speckit.sf.analyze"),
    (r"/[Ss][Ff][Ss]peckit-implement", "/speckit.sf.implement"),
    (r"/[Ss][Ff][Ss]peckit-review", "/speckit.sf.review"),
    (r"/[Ss][Ff][Ss]peckit-verify", "/speckit.sf.verify"),
    (r"/[Ss][Ff][Ss]peckit-pr", "/speckit.sf.pr"),
    (r"/[Ss][Ff][Ss]peckit-qa", "/speckit.sf.qa"),
    (r"/[Ss][Ff][Ss]peckit-uat", "/speckit.sf.uat"),
    (r"/[Ss][Ff][Ss]peckit-score", "/speckit.sf.score"),
    (r"/[Ss][Ff][Ss]peckit-deploy", "/speckit.sf.deploy"),
    (r"/[Ss][Ff][Ss]peckit-change", "/speckit.sf.change"),
    (r"/[Ss][Ff][Ss]peckit-hotfix", "/speckit.sf.hotfix"),
    (r"/[Ss][Ff][Ss]peckit-regression", "/speckit.sf.regression"),
    (r"/[Ss][Ff][Ss]peckit-release-notes", "/speckit.sf.release-notes"),
    (r"/[Ss][Ff][Ss]peckit-setup", "/speckit.sf.setup"),
    (r"sfspeckit-data/", ".specify/"),
    (r"Read the sf-metadata skill: `\.agents/skills/sf-metadata/SKILL\.md`", "Consult the **Metadata Best Practices Checklist** in `docs/scoring.md`"),
    (r"Read the sf-apex skill: `\.agents/skills/sf-apex/SKILL\.md`", "Consult the **Apex Best Practices Checklist** in `docs/scoring.md`"),
    (r"Read the sf-flow skill: `\.agents/skills/sf-flow/SKILL\.md`", "Consult the **Flow Best Practices Checklist** in `docs/scoring.md`"),
    (r"Read the sf-lwc skill: `\.agents/skills/sf-lwc/SKILL\.md`", "Consult the **LWC Best Practices Checklist** in `docs/scoring.md`"),
    (r"1\. Read the sf-testing skill: `\.agents/skills/sf-testing/SKILL\.md`", "1. Consult the **Testing Best Practices Checklist** in `docs/scoring.md`"),
    (r"Invoke sf-metadata scoring logic \(`\.agents/skills/sf-metadata/SKILL\.md`\)", "Evaluate metadata quality using the rubric in `docs/scoring.md`"),
    (r"Invoke sf-apex scoring logic \(`\.agents/skills/sf-apex/SKILL\.md`\)", "Evaluate Apex quality using the rubric in `docs/scoring.md`"),
    (r"Invoke sf-lwc scoring logic \(`\.agents/skills/sf-lwc/SKILL\.md`\)", "Evaluate LWC quality using the rubric in `docs/scoring.md`"),
    (r"Invoke sf-testing scoring logic \(`\.agents/skills/sf-testing/SKILL\.md`\):", "Evaluate test quality using the rubric in `docs/scoring.md`:"),
    (r"Use sf-debug skill \(`\.agents/skills/sf-debug/SKILL\.md`\)", "Use optional `sf-debug` accelerator skill if available"),
    (r"Reference sf-deploy skill for Flow activation commands\.", "Activate flows using `sf project deploy start` after draft validation."),
    (r"If metadata dependencies cause issues, deploy in phases using sf-deploy skill:", "If metadata dependencies cause issues, deploy in phases:"),
    (r"\./SFSpeckit/bin/sfspeckit verify --id \$STORY_ID --target-org dev", "Run Apex and security verification commands from Step 3 in this command"),
    (r"Run the integrated verification engine:\n```bash\nRun Apex and security verification commands from Step 3 in this command\n```", "Run Apex tests and security scans using the commands in Step 3."),
    (r"1\. \*\*Spectrum Engine Log\*\*:.*\n", ""),
    (r"2\. \*\*Evidence File\*\*: Traceability maintained in sfspeckit-data/\n", ""),
    (r"2\. \*\*Evidence File\*\*: Traceability maintained in \.specify/\n", ""),
    (r"- \*\*CLI Failure\*\*: Report the specific Spectrum Engine error code\.\n", ""),
    (r"sf plugins install @salesforce/sfdx-scanner", "sf plugins install code-analyzer"),
    (r"sf scanner run", "sf code-analyzer run"),
    (r"sf plugins inspect @salesforce/sfdx-scanner", "sf plugins inspect code-analyzer"),
    (r"All SFSpeckit skills will reference", "All SFSpeckit commands will reference"),
    (r"before running `/speckit\.sf\.implement`", "before running `/speckit.sf.analyze` and `/speckit.sf.implement`"),
    (r"Install and rerun this skill\.", "Install and rerun this command."),
    (r"rerun this skill\.", "rerun this command."),
]

VERIFY_STEP_3 = """### Step 3: Run Apex Tests & Security Scans

```bash
sf apex run test \\
  --class-names [Class1Test,Class2Test] \\
  --code-coverage \\
  --result-format json \\
  --output-dir .specify/logs/tests \\
  --target-org dev
```

Run Code Analyzer v5 security snapshot:
```bash
sf code-analyzer run --path "force-app/" --engine pmd,eslint
```"""

TEMPLATE_FILES = [
    ("sfspeckit-constitution/constitution-template.md", "constitution-template.md"),
    ("sfspeckit-specify/spec-template.md", "spec-template.md"),
    ("sfspeckit-plan/plan-template.md", "plan-template.md"),
    ("sfspeckit-stories/story-template.md", "story-template.md"),
    ("sfspeckit-clarify/clarify-template.md", "clarify-template.md"),
    ("sfspeckit-clarify/clarification-report-template.md", "clarification-report-template.md"),
    ("sfspeckit-qa/test-scripts-template.md", "test-scripts-template.md"),
    ("sfspeckit-uat/uat-script-template.md", "uat-script-template.md"),
    ("sfspeckit-hotfix/hotfix-template.md", "hotfix-template.md"),
]


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    frontmatter = text[4:end]
    body = text[end + 5 :]
    meta: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    return meta, body


def apply_replacements(text: str) -> str:
    for pattern, replacement in COMMAND_REPLACEMENTS:
        text = re.sub(pattern, replacement, text)
    return text


def extract_sections(body: str) -> list[tuple[str, str]]:
    lines = body.splitlines()
    sections: list[tuple[str, str]] = []
    current_title = ""
    current_lines: list[str] = []

    for line in lines:
        if line.startswith("## "):
            if current_title or current_lines:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_title or current_lines:
        sections.append((current_title, "\n".join(current_lines).strip()))
    return sections


def convert_skill_body(body: str) -> str:
    body = apply_replacements(body)
    sections = extract_sections(body)
    kept: list[str] = []

    for title, content in sections:
        normalized = title.lower()
        if normalized in SKIP_SECTIONS:
            continue
        if normalized.startswith("verification evidence"):
            continue
        if normalized == "steps":
            kept.append(("Instructions", content))
            continue
        if normalized == "":
            continue
        kept.append((title, content))

    # Remove generic output boilerplate when it's only spectrum placeholders
    filtered: list[tuple[str, str]] = []
    for title, content in kept:
        if title.lower() == "output" and "Updated Metadata: [list affected files]" in content:
            continue
        filtered.append((title, content))

    parts = []
    seen_titles: set[str] = set()
    for title, content in filtered:
        key = title.lower()
        if key in seen_titles:
            if content:
                parts.append(content)
            continue
        seen_titles.add(key)
        if not content:
            parts.append(f"## {title}")
        else:
            parts.append(f"## {title}\n\n{content}")
    return "\n\n".join(parts).strip()


def build_command(command: str, skill_text: str) -> str:
    meta, body = parse_frontmatter(skill_text)
    description = COMMAND_DESCRIPTIONS.get(command, meta.get("description", ""))
    title = COMMAND_TITLES.get(command, command.replace("-", " ").title())
    converted_body = convert_skill_body(body)

  # Ensure prerequisites/implement sections use extension paths in constitution step 4
    if command == "constitution":
        converted_body = converted_body.replace(
            "1. Copy `.specify/templates/constitution-template.md` to `.specify/memory/constitution.md`",
            "1. Create `.specify/memory/constitution.md` from `.specify/templates/constitution-template.md`",
        )

    if command == "verify":
        converted_body = re.sub(
            r"### Step 3: Run Unit Tests & Security Scans\n\n(?:Run the integrated verification engine:\n```bash\n.*?\n```|Run Apex tests and security scans using the commands in Step 3\.)",
            VERIFY_STEP_3,
            converted_body,
            flags=re.S,
        )
        converted_body = converted_body.replace(
            "- Location: `.specify/specs/[feature-dir]/verification-evidence.md`",
            "- Location: `.specify/specs/[feature-dir]/test-logs/story-$ID-verify.md`",
        )
        converted_body = converted_body.replace("### Step 5: Review Generated Evidence", "### Step 5: Generate Unit Test Evidence Document")
        converted_body = converted_body.replace("### Step 6: Final Git Commit and Update Story", "### Step 6: Update Story File")
        converted_body = re.sub(
            r"Only after verification passes and the evidence document is generated:\n\n1\. \*\*Commit and Push\*\*:.*?\n```\n\n2\. \*\*Update Story File\*\*:",
            "Update the story file:",
            converted_body,
            flags=re.S,
        )

    parts = [
        "---",
        f'description: "{description}"',
        "---",
        "",
        f"# {title}",
        "",
        "## User Input",
        "",
        "$ARGUMENTS",
        "",
    ]

    if command in SUPPLEMENTAL_SECTIONS:
        parts.append(SUPPLEMENTAL_SECTIONS[command].rstrip())
        parts.append("")

    if command in COMMANDS_WITH_EXTENSION_CONFIG:
        if command in COMMANDS_WITH_SCORING_CONFIG:
            parts.append(EXTENSION_CONFIG_WITH_SCORING.rstrip())
        else:
            parts.append(EXTENSION_CONFIG_SECTION.rstrip())
        parts.append("")

    if command == "implement":
        parts.append("## Extension Configuration")
        parts.append("")
        parts.append("Load extension config from `.specify/extensions/sf/sf-config.yml` if it exists.")
        parts.append("")

    parts.append(converted_body)

    if command in NEXT_STEPS:
        parts.extend(["", "## Next Step", "", NEXT_STEPS[command]])

    return "\n".join(parts).rstrip() + "\n"


def sync_templates() -> None:
    TARGET_TEMPLATES.mkdir(parents=True, exist_ok=True)
    for source_rel, target_name in TEMPLATE_FILES:
        source = SOURCE_SKILLS / source_rel
        if not source.exists():
            continue
        content = apply_replacements(source.read_text())
        (TARGET_TEMPLATES / target_name).write_text(content)


def update_setup() -> None:
    setup_path = TARGET_COMMANDS / "setup.md"
    content = setup_path.read_text()
    content = content.replace(
        "### Step 4: Check SF Code Analyzer (`sf-scanner`)\n\n1. Run: `sf plugins inspect @salesforce/sfdx-scanner`\n2. If found: Report version. Ensure version is ≥ 5.0.0 for PMD 7 support.\n3. If NOT found or version is < 5.0.0:\n   - Suggest: `sf plugins install @salesforce/sfdx-scanner@latest`\n   - Ask for permission to run the install command.",
        "### Step 4: Check SF Code Analyzer (`code-analyzer`)\n\n1. Run: `sf plugins inspect code-analyzer`\n2. If found: Report version. Ensure version is ≥ 5.0.0 for PMD 7 support.\n3. If NOT found or version is < 5.0.0:\n   - Suggest: `sf plugins install code-analyzer`\n   - Ask for permission to run the install command.",
    )
    setup_path.write_text(content)


def main() -> None:
    for skill_name, command in SKILL_TO_COMMAND.items():
        skill_path = SOURCE_SKILLS / skill_name / "SKILL.md"
        if not skill_path.exists():
            print(f"SKIP missing skill: {skill_name}")
            continue
        command_text = build_command(command, skill_path.read_text())
        out_path = TARGET_COMMANDS / f"{command}.md"
        out_path.write_text(command_text)
        print(f"Updated {out_path.name}")

    sync_templates()
    print(f"Synced {len(TEMPLATE_FILES)} templates")
    update_setup()
    print("Updated setup.md")


if __name__ == "__main__":
    main()
