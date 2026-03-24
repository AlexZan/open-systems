# Brainstorm 015: Certification Contract Design

**Date:** 2026-03-23
**Status:** Brainstorm — critic-chain validated (6 rounds, 59 issues, all FATAL/HIGH resolved)
**Relates to:** Brainstorm 011 (Constitutional Governance Model), Brainstorm 012 (Certification Anatomy), Expression Contract Spec
**Goal:** Design the on-chain certification contract — the registry of governance standards that entities adopt to declare their commitments.

---

## The Role of Certifications

Certifications are **shared, reusable governance standards** created by the ecosystem. They are NOT custom per-entity — they are templates that carry meaning through standardization and adoption. Like ISO 9001, Fair Trade, B Corp: they exist independently of any entity, entities adopt them voluntarily, and the track record of both the certification and its adopters is publicly visible.

The certification contract is a **registry** — anyone can publish a certification, anyone can adopt one. The chain stores the enforceable parameters and tracks adherence. The full human-readable text lives in the vault.

---

## Design Principles

1. **Cert = published standard.** Created once, adopted many times. Like a crate on crates.io.
2. **Adoption = entity's commitment.** Links an address to a certification version. Tracked on-chain.
3. **Entity = any address.** No separate entity registry. A person, multisig, or governance contract can adopt.
4. **Parameters are typed key-value pairs.** Flexible enough for any domain, structured enough for machine enforcement.
5. **Overrides only stricter.** Entities can exceed a certification's requirements but never weaken them.
6. **Track record per adoption.** Violations tracked per (entity, certification) pair, not lumped per entity.
7. **Version-pinned.** Entities adopt a specific version. No automatic upgrades. Active re-adoption required for new versions.
8. **KN is advisory.** Knowledge Network detects conflicts and provides evidence but never blocks adoption.

---

## Contract: Certification Registry

### State

