# Expression Contract — Technical Specification

**Date:** 2026-03-21
**Status:** Critic-chain validated (4 rounds, 55 issues, all FATAL/HIGH resolved)
**Depends on:** Experience contract, Subject contract, Governance contract
**Derives from:** Brainstorm 011 (Constitutional Governance Model), Brainstorm 012 (Certification Anatomy), Brainstorm 013 (Expression UX Refinements)

---

## Goal

Community members express their positions on governance dimensions using continuous values. The contract calculates cohesion (degree of consensus) per dimension. When cohesion sustains above threshold, the system observes, reconfirms, and auto-enacts parameter changes — no formal vote required for GER/CEP tracks. Subject-level expression feeds into the existing governance dual-track (Decision 007).

---

## 1. Tracks

Three governance tracks operate at different levels with a supremacy hierarchy:

### 1.1 Track 1: Subject/Project

- **Who can express:** Anyone with ≥1 XP in the subject
- **Voice model:** XP-weighted (your vote weight = your XP in that subject)
- **What it governs:** Domain-specific parameters within a subject
- **Amendment flow:** Cohesion detection → bridge (3-of-5 epoch stabilization → 70% XP-weighted vote) → GER supremacy check
- **Supremacy check:** 1-epoch challenge window after vote passes. External auditor panel (5 people) if challenged.

### 1.2 Track 2: GER (Global Ethical Anchors)

- **Who can express:** Qualified accounts (see §2)
- **Voice model:** 1-person-1-vector, equal voice (gate IS the sybil defense)
- **What it governs:** Interpretations of the Sovereign Choice Axiom ("No person may reduce another's ability to choose")
- **Amendment flow:** Cohesion ≥9000 + quorum + population minimum → 12-of-20 epoch observation → 4-epoch reconfirmation → auto-enact
- **Examples:** "Should anonymous participation be protected?" "Does mandatory insurance restrict freedom?"

### 1.3 Track 3: CEP (Core Expression Protocol)

- **Who can express:** GER-qualified + ≥1 on-chain governance vote
- **Voice model:** 1-person-1-vector, equal voice, no governance experience bonus
- **What it governs:** Governance mechanics, GER dimension-to-parameter mappings
- **Amendment flow:** Same as GER
- **Supremacy check:** 2-epoch GER challenge window after passage. 7-person panel (supermajority 5/7) if challenged.

### 1.4 Supremacy Hierarchy

```
GER (ethical anchors) — hardest to change, most protected
    > CEP (governance mechanics)
        > Subject/Project (domain governance)
```

Children cannot contradict parents. Challenge mechanisms at each boundary.

---

## 2. Qualification

### 2.1 Subject/Project Qualification

Any account with ≥1 XP in the subject. Checked via cross-contract query to experience contract.

No configurable gates per subject at launch. If problems emerge, governance can propose adding gates later.

### 2.2 GER Qualification

EITHER path qualifies:

- **Path A (breadth):** ≥100 total verified XP + ≥3 distinct subjects with XP + ≥2 distinct contribution types
- **Path B (depth):** ≥300 verified XP in a single subject + ≥2 distinct contribution types

**Qualification checking:** The experience contract does NOT have efficient queries for "distinct subjects with XP" or "distinct contribution types." Iterating `TransactionHistory` is a global scan — infeasible at scale.

**Solution:** The expression contract maintains its own qualification index, updated via a permissionless `RefreshQualification` message:

1. `RefreshQualification { account }` queries the experience contract's `BalancesByUser` (paginated, returns subject→balance pairs) and counts distinct subjects with balance > 0
2. For contribution types: the experience contract needs a new query `DistinctSourceTypes { user }` that returns the set of SourceType values the user has earned XP from. This requires a new storage index in the experience contract: `SOURCE_TYPES_BY_USER: Map<&Addr, Vec<SourceType>>` updated on each XP mint.
3. The expression contract caches the result in `QUALIFICATION_CACHE` with a TTL (default: 1 epoch)
4. On `Express`, if cache is stale or missing, the caller must first call `RefreshQualification` (or the contract auto-refreshes if gas allows — single `BalancesByUser` + single `DistinctSourceTypes` = 2 cross-contract queries, ~100-150K gas total)

### 2.3 CEP Qualification

GER qualification (Path A or B) + ≥1 on-chain governance vote at any level. Vote history checked via cross-contract query to governance contract.

### 2.4 Contribution Types

Contribution types map to `SourceType` values in the experience contract:

| SourceType | Contribution Type |
|------------|------------------|
| PostApproval | Content creation (forum post approved) |
| AuditApproval | Content approved through audit |
| AuditParticipation | Auditing (auditor earned XP for participating) |
| Upvote / Downvote | Curation |
| TagMismatch | Tag quality enforcement (penalty/reward) |
| VoteStake / VoteReturn | Governance participation |
| Genesis | Bootstrap seed XP (excluded from qualification) |

"≥2 distinct contribution types" means XP earned from at least 2 different SourceType categories (excluding Genesis). All 6 non-Genesis types count.

---

## 3. State (state.rs)

### 3.1 Track Keys

Track is NOT used directly as a Map key (enum with String cannot implement PrimaryKey).
Instead, tracks are converted to canonical string keys for storage:

```rust
/// Track identifier (used in messages, NOT as storage key)
pub enum Track {
    Subject { tag: String },
    GER,
    CEP,
}

impl Track {
    /// Canonical storage key: "ger", "cep", "subject:rust", etc.
    pub fn storage_key(&self) -> String {
        match self {
            Track::GER => "ger".to_string(),
            Track::CEP => "cep".to_string(),
            Track::Subject { tag } => format!("subject:{}", tag),
        }
    }
}
```

All Map keys use `&str` (from `storage_key()`) instead of `Track` directly.

