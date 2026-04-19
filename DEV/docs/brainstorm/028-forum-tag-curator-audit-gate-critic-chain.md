# 028 — Critic Chain Record

Companion to `028-forum-tag-curator-audit-gate.md`. Five rounds, converged with zero FATAL / HIGH remaining.

## Executive Summary

The original design proposed two abuse-defense mechanisms for the forum tag system: a stake-based report mechanism when someone picks the wrong primary tag on a post to farm XP in an unrelated category, and an adoption flow with a challenge window for setting a tag's parent in the taxonomy tree. Critics across five rounds showed the first draft's defenses were themselves exploitable — trivially-farmed standing, juries that could be rented, stakes that could be weaponized against honest participants, state that could be griefed into bloat, and several race conditions around timing-sensitive verdicts. The revised design swapped simple thresholds for a layered system: standing proportional to actual skin in the game, juries that exclude parties with monetized stakes in the verdict, stake-return on liveness failures so jury unavailability doesn't punish the flagger, serial case handling instead of subsumption (to prevent fake cancellations), burn-debt queues so post-hoc corrections don't silently reward authors who spent their unearned XP, per-post cooldowns to prevent infinite holds, and abandonment penalties to clear stale proposals. Core idea survived; defense depth increased substantially.

## Scorecard

| Round | FATAL | HIGH | MODERATE | Fixed this round |
|---:|---:|---:|---:|---|
| 1 | 0 | 4 | 6 | 4 HIGH + 6 MODERATE |
| 2 | 0 | 5 | 4 | 5 HIGH + 4 MODERATE |
| 3 | 0 | 6 | 1 | 6 HIGH + 1 MODERATE |
| 4 | 0 | 5 | 0 | 5 HIGH |
| 5 | 0 | 0 | 0 | Converged |

Total: 20 HIGH + 11 MODERATE identified and resolved across 5 rounds.

---

## Round 1

### Critique findings
1. **HIGH — Standing gate trivially farmable** — 1 XP in proposed subject is cheap; raised to ≥3 XP (matches RegisterAuditor).
2. **HIGH — Empty proposed subject breaks jury selection** — added `MIN_JURY_POOL = 3` unique holders precondition.
3. **HIGH — `Correct` verdict race with AutoPromote** — pre/post-promotion both handled; atomic compensating burn+mint via audit contract.
4. **HIGH — Feature-flag query brittle** — versioned `CapabilitiesResponse { version, ... }` with `MIN_AUDIT_CAPABILITIES_VERSION` gate.
5-10. Moderate-severity cleanup (one-shot challenge cooldown, deadlock semantics, double-reporting serialization, bootstrap cost, target-subject jury inclusion, bootstrap-window detection) — all addressed.

---

## Round 2

### Critique findings
1. **HIGH — Burn walk mismatches mint walk under tree mutations** — use ancestor_snapshot from each post's original tx.
2. **HIGH — Compensating burn revert breaks Correct liveness** — saturating burn + unrecovered residue (escalated next round).
3. **HIGH — Tag-level cooldown punishes uninvolved third parties** — keyed on (tag, sorted_pair) triple only; third parties unaffected.
4. **HIGH — Target-subject jury enables rent extraction** — reverted to hard exclusion of target-subject holders from both misattribution and adoption juries.
5. **HIGH — Standing = 3 XP dead-on-arrival at bootstrap** — lowered to 1, governance-tunable, tension documented in §5.1.
6-9. Moderate cleanup (upgrade ordering, CASE_BY_POST spam escalation, state retention, jury-pool TOCTOU) — addressed.

---

## Round 3

### Critique findings
1. **HIGH — Snapshot stores tags not amounts** — burn uses per-tx `amount` field directly, no reconstruction needed.
2. **HIGH — Saturating burn residue iteratively farmable** — added `BURN_DEBT: Map<(Addr, subject), u64>` queue consumed by future mints.
3. **HIGH — Spam subsumption is an attack primitive** — removed the carve-out, strict one-case-per-post.
4. **HIGH — CASE_BY_POST vs FlagPost coordination unspecified** — FlagPost is orthogonal (review-extension), audit is promotion-block, no overlap.
5. **HIGH — Standing migration breaks in-flight proposals** — `PendingAdoption` snapshots governance params at propose-time.
6. **HIGH — Submission-time pool check weaponizes flagger stake** — reveal-timeout defaults to `no_consensus` (all stakes returned), not flagger-burn.
7. **MODERATE — AutoPromote timing race** — forum's `HoldPost` must accept Promoted state (explicitly added as deliverable).

---

## Round 4