```rust
/// A published certification
pub struct Certification {
    pub id: u64,
    pub creator: Addr,
    pub name: String,              // max 128 chars, e.g. "Fair Housing Standards"
    pub version: u32,              // numeric version (1, 2, 3...) — simple integer comparison
    pub content_hash: String,      // SHA-256 of full document (stored in vault)
    pub parameters: Vec<ParameterDef>,
    pub dimensions: Vec<DimensionDef>,
    pub requires: Vec<Requirement>, // parent certs required for adoption
    pub conflicts_with: Vec<u64>,   // cert IDs that can't coexist with this one
    pub previous_version: Option<u64>, // cert ID of the version this supersedes
    pub is_chain_level: bool,     // true = only governance can adopt; false = anyone can adopt
    // Validation: at publish time, reject certs with GER/CEP dimensions unless is_chain_level=true
    pub created_at: u64,
    pub status: CertStatus,
}

pub enum CertStatus {
    Active,
    Deprecated,    // creator marked it as superseded; existing adoptions still valid
}

/// A requirement: must hold cert X at version >= Y
pub struct Requirement {
    pub cert_id: u64,
    pub min_version: u32,     // numeric version (simple integer comparison)
}

/// A parameter definition within a certification
pub struct ParameterDef {
    pub key: String,                  // machine-readable key, e.g. "exit_notice_period"
    pub display_name: String,         // human-readable, e.g. "Exit Notice Period"
    pub value: ParameterValue,        // default value
    pub param_type: ParameterType,    // what kind of enforcement
    pub override_allowed: bool,       // can adopters customize?
    pub override_direction: Option<OverrideDirection>, // if overridable, which way?
    pub notice_period: Option<u64>,   // seconds before override reduction takes effect (None = 30 days default)
    pub weaken_is_lower: Option<bool>, // for Either direction: true = lower values are weaker, false = higher values are weaker
    pub description_hash: String,     // vault hash of human explanation
}

pub enum ParameterValue {
    Uint(u64),                // thresholds, gates, timeframes (seconds)
    Bool(bool),               // flags
    Text(String),             // enums, labels
    TextList(Vec<String>),    // scope lists (e.g. ["events", "garden", "meals"])
}

pub enum ParameterType {
    /// Machine-enforced: other contracts query this parameter and enforce it.
    /// The certification contract exposes `EffectiveParameters` query.
    /// Consuming contracts (child governance, projects, forum) check effective
    /// parameter values via cross-contract query at action time.
    /// Example: child governance queries "community_can_govern" before allowing proposals.
    /// Example: a makerspace app queries "laser_cutter_xp_gate" before granting access.
    MachineEnforced,
    /// Human-audited: relies on reporting + audit for compliance.
    /// Parameters like "insurance_required" can't be checked on-chain.
    HumanAudited,
}

pub enum OverrideDirection {
    OnlyHigher,               // entity can only increase (stricter)
    OnlyLower,                // entity can only decrease (lower barrier)
    Either,                   // entity can go either way
}

/// An expression dimension introduced by this certification
pub struct DimensionDef {
    pub name: String,              // dimension name for the expression contract
    pub dim_type: DimensionType,   // Gradient | Binary
    pub track: DimensionTrack,     // which governance track
    pub description_hash: String,  // vault hash of what this dimension means
    // ParameterMapping for the expression contract (what on-chain parameter this dimension controls)
    pub parameter_mapping: ParameterMapping,
}

/// What on-chain parameter an expression dimension maps to
pub struct ParameterMapping {
    pub contract: String,          // target contract address
    pub parameter: String,         // parameter key on target contract
    pub low_value: String,         // value when mean anchors at 0
    pub high_value: String,        // value when mean anchors at 10000
    pub enactment_target: EnactmentTarget,
}

pub enum EnactmentTarget {
    GovernanceAutoExecute,         // GER/CEP: auto-enact after observation
    GovernanceProposal,            // Subject: requires governance vote
}

pub enum DimensionType {
    Gradient,    // 0-10000 continuous
    Binary,      // 0 or 10000 only
}

pub enum DimensionTrack {
    Subject { tag: String },  // registered at subject level (tag must match an existing subject)
    GER,                      // registered at GER level (only valid for chain-level certs)
    CEP,                      // registered at CEP level (only valid for chain-level certs)
}
```

### Storage

```rust
pub const CERTIFICATIONS: Map<u64, Certification> = Map::new("certs");
pub const CERT_COUNTER: Item<u64> = Item::new("cert_ctr");
// NOTE: CERT_COUNTER initialized to 2 at instantiation. IDs 0 and 1 are reserved
// as sentinels for CEP and GER chain-level requirements (see "Chain-Level Requirement Checking").

// Indexes
pub const CERTS_BY_CREATOR: Map<(&Addr, u64), ()> = Map::new("certs_by_creator");
pub const CERTS_BY_NAME: Map<(&str, u64), ()> = Map::new("certs_by_name");

// Adoptions
pub const ADOPTIONS: Map<(&Addr, u64), Adoption> = Map::new("adoptions");
pub const ADOPTIONS_BY_CERT: Map<(u64, &Addr), ()> = Map::new("adopt_by_cert");
pub const ADOPTION_COUNT: Map<u64, u32> = Map::new("adopt_count");

// Admin
pub const ADMIN: Item<Option<Addr>> = Item::new("admin");
pub const AUTHORIZED_CALLERS: Map<&Addr, ()> = Map::new("authorized_callers");
```

### Messages