### 3.2 Core Types

```rust
/// A single expression on a dimension
pub struct Expression {
    pub value: u16,            // 0-10000 (basis points)
    pub timestamp: u64,        // block time when first expressed
    pub renewed_at: u64,       // last renewal timestamp
    pub xp_weight: u64,        // XP at expression time (Subject track only; 1 for GER/CEP)
}

/// Configuration for a dimension
pub struct DimensionConfig {
    pub name: String,                    // human-readable name, max 64 chars, alphanumeric + hyphens
    pub description_hash: String,        // SHA-256 of full description (off-chain)
    pub dim_type: DimensionType,         // Gradient | Binary
    pub parameter_mapping: ParameterMapping, // what on-chain parameter this controls
    pub created_at: u64,
    pub created_by: Addr,
    pub frozen_since: Option<u64>,       // epoch when current freeze started (None if not frozen)
    pub total_frozen_epochs: u64,        // cumulative frozen epochs from all past observations
}

pub enum DimensionType {
    Gradient,    // 0-10000 continuous
    Binary,      // 0 or 10000 only
}

/// What on-chain parameter a dimension maps to
pub struct ParameterMapping {
    pub contract: Addr,         // target contract
    pub parameter: String,      // parameter key
    pub low_value: String,      // value when mean anchors at 0
    pub high_value: String,     // value when mean anchors at 10000
    pub enactment_target: EnactmentTarget, // what passes the value to the target contract
}

pub enum EnactmentTarget {
    /// Expression contract submits governance proposal that auto-executes (GER/CEP)
    GovernanceAutoExecute,
    /// Expression contract submits governance proposal that requires normal vote (Subject bridge)
    GovernanceProposal,
}
```

### 3.3 Incremental Cohesion Accumulators

Cohesion is calculated incrementally using running statistics — O(1) per expression change, no iteration.

```rust
/// Running statistics for O(1) cohesion calculation
pub struct CohesionAccumulator {
    // Unweighted (GER/CEP)
    pub count: u32,              // number of active expressions
    pub sum: u64,                // sum of values
    pub sum_sq: u64,             // sum of values squared

    // Weighted (Subject track only — stored but unused for GER/CEP)
    pub sum_weight: u64,         // sum of XP weights
    pub sum_weighted_val: u128,  // sum of (value * weight) — u128 to prevent overflow
    pub sum_weighted_val_sq: u128, // sum of (weight * value^2) — u128 required at scale

    // Derived (cached, recalculated on update)
    pub cohesion: u16,           // 0-10000
    pub last_updated: u64,
}
// Note: u128 is necessary for weighted accumulators because weight * value^2 can reach
// 10^7 (XP) * 10^8 (value^2) = 10^15 per expression. At 10K expressors: 10^19, near u64 max.
// u128 supports up to 3.4 * 10^38 — safe for any realistic scale.
```

**On Express:** Add new value to accumulators. If updating existing expression, subtract old value first, then add new.
**On WithdrawExpression:** Subtract value from accumulators.
**On SnapshotEpoch:** Read cached cohesion directly — no iteration needed.

Variance from accumulators:
- Unweighted: `variance = sum_sq/count - (sum/count)^2`
- Weighted: `variance = sum_weighted_val_sq/sum_weight - (sum_weighted_val/sum_weight)^2`

### 3.4 Observation and Challenge State

```rust
pub struct ObservationState {
    pub start_epoch: u64,
    pub current_epoch: u64,
    pub qualifying_epochs: u8,
    pub total_epochs: u8,
    pub snapshots: Vec<EpochSnapshot>,  // max OBSERVATION_WINDOW entries
    pub status: ObservationStatus,
}

pub enum ObservationStatus {
    Observing,
    ReadyForReconfirmation,
    Reconfirming { window_end: u64, extended: bool },
}

pub struct EpochSnapshot {
    pub epoch: u64,
    pub cohesion: u16,
    pub expressor_count: u32,
    pub qualified: bool,
}

pub struct Moratorium {
    pub until_epoch: u64,
    pub consecutive_failures: u8,   // u8 sufficient — "contested" flag at 3
}

pub struct SupremacyChallenge {
    pub dimension: String,
    pub track_key: String,               // storage key of track being challenged
    pub challenger_track_key: String,    // "ger" for all challenges
    pub justification_hash: String,
    pub flaggers: Vec<Addr>,
    pub panel: Option<Vec<Addr>>,
    pub commits: Vec<(Addr, String)>,
    pub reveals: Vec<(Addr, bool)>,
    pub status: ChallengeStatus,
    pub created_at: u64,
    pub deadline: u64,
}

pub enum ChallengeStatus {
    Gathering,
    PanelSelected,
    Revealing,
    Resolved { result: ChallengeResult },
}

pub enum ChallengeResult {
    Blocked,
    Allowed,
}
```

### 3.5 Storage Keys

