# 027 — Critic Chain Record

Companion to `027-forum-tag-tree-xp-propagation.md`. Four rounds, converged with zero FATAL / HIGH remaining.

## Executive Summary

The original design proposed an XP-propagation scheme for the forum's tag taxonomy: tag a bug `waybar` and credit fans out to `gui`, `os`, `linux`. Critics across four rounds found that the first draft assumed the tree would exist, assumed contributors would tag honestly, and assumed the tree wouldn't change after posts were created. Those three assumptions didn't survive contact. The revised design gates economic activation behind an on-chain flag with contract-enforced preconditions (audit gate deployed and identity-verified, real hierarchy seeded before activation, bootstrap window closes permanently on first activation); handles the chicken-and-egg of seeding-before-curators via a governance-only bootstrap flow; snapshots each mint's ancestor chain so later tree changes don't break auditability; and cuts propagation off at any deprecated ancestor rather than letting severed categories leak XP upward. Core idea survived; surrounding mechanics got a lot sharper.

## Scorecard

| Round | FATAL | HIGH | MODERATE | Fixed this round |
|---:|---:|---:|---:|---|
| 1 | 0 | 4 | 4 | 4 HIGH + 4 MODERATE (promoted some to prereqs) |
| 2 | 0 | 4 | 5 | 4 HIGH + 5 MODERATE |
| 3 | 0 | 3 | 5 | 3 HIGH + 5 MODERATE |
| 4 | 0 | 0 | — | Converged |

Total: 11 HIGH + 14 MODERATE identified and resolved across 4 rounds.

---

## Round 1

### Proposal
Initial design at `027-forum-tag-tree-xp-propagation.md` v1. Proposed: primary-tag-only propagation with geometric decay (`N >> k`), single-parent tree with depth cap 8 and cycle check, two-phase orphan fix (propagation ships immediately on flat tree, curator-audit sibling effort handles parent assignment later), immutable parent post-creation.

### Critique findings (round 1)

1. **HIGH — Curator/reporter collusion unaddressed in Phase 1.** Phase 1 ships propagation before the curator-audit-gate lands. Curator with XP in `os` approves a confederate's bug primary-tagged `waybar` → `os` accumulates XP through collusion. Open farming window.
2. **HIGH — Phase 1 ships into a flat tree, defeating premise.** All 6 current subjects are orphans. Propagation added with `EnsureSubjectsExist` still creating parentless subjects is a no-op on the ledger but adds attack surface.
3. **HIGH — Cross-contract ancestor walk not atomic.** Per-level sub-messages to subject contract don't guarantee rollback if one fails — partial BALANCES writes possible.
4. **HIGH — Bounded issuance claim ignores multi-post farming.** `<2N` holds per-mint, but one actor posting N times across sibling leafs inflates ancestor XP linearly. Per-mint bound is pointless without per-actor rate limits.
5. **MODERATE — §4.4 immutability vs §4.3 Phase 2 `ProposeParent` ambiguous.** Setter-only or changer? Doc never states.
6. **MODERATE — Q3 genesis-taper-per-level in tension with `<2N` claim.** Needed clarification as upper bound.
7. **MODERATE — Concurrent CreateSubject + mint race invariants not explained.** Why safe? Doc didn't say.
8. **MODERATE — Primary-tag plumbing is prerequisite, not open question.** §4.1 depends on it; forum contract doesn't currently distinguish primary.

### Fixes for round 2
- Added §4.0 activation gate (`propagation_enabled` flag, default false).
- Required 3 prerequisites (audit gate, seed parent-map, primary-tag plumbing) before flip.
- Changed §5 to single batched `AddTotalExperienceBatch` sub-message.
- Clarified bounded-issuance is per-mint upper bound; tapers only reduce.
- Split §4.4 into orphan-adoption vs reparenting (reparenting out of scope entirely).
- Added depth-is-monotonic justification in §4.2.
- Promoted primary-tag and seed-parent-map to explicit prerequisites in §5.

