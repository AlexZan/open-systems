# 027 — Forum Tag Tree & XP Propagation (Design)

**Effort:** `forum-tag-tree-semantics-design`
**Parent:** `forum-tag-tree-xp-propagation`
**Sibling:** `forum-tag-curator-audit-gate` (abuse gate — separate doc)
**Status:** Draft v1
**Created:** 2026-04-19

---

## 1. Problem

The bug-incentive mechanic that's meant to make friends want to hunt bugs assumes XP fans out up a tag hierarchy: tagging a bug `waybar` credits `gui`, `os`, and `linux` too. Without that fan-out, the incentive loop collapses to one-XP-per-bug and reporters have no reason to tag carefully. Misattribution (dropping `finance` on a waybar bug to farm) is the primary abuse vector.

Current reality, verified by reading the contracts:

- `subject` contract **already has** `parent_tag: Option<String>` on `Subject`, a `SUBJECT_CHILDREN: Map<&str, Vec<String>>` index, a `SubjectChildren` query, and a parent-existence check on `CreateSubject` (`contracts/subject/src/contract.rs:100-113`).
- **But**: the `experience` contract mints XP to a single `subject` string only (`mint_experience_internal`, `contracts/experience/src/contract.rs:250-320`). No ancestor walk. No propagation.
- **And**: `EnsureSubjectsExist` auto-creates missing subjects with `parent_tag: None` (`contracts/subject/src/contract.rs:142-160`), so every subject organically created from forum posts is an orphan at the root of the tree. Today's chain state — 6 subjects, all root-level — reflects this.
- **And**: `CreateSubject` doesn't check for cycles (`A → B → A`) or depth bounds. The parent-existence check alone doesn't guarantee a well-formed tree.

So the tree infrastructure exists but XP doesn't use it, and what little gets created from posts is flat anyway.

## 2. Scope of this doc

Four questions, in order of impact:

1. **Propagation rule** — who gets XP when a contribution is credited to a leaf subject?
2. **Tree shape** — single-parent (tree) or multi-parent (DAG)? Depth cap? Cycle prevention?
3. **Orphan-fix** — how do auto-created subjects get parents?
4. **Mutability** — can a subject's parent change after creation? Under what rules?

Out of scope (sibling effort `forum-tag-curator-audit-gate`): the curator-audit gate that prevents tag farming at post-approval time. This doc assumes the tree is trustworthy; that effort is how we make it so.

## 3. Current state — exact API surface

Relevant snippets from the contracts:

```rust
// contracts/subject/src/state.rs
pub const SUBJECTS: Map<&str, Subject> = Map::new("subjects");
pub const SUBJECT_CHILDREN: Map<&str, Vec<String>> = Map::new("subject_children");

pub struct Subject {
    pub tag: String,
    pub parent_tag: Option<String>,
    // ...
    pub total_experience: u64,
}
```

```rust
// contracts/subject/src/msg.rs
InternalMsg::AddTotalExperience { tag: String, amount: u64 }
InternalMsg::EnsureSubjectsExist { tags: Vec<String> }  // creates with parent_tag=None
```

```rust
// contracts/experience/src/contract.rs (mint_experience_internal)
BALANCES.save(deps.storage, (user, subject), &new_balance)?;  // single subject
// ... notifies subject contract: AddTotalExperience { tag: subject, amount }
```

The experience contract notifies the subject contract for exactly one tag. No loop, no walk.

## 4. Proposed design

### 4.0 Activation gate — code ships now, economic activation waits

This is a prerequisite for every other subsection. The subject + experience contract changes below ship as code, but their propagation behavior is guarded by an on-chain `propagation_enabled: Item<bool>` in the experience contract, **default `false`**. When the flag is false, `MintExperience` behaves exactly as today: single-subject only, no ancestor walk, no parent reads.

`SetPropagationEnabled(true)` does **not** rely on human trust that the prerequisites are met. The experience contract asserts all of the following on-chain before accepting the flip, and rejects otherwise:

1. **Audit gate is registered AND identity-checked.** `AUDIT_GATE_CONTRACT: Item<Option<Addr>>` is `Some(addr)`, AND a cw2 `ContractInfo` query to that address returns a `contract` field matching the expected `"crates.io:os-forum-audit-gate"`. A stub or malicious address that merely exists will not self-identify correctly and fails the check. Version pinning (minimum compatible version) is enforced the same way.
2. **Tree is non-trivially seeded.** Cross-contract query to the subject contract confirms:
   - At least `MIN_SEEDED_PARENTS = 3` subjects have `parent_tag.is_some()`, AND
   - At least one of those parented subjects has depth ≥ 2 (i.e. its own parent is also parented, proving a real hierarchy exists and not just three flat adoptions).
3. **Bootstrap window must already be closed on any flip after the first.** For the first-ever flip to `true`, this is vacuously true because the flip closes the window as part of its own commit (via atomic sub-message, §5). For every subsequent `true`-flip (after an intervening `false`-flip), `BOOTSTRAP_WINDOW_OPEN == false` is an explicit precondition. This enforces the invariant "once propagation has ever been true, bootstrap is closed forever" at the flag contract directly, not by chain of sub-message reliance.

Flipping back to `false` is always permitted (governance can disable propagation without prerequisites). Each flip emits an event and advances a monotonic `PROPAGATION_REGIME: Item<u32>` counter so historical mint transactions can be attributed to a specific regime window (see §5, `ExperienceTransaction.regime`).

**Concurrent seed/flip.** CosmWasm serializes tx execution within a block. An `AdminSeedParent` tx and a `SetPropagationEnabled(true)` tx in the same block execute in block-included order: seed-first → seed succeeds, flip sees updated parented count; flip-first → flip's atomic commit closes the window, subsequent seed tx fails with `BootstrapWindowClosed`. Both orderings are well-defined; clients should not assume either.

### 4.1 Propagation rule — primary tag only, geometric decay

Once `propagation_enabled = true`, each post declares **one primary tag** (the first tag, enforced by the forum contract per §5 Prerequisites). Secondary tags exist for discoverability but earn no XP. When a contribution mints `N` XP on the primary tag `t`:

- Walk up `t.parent_tag` chain.
- Level 0 (leaf `t`): user gets `N` XP, capped at the subject's taper factor (existing genesis mechanic).
- Level 1 (parent): user gets `N/2` XP.
- Level 2 (grandparent): user gets `N/4` XP.
- ... until the root is reached or depth cap hit.

Integer math: `amount_at_level_k = N >> k` (right shift, saturating at 0). With the current `N = 1` bug-report payout, the reporter gets 1 at the leaf, 0 everywhere upstream. That's fine — the first meaningful propagation kicks in when `N ≥ 2`. Larger contributions (audits, curated posts) can mint `N = 4` or `N = 8` and get natural multi-level propagation without extra parameters.

**Why this rule:**

- **Honest declaration.** Forcing a primary tag makes tag choice accountable. The curator-audit gate has one claim to verify instead of a set.
- **No multi-tag farming.** Secondary tags earn no XP, so tagging `finance, waybar, cooking` on a bug is just spam, not a payday.
- **Bounded per-mint issuance.** Geometric series sums to `< 2N` — this is an **upper bound**. Per-level tapers (when a level is still in genesis) and orphan-roots (walk stops early) only reduce actual issuance below the bound; they never exceed it. Auditors model the system economics without worrying about tree shape.
- **Per-mint bound, not per-actor.** One actor can still mint multiple times across distinct posts. That is precisely the attack the curator-audit-gate (sibling effort) exists to bound — rate-limiting happens at post-approval, not at XP-mint. This design does not try to solve multi-post farming inside propagation; propagation only guarantees the per-mint bound.
- **Governance-tunable later.** The decay base (currently 2, i.e. halving) can be moved to on-chain state once we have evidence of need.

Rejected alternatives:

- **Flat 1-XP-to-every-ancestor (linear):** gaming incentive to lobby for deeper trees; unbounded total issuance.
- **All tags, no primary:** rewards tag-stuffing; abuse vector per above.
- **Capped N-ancestors-at-1:** arbitrary cliff; harder to reason about.
- **Decay per-level-configurable per-subject:** premature surface area, invites lobbying.

### 4.2 Tree shape — single-parent tree, depth cap 8, cycle check

- **Single parent** (`parent_tag: Option<String>`) — already the data model. DAG is tempting for `waybar under gui AND linux` but:
  - Doubles propagation cost (two paths to walk).
  - Requires visited-set for cycle detection.
  - Makes "primary ancestor chain" ill-defined for XP math.
  - Defer. Frontend can display cross-links as metadata without the contract caring.