```rust
// Expressions: keyed by (track_key, dimension_name, address)
pub const EXPRESSIONS: Map<(&str, &str, &Addr), Expression> = Map::new("expr");
// Accumulators: keyed by (track_key, dimension_name)
pub const ACCUMULATORS: Map<(&str, &str), CohesionAccumulator> = Map::new("acc");
// Dimensions: keyed by (track_key, dimension_name)
pub const DIMENSIONS: Map<(&str, &str), DimensionConfig> = Map::new("dims");
// Observations
pub const OBSERVATIONS: Map<(&str, &str), ObservationState> = Map::new("obs");
// Moratoriums
pub const MORATORIUMS: Map<(&str, &str), Moratorium> = Map::new("mora");
// Challenges
pub const CHALLENGES: Map<u64, SupremacyChallenge> = Map::new("chal");
pub const CHALLENGE_COUNTER: Item<u64> = Item::new("chal_ctr");

// Active expressors index: per (track_key, dimension), stores count
pub const EXPRESSOR_COUNT: Map<(&str, &str), u32> = Map::new("expr_cnt");

// Qualified count per track (governance-updated)
pub const QUALIFIED_COUNT: Map<&str, u32> = Map::new("qual_cnt");

// Qualification cache
pub const QUALIFICATION_CACHE: Map<(&str, &Addr), QualificationEntry> = Map::new("qual");
pub struct QualificationEntry {
    pub qualified: bool,
    pub checked_at: u64,  // block time
}

// Reconfirmation interaction tracking: (track_key, dimension) → count of unique interactors
pub const RECONFIRMATION_INTERACTIONS: Map<(&str, &str), u32> = Map::new("reconf_int");
// Bitmap of who interacted: (track_key, dimension, address) → bool
pub const RECONFIRMATION_INTERACTED: Map<(&str, &str, &Addr), bool> = Map::new("reconf_who");

// Frivolous flag tracking
pub const FRIVOLOUS_FLAGS: Map<&Addr, FrivolousRecord> = Map::new("friv");
pub struct FrivolousRecord {
    pub count: u8,
    pub last_frivolous_epoch: u64,
}

// Bootstrap phase (manually transitioned by governance)
pub const BOOTSTRAP_PHASE: Item<BootstrapPhase> = Item::new("bootstrap");
pub enum BootstrapPhase {
    Genesis,                    // No expressions collected
    ExpressionsOpen,            // GER expressions begin (informational)
    SupremacyActive,            // ≥50 qualified → challenges active
    FullyOperational,           // ≥200 qualified → observation can trigger
}

// Config
pub const EXPERIENCE_CONTRACT: Item<Addr> = Item::new("exp_addr");
pub const SUBJECT_CONTRACT: Item<Addr> = Item::new("sub_addr");
pub const GOVERNANCE_CONTRACT: Item<Addr> = Item::new("gov_addr");
pub const EPOCH_LENGTH: Item<u64> = Item::new("epoch_len");
pub const EXPRESSION_TTL: Item<u64> = Item::new("expr_ttl");
pub const GER_COHESION_THRESHOLD: Item<u16> = Item::new("ger_thresh");
pub const GER_QUORUM_PERCENT: Item<u16> = Item::new("ger_quorum_pct");
pub const GER_QUORUM_MIN: Item<u32> = Item::new("ger_quorum_min");
pub const GER_POPULATION_MIN: Item<u32> = Item::new("ger_pop_min");
pub const OBSERVATION_WINDOW: Item<u8> = Item::new("obs_window");
pub const OBSERVATION_REQUIRED: Item<u8> = Item::new("obs_required");
pub const RECONFIRMATION_WINDOW: Item<u8> = Item::new("reconfirm_win");
pub const MORATORIUM_LENGTH: Item<u8> = Item::new("mora_len");
// Subject-track config (separate from GER/CEP defaults)
pub const SUBJECT_COHESION_THRESHOLD: Item<u16> = Item::new("sub_thresh"); // default: 7000
pub const SUBJECT_STABILIZATION_WINDOW: Item<u8> = Item::new("sub_stab_win"); // default: 5
pub const SUBJECT_STABILIZATION_REQUIRED: Item<u8> = Item::new("sub_stab_req"); // default: 3
pub const SUBJECT_BRIDGE_COOLDOWN: Item<u8> = Item::new("sub_cooldown"); // default: 3
pub const SUBJECT_MIN_EXPRESSORS: Item<u32> = Item::new("sub_min_expr"); // default: 3
pub const ADMIN: Item<Option<Addr>> = Item::new("admin");
```

---

## 4. Messages (msg.rs)

