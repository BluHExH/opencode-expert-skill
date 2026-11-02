# OpenCode Expert

OpenCode Expert is a source-grounded knowledge base for HEX CLI engineering. It explains OpenCode's architecture and behavior at a versioned level, and turns those findings into native, compatible implementation guidance for HEX CLI.

OpenCode is a technical reference, not HEX CLI's identity. HEX CLI remains HEX / NeonBuild: retain its Python + Textual implementation, branding, commands, configuration compatibility, and user-facing behavior.

## What problems it solves

- Answer how OpenCode subsystems work — agent runtime, tools, permissions, sessions, storage, streaming, context, providers, models, TUI, commands, diffs/snapshots, MCP, LSP, plugins, skills, configuration, server API, Git, errors, security — with cited, source-verified evidence instead of guesswork.
- Decide which OpenCode behaviors are worth porting into HEX CLI and which must stay native.
- Maintain a feature parity view with explicit gaps, risks, and recommendations.
- Produce native implementation plans with regression and security risks, without copying OpenCode source wholesale.

## Directory structure

- `SKILL.md` — entry point: purpose, mandatory workflow, evidence policy, navigation, glossary.
- `references/` — deep dives, one per OpenCode system module (`01-opencode-overview.md` … `28-testing-strategy.md`).
- `architecture/` — original Mermaid diagrams (system, agent/session/tool/lifecycle flows, TUI rendering).
- `hex-mapping/` — HEX architecture mapping, feature parity matrix, implementation roadmap, compatibility guide.
- `sources/` — official documentation index, source code map, source manifest, version history.
- `scripts/` — local validation tooling (`validate_skill.py`).
- `docs/` — delivery artifacts such as hardening reports.

## Loading the Skill

### Native loading (verified where possible)

OpenCode discovers Agent Skills from project or global locations:

- Project: `.opencode/skills/<name>/SKILL.md`, `.claude/skills/<name>/SKILL.md`, `.agents/skills/<name>/SKILL.md`
- Global: `~/.config/opencode/skills/<name>/SKILL.md`, `~/.claude/skills/<name>/SKILL.md`, `~/.agents/skills/<name>/SKILL.md`

For project-local skills, OpenCode walks up from the current working directory until the git worktree. Skills load on demand via the native `skill` tool; agents see available skills through the `<available_skills>` block in the tool description and load one via `skill({ name })`.

Access is controlled by pattern-based permissions (`permission.skill` in `opencode.json` with `allow` / `deny` / `ask` and wildcard patterns such as `internal-*`). Access can also be disabled per agent.

Behavior may change between OpenCode versions; re-check official documentation before relying on discovery details.

### Manual loading (fallback)

If the host agent does not support native skill loading, use this manual workflow:

1. Provide `SKILL.md` and the relevant reference files.
2. Ask the agent to follow the mandatory workflow in `SKILL.md`.
3. Require source links and commit/release citations for behavior that can change.
4. Ask the agent to inspect the current HEX implementation before proposing changes.
5. Ask the agent to update the relevant reference and parity row after implementation.

## Verifying that references were used

- Ask the agent to name the specific reference files it loaded for the task.
- Require citations: source paths, commit/release, evidence level.
- Treat answers that skip the references as incomplete.

## Updating and maintaining the knowledge base

1. Record the date, OpenCode release/tag or commit, and documentation URLs.
2. Inspect official documentation and source at the pinned revision.
3. Update or add `sources/source-manifest.json` entries.
4. Revise modules from source, not documentation alone.
5. Re-run `python scripts/validate_skill.py`.
6. Update `references/version-history.md` and `CHANGELOG.md`.
7. Refresh affected feature parity rows.

### Refresh procedure

1. Check official OpenCode releases.
2. Identify latest relevant changes.
3. Compare against the pinned source commit.
4. Update only affected modules.
5. Revalidate citations and source paths.
6. Update the manifest.
7. Update version history.
8. Run validation.

Do not automatically change the pinned commit without reviewing the differences. Keep historical research traceable.

## Evidence levels

- `DOCUMENTED` — stated in official documentation.
- `SOURCE VERIFIED` — inspected in a pinned official source revision.
- `PARTIAL` — evidence exists but details remain incomplete.
- `UNVERIFIED` — no sufficient evidence; do not use as implemented fact.

## Provider independence

The Skill itself is provider-neutral and must not depend on one AI provider. Provider-specific usage examples may exist separately; the core workflow and evidence policy apply across hosts.
