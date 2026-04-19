# 028 — Forum Tag Curator Audit Gate (Design)

**Effort:** `forum-tag-curator-audit-gate`
**Parent:** `forum-tag-tree-xp-propagation`
**Sibling (closed):** `forum-tag-tree-semantics-design` — see brainstorm 027.
**Status:** Draft v1
**Created:** 2026-04-19

---

## 1. Problem

Brainstorm 027 (semantics design) bounds propagation per-mint to `<2N` XP, but explicitly defers per-actor abuse bounding to this effort. Two abuse paths remain unaddressed:

**A. Primary-tag misattribution at post-promotion.** A post's `primary_tag` determines which subject (and thus which ancestor chain) earns XP when the post auto-promotes. An author dropping `finance` as primary on a waybar bug farms XP in `finance` through a post that has no legitimate finance content. The existing `FlagPost` mechanism can't defend against this: FlagPost requires the flagger to have XP in a tag *that's on the post*, so an `waybar`-XP-holder who notices the misattribution has no standing because `waybar` isn't on the post at all.

**B. `ProposeParent` adoption without abuse protection.** Brainstorm 027 §4.3 says post-bootstrap, parent adoption goes through "the curator-audit-gate sibling effort's challenge window + audit-jury resolution." That's a one-line sketch; this doc has to make it real. Without it, a `finance`-XP-holder racing `ProposeParent waybar → finance` locks the tree permanently (§4.4 immutability).

Beyond those two, this effort is also a hard prerequisite for brainstorm 027's activation flag to flip (§4.0). Until this ships, propagation stays dormant and the tree-fan-out-for-bug-incentives plan never materializes.

Scope:

1. **Tag-misattribution defense** at auto-promote time, leveraging the existing `auditing` contract's commit-reveal jury.
2. **`ProposeParent`** flow on the `subject` contract with a challenge window and audit-jury resolution.
3. Everything else (UI flows, automated detectors, post-audit-verdict XP rewards/penalties beyond what the audit contract already handles) is out of scope — drives the design toward reusing existing mechanics instead of inventing.

## 2. Existing mechanics to reuse

Reading the current contracts:

**`auditing` contract** (`contracts/auditing/src/msg.rs`) is mature: `RegisterAuditor { subjects }` (requires XP in those subjects), `Report { post_id, reason }`, `CommitVote { case_id, commit_hash }`, `RevealVote { case_id, vote, salt }`, `FinalizeCase`, `Appeal { case_id, subject }` with `appeal_cost` XP staked. Commit phase 8h, reveal 4h, appeal window 7d. Calls `forum` contract's `HoldPost`/`ApprovePost`/`RejectPost`/`ReopenPost` via `InternalMsg`.