```rust
pub enum InstantiateMsg {
    pub admin: String,
    pub experience_contract: String,
    pub subject_contract: String,
    pub governance_contract: String,
    pub epoch_length: u64,           // seconds
    pub expression_ttl: u64,         // epochs
    pub ger_cohesion_threshold: u16, // basis points
    pub ger_quorum_percent: u16,     // basis points
    pub ger_quorum_min: u32,
    pub ger_population_min: u32,
    pub observation_window: u8,
    pub observation_required: u8,
    pub reconfirmation_window: u8,
    pub moratorium_length: u8,
    // Subject-track config
    pub subject_cohesion_threshold: u16,    // default: 7000
    pub subject_stabilization_window: u8,   // default: 5
    pub subject_stabilization_required: u8, // default: 3
    pub subject_bridge_cooldown: u8,        // default: 3
    pub subject_min_expressors: u32,        // default: 3
}

pub enum ExecuteMsg {
    // --- Expression ---

    /// Express a position on a dimension. Creates or updates.
    Express {
        track: Track,
        dimension: String,
        value: u16,               // 0-10000
    },

    /// Renew an existing expression without changing the value.
    /// Resets the aging clock.
    RenewExpression {
        track: Track,
        dimension: String,
    },

    /// Withdraw an expression (active removal, not just letting it fade).
    WithdrawExpression {
        track: Track,
        dimension: String,
    },

    // --- Dimensions ---

    /// Register a new dimension (GER/CEP: governance only; Subject: governance proposal)
    RegisterDimension {
        track: Track,
        name: String,
        description_hash: String,
        dim_type: DimensionType,
        parameter_mapping: ParameterMapping,
    },

    /// Retire a dimension (governance only)
    RetireDimension {
        track: Track,
        dimension: String,
    },

    // --- Observation lifecycle (permissionless cranks) ---

    /// Start observation if thresholds are met
    StartObservation {
        track: Track,
        dimension: String,
    },

    /// Snapshot current epoch's cohesion during observation
    SnapshotEpoch {
        track: Track,
        dimension: String,
    },

    /// Begin reconfirmation window after observation passes
    StartReconfirmation {
        track: Track,
        dimension: String,
    },

    /// Finalize amendment after reconfirmation (submits governance proposal)
    FinalizeAmendment {
        track: Track,
        dimension: String,
    },

    // --- Supremacy challenges ---

    /// Flag a passed proposal/amendment as incompatible with parent track
    FlagSupremacy {
        track: Track,              // track being challenged
        dimension: String,
        justification_hash: String,
    },

    /// Commit sealed vote on a supremacy challenge (panel member only)
    CommitChallengeVote {
        challenge_id: u64,
        sealed_vote: String,       // SHA-256(vote + salt)
    },

    /// Reveal vote on a supremacy challenge
    RevealChallengeVote {
        challenge_id: u64,
        vote: bool,                // true = block, false = allow
        salt: String,
    },

    /// Finalize a supremacy challenge
    FinalizeChallenge {
        challenge_id: u64,
    },

    // --- Maintenance cranks ---

    /// Clean up expired expressions from accumulator (permissionless, max 50 per call)
    CleanupExpired {
        track: Track,
        dimension: String,
        accounts: Vec<String>,
    },

    /// Refresh qualification cache for an account (permissionless)
    RefreshQualification { account: String },

    /// Update qualified count for a track (governance only)
    UpdateQualifiedCount { track: Track, count: u32 },

    // --- Bootstrap ---

    /// Advance bootstrap phase (governance only)
    AdvanceBootstrapPhase { new_phase: BootstrapPhase },

    // --- Admin ---
    AdminRegisterCaller { contract_addr: String },
    DisableAdmin {},
    UpdateConfig { /* individual config fields, all optional */ },
}

pub enum QueryMsg {
    /// Get a single expression
    Expression {
        track: Track,
        dimension: String,
        account: String,
    },

    /// Get expressions for an account (paginated)
    ExpressionsByAccount {
        account: String,
        track: Option<Track>,
        start_after: Option<String>,  // dimension name
        limit: Option<u32>,           // default 30, max 100
    },

    /// Get cohesion state for a dimension
    Cohesion {
        track: Track,
        dimension: String,
    },

    /// Get observation state
    Observation {
        track: Track,
        dimension: String,
    },

    /// Check qualification status
    QualificationStatus {
        account: String,
        track: Track,
    },

    /// List all active dimensions for a track
    Dimensions {
        track: Track,
    },

    /// Get dimension config
    DimensionConfig {
        track: Track,
        dimension: String,
    },

    /// Get moratorium state
    Moratorium {
        track: Track,
        dimension: String,
    },

    /// Get challenge details
    Challenge {
        challenge_id: u64,
    },

    /// Contract config
    Config {},
}
```

---

## 5. Logic

### 5.1 Express

1. Validate `value` is in range (0-10000; for Binary dimensions: must be 0 or 10000)
2. Check bootstrap phase allows expression for this track
3. Check qualification for the track (§2), using cached qualification when available:
   - Subject: query experience contract for balance in subject ≥ 1
   - GER: check qualification (Path A or B), cache result
   - CEP: GER qualification + governance vote history (query governance `HasVoted`)
4. Check dimension exists and is active (not retired)
5. Check no moratorium on this dimension (for GER/CEP)
6. Determine XP weight:
   - GER/CEP: `xp_weight = 1` (equal voice)
   - Subject: `xp_weight = xp_balance(sender, subject)` — queried and **snapshotted** at expression time
7. If updating existing expression: subtract old values from accumulator first
8. Store expression: `(track_key, dimension, sender) → Expression { value, timestamp: now, renewed_at: now, xp_weight }`
9. Add new values to accumulator (O(1) — see §5.5)
10. Increment expressor count if new expression
11. Emit event: `expression_updated { track, dimension, account, value }`

### 5.2 RenewExpression

1. Verify expression exists for `(track, dimension, sender)`
2. Check expression has not already expired
3. Update `renewed_at = now`
4. No cohesion recalculation needed (value unchanged)
5. Emit event: `expression_renewed { track, dimension, account }`

### 5.3 WithdrawExpression

1. Verify expression exists for `(track_key, dimension, sender)`
2. Subtract old values from accumulator
3. Decrement expressor count
4. Remove expression from storage
5. Emit event: `expression_withdrawn { track, dimension, account }`

### 5.4 Expression Aging

Expressions are considered **active** if: `effective_age < EXPRESSION_TTL`

Where:
- `epoch = timestamp / EPOCH_LENGTH`
- `renewed_epoch = expression.renewed_at / EPOCH_LENGTH`
- `current_epoch = env.block.time / EPOCH_LENGTH`
- `real_age = current_epoch - renewed_epoch`

**Freeze mechanism:** `DimensionConfig` tracks both `frozen_since` (current freeze start) and `total_frozen_epochs` (cumulative from all past observations).

```
if frozen_since is Some(freeze_start):
    current_freeze = current_epoch - freeze_start
else:
    current_freeze = 0
total_frozen = total_frozen_epochs + current_freeze
effective_age = real_age - total_frozen
```

On unfreeze: `total_frozen_epochs += (current_epoch - frozen_since)`, then `frozen_since = None`. This preserves the frozen duration across observation cycles. No per-expression updates needed.

**Expired expression cleanup:** Lazy cleanup on self-access is insufficient — if 50 users expire without re-expressing, the accumulator drifts. Solution: a permissionless crank:

```rust
ExecuteMsg::CleanupExpired {
    track: Track,
    dimension: String,
    accounts: Vec<String>,  // max 50 per call
}
```