```rust
pub enum ExecuteMsg {
    // --- Publishing ---

    /// Publish a new certification (requires XP stake — anti-spam)
    /// Hard limits: max 20 parameters, max 5 dimensions, max 10 requirements, max 10 conflicts
    PublishCertification {
        name: String,
        version: u32,
        content_hash: String,
        parameters: Vec<ParameterDef>,     // max 20
        dimensions: Vec<DimensionDef>,     // max 5
        requires: Vec<Requirement>,        // max 10
        conflicts_with: Vec<u64>,          // max 10
        previous_version: Option<u64>,
        publish_subject: String,           // subject for XP staking (anti-spam)
    },

    /// Deprecate a certification (creator only)
    DeprecateCertification { cert_id: u64 },

    // --- Adoption ---

    /// Adopt a certification (any address)
    AdoptCertification {
        cert_id: u64,
        parameter_overrides: Vec<ParameterOverride>,
    },

    /// Drop (un-adopt) a certification
    DropCertification { cert_id: u64 },

    /// Update parameter overrides on an existing adoption.
    /// Rules:
    /// Override update rules:
    /// - OnlyHigher/OnlyLower: can only move FURTHER from default, never back toward it.
    ///   To reduce toward default: requires notice_period (cert param, or 30 days default).
    /// - Either: any direction change that weakens the parameter (moves toward a value less
    ///   favorable for community members) requires notice_period. Changes that strengthen
    ///   are immediate. "Weaken" is defined per parameter by the cert creator.
    /// - Removing an override entirely = reducing to default. Same notice rules apply.
    UpdateOverrides {
        cert_id: u64,
        parameter_overrides: Vec<ParameterOverride>,
    },

    /// Apply pending override changes after notice period expires (permissionless crank)
    ApplyPendingOverrides { entity: String, cert_id: u64 },

    // --- Enforcement ---

    /// Record a violation against an adoption (authorized callers only — auditing contract)
    RecordViolation {
        entity: String,
        cert_id: u64,
        violation_hash: String,  // evidence stored in vault
        severity: ViolationSeverity,
    },

    /// Advance enforcement ladder (authorized callers only — auditing/governance)
    AdvanceEnforcement {
        entity: String,
        cert_id: u64,
        new_step: EnforcementStep,
    },

    // --- Admin ---
    AdminRegisterCaller { contract_addr: String },
    DisableAdmin {},
}

pub struct ParameterOverride {
    pub key: String,
    pub value: ParameterValue,
}

pub enum ViolationSeverity {
    Minor,
    Major,
    Critical,
}

pub enum EnforcementStep {
    Clean,             // no enforcement actions taken (initial state)
    Warning,           // 1st confirmed violation
    Probation,         // 2nd confirmed violation
    Decertification,   // 3rd confirmed violation
}

pub enum QueryMsg {
    /// Get a certification by ID
    Certification { id: u64 },

    /// List certifications by creator
    CertificationsByCreator {
        creator: String,
        start_after: Option<u64>,
        limit: Option<u32>,
    },

    /// Search certifications by name
    CertificationsByName {
        name: String,
        start_after: Option<u64>,
        limit: Option<u32>,
    },

    /// Get an entity's adoption of a specific cert
    Adoption { entity: String, cert_id: u64 },

    /// List all adoptions for an entity
    AdoptionsByEntity {
        entity: String,
        start_after: Option<u64>,
        limit: Option<u32>,
    },

    /// List all adopters of a certification
    AdoptersByCert {
        cert_id: u64,
        start_after: Option<String>,
        limit: Option<u32>,
    },

    /// Get adoption count for a certification
    AdoptionCount { cert_id: u64 },

    /// Check if an entity meets all requirements for a certification
    CheckRequirements { entity: String, cert_id: u64 },

    /// Check for conflicts between an entity's current adoptions and a new cert
    CheckConflicts { entity: String, cert_id: u64 },

    /// Get the effective parameters for an adoption (base + overrides)
    EffectiveParameters { entity: String, cert_id: u64 },

    /// Contract config
    Config {},
}
```

---

## Anti-Spam: Publishing Cost

**Problem:** Free accounts + permissionless publishing = unlimited spam certifications.

**Solution:** Publishing a certification requires staking XP in the specified subject:

