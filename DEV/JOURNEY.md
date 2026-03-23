# Journey Log

> Where we are in building Open Systems. For humans and agents to regain context.

## Source of Truth

- **Specs**: [SPECS/INDEX.md](../SPECS/INDEX.md) — formal specifications
- **Decisions**: [DEV/docs/decisions/](docs/decisions/) — architectural decisions (001-009)
- **Brainstorms**: [DEV/docs/brainstorm/](docs/brainstorm/) — design explorations (001-014)
- **Roadmap**: [DEV/docs/roadmap.md](docs/roadmap.md) — slice-based implementation plan
- **Chain dev notes**: [chain-dev.md](../../.claude/projects/-data-Dev-Open-Systems/memory/chain-dev.md) — implementation details
- **Glossary**: [SPECS/GLOSSARY.md](../SPECS/GLOSSARY.md) — terminology

Read those first. This doc tracks **implementation progress and pivots**.

---

## Current Status: Community-Governed Development

10 contracts deployed on sovereign Cosmos SDK appchain. os-git CLI bridges git workflows to on-chain governance. The system dogfoods itself — code changes go through community voting with XP-weighted quorum.

**Chain**: 10 CosmWasm contracts, 197 tests (135 unit + 62 e2e), zero clippy warnings.

**Tooling**: 75 MCP tools, os-git CLI (11 commands), web explorer (10 tabs), Rust vault daemon.

**Infrastructure**: Chain node + vault daemon running as systemd services. Auto-restart on crash/hibernation.

**Seeded state**: 3 subjects, 3 users with XP, 2 projects (1 released/community-governed), 9+ contributions, full lifecycle verified.

### What's Built

| Component | Status | Details |
|-----------|--------|---------|
| Chain scaffold | Done | Cosmos SDK v0.53.6, CometBFT, CosmWasm v0.61.8 |
| Subject registry | Done | 5 unit + 8 e2e tests |
| Experience system | Done | 14 unit tests, non-transferable XP, lock/unlock/burn |
| Forum | Done | 26 unit + 11 e2e, posts with review period + upvoting |
| Auditing | Done | 5 unit + 18 e2e, commit-reveal blind voting, appeals |
| Projects | Done | 10 unit + 22 e2e, incubator model, **XP-weighted voting, quorum, staking** |
| Governance | Done | 6 unit + 11 e2e, executable proposals, x/upgrade |
| Build sovereignty | Done | 15 unit + 6 e2e, build specs, builder registry, artifact verify |
| Expression | Done | 53 unit tests, 3 governance tracks, observation lifecycle |
| MCP server | Done | 75 tools, Python + FastMCP |
| Vault (Python) | Deprecated | Replaced by Rust vault daemon |
| Vault (Rust) | Done | 18 tests, libp2p + Axum, systemd service |
| Web explorer | Done | 10 tabs, dark theme, all data visible |
| os-git CLI | Done | 11 commands, canonical diff hashing, vault integration |
| Redeploy scripts | Done | deploy-all.sh for incremental deployment |

---

## Session: Chain Scaffold & First Contracts (2026-03-07)

Started the project. The key decision was **Decision 001: Cosmos SDK** — build a sovereign appchain from day one instead of deploying on Solana or Ethereum L2. No migration needed; the bootstrap chain IS the real chain.

Scaffolded the chain with Ignite CLI. Configured PoA with a single validator for bootstrap. Set up zero-fee transactions (we control gas prices). The chain binary (`opensystemsd`) was up and running by end of session.

Also made **Decision 003: Content Discovery** — Nostr-inspired relay model on libp2p with Kademlia DHT + GossipSub. Content is self-hosted; chain stores hashes only.

And **Decision 004: Project-Level Governance First** — build the Projects + Contributions contracts before the global constitution. Bottom-up: extract global rules from real usage patterns, don't speculate.

**Commits**: `d410884` (Ignite scaffold)

---

## Session: CometBFT Patch & Contract Foundation (2026-03-08)

Patched CometBFT v0.38.21 to fix idle CPU on the dev node (`create_empty_blocks=false` was causing a busy-wait loop). The patch was upstreamed.

Started designing the incubator ownership model (Brainstorm 006) — projects start creator-driven, transition to community governance via irreversible release. This pattern became foundational for everything that followed.

**Commits**: `51a45a8` (CometBFT patch)

---

## Session: The Big Build (2026-03-09)

The most productive day. Built and deployed 9 contracts in a single session:

**Contracts built**: subject, experience, forum, auditing, projects, governance, build-spec, builder-registry, artifact-verify. All with unit tests, all deployed to the chain, all wired with cross-contract caller registrations.

**Key technical discoveries**:
- `cw_serde` adds `deny_unknown_fields` — cross-contract response types must include ALL fields from the source struct
- `start_after: 0` skips ID 0 in pagination — use `null` for initial queries
- Block time only advances with transactions when `create_empty_blocks=false`