Anyone can call this with a list of accounts to check. For each account: if their expression on this dimension is expired, subtract from accumulator and decrement expressor count. Max 50 accounts per call to bound gas. The caller doesn't need to know who's expired — they can speculatively submit accounts and the contract checks each one. Incorrect submissions (active expressions) are simply skipped.

**RenewExpression on near-expired:** An expression can be renewed at any time before expiry. One second or one epoch — both valid. After expiry, renewal is rejected (must re-express).

### 5.5 Cohesion Calculation (Incremental)

Cohesion is derived from running accumulators — **never iterates over expressions**. All updates are O(1).

**For GER/CEP (unweighted, 1-person-1-vector):**

Using accumulators `count`, `sum`, `sum_sq`:
```
mean = sum / count
variance = sum_sq / count - mean^2
std_dev = isqrt(variance)          // integer square root
cohesion = max(0, 10000 - 2 * std_dev)
```

All arithmetic in u64. Values are u16 (0-10000), so `sum` fits in u64 for up to 2^48 expressions, `sum_sq` fits for up to 2^38 expressions (~274 billion). No overflow risk at any realistic scale.

**For Subject (XP-weighted):**

Using accumulators `sum_weight`, `sum_weighted_val`, `sum_weighted_val_sq`:
```
weighted_mean = sum_weighted_val / sum_weight
weighted_variance = sum_weighted_val_sq / sum_weight - weighted_mean^2
weighted_std_dev = isqrt(weighted_variance)
cohesion = max(0, 10000 - 2 * weighted_std_dev)
```

XP weight is **snapshotted at expression time** (stored in `Expression.xp_weight`). This prevents unrelated XP changes from silently shifting cohesion scores. When a user re-expresses, their weight is updated to current XP. This means cohesion reflects the governance opinion at the time each person expressed, weighted by their standing at that time.

**Trade-off:** Stale weights vs incoherent shifting. Stale weights are preferable because: (a) the user chose to express at that weight, (b) re-expressing updates the weight naturally, (c) observation periods are long enough that active participants re-express during them. If a user's XP doubles since their expression, they are incentivized to re-express (which captures the new weight).

**Quorum check (GER/CEP):**
```
quorum_met = expressor_count >= max(GER_QUORUM_MIN, qualified_count * GER_QUORUM_PERCENT / 10000)
```

**Note on qualified_count:**
- **GER/CEP:** Updated via `UpdateQualifiedCount` (governance-driven). A slightly stale count errs conservatively (requires more expressors for quorum).
- **Subject track:** `qualified_count` = total accounts with ≥1 XP in the subject. This can be derived from the experience contract's `BalancesByUser` query per subject, but doing so on-chain is expensive. For Subject-track reconfirmation, use the `EXPRESSOR_COUNT` (active expressors on the dimension) as the denominator instead of total qualified population. This is a tighter, more meaningful measure: "what fraction of people who actually expressed on this dimension interacted during reconfirmation?" The 30% threshold applies to expressors, not the entire subject population.

### 5.6 Observation Lifecycle

**StartObservation:**
1. Check bootstrap phase is `FullyOperational` (for GER/CEP) or `ExpressionsOpen`+ (for Subject)
2. Check cohesion ≥ threshold (9000 for GER/CEP)
3. Check quorum met
4. Check population minimum met (GER_POPULATION_MIN qualified expressors)
5. Check no active observation already running
6. Check no moratorium active
7. Create ObservationState: `start_epoch = current_epoch, qualifying_epochs = 0, total_epochs = 0, status = Observing`
8. Freeze expression aging: set `DimensionConfig.frozen_since = Some(current_epoch)`

**SnapshotEpoch:**
1. Check observation is active
2. Check current epoch > last snapshot epoch (one snapshot per epoch)
3. Calculate current cohesion
4. Record snapshot: `{ epoch, cohesion, expressor_count, qualified: cohesion >= threshold && quorum_met }`
5. Increment `qualifying_epochs` if qualified
6. Increment `total_epochs`
7. If `total_epochs >= OBSERVATION_WINDOW`:
   - If `qualifying_epochs >= OBSERVATION_REQUIRED` → observation passes, status = ready for reconfirmation
   - Else → observation fails, create moratorium, unfreeze aging (`total_frozen_epochs += current_epoch - frozen_since; frozen_since = None`)

**StartReconfirmation:**
1. Check observation status = `ReadyForReconfirmation`
2. Set status to `Reconfirming { window_end: current_epoch + RECONFIRMATION_WINDOW, extended: false }`
3. Emit event: `reconfirmation_started { track, dimension, window_end_epoch }`

**FinalizeAmendment:**
1. Check observation status is `Reconfirming` and window has ended
2. **Active-user check:** If < 30% of qualified expressors interacted with the system during the window AND not yet extended → extend window by 2 epochs, set `extended = true`, return early
3. Read cohesion from accumulator (O(1) — already maintained incrementally)
4. If cohesion still ≥ threshold:
   - Determine parameter value from mapping function (§5.9)
   - Submit via SubMsg to governance contract:
     - GER/CEP: `ProposalAction::ExpressionAmendment` with `auto_execute: true`
     - Subject: `ProposalAction::ExpressionAmendment` with `auto_execute: false` (requires normal vote)
   - Unfreeze aging: `total_frozen_epochs += current_epoch - frozen_since; frozen_since = None`
   - Delete `ObservationState` from storage (allows future observations on this dimension)
   - Reset `Moratorium.consecutive_failures = 0` if a moratorium record exists
   - Clear `RECONFIRMATION_INTERACTIONS` and `RECONFIRMATION_INTERACTED` for this dimension
   - Emit event: `amendment_enacted { track, dimension, parameter, value }`