- **Stake amount:** Configurable (default: 10 XP). Must have XP in `publish_subject`.
- **Stake is time-locked, not adoption-gated.** The stake is locked for 26 epochs (same as expression TTL). After 26 epochs, it's returned regardless of adoption count. This prevents the sybil bypass (create 3 fake accounts → adopt → recover stake) because creating accounts with enough XP to meaningfully adopt takes real work, and the time-lock ensures the creator has skin in the game during the cert's early life.
- **Stake burned on deprecation.** If the cert is deprecated before the time-lock expires, the stake is burned.
- **No stake for governance-published certs:** Chain-level certifications published via governance proposal don't require staking (the governance vote IS the quality gate).

This anchors publishing cost to something scarce (verified work in a domain), consistent with the contribution staking pattern in the projects contract.

## Version Rules

Versions are **numeric integers** (1, 2, 3, ...). No semver, no dots, no strings.

- Comparison is simple: `version >= min_version` uses integer `>=`
- A new version of a cert must have `version > previous cert's version`
- Validated at publish time — the contract rejects non-sequential versions
- Human-readable version descriptions go in the content document (vault)

---

## Adoption Logic

### Adopt Flow

```
1. Validate cert exists and is Active (not Deprecated)
1b. Check decertification cooldown: if entity was previously decertified for this cert,
    verify cooldown has expired (26 epochs). Prevents immediate re-adoption after bad behavior.
2. Check requirements: for each cert in requires[], verify entity has an active adoption
   of that cert at >= min_version
2b. Check adoption limit: entity cannot hold more than 20 active certifications
    (prevents unbounded gas during bidirectional conflict check)
3. Check conflicts BIDIRECTIONALLY:
   a. For each cert in NEW cert's conflicts_with[], verify entity does NOT hold it
   b. For each of entity's EXISTING adoptions, check if that cert's conflicts_with[]
      includes the new cert's ID
   This prevents holding conflicting certs by exploiting adoption order
4. Validate parameter overrides:
   a. Each override key must exist in the cert's parameters
   b. Each override must be for a parameter with override_allowed = true
   c. Each override must comply with override_direction:
      - OnlyHigher: override value must be >= default (for Uint), true >= false (for Bool)
      - OnlyLower: override value must be <= default
      - Either: any value accepted
5. Store adoption: (entity, cert_id) → Adoption { ... }
6. Increment adoption count
7. If cert has dimensions: register them in the expression contract.
   With max 5 dimensions per cert and ~200K gas per SubMsg, this fits
   within a single transaction (~1M gas for dimension registration).
   Each dimension's DimensionDef includes the full ParameterMapping
   needed by the expression contract's RegisterDimension message.
8. Emit event: certification_adopted { entity, cert_id, cert_name, version }
```

### Drop Flow

```
1. Verify adoption exists and status is Active
2. Check if any OTHER adopted certs require this one
   (can't drop a cert that's a prerequisite for another active adoption)
3. Check enforcement: if entity is under Probation or Warning, dropping is still allowed
   (you can always exit — Rule of Freedom)
   But: the drop is recorded in track record (visible as "dropped while under enforcement")
4. Set adoption status to Dropped (NOT deleted — track record preserved)
5. Decrement adoption count
6. Decrement dimension reference counters (retire if counter reaches 0)
7. Emit event: certification_dropped { entity, cert_id, was_under_enforcement }

**Re-adoption after drop:** Allowed immediately (no cooldown, unlike decertification).
Creates a new adoption generation. The old Dropped record is preserved.
Violation storage keys use `(entity, cert_id, violation_index)` — the violation_count
on the new adoption starts at 0, but old violation records remain accessible for
track record queries. The key separation (index-based) prevents collisions.
```

### Override Validation

For `OnlyHigher` with `Uint`:
```
override_value >= default_value  → allowed
override_value < default_value   → rejected: "Override must be >= {default}"
```

For `OnlyHigher` with `Bool`:
```
default = false, override = true  → allowed (stricter)
default = true, override = false  → rejected
default = true, override = true   → no-op (same as default)
default = false, override = false → no-op
```

For `TextList` (scope lists like `["events", "garden"]`):
```
OnlyHigher = can only ADD items (expand scope, which is more permissive for the community)
OnlyLower = can only REMOVE items (restrict scope)
```

