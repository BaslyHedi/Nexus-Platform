# Claude Code skills

Skills used by Claude Code across the Nexus repositories. They hold process, not product: how work is reviewed and taught. One folder per skill.

| Skill | Does |
|---|---|
| [`learn-review/`](learn-review/SKILL.md) | Reviews Hedi's changes on a branch as a coach: explains the build errors, gives hints instead of fixes, and introduces one new concept at a time from a ladder per language |

## Installing

Every Nexus repository ignores `.claude/` (global gitignore), so a skill is not copied into each repository. It is linked once into the user's skills, from where every repository sees it:

```bash
ln -s ~/work/Nexus-Platform/tools/claude-skills/learn-review ~/.claude/skills/learn-review
```

A change to a skill or a ladder is then a change in this repository, on a branch, like any other.
