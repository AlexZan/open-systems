# Admin Capability Audit — Plan

**Date**: 2026-04-14
**Design doc**: (none — derived from in-session audit against the 10-contract admin capability matrix)
**Parent effort**: admin-capability-audit

## Problem

Decision-187 says admin is the safety net during incubation — meaning before the system can demonstrably self-govern, a founder-held admin must be able to intervene when things go wrong. A capability audit against nine real-world failure scenarios (content moderation, bad actors, XP gaming, broken state, emergency recovery) found nine gaps between what admin CAN do today and what it needs to do to actually be a safety net. Launching with real users before closing the launch-critical gaps means admin will face situations it has no tool to fix.

## Discovery

**Capability matrix (prior step in this session):**
- 22 admin-gated messages across 10 contracts, 11 exposed via MCP.
- Every contract has `DisableAdmin` (one-way kill switch) and `AdminRegisterCaller`.
- CosmWasm admin on all 10 contracts is the governance contract, so `MigrateContract` and `TransferContractAdmin` work via governance proposal.
- Direct admin powers of note: `experience::AdminGrantExperience` (mint XP, MCP exposed), `governance::DisableAdmin`, `expression::RegisterDimension`.

**Confirmed absent via code search (`contracts/**/*.rs`):** `Slash*`, `PauseContract`, `HidePost`, `DeletePost`, `RotateAdmin`, `TransferAdmin`, `DeregisterAuditor`, `RedactPost`. The nine scenario gaps are real gaps, not misreads.

**Prior art found:**
- **Tombstone mechanism** (brainstorm-008, "Expression tombstone mechanism", lines 742–746): user-initiated retraction design. On-chain tombstone marker (hash of retraction + timestamp); original hash persists but marked retracted; off-chain vault content deleted; future calculations exclude tombstoned items. This is the existing design pattern for admin content takedown — the admin version just gates the retraction on admin instead of post author. **This fold #9 (on-chain content redaction) into #1 (content takedown)**: tombstones are the answer to "you can't erase a hash, but you can mark it retracted."
- **sovereignty-plan.md** (DEV/docs/designs/): establishes the same "admin is safety net during incubation" framing. This plan inherits its rationale.

**Discrepancies:**
- None in the capability matrix itself. The CLAUDE.md in the project root is stale (says "specification project, not yet code"); the real implementation is in `opensystems/contracts/`.

## MVP Scope

### 1. Admin content takedown via tombstone
**Why MVP**: Smoke test + data integrity — a public platform launching with real users cannot demonstrate safety if admin has no tool to hide illegal/harassing content on day one. Combines the original gap #1 (no path to hide vault or on-chain posts) and gap #9 (on-chain hash redaction) because the tombstone design (brainstorm-008) solves both at the only level they're solvable: the on-chain post is marked retracted, and the vault content is deleted/unserved.
**Blocked by**: none
**Effort description**: Forum contract has no `HidePost`, `DeletePost`, or admin-side tombstone message. Users have `FlagPost` (requires XP) but admin cannot force-takedown. Vault daemon has no API for admin-triggered content deletion, and posts gossip across peers so a single-host delete doesn't propagate. Build: admin/governance-gated `TombstonePost` on forum contract (sets a tombstone flag + reason hash on the post state); vault daemon honors the tombstone by unserving content on HTTP fetch and propagating the tombstone via GossipSub; frontend renders tombstoned posts as "[retracted by admin]" instead of content. Reuse the brainstorm-008 tombstone design, adapt author-check to admin-check.

### 2. Admin key rotation
**Why MVP**: Data integrity — `DisableAdmin` is one-way kill, not rotate. If the admin private key is compromised, the attacker can `AdminGrantExperience` indefinitely (minting unbounded XP and polluting the governance signal) or preemptively call `DisableAdmin` to block recovery. With no rotation path, a single stolen key voids the safety net that decision-187 assumes exists. Admin cannot be a safety net if the admin key itself is a single point of failure.
**Blocked by**: none
**Effort description**: No contract has a `RotateAdmin` or `TransferInternalAdmin` message. The only "admin change" path is `DisableAdmin` (permanent). CosmWasm admin transfer exists at the chain level but doesn't affect in-contract `admin` state. Build: admin-gated `RotateAdmin { new_admin }` message on the shared `os_types::admin` helper, exposed on all 10 contracts. Optionally: governance-gated fallback `ForceRotateAdmin` via proposal so compromised key → governance rescue. MCP tool `os_rotate_admin` for founder use.

### 3. Emergency pause / circuit breaker
**Why MVP**: Data integrity — governance migration is the only current way to stop an active exploit, but proposal voting periods take 120s+ minimum (longer in prod). An exploit draining XP or minting posts at the rate cap can inflict significant damage in that window. Pause is the literal "break glass" lever that makes admin a safety net rather than a post-hoc cleaner. Without it, #1 and #2 still leave admin unable to stop *ongoing* damage.
**Blocked by**: none
**Effort description**: No contract has a pause toggle. `AdminDisabled` flags exist on 4 contracts (experience, auditing, artifact-verify, builder-registry) but they gate a *single* specific admin message, not the contract as a whole. Build: admin-gated `PauseContract` / `UnpauseContract` messages on the shared `os_types::admin` helper, exposed on all 10 contracts. When paused, all non-query execute messages return an error. Governance can override (proposal to unpause even if admin is gone). MCP tool `os_pause_contract` for emergency use.

## Deferred Scope

### Efforts

