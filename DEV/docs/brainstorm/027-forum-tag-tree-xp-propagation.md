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

### 4.1 Propagation rule — primary tag only, geometric decay

Each post declares **one primary tag** (the first tag). Secondary tags exist for discoverability but earn no XP. When a contribution mints `N` XP on the primary tag `t`:

- Walk up `t.parent_tag` chain.
- Level 0 (leaf `t`): user gets `N` XP, capped at the subject's taper factor (existing genesis mechanic).
- Level 1 (parent): user gets `N/2` XP.
- Level 2 (grandparent): user gets `N/4` XP.
- ... until the root is reached or depth cap hit.

Integer math: `amount_at_level_k = N >> k` (right shift, saturating at 0). With the current `N = 1` bug-report payout, the reporter gets 1 at the leaf, 0 everywhere upstream. That's fine — the first meaningful propagation kicks in when `N ≥ 2`. Larger contributions (audits, curated posts) can mint `N = 4` or `N = 8` and get natural multi-level propagation without extra parameters.

**Why this rule:**

- **Honest declaration.** Forcing a primary tag makes tag choice accountable. The curator-audit gate has one claim to verify instead of a set.
- **No multi-tag farming.** Secondary tags earn no XP, so tagging `finance, waybar, cooking` on a bug is just spam, not a payday.
- **Bounded total issuance.** Geometric series sums to `< 2N` across infinite depth — no matter the tree, the chain mints at most `2N − 1` XP for a payout of `N`. Auditor models the system economics without worrying about tree shape.
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

### 4.3 Orphan-fix — two-phase

Phase 1 (this effort): leave `EnsureSubjectsExist` alone. Auto-created subjects stay at the root. The tree is sparse — only subjects with deliberately-set parents form a hierarchy. No regression on today's behavior.

Phase 2 (sibling effort `forum-tag-curator-audit-gate`): adds `ProposeParent { tag, parent }` as a curator-gated flow. Curators with XP in the claimed parent can set or change a subject's parent. Parenthood becomes a separate, audited governance action, which also gives us a natural insertion point for abuse checks.

This split is the reason the two efforts are siblings: the propagation math can ship today even with a flat tree (no-op for orphans), and the tree fills in as curators wire subjects together.

### 4.4 Mutability — parent is immutable after creation (for now)

Once set, `Subject.parent_tag` cannot change without a governance proposal. Rationale: changing a parent mid-flight retroactively shifts who-earned-XP-from-what-ancestor, which is a nightmare for audit trails. If we need a `ReparentSubject` later, it's a governance-only call that:

- emits an event logging the old and new parent,
- does **not** backfill historical balances (past grants stay with whatever chain existed at the time),
- applies only to future `MintExperience` calls.

Explicit decision to defer: the curator-audit-gate effort will introduce `ProposeParent` for **new** parent assignments (orphans → parented). Reparenting (changing an existing parent) is a separate later question.

## 5. Implementation sketch

Two contract changes:

**`subject` contract:**
- Add `CycleDetected` and `TreeTooDeep` errors.
- Add the walk-check to `execute_create_subject`.
- Add a query `QueryMsg::AncestorChain { tag: String } -> Vec<String>` returning the ordered ancestor list (leaf → root). Used by the experience contract for propagation. Bounded by `MAX_TAG_DEPTH`.
- Add `InternalMsg::AddTotalExperienceWithPropagation { tag, amount }` that walks ancestors internally and updates `total_experience` on each, OR keep the walk on the experience-contract side. (Design choice: do it on the **experience** side — it already owns the user-balance ledger and knows the user address. Subject contract stays a passive aggregator.)

**`experience` contract:**
- In `mint_experience_internal`:
  1. Query `AncestorChain` from the subject contract for the target `subject`.
  2. Loop over ancestors; for each level `k` with `amount_k = N >> k`, skip if 0, else:
     - Update `BALANCES[(user, ancestor_tag)]` (same logic as today, single write).
     - Record an `ExperienceTransaction` per level for full audit trail.
     - Emit an `AddTotalExperience` sub-message per level.
  3. `SUBJECT_USERS[(ancestor_tag, user)] = ()` for each level to support `BalancesBySubject` queries.

**Gas profile.** With `MAX_TAG_DEPTH = 8` and current bug-payout `N = 1`, only the leaf actually gets XP (the shift zeroes out at level 1). Cost is dominated by the ancestor-chain query (one read per level, 8 reads worst-case). For larger payouts (`N = 8`), all 8 levels get balance writes — still bounded.

**Tests:**
- `mint_experience` with primary-only propagation; check all ancestors got their share.
- Depth cap boundary (depth 8 ok, depth 9 rejects).
- Cycle detection (`CreateSubject { tag: "a", parent_tag: Some("b") }` with `b → a` pre-existing).
- Orphan case: `parent_tag = None` leaf mints as today with no propagation.
- `N = 1` case: only leaf gets XP, no zero-amount writes to ancestors.

## 6. Open questions (for critic-chain / sibling efforts)

- **Q1: Who votes weight for governance proposals scoped to a parent subject?** If `gui` has no direct XP holders but inherits 100 XP across all `waybar` holders, does voting on `gui`-level rules tally direct `gui` XP only, or inherited too? (Likely: inherited, to match the propagation intent. But this cross-cuts into governance contract logic.)
- **Q2: Should the primary tag be declared on the post, the contribution, or at XP-grant time?** Currently the post has a `tags` array and no primary marker. Easiest: first tag in the array is primary. Needs frontend + forum-contract plumbing.
- **Q3: What does genesis taper do across the tree?** If `waybar` has exited genesis but `os` (parent) hasn't, does the parent-level XP get tapered? (Proposed: yes — each level applies its own taper independently. Consistent with "each subject is its own economy.")
- **Q4: Should secondary tags earn anything at all?** Zero is clean but harsh — maybe a nominal `N / (2^depth + sec_count)` fixed small allocation so tagging adjacent subjects isn't pure cost. Counter: makes abuse math fuzzier. Default to zero; revisit with data.
- **Q5: How do we bootstrap a parent when all three subjects (`waybar`, `gui`, `os`, `linux`) are orphans today?** The curator-audit-gate effort answers this, but the migration story matters: on deploy, do we ship a seed parent-map for the current 6 subjects, or leave it to organic curation? (Lean: governance proposal on launch seeds the obvious ones; the rest wait for curators.)

## 7. Critic-chain review — TBD

Convergence target per project methodology: FATAL + HIGH count = 0. Run this doc through critic-chain (3–5 rounds expected) before implementation sub-effort opens.

## 8. Handoff

On convergence, this doc produces:

- A decision node (tree shape, propagation formula, depth cap).
- An implementation sub-effort with the test list from §5 as acceptance criteria.
- The sibling `forum-tag-curator-audit-gate` stays independent but will reference §4.3 Phase 2 and §6 Q5 as inputs.