This is a semantic question — "higher" for a scope list means "more delegated to community" which is the OPPOSITE of "stricter." The cert creator must define the semantics per parameter. A scope delegation list with `OnlyHigher` means the entity can delegate MORE but never less than what the cert specifies.

---

## Track Record

Every adoption accumulates a track record:

```rust
pub struct Adoption {
    pub entity: Addr,
    pub cert_id: u64,
    pub version: u32,              // numeric version (see Version Rules below)
    pub adopted_at: u64,
    pub parameter_overrides: Vec<ParameterOverride>,
    pub enforcement_step: EnforcementStep,
    pub last_enforcement_at: u64,  // timestamp of last enforcement action (for 2-epoch cooldown)
    pub violation_count: u32,
    pub status: AdoptionStatus,
}

pub enum AdoptionStatus {
    Active,
    Dropped,           // voluntarily dropped by entity
    Decertified,       // removed via enforcement ladder
}

// Cooldown tracking: prevents immediate re-adoption after decertification
pub const DECERT_COOLDOWNS: Map<(&Addr, u64), u64> = Map::new("decert_cool");

// Pending override changes (for notice-period enforcement)
pub const PENDING_OVERRIDES: Map<(&Addr, u64), Vec<PendingOverride>> = Map::new("pend_over");
pub struct PendingOverride {
    pub key: String,
    pub new_value: ParameterValue,
    pub effective_at: u64,           // block time when switch happens
}
// EffectiveParameters query returns old values until effective_at, new values after.
// A permissionless crank `ApplyPendingOverrides { entity, cert_id }` finalizes the switch.


// Violations stored separately — NOT inline in Adoption (gas safety)
// Keyed by (entity, cert_id, violation_index)
pub const VIOLATIONS: Map<(&Addr, u64, u32), ViolationRecord> = Map::new("violations");
pub const VIOLATION_COUNTER: Map<(&Addr, u64), u32> = Map::new("viol_ctr");
pub const ENFORCEMENT_HISTORY: Map<(&Addr, u64, u32), EnforcementEvent> = Map::new("enforce_hist");
pub const ENFORCEMENT_COUNTER: Map<(&Addr, u64), u32> = Map::new("enforce_ctr");

pub struct ViolationRecord {
    pub timestamp: u64,
    pub violation_hash: String,    // evidence in vault
    pub severity: ViolationSeverity,
    pub confirmed_by: u64,         // audit case ID that confirmed this
}

pub struct EnforcementEvent {
    pub timestamp: u64,
    pub step: EnforcementStep,
    pub reason_hash: String,       // vault hash of reasoning
}
```

The enforcement ladder from brainstorm 012:
1. **Warning** (1st confirmed violation) — public record, no mechanical effect
2. **Probation** (2nd confirmed violation) — visible flag, entity loses eligibility to serve on auditor panels
3. **Decertification** (3rd confirmed violation) — entity loses the certification, exit terms enforced

Each step requires an **audit-confirmed violation** and a **2-epoch minimum cooldown** between steps. The auditing contract calls `RecordViolation` and `AdvanceEnforcement` through authorized caller registration.

**Decertification side effects:** When `AdvanceEnforcement` moves to `Decertification`:
1. Adoption status set to `Decertified` (not deleted — track record preserved)
2. Adoption excluded from all active queries (`AdoptionsByEntity`, `AdoptersByCert` filter by status)
3. Adoption count decremented
4. Expression dimension ref counters decremented (retired if counter reaches 0)
5. Entity marked with `decertification_cooldown` — cannot re-adopt the same cert for 26 epochs
6. Event emitted: `entity_decertified { entity, cert_id, violations }`

---

## Interaction with Expression Contract

### The Dimension Scoping Problem

Expression dimensions are **global per track** — a dimension named `"safety_strictness"` on `Track::Subject { tag: "makerspaces" }` is shared by ALL participants in that subject. But certifications are adopted by individual entities. When Entity A adopts a cert with dimensions, the dimensions become available to everyone in that subject, not just Entity A's members.