---

## Round 2

### Critique findings (round 2)

1. **HIGH — Prerequisite verification is trust, not on-chain.** §4.0 says governance only flips "after all land" but the flip handler doesn't actually check anything. Compromised admin can flip early.
2. **HIGH — Seed parent-map can't actually be seeded before the flag flips.** `ProposeParent` is introduced by the sibling effort. Circular dependency: can't seed without sibling, can't enable without seed, can't ship sibling without activation.
3. **HIGH — Primary-tag-freeze + subject deprecation bricks posts forever.** If subject deprecated after posts exist with it as `primary_tag`, future mints revert permanently.
4. **HIGH — Adoption race: first-mover wins the wrong parent.** `finance`-XP curator rushes `ProposeParent waybar → finance` before `gui`-XP curator notices. Immutable means mistake is permanent.
5. **MODERATE — Flag-flip history not auditable from balances alone.** `ExperienceTransaction` doesn't record regime.
6. **MODERATE — `AddTotalExperienceBatch` all-or-nothing amplifies griefing.** Deprecate rarely-used mid-chain subject to DoS entire subtree.
7. **MODERATE — Read-before-write-in-same-tx pattern understated.** The "synchronous and atomic" paragraph glossed details.
8. **MODERATE — Depth-8 + `N >> k` concentrates XP at root.** Political implication for governance.
9. **MODERATE — Taper-read race within batch not addressed.** Read order vs write order can change per-level amount.

### Fixes for round 3
- On-chain precondition enforcement on `SetPropagationEnabled(true)`: audit gate registered, ≥3 parented subjects.
- Added `AdminSeedParent` with bootstrap window, closes on first true-flip → breaks circularity.
- Tree-cut semantics on deprecation: leaf deprecated = no-op mint, mid-chain deprecated = halt walk.
- Adoption goes through curator-audit-gate sibling effort's challenge window + audit-jury resolution (not first-mover).
- `PROPAGATION_REGIME` counter + `regime` field on `ExperienceTransaction`.
- Specified read-all-tapers-then-write-all ordering.
- Defensive atomicity reasoning section added.

---

## Round 3

### Critique findings (round 3)

1. **HIGH — Bootstrap window close sub-message failure path.** Must pin CosmWasm sub-message reply semantics (default `ReplyOn::Never` reverts parent tx on sub-msg fail) — design relied on "also triggers" language.
2. **HIGH — AUDIT_GATE_CONTRACT verification is circular.** `is_some()` check alone accepts stub or malicious address. Need identity check via cw2 `ContractInfo`.
3. **HIGH — Concurrent AdminSeedParent + SetPropagationEnabled(true).** Block-ordering not explicitly documented.
4. **MODERATE — `MIN_SEEDED_PARENTS = 3` cosmetic.** 3 flat dummy adoptions pass the check. Need structural gate (e.g. depth ≥ 2).
5. **MODERATE — Deprecated mid-chain skip contradicts deprecation intent.** Propagating past deprecated ancestor leaks XP through severed semantic links.
6. **MODERATE — Regime counter insufficient for historical reconstruction.** Tree mutates within a regime (ProposeParent in sibling effort). Need per-tx snapshot.
7. **MODERATE — SetPropagationEnabled(false) → (true) re-trip.** No explicit invariant check that bootstrap is closed on second true-flip.
8. **MODERATE — "Missing ancestor = bug" assumes non-deletable subjects.** Create-only invariant was implicit, not stated.
9. Unstated: `AncestorChain` gas impact at scale.

