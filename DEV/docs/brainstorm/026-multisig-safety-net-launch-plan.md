# Multisig + Safety Net Launch Plan

**Problem:** The admin safety nets we built (pause, rotation, tombstone, governance authorized-caller bypass) assume the founder controls a single admin key. But a single founder key means one stolen laptop = full system takeover — pause, rotation, tombstone, and DisableAdmin all become attacker tools. Decision-187 says admin is the safety net during incubation. If the safety net itself can be stolen via a single key compromise, the entire incubation strategy is theater. Multisig at the wallet layer is the standard fix, but combining multisig with our existing safety nets creates non-obvious interaction holes (pause speed, governance bypass, lost-key recovery, threshold drift) that are NOT in the multisig literature because they're specific to our system. We need a hardened design before launch.

**Status:** IN PROGRESS

**Why it matters:** This is the LAUNCH BLOCKER. None of the MVP admin work (pause, rotation, tombstone — all done in code, all 398 tests passing) ships to the live chain until this design converges. Multisig is a wallet-level decision applied at deployment time (no contract code changes), so the work here is purely design + critic chain.

---

## Final Solution

[TBD — to be filled in after critic chain converges]

---

## Iteration Chain

### Round 1

**Proposal:** [original draft — see git history, summarized as 2-of-3 multisig with Key A/laptop + Key B/Ledger + Key C/paper-in-safe; routine ops use A+B; governance partially walled off from RotateAdmin only]

**Critique findings (3 FATAL, 7 HIGH, 4 MODERATE):**

1. **FATAL — Governance bypass for RotateAdmin is theatre.** Walling off RotateAdmin from governance is meaningless because (a) governance is still authorized for `register_caller` (admin-only check), (b) governance is the CosmWasm admin on all 10 contracts (per project memory) so it can migrate contract code and rewrite admin entirely. The mitigation only addresses one of three bypass paths.
2. **FATAL — Recovery path circular dependency through pausable governance.** 2-key loss recovery routes through `ScheduleUpgrade` governance proposal, but governance is a contract subject to the same pause guard. Attacker with 2 keys pauses governance, founder's surviving Key C cannot route recovery. "2 keys lost" collapses into "3 keys lost" under active attack.
3. **FATAL — 2-of-3 with routine ops on Key A + Key B = effective 1-of-1.** Laptop + hardware wallet are physically within 1 meter during routine signing (Ledger plugged into laptop USB). Single break-in / mugging / remote compromise captures both keys simultaneously. The cold key in the safe is never used in routine ops, so the effective day-to-day threshold is whoever controls the founder's immediate vicinity.
4. **HIGH — "Remove governance from RotateAdmin" mitigation isn't cleanly implementable.** The current `check_admin_or_authorized` helper has no message-level granularity. It's a single set membership check used uniformly across pause/unpause/rotate/tombstone in all 10 contracts. The mitigation requires either splitting the helper or auditing every contract — code change, not a deployment-time config trick.
5. **HIGH — Tombstone-via-governance is destructive, not reversible.** The proposal allowed governance to tombstone on the premise that "tombstones are append-only and don't grant control." False: tombstoning is destructive in the sense that matters — a malicious governance proposal can mass-tombstone every legitimate post, the vault deletes the blob, and rotation does NOT restore content. At launch the founder holds essentially all XP, so "governance tombstone" = "founder-key-on-governance tombstone" with no multisig protection.
6. **HIGH — Pause race during signing flow if Key A is compromised.** Attacker on laptop (Key A keylogger) can substitute message bytes between Ledger sign and broadcast. Founder approves a pause on the Ledger screen; laptop swaps the body for RegisterCaller/Migrate before broadcast. Many Cosmos Ledger apps display only condensed summaries, making the substitution invisible.
7. **HIGH — 3am latency is fictional.** "Under 5 minutes from incident detection to signature" assumes the founder is awake, oriented, laptop is unlocked, and Ledger is plugged in. Realistic 3am latency: 10-20 minutes for boot/decrypt/login/PIN/navigate. Meanwhile the attacker is automated. No deadman tripwire, no pre-signed pause, no tripwire service.
8. **HIGH — Founder death/incapacitation has no recovery path.** "All 3 keys lost = community fork" dismisses the more probable failure (founder dies, hospitalized, uncooperative). Keys may still exist physically but no one knows where to find them or how to use them. No executor, no dead-man's switch, no successor plan documented. For a 2-year incubation, founder incapacitation is non-trivial probability.
9. **HIGH — No defined dissolution ramp.** Proposal says "admin during incubation" but never defines what triggers dissolution. Decision-006 says no human has special power. Historical crypto projects: "safety net admin" never dissolves, founder always finds a new reason to keep it. Without a hard trigger, this proposal contradicts decision-006 by design.
10. **HIGH — Key C retrieval has no duress defense.** Wrench attack: adversary mugs founder for Key B, compels them to retrieve Key C from the safe. Proposal has no duress PIN, no decoy wallet, no time-lock, no third-party escrow.
11. **MODERATE — 2-of-3 has no headroom.** Lose 1 to compromise + 1 to device failure (Ledger bricked, dead battery) and you're at 1-of-3, which is the "can't act" state. 3-of-5 would give real headroom.
12. **MODERATE — No monitoring/tripwire requirement.** Detection clock doesn't start until founder happens to notice. Pause-as-safety-net without monitoring is a seatbelt without a collision sensor.
13. **MODERATE — XP-vs-multisig key conflation in recovery path.** The "surviving key wallet votes governance" assumption requires the founder's XP to be tied to one of the multisig keys — but if the founder's XP is on a separate "voting" key, the multisig has no governance power. Proposal doesn't clarify.
14. **MODERATE — Paper backup operational risk under-specified.** Standard failure modes (handwriting fade, water/fire damage, unverified write, ink legibility after years) not addressed. Canonical fix (SLIP-39 split, metal seed plate, verified from cold boot) not required.