**`forum` contract** (`contracts/forum/src/msg.rs`) has `FlagPost { content_hash, subject }` (XP-holder in one of the post's tags can flag, extends review), `AutoPromote`, plus `InternalMsg::{HoldPost, ApprovePost, RejectPost, ReopenPost, UpdateConfig}` reserved for the audit contract.

**What's missing** for this effort:

- Forum has no message that permits flagging a post based on the *absence* of a legitimate primary tag — only based on XP in a present tag.
- Forum `primary_tag` doesn't exist yet (brainstorm 027 §5 prerequisites introduces it).
- Subject contract has no `ProposeParent` or adoption-pending state.
- Audit contract's `Report { post_id, reason: String }` has a free-form reason string with no typed payload to carry a proposed-correct-primary-tag or a proposed-parent.

## 3. Proposed design

### 3.1 Tag-misattribution defense — `ReportTagMisattribution` via existing audit contract

Add one message to the auditing contract's `ExecuteMsg`:

```rust
ReportTagMisattribution {
    post_id: u64,
    /// The primary tag the reporter claims SHOULD apply instead.
    proposed_primary_tag: String,
    /// Reason text (shown to auditors).
    reason: String,
}
```

Semantics:

- **Standing gate: ≥3 XP in `proposed_primary_tag`'s subject.** Matches the existing `RegisterAuditor` threshold so standing costs real skin, not a trivially-farmed single post. Prevents single-XP bootstrap attacks where a one-post seeder auto-credentials to flag-farm.
- **Jury-pool precondition (submission-time only).** At submission, the audit contract queries XP-holders in current + proposed subjects. If the union (deduplicated) contains fewer than `MIN_JURY_POOL = 3` unique holders, `ReportTagMisattribution` rejects with `InsufficientJuryPool`. This handles the case where `proposed_primary_tag` was auto-created empty and has no holders. The check is **submission-time only** — by reveal phase, holders may have lost XP or unregistered as auditors. The standard reveal-timeout path (defaults to `Keep`, flagger stake burned) covers the case where the pool shrinks mid-case.
- **Stake.** Caller stakes `tag_dispute_cost: u64` XP in `proposed_primary_tag`'s subject. Bootstrap value = 1 (aligned with `N=1` bug-report payouts); governance-tunable. Stake is locked (not burned until verdict) using existing `LockExperience`/`BurnLocked`/`UnlockExperience` mechanics.
- Forum post enters held state via `InternalMsg::HoldPost` (existing machinery, no new forum message needed).
- **Pre- or post-promotion.** A misattribution report can be submitted either before AutoPromote has fired (post in held state blocks promotion entirely) or after (post is already on chain with XP minted to the wrong subject). For post-promotion reports, the `Correct` verdict triggers compensating transfers (see below) via internal audit → experience calls. This avoids the race where a report arrives after AutoPromote and the XP is stuck in the wrong subject.
- Commit-reveal proceeds with existing phases (8h + 4h).
- **Jury composition.** XP-holders in `primary_tag_current` ∪ `primary_tag_proposed` (deduplicated). The post's secondary tags (anything in `Post.tags` other than the primary tags at issue) are irrelevant for jury selection. A holder is included iff they have XP in at least one of the two candidate primary tags. No soft-exclusion or dual-XP carve-out — one clean rule, consistent with §3.2's adoption-jury rule.
- Vote options: `Keep` (current primary_tag is correct) | `Correct` (proposed_primary_tag is correct) | `Reject` (post should not promote at all, e.g. the post is spam).
- **Verdicts:**
  - **Keep**: flagger's staked XP is burned (consistent with appeal-loss mechanics). Pre-promotion: post auto-promotes as originally tagged. Post-promotion: no-op, existing XP stays put.
  - **Correct**: flagger's stake is returned. Pre-promotion: `InternalMsg::UpdatePrimaryTag { post_id, new_primary_tag }` called on forum, post auto-promotes with corrected tag. Post-promotion: atomic compensating flow via auditing → experience contract.
    - **Burn amounts are per-tx, not reconstructed.** Brainstorm 027 §5 generates one `ExperienceTransaction` per level at mint time, each with its own `amount` field (the `N >> k` value credited to that ancestor). The audit contract queries experience for all tx records matching `source_id = post_id.to_string()` and gets an exact list of `(subject, amount)` pairs to burn. The `ancestor_snapshot` duplicated on each record is useful for audit-trail reading, but the burn doesn't need to reconstruct from it — the per-level amounts are already recorded. No ambiguity about what to burn per level.
    - **Mint walk uses the current tree** for the new primary tag, applying the same tree-cut rule from brainstorm 027 §4.5.
    - **Saturating burn + debt queue.** At each ancestor level in the burn walk, the author's available balance may be lower than the amount originally minted there (they may have spent/locked/burned XP in the interim). Burn `actual = min(available_at_level, amount_originally_minted_at_level)`. The unrecovered residue `(amount_originally_minted - actual)` is NOT accepted as lost — it's written to a new `BURN_DEBT: Map<(Addr, String), u64>` in the experience contract. On every future `MintExperience` to the same `(author, subject)` pair, `BURN_DEBT` is consumed first: `credited = max(0, mint_amount - debt)`, with the debt reduced accordingly. This closes the iterated-farming attack: residue doesn't vanish, it queues against the author's future XP in that subject. Debt entries auto-delete on reaching zero.
    - Both BurnExperience and MintExperience sub-messages execute in one transaction using `SubMsg::new(...)` (default `ReplyOn::Never`). Per brainstorm 027's pinned semantics, default behavior is: sub-message failure propagates to the parent, and the parent tx reverts atomically. If either sub-message fails catastrophically (e.g., contract paused), the whole verdict application reverts. Saturating burns and debt writes do NOT trigger this revert; they're expected behavior within a non-failing sub-message path.
  - **Reject**: both flagger and author lose XP. Flagger stake burned. Pre-promotion: post rejected via existing `InternalMsg::RejectPost`. Post-promotion: author's minted XP is burned across the same per-tx record list (saturating + debt-queue semantics apply).
  - **Reveal-timeout (no quorum).** Reveal phase elapsed without enough auditors revealing a valid vote → no verdict. All stakes returned (flagger and author both unlocked, no burn). Case closes with `no_consensus` event. Flagger may re-file after the lock is released. This differs from the original draft (which defaulted to `Keep` and burned the flagger) — a liveness failure in the jury isn't the flagger's fault, so stake-burn would weaponize jury-unavailability as a grief vector against honest flaggers.

**Why this works:**

- Standing gate (XP-in-proposed-subject) keeps the flood bounded without introducing yet another rate limit.
- Stake + burn makes honest-but-wrong flags cost something; makes dishonest flags expensive.
- Jury selection from *both* affected subjects is the only fair adjudication — picking only from the current tag's subject would let author-friendly auditors rubber-stamp.
- Reuses every existing audit-contract state transition. One new message, one new audit verdict variant, one new forum internal message. Small surface.

**Why not extend `FlagPost`:** the existing FlagPost is intentionally cheap (no stake, just XP-in-tag standing) because it's for "this post is bad" — a shallow veto. Tag-misattribution needs deeper adjudication; the jury/commit-reveal path is already sized for that and FlagPost isn't.

### 3.2 `ProposeParent` — adoption with challenge window

The subject contract adds:

```rust
// State
pub const PENDING_ADOPTIONS: Map<&str, PendingAdoption> = Map::new("pending_adoptions");

pub struct PendingAdoption {
    pub proposed_parent: String,
    pub proposer: Addr,
    pub challenge_deadline: u64,       // block time in seconds
    pub challenged: bool,              // set true when a counter-proposal lands
    pub challenge_case_id: Option<u64>, // populated if an audit case opens
    /// Snapshot of governance-tunable params at propose-time.
    /// ChallengeAdoption checks against THESE values, not current config,
    /// so raising standing/cost mid-window doesn't retroactively lock out
    /// a would-be challenger who qualified when the proposal was filed.
    pub snapshot_standing_min_xp: u64,
    pub snapshot_propose_cost: u64,
}

// Constants (all governance-tunable via UpdateConfig)
pub const ADOPTION_CHALLENGE_WINDOW: u64 = 604_800;      // 7 days, matches appeal_window
pub const ADOPTION_PROPOSE_COST: u64 = 1;                // bootstrap value
pub const ADOPTION_COOLDOWN_AFTER_NEITHER: u64 = 2_592_000; // 30 days; cooldown applies to the specific (tag, p1, p2) triple that NeitherWins'd, not to the tag at large — legit third-party proposals with different parents proceed immediately
pub const ADOPTION_STANDING_MIN_XP: u64 = 1;             // bootstrap value; raise via governance once XP supply grows
pub const ADOPTION_MAX_AGE: u64 = 5_184_000;             // 60 days; after this, Finalize burns proposer stake as Abandoned

// ExecuteMsg additions
ProposeParent { tag: String, proposed_parent: String },
ChallengeAdoption { tag: String, counter_parent: String },
FinalizeAdoption { tag: String }, // permissionless crank after deadline
```

Additional state for cooldowns:

```rust
// Keyed on (tag, proposed_parent, counter_parent) triple (as a composite string key),
// NOT on tag alone. Preserves third-party legitimate proposals after a grief NeitherWins.
// Encoding: format!("{tag}|{p1}|{p2}") with p1, p2 lexicographically sorted so the pair
// is direction-independent (grief pair swapping roles doesn't bypass the cooldown).
pub const ADOPTION_COOLDOWNS: Map<&str, u64> = Map::new("adoption_cooldowns"); // triple_key -> cooldown_end_time
```

Flow:

1. **Propose.** `ProposeParent { tag, proposed_parent }`:
   - Global `BOOTSTRAP_WINDOW_OPEN` must be `false` (cross-contract query from subject contract's own state, not from experience contract). During bootstrap, seeding is `AdminSeedParent`'s job, not `ProposeParent`'s.
   - Target subject must be orphan (`parent_tag.is_none()`).
   - No existing pending adoption on this tag.
   - Triple-key `(tag, min(p1,p2), max(p1,p2))` not in `ADOPTION_COOLDOWNS` with expiry > now. For a fresh `ProposeParent` (no challenger yet) this is a no-op check — triples are only written to cooldowns by a `NeitherWins` finalization (§3). A later propose with a different `proposed_parent` is unaffected by prior NeitherWins on a different pair. A re-propose identical to a prior NeitherWins pair is also unaffected *at propose time*, but if challenged by the same counter_parent, the triple key matches and `ChallengeAdoption` rejects until cooldown expires.
   - Proposer must hold ≥ `ADOPTION_STANDING_MIN_XP` XP in `proposed_parent`'s subject (standing, matches RegisterAuditor threshold).
   - Proposer stakes `ADOPTION_PROPOSE_COST` XP in `proposed_parent`'s subject (locked via experience contract).
   - Cycle + depth checks run (same as `CreateSubject` and `AdminSeedParent`).
   - Write `PENDING_ADOPTIONS[tag] = PendingAdoption { ... }` with `challenge_deadline = now + ADOPTION_CHALLENGE_WINDOW`.

2. **Challenge** (optional, within window). `ChallengeAdoption { tag, counter_parent }`:
   - Pending adoption must exist, be unfinalized, and `now < challenge_deadline`.
   - `counter_parent` must differ from `proposed_parent`.
   - Challenger stakes `PendingAdoption.snapshot_propose_cost` in `counter_parent`'s subject and must hold ≥ `PendingAdoption.snapshot_standing_min_xp` XP there. Uses the snapshot from propose-time, not current config — governance raising the params mid-window doesn't retroactively disqualify.
   - Opens an audit case via a new auditing-contract message: `ReportAdoptionChallenge { tag, proposed_parent, counter_parent, proposer, challenger }`.
   - Marks `challenged = true`, records `challenge_case_id`.
   - Only one challenge per pending adoption. Rationale: binary contests are tractable for commit-reveal; N-way ranked voting would need a voting-mechanism overhaul. Third-community claims surface on re-propose after the 30-day cooldown (see NeitherWins path below).

3. **Finalize** (permissionless crank). `FinalizeAdoption { tag }`:
   - **Abandonment**: if `now ≥ challenge_deadline + ADOPTION_MAX_AGE` (60 days), treat as `Abandoned`: proposer stake burned, parent stays None, pending deleted. Incentivizes the proposer (or any interested party) to crank Finalize promptly — abandonment is not free. Storage auto-reclaimed.
   - **Unchallenged path**: `challenged == false` and `challenge_deadline ≤ now < challenge_deadline + ADOPTION_MAX_AGE`: write `Subject.parent_tag = Some(proposed_parent)`, append to `SUBJECT_CHILDREN[proposed_parent]`, unlock + return proposer stake, delete pending. Subject is now immutably parented per brainstorm 027 §4.4.
   - **Challenged path — audit verdict received**: query the audit case. Verdict options: `ProposedWins` | `CounterWins` | `NeitherWins`.
     - `ProposedWins`: proposer's stake returned, challenger's stake burned. `parent_tag = Some(proposed_parent)`.
     - `CounterWins`: challenger's stake returned, proposer's stake burned. `parent_tag = Some(counter_parent)`.
     - `NeitherWins`: both stakes burned. `parent_tag` stays `None`. Writes `ADOPTION_COOLDOWNS[(tag, sorted_pair)] = now + ADOPTION_COOLDOWN_AFTER_NEITHER` (30-day cooldown on the specific triple). Third-party proposals with a *different* parent proceed immediately; only the exact grief pair is locked out.
   - **Challenged path — audit reveal phase times out with no quorum**: treated as `NeitherWins`. Both stakes burned, 30-day cooldown applied. This is the explicit deadlock resolution: if there aren't enough auditors in (proposed ∪ counter ∪ target) subjects to hit quorum, adoption fails safe to orphan state rather than locking the tag forever.

**Jury selection for challenged adoptions:** XP-holders in `proposed_parent`'s subject ∪ `counter_parent`'s subject, **excluding** target-subject XP-holders. Target-subject holders' XP fans out differently depending on the verdict, which creates a monetized private preference — and commit-reveal hides votes until reveal, so a side-payment ("vote X, I'll pay you Y off-chain") is unobservable on-chain. Excluding target-subject holders forfeits some domain expertise, but the rent-extraction vulnerability of including them is strictly worse than the dilution argument admits. Proposer and challenger can channel domain knowledge through their `reason` text and through the commit-reveal jury's own research — they just can't vote on the case directly via their target-subject XP.

**Why a 7-day challenge window?**

- Matches the existing appeal window (`appeal_window = 604_800`) for operational consistency — operators, monitoring, and dashboards already reason in 7-day terms.
- Long enough that an interested counter-parent community can realistically notice a misaimed adoption and respond.
- Not so long that the tree stays in limbo indefinitely while contributors wait to earn propagation XP.

### 3.3 Relationship to the propagation-activation flag (brainstorm 027 §4.0)

For `SetPropagationEnabled(true)` to pass the cw2 `ContractInfo` check, this effort's deployed audit-gate must register as `"crates.io:os-forum-audit-gate"`. But there is no new contract — the audit-gate mechanics live on the *existing* auditing contract (`os-auditing`) plus additions to subject + forum.

Resolution: **rename the auditing contract** is disruptive and wrong. Instead, the "audit gate" for propagation purposes is satisfied by the auditing contract advertising the `ReportTagMisattribution` capability. The experience contract's identity-check (brainstorm 027 §4.0 item 1) is relaxed to accept the existing auditing contract name plus a feature-flag query: `AuditCapabilities {} -> { tag_misattribution: bool, adoption_challenge: bool }`. Both must return true before propagation can activate. This keeps the identity-check on-chain and doesn't require a fake standalone contract.

Concretely, auditing contract adds:

```rust
pub enum QueryMsg {
    // ... existing ...
    #[returns(CapabilitiesResponse)]
    AuditCapabilities {},
}

pub struct CapabilitiesResponse {
    /// Schema version for forward compatibility. Bumped when fields are added/removed.
    pub version: u32,
    pub tag_misattribution: bool,     // true once ReportTagMisattribution handler exists
    pub adoption_challenge: bool,      // true once ReportAdoptionChallenge handler exists
}
```

The `version` field exists so the experience contract's flip-to-true gate can assert a minimum compatible version (`version >= MIN_AUDIT_CAPABILITIES_VERSION`) rather than blindly decoding into a struct that might have drifted. If a future effort adds a third bool, bump `version` and experience contract refuses the flip until its own constant is raised through an experience-contract migration — explicit version gating, not silent-decode-failure.

**Upgrade ordering.** When either contract migrates, land migrations in this order: (1) audit contract migration first (bumps `version` in the capability response), (2) then experience contract migration if it needs to raise `MIN_AUDIT_CAPABILITIES_VERSION`. Submitting the experience migration first creates a window where flip-to-true fails because the old audit contract still reports the old `version`. Not a deadlock (eventual convergence once both land), but documented here so the governance process sequences proposals correctly.

Experience-contract flip-to-true gate becomes:

1. `AUDIT_GATE_CONTRACT` is `Some(addr)`.
2. cw2 `ContractInfo` query returns `contract == "crates.io:os-auditing"`.
3. `AuditCapabilities {}` returns `version >= MIN_AUDIT_CAPABILITIES_VERSION` AND both capability flags true.

Replaces brainstorm 027 §4.0 item 1's `"crates.io:os-forum-audit-gate"` string, which was a placeholder.

## 4. Implementation sketch

**`auditing` contract changes:**
- Add `ReportTagMisattribution { post_id, proposed_primary_tag, reason }` execute msg. Enforces: standing check (≥3 XP in proposed), stake lock, jury-pool precondition (current ∪ proposed has ≥3 unique holders), and one-active-case-per-post serialization (rejects if any other case is active on `post_id`, including existing `Report` or `FlagPost`-derived holds).
- Add `ReportAdoptionChallenge { tag, proposed_parent, counter_parent, proposer, challenger }` (only callable by subject contract).
- Extend `AuditVote` enum with case-type-aware variants: `Keep | Correct | Reject` for misattribution; `ProposedWins | CounterWins | NeitherWins` for adoption. Original `pass | reject` remains for generic `Report` cases.
- Record `case_type` on each `AuditCase` so `FinalizeCase` dispatches to the right resolution (and rejects votes with wrong variant for the case type).
- **Strict one-case-per-post + per-post refile cooldown.** Module-level guards:
  - `CASE_BY_POST: Map<u64, u64>` (post_id → active case_id). `ReportTagMisattribution` or `Report` rejects if `post_id` has an entry.
  - `MISATTRIBUTION_COOLDOWN: Map<u64, u64>` (post_id → cooldown_end). Set to `now + 86400` (24h) when any `ReportTagMisattribution` case closes with `no_consensus`, `Keep`, or `Correct`. New misattribution filings on that post are rejected until the cooldown expires. `Reject` verdicts don't set a cooldown because the post is already gone.
  - Rationale: without the cooldown, a flagger who causes their own jury to never reveal can keep a post Held indefinitely at zero cost — file → 12h timeout → refund → refile → repeat. The 24h cooldown caps hold-duration per (post, 24h window) to one case, so infinite-hold becomes 50% uptime at most even under worst-case grief.
  - No subsumption carve-out for spam: spam Reports during an active misattribution case wait their turn. Allowing subsumption was dropped because a fake spam-Report was a free cancellation primitive against honest flaggers.
- **FlagPost is orthogonal to audit cases.** `FlagPost` (on forum) extends the review window; it does NOT open an `AuditCase`, does not touch `CASE_BY_POST`, and does not block `ReportTagMisattribution`. Post states become:
  - `UnderReview` (pre-promotion): FlagPost resets the review timer. Can coexist with a misattribution `AuditCase` (which transitions the post to `Held`).
  - `Held` (promotion blocked by audit): FlagPost rejects — nothing to extend, auto-promote isn't running.
  - `Promoted`: FlagPost rejects. ReportTagMisattribution and Report still allowed (case opens on Promoted post; forum's `HoldPost` is accepted in Promoted state — this is a forum-contract prerequisite for this effort).
- **Reveal-timeout semantics for new case types.** If reveal phase elapses without quorum:
  - Misattribution: `no_consensus` — all stakes returned, no verdict, case closes. Flagger can refile. This changed from an earlier draft that defaulted to `Keep` + flagger-stake-burned; that design weaponized jury-unavailability against honest flaggers (an attacker causes their own jury to not reveal, burning the flagger's stake for free). Liveness failure is no one's fault.
  - Adoption challenge: `NeitherWins` *for the specific triple* — both stakes burned, 30-day cooldown written on `(tag, sorted_pair)`. Third parties can propose with a different parent immediately.
- Jury-selection helper that queries XP holders across one, two, or three subjects (deduplicated).
- `AuditCapabilities` query with version field.
- Stake lock/burn mechanics reuse existing experience-contract `LockExperience`/`BurnLocked`/`UnlockExperience` calls.
- **Post-promotion Correct verdict:** audit contract emits an internal-call sequence to experience contract: `BurnExperience` the full ancestor chain of the old primary_tag, then `MintExperience` the new chain. Both walks bounded at `MAX_TAG_DEPTH = 8`. Atomic via a single tx (failure of either step reverts the verdict application).

**`forum` contract changes:**
- Add `primary_tag: String` to `Post` (brainstorm 027 §5 prereq 1; lives in THIS effort as deliverable).
- Populate `primary_tag = tags[0]` at `CreatePost`, frozen after.
- Add `InternalMsg::UpdatePrimaryTag { post_id, new_primary_tag }` callable by auditing contract after a `Correct` verdict.
- `AutoPromote` continues to use `primary_tag`, not `tags[0]`, so the experience-contract mint targets the frozen (and possibly corrected) primary.
- **`HoldPost` must accept posts in `Promoted` state, not only `UnderReview`.** Pre-existing `HoldPost` was designed assuming holds block auto-promotion; this effort extends it to also hold already-promoted posts for post-hoc misattribution correction. Behavior on Held-while-Promoted: post's chain presence stays but new upvotes/interactions are blocked until `ApprovePost` or `RejectPost` fires. Without this change, post-promotion `Correct` verdicts can't be applied and the whole post-promotion path breaks.

**`experience` contract changes:**
- Add `BURN_DEBT: Map<(Addr, String), u64>` — tracks unrecovered burn residue per `(user, subject)` pair. Consumed first on any subsequent `MintExperience` to that pair. Entry auto-deleted on reaching zero. One new internal entry-point `RecordBurnDebt { user, subject, amount }` callable only by the auditing contract for the saturating-burn residue path.
- Extend `MintExperience`: before crediting, subtract outstanding `BURN_DEBT[(user, subject)]` from the incoming amount; credit `max(0, amount - debt)` and reduce the debt record by `min(amount, debt)`. This is the per-level consumption: when brainstorm 027's propagation mints fan up the ancestor chain, each ancestor's credit is reduced by that ancestor's outstanding debt first. The subject contract's `AddTotalExperienceBatch` sub-message (027 §5) is invoked with the NET credited amounts, not the gross — so the subject-level `total_experience` counter only reflects actual net-new credits.
- Extend `ExperienceTransaction` (already being extended by 027 for `regime` and `ancestor_snapshot`): no further fields needed — the existing per-level `amount` is the source of truth for the compensating burn, and debt-consumed credits are reflected in the per-level `amount` being written.

**Debt consumption during propagation — worked example.** Author has `BURN_DEBT[(alice, os)] = 3` from a prior Correct-verdict saturating burn. Alice posts a legit bug primary-tagged `waybar`, tree is `waybar → gui → os → linux`, auto-promote mints `N=8`:
- Leaf `waybar`: debt 0, credit = 8, tx records `amount: 8`.
- `gui`: debt 0, credit = `8 >> 1 = 4`, tx records `amount: 4`.
- `os`: debt = 3, incoming = `8 >> 2 = 2`. Net credit = `max(0, 2 - 3) = 0`, debt becomes `3 - min(2, 3) = 1`. Tx records `amount: 0` (net). Subject contract's batch entry for `os` is `(os, 0)`.
- `linux`: debt 0, credit = `8 >> 3 = 1`, tx records `amount: 1`.

Net: Alice gets 8 in `waybar`, 4 in `gui`, 0 in `os` (debt absorbed), 1 in `linux`. Her remaining `os` debt is 1. The next `os`-level credit will consume it in full.

This is intended cross-contamination: debt represents XP the author owed to a subject that couldn't be recovered at burn time. Future earnings in that subject pay it back. The author's net ledger over time is correct; individual post earnings may be reduced.

**Debt state bloat.** `BURN_DEBT` entries are bounded by `(author × subject)` pairs the author has ever earned XP in. Not unbounded — scales with actual system activity, not with attacker will. Pruned on reaching zero (see `MintExperience` change above). Abandoned debts (author never mints in that subject again) persist but are a bounded cost proportional to real activity, not a DoS surface.

**`subject` contract changes:**
- Add `PENDING_ADOPTIONS` map + `PendingAdoption` struct (with governance-param snapshots).
- Add `ADOPTION_COOLDOWNS: Map<&str, u64>` keyed on the composite `(tag, sorted_pair)` string.
- **Retention / lazy cleanup.** `ADOPTION_COOLDOWNS` entries never need active pruning: on every read that sees `expiry <= now`, delete the entry in the same tx (lazy garbage collection). `PENDING_ADOPTIONS` entries are deleted on successful `FinalizeAdoption`; stuck entries (proposer's audit case deadlocks, etc.) are pruned by the same `FinalizeAdoption` crank once the audit case's reveal-timeout `NeitherWins` fires, which is permissionlessly crankable. `CASE_BY_POST` in auditing contract is cleared on `FinalizeCase` including timeout finalizations.
- Add constants: `ADOPTION_CHALLENGE_WINDOW`, `ADOPTION_PROPOSE_COST`, `ADOPTION_COOLDOWN_AFTER_NEITHER`, `ADOPTION_STANDING_MIN_XP` (all governance-tunable via `UpdateConfig`).
- Add `ProposeParent`, `ChallengeAdoption`, `FinalizeAdoption` execute msgs.
- `ProposeParent` reads the same `BOOTSTRAP_WINDOW_OPEN` item as `AdminSeedParent`; rejects when open. (That item lives in the subject contract itself per brainstorm 027 §5, so the check is a local state read, not a cross-contract query.)
- Also rejects when `ADOPTION_COOLDOWNS[tag]` is present and greater than `env.block.time`.
- On `FinalizeAdoption` success, the `parent_tag = Some` write is the final, immutable transition per 027 §4.4 — no further modifications allowed by any mechanism in this contract.

## 5. Tests

- Happy path tag misattribution: `Correct` verdict → primary_tag updated, stakes returned, post auto-promotes with new tag.
- `Keep` verdict → flagger stake burned, post auto-promotes unchanged.
- `Reject` verdict → both stakes burned, post rejected.
- Standing gate: `ReportTagMisattribution` by someone with 0 XP in `proposed_primary_tag` rejects.
- Stake sufficiency: `ReportTagMisattribution` with insufficient XP to lock rejects.
- `ProposeParent` happy path unchallenged: after 7 days, `FinalizeAdoption` cranks and `parent_tag = Some`.
- `ProposeParent` challenged, `ProposedWins`: parent set to proposed, challenger stake burned.
- `ProposeParent` challenged, `CounterWins`: parent set to counter, proposer stake burned.
- `ProposeParent` challenged, `NeitherWins`: parent stays None, both stakes burned.
- Double `ProposeParent` on same pending: rejects (pending already exists).
- `ProposeParent` on already-parented subject: rejects.
- `ProposeParent` during bootstrap window: rejects.
- `ChallengeAdoption` after deadline: rejects.
- `ChallengeAdoption` with same parent as proposed: rejects.
- `AuditCapabilities` returns `{tag_misattribution: true, adoption_challenge: true}` after this effort ships; `{false, false}` on pre-effort auditing contracts.
- Experience contract's `SetPropagationEnabled(true)` passes with this audit contract registered; fails if audit contract is a pre-effort version (capabilities false).

## 5.1 Bootstrap-XP tension

Brainstorm 027 §4.0 says propagation activates only after parents are seeded. This effort's `ProposeParent` is the mechanism for seeding parents *post-bootstrap* (during bootstrap, `AdminSeedParent` does the seeding). But at the moment the bootstrap window closes and propagation activates, most accounts have only 1–2 XP in any single subject (per current chain state). Setting `ADOPTION_STANDING_MIN_XP = 3` at launch would make `ProposeParent` dead-on-arrival — no one could call it.

Resolution: launch with `ADOPTION_STANDING_MIN_XP = 1`. Raise to `3` (matching `RegisterAuditor`) via governance once the XP economy has matured. This is an accepted weakness at bootstrap: a single-XP attacker can file adoption proposals. The stake cost + 7-day challenge window + audit-jury resolution still defend against bad-faith adoption, just more expensively. The audit-jury's quorum is the real defense — standing is a convenience filter. Document the intent to raise so future governance knows the target.

## 6. Open questions

- **Q1: Should `Correct` verdict reward the flagger with XP in the newly-correct subject?** Tempting (incentivizes vigilance) but adds an XP-source outside of post contributions. Default zero; revisit.
- **Q2: Should the jury for adoption disputes include auditors from the target subject (the one being adopted)?** E.g. disputed `waybar → gui` vs `waybar → os`: include `waybar`-XP-holders in jury? Argument for: they have the most at stake. Argument against: they're self-interested (their XP will fan out differently based on the parent). Default: exclude target-subject XP-holders from jury; proposer's and challenger's subjects only.
- **Q3: What if the audit case on a challenged adoption deadlocks (insufficient quorum, reveal timeout)?** Existing audit contract has quorum/reveal semantics; if jury fails to reach consensus, `NeitherWins` by default — stakes burned, subject stays orphan. Re-propose is allowed.
- **Q4: Double-flagging on the same post.** Should `ReportTagMisattribution` allow multiple simultaneous reports with different proposed-primary-tags? Simpler to allow only one active misattribution case per post at a time.

## 7. Handoff

Critic-chain this doc. On convergence, the implementation can land in `forum-tag-tree-implementation` alongside the semantics changes, OR in a standalone sub-effort if scope demands. Brainstorm 027's §4.0 item 1 gets updated to reference the `AuditCapabilities` check described in §3.3 above.
