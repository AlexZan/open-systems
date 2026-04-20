# Decision 013: Launch Admin — Trezor + Throttled Powers + Community Override

**Date:** 2026-04-14
**Status:** Proposed
**Refines:** decision-187 (admin is the safety net during incubation) — keeps the spirit, refines the mechanism. Does NOT contradict decision-006 (no human has special power) — admin powers are bounded by throttles AND by community vote AND by gradual community-driven dissolution.
**Replaces draft:** Earlier draft titled "launch without admin" was wrong. We are NOT disabling admin at launch. We are launching admin with bounded power.

## Context

Decision-187 said admin is the safety net during incubation. We built the admin features in code: pause, rotate, tombstone (398 tests passing). The remaining question was: how is the admin key stored and bounded so that a single founder running the project doesn't become a single point of failure?

We explored a multisig-based design across 3 critic chain rounds in `DEV/docs/brainstorm/026-multisig-safety-net-launch-plan.md` and accumulated 9 FATAL + 19 HIGH + 13 MODERATE issues without converging. Captured in fact-2952: admin-as-safety-net is structurally hard for a single-founder incubation when you also try to add multisig + dissolution + recovery + bounded power as four simultaneous constraints.

The pivot wasn't "remove admin." The pivot was **simpler key topology + smaller per-action damage caps + community can always vote you back in**. Three layers of defense, each handling a different threat profile.

## Decision

**Launch with a single-founder admin key, hardware-stored on 3× Trezor Safe 3 devices loaded with the same seed, with per-action throttles and a community-vote override path.**

Specifically:

### Layer 1 — Key storage (Trezor × 3)

- **Hardware:** 3× Trezor Safe 3. Open-source firmware (auditable, no Recover-equivalent that ties trust to vendor honesty). Certified secure element. On-device display so the device shows the actual transaction being signed — defeats the "compromised laptop lies about which tx is being signed" attack.
- **Setup:** Generate the seed on Trezor #1 (24 words shown on the device screen, never on a computer). In a single private session with no cameras, write the 24 words on paper temporarily. Initialize Trezors #2 and #3 via "restore from recovery phrase" using the same 24 words. Verify by signing a test message on each device and confirming all 3 produce the same Cosmos address. Physically destroy the paper (shred + burn). Done.
- **Storage:** 3 devices in 3 physically separate locations. Suggested: founder's pocket / home safe / second location (office, family member, safe deposit box).
- **PIN protection per device.** Wrong PIN attempts trigger lockout per Trezor defaults.
- **Backup model:** lose 1 device → use one of the others, continue normally. Lose all 3 simultaneously → the key is gone forever, the system enters "no admin" state, recovery falls to the community vote layer (Layer 3).
- **No paper backup after setup.** Honors the "no written down" preference. The trade-off (a future Trezor firmware vuln could brick all 3 simultaneously) is accepted because the recovery layer covers it.

### Layer 2 — Per-action throttles (containment)

Bound the per-day damage from any compromise of the admin key. Each destructive admin action gets a rate limit and/or cap.

| Admin action | Throttle |
|---|---|
| Mint XP (`AdminGrantExperience`) | Max N XP per day per recipient, max M XP per day total. Tunable at launch. |
| Tombstone post | Max N tombstones per hour. Reversible by community vote (governance migrate can untombstone). |
| Pause contract | Auto-expires after T hours unless explicitly renewed. Reversible by Unpause. Stays fast — pause is the panic button, no time-lock. |
| Rotate admin | Stays fast at this stage; defended by the Trezor hardware + the recovery layer. Time-locks were considered and rejected (cancel-loop problem — see brainstorm-026 critic chain). |
| Disable admin | Stays as one-way kill switch. Worst case: attacker neutralizes admin, system continues without admin. |

The math: if the community can pass a "remove admin" governance proposal in T minutes, admin should not be able to inflict more than T-minutes-worth of damage per day. Throttles enforce the cap.

Implementation: ~1-2 days of contract code per throttle (storage for "actions in current window," check on each handler, refuse if cap exceeded).

### Layer 3 — Community vote override (recovery)

The community vote is **always** the higher authority. Even if the attacker fully owns the admin key, the founder can recover by:

1. **Submitting a governance proposal** from the founder's XP-holding wallet (a SEPARATE key from the admin key — different threat surface). The proposal is a `MigrateContract` action that rewrites the contract state to install a new admin or disable admin entirely.
2. **Founder votes yes** with their XP (founder holds essentially all XP at launch).
3. **Proposal passes and finalizes** within the configured voting period (~60 seconds at launch).
4. **Migrate executes** and admin is rotated/removed.

Total recovery time: under 5 minutes from realization of compromise. Slower than instant rotation, but it's the ultimate fallback if the hardware key is somehow defeated.

### Layer 4 — Tripwire monitoring (detection)

A 24/7 watch service with READ-ONLY chain access. Pages the founder via SMS + email + push when any admin action executes on chain. The founder knows whether they performed it. If the page comes in and they didn't act, that's the alarm — they immediately invoke Layer 3 (governance proposal recovery).