### Resolution: Reference-Counted Dimensions

Dimensions introduced by certifications use **reference counting**:

1. When the FIRST entity in a subject adopts a cert with dimensions, the dimensions are registered in the expression contract (via SubMsg). A reference counter is stored: `DIMENSION_REFS: Map<(&str, &str), u32>` keyed by (track_key, dimension_name).
2. When subsequent entities adopt the same cert, the dimension already exists. The reference counter increments.
3. When an entity drops the cert, the reference counter decrements.
4. When the counter reaches 0, the dimension is retired (no new expressions, existing data preserved).

This means dimensions are global (anyone in the subject can express), but their lifecycle is tied to whether ANY entity in that subject holds the cert that defines them. This is correct: "safety_strictness" is a community-wide question, not an entity-private one. The cert defines WHAT the community debates; the expression system handles HOW.

```rust
// In certification contract storage
pub const DIMENSION_REFS: Map<(&str, &str), u32> = Map::new("dim_refs");
```

Registration is **idempotent** — if the dimension already exists, the SubMsg is skipped and only the ref counter increments.

**Cross-subject adoption:** An entity in "gardening" could adopt "Maker Space Safety" (which has dimensions in "makerspaces"), inflating the ref counter. This is acceptable: the dimension only retires when ALL adopters drop, and irrelevant adoptions waste the entity's 20-adoption limit. The ref counter accurately tracks "how many entities have a stake in this dimension existing." Self-correcting via the adoption limit.

**Authorization:** The expression contract spec currently gates `RegisterDimension` and `RetireDimension` as "governance only." This must be relaxed to accept authorized callers (same as other contracts). **Required expression contract spec change:** `RegisterDimension` and `RetireDimension` should accept either governance OR authorized callers. The certification contract is registered as an authorized caller on the expression contract (via `AdminRegisterCaller`). This is a deployment step — same pattern as projects→experience caller registration.

For chain-level certs (CEP/GER): dimensions are registered at GER/CEP track level. Chain-level certs are marked with `is_chain_level: true` and can only be adopted via governance (the adopt message checks `AUTHORIZED_CALLERS` if the cert is chain-level).

---

## Interaction with Nested Governance

When an entity (parent governance contract) delegates scope to a community (child governance contract):

```
Entity adopts "Community Land Access v1"
  → Parameters include: community_can_govern: ["garden", "events", "meals"]
  → Parameters include: entity_retains: ["structures", "land_sale", "liability"]

Community governance contract (child):
  → On any proposal, queries parent: "Is this within my scope?"
  → Parent returns: intersection of all adopted certs' delegated scopes
  → If proposal touches "structures" → rejected (outside scope)
  → If proposal touches "garden" → allowed (within scope)
```

The child **pulls** the scope from the parent at proposal-validation time (not cached). This ensures the scope is always current — if the parent drops a cert or modifies overrides, the child's scope changes immediately.

**Deadlock escape** (from 012): If the intersection of all parent scopes blocks ALL proposals for 3 consecutive epochs (verified by multiple distinct proposers), the parent governance regains authority to un-adopt certifications without community vote.

---

## What CEP and GER Are NOT

CEP and GER are **not certifications in this contract**. They are chain-level parameters governed by the expression contract's Track 2 (GER) and Track 3 (CEP) amendment flows.

### Chain-Level Requirement Checking

Domain certifications can declare requirements on chain-level governance:

```rust
// Reserved cert IDs for chain-level requirements
const CEP_SENTINEL: u64 = 0;  // "requires CEP compatibility"
const GER_SENTINEL: u64 = 1;  // "requires GER compatibility"

// When CheckRequirements encounters a sentinel ID:
// 1. Query the expression contract for the current bootstrap phase
// 2. If FullyOperational: CEP/GER requirements are satisfied
// 3. If not yet FullyOperational: requirement check returns a warning
//    (adoption still proceeds — the cert was created under the
//    assumption CEP exists, but the chain hasn't matured yet)
```