#### 4. XP slashing
**Why deferred**: Adversarial origin + optimization — abuse scenarios (sybil rings, vote trading) are theoretical at launch scale (tens of users). In the short term, the stopgap is "governance migrates experience contract to a state with the bad actor's XP zeroed out" — ugly but possible. Building `SlashExperience` without observing real abuse patterns risks designing the wrong penalty model.
**Origin**: admin-capability-audit (this session)
**Promotion trigger**: First observed XP gaming incident in production, OR active user count > ~100 (where sybil rings become cheap enough to try).
**Effort description**: `experience::AdminGrantExperience` mints XP but no inverse exists. Sybil self-upvote rings and vote-trading cannot be punished without either a coordinated contract migration (state reset for specific accounts) or a new `SlashExperience` message. Admin has the observational data (TX history) but no lever. Design questions when promoted: subject-scoped vs global slash? Burn to zero vs decrement? Slash target includes governance contract's XP record? Appeal path?

#### 5. Subject management (delete / merge / quarantine)
**Why deferred**: Edge case — tag-spam fake subjects are cosmetic clutter at launch scale, not a functional breakage. The auto-create design (decision "subjects emerge from posts") is deliberate. Premature delete/merge tooling risks contradicting that principle.
**Origin**: admin-capability-audit (this session)
**Promotion trigger**: Subject count > ~1000 AND observable user complaints about discoverability / search pollution; OR a specific abuse pattern observed where tag-spam is being used to farm XP.
**Effort description**: Subjects auto-create from post tags (design-intentional, see "subjects emerge from posts" feedback). Admin has no `DeleteSubject`, `MergeSubjects`, or `QuarantineSubject` path. A bad actor could flood post tags to create garbage subjects and farm XP in them via auto-promote. Fix space: delete (breaks references), merge (preserves XP), quarantine (hides from discovery but preserves state). Pick a strategy when real abuse is observed.

#### 6. Auditor revocation
**Why deferred**: Edge case + related to #4 — `os_register_auditor` self-registers at ≥3 XP (trivially low). A captured/colluding auditor is a real concern but, as with XP slashing, the launch-scale stopgap is contract migration. At launch there will be <10 auditors — a single bad actor is handled human-in-the-loop through the founder, not through contract logic.
**Origin**: admin-capability-audit (this session)
**Promotion trigger**: First observed auditor collusion or sabotage incident, OR auditor count > 10 (where founder can no longer eyeball them).
**Effort description**: Auditing contract has no `DeregisterAuditor` admin message. Auditors self-register via `RegisterAuditor` at ≥3 XP. If an auditor is captured or sabotaging, admin must migrate the auditing contract to remove them from state. Builds on #4's design discussion (slashing vs removal vs quarantine).

#### 7. Governance override / emergency veto — NEEDS BRAINSTORM
**Why deferred**: Design tension, not a build task. Low-XP governance capture (attacker hits 20 XP quorum at small scale) is a real risk, but an admin veto directly contradicts the sovereignty trajectory (decision-006) and decision-187's framing of admin as "safety net, not dictator." This needs a design brainstorm to resolve the tension before any implementation effort — otherwise we're building something the design principles say shouldn't exist.
**Origin**: admin-capability-audit (this session)
**Promotion trigger**: After a brainstorm reconciles "admin safety net during incubation" with "no special power" sovereignty target. Likely form: time-boxed veto that expires at a specific XP-holder threshold, not a permanent power. Alternatively: admin has no veto but #3 (pause) + #2 (key rotation) provide enough defense.
**Effort description**: Governance has no admin veto or emergency override. Low quorum barrier (20 XP at launch) means a well-funded attacker could pass malicious proposals (e.g., mint themselves XP via a crafted `MigrateContract` payload) without founder recourse short of chain halt. But admin veto is a design tension with sovereignty principles. This effort is a *brainstorm effort*, not a build effort: output should be a brainstorm doc that either (a) proposes a sovereignty-compatible veto design, or (b) argues that #3 (pause) + migration are sufficient and closes without a veto.

#### 8. Stuck-state rescue (ForcePromote / CancelProposal / ForceFinalize)
**Why deferred**: Edge case — auto-promote silent failures (fact-1303) and unfinalizable proposals are known but rare. Contract migration handles all of them. Building purpose-built rescue messages before observing which states actually get stuck at launch risks designing for the wrong stuck-state patterns.
**Origin**: admin-capability-audit (this session)
**Promotion trigger**: Observed stuck state in production that migration cannot cleanly fix; OR migration becomes operationally painful (e.g., repeated migrations for the same class of bug).
**Effort description**: Vault auto-promote loop has a known silent-failure path (fact-1303). Governance proposals can get stuck if voting window expires with edge-case state. Forum contract has no `ForcePromote`, governance has no `CancelProposal` or `ForceFinalize`. These are rescue levers — nice to have, but not first-day essential because migration is the stopgap.

### Notes

(None — all six deferred items have enough identity to warrant their own effort.)

## Triage Rationale

Pattern: three gaps are genuinely launch-blocking (cannot demonstrate safety without them), six are handleable via the existing migration escape hatch at launch scale. The MVP items all pass the "smoke test" (can you show admin being a safety net without this?) — content takedown, key rotation, and pause are the three levers that fail the smoke test individually. Everything else — slashing, subject management, auditor revocation, stuck-state rescue — has migration as a stopgap, and building purpose-built tools for theoretical abuse patterns before real usage risks designing the wrong tool. 6 of 9 items deferred (~67%), matching the default-defer bias. Notable: #7 (governance override) is the one item that isn't a pure build task — it's a design tension with sovereignty principles that needs a brainstorm before any effort tree, so it's deferred as a *brainstorm* effort rather than an implementation effort.

One other observation: folding gap #9 (on-chain content redaction) into #1 (content takedown) via the existing brainstorm-008 tombstone design cut the MVP count from four to three without losing coverage. This is worth noting — the plan skill's grounding step found prior art that made the triage cleaner.