5. If cohesion dropped below threshold:
   - Create moratorium (increment consecutive failures)
   - If 3 consecutive failures → set "contested" flag
   - Unfreeze aging: `total_frozen_epochs += current_epoch - frozen_since; frozen_since = None`
   - Emit event: `amendment_failed { track, dimension, reason: "reconfirmation_failed" }`

### 5.7 Moratorium

After a failed observation or reconfirmation:
- Moratorium lasts `MORATORIUM_LENGTH` epochs (default 6)
- No new observation can start on this dimension during moratorium
- Expressions continue to be collected normally
- After 3 consecutive failures: "contested" flag set (structured deliberation — mechanism TBD)

### 5.8 Subject-Track Bridge (3-of-5 Stabilization → Vote)

The Subject track does NOT auto-enact. It bridges to a governance vote:

1. **Cohesion detection:** Subject-track cohesion on a dimension exceeds a configurable threshold (default: 7000) for the first time
2. **3-of-5 stabilization:** Over the next 5 epochs, cohesion must remain above threshold for at least 3 epochs. This is a mini-observation — uses the same SnapshotEpoch mechanism but with shorter window (5 epochs, 3 required)
3. **Governance proposal:** On stabilization success, the expression contract submits a `ProposalAction::ExpressionAmendment { auto_execute: false }` to the governance contract. This creates a standard governance proposal that requires a 70% XP-weighted vote with 30% quorum.
4. **Supremacy check:** After the governance vote passes, the 1-epoch GER challenge window applies (see §5.10)
5. **If governance vote fails:** 3-epoch cooldown before the bridge can trigger again on this dimension

The bridge is intentionally simpler than GER/CEP observation because Subject-track has the governance vote as a second filter. The expression layer provides signal; the governance layer provides decision.

**Note:** Subject-track dimensions have different config defaults: `subject_cohesion_threshold: 7000`, `subject_stabilization_window: 5`, `subject_stabilization_required: 3`, `subject_bridge_cooldown: 3`.

### 5.9 Parameter Mapping Function

When an amendment passes, the contract must determine what parameter value to enact.

**For Gradient dimensions:** Linear interpolation based on the weighted mean of expressions.
```
mean = accumulator.sum / accumulator.count  // (or weighted equivalent for Subject)
// mean is 0-10000. Map to parameter range:
// mean=0 → low_value, mean=10000 → high_value
// For integer parameters: value = low + mean * (high - low) / 10000
// For boolean parameters: value = (mean >= 5000) ? high_value : low_value
```

**For Binary dimensions:** Majority vote.
```
// Binary values are 0 or 10000. Mean > 5000 → high_value, else low_value
```

The mapping function uses the **mean** (not cohesion). Cohesion measures consensus; the mean measures direction.

### 5.10 Supremacy Challenges

**FlagSupremacy (Subject → GER check):**
1. Caller must be GER-qualified
2. Must provide `justification_hash` (off-chain reasoning linked to specific GER dimension)
3. Within 1-epoch window after subject-level vote passed
4. Threshold to trigger panel: `max(10, 5% of qualified GER expressors within the subject)`
5. Multiple flaggers can flag the same proposal; counted toward threshold
6. When threshold reached: select 5-person panel

**FlagSupremacy (CEP → GER check):**
1. Within 2-epoch window after CEP amendment enacted
2. Threshold: 10% of qualified GER expressors
3. When threshold reached: select 7-person panel

**Panel selection:**
1. Pool: qualified GER expressors OUTSIDE the subject (for Subject challenges) or who did NOT initiate the challenge (for CEP challenges — only minimum required initiators excluded, not all supporters)
2. Selection: chain-randomness from future block hash (commit block hash at flag time, select from hash at threshold+1 block)
3. Commit-reveal voting (same mechanism as auditing contract)

**Panel decision:**
- Subject challenge: majority 3/5, 2-epoch decision window
- CEP challenge: supermajority 5/7, 3-epoch decision window
- "Block" = amendment/proposal suspended
- "Allow" = amendment/proposal proceeds

**Frivolous flag defense:**
- After 3 frivolous flags (panel voted "allow"), flagger suspended from flagging for 26 epochs
- Tracked per account

---

## 6. Cross-Contract Interactions

```
Expression Contract
    ├── queries → Experience Contract (XP balances, transaction history for qualification)
    ├── queries → Subject Contract (subject existence, participant lists)
    ├── queries → Governance Contract (vote history for CEP qualification)
    └── submits → Governance Contract (auto-enacted amendments via SubMsg)
```

