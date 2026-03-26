# Journey Log

> Where we are in building Open Systems. For humans and agents to regain context.

## Source of Truth

- **Specs**: [SPECS/INDEX.md](../SPECS/INDEX.md) — formal specifications
- **Decisions**: [DEV/docs/decisions/](docs/decisions/) — architectural decisions (001-009)
- **Brainstorms**: [DEV/docs/brainstorm/](docs/brainstorm/) — design explorations (001-015a)
- **Roadmap**: [DEV/docs/roadmap.md](docs/roadmap.md) — slice-based implementation plan
- **Chain dev notes**: [chain-dev.md](../../.claude/projects/-data-Dev-Open-Systems/memory/chain-dev.md) — implementation details
- **Glossary**: [SPECS/GLOSSARY.md](../SPECS/GLOSSARY.md) — terminology

Read those first. This doc tracks **implementation progress and pivots**.

---

## Current Status: SOVEREIGN (2026-03-25)

**The system governs itself. No human holds special power.**

10 contracts deployed on sovereign Cosmos SDK appchain. All internal admin dissolved. All CosmWasm admin transferred to governance contract. Code changes go through community voting via os-git. The bootstrap phase is over.

**Chain**: 10 CosmWasm contracts, 204 tests, zero clippy warnings. Admin = null on all contracts. CosmWasm admin = governance on all contracts.

**Tooling**: 75 MCP tools, os-git CLI (11 commands), web explorer (10 tabs), Rust vault daemon with P2P content transfer.

**Infrastructure**: Chain node + vault daemon running as systemd user services (`Restart=always`). Auto-restart on crash/hibernation.

**Seeded state**: 4 subjects (rust, cosmwasm, governance, sovereign), 8 users with XP, 2 projects (both released/community-governed), 13+ contributions, full lifecycle verified (forum, auditing, governance proposals, build sovereignty, expression dimensions).

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

## Session: Decentralized Web Access + Browser Participation (2026-03-25)

The session after sovereignty. Built the full decentralized web access layer — the path for anyone on any device to participate in Open Systems from a browser.

### Certification Contract Design

Wrote brainstorm 015 (certification registry) with 6-round critic chain (59 issues). Key insight from user feedback: XP gates (value creation) and certification gates (competency attestation) are fundamentally different. Training ≠ value creation. Added attestation model. Documented in 015a.

### Decentralized Web Access (Brainstorm 016)

Designed and critic-chain validated (5 rounds, 33 issues) the system for browser-based participation. Core idea: the web app IS vault content — content-addressed, replicated, governed. Minimal bootstrap loader for first-load verification. PoW for spam defense. Service worker for offline + governed updates. Peer registry on-chain for decentralized discovery.

### Implementation (7 Slices + 5 Participation Tasks)

Built and deployed all 7 slices of the web access layer:

1. **Vault `/app/` route** — manifest-based web serving with MIME types, SPA fallback, CSP headers, immutable caching. 30 Rust tests.
2. **Frontend SPA** — vanilla JS (no deps, no npm), dark theme, client-side routing with base-path detection. Dashboard, Subjects, Posts, Governance, Projects pages.
3. **Governance contract migration** — deployed on-chain via governance proposal #5. Added peer registry (RegisterPeer, RenewPeer, DeregisterPeer, CleanupPeers with lazy expiry) and UpdateAppHash proposal action with AppConfig state (manifest hash, monotonic version, proposal ID).
4. **Browser chain client** — minimal JS LCD client. All pages show live chain data (6 subjects, 3 posts, 5 proposals, 2 projects). LCD proxy through vault (`/v1/chain/*` → localhost:1317) so remote users only need one URL.
5. **Service worker** — cache-first for `/app/` routes, offline fallback, manifest hash pinning in IndexedDB, governed update detection with anti-downgrade, update banner UI.
6. **PoW ante handler** — Go module (`x/pow/`) with SHA-256 proof-of-work. 0-XP accounts require 16 leading zero bits (~2s). Accounts with XP exempt. 4 Go tests. Browser solver (`pow.js`). Binary builds but deployment blocked by x/upgrade authority mismatch.
7. **Bootstrap loader** — ~40 lines of verification logic. Fetches manifest, verifies every file's SHA-256, stores verification in IndexedDB, redirects to app. External JS (CSP compliant).