**MCP server**: Built Python + FastMCP server with 51 tools for chain interaction. Claude Code integration via `.mcp.json`.

**Vault v0**: Python content-addressed store with git-style `hash[:2]/hash[2:]` layout. SHA-256 keyed, integrity verification on read.

**Web explorer**: Single-page dark-themed app with Overview, Subjects, Forum, Projects, Governance tabs. Real-time chain queries via Python backend.

**Admin dissolution**: All 6 original contracts had admin set to null, CosmWasm admin transferred to governance contract. System became self-governing.

**x/upgrade**: Live tested — governance proposal → ScheduleUpgrade → plan registered on chain. The community can upgrade the chain binary itself.

**Build sovereignty**: Build specs, builder registry, artifact verification. The community controls the entire build pipeline — from source to binary.

**Refactor pass**: Extracted admin helpers to shared `os_types::admin` module, created shared Python CLI library (`lib/cli.py`), standardized storage keys, added shared test helpers. Grade: A-.

**Auditing lifecycle verified**: 3 cases tested — fast-track approval (4 PASS), instant rejection (2 REJECT), successful appeal (excluded auditors + fresh panel). Bug found and fixed: `reveal_deadline` not reset at commit→reveal transition.

**Seeded state**: 4 subjects, 7 forum posts, 2 governance proposals (both executed), 2 projects with 3 contributions, build sovereignty data, admin dissolution on all 9 contracts.

134 tests passing at end of session. 51 MCP tools. Full chain lifecycle verified.

**Commits**: `d9c7d0a` through `c69d389` (7 commits)

---

## Session: Constitution & Expression (2026-03-21 — 2026-03-22)

Major design + implementation session spanning two days.

### Design Work