**Fixes applied for Round 2:**

The most important architectural change: **Round 1 tried to mitigate the governance bypass by walling off RotateAdmin specifically. Round 2 instead removes governance as an admin authority entirely.** Multisig becomes the SOLE admin path. Governance is for community decisions, not for safety-net actions.

Specifically:
- Governance is no longer in `AUTHORIZED_CALLERS` for any of the 10 contracts (closes FATAL 1: no governance bypass for any admin path).
- CosmWasm admin (chain-level migrate/upgrade authority) is transferred from the governance contract to the multisig wallet directly (closes FATAL 1's contract-migration vector).
- The shared `check_admin_or_authorized` helper is replaced by `check_admin` for all admin-gated paths (Pause, Unpause, RotateAdmin, TombstonePost). The helper still exists for non-admin internal cross-contract calls, but admin-gated paths use admin-only checks (closes HIGH 4: now it's a clean code change, not a config trick).
- Tombstone-via-governance is removed (closes HIGH 5: no destructive governance bypass).
- Recovery path no longer routes through the governance contract (closes FATAL 2): for 2-key loss, recovery is via x/upgrade chain-binary migration coordinated by the validator set, NOT a governance proposal. At launch the founder is the validator, so this is a manual operator procedure with no contract dependency.

Routine signing topology is redesigned (closes FATAL 3): Key A is laptop (hot), Key B moves from "Ledger plugged into laptop" to **a separate phone with hardware-backed keystore that signs independently of the laptop** (warm but physically separate device). Routine ops require the founder to authorize on TWO independent devices — laptop keylogger alone gives only Key A, attacker still needs phone unlock to get Key B. Key C stays cold in lawyer-held escrow with duress-resistant property.

Operational hardening:
- **Hardware wallet display requirement** (closes HIGH 6): all signing devices used in admin flows MUST display the full Cosmos message bytes for human verification before signing — not condensed summaries. This is an explicit operational requirement, with verification at quarterly drills.
- **Monitoring/tripwire service required** (closes HIGH 7 + MODERATE 12): a watch service monitors the chain for suspicious admin-action patterns and pages the founder on out-of-band channels. The service does NOT have signing authority — it only detects and alerts. (Deadman pre-signed pause noted as future improvement; doesn't mix cleanly with multisig and is deferred.)
- **Successor plan / dead-man's switch** (closes HIGH 8): founder maintains a sealed envelope with a designated lawyer containing key locations, recovery runbook, and "do not release except on verified incapacitation" instructions. Required before mainnet launch.
- **Dissolution triggers** (closes HIGH 9): three hard triggers added — XP distribution falls below 50% founder-held → multisig MUST dissolve; active validator count > 5 → multisig MUST dissolve; 24-month time cap from mainnet launch → multisig dissolves regardless. Dissolution sequence: multisig calls DisableAdmin on all 10 contracts in one batch tx, CosmWasm admin transferred to a no-op address (or to a new community-multisig).
- **Lawyer-held Key C** (closes HIGH 10): Key C is held in legal escrow with a trusted attorney, NOT in a personal safe. Release requires verified founder authorization through a documented procedure that resists coercion. Attorney-client privilege provides legal/social cover.
- **Quarterly key rotation drill** added: founder practices the full rotation flow once per quarter to ensure the procedures actually work and to catch operational issues before a real incident.

XP-vs-multisig clarification (closes MODERATE 13): the founder's XP-holding wallet is SEPARATE from the multisig admin keys. The multisig has zero governance voting power by design. This means recovery-via-governance is impossible by design — recovery is only via x/upgrade chain-binary migration. (Acknowledges and resolves the conflation explicitly.)

Paper-backup standard added (closes MODERATE 14): if any cold key uses a written backup, it MUST be a SLIP-39 split or a metal seed plate, generated and verified from a cold-boot air-gapped machine. Plain paper-in-envelope is prohibited.

2-of-3 vs 3-of-5 (MODERATE 11): retained 2-of-3 for round 2 but with explicit acknowledgment that 3-of-5 is the recommended topology for any future scaling. Documented as an "implementation note" — to be revisited if Key B or Key C ever fails or needs replacement.

---

### Round 2

**Revised Proposal:**

**1. Multisig topology — 2-of-3 with physically distributed routine signers**

Cosmos SDK 2-of-3 multisig wallet as the in-contract admin address on all 10 contracts at instantiation time.

- **Key A — Laptop (hot).** Founder's primary dev machine. Cosmos signing key stored encrypted (FDE + login). Used as one of the two routine signers.
- **Key B — Phone with hardware-backed keystore (warm, physically separate from laptop).** A standalone Cosmos signer app on the founder's smartphone, key sealed in the phone's hardware security element (Secure Enclave / TEE). Phone is in a separate physical pocket from the laptop and has its own biometric unlock. Independent compromise vector from the laptop. Used as the second routine signer.
- **Key C — Lawyer-held cold key (cold, duress-resistant).** Generated offline on an air-gapped machine, written via SLIP-39 split OR metal seed plate (paper-in-envelope is prohibited), held in legal escrow with a trusted attorney. Release procedure documented with the attorney; release requires verified founder authorization that resists coercion (e.g., founder must appear in person during business hours over a defined waiting period).

Threshold: 2-of-3.

**2. Safety net flows**

- **Routine pause / unpause / tombstone:** Key A (laptop) + Key B (phone). Founder constructs the tx on laptop, gets Key A signature, then independently signs the same tx body on the phone — verifying the full message bytes on the phone screen before approving. Two independent compromise surfaces. Target latency: under 10 minutes from incident detection (revised from 5 minutes per HIGH 7).
- **Rotation:** Founder retrieves Key C from legal escrow (multi-day procedure) and signs with B + C. Or, if Key A is suspected compromised, B + C is the rotation set; if Key B is compromised, A + C. Target latency: 3-5 days due to escrow retrieval.
- **Lost-key recovery (2 keys):** Founder uses surviving key + chain-binary migration via x/upgrade. NOT a governance proposal — at launch the founder is the validator; post-launch this requires validator set coordination. Manual operator procedure. Documented in a runbook.
- **Founder death / incapacitation:** Sealed envelope with executor lawyer triggers the recovery runbook. The lawyer has Key C and the runbook for transferring control to a designated successor or community-multisig.

**3. Authorization model — multisig is sole admin, governance has zero admin powers**

Governance is REMOVED from `AUTHORIZED_CALLERS` on all 10 contracts. CosmWasm admin (chain-level) is transferred from the governance contract address to the multisig wallet address. The shared `check_admin_or_authorized` helper continues to exist for inter-contract internal calls (e.g., experience contract validating that forum is calling its mint function), but admin-gated message handlers (Pause, Unpause, RotateAdmin, TombstonePost) use `check_admin` directly — no authorized-caller bypass for admin paths.

Implications:
- Governance can still pass proposals, vote, manage subjects, process auditing — all the community-decision functions stay intact.
- Governance can NO LONGER call Pause/Unpause/RotateAdmin/TombstonePost or migrate contract code.
- The multisig is the only path to admin-gated actions.
- This creates a clean separation: multisig = safety net (founder-controlled), governance = community decisions.

**4. Recovery paths**

| Failure | Action | Latency |
|---|---|---|
| 1 key suspected compromised | Rotate via the other 2 keys | Hours-to-days |
| 1 key lost (device dies / forgotten phone) | Continue with remaining 2 of 3, rotate at convenience | Days |
| 2 keys lost | Surviving key + chain-binary migration via x/upgrade (validator-coordinated) | Days |
| 3 keys lost | Community fork only (manual social process) | Weeks |
| Founder incapacitation | Lawyer triggers successor runbook | Per legal procedure |

Recovery path explicitly does NOT depend on the governance contract being unpaused or operational — it depends on the validator set, which is operationally separate.

**5. Operational requirements (BLOCKING for mainnet launch)**

- **R1.** Hardware wallet / phone signer must display FULL Cosmos message bytes for verification before signing. Verified during quarterly drill. (Closes HIGH 6: signing-host substitution.)
- **R2.** Monitoring / tripwire service running 24/7. Monitors chain for suspicious admin-action patterns (rate of admin-gated messages, large XP grants, contract migration attempts) and pages the founder via out-of-band channels (SMS + email + push). The service has READ-ONLY chain access; no signing authority. (Closes HIGH 7 + MODERATE 12.)
- **R3.** Successor plan documented and lodged with attorney. Sealed envelope contents: key locations, recovery runbook, "do not release except on verified incapacitation," and successor designation. (Closes HIGH 8.)
- **R4.** Quarterly key rotation drill. Founder runs through the full rotation procedure (retrieve Key C, sign rotation tx, verify on chain, restore Key C to escrow) once per quarter to keep procedures fresh and catch operational issues. (Operational hardening.)
- **R5.** Backup standard: if any cold key uses a written backup, it MUST be a SLIP-39 split OR a metal seed plate, generated and verified from a cold-boot air-gapped machine. Paper-in-envelope is prohibited. (Closes MODERATE 14.)

**6. Decision-006 dissolution ramp**

The multisig is incubation-only. Dissolution is REQUIRED when any of the following triggers fire:

- **Trigger D1 (XP distribution):** No single entity holds more than 50% of total XP across all subjects. Measured via on-chain query.
- **Trigger D2 (validator decentralization):** Active validator count exceeds 5 with no single entity controlling more than 1/3 of voting power.
- **Trigger D3 (time cap):** 24 months from mainnet launch, regardless of D1 / D2 status.

Dissolution sequence:
1. Multisig calls `DisableAdmin` on all 10 contracts in one batch tx (signed by 2-of-3).
2. CosmWasm admin transferred from the multisig wallet to a community-controlled multisig OR to a no-op burn address (depending on community decision at the time).
3. Multisig wallet is wiped (keys destroyed) after a 30-day cooldown to ensure no rollback is needed.
4. From this point, the only path to admin-gated actions is via the post-incubation governance topology (designed in a separate effort).

Dissolution is NOT optional once a hard trigger fires. The founder may dissolve earlier at their discretion but may NOT delay past a fired trigger.

**7. XP vs multisig key separation**

The founder's XP-holding wallet is a DIFFERENT address from the multisig admin wallet. The multisig has zero XP and zero governance voting power by design. This explicitly resolves MODERATE 13: there is no recovery path through governance because the multisig cannot vote. Recovery is exclusively via x/upgrade chain-binary migration.

**8. Trade-offs explicitly accepted**

- Pause is a 5-10 minute lever, not a single-second lever. Documented and accepted; bridged by the monitoring service (R2) which provides early detection.
- Lost-key recovery requires validator coordination, not governance. At launch this is "founder-as-validator does manual restart"; post-launch this requires a validator-rescue runbook.
- Governance loses all admin powers. This is an explicit choice — community-decision layer is separate from safety-net layer.
- 2-of-3 has minimal headroom. Documented; revisit at first key replacement event.
- Multisig will dissolve at a defined trigger (no permanent backdoor). The founder commits to this in writing.

**9. Out of scope for round 2 (deferred to future effort or implementation notes)**

- Deadman pre-signed pause via tripwire (doesn't mix cleanly with multisig; deferred)
- 3-of-5 topology upgrade (revisit on first key replacement)
- Time-locked rotation with cancel-window
- HSM / KMS integration
- MPC instead of multisig
- Co-founder onboarding flow

**Critique findings — Round 2 (3 FATAL, 8 HIGH, 5 MODERATE):**

Round 2 critic actually read the chain code and found chain-level authority paths the proposal hadn't addressed at all.

1. **FATAL — Chain-level x/gov retains wasm authority.** `app/wasm.go:61` instantiates WasmKeeper with `govModuleAddr` (Cosmos SDK x/gov module) as authority. **x/gov can issue MsgStoreCode, MsgMigrateContract, MsgUpdateAdmin, MsgUpdateInstantiateConfig, MsgPinCodes against any contract** regardless of in-contract admin or CosmWasm contract admin. At launch the founder is sole validator, can self-approve any x/gov proposal from their staking key alone. Staking key is a 4th key not in the multisig. The multisig is bypassed at the chain level.
2. **FATAL — `ScheduleUpgrade` / `CancelUpgrade` authority is hardcoded to the governance contract in app_config.go.** `app/app_config.go:226` sets `upgradetypes.Module.Authority = "os1hnvfl0z2madv8k505msf9f4lztjtv9sh4pf5z4tjxpuded337unqu6e03d"` — the governance contract address is compiled into the chain binary. Multisig CANNOT revoke this without rebuilding the chain binary. A passing governance proposal can schedule a chain-binary swap, and the founder's ~100% XP makes such a proposal trivial to pass.
3. **FATAL — `AUTHORIZED_CALLERS` is append-only.** No `unregister_caller` helper, no `AdminUnregisterCaller` message on any contract. The Round 2 "remove governance from AUTHORIZED_CALLERS" claim is unimplementable as stated — it requires (a) new helper code, (b) new ExecuteMsg variant on all 10 contracts, (c) migration of all 10 contracts via WasmMsg::Migrate, (d) which requires CosmWasm admin = governance, (e) which means a governance proposal authorizing migration, (f) which during the migration window the governance contract still has the bypass we're trying to remove. Catch-22.
4. **HIGH — Multisig has dictator power over governance.** Round 2 makes the multisig the admin of the governance contract. Multisig can Pause governance, halting any in-flight proposal, permanently. `FinalizeProposal` is NOT pause-exempt. Multisig has unaccountable veto over all democracy. Contradicts decision-006. No on-chain constraint, no auto-unpause timer.
5. **HIGH — Dissolution triggers D1/D2 not on-chain enforceable, gameable.** Multisig is a wallet — no cron, no enforcement logic. D1 ("no single entity holds >50% XP") is off-chain concept; founder can sybil to alts. Trust in dissolution = trust in founder's willingness to dissolve.
6. **HIGH — D3 unconditional dissolution at month 24 incompatible with active incident response.** Concrete failure: live exploit on day 720, founder must dissolve on schedule and abandon the incident. No grace period.
7. **HIGH — `AdminUnregisterCaller` doesn't exist** (paired with FATAL 3). Round 2 doesn't acknowledge the implementation cost.
8. **HIGH — Validator key threat model entirely absent.** Validator signing key is a 4th key not in multisig. Compromised validator key = malicious blocks, double-sign slashing, single-validator chain halt. At launch validator IS only staking-token holder, can self-approve any x/gov proposal alone.
9. **HIGH — Phone signer app doesn't exist.** R1 specifies a Cosmos signer app with Secure Enclave / TEE sealed signing and full-bytes display. Keplr Mobile uses JS-side secp256k1 — not sealed. Ledger Live Mobile is a thin viewer. No widely-audited option exists. Either build it (major sub-project) or accept degraded R1.
10. **HIGH — Laptop→phone tx bridge has substitution window.** Tx body gets from laptop to phone via QR / BT / NFC / USB — all of these can be intercepted by a laptop-level attacker (laptop is "Key A — hot," in scope for compromise). Phone displays "full message bytes" but those bytes are the substituted ones. "Two independent compromise surfaces" claim degenerates to one if the laptop is compromised before transmit.
11. **HIGH — Lawyer escrow has no specified legal instrument.** No jurisdiction, no backup attorney, no specification of what happens if lawyer dies / is disbarred / is compelled by court order / has office burn down. "Verified incapacitation" determination procedure not specified. Single-attorney single point of failure dressed as a launch blocker.
12. **HIGH — 3-5 day rotation latency conflicts with 10-min incident response.** Concrete: Key A confirmed compromised. Founder needs 2 valid signatures to do anything — but A is now untrusted. Need B + C, but C is 3-5 days away. During those 3-5 days, attacker still has half of the 2-of-3 threshold and can co-sign with B if B is also locally compromised, or simply watch every recovery move from the laptop.
13. **HIGH — Multisig needs PoW exemption to function.** Project's `x/pow/ante.go` requires every wasm execute tx from a 0-XP account to include a `pow:<nonce>` memo hashing below the difficulty target. Multisig has zero XP by design (item 7), so EVERY admin call requires PoW computed over the tx bytes BEFORE signing. For multisig flows using `--generate-only` + offline signing, the memo is part of the signed bytes — so PoW must be computed by the founder before initiating laptop signing. Workflow wrinkle nobody walked through. Higher-difficulty future PoW can push multisig response from 2s to minutes.
14. **MODERATE — R4 quarterly drill exposes Key C 4×/year at predictable intervals.** If drill is real, attacker can target the drill window. If drill is skipped, R4 fails.
15. **MODERATE — "Validator-coordinated recovery" has no concrete runbook.** And `x/upgrade` MsgSoftwareUpgrade authority is the governance contract per app_config.go:226 — circular dependency on the same governance surface the proposal sidelined.
16. **MODERATE — `execute_tombstone_post` still calls `check_admin_or_authorized` at `contracts/forum/src/contract.rs:754`.** Code doesn't match Round 2 proposal. Fix requires migration + new helper.
17. **MODERATE — No pre-launch sign-off owner for R1-R5.** Founder self-certifies items that protect against founder compromise = least useful checker.
18. **MODERATE — Recovery runbook referenced 4× and never attached.** If wrong, all four recovery paths fail.
19. **MODERATE — `DisableAdmin` batch is not atomic.** 10 separate WasmMsg::Execute in one tx, each can fail independently. Partial-failure mode: some disabled, others not.

**Fixes applied for Round 3:**

The critic's most important contribution: **the multisig design is at the contract layer, but the chain has THREE additional authority surfaces (x/gov, x/upgrade, CosmWasm contract admin) that bypass it entirely.** Round 3 must address chain-level authority, not just contract-level.

Major changes for Round 3:

**A. Chain binary rebuild required (closes FATAL 1, FATAL 2).** Pre-launch chain reset already happened once (2026-03-31). One more reset for launch with these chain binary changes:
- `app/wasm.go`: change WasmKeeper authority from `govModuleAddr` to the multisig wallet address. x/gov no longer has wasm authority. Wasm operations (StoreCode, MigrateContract, UpdateAdmin, UpdateInstantiateConfig, PinCodes) require multisig signature.
- `app/app_config.go`: change `upgradetypes.Module.Authority` from the hardcoded governance contract address to the multisig wallet address. x/upgrade ScheduleUpgrade / CancelUpgrade now require multisig signature, NOT a governance proposal.
- This means the multisig genuinely IS the sole admin path at the chain level. x/gov can still pass proposals on its own scope (parameter changes for validator set, slashing, etc.) but cannot touch wasm.

**B. Chain reset closes the AdminUnregisterCaller catch-22 (closes FATAL 3, HIGH 7).** Pre-launch we still have one chain reset budget. The reset is the natural moment to fix the authorization model:
- Add `AdminUnregisterCaller { contract_addr }` to the shared `os_types::admin` helper and to all 10 contracts' ExecuteMsg.
- Bifurcate the shared helper: `check_admin` (admin only, no bypass) vs `check_admin_or_authorized` (existing, for inter-contract internal calls only).
- Pause/Unpause/RotateAdmin/TombstonePost handlers switch from `check_admin_or_authorized` → `check_admin`. (Closes MODERATE 16: tombstone code matches proposal.)
- At genesis, governance is NOT registered as authorized caller for any of the 10 contracts. The `AdminUnregisterCaller` message exists for future use but doesn't need to be called at launch.
- All 10 contracts redeployed as part of the reset, no migration dance needed.

**C. Governance is non-pausable (closes HIGH 4 — dictator over governance).** The governance contract is added to the pause exemption list at the dispatch layer — `if !matches!(msg, Pause | Unpause | RotateAdmin | TombstonePost) && contract_id != GOVERNANCE_CONTRACT_ID`. Or simpler: governance contract uses a different dispatcher template that doesn't include the pause guard at all. The multisig can still rotate governance's admin and migrate its code (it's still the admin), but cannot pause governance into silence. This preserves the safety-net role for governance contract bugs while removing the dictator vector.

Actually simpler and stronger: **governance contract has NO admin authority at all post-genesis**. The genesis state sets governance contract's admin to None. Governance is fully autonomous — no Pause, no Unpause, no Rotate, no Migrate via wasm-admin. Only x/gov-on-its-own-params can affect it (which is a chain-level concern, separate from the multisig). This is more aligned with decision-006 anyway.

We adopt this: **governance contract starts with admin = None at genesis.** The shared admin helper still exists in governance's code for any reasonable future where a governance bug needs an emergency upgrade, but the genesis config disables admin from day 0. Multisig has zero authority over governance.

**D. Hard time-cap built into contract code (closes HIGH 6 — D3 vs incident response).** Each contract has a `DISSOLUTION_BLOCK` constant set at instantiation. After that block, all admin-gated handlers (Pause, Unpause, RotateAdmin, TombstonePost) return `DissolutionPassed` error. The multisig can extend by submitting `ExtendDissolution { new_block }` — gated by check_admin, requires the new_block to be at most CURRENT + 30 days, AND the total cumulative extension cannot exceed 12 months past the original DISSOLUTION_BLOCK. So the hard ceiling is: original 24 months + 12 months extension cap = 36 months absolute maximum.

This means dissolution is enforced ON CHAIN by contract code, not by the founder's honor. D1/D2 stay advisory (closes HIGH 5 with the acknowledgment that those triggers can't be on-chain enforced anyway). D3 becomes hard-enforced with a bounded extension window for incident response.

**E. Validator key topology decision (closes HIGH 8).** At launch the founder runs a single validator. The validator signing key (the consensus key, NOT the operator key) is a separate concern from the multisig — Cosmos validator keys are required to be online (warm) for block production and can't easily be multisigged. The validator OPERATOR key (used to delegate / undelegate / change commission / vote in x/gov as a validator) IS a normal account key and can be multisigged.

Round 3 design:
- Validator consensus key: single key, on the validator machine. Standard Cosmos pattern. Documented as a separate trust component with its own threat model. Compromise = double-signing risk + halt risk. Mitigation: dedicated machine, no other software, network-isolated from the founder's dev environment.
- Validator operator key: SAME multisig as the contract admin. So delegation, commission changes, and validator-account x/gov votes all require 2-of-3.

This means a compromised consensus key can halt the chain or double-sign but cannot vote x/gov. The 4th-key threat model is bounded to "can sabotage block production" not "can take over governance."

**F. Phone signer app dropped, replaced with hardware-wallet-with-byte-display (revises HIGH 9, HIGH 10).** Round 2's phone signer requirement was unrealistic. Round 3 replaces it with the realistic Cosmos pattern:
- Key B is a Ledger or similar hardware wallet plugged into the laptop.
- Operational requirement: the Ledger MUST display the FULL Cosmos message bytes for verification before signing (R1 unchanged in spirit but specified for hardware wallet, not phone). This requires the Cosmos Ledger app version that supports full-message display — verified at launch time and at quarterly drills.
- We accept that this returns to the "1-of-1 effective threshold" problem from Round 1's FATAL 3 in the literal sense of physical proximity. Mitigation: the Ledger's secure element protects against laptop-only compromise as long as the byte verification is real. A laptop attacker can substitute the message bytes the Ledger sees, but the founder MUST mentally compare the displayed bytes against the intended action.
- Compensating control: tripwire monitoring (R2 unchanged) detects post-signing anomalies and pages the founder. If a substitution attack succeeds, the tripwire catches the result within seconds.
- Compensating control: the multisig has a separate rotation gate (Key C in escrow) that the laptop attacker cannot reach. So a successful substitution attack cannot rotate the admin to attacker keys — only B + C can.

This trades "two physical surfaces" for "one physical surface + verified hardware verification + tripwire detection + cold rotation gate." Less ideal than two separate devices but actually deployable.

**G. Multisig PoW exemption (closes HIGH 13).** Two options:
- (i) Add the multisig wallet address to the PoW ante decorator exemption list at the chain level. Hardcoded in `x/pow/ante.go`. Requires chain binary change but is included in the Round 3 chain rebuild anyway.
- (ii) Pre-fund the multisig wallet with a small XP balance at genesis (1 XP in any subject) so the existing balance-based exemption fires.

Pick (i) — explicit allowlist is clearer. Multisig address is added to the exemption list as part of the chain binary changes for Round 3.

**H. Lawyer escrow upgraded (closes HIGH 11).** Replace single-attorney with multi-attorney redundancy:
- Key C is generated and split via SLIP-39 into a 2-of-3 share scheme.
- Each share is held by a different attorney in a different jurisdiction (e.g., one US, one EU, one Singapore).
- Release procedure: founder must request from at least 2 of 3 attorneys, providing duress-resistant verification (in-person appearance during business hours, at least 7-day waiting period, lawyer can refuse on suspicion of coercion).
- Legal instrument: contingent release deed at each attorney's office, governed by that jurisdiction's law.
- Backup if attorney dies / firm dissolves: each release deed designates a successor firm.
- This is THREE single-points-of-failure that all have to fail simultaneously — meaningfully more robust than one attorney.

**I. Faster compromise rotation path (closes HIGH 12).** The 3-5 day rotation latency was an artifact of "Key C in one safe." With Key C now SLIP-39 split across 3 attorneys, the founder can pre-coordinate with attorneys to maintain a "warm escrow" relationship — attorneys know the founder, know the procedure, can respond faster than cold escrow. Target rotation latency: under 48 hours from incident detection.

For incident-pause specifically (NOT rotation), the founder can still pause within 10 minutes using the routine signing flow (laptop + Ledger). Pause is the immediate response. Rotation comes after. The 48-hour rotation latency is acceptable IF pause works, because pause stops further damage.

If both A AND B are compromised simultaneously, the founder has lost all routine signing capacity AND can't even pause. In that scenario, the founder must contact attorneys to retrieve Key C parts AND have nothing to combine with (since both A and B are compromised). They need to generate fresh Key D and Key E from cold, then use Key C + D for emergency rotation. This is the "all keys compromised" scenario and recovery time is days.

We accept this as the worst case. Mitigation: tripwire detects A+B compromise quickly so the window is small.

**J. Recovery runbook is a required artifact (closes MODERATE 18, MODERATE 15).** Add R6 to the launch blockers: `docs/runbooks/admin-recovery.md` exists, covers: 1-key compromise, 2-key compromise, 3-key compromise, founder incapacitation, validator key compromise, chain halt recovery. Each scenario has a step-by-step procedure. The runbook is reviewed annually by the founder + at least one trusted advisor.

**K. Pre-launch sign-off (closes MODERATE 17).** Add R7: a designated trusted advisor (lawyer, technical advisor, or auditor) reviews and signs off on R1-R6 before mainnet launch. The sign-off is a one-page document with their name, the date, and a checklist. Filed with the legal escrow.

**L. DisableAdmin atomicity (closes MODERATE 19).** Dissolution sequence is changed from "one batch tx with 10 calls" to "10 separate txs, executed in dependency order, each verified before the next." A small Python script orchestrates the sequence and aborts on any failure. Document in the runbook.

**M. R4 drill safer (closes MODERATE 14).** Quarterly drill becomes a TABLETOP exercise, not an actual key retrieval. The founder walks through the procedure with attorneys without actually moving keys. Real key movement only on actual incidents. This means a "real" rotation has never been live-tested before its first use — accepted risk, mitigated by the tabletop exercise being thorough.

---

### Round 3

**Revised Proposal:**

**1. Multisig topology — 2-of-3 (laptop + Ledger + lawyer-escrowed SLIP-39 split)**

Cosmos SDK 2-of-3 multisig wallet as the in-contract admin address on all 10 contracts AND as the validator operator key.

- **Key A — Laptop (hot).** Founder's primary dev machine. Cosmos signing key encrypted at rest (FDE + login).
- **Key B — Ledger hardware wallet (warm).** Plugged into laptop for signing. **The Ledger MUST run a Cosmos app version that displays the FULL message bytes for human verification before signing** — not condensed summaries. Verified at launch and quarterly.
- **Key C — Lawyer escrow with SLIP-39 split.** Generated offline on an air-gapped machine. SLIP-39 2-of-3 share scheme. Each share held by a different attorney in a different jurisdiction (e.g., one US, one EU, one Singapore). Each attorney holds a contingent release deed governed by their jurisdiction. Each release deed names a successor firm. Release procedure: founder requests from at least 2 of 3 attorneys, in-person appearance during business hours, 7-day waiting period, lawyer can refuse on suspicion of coercion.

Threshold: 2-of-3.

**2. Chain binary changes (REQUIRED, applied in pre-launch chain reset)**

The chain binary is rebuilt with the following changes before mainnet launch:
- `app/wasm.go`: WasmKeeper authority changed from `govModuleAddr` to the multisig wallet address. **x/gov no longer has wasm authority.** Wasm operations (StoreCode, MigrateContract, UpdateAdmin, UpdateInstantiateConfig, PinCodes) require multisig signature.
- `app/app_config.go`: `upgradetypes.Module.Authority` changed from the hardcoded governance contract address to the multisig wallet address. **x/upgrade ScheduleUpgrade / CancelUpgrade require multisig signature**, not a governance proposal.
- `x/pow/ante.go`: multisig wallet address added to PoW exemption list.
- Genesis state: governance contract's `admin` field set to `None` from day 0 (governance is autonomous, not multisig-controlled).
- Genesis state: the 10 contracts' `AUTHORIZED_CALLERS` map does NOT include the governance contract.
- Genesis state: each contract's `DISSOLUTION_BLOCK` constant set to `genesis_block + (24 months in blocks)`.

**3. Authorization model — multisig is sole chain-level admin path**

- Pause/Unpause/RotateAdmin/TombstonePost handlers use `check_admin` (admin only, no bypass).
- Cross-contract internal calls (e.g., experience contract validating that forum is calling its mint function) use `check_admin_or_authorized`.
- The shared `os_types::admin` helper is bifurcated: `check_admin` and `check_admin_or_authorized` are separate functions with separate uses.
- `AdminUnregisterCaller { contract_addr }` message added to all 10 contracts as a future tool — not used at launch but available.
- Governance contract has admin = None from genesis. **No human or multisig has authority over the governance contract.**

**4. Hard dissolution time-cap (on-chain enforced)**

Each contract has a `DISSOLUTION_BLOCK` storage item set at instantiation. After that block, all admin-gated handlers return `DissolutionPassed` error.

The multisig can extend dissolution via `ExtendDissolution { new_block }`:
- Gated by `check_admin` (multisig only).
- new_block must be at most CURRENT + 30 days.
- Cumulative extensions cannot exceed 12 months past the original DISSOLUTION_BLOCK.
- Hard ceiling: 24 months + 12 months extension = 36 months absolute maximum.

After 36 months from genesis, the multisig CANNOT be extended further. All admin functions return errors permanently. Recovery from this point is via x/gov-on-chain-params (which still has authority over Cosmos SDK parameter governance).

D1/D2 from Round 2 are now ADVISORY ONLY and not enforced on-chain (acknowledged limitation).

**5. Safety net flows**

- **Routine pause / unpause / tombstone:** Key A (laptop) + Key B (Ledger plugged into laptop, full byte verification). Target latency: under 10 minutes from incident detection.
- **Rotation (compromise scenario):** Key A (or B) + Key C (retrieved from at least 2 of 3 attorneys via warm escrow procedure). Target latency: under 48 hours.
- **Lost-key recovery (2 keys lost):** Surviving key + Key C reconstruction (2 of 3 attorney shares) + new key generation. Procedure documented in admin-recovery runbook.
- **Chain-binary recovery:** Multisig signs `MsgSoftwareUpgrade` directly via x/upgrade authority. No governance dependency.

**6. Validator key topology**

- **Validator consensus key:** Single key, on the validator machine. Standard Cosmos pattern. Documented as separate trust component with its own threat model. Mitigation: dedicated machine, no other software, network-isolated from founder's dev environment.
- **Validator operator key:** SAME 2-of-3 multisig as the contract admin. Delegation, commission changes, and validator-account x/gov votes all require 2-of-3.
- **Compromise scope:** A compromised consensus key can halt the chain or double-sign but cannot vote x/gov on substantive proposals. 4th-key threat is bounded to "sabotage block production," not "take over governance."

**7. Operational requirements (BLOCKING for mainnet launch)**

- **R1.** Cosmos Ledger app verified to display FULL message bytes for human verification.
- **R2.** Monitoring / tripwire service running 24/7. Pages founder via SMS + email + push on suspicious admin-action patterns. READ-ONLY chain access.
- **R3.** SLIP-39 split of Key C across 3 attorneys in 3 jurisdictions, each with contingent release deeds and successor firm designations.
- **R4.** Quarterly TABLETOP rotation drill (not live retrieval). Founder walks through the procedure with attorneys.
- **R5.** Backup standard: SLIP-39 split OR metal seed plate. Paper-in-envelope prohibited.
- **R6.** `docs/runbooks/admin-recovery.md` exists, covers all recovery scenarios, reviewed annually.
- **R7.** Designated trusted advisor reviews and signs off on R1-R6 before mainnet launch. Sign-off filed with legal escrow.

**8. XP vs multisig key separation**

The founder's XP-holding wallet is a DIFFERENT address from the multisig admin wallet. The multisig has zero XP and zero governance voting power. Recovery via governance is impossible by design — recovery is via multisig-controlled x/upgrade chain-binary migration (per the chain binary changes in section 2).

**9. Dissolution sequence**

When DISSOLUTION_BLOCK passes (or the founder triggers early dissolution at their discretion):

1. Multisig calls `DisableAdmin` on each of the 10 contracts in 10 SEPARATE txs, executed in dependency order. Each tx is verified before the next is submitted. A Python script orchestrates the sequence and aborts on any failure.
2. Multisig calls `MsgUpdateInstantiateConfig` to remove instantiation permissions from the wasm module (no new admin-controlled contracts can be instantiated by the multisig).
3. Chain binary `WasmKeeper` authority is migrated from multisig to a no-op burn address via a final multisig-signed `MsgSoftwareUpgrade`.
4. Multisig wallet keys are destroyed after a 30-day cooldown.

**10. Trade-offs explicitly accepted**

- Pause is a 5-10 minute lever (bridged by R2 monitoring).
- Routine signing surface is laptop + Ledger physically together — single laptop compromise + successful Ledger byte substitution = adversary can sign one routine action. Compensating controls: byte verification (R1), tripwire detection (R2), cold rotation key (Key C) that the laptop attacker cannot reach, so substitution attacks cannot rotate admin to attacker.
- Multisig has dictator power over the 10 admin contracts (but NOT governance, which is autonomous from genesis).
- 36-month hard ceiling means the safety net WILL dissolve regardless of incidents in progress at month 36. Accepted because the alternative (perpetual safety net) contradicts decision-006.
- D1 / D2 dissolution triggers are honor-system advisory. D3 (time cap) is the only on-chain enforced trigger.
- Validator consensus key is single-key (compromise = block production sabotage, not governance takeover).

**11. Implementation requirements (NEW work to be done before launch)**

- Add `AdminUnregisterCaller` ExecuteMsg + handler to all 10 contracts.
- Bifurcate `os_types::admin` into `check_admin` and `check_admin_or_authorized` with clear use cases.
- Update Pause/Unpause/RotateAdmin/TombstonePost handlers in all 10 contracts to use `check_admin` (currently they use `check_admin_or_authorized` per the existing helper).
- Update `execute_tombstone_post` in `contracts/forum/src/contract.rs` to use `check_admin`.
- Add `DISSOLUTION_BLOCK` storage item to all 10 contracts.
- Add `ExtendDissolution { new_block }` ExecuteMsg + handler with the bounded-extension logic.
- Add `DissolutionPassed` error variant.
- Update execute() dispatchers to check `DISSOLUTION_BLOCK` before processing admin-gated messages.
- Chain binary changes: WasmKeeper authority, x/upgrade authority, x/pow exemption list, governance contract genesis admin = None.
- Build Python orchestration script for dissolution sequence.
- Write `docs/runbooks/admin-recovery.md`.
- Build monitoring / tripwire service (separate sub-effort, blocking R2).
- Negotiate legal escrow with 3 attorneys in 3 jurisdictions (operational, not code).
