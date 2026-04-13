# Migrating from Standalone SFSpeckit

This guide helps existing SFSpeckit users (agent skills version) migrate to the Spec Kit extension.

## What Changed

| Aspect | Standalone (Agent Skills) | Extension (Spec Kit) |
|--------|--------------------------|---------------------|
| **Installation** | Copy `.agents/skills/sfspeckit-*` folders | `specify extension add sf` |
| **Commands** | `/SFSpeckit-specify`, `/SFSpeckit-plan` | `/speckit.sf.specify`, `/speckit.sf.plan` |
| **Data directory** | `sfspeckit-data/` | `.specify/` |
| **Templates** | `sfspeckit-data/templates/` | `.specify/templates/` |
| **Constitution** | `sfspeckit-data/memory/constitution.md` | `.specify/memory/constitution.md` |
| **Feature specs** | `sfspeckit-data/specs/NNN-*/` | `.specify/specs/NNN-*/` |
| **Config** | None (inline in SKILL.md) | `.specify/extensions/sf/sf-config.yml` |
| **Updates** | `git pull` | `specify extension update sf` |
| **Skill references** | Hardcoded `.agents/skills/sf-*/SKILL.md` | Dynamic discovery |

## Migration Steps

### Step 1: Install the Extension

```bash
# Ensure spec-kit is installed
uv tool install specify-cli

# Initialize your project (if not already)
specify init . --ai claude

# Install the extension
specify extension add sf --from https://github.com/ysumanth06/spec-kit-sf/archive/refs/tags/v1.0.0.zip
```

### Step 2: Move Your Data

If you have existing `sfspeckit-data/` content:

```bash
# Move constitution
cp sfspeckit-data/memory/constitution.md .specify/memory/constitution.md

# Move specs
cp -r sfspeckit-data/specs/ .specify/specs/

# Move templates (optional — extension provides defaults)
cp sfspeckit-data/templates/ .specify/templates/
```

### Step 3: Update Paths in Existing Files

If you have existing spec, plan, or story files with `sfspeckit-data/` references:

```bash
# Find and replace paths (review before applying)
grep -r "sfspeckit-data/" .specify/specs/ --include="*.md" -l
```

Replace:
- `sfspeckit-data/memory/` → `.specify/memory/`
- `sfspeckit-data/specs/` → `.specify/specs/`
- `sfspeckit-data/templates/` → `.specify/templates/`

### Step 4: Update Command References

In any existing documentation or story files that reference old commands:

| Old Command | New Command |
|-------------|-------------|
| `/SFSpeckit-constitution` | `/speckit.sf.constitution` |
| `/SFSpeckit-specify` | `/speckit.sf.specify` |
| `/SFSpeckit-clarify` | `/speckit.sf.clarify` |
| `/SFSpeckit-plan` | `/speckit.sf.plan` |
| `/SFSpeckit-stories` | `/speckit.sf.stories` |
| `/SFSpeckit-review` | `/speckit.sf.review` |
| `/SFSpeckit-implement` | `/speckit.sf.implement` |
| `/SFSpeckit-change` | `/speckit.sf.change` |
| `/SFSpeckit-qa` | `/speckit.sf.qa` |
| `/SFSpeckit-pr` | `/speckit.sf.pr` |
| `/SFSpeckit-verify` | `/speckit.sf.verify` |
| `/SFSpeckit-deploy` | `/speckit.sf.deploy` |
| `/SFSpeckit-score` | `/speckit.sf.score` |
| `/SFSpeckit-hotfix` | `/speckit.sf.hotfix` |
| `/SFSpeckit-regression` | `/speckit.sf.regression` |
| `/SFSpeckit-release-notes` | `/speckit.sf.release-notes` |
| `/SFSpeckit-uat` | `/speckit.sf.uat` |

### Step 5: Configure the Extension

```bash
cp .specify/extensions/sf/sf-config.template.yml \
   .specify/extensions/sf/sf-config.yml
```

Edit `sf-config.yml` with your org aliases and scoring thresholds.

### Step 6: Remove Standalone Skills (Optional)

Once you've verified the extension works:

```bash
# Remove standalone agent skills
rm -rf .agents/skills/sfspeckit-*

# Keep foundational SF skills — they work alongside the extension
# .agents/skills/sf-apex, sf-lwc, sf-metadata, etc.
```

## FAQ

### Can I use both standalone and extension simultaneously?
Yes, but it may cause confusion with duplicate commands. The extension is recommended as the primary interface.

### What about my foundational SF skills (sf-apex, sf-lwc, etc.)?
Keep them! The extension's dynamic discovery feature will automatically detect and use them.

### Do I need to re-run constitution?
Not if you migrated the file. The extension reads from `.specify/memory/constitution.md` — same format, different path.

### What if I have in-progress features?
Complete them using the current tool, then start new features with the extension. Migration mid-feature is possible but not recommended.