Additional participation infrastructure:
- **LCD proxy on vault** — `/v1/chain/*` forwards to localhost:1317. One tunnel, one port.
- **Root redirect** — `GET /` redirects to current app. `PUT/GET /v1/app-hash` manages default.
- **Real secp256k1 identity** — vendored noble-secp256k1 v3.0.0 (~5KB). Browser generates real keypairs, encrypts with user password (PBKDF2 + AES-GCM), stores in localStorage. Real bech32 `os1...` addresses.
- **CSP-safe event handling** — all button handlers use `data-action` delegation, no inline onclick (required by `script-src 'self'`).
- **Cloudflare tunnel** — `cloudflared tunnel --url http://localhost:9191` gives instant public HTTPS URL.

### On-Chain Deployments

- **Governance contract** migrated to code ID 11 (proposal #5, approved)
- **1 peer registered** (this node: vault + RPC URLs)
- **AppConfig v1** set (proposal #6, approved): manifest hash on-chain
- **PoW upgrade proposal #8** blocked: x/upgrade authority expects native gov module address, not CosmWasm governance contract. PoW code ready, deployment deferred.

### What's Live

The web app is accessible at `http://localhost:9191/` (redirects to current manifest). Via Cloudflare tunnel, accessible from anywhere. Shows live chain data: 6 subjects, forum posts, 8 governance proposals, 2 community-governed projects. Users can create identities with real secp256k1 keypairs.

### What's Next

TX building + signing + broadcast from the browser. Once done, users can create posts, vote on proposals, and earn XP — completing the participation loop.

### Commits

- Chain repo: `60a604f` through `eceaf42` (10 commits)
- Vault repo: `e84f208` through `cffc87b` (4 commits)
- Spec repo: `3f3becd` through `787e123` (5 commits)

### Cross-Agent Coordination

KN agent completed Vault integration (vault_client.rs, ContentRef on nodes, mcp_store_content + mcp_fetch_content tools). Integration test passed: store/fetch round-trip verified. KN agent now building Phase 1 of KG ↔ chain integration (community KG, publish-to-forum flow).

---

## Session: Sovereignty Achieved (2026-03-25)

The milestone. Open Systems became self-governing.

### Admin Dissolution

Disabled internal admin on all 10 contracts — `admin: null` across the board. Transferred CosmWasm-level admin (migration authority) to the governance contract on all 10 contracts. Verified: admin key now gets "unauthorized" on every operation. `AdminGrantExperience` returns "Admin is disabled." `set-contract-admin` returns "unauthorized." No backdoors remain.

### Governance Verification

Submitted governance proposal #4: "Create sovereignty-verified subject." Alice voted yes. After 120s voting period, finalized. The "sovereign" subject was created on-chain — with the governance contract as creator, proving cross-contract execution works through governance without admin.

### First Sovereign Code Change

Added a sovereignty transition comment to the projects contract. Committed, submitted via os-git as contribution #13. Bob (151 XP) and charlie (110 XP) voted approve through the CLI. Finalized through community vote. **The first code change governed entirely by the community.**

### What This Means

From this point forward:
- Every code change requires community review (os-git submit → vote → finalize)
- Every contract upgrade requires a governance proposal (MigrateContract action)
- Every parameter change requires a governance proposal
- Every new subject requires a governance proposal
- No human can bypass any of these. The admin key is inert.

The system that was supposed to enable community-driven development now governs its own development through community governance. 18 days from `Initialized with Ignite CLI` to sovereignty.

---

## Session: Certification Design & Infrastructure (2026-03-23 — 2026-03-25)

### Certification Contract Design

Wrote brainstorm 015: certification contract — the registry of governance standards. Critic-chain validated over 6 rounds (59 issues: 4 FATAL + 23 HIGH + 32 MODERATE, all FATAL/HIGH resolved). Key architectural decisions:
- Reference-counted expression dimensions (global per track)
- Time-locked XP publish staking (26 epochs, anti-sybil)
- Bidirectional conflict checking with 20-adoption limit
- Enforcement ladder (Clean → Warning → Probation → Decertification)
- Notice period for override weakening (prevents bait-and-switch)

### XP Gates vs Certification Gates (Key Insight)

User feedback on the maker space scenario revealed a fundamental distinction:
- **XP gates** = "has this person created value?" → governance participation
- **Certification gates** = "has this person demonstrated competence?" → equipment/role access

Training a newcomer to use a laser cutter isn't value creation — it's competency attestation. The certification contract needs an attestation model: a trainer vouches for the newcomer's competency. Documented in brainstorm 015a.

### Rust Vault P2P Content Transfer

Implemented the missing piece: actual byte transfer between vault peers. Request-response protocol (`/vault/content/1.0.0`), auto-fetch on GossipSub announcement, hash verification before storage. Two daemons replicate 3 objects bidirectionally in <2 seconds.

### os-git Improvements

Renamed `os-git/` → `os_git/` (Python module naming), added `withdraw` command, fixed `finalize` local tracking (queries chain instead of parsing events), added TX sequence mismatch retry in `lib/cli.py`.

### Full Lifecycle Re-Seed

Re-exercised all lifecycle flows on the current chain:
- Forum: 5 posts (3 approved, 1 held/audited, 1 approved via audit)
- Auditing: Case 1 ran full commit-reveal cycle → approved (4 PASS votes, early consensus)
- Governance: 3 proposals (create blockchain subject ✓, duplicate rejected ✓, reduce review period ✓)
- Build sovereignty: 1 build spec, 2 builders, 2 attestations, 1 verified artifact
- Expression: dimensions registered, expressions recorded

### Infrastructure

- Both chain node and vault daemon running as systemd user services with `Restart=always`
- CONTRIBUTING.md written for onboarding new developers
- Full system verification: 204 tests, 75 MCP tools, all services healthy

### Commits

- Chain repo: `76c6a98` through `256b419` (16 commits)
- Spec repo: `431f682` through `f76872f` (5 commits)
- Vault repo: `846dc7a` (P2P content transfer)

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
| 015 | 2026-03-23 | Certification Contract Design | 6 rounds, 59 issues |
| 015a | 2026-03-25 | Certification Scenarios Feedback | — |
| 016 | 2026-03-25 | Decentralized Web Access | 5 rounds, 33 issues |

## Milestones

| Date | Milestone |
|------|-----------|
| 2026-03-07 | Chain scaffold (Ignite CLI) |
| 2026-03-09 | 9 contracts deployed, admin dissolved, full lifecycle verified |
| 2026-03-21 | Expression contract + governance HasVoted |
| 2026-03-22 | Git governance design, Rust vault daemon, projects migration, os-git CLI |
| 2026-03-23 | Dogfood: first community-governed code change, P2P vault content transfer |
| **2026-03-25** | **SOVEREIGNTY: admin dissolved on all 10 contracts, system self-governing** |
| **2026-03-25** | **WEB ACCESS: browser-based participation, vault-served SPA with live chain data** |

## Test Counts Over Time

| Date | Unit | E2e | Total | Contracts | Sovereign |
|------|------|-----|-------|-----------|-----------|
| 2026-03-09 | 76 | 58 | 134 | 9 | No (admin active) |
| 2026-03-21 | 129 | 58 | 187 | 10 | No |
| 2026-03-23 | 135 | 62 | 197 | 10 | No |
| 2026-03-25 | 142 | 62 | 204 | 10 | **Yes** |
| 2026-03-25 | 142+30 | 62 | 234+ | 10+gov migrated | Yes + web app |

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
    ├── P2P networking (libp2p: GossipSub + mDNS + Kademlia)
    └── Content transfer (request-response protocol, auto-fetch)
```