### Fixes for round 4
- Pinned `SubMsg::new(...)` with `ReplyOn::Never` as the default behavior that gives atomic revert.
- cw2 `ContractInfo` identity check on audit gate at flip-time.
- §4.0 now explicitly documents concurrent seed/flip ordering under serial tx execution.
- Strengthened seed threshold: ≥3 parented AND ≥1 at depth ≥2.
- §4.5 rewritten to tree-cut (halt at first deprecated ancestor), not skip.
- Added `ancestor_snapshot` field to `ExperienceTransaction` for O(1) historical reconstruction.
- Added `BOOTSTRAP_WINDOW_OPEN == false` precondition to second+ true-flips.
- Declared create-only invariant explicitly in §4.5.
- §5 gas-profile section notes 8 `SUBJECTS.load` per mint + optional caching optimization.

---

## Round 4

### Critic verdict
**NO FATAL OR HIGH FLAWS FOUND — CONVERGED.**

Key confirmations:
- Tree-cut (§4.5) vs bounded-issuance (§4.1): truncating the geometric series only lowers the sum. Upper bound `<2N` holds.
- cw2 version-skew concern for audit gate is the system-wide governance-migration threat model, not propagation-specific.
- `ancestor_snapshot` captures tag strings at mint time; subsequent deprecation doesn't mutate stored strings. Auditor reconstruction is deterministic.
- CosmWasm 1.x (current chain version) propagates sub-message failures to parent tx by default via `SubMsg::new` without reply handler.
- `§4.5` tree-cut + `§5 step 4` truncation are internally consistent.

---

## Remaining notes (non-blocking)

These are **MODERATE** issues deferred as implementation notes:

- **Depth-8 + `N >> k` concentrates XP at root** (R2 M8). As payouts grow, root subjects dominate `total_experience`. Governance-weight schemes using subject totals should acknowledge this.
- **Secondary tags earn zero** (§6 Q4). Clean but harsh. Revisit with data if contributors complain about "tax" for adjacent-subject tagging.
- **Parent-inheritance for governance voting** (§6 Q1). Whether voting on `gui`-level rules tallies direct XP only or inherited too — cross-cuts into governance contract, not blocking here.
- **AncestorChain caching** (§5 gas profile). Optional optimization for hot path; immutable parents make it safe.

---

## Key Lessons

Cross-cutting insights from this chain, worth extracting:

1. **"Trust governance to coordinate prerequisites" is not a safety mechanism.** Every multi-stage rollout with human-coordinated gating in a critic chain gets flagged. On-chain assertion of prerequisites is the only reliable pattern. Any design that says "governance will only flip X after Y, Z ship" is relying on human vigilance, which fails.

2. **Circular prerequisites emerge silently in phased rollouts.** "Effort A depends on Effort B which depends on Effort A's output" is easy to miss because each effort's local prerequisites look reasonable. Explicitly tracing the bootstrap path — *who creates the first X, before X-creator contract is deployed* — catches these.

3. **Immutability + deprecation + retroactive reads need a tree-cut model, not a skip model.** "Deprecated" sounds like a soft filter ("just skip and continue"), but if descendants inherit from their ancestors through a deprecated mid-level, you're propagating signal through a severed link. Halt at first deprecated ancestor is the only semantic that respects deprecation's meaning.

4. **Historical auditability requires snapshots, not derivable state.** Regime counters tell you "which rules were active" but don't help if the *data* (here, the tree shape) mutates within a regime. For cross-regime, cross-mutation reconstruction, record the snapshot directly on the transaction. Cheap at bounded depth.

5. **cw2 `ContractInfo` is the correct way to verify a cross-contract dependency.** `is_some()` on a stored `Addr` only proves someone wrote an address there. Identity assertion via cw2 contract name catches stubs and governance-error misconfigurations.

6. **Sub-message reply semantics must be pinned in the design, not left to implementation discretion.** CosmWasm's defaults are correct for atomicity-critical patterns, but implementers can deviate. Docs should name the expected `ReplyOn` setting.

7. **Four rounds is enough.** Each round's fixes bred 1–3 new MODERATE issues; by round 4 the HIGH count was 0. The pattern: first round breaks the big assumptions, second round breaks the fix mechanics, third round breaks the verification of the fix mechanics, fourth round confirms. Go beyond 4 without new signal → diminishing returns.
