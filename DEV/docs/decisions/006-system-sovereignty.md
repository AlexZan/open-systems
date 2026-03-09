# Decision 006: System Sovereignty

**Date:** 2026-03-09
**Status:** Accepted

## Context

Open Systems aims to eliminate power hierarchies in collaborative development. We've built executable governance — proposals can change parameters, upgrade contracts, and transfer control. But the system still depends on external actors for critical operations:

- A developer compiles the chain binary
- A human runs the deployment script
- Build artifacts are trusted implicitly
- The chain's Go code can only be changed by someone with repo access

As long as any layer requires a privileged human, we haven't achieved decentralization — we've just moved the admin.

## Decision

Define **System Sovereignty** as the architectural milestone where the community can modify absolutely everything: all contracts, all parameters, the chain binary, the build pipeline, the deployment process, the constitution, and the governance logic itself. No human has special power at any layer.

## Architecture

Everything is a contribution to a project. The same review/audit/approve flow handles all changes:

```
Source Code (vault)
     |
Community Review (auditing, XP-weighted)
     |
Build Specification (declarative, vault-stored, governed)
     |
Reproducible Build (N independent builders compile, compare hashes)
     |
Artifact Verification (on-chain consensus — builders agree on output hash)
     |
Deployment Proposal (governance vote on verified artifact)
     |
Coordinated Rollout (validators/nodes adopt)
```

Every box is itself a governed component. The pipeline governs the pipeline.

### Required Components

1. **Build Spec Contract** — declarative build configurations stored on-chain/vault. Maps input hashes (source + dependencies) to expected output hash. Community-governed.

2. **Builder Registry** — XP-weighted set of build attestors. Like auditors but for compilation. Community adds/removes builders through governance. N-of-M agreement required.

3. **Artifact Verification** — builders independently compile from source, submit output hashes. When threshold builders agree, artifact is marked "verified." Hash stored on-chain.

4. **Deployment Orchestration** — governance proposal type that triggers coordinated upgrades. For contracts: `MigrateContract` (already implemented). For chain binary: Cosmos SDK `x/upgrade` module integration.

5. **Chain Binary Governance** — governance proposals that trigger `x/upgrade` software upgrade plans. Validators auto-halt at designated block height, switch to new binary.

### What We Already Have

| Component | Status |
|---|---|
| Executable governance proposals | Done |
| Contract migration via governance | Done |
| CosmWasm admin transferred to governance | Done |
| All contracts have migrate entry points | Done |
| Projects with contributions + review | Done |
| Auditing with commit-reveal voting | Done |
| Vault for content-addressed storage | Done |
| Experience-weighted voting | Done |

### What's Needed

| Component | Status |
|---|---|
| Build Spec contract | Done |
| Builder Registry contract | Done |
| Artifact Verification contract | Done |
| x/upgrade integration in Go code | Done (live tested via governance proposal) |
| Deterministic/reproducible build tooling | Not started |
| Deployment orchestration | Not started |

## Composability Principle

This architecture is not specific to Cosmos, Go, Rust, or any technology. A "build spec" is generic: it takes input hashes and produces output hashes. The same pipeline that builds a CosmWasm contract builds a Go binary, a JavaScript frontend, or a mobile app. The governance layer doesn't care what's being built — it cares that the community reviewed it, independent builders verified it, and the community voted to deploy it.

## The Transition

1. **Bootstrap** — admin wires contracts, creates subjects, grants seed XP (done)
2. **Admin Dissolution** — admin calls DisableAdmin on all contracts, CosmWasm admin transferred to governance (done — 2026-03-09)
3. **Contract Sovereignty** — community can upgrade all contracts, schedule chain upgrades (done — x/upgrade live tested)
4. **Build Sovereignty** — community governs the build pipeline itself (done — contracts deployed: build-spec, builder-registry, artifact-verify)
5. **System Sovereignty** — remaining: deterministic/reproducible build tooling, deployment orchestration, real builder nodes

## Consequences

- The system becomes fully self-governing and self-evolving
- No single point of failure or control at any layer
- Upgrades require community consensus at every step
- The same primitives (projects, contributions, auditing, governance) handle everything from forum posts to chain upgrades
