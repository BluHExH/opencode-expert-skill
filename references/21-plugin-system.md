# Plugin System

## Overview

OpenCode has core plugin services and package integrations under `packages/core/src/plugin/**` and `packages/plugin/**`.

## Likely responsibilities to verify per version

- Plugin discovery/load.
- Lifecycle initialization.
- Hooks/events.
- Extension registration.
- Configuration.
- Compatibility and permission boundaries.
- Error and unload handling.

## Source status

Core/plugin paths are source verified at repository level; exact hook names and signatures must be read from the pinned revision before documentation or implementation.

## Evidence gaps

- Exact registration, lifecycle, hook/event contracts, and configuration schema were not fully read in the pinned inspection pass.
- Plugins must not be confused with MCP servers or skills; they are separate extension mechanisms.

## HEX implications

No equivalent production plugin system exists in the HEX baseline. Prefer an explicit Python entry point contract with allow-listing and isolated failures rather than dynamic unreviewed loading.

## Verification checklist for future passes

- Read pinned plugin service and package integration source paths.
- Document hook names and signatures from source, not assumption.
- Define permission boundaries for plugin-contributed tools or actions.