- **Depth cap: 8.** At `CreateSubject`, walk up from claimed parent; if depth ≥ 8, reject. Bounds gas cost of propagation (~8 contract-internal calls per mint). Arbitrary but far beyond any real taxonomy.
- **Cycle check.** Walk up from claimed parent; if the walk revisits the new tag, reject. Cheap, same walk as the depth check.
- **Depth is monotonic at a subject.** Because `parent_tag` is immutable after creation (§4.4), a subject's distance to root is fixed at create time. New children can be added under it, extending the tree *downward*, but a mint walks parents (upward), so newly-added descendants can never affect an existing subject's mint walk. The create-time depth-8 check is therefore sound forever, not just at the instant of creation — no runtime re-validation needed, no concurrent mint/create race.

Add these checks to `execute_create_subject`:

```rust
// after existing parent-existence check
let mut cur = parent_tag.clone();
let mut depth = 1usize;
while let Some(p) = cur {
    if p == tag {
        return Err(ContractError::CycleDetected { tag });
    }
    if depth > MAX_TAG_DEPTH {  // MAX_TAG_DEPTH = 8
        return Err(ContractError::TreeTooDeep { tag });
    }
    cur = SUBJECTS.load(deps.storage, &p)?.parent_tag;
    depth += 1;
}
```

### 4.3 Orphan-fix — bootstrap + audit-gated adoption

There is a bootstrapping circularity: propagation is gated on a seed parent-map existing, but the sibling effort's `ProposeParent` hasn't shipped when we need to seed. This design breaks the circularity with a two-window model:

**Bootstrap window (this effort).** Subject contract gains `AdminSeedParent { tag, parent }`, callable by the admin OR by an authorized caller (governance). Semantics:

- Only valid when `Subject.parent_tag.is_none()` — pure orphan adoption, no reparenting.
- Cycle and depth checks run same as `CreateSubject` (§4.2).
- Available *only* during the bootstrap window: closes permanently the first time `propagation_enabled` flips to `true` (or explicitly via `CloseBootstrapWindow`, admin-or-governance, irreversible).

This lets governance seed the initial parent-map before propagation activates, using the trusted governance path rather than requiring the sibling contract to be deployed first.

**Post-bootstrap window (sibling effort).** Once the bootstrap window is closed, the ONLY way `Subject.parent_tag` ever becomes `Some` is via the sibling `forum-tag-curator-audit-gate` effort's `ProposeParent` flow, which is gated by:

- Proposer must be an XP-holder in a plausible parent (the sibling effort defines "plausible").
- Proposal enters a challenge window during which any XP-holder in a competing plausible parent can counter-propose.
- Unchallenged at deadline → adoption finalizes.
- Challenged → resolution via the audit contract's commit-reveal jury, with stake on the losing side slashed.

The challenge window directly addresses the adoption-race critique: a single curator with XP in `finance` cannot lock `waybar → finance` by racing a `ProposeParent`, because other XP-holders have a challenge window to respond, and the ultimate resolution is an audit-jury vote rather than first-mover-wins.

For `EnsureSubjectsExist` (auto-created orphans from posts): no change. Auto-created subjects stay at the root until seeded (bootstrap window) or adopted (post-bootstrap).

### 4.4 Mutability — adoption-only; no reparenting; deprecated ≠ locked

Three distinct states for `Subject.parent_tag`, kept clean:

- **Orphan** (`None`): subject exists, no parent set. Can be adopted exactly once, via the mechanisms in §4.3.
- **Parented** (`Some(p)`): immutable. Reparenting (`Some → Some'`) is **out of scope for this effort** and is intentionally locked out at the contract level. Changing a parent retroactively shifts who-earned-XP-from-what-ancestor, poisoning the audit trail. If a real reparenting need ever arises, it's a future effort with governance-only mechanics, explicit event logging, and explicit no-backfill semantics.
- **Deprecated** (`deprecated_at: Some(t)`): orthogonal to `parent_tag`. A deprecated subject keeps its parent link intact (so descendants' walks still traverse through it), but does not accumulate new `total_experience` or `total_users` counts. See §4.5 for deprecation semantics during mint.

This structure resolves the ambiguity: adoption is not mutation, and deprecation is not "gone" — it's "frozen."

### 4.5 Deprecation semantics during mint — tree-cut, not skip

Deprecation is a structural signal ("this category is no longer meaningful"), not just a filter. Propagating through a deprecated ancestor would keep that severed category alive by crediting its own ancestors via its descendants. The cleaner semantic is **tree-cut at first deprecated ancestor**:

- **Leaf (primary tag) is deprecated:** mint completes as a no-op (zero XP written anywhere, transaction succeeds with a `deprecated_leaf` event). Posts with frozen `primary_tag` pointing at a later-deprecated subject do not brick; they simply stop earning.
- **Mid-chain ancestor is deprecated:** the walk halts at that ancestor. Levels strictly above the deprecated ancestor do not receive XP. Levels strictly below still receive their (pre-cut) share.
- Rationale: if `gui` is deprecated between `waybar` and `os`, then `os` should not receive XP via `waybar`-contributions funneling through a severed category. `waybar` still gets its own direct XP; the cut is real.
- `AddTotalExperienceBatch` (§5) applies the batch as filtered by the experience contract (which does the walk and the cut); the subject contract receives only non-deprecated entries up to the cut.

**Invariant: subjects are create-only.** Deprecation is the terminal state for a subject — there is no "delete subject" operation anywhere in the contract surface. This invariant is what lets mint treat `missing` as a bug (transaction-reverting) while `deprecated` is normal (tree-cut). No future effort should add subject deletion without revisiting the whole propagation path. If someone ever needs to "really remove" a subject, the answer is a migration that never mutates existing subjects — not deletion.

This directly addresses the round-3 critiques: primary-tag freeze + deprecation does not permanently fail mints; deprecation severs propagation paths consistently with its meaning; missing-ancestor is unambiguously a bug because deletion is forbidden.

## 5. Implementation sketch

### Prerequisites (must land before `propagation_enabled = true`)

1. **Forum-contract primary-tag plumbing.** The post schema today stores `tags: Vec<String>` with implicit first-is-primary ordering enforced nowhere. Change: the forum contract records the primary tag as an explicit `primary_tag: String` on each post (derived once from `tags[0]` at post creation, then frozen). `MintExperience` calls pass `primary_tag`, not `tags[0]`. Frontend and vault daemon are updated to match. Without this, propagation's "primary tag" concept relies on ordering conventions that no contract enforces.
2. **Seed parent-map governance proposal.** Before flipping the flag, a governance proposal populates parents for the existing top subjects (rust, cosmwasm, governance, cooking, gardening, etc.) via `ProposeParent` calls from the curator-audit-gate sibling effort. Otherwise flipping the flag changes nothing visible on the current 6-orphan tree.
3. **Curator-audit gate deployed.** Sibling effort `forum-tag-curator-audit-gate`. Without it, propagation opens the multi-post-farming window flagged in round-1 critique H4.

### Contract changes

**`subject` contract:**
- Add `CycleDetected`, `TreeTooDeep`, `AlreadyParented`, `BootstrapWindowClosed` errors.
- Add the walk-check to `execute_create_subject` (§4.2).
- Add a query `QueryMsg::AncestorChain { tag: String } -> AncestorChainResponse` returning the ordered ancestor list plus each ancestor's `taper_factor_bps` and `deprecated` flag (all in one query to avoid multiple round-trips during a mint). Bounded by `MAX_TAG_DEPTH`.
- Add `BOOTSTRAP_WINDOW_OPEN: Item<bool>`, default `true`.
- Add `ExecuteMsg::AdminSeedParent { tag, parent }` (admin-or-authorized-caller; valid only when bootstrap window is open, target subject is orphan, cycle + depth checks pass).
- Add `ExecuteMsg::CloseBootstrapWindow {}` (admin-or-authorized-caller, irreversible).
- The experience contract's `SetPropagationEnabled(true)` handler also triggers a `CloseBootstrapWindow` sub-message automatically, so the two can never drift.
- Add `InternalMsg::AddTotalExperienceBatch { updates: Vec<(String, u64)> }` — the subject contract applies updates to non-deprecated entries and silently skips deprecated ones (rather than failing the batch, per §4.5). Still fails if any tag is missing (missing ≠ deprecated), which indicates a real bug.

**`experience` contract:**
- Add `PROPAGATION_ENABLED: Item<bool>`, default false.
- Add `PROPAGATION_REGIME: Item<u32>`, default 0. Incremented on every flip.
- Add `AUDIT_GATE_CONTRACT: Item<Option<Addr>>`, default None.
- Setter: `SetAuditGate { addr: String }`, admin-or-authorized-caller.
- Setter: `SetPropagationEnabled { enabled: bool }`, admin-or-authorized-caller. Flipping to `true` requires (per §4.0):
  - `AUDIT_GATE_CONTRACT.is_some()` AND cw2 `ContractInfo` query to that address returns `contract == "crates.io:os-forum-audit-gate"` with compatible version.
  - Subject contract reports ≥ `MIN_SEEDED_PARENTS = 3` parented subjects AND at least one parented subject at depth ≥ 2.
  - For second and subsequent true-flips: `BOOTSTRAP_WINDOW_OPEN == false` must already hold.
  - On success: increments `PROPAGATION_REGIME`, emits `propagation_enabled` event, issues a `CloseBootstrapWindow` sub-message to the subject contract using `SubMsg::new(...)` (default `ReplyOn::Never`). CosmWasm semantics: if the sub-message fails, the parent tx reverts atomically — the flip does not commit without the window being closed. No `reply_on_error` handler, no suppression: the default is the correct semantics here.
- Flipping to `false` has no preconditions (governance can always disable).
- Extend `ExperienceTransaction` with:
  - `regime: u32` — propagation-regime counter at mint time.
  - `ancestor_snapshot: Vec<String>` — the ordered ancestor chain (post tree-cut per §4.5) used for this mint. Bounded at `MAX_TAG_DEPTH = 8`. Gives auditors O(1) reconstruction independent of later tree mutations. Costs up to 8 strings per mint record; acceptable.

- In `mint_experience_internal`:
  1. If `PROPAGATION_ENABLED == false`: existing single-subject path, unchanged (but now also writes `regime: current_regime` to the transaction record). Return.
  2. Query `AncestorChain` from the subject contract (one read, returns leaf-through-root with taper + deprecated flags).
  3. If leaf is deprecated (§4.5): record a zero-amount transaction with `deprecated_leaf` marker and empty ancestor snapshot, skip all writes, return successfully. Mint does not revert.
  4. **Apply tree-cut** (§4.5): walk the returned chain leaf→root; the moment a deprecated ancestor is encountered, truncate the chain at the level immediately below. All levels at or above the first deprecated ancestor are excluded from writes.
  5. **Read-all-then-write-all ordering**: build the full per-level write list in memory using the taper factors from the query response (a single block-consistent snapshot), skipping zero-amount levels. Only after the full list is computed, begin writes. This removes any taper-read race across the batch.
  6. **In-contract synchronous writes**: for each non-skipped entry, update `BALANCES[(user, ancestor_tag)]`, `SUBJECT_USERS[(ancestor_tag, user)]`, record an `ExperienceTransaction` with `regime: current_regime` and the snapshot of the truncated ancestor chain.
  7. **One** `AddTotalExperienceBatch` sub-message to the subject contract with the filtered `(tag, amount)` list. Since the experience contract has already applied the tree-cut, no entry in the batch should be deprecated; the subject contract still double-checks and skips any straggler (defense in depth). If any tag in the batch is genuinely missing (impossible per §4.5 create-only invariant, but defensive), the whole tx reverts atomically — BALANCES writes roll back in the same tx.

### Atomicity reasoning

CosmWasm serializes message execution within a transaction and transactions within a block. Sub-messages execute synchronously from the caller's point of view unless explicit reply semantics are used. The batched approach guarantees atomicity by construction:

- The `AncestorChain` query and all `BALANCES` writes happen in one synchronous path inside `mint_experience_internal`. No external messages between them.
- The single `AddTotalExperienceBatch` sub-message is the only external effect. If it fails, the parent transaction reverts, and all `BALANCES` changes revert with it.
- Between the `AncestorChain` query (step 2) and the sub-message (step 6), no other transaction can execute — CosmWasm serializes tx execution within a block and this entire flow is within one tx.
- Deprecation or tree mutation that could affect the walk can only happen in a *different* tx in the same or later block. Different tx = ordered after this one = cannot affect this tx's snapshot.

### Gas profile

- `propagation_enabled = false` (default): identical to today — one BALANCES write, one `AddTotalExperience` sub-message. Zero added cost.
- `propagation_enabled = true`, orphan leaf (no parent): one `AncestorChain` query returning empty, one BALANCES write, one `AddTotalExperienceBatch` with one entry. +1 query cost (cheap: single `SUBJECTS.load`).
- `propagation_enabled = true`, depth-8 leaf, `N ≥ 8`: one `AncestorChain` query (internally up to 8 `SUBJECTS.load` calls), up to 8 BALANCES writes, one batched sub-message with 8 entries. Each mint therefore costs up to 8 chain storage reads on the subject contract plus the experience-contract writes. At scale (thousands of mints per day), this is the load-bearing cost item; the depth cap of 8 is chosen so it stays bounded. If profiling later shows `AncestorChain` in the hot path, caching ancestry for immutable-parented subjects is a cheap optimisation (since parents are frozen post-adoption).

### Tests

- `propagation_enabled = false` (default): mint behaves exactly as today. Regression guard.
- `propagation_enabled = true`, `N = 1`: only leaf gets XP, no zero-amount writes to ancestors.
- `propagation_enabled = true`, `N = 8`: every level 0..7 gets the expected shifted amount.
- Depth cap boundary (depth 8 ok, depth 9 rejects at `CreateSubject`).
- Cycle detection (`CreateSubject { tag: "a", parent_tag: Some("b") }` with `b → a` pre-existing).
- **Deprecated leaf:** `primary_tag` points to a deprecated subject → mint returns success with zero XP, `deprecated_leaf` event, no reverts.
- **Deprecated mid-chain ancestor:** walk skips it, other ancestors still receive their share, no revert.
- **Missing ancestor (bug):** `AddTotalExperienceBatch` rejects for a genuinely missing tag → whole mint reverts, BALANCES unchanged.
- `SetPropagationEnabled(true)` **precondition enforcement:** rejects when audit gate is unset; rejects when fewer than 3 subjects have non-null parent; succeeds otherwise and auto-closes bootstrap window.
- `SetPropagationEnabled(false)` always permitted regardless of preconditions.
- `PROPAGATION_REGIME` counter increments on each flip and is recorded on every `ExperienceTransaction`.
- `AdminSeedParent` rejects after bootstrap window closes; rejects when target subject already parented; rejects on cycle/depth violation.
- Bootstrap window closes exactly once and stays closed (idempotent `CloseBootstrapWindow`).
- `ProposeParent` is not defined in this contract (sibling effort); sibling effort's tests cover the challenge-window flow.

## 6. Open questions (for critic-chain / sibling efforts)

- **Q1: Voting weight scoped to a parent subject.** If `gui` has no direct XP holders but inherits across all `waybar` holders, does voting on `gui`-level rules tally direct `gui` XP only, or inherited too? (Likely: direct only — once XP propagates, ancestors have their own direct balances. But cross-cuts into governance contract logic, worth confirming with the governance effort.)
- **Q3: Genesis taper per level.** Each level applies its own taper independently (consistent with "each subject is its own economy"). This only reduces issuance below the `< 2N` upper bound, never exceeds it, so the audit invariant holds. Noted here for implementation clarity; not a blocker.
- **Q4: Should secondary tags earn anything at all?** Zero is clean but harsh — maybe a nominal fixed small allocation so tagging adjacent subjects isn't pure cost. Counter: makes abuse math fuzzier. Default to zero; revisit with data.

(Promoted to prerequisites in §5 and removed from this list: original Q2 — primary tag plumbing; original Q5 — seed parent map.)

## 7. Critic-chain review — TBD

Convergence target per project methodology: FATAL + HIGH count = 0. Run this doc through critic-chain (3–5 rounds expected) before implementation sub-effort opens.

## 8. Handoff

On convergence, this doc produces:

- A decision node (tree shape, propagation formula, depth cap).
- An implementation sub-effort with the test list from §5 as acceptance criteria.
- The sibling `forum-tag-curator-audit-gate` stays independent but will reference §4.3 Phase 2 and §6 Q5 as inputs.
