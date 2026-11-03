# Changelog

## 2026-11-03 — OpenCode Expert Skill v1.1.1

### Fixed
- Corrected agent prompt module path: `packages/core/src/session/prompt.ts` (not `session/runner/prompt.ts`).
- MCP HTTP: documented `StreamableHTTPClientTransport` as SOURCE VERIFIED at pin `ff90ed9…`; lifecycle edge cases remain PARTIAL.
- Validator: repository clone directory may differ from skill `name`; strict name/folder match only under a `skills/` parent install layout.

### Changed
- Updated MCP reference, parity matrix, source-code-map, and source-manifest notes from Phase 2 audit.
- Extended validator tests for alternate clone directory names.

### Unchanged
- Pinned OpenCode source remains `ff90ed91607cabf420a369e9009539c1aa0932af`.
- LSP runtime remains PARTIAL/UNVERIFIED; server API request map remains PARTIAL.

## 2026-11-02 — OpenCode Expert Skill v1.1.0

### Added

- Local validation tooling: `scripts/validate_skill.py`.
- Validator test suite: `scripts/tests/test_validate_skill.py`.
- Hardening report: `docs/SKILL_V1.1.0_HARDENING_REPORT.md`.

### Changed

- `SKILL.md` frontmatter updated to the verified OpenCode Agent Skills specification:
  required `name` and `description` retained; supported optional `compatibility: opencode`
  added. Unsupported fields (`version`, `allowed-tools`) were intentionally not added.

### Research

- Completed thin research module improvements for Server API, Plugins, MCP HTTP, LSP, and
  Context Compaction while preserving existing evidence levels and marking unverified details.

### Validation

- `python scripts/validate_skill.py` -> PASS (0 errors, 0 warnings, 0 info).
- `python scripts/tests/test_validate_skill.py` -> 8/8 OK.

## 2026-11-02 — Initial research baseline

- Added the initial OpenCode Expert Skill.
- Pinned initial source inspection to OpenCode commit
  `ff90ed91607cabf420a369e9009539c1aa0932af`.
- Verified HEX baseline as commit
  `ed3807ec2d48ffb21a093e7a50f94ba7bbf3af3c`.