**Expression contract spec**: Wrote the full technical specification for the expression contract (contract #10). Critic-chain validated over 4 rounds — 55 issues found (2 FATAL + 22 HIGH + 31 MODERATE), all FATAL/HIGH resolved. Key architectural pivots:
- Full-iteration cohesion → O(1) incremental accumulators (FATAL: gas-unbounded at ~30 users)
- Live XP weights → snapshotted at expression time (FATAL: unrelated activity shifts cohesion)
- Auto-execute from day one → safety-first deployment (all amendments go through vote initially)
- Lazy cleanup → permissionless `CleanupExpired` crank (accumulator drift from stale expressions)
- Subject-scoped governance → cross-subject proposal mode for GER/CEP

**Brainstorm 013: Expression UX Refinements**: Expression fading (not nagging), 1 XP = participation at subject level (XP weighting IS sybil defense), no configurable gates at launch.

**Git governance design (Brainstorm 014)**: Critic-chain validated over 5 rounds — 48 issues found (4 FATAL + 20 HIGH + 24 MODERATE), all FATAL/HIGH resolved. Key decisions:
- Canonical diff hashing with exact commit SHAs + normalization
- One contribution per PR revision (withdraw old, submit new)
- XP stake on submission as anti-spam (anchored to something scarce)
- Self-vote prevention
- Primary-subject-only XP minting and voting

**Decision 009: Vault Standalone Rust**: Vault must be shared infrastructure (chain, KN, os-git). Build as standalone Rust daemon using Automerge + libp2p + Axum. The Open-Intelligence prototype from the Windows backup validated the tech stack but the use case differs — start fresh, use as reference.

### Implementation

**Expression contract (#10)**: Scaffolded and implemented with 53 unit tests. Core expression layer (Express, Renew, Withdraw) with O(1) incremental cohesion accumulators. Full observation lifecycle (StartObservation → SnapshotEpoch → StartReconfirmation → FinalizeAmendment). Moratorium after failed observation. Three governance tracks (GER, CEP, Subject) with separate config.

**Governance HasVoted query**: Added `HasVoted` query + `HAS_VOTED` storage index to governance contract for CEP qualification checking.

**Projects contract migration**: 8 changes for git governance — WithdrawContribution + Withdrawn status, content hash deduplication, XP-weighted voting with snapshot quorum (30%) and approval threshold (70%), self-vote prevention, primary-subject-only XP minting, contribution staking (lock on submit, burn on reject, unlock on accept/withdraw), supersession.

**Rust vault daemon**: Built at `/data/Dev/Open Systems/vault/`. Content-addressed store with SHA-256 keying, Axum HTTP API (compatible with Python relay endpoints), libp2p networking (GossipSub + mDNS + Kademlia DHT). 18 tests.

**os-git CLI**: Python CLI with 11 commands — init, submit, vote, accept, reject, withdraw, finalize, status, list, audit, release. Canonical diff computation, vault client (HTTP to vault daemon), local contribution tracking.

**MCP server**: Updated to 75 tools (was 63). Added 10 expression contract tools, WithdrawContribution, HasVoted query.

**Web explorer**: Added Expression tab (10th), projects enhancements (vote weights, quorum bars, staking display, Withdrawn status).

**E2e integration tests**: 10 new tests covering all 8 projects migration features. 197 workspace tests total, 62 e2e.

**Commits**: `6da9f8e` through `d074f1d` (chain repo), `f93a940` through `f8692d1` (spec repo), `359772b` (vault repo)

---

## Session: Dogfood & Infrastructure (2026-03-23)

### Dogfooding

First real use of os-git to manage Open Systems through its own governance:

1. Initialized os-git for project 0 ("Open Systems Chain")
2. Submitted real code changes as contributions
3. Owner accepted during incubation
4. Released project to community governance (irreversible)
5. Community voting: alice submitted, bob + charlie voted approve
6. Quorum enforcement worked: bob alone (150 XP) wasn't enough (needed 168), charlie's 30 XP pushed it over (180 > 168)
7. Self-vote prevention worked: alice couldn't vote on her own contribution
8. Finalization: contribution accepted, XP minted to author

**The system governed its own code change through community voting with XP-weighted quorum.**

### Infrastructure Hardening

**Problem discovered**: Computer hibernation kills background processes (chain node, vault daemon, running agents). Lost seeded chain state overnight.

**Solution**: Set up both chain node and vault daemon as systemd user services with `Restart=always`. Enabled lingering (`loginctl enable-linger`). Both services now auto-restart on crash, hibernation resume, and reboot.

```
● opensystems-chain.service — active (running)
● vault.service             — active (running)
```

**Rust vault integration**: Replaced the Python vault relay with the Rust vault daemon on port 9191. os-git's Python vault client talks to it seamlessly over HTTP — same API, different backend. Content storage verified end-to-end.

**Deploy scripts**: Created `deploy-all.sh` for robust incremental deployment. Handles existing chain state, maps checksums to code IDs.

**Commits**: `76c6a98` through `6a5a4e5`

---

## Key Decisions Timeline

| # | Date | Decision | Status |
|---|------|----------|--------|
| 001 | 2026-03-07 | Cosmos SDK as sovereign appchain | Accepted |
| 003 | 2026-03-07 | Content discovery via libp2p (Kademlia + GossipSub) | Accepted |
| 004 | 2026-03-08 | Project-level governance before global constitution | Accepted |
| 005 | 2026-03-08 | MCP server in Python + FastMCP | Accepted |
| 006 | 2026-03-09 | System Sovereignty (everything is a contribution) | Accepted |
| 007 | 2026-03-09 | Expressive Politics & Constitutional Architecture | Accepted |
| 008 | 2026-03-13 | Constitutional Derived Principles | Accepted |
| 009 | 2026-03-22 | Vault as standalone Rust daemon | Accepted |

## Brainstorms Timeline

| # | Date | Topic | Critic Chain |
|---|------|-------|--------------|
| 001-006 | 2026-03-07/08 | Self-hosted content, IDs, voting, vault, on/off chain, incubator | — |
| 007 | 2026-03-09 | Constitution & Expressive Politics | — |
| 008 | 2026-03-09 | Constitution Open Questions | 18 rounds, 8F + 23H |
| 009 | 2026-03-10 | Proof of Residency Network | 20 rounds, 111 issues |
| 010 | 2026-03-11 | Expressive Politics Scenarios | — |
| 011 | 2026-03-11 | Constitutional Governance Model | 10 rounds, 82 issues |
| 011a | 2026-03-12 | Constitutional Scenarios Extended | — |
| 012 | 2026-03-13 | Certification Anatomy & GER | 4 rounds, 28 issues |
| 013 | 2026-03-21 | Expression UX Refinements | — |
| 014 | 2026-03-22 | Git Governance | 5 rounds, 48 issues |

## Test Counts Over Time

| Date | Unit | E2e | Total | Contracts |
|------|------|-----|-------|-----------|
| 2026-03-09 | 76 | 58 | 134 | 9 |
| 2026-03-21 | 129 | 58 | 187 | 10 |
| 2026-03-23 | 135 | 62 | 197 | 10 |

## Architecture

```
Developer
    │
    ├── os-git CLI (Python) ──→ Chain (CosmWasm contracts)
    │       │                        │
    │       └── Vault (Rust) ◄──────→│ (hash verification)
    │                                │
    ├── MCP Server (Python) ────────→│
    │                                │
    └── Web Explorer (Python) ──────→│

Chain (Cosmos SDK + CosmWasm)
    ├── subject      — subject registry
    ├── experience   — non-transferable XP
    ├── forum        — posts with review period
    ├── auditing     — commit-reveal blind voting
    ├── projects     — incubator → community governance
    ├── governance   — executable proposals
    ├── build-spec   — declarative build configs
    ├── builder-registry — XP-weighted build attestors
    ├── artifact-verify  — community-verified builds
    └── expression   — constitutional governance (3 tracks)

Vault (standalone Rust daemon)
    ├── Content-addressed store (SHA-256)
    ├── HTTP API (Axum)
    └── P2P networking (libp2p)
```