The version number in the requirement (e.g., `min_version: 1`) maps to the chain's governance epoch. At genesis, CEP version = 1. CEP track amendments increment it.

**Required expression contract change:** Add `ChainGovernanceVersion { track }` query that returns `{ version: u32 }`. Backed by `CHAIN_GOVERNANCE_VERSION: Map<&str, u32>` storage, incremented on each successful `FinalizeAmendment`. This is a small addition to the expression contract spec (Open Item for implementation).

This is a **simple interface**: the certification contract asks the expression contract "what version is CEP at?" and compares it to the requirement. No special case logic beyond the sentinel check.

**Why not make CEP a certification?** Circular dependency: a certification that requires CEP can't exist if CEP is itself a certification requiring adoption. CEP is the substrate, not a package on the substrate.

---

## Example: Maker Space

```
Certification: "Maker Space Safety v2"
  Creator: makerspace_association_addr
  Parameters:
    - 3d_printer_xp_gate: Uint(5), OnlyHigher, MachineEnforced
    - laser_cutter_xp_gate: Uint(15), OnlyHigher, MachineEnforced
    - cnc_mill_xp_gate: Uint(30), OnlyHigher, MachineEnforced
    - insurance_required: Bool(true), no override, HumanAudited
    - max_occupancy: Uint(20), OnlyLower, HumanAudited
  Dimensions:
    - "safety_strictness": Gradient, Subject track
  Requires: none
  Conflicts: none

Entity "Downtown Makers" adopts with overrides:
    - laser_cutter_xp_gate: 20 (stricter than 15 ✓)
    - max_occupancy: 15 (lower than 20 ✓)

Entity "Loose Workshop" tries to adopt with:
    - 3d_printer_xp_gate: 2 (less than 5 ✗ — rejected, OnlyHigher)
```

## Example: Farm Community

```
Certification: "Community Land Access v1"
  Parameters:
    - exit_notice_days: Uint(60), OnlyHigher, MachineEnforced
    - rule_change_notice_days: Uint(30), OnlyHigher, MachineEnforced
    - community_can_govern: TextList(["garden", "events", "meals"]), OnlyHigher, MachineEnforced
    - entity_retains: TextList(["structures", "land_sale", "liability"]), no override, MachineEnforced
    - stability_guarantee_days: Uint(180), OnlyHigher, MachineEnforced
  Requires:
    - CEP_SENTINEL, min_version: 1

Farm owner adopts with overrides:
    - exit_notice_days: 90 (stricter ✓)
    - community_can_govern: ["garden", "events", "meals", "workshops"] (expanded ✓)
```

---

## Open Questions

1. ~~Version comparison~~ — **RESOLVED:** Numeric integers (1, 2, 3). Simple `>=` comparison.

2. **Certification update notification.** When v2 is published, should v1 adopters be notified on-chain (event)? Or purely KN/off-chain concern? Leaning: emit event, KN supplements.

3. **Cross-entity certification recognition.** "CNC certified at MakerSpace A → recognized at MakerSpace B." A relationship between adoptions, not certifications. Probably a separate "recognition" declaration or a cert parameter.

4. ~~Maximum parameters per cert~~ — **RESOLVED:** Hard limits: 20 parameters, 5 dimensions, 10 requirements, 10 conflicts.

5. **Dimension lifecycle on drop.** When a cert is dropped, expression dimensions are "retired." Existing expressions preserved (read-only) or cleaned up? Leaning: preserved, same as the expression contract's retire mechanism.

6. **UpdateOverrides notification.** Should emit events. Scope-affecting parameter changes may need notice periods matching the cert's amendment rules.

7. **Auditing integration.** The existing auditing contract is forum-post-scoped. Certification violation reports need either a new case type or separate flow. Deferred to implementation.

