# 027/028 — Implementation Plan

**Date:** 2026-04-19
**Design docs:** `DEV/docs/brainstorm/027-forum-tag-tree-xp-propagation.md` + `DEV/docs/brainstorm/028-forum-tag-curator-audit-gate.md`
**Parent effort:** `forum-tag-tree-implementation` (already open, sibling of closed designs)

---

## Problem (from design docs)

Today the forum's tag system is flat: posts get `tags: Vec<String>` and XP mints to one subject only. The bug-incentive mechanic the project needs to stand up requires XP to fan out up a parent hierarchy (`waybar → gui → os → linux`), and the two main abuse vectors (primary-tag misattribution, unbounded tree mutation) need structural defenses before economic activation. Brainstorm 027 worked out the propagation mechanics; 028 worked out the defenses. Both converged via adversarial critic chains (4 and 5 rounds respectively). Everything is now spec; nothing is code.

## Discovery

Grounded against current contracts:

- **subject** (`contracts/subject/`): already has `Subject.parent_tag: Option<String>`, `SUBJECT_CHILDREN`, parent-existence check on `CreateSubject`, genesis taper mechanics. Missing: cycle/depth check, `BOOTSTRAP_WINDOW_OPEN`, `AdminSeedParent`/`CloseBootstrapWindow`, `AncestorChain` query, `AddTotalExperienceBatch`, `PENDING_ADOPTIONS`/`ADOPTION_COOLDOWNS`, `ProposeParent`/`ChallengeAdoption`/`FinalizeAdoption`. `EnsureSubjectsExist` still creates orphans.
- **experience** (`contracts/experience/`): `ExperienceTransaction { id, tx_type, user, subject, amount: i64, source_type, source_id, block_height, timestamp }` is in place — the `amount` field is exactly the per-level credit the 028 design needs for compensating burns, no reconstruction required. Mint path is single-subject, no ancestor walk. Missing: `PROPAGATION_ENABLED`/`PROPAGATION_REGIME`/`AUDIT_GATE_CONTRACT` items, `SetAuditGate`/`SetPropagationEnabled` setters, `regime`+`ancestor_snapshot` on tx records, propagation mint path, `BURN_DEBT`.
- **auditing** (`contracts/auditing/`): commit-reveal infrastructure is complete (`Report`/`CommitVote`/`RevealVote`/`FinalizeCase`/`Appeal`, 8h+4h phases, appeal stake mechanics). `AuditVote` is `pass|reject`. Missing: `ReportTagMisattribution`, `ReportAdoptionChallenge`, case-type-aware verdict variants, `CASE_BY_POST` invariant guard, `MISATTRIBUTION_COOLDOWN`, `AuditCapabilities`, jury-selection across multiple subjects.
- **forum** (`contracts/forum/`): `Post.tags: Vec<String>` with no primary marker. `FlagPost`, `AutoPromote`, `InternalMsg::{HoldPost, ApprovePost, RejectPost, ReopenPost, UpdateConfig}` exist. Missing: `primary_tag: String` on `Post`, `InternalMsg::UpdatePrimaryTag`, `HoldPost` accepting `Promoted` state.

No discrepancies between design assumptions and current code — both designs explicitly accounted for the existing state.

## MVP Scope

Triage principle: ship the smallest set that gets "flag a post, earn XP, see XP fan up the tree" working end-to-end. The activation flag stays `false` by default, so even if something's wrong, nothing catastrophic happens economically — propagation is inert until governance flips it.

### 1. subject-tree-hardening
**Why MVP:** Data integrity. Without cycle/depth checks, an attacker or a typo can corrupt the tree into a loop or unbounded depth, breaking every downstream mint walk.
**Blocked by:** none.
**Scope:** Add `CycleDetected` + `TreeTooDeep` errors. Add walk-check in `execute_create_subject`: walk up from claimed parent, reject if new tag appears or depth ≥ 8. Tests for depth boundary and cycle rejection. Small PR.

### 2. subject-bootstrap-window
**Why MVP:** Core dependency for activation. Without `BOOTSTRAP_WINDOW_OPEN` + `AdminSeedParent` + `CloseBootstrapWindow`, governance has no way to seed the initial parent-map required to flip propagation on.
**Blocked by:** MVP-1 (cycle/depth checks must be in place before AdminSeedParent uses them).
**Scope:** Add `BOOTSTRAP_WINDOW_OPEN: Item<bool>` default true. Add `ExecuteMsg::AdminSeedParent { tag, parent }` (admin-or-authorized-caller, orphan-only, window-open-only, reuses cycle+depth checks). Add `ExecuteMsg::CloseBootstrapWindow {}` (admin-or-authorized-caller, idempotent, irreversible). Tests.

