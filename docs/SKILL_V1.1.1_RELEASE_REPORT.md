# OpenCode Expert Skill v1.1.1 Release Report

## Summary
Phase 3 applied Phase 2 source-audit corrections and validator portability hardening.

## Pinned OpenCode source
`ff90ed91607cabf420a369e9009539c1aa0932af` (unchanged)

## Documentation corrections
- `architecture/agent-lifecycle.md`: prompt path → `packages/core/src/session/prompt.ts`
- `references/03-agent-runtime.md`: same path clarification
- `references/19-mcp-integration.md`: HTTP `StreamableHTTPClientTransport` SOURCE VERIFIED; lifecycle PARTIAL
- `hex-mapping/feature-parity-matrix.md`: MCP HTTP row updated
- `sources/source-code-map.md`, `sources/source-manifest.json`: MCP HTTP notes
- LSP/server PARTIAL statuses preserved

## Validator
- Directory name vs skill name: ERROR only under `skills/` parent; INFO for repo clones
- Tests added for mismatched clone names and skills/ layout

## Out of scope
HEX CLI application code was not modified.
