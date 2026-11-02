# Server API

## Overview

Typed server protocol groups are under `packages/protocol/src/groups/**`, while handlers are in `packages/server/src/handlers/**`.

## Evidence status

- OpenCode pinned commit: `ff90ed91607cabf420a369e9009539c1aa0932af`; inspected 2026-11-02.
- HEX CLI pinned baseline: `ed3807ec2d48ffb21a093e7a50f94ba7bbf3af3c` (v1.5.1).

## Verified patterns

- Session, command, config, MCP, skill, and VCS handler groups.
- Shared protocol routes consumed by clients.
- Server event streams must be audited per exact route and version.

## Research gaps

- The durable server API surface, implemented endpoint inventory, request/response schemas, event streaming semantics, authentication, and error handling were not fully source-verified in the pinned snapshot.
- Exact handler coverage and protocol group boundaries should be confirmed against the pinned source before implementation decisions are recorded as facts.

## Verification checklist for future passes

- Enumerate protocol groups and routes at the pinned commit.
- Audit event stream routes for ordering, replay, auth, and error semantics.
- Confirm typed error response shapes and redaction behavior.

## HEX implications

HEX has no equivalent durable server API or HTTP event service. Do not implement parity solely because core services share concepts; define requirements and native Python API boundaries.