The expression contract is a NEW contract (contract #10), not a modification of existing contracts.

### 6.1 Required Changes to Existing Contracts

**Governance contract** needs:

1. New `ProposalAction` variant:
```rust
ProposalAction::ExpressionAmendment {
    contract: Addr,      // target contract to modify
    parameter: String,   // parameter key
    value: String,       // new value
    auto_execute: bool,  // true for GER/CEP, false for Subject (requires vote)
}
```

2. Authorization: The governance contract must verify the SubMsg sender is the registered expression contract (stored as an authorized caller). The `(contract, parameter)` pair must be in a whitelist set by governance proposals via `RegisterParameterMapping`. This prevents the expression contract from being used as an oracle for arbitrary contract calls.

3. **Safety-first deployment:** At launch, ALL expression amendments (including GER/CEP) go through a governance vote (`auto_execute: false`). The expression system proposes; the community votes to confirm. This gives the community time to verify the cohesion/observation mechanics work correctly before trusting them.

4. **Auto-execute activation:** Once the community has confidence in the expression system (after several successful observation → vote → enact cycles), governance can vote to enable `auto_execute` for GER/CEP tracks via an `EnableAutoExecute` governance proposal. This is a one-time activation stored in the governance contract's config. Until activated, all expression amendments require a vote.

5. Auto-execute proposals (once enabled) skip the voting phase and execute immediately in `FinalizeProposal`. They are still recorded as proposals for transparency and audit trail.

**Governance contract** also needs:

A new query:
```rust
QueryMsg::HasVoted { voter: String } → { has_voted: bool }
```
Requires `HAS_VOTED: Map<&Addr, bool>` storage index, set to `true` on first vote. O(1) check.

A new proposal mode for GER/CEP expression amendments:
```rust
ProposalMode::Expression {
    // No subject — GER/CEP proposals are cross-subject
    // Voting model: 1-person-1-vector, equal voice among qualified expressors
    // Qualification checked via cross-contract query to expression contract
    // Quorum and approval thresholds from expression contract config
}
```
The current governance contract is subject-scoped (every proposal has a `subject: String`, voting power = XP in that subject). GER/CEP expression amendments are cross-subject by definition. The governance contract needs a new proposal mode that:
1. Has no subject field (or uses a reserved subject like `"_ger"` / `"_cep"`)
2. Uses equal-voice voting (1-person-1-vote among qualified expressors) instead of XP-weighted
3. Checks voter qualification via cross-contract query to the expression contract
4. This mode is ONLY used during safety-first deployment (before `EnableAutoExecute`). Once auto-execute is enabled, GER/CEP amendments skip the governance vote entirely.

**Experience contract** needs no changes — existing `Balance` and `BalancesByUser` queries are sufficient for qualification checks.

---

## 7. Bootstrap

### 7.1 Genesis Parameters

At launch, the expression contract is deployed with:
- GER dimensions: none initially (added via governance proposals once population grows)
- CEP dimensions: none initially
- Subject dimensions: can be proposed via subject-level governance
- All observation mechanisms inactive until population thresholds are met

### 7.2 Bootstrap Phase Transitions

Population thresholds are NOT computed on-chain in real-time (would require unbounded cross-contract queries). Instead, `BOOTSTRAP_PHASE` is an explicit state transitioned via governance:

```rust
ExecuteMsg::AdvanceBootstrapPhase { new_phase: BootstrapPhase }
```

This can only be called by governance (authorized caller). The governance proposal to advance the phase should include evidence (e.g., "there are now 523 unique XP-holders based on experience contract queries").

**Phase transitions:**

1. **Genesis:** No GER/CEP expressions collected. Subject-level expressions allowed.
2. **ExpressionsOpen:** GER/CEP expressions begin, cohesion calculated (informational only). Requires governance proposal asserting ≥500 unique XP-holders.
3. **SupremacyActive:** Supremacy challenges activate. Requires governance proposal asserting ≥50 qualified GER expressors.
4. **FullyOperational:** GER/CEP observation can trigger. Requires governance proposal asserting ≥200 qualified GER expressors.

Expression aging is paused during `Genesis` and `ExpressionsOpen` phases (before observation is possible). This is implemented by treating `frozen_since` as set for all dimensions during these phases.

**Why governance-driven transitions instead of automatic:** Computing "unique XP-holders system-wide" requires iterating the entire experience contract state — impossible in a single transaction. Governance proposals with evidence are transparent and auditable. The community verifies the claim before voting to advance.

### 7.3 Genesis GER Dimensions

When the population reaches 500 XP-holders, the system ships with suggested GER dimensions derived from the Sovereign Choice Axiom. These are added via governance proposal and are all modifiable through the amendment process:

- `anonymous_participation` — "Does anonymous participation protect freedom of choice?"
- `consent_requirement` — "Must consent be obtained before binding someone to rules?"
- `exit_freedom` — "Must exit from any community always be possible?"
- `fork_right` — "Must the right to fork always be preserved?"

These are starting points. Communities can add, modify, or remove dimensions through the CEP track.

---

## 8. Gas Considerations

- **Cohesion:** O(1) per expression change via incremental accumulators. No iteration. Gas cost is constant regardless of population size.
- **Qualification checks:** Require 1-3 cross-contract queries (~50-100K gas each). Cached in `QUALIFICATION_CACHE` with TTL (default: 1 epoch). Cache hit = 1 storage read (~5K gas).
- **SnapshotEpoch:** Reads cached cohesion from accumulator (O(1)), creates one snapshot entry. Constant gas.
- **XP weight staleness:** Subject-track snapshots XP at expression time. Users who gain significant XP are naturally incentivized to re-express (captures new weight). No periodic reconciliation needed.
- **Lazy expiry cleanup:** Expired expressions are cleaned up when encountered during Express (subtract from accumulator), not via batch scan. At most 1 stale entry cleaned per transaction.

---

## 9. Events

```
expression_updated     { track, dimension, account, value }
expression_renewed     { track, dimension, account }
expression_withdrawn   { track, dimension, account }
observation_started    { track, dimension, start_epoch, window }
epoch_snapshot         { track, dimension, epoch, cohesion, qualified }
observation_failed     { track, dimension, qualifying_epochs, required }
reconfirmation_started { track, dimension, window_end_epoch }
amendment_enacted      { track, dimension, contract, parameter, value }
amendment_failed       { track, dimension, reason }
moratorium_started     { track, dimension, until_epoch, consecutive_failures }
challenge_filed        { challenge_id, track, dimension, flagger }
challenge_panel        { challenge_id, panel_members }
challenge_resolved     { challenge_id, result: "blocked" | "allowed" }
```

---

## 10. Open Items (for implementation)

1. **Active-user interaction metric** — What counts as "interaction" for the reconfirmation active-user check? Proposal: any execute message to the expression contract counts. Simple, on-chain verifiable.
2. **Contested dimension resolution** — What does structured deliberation produce after 3 consecutive failures? Timeline, participants, outcome states.
3. **Chain-randomness for panels** — Exact mechanism for deriving randomness from future block hash. Must use multi-party seeds (not just block hash alone) to resist PoA validator manipulation. Can reuse pattern from auditing contract.
4. **Input validation** — Dimension names: max 64 chars, alphanumeric + hyphens only. Subject tags in Track: validate against subject contract constraints. Reject empty strings, control characters, excessively long inputs.
5. **RegisterParameterMapping whitelist** — Governance must maintain a whitelist of valid `(contract, parameter)` pairs that expression amendments can target.
6. ~~Moratorium counter reset~~ — RESOLVED: added to `FinalizeAmendment` step 4.
7. **Frivolous flag decay** — Counter decrements by 1 every 26 epochs with no frivolous flags. Stored in `FRIVOLOUS_FLAGS`.
8. ~~Query pagination~~ — RESOLVED: added to `ExpressionsByAccount` query definition.
9. **RetireDimension guards** — Must reject if observation is active, cancel pending challenges, mark dimension so `Express` rejects new expressions.
10. **Experience contract change** — Add `DistinctSourceTypes { user }` query with `SOURCE_TYPES_BY_USER` storage index for efficient qualification checking.
11. ~~Observation cleanup after success~~ — RESOLVED: `FinalizeAmendment` deletes ObservationState on success.
12. **Stalled observation timeout** — Add `CancelObservation { track, dimension }` callable by governance if `SnapshotEpoch` hasn't been called for 3+ epochs. Unfreezes aging, resets observation state. Prevents permanent freeze from abandoned cranks.
13. **SnapshotEpoch crank semantics** — If a snapshot is missed for epoch N and the crank is called in epoch N+2, record epochs N and N+1 as non-qualifying (missed). This prevents observation from stretching indefinitely. Missed epochs reduce the qualifying ratio.
14. **XP concentration acknowledgment** — For Subject-track: document that weighted cohesion reflects XP distribution. A single high-XP participant can dominate the signal. The governance vote (bridge step) is the safeguard, not the expression layer. Minimum expressor count (`subject_min_expressors`, default 3) prevents single-person observations.
15. **Supremacy panel pool fallback** — If fewer qualified GER expressors exist outside the subject than the required panel size, the challenge cannot proceed. Store the challenge as `Gathering` indefinitely until the pool grows. Document this as a known limitation during early bootstrap.
16. **Qualification cache invalidation on quarantine** — If XP quarantine (brainstorm 012) is implemented, quarantine events should force-clear `QUALIFICATION_CACHE` entries for the affected account.

---

## Critic Chain Results

**4 rounds, 55 total issues (2 FATAL + 22 HIGH + 31 MODERATE). All FATAL and HIGH resolved.**

| Round | FATAL | HIGH | MOD | Key Fixes |
|-------|-------|------|-----|-----------|
| 1 | 2 | 7 | 10 | Incremental O(1) accumulators, XP weight snapshot, Track storage keys, freeze mechanism, parameter mapping function, governance contract changes, bootstrap phases, subject-track bridge |
| 2 | 0 | 6 | 8 | Qualification queries (RefreshQualification + DistinctSourceTypes), u128 weighted accumulators, qualified_count storage, CleanupExpired crank, cumulative freeze duration, safety-first auto_execute |
| 3 | 0 | 3 | 7 | SourceType table corrected, subject config params in storage/InstantiateMsg, reconfirmation interaction tracking storage |
| 4 | 0 | 6 | 6 | Cross-subject governance proposal mode, ObservationState cleanup on success, consecutive_failures reset, query pagination, subject qualified_count denominator |

### Key Architectural Pivots

1. **Full iteration → incremental accumulators** (Round 1): Cohesion recalculation was O(N) per expression — breaks at ~30 users on Subject track due to cross-contract XP queries. Replaced with O(1) running statistics (sum, sum_sq, count).
2. **Live XP → snapshotted weights** (Round 1): Subject-track cohesion used live XP balances that shift from unrelated activity. Now snapshots XP at expression time. Re-expressing updates the weight.
3. **Auto-execute from day one → safety-first** (Round 2): All expression amendments go through governance vote until community enables auto-execute. Prevents a cohesion bug from causing unauthorized parameter changes.
4. **Lazy cleanup → permissionless CleanupExpired crank** (Round 2): Expired expressions only cleaned on self-access caused unbounded accumulator drift. Added CleanupExpired for batch cleanup by any caller.
5. **frozen_since cleared on unfreeze → cumulative total_frozen_epochs** (Round 2): Clearing frozen_since on unfreeze lost the freeze duration, causing instant mass expiry. Now accumulates frozen time across observation cycles.
6. **Subject-scoped governance → cross-subject proposal mode** (Round 4): Governance contract is subject-scoped; GER/CEP proposals need cross-subject equal-voice voting. Added ProposalMode::Expression.

### Remaining MODERATE Issues (31 items — for implementation phase)

1. Panel randomness exploitable by PoA validators (use multi-party seeds)
2. SnapshotEpoch timing within epoch can be gamed
3. Subject track tags lack validation in expression contract
4. Supremacy challenge panel pool may be empty during bootstrap
5. Qualification cache TTL gap during XP quarantine
6. No mechanism to cancel stalled observation (needs governance escape hatch)
7. Frivolous flag counter needs decay mechanism
8. RetireDimension needs lifecycle guards
9. Binary dimensions require ~99.75% unanimity for 9000 cohesion (intentional but should document)
10. Reconfirmation active-user check is gameable (30% threshold trivially met/blocked)
11. Division by zero when count=0 or sum_weight=0 (guard in implementation)
12. Frivolous flag records accumulate in storage without cleanup
13. XP concentration makes Subject-track expression cosmetic for whale-dominated subjects
14. ObservationState snapshot Vec grows up to 20 entries (bounded, acceptable)
15. Experience contract needs DistinctSourceTypes query and storage index