### Critique findings
1. **HIGH — BURN_DEBT never GC'd for inactive authors** — acknowledged as bounded-by-activity, auto-delete on zero; abandoned debts are bounded by real user behavior, not attacker will.
2. **HIGH — Infinite-hold loop via serial misattribution refiling** — added `MISATTRIBUTION_COOLDOWN: Map<u64, u64>` — 24h per-post cooldown after any case close except Reject.
3. **HIGH — PendingAdoption stale snapshot + permanent storage** — 60-day `ADOPTION_MAX_AGE`, Finalize burns proposer stake as Abandoned.
4. **HIGH — Target-subject jury exclusion inconsistent** — reconciled: misattribution jury is strictly `current_primary ∪ proposed_primary`, no secondary tags.
5. **HIGH — Mint-debt interaction with propagation unspecified** — added worked example showing per-level debt consumption; subject contract receives NET credits in `AddTotalExperienceBatch`.

---

## Round 5

### Critic verdict
**NO FATAL OR HIGH FLAWS FOUND — CONVERGED.**

The round-4 fixes held under stress. Confirmations:

- 24h misattribution cooldown blocks infinite-hold while accepting 50% uptime under worst-case grief — better than the alternative.
- 60-day abandonment penalty scales state bloat with tag-count, not attacker-will (only one pending per orphan tag).
- Zero-amount tx records are intentional audit-trail preservation; subject-level total_experience uses net credits.
- Bootstrap chicken-and-egg (MIN_JURY_POOL = 3 blocks tiny trees; adoption juries use non-target subjects) is openly accepted.
- Sub-message ordering follows 027's pinned `SubMsg::new` default semantics.

Shippable.

---

## Remaining notes (non-blocking)

- Post-Correct nicety: flagger earns XP in newly-correct subject (§6 Q1). Default zero; revisit with data.
- Bootstrap-XP tension (§5.1): `ADOPTION_STANDING_MIN_XP = 1` is the pragmatic launch value; governance should raise as XP supply matures.
- Lazy cleanup of `ADOPTION_COOLDOWNS`, `PENDING_ADOPTIONS`, `CASE_BY_POST`, `BURN_DEBT` zero-entries — all pruned on next read-hit or on the action that zeroes them. No separate cron crank needed.

---

## Key Lessons

Cross-cutting insights worth extracting:

1. **Defensive mechanisms are themselves attack surfaces.** The design added a stake to prevent grief; the stake became a weapon against honest flaggers when jury timed out. Every defense introduced must be stress-tested against "what if the attacker WANTS this defense to fire?" The stake-return-on-timeout fix is a common pattern: liveness failures should not punish the honest party.

2. **Binary state machines preempt subsumption shortcuts.** The draft tried to be "helpful" by letting spam Reports cancel misattribution cases. That helpfulness was the attack. Strict one-case-per-post is boring but safe; helpful shortcuts across state machines are where bugs hide.

3. **Governance-tunable parameters need snapshots.** Any parameter that affects an in-flight case (standing thresholds, stake costs, cooldown durations) should be snapshotted at case-open time. Raising a parameter mid-case to disqualify opponents is a legitimate governance concern and the mechanism should guard against it at the protocol level.

4. **Burn-debt queues elegantly resolve "saturating burn vs hard revert" dilemma.** When compensating transactions can't fully recover because assets have moved, neither silent-ignore (unfair) nor hard-revert (liveness-kill) is right. A debt queue paid by future earnings in the same resource pool is usually the principled answer.

5. **State bloat is manageable when writes are stake-gated.** Proposer stake on PendingAdoption + Abandoned-burns-the-stake means attacker bloat costs real XP. Standing gates + staked operations transform state-bloat concerns into economic concerns, which the existing tokenomics already handle.

6. **Per-tx records are simpler than reconstruction-from-snapshot.** The first instinct was to snapshot the ancestor chain and reconstruct amounts from it. The simpler approach: emit one tx per level at mint time with its own amount field. Compensating burns query tx history by source_id. No math, no reconstruction, no ambiguity — just replay the ledger.

7. **Strict exclusion beats soft exclusion when side-channels exist.** Including target-subject holders in juries is appealing ("they know the subject"), but commit-reveal hides votes and off-chain side payments are unobservable. Strict exclusion gives up some expertise to close a rent-extraction vulnerability. Hard rules beat soft rules when monitoring is impossible.

8. **Five rounds converged.** One more round than 027's four — the audit-gate's defense-in-depth surface is meaningfully larger than the propagation math's, and each round's fixes unlocked new attack surfaces. Each subsequent round's HIGH count stayed roughly constant (4, 5, 6, 5, 0), suggesting iteration was mining a reasonably deep vein until convergence. Stop criterion held: no new signal at round 5 = done.