### 3. subject-propagation-primitives
**Why MVP:** Core dependency. Experience contract's propagation mint path can't function without these two.
**Blocked by:** none.
**Scope:** Add `AncestorChain { tag }` query returning ordered ancestor list (leaf through root, excluding leaf; simple version — skip taper and deprecated flags for v1, add when deprecation mechanism exists). Bounded at `MAX_TAG_DEPTH = 8`. Add `InternalMsg::AddTotalExperienceBatch { updates: Vec<(String, u64)> }` — simple all-or-nothing version; deprecation-skip logic deferred. Tests for both.

### 4. experience-propagation-engine
**Why MVP:** Smoke test. This IS the thing we're building. Propagation mint + activation gate.
**Blocked by:** MVP-3 (needs `AncestorChain` + `AddTotalExperienceBatch`).
**Scope:**
- Add items: `PROPAGATION_ENABLED: Item<bool>` (default false), `PROPAGATION_REGIME: Item<u32>` (default 0), `AUDIT_GATE_CONTRACT: Item<Option<Addr>>` (default None).
- Extend `ExperienceTransaction` with `regime: u32` and `ancestor_snapshot: Vec<String>`.
- Add `SetAuditGate { addr }` setter (admin-or-authorized-caller, cw2 ContractInfo check must return `"crates.io:os-auditing"`).
- Add `SetPropagationEnabled { enabled }` setter with preconditions on true-flip: audit gate set, ≥3 parented subjects. Flipping true closes bootstrap window via sub-message. Regime counter increments on every flip.
- Propagation mint path: branches on flag, queries `AncestorChain`, applies `N >> k` per level, one `AddTotalExperienceBatch` sub-message. Read-all-then-write-all ordering (safe default even though v1 has no tapers). No tree-cut logic yet (deprecation mechanism doesn't exist).
- Tests for all state transitions.

### 5. forum-primary-tag
**Why MVP:** Core dependency + data integrity. Without `primary_tag` as an explicit frozen field, propagation relies on array ordering that nothing enforces, and misattribution correction has no field to correct.
**Blocked by:** none (can ship independently of MVP 1–4; fits naturally in parallel).
**Scope:**
- Add `primary_tag: String` to `Post`, populated from `tags[0]` at `CreatePost`, frozen thereafter.
- `AutoPromote` uses `primary_tag` (not `tags[0]`) as the mint target.
- Add `InternalMsg::UpdatePrimaryTag { post_id, new_primary_tag }` callable by auditing contract.
- Tests for creation, auto-promote targeting, and tag-update path.

### 6. auditing-tag-misattribution
**Why MVP:** Smoke test. Without this, `SetPropagationEnabled(true)` fails the audit-gate precondition and propagation can never activate.
**Blocked by:** MVP-5 (needs `primary_tag` + `UpdatePrimaryTag`).
**Scope:**
- Add `ReportTagMisattribution { post_id, proposed_primary_tag, reason }` execute msg. Pre-promotion only (caller posts in `UnderReview` state). Standing check (≥1 XP in proposed subject — bootstrap value), stake lock (1 XP), jury-pool precondition (≥3 unique holders in current ∪ proposed).
- Extend `AuditVote` to be case-type-aware: add `Keep | Correct | Reject` variants alongside existing `pass | reject`. Add `case_type: CaseType` to `AuditCase` so `FinalizeCase` dispatches correctly.
- Verdicts: `Keep` (flagger stake burned, post auto-promotes unchanged), `Correct` (flagger stake returned, forum's `UpdatePrimaryTag` invoked before AutoPromote fires), `Reject` (flagger stake burned, post rejected via existing `RejectPost`). Reveal-timeout = no-consensus, all stakes returned.
- `CASE_BY_POST: Map<u64, u64>` guard rejects overlapping reports on same post.
- Add `AuditCapabilities {}` query returning `{ tag_misattribution: true, adoption_challenge: true }` (simple struct; version field deferred).
- Tests for all verdicts, timeout, standing + pool rejections.

### 7. subject-propose-parent
**Why MVP:** Core dependency for long-term. Without ProposeParent, post-bootstrap, the tree freezes into whatever AdminSeedParent managed to set. That's a dead-end — governance-only seeding isn't sustainable.
**Blocked by:** MVP-6 (needs `ReportAdoptionChallenge` on auditing — part of MVP-6's scope extension, see below).
**Scope:**
- Add `PENDING_ADOPTIONS: Map<&str, PendingAdoption>` with minimal struct (proposed_parent, proposer, challenge_deadline, challenged, challenge_case_id — NO governance-param snapshots in MVP).
- Add `ADOPTION_COOLDOWNS: Map<&str, u64>` — simple tag-level cooldown keying for v1 (triple-keying deferred; tag-level is stricter but easier to reason about, upgrade when grief observed).
- Add constants: `ADOPTION_CHALLENGE_WINDOW = 604_800` (7d), `ADOPTION_PROPOSE_COST = 1` XP, `ADOPTION_COOLDOWN_AFTER_NEITHER = 2_592_000` (30d), `ADOPTION_STANDING_MIN_XP = 1`.
- Add execute messages: `ProposeParent`, `ChallengeAdoption`, `FinalizeAdoption`. Reject `ProposeParent` when bootstrap window is open. Stake locking via experience contract.
- On `FinalizeAdoption` unchallenged: set `parent_tag`, return stake, delete pending. On challenged + audit verdict: apply `ProposedWins | CounterWins | NeitherWins` semantics. Reveal-timeout = `NeitherWins`.
- Tests for all paths.

### 8. auditing-adoption-challenge
**Why MVP:** Part of MVP-6's scope but called out separately because it's blocked by MVP-7. Add `ReportAdoptionChallenge` (callable by subject contract only) + adoption verdict variants (`ProposedWins | CounterWins | NeitherWins`) to the same auditing-contract changes.
**Blocked by:** MVP-6 (same contract, same case_type machinery).
**Scope:** Add `ReportAdoptionChallenge { tag, proposed_parent, counter_parent, proposer, challenger }` execute msg. Extend `AuditVote` with adoption verdict variants. Verdict dispatch calls subject contract back with the outcome so FinalizeAdoption can apply it. Jury = `proposed_parent`-holders ∪ `counter_parent`-holders (no target-subject exclusion enforced in v1 — target-subject holders only vote if they also hold XP in proposed or counter). Tests.

### 9. integration-tests
**Why MVP:** Smoke test. The unit tests per MVP cover individual paths; an end-to-end test is what proves the feature works.
**Blocked by:** MVP 1–8.
**Scope:** Integration test in `opensystems/tests/integration/tests/` covering: (a) admin seeds parents during bootstrap, (b) governance flips `SetPropagationEnabled(true)` successfully and auto-closes bootstrap window, (c) post created with `primary_tag`, auto-promotes, author earns XP at leaf and ancestors per shift math, (d) another user reports misattribution, Correct verdict updates primary_tag, new auto-promote targets corrected tag, (e) ProposeParent + ChallengeAdoption + audit resolution paths. This is the thing you demo.

## Deferred Scope

### Efforts

#### burn-debt-queue
**Why deferred:** Adversarial origin (round 3 of 028 critic chain). Residue from post-promotion `Correct` saturating burns only matters when post-promotion reports are filed, which is itself deferred. Shipping MVP with pre-promotion-only misattribution means burns never fire on already-minted XP.
**Origin:** critic-chain 028 round 3.
**Promotion trigger:** when post-promotion misattribution reports are enabled (see `post-promotion-misattribution-reports` effort) — they can't exist without debt handling.
**Effort description:** Per 028 §4, add `BURN_DEBT: Map<(Addr, String), u64>` in experience contract. Saturating-burn residue writes to this map. Future `MintExperience` to same `(user, subject)` consumes debt before crediting. `RecordBurnDebt` internal entry-point callable only by auditing contract. Worked example in 028 §4 shows cross-contamination (debt from one post reduces future earnings in that subject). Resists iterated-farming attack where author spends unearned XP before verdict lands.

#### post-promotion-misattribution-reports
**Why deferred:** Adversarial origin (round 2 of 028). v1 restricts `ReportTagMisattribution` to posts in `UnderReview` state. The compensating atomic burn+mint on already-promoted posts adds significant complexity (saturating burns, debt queue, HoldPost-on-Promoted, tx-history query by source_id) that MVP doesn't need to demo.
**Origin:** critic-chain 028 round 2.
**Promotion trigger:** first real misattribution case filed against a post that already auto-promoted (proves pre-promotion-only is insufficient).
**Effort description:** Per 028 §3.1, allow `ReportTagMisattribution` on posts in `Promoted` state. Correct verdict triggers `BurnExperience` across the post's original `ExperienceTransaction.amount` records (queried by `source_id = post_id`), then `MintExperience` on the new primary's current ancestor chain. Saturating burn per level with residue → `BURN_DEBT`. Requires forum's `HoldPost` to accept `Promoted` state.

#### misattribution-refile-cooldown
**Why deferred:** Adversarial origin (round 4 of 028). The infinite-hold-loop attack requires multiple no-consensus timeouts; if MVP gets deployed and no one attempts the attack, the cooldown is theater. If the attack happens, ship this.
**Origin:** critic-chain 028 round 4.
**Promotion trigger:** observed or threatened infinite-hold pattern (a single post held for > 24h via repeated reports).
**Effort description:** Per 028 §4, add `MISATTRIBUTION_COOLDOWN: Map<u64, u64>` keyed on `post_id`. Set to `now + 86400` (24h) on any case close except `Reject`. Block new `ReportTagMisattribution` on a post while its cooldown is active. Tests for cooldown enforcement + expiry.

#### pending-adoption-param-snapshots
**Why deferred:** Adversarial origin (round 3 of 028). Only matters if governance raises `ADOPTION_STANDING_MIN_XP` or `ADOPTION_PROPOSE_COST` while a proposal is in-flight. v1 has no such raises planned; bootstrap values are low and stable.
**Origin:** critic-chain 028 round 3.
**Promotion trigger:** governance raises any adoption parameter; add before the raise lands.
**Effort description:** Per 028 §3.2, extend `PendingAdoption` with `snapshot_standing_min_xp: u64` and `snapshot_propose_cost: u64` frozen at propose time. `ChallengeAdoption` checks against the snapshot, not current config. Prevents retroactive disqualification of honest challengers.

#### adoption-abandonment-penalty
**Why deferred:** Adversarial origin (round 4 of 028). The 60-day threshold only matters for pendings that nobody cranks. If MVP's propagation value-proposition works, proposers crank their own pendings promptly (stake return incentive). If abandonment-at-scale actually happens, ship this.
**Origin:** critic-chain 028 round 4.
**Promotion trigger:** observed abandoned pending (≥30 days since challenge_deadline expired with no FinalizeAdoption call).
**Effort description:** Per 028 §3.2, add `ADOPTION_MAX_AGE = 5_184_000` (60d) constant. `FinalizeAdoption` on pending past `challenge_deadline + ADOPTION_MAX_AGE` treats as `Abandoned`: proposer stake burned, parent stays None, pending deleted. Incentivizes timely cranks.

#### triple-keyed-adoption-cooldown
**Why deferred:** Adversarial origin (round 2 of 028, refined in round 4). v1 ships with tag-level cooldown (stricter — whole tag locks for 30d after a NeitherWins). This hurts legit third-party proposals but is simpler. Upgrade once third-party griefing is an actual problem.
**Origin:** critic-chain 028 rounds 2 and 4.
**Promotion trigger:** observed grief pair intentionally NeitherWins'ing a tag to block a third community.
**Effort description:** Per 028 §3.2, change `ADOPTION_COOLDOWNS` key from `&str` (tag) to `(tag, sorted_pair)` composite key. Third parties proposing with a different parent bypass the cooldown; only the exact grief triple is locked.

#### versioned-audit-capabilities
**Why deferred:** Adversarial origin (round 1 of 028). v1 ships with a simple `{ tag_misattribution: bool, adoption_challenge: bool }` response. Versioning matters only when a future capability is added and the experience contract needs to gate on its presence.
**Origin:** critic-chain 028 round 1.
**Promotion trigger:** when a third capability is added and experience contract needs to enforce a minimum.
**Effort description:** Per 028 §3.3, extend `CapabilitiesResponse` with `version: u32`. Add `MIN_AUDIT_CAPABILITIES_VERSION` constant in experience contract, enforced in `SetPropagationEnabled(true)`. Document audit-contract-migration-before-experience-contract-migration ordering.

#### target-subject-jury-exclusion
**Why deferred:** Adversarial origin (round 3 of 028). v1 jury = `proposed_parent` ∪ `counter_parent` (for adoption) or `current_primary_tag` ∪ `proposed_primary_tag` (for misattribution). Target-subject holders vote only if they also hold XP in one of the candidate subjects — implicit exclusion is the default, explicit exclusion logic is extra code that matters only when rent extraction becomes observable.
**Origin:** critic-chain 028 round 3.
**Promotion trigger:** observed side-payment coordination in commit-reveal voting patterns.
**Effort description:** Per 028 §3.2, add explicit filter in jury-selection helper: exclude addresses that hold XP in the target subject (the post's `primary_tag` for misattribution, the subject-being-adopted for adoption). Even if they also hold XP in a candidate subject, target-subject standing disqualifies.

#### deprecation-mechanism-and-tree-cut
**Why deferred:** No deprecation mechanism exists in the current codebase. `Subject.deprecated_at: Option<u64>` field exists but nothing ever sets it. 027 §4.5's tree-cut logic is untestable without a way to deprecate, so the code would be dead code in v1. Ship when deprecation lands.
**Origin:** brainstorm 027 §4.5.
**Promotion trigger:** deprecation mechanism shipped (separate effort).
**Effort description:** Per 027 §4.5, once deprecation exists: extend `AncestorChain` query to return per-level `deprecated: bool` + `taper_factor_bps`. Experience contract's propagation mint applies tree-cut at first deprecated ancestor (not skip): leaf deprecated → no-op mint; mid-chain deprecated → halt walk, levels above excluded. `AddTotalExperienceBatch` skips deprecated entries as defense-in-depth.

#### seed-threshold-depth-check
**Why deferred:** Adversarial origin (round 3 of 027). v1 requires ≥3 parented subjects for `SetPropagationEnabled(true)` precondition — depth-≥2 check adds `the seeded hierarchy must have a real tree`, which is belt-and-suspenders for v1's small seeded set.
**Origin:** critic-chain 027 round 3.
**Promotion trigger:** observed governance pattern of seeding 3 flat dummy parents to trip the gate.
**Effort description:** Per 027 §4.0, add structural check: at least one parented subject's own parent must itself be parented (depth ≥ 2). Rejects flat-dummy seeding.

### Notes (implementation details, not separate efforts)

| Item | Why deferred | Promotion trigger |
|------|--------------|-------------------|
| Lazy cleanup of `ADOPTION_COOLDOWNS` / `PENDING_ADOPTIONS` | No measurable state bloat at launch scale | Contract storage grows > 10MB from these maps |
| Formal FlagPost vs audit-held state-machine unification | Implicit ordering works for v1 | Observed state-transition collision (Hold + Flag simultaneously) |
| Jury-pool submission-time check explicit reveal-phase re-check | Reveal-timeout-returns-stakes (MVP-6) covers this case | If quorum rules tighten in a future effort |
| AncestorChain query caching for hot-path optimization | Depth-8 is cheap enough in v1 | Profiling shows `SUBJECTS.load` in the hot path under measurable load |
| Saturating-burn event emission for observability | Not a behavior requirement | Ops needs to monitor unrecovered residue |

## Triage Rationale

Two distinct design docs totaling 9 rounds of critic-chain produced a lot of edge-case work. Most of the round-3-and-later critic findings were defensive layering: what happens if an attacker WANTS this defense to fire, what happens if governance raises a parameter mid-case, what happens if a subject is deprecated between mint and verdict. None of those scenarios exist in v1's minimal operating state (few users, few subjects, no deprecation mechanism, no governance raises). So ~70% of what the design docs specify is correctly deferred until signal. The MVP reduces to: the tree hardens against bad creates, bootstrap can seed initial parents, propagation mints through the tree when the flag flips, posts have a frozen primary tag, misattribution works pre-promotion, adoption works via the commit-reveal jury. That's 9 efforts, mostly contract-local, with clean dependencies, plus the end-to-end integration test.

The fact that the activation flag stays default-false is the key operational safety net: even if the MVP ships with a bug in the propagation math, nothing catastrophic can happen economically until governance explicitly flips the flag. That lets MVP ship without the full defensive stack; the deferred items get promoted when real operational signal says they're needed.
