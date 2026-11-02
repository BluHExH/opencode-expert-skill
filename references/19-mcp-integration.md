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

- Whether a remote HTTP MCP transport is supported in the pinned OpenCode version is not established from the pinned source inspection.
- Treat HTTP transport support as unverified until source inspection confirms it; do not label a transport missing without source evidence.

## HEX implications

`hex_cli/mcp/client.py` has stdio sessions and tool listing/calling, but HTTP servers and model-loop integration are missing. Start with process lifecycle, credentials, timeout, tool schema conversion, and permission tests.