8. **Missing queries (for implementation):**
   - `PendingOverrides { entity, cert_id }` — show pending override changes and effective dates
   - `AdoptionHistory { entity, cert_id }` — show all adoption generations (active, dropped, decertified). Requires storage key change: `ADOPTIONS: Map<(&Addr, u64, u32), Adoption>` with generation counter, or a separate `HISTORICAL_ADOPTIONS` map.

9. **Version lineage validation.** Should `previous_version` require same creator? Or allow forkable certification lineages (anyone can publish a "v3" claiming to supersede someone else's "v2")? Leaning: validate same creator for lineage integrity.

10. **EffectiveParameters during notice period.** The query must check BOTH `Adoption.parameter_overrides` AND `PENDING_OVERRIDES`, merging based on `block.time >= effective_at`. Document this dual-source behavior explicitly for implementors.

---

## Critic Chain Results

**6 rounds, 59 total issues (4 FATAL + 23 HIGH + 32 MODERATE). All FATAL and HIGH resolved.**

| Round | FATAL | HIGH | MOD | Key Fixes |
|-------|-------|------|-----|-----------|
| 1 | 1 | 5 | 7 | ParameterMapping in DimensionDef, separate violation storage, bidirectional conflicts, numeric versions, hard limits, XP publish staking, CEP sentinel interface |
| 2 | 1 | 5 | 6 | Reference-counted dimensions, MachineEnforced docs, decertification cleanup, time-locked stake, re-adoption cooldown, UpdateOverrides notice period |
| 3 | 0 | 4 | 5 | Expression contract auth change, pending overrides storage, EnforcementStep::Clean, Subject dimension tag, is_chain_level field |
| 4 | 2 | 6 | 5 | Sentinel ID reservation (counter starts at 2), Drop preserves status, ChainGovernanceVersion, violation counters, adoption limit (20), enforcement cooldown, Either direction rules |
| 5 | 0 | 3 | 5 | notice_period + weaken_is_lower fields, cross-subject ref counting, GER/CEP dimension publish validation |
| 6 | 0 | 0 | 4 | Converged |

### Key Architectural Decisions

1. **Reference-counted dimensions** — global per track, not per entity. Ref counter tracks adopters; dimension retires when all drop.
2. **Time-locked publish stake** — 26-epoch lock prevents sybil bypass (vs adoption-count-gated which was trivially bypassable)
3. **Numeric versions** — simple integer comparison, no semver complexity
4. **Adoption preserved on drop/decertification** — track record never destroyed, status field distinguishes active/dropped/decertified
5. **Bidirectional conflict checking** — both new cert's conflicts AND existing adoptions' conflicts checked
6. **Notice period for override weakening** — prevents bait-and-switch; strengthening is immediate
7. **20-adoption limit** — bounds gas for bidirectional conflict checking

### Remaining MODERATE Issues (for implementation)

1. Override ratchet semantics: relative to default or current value? Clarify.
2. `AdvanceEnforcement` message missing `reason_hash` field
3. `ViolationRecord.confirmed_by` depends on undesigned auditing integration
4. Pending overrides: duplicate key behavior (replace, not stack)
5. Version lineage: validate same creator for `previous_version` references
6. Deprecation stake burn creates perverse incentive (penalizes responsible early deprecation)
7. `ParameterMapping.contract` type: String vs Addr consistency
8. No existence validation for `conflicts_with` cert IDs at publish time

---

## References

- [Brainstorm 011: Constitutional Governance Model](011-constitutional-governance-model.md)
- [Brainstorm 012: Certification Anatomy & GER](012-certification-anatomy.md)
- [Decision 008: Constitutional Derived Principles](../decisions/008-constitutional-derived-principles.md)
- [Expression Contract Spec](../specs/expression-contract.md)
- [CEP v1](../../DATA-DUMP/Open%20Systems%20Shared/Open%20Community/Core%20Expression%20Protocol%20(CEP)%20v1.md)
- [Land Co-Ownership Certificate v1](../../DATA-DUMP/Open%20Systems%20Shared/Open%20Community/Land%20Co-Ownership%20Certificate%20v1.md)
