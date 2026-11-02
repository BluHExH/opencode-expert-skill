# Version History

| Date | HEX CLI | OpenCode source | Documentation state | Scope |
|---|---|---|---|---|
| 2026-11-02 | `ed3807ec2d48ffb21a093e7a50f94ba7bbf3af3c`, v1.5.1 | `ff90ed91607cabf420a369e9009539c1aa0932af` | `https://opencode.ai/docs/` current at inspection | Initial modular Skill |
| 2026-11-02 | `ed3807ec2d48ffb21a093e7a50f94ba7bbf3af3c`, v1.5.1 | `ff90ed91607cabf420a369e9009539c1aa0932af` | `https://opencode.ai/docs/skills/` current at inspection | OpenCode Expert Skill v1.1.0 hardening: frontmatter conformance, portable README, thin modules completed, validator + tests added, link audit clean |

Refresh this table before implementation whenever official behavior is version-sensitive. Do not
silently substitute a newer commit for a previously verified claim.

## Refresh procedure

1. Check official OpenCode releases.
2. Identify latest relevant changes.
3. Compare against the pinned source commit.
4. Update only affected modules.
5. Revalidate citations and source paths.
6. Update the manifest.
7. Update version history.
8. Run validation.