Tripwire is what makes "silent compromise" detectable. Without it, an attacker with the key could act quietly and the founder wouldn't notice. With it, every admin action makes the phone ring.

### Gradual dissolution by community vote

Decision-187's "incubation safety net" is designed to dissolve. Dissolution is **community-driven and gradual** — not a hard 24-month cap. Each admin power gets dissolved by a separate governance vote when the community is mature enough to handle that responsibility:

| # | Power | Why dissolved early/late |
|---|---|---|
| 1 | Mint XP | Dissolved first. Most game-able. Once organic XP flow (audit approval, post promotion) works, admin minting is just a backdoor. |
| 2 | Tombstone post | Dissolved second. Once audit pools and community flagging are active, admin moderation is redundant. |
| 3 | Rotate admin | Dissolved third. Once admin is mostly defanged, key rotation is moot. |
| 4 | Pause contract | Dissolved LAST. Pause is *protective* — it stops damage, doesn't cause it. Keep it longest as the safety net for unforeseen contract bugs. |
| 5 | Full dissolution | DisableAdmin called. System is purely community-governed. Decision-006 fully realized. |

Each dissolution is a community-validated trust transfer. The founder doesn't decide when sovereignty happens — the community votes when they're ready.

Implementation: per-power dissolution flags in each contract's state. A governance proposal type "DissolveAdminPower" that sets the flag. Each admin handler checks its flag and refuses if dissolved. Half a day of contract code.

## Conditional commitment (decision-236)

If the in-contract admin still exists past ~1 year from launch — meaning gradual dissolution has stalled and most destructive admin powers are still active — we will upgrade to a **hot/cold key split** where the everyday signing key is separate from a cold rotation-only key kept in physically separate safes. Single-key topology is acceptable ONLY because admin is expected to be community-dissolved within months. If that expectation is wrong, the topology must upgrade.

See decision-236 for the trigger language.

## Trade-offs explicitly accepted

- **Single hardware-key compromise (e.g., evil maid attack with PIN extraction) is a real risk** mitigated by per-action throttles + community override + tripwire + on-device transaction display. Not zero risk, but bounded.
- **All 3 Trezors lost in one incident → key gone forever.** Accepted because recovery layer (community vote) restores admin via governance proposal.
- **Pause is fast (no time-lock).** Time-locks were considered and rejected because the cancel-loop problem (attacker with the same key can cancel the founder's recovery rotation indefinitely) makes them ineffective against compromise.
- **Trust model includes "Trezor's open-source firmware doesn't have a hidden bug."** Lower trust requirement than Ledger (which requires trusting the company), but not zero.
- **The admin lifetime is short.** This entire design is justified by the expectation that destructive powers are dissolved within months. If dissolution stalls past ~1 year, decision-236 fires and the topology upgrades.

## What this means for launch

Launch blockers (replacing the abandoned multisig launch plan):

1. **Bundled deployment of MVP code** — pause/rotate/tombstone code goes to live chain via the existing chain reset path. All 10 contracts instantiate with admin = founder's Trezor wallet address.
2. **Trezor setup** — buy 3 devices, run the setup session (one private evening, ~1 hour).
3. **Per-action throttle code** — add throttle storage + checks to mint, tombstone, pause handlers. Rotate stays unthrottled. ~2 days.
4. **Per-power dissolution flags** — add `DISSOLVED_POWERS` map + governance proposal type to dissolve a specific power. ~half day.
5. **Tripwire monitoring service** — 24/7 watcher, READ-ONLY chain access, SMS + email + push paging on admin actions. Separate sub-effort.
6. **Auto-expiring pause** — pause has a max duration; needs explicit renewal. ~half day.
7. **Recovery runbook** — `docs/runbooks/admin-recovery.md` documents how to invoke Layer 3 if the hardware key is compromised. Reviewed by founder + one trusted advisor.
8. **Pre-launch advisor sign-off** — designated trusted advisor reviews and signs off on the launch posture.

What's NOT done at launch (deferred or out of scope):
- Multisig setup
- Legal escrow with lawyers
- Chain binary changes (wasm/upgrade authority redirects)
- AdminUnregisterCaller code
- DISSOLUTION_BLOCK on-chain time-cap (replaced by community-driven gradual dissolution)
- ExtendDissolution mechanism
- The entire abandoned multisig launch plan (preserved at brainstorm-026 for future reference)

## Related

- decision-187 (admin is incubation safety net) — refined, not contradicted
- decision-006 (no human has special power) — honored via gradual dissolution + bounded throttles
- decision-236 (conditional commitment to upgrade key topology if admin lasts past ~1 year)
- fact-2952 (admin-as-safety-net is structurally hard with a multisig overlay)
- fact-2953 (Cosmos SDK chain has multiple authority paths beyond contract admin)
- effort `multisig-safety-net-critic-chain` (PAUSED; preserved as starting point if future admin re-enablement happens)
- effort `launch-without-admin-deployment` (renamed to launch-admin-trezor-deployment to reflect this decision)
- DEV/docs/brainstorm/026-multisig-safety-net-launch-plan.md (3-round critic chain artifacts)
