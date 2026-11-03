# MCP Integration

## Overview

OpenCode's MCP service is under `packages/core/src/mcp/**`, with server handlers and protocol definitions.

## Lifecycle

- Load server configuration.
- Start/transport-connect.
- Authenticate where applicable.
- Initialize protocol.
- Discover tools/resources/prompts.
- Register tools in tool runtime.
- Handle calls/errors/reconnects.
- Disconnect and clean up.

## Source areas

`packages/core/src/mcp/index.ts`, `connection.ts`, `client.ts`, `stdio.ts`, `socket-client.ts`, `oauth.ts`, and server/protocol handlers.

## Evidence status

- MCP service structure inspected at pinned commit `ff90ed91607cabf420a369e9009539c1aa0932af`; inspected 2026-11-02.
- `hex_cli/mcp/client.py` has stdio sessions and tool listing/calling in the HEX baseline.

## MCP HTTP / remote transport

**Evidence (pinned commit `ff90ed91607cabf420a369e9009539c1aa0932af`):** `SOURCE VERIFIED` for client transport construction.

- `packages/core/src/mcp/client.ts` imports and constructs `StreamableHTTPClientTransport` for non-local MCP configs.
- Local servers use `McpStdio.make` when `config.type === "local"`.
- An `attached` mode reuses a caller-supplied transport.
- HTTP session expiry / `SdkHttpError` handling and `terminateSession` paths exist in the same module.

**Still PARTIAL (do not over-claim):**

- Full production auth flows, every remote server flavor, and end-to-end reconnection under all failure modes were not exhaustively proven in Phase 2.
- Treat lifecycle edge cases as PARTIAL until covered by targeted tests against live servers.


## HEX implications

`hex_cli/mcp/client.py` has stdio sessions and tool listing/calling, but HTTP servers and model-loop integration are missing. Start with process lifecycle, credentials, timeout, tool schema conversion, and permission tests.
