# OpenCode Expert Skill — v1.1.0 Hardening Report

## Scope

- Skill directory: `D:\skills\opencode-expert`
- Version under test: v1.1.0
- Inspection date: 2026-11-02

## Files changed

- `SKILL.md` — frontmatter updated to verified OpenCode Agent Skills specification (added supported optional field `compatibility: opencode`; retained required `name` and `description`).
- `README.md` — rewritten to be provider-neutral and portable.
- `CHANGELOG.md` — added v1.1.0 entry.
- `references/version-history.md` — added v1.1.0 row and refresh procedure.
- `references/24-server-api.md` — completed thin module structure and gaps.
- `references/21-plugin-system.md` — completed thin module structure and gaps.
- `references/19-mcp-integration.md` — added MCP HTTP / remote transport status section.
- `references/20-lsp-integration.md` — added verification checklist and status clarity.
- `references/11-context-management.md` — added compaction research gaps.
- `scripts/validate_skill.py` — new local validator.
- `scripts/tests/test_validate_skill.py` — new validator tests.
- `docs/` — this hardening report.

## Frontmatter specification used

Authoritative source: OpenCode Agent Skills documentation (`https://opencode.ai/docs/skills/`), inspected 2026-11-02.

- Required fields: `name`, `description`.
- Optional fields: `license`, `compatibility`, `metadata` (string-to-string map).
- Unknown frontmatter fields are ignored by OpenCode; OpenCode 1 does not use `metadata` to control slash commands or automatic skill selection.
- `name` constraints: 1-64 characters; lowercase alphanumeric with single hyphen separators; no leading/trailing hyphen; no consecutive hyphens; must match containing directory name; regex `^[a-z0-9]+(-[a-z0-9]+)*$`.
- `description` constraints: 1-1024 characters; specific enough for agent selection.

Findings for `opencode-expert`:

- `name: opencode-expert` conforms.
- `description` length within 1-1024; content suitable for selection.
- Added supported optional field: `compatibility: opencode`.
- `version` and `allowed-tools` are not supported frontmatter fields for this specification; they were not added.

## Research improvements

- Thin modules completed with evidence status, gaps, verification checklists, and HEX implications preserved.

## Validation tooling

- `python scripts/validate_skill.py` — checks frontmatter, required files, source manifest JSON, markdown links, mermaid fences.
- `python scripts/tests/test_validate_skill.py` — 8 tests.

## Link audit results

- Full internal markdown link check run across the skill directory.
- No broken internal links found.

## Tests

- Validator tests: 8/8 OK.

## Remaining limitations

- Server API, MCP HTTP, LSP runtime, and context compaction details remain partially or unverified; they are explicitly marked and should be re-verified against newer source pins.
- No network-based validation in ordinary local runs.

## Final acceptance criteria status

- Existing research preserved: yes (no substantial research deleted; only thin modules structured).
- Frontmatter specification verified: yes.
- README made portable: yes.
- Thin modules improved or honestly deferred: yes.
- Automated validator implemented: yes.
- Internal links audited: yes.
- Source manifest valid: yes.
- Research maintenance documented: yes.
- Skill version updated to v1.1.0: yes (documentation version; no application version change).
- Final hardening report created: yes.
- Git status and delivery accurately reported: pending final step.