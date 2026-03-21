# Brainstorm 014: Git Governance — Community-Driven Code Management

**Date:** 2026-03-21
**Status:** Brainstorm — critic-chain validated (5 rounds, 48 issues, all FATAL/HIGH resolved)
**Relates to:** Decision 004 (Project-Level Governance First), Decision 006 (System Sovereignty), Brainstorm 006 (Incubator Ownership Model)
**Goal:** Define how git repositories integrate with the existing Projects/Contributions contracts so that Open Systems can manage its own development through community governance.

---

## The Problem

Open Systems has 10 smart contracts, a governance system, and an experience-weighted voting mechanism — but all of it was built by a single developer using admin powers. The system that's supposed to enable community-driven development can't yet manage its own development through community governance.

The missing piece: a bridge between git (where code lives) and the chain (where governance lives).

## What Already Exists

### On-Chain (Ready to Use)

| Component | What It Does |
|-----------|-------------|
| **Projects contract** | Register projects, submit contributions, owner accept/reject (incubation), community vote (released), failover |
| **Contributions** | `SubmitContribution { project_id, title, content_hash }` → Review → Accept/Reject → XP minted |
| **Auditing** | Commit-reveal blind voting for quality control |
| **Governance** | Executable proposals (upgrade contracts, change params, create subjects) |
| **Build Sovereignty** | Build specs, builder registry, artifact verification |
| **Experience** | Non-transferable, subject-scoped, earned from verified contributions |

### Off-Chain (Ready to Use)

| Component | What It Does |
|-----------|-------------|
| **Vault** | Content-addressed storage with relay network |
| **MCP Server** | 63 tools for chain interaction |
| **Web Explorer** | 9-tab dashboard for chain state visualization |
| **CLI library** | `lib/cli.py` wraps all chain interactions |

### The Gap

No way to say: "This PR on GitHub = this contribution on-chain." No way for a reviewer to vote on-chain when reviewing code. No way for the chain to know a PR was merged.

---

## Design Principles

1. **Git-agnostic.** Works with GitHub, Gitea, GitLab, bare repos. The chain doesn't know or care about the hosting platform — it cares about commit hashes and content hashes.

2. **Self-hosted content.** Consistent with the existing architecture: developers host repos, chain stores hashes only. The diff/PR content lives in the vault (or directly in the git host), not on-chain.

3. **Same flow for everything.** Decision 006 says: "Everything is a contribution to a project. The same review/audit/approve flow handles all changes." Code PRs use the same Projects contract as forum posts and build specs.

4. **Incubator model applies.** During incubation, the project owner (lead dev) accepts/rejects PRs directly. After release, the community votes. Same lifecycle as brainstorm 006.

5. **No new contracts needed.** The Projects contract already handles the contribution lifecycle. We need a bridge layer (off-chain tooling), not new on-chain logic.

6. **Developer experience matters.** If the workflow is painful, nobody will use it. The git integration should feel like a natural extension of git, not a bureaucratic layer.

---

## Architecture

### The Bridge

```
Developer                    Bridge                      Chain
─────────                    ──────                      ─────

git push + open PR    →    CLI/webhook detects PR   →   SubmitContribution {
                            computes diff hash            project_id,
                            stores diff in vault          title: "PR #42: Fix auth",
                                                          content_hash: diff_sha256
                                                        }

Review PR on GitHub   →    Reviewer runs CLI        →   VoteContribution {
 (or in explorer)          (or clicks in explorer)       contribution_id,
                                                          vote: Approve
                                                        }

PR approved on-chain  →    Bridge detects            →  Merge PR on git host
                            FinalizeContribution          (or notify to merge)
                            result = Accepted

XP minted to author   ←    Chain event               ←  experience.mint_internal
```

### What the Bridge Does

The bridge is a **thin translation layer** between git events and chain transactions. It can be:

1. **A CLI tool** (`os-git`) — developer runs commands manually
2. **A webhook service** — watches git host, acts automatically
3. **Both** — CLI for development, webhook for production

The bridge is NOT a smart contract. It's off-chain tooling that calls existing contracts.

### Content Hashing

When a PR is submitted, the bridge computes a content hash from the **exact commit range**, not from branch names:

```
base_commit = merge-base of PR branch and target branch (exact SHA)
head_commit = head of PR branch (exact SHA)

# Step 1: Generate raw diff (exclude binaries, exact commits)
raw_diff = git diff --no-renames --no-color --no-ext-diff base_commit..head_commit -- . ':!*.png' ':!*.jpg' ':!*.bin'

# Step 2: Normalize
# - Sort hunks by file path (alphabetical)
# - Strip index/mode metadata lines (keep only ---, +++, @@, content)
# - Normalize line endings to LF
canonical_diff = normalize(raw_diff)

# Step 3: Hash
content_hash = SHA-256(canonical_diff)
```

Both `base_commit` and `head_commit` SHAs are recorded alongside the hash (stored in vault metadata). This ensures:
- **Determinism:** Exact commits + normalization = same hash on any machine, any git version
- **Verifiability:** Anyone can clone, run the same steps, verify the hash

**Binary files:** Excluded from the canonical diff via pathspec exclusions. Binary changes (images, compiled assets) are listed separately in vault metadata with their own SHA-256 hashes computed from `git hash-object`. The reference implementation (shipped as `os-git`) is the authoritative source for the canonical diff algorithm.

**Note:** There is ONE canonical diff specification (above). The normalization steps are part of the algorithm, not an alternative to it.

The full diff (with metadata headers) is stored in the vault alongside the canonical hash for reference.

**Why diff hash, not commit hash?** A commit SHA includes metadata (author, timestamp, parent) that changes across rebases. The diff content is what matters for review. However, the commit SHAs are recorded as supplementary metadata for reproducibility.

### PR Revision Model

**Problem:** PRs are mutable (developers push new commits). But on-chain contributions are immutable (`content_hash` is set once, no update path). If a voter approves hash H1 but the developer pushes H2 before merge, the voted-on code ≠ the merged code.

**Solution: One contribution per revision.** When a PR is updated with material changes:

1. The previous contribution is **withdrawn** by the author (see §Contract Changes below)
2. A new contribution is submitted with the new diff hash and a `supersedes: Option<u64>` reference to the previous contribution ID
3. Votes do NOT carry over — the new revision must be reviewed independently
4. The vault stores the full revision history (contribution_id → diff hash → commit SHAs)

The bridge CLI handles this automatically: `os-git submit` checks if a contribution already exists for this PR. If so, it withdraws the old one and submits a new one.

**No tolerance for hash mismatch.** If the diff changes, the developer must withdraw and resubmit — even for typo fixes. The revision model handles this cleanly. The approved hash must match the merged code, period. Any post-approval change without resubmission is detectable by `os-git audit` and should be flagged.

### Reconciliation

**Problem:** Git and chain can desynchronize — PR merged without on-chain acceptance, contribution accepted but PR never merged, bridge crashes mid-operation.

**Solution: `os-git audit` reconciliation tool.** Compares git log of merged commits against on-chain contribution records:

```bash
os-git audit --project 0 --since 2026-03-01
```

Reports:
- PRs merged without accepted contribution (governance gap)
- Accepted contributions without corresponding merged PR (stale approvals)
- Contributions in Review with closed/merged PRs (orphaned reviews)

Run periodically or as a CI check. The reconciliation tool is informational — it doesn't auto-fix, just reports.

---

## Workflow: Incubation Phase (Owner-Driven)

During incubation, the project owner has direct accept/reject power. This is how Open Systems works RIGHT NOW — single developer making decisions.

```
1. Developer opens PR on GitHub
2. Developer (or webhook) runs:
   $ os-git submit --project 0 --pr https://github.com/org/repo/pull/42
   → Computes diff hash
   → Stores diff in vault
   → Calls SubmitContribution { project_id: 0, title: "PR #42: Fix auth", content_hash }
   → Returns contribution_id

3. Owner reviews the code on GitHub (normal code review)
4. Owner accepts:
   $ os-git accept --contribution 5
   → Calls AcceptContribution { contribution_id: 5 }
   → XP minted to author

5. Developer merges PR on GitHub
```

**Key insight:** During incubation, the on-chain step is lightweight — the owner just records their accept/reject decision. Code review happens on GitHub as normal. The chain tracks the history and mints XP.

## Workflow: Released Phase (Community-Governed)

After release, contributions go through community voting. This is the target state.

```
1. Developer opens PR on GitHub
2. Bridge (webhook or developer) submits contribution on-chain:
   → SubmitContribution { project_id: 0, title: "PR #42: ...", content_hash }
   → Contribution enters Review status

3. Community members review the code:
   - Read the diff on GitHub or in the vault
   - Vote on-chain:
     $ os-git vote --contribution 5 --approve
     → VoteContribution { contribution_id: 5, vote: Approve }

4. After review_period expires, anyone finalizes:
   $ os-git finalize --contribution 5
   → FinalizeContribution { contribution_id: 5 }
   → If approved (meets quorum + threshold): XP minted, status = Accepted
   → If rejected: status = Rejected

5. On acceptance: merge PR on GitHub
   (manual, or webhook auto-merges)
```

**Dispute resolution:** If a contribution is rejected, the author can modify the PR and submit a new contribution. The auditing contract's appeal mechanism is available if needed (author stakes XP to appeal).

## Workflow: System Sovereignty (Self-Governing)

The ultimate goal: Open Systems manages its own chain code through this process.

```
1. Developer writes a contract fix
2. Opens PR → bridge creates contribution on opensystems project
3. Community reviews and votes
4. On acceptance:
   a. Merge PR
   b. Build sovereignty pipeline: build spec → builders compile → artifact verification
   c. Governance proposal: MigrateContract with verified artifact
   d. Community votes on deployment
   e. Contract upgraded on-chain

Same flow for chain binary changes (Go code):
   c. Build spec → builders compile Go binary → artifact verification
   d. Governance proposal: ScheduleUpgrade with verified binary hash
   e. Community votes → x/upgrade coordinates validator halt + switch
```

---

## The CLI Tool: `os-git`

### Commands

```bash
# Project management
os-git init --repo https://github.com/org/repo --project 0
    # Links a git repo to an on-chain project
    # Stores mapping in .os-git/config

# Submit a PR as contribution
os-git submit [--pr URL | --diff FILE | --commit SHA]
    # Computes canonical diff hash
    # Stores diff in vault
    # Calls SubmitContribution
    # Stores contribution_id ↔ PR mapping in .os-git/contributions.json

# Review and vote
os-git vote CONTRIBUTION_ID [--approve | --reject]
    # Calls VoteContribution

# Owner accept/reject (incubation only)
os-git accept CONTRIBUTION_ID
os-git reject CONTRIBUTION_ID

# Finalize after review period
os-git finalize CONTRIBUTION_ID
    # Calls FinalizeContribution (permissionless crank)

# Status
os-git status [CONTRIBUTION_ID | --project PROJECT_ID]
    # Shows contribution status, votes, review period remaining

# List contributions
os-git list --project PROJECT_ID [--status review|accepted|rejected]
```

### Configuration

```json
// .os-git/config.json
{
  "project_id": 0,
  "repo_url": "https://github.com/opensystems/opensystems",
  "chain_binary": "~/go/bin/opensystemsd",
  "chain_home": "~/.opensystems",
  "key_name": "alice",
  "vault_url": "http://localhost:9191",
  "contracts": {
    "projects": "os1eyfccm..."
  }
}
```

### Local Tracking

```json
// .os-git/contributions.json
{
  "contributions": [
    {
      "contribution_id": 5,
      "pr_url": "https://github.com/org/repo/pull/42",
      "commit_sha": "abc123...",
      "diff_hash": "def456...",
      "vault_hash": "def456...",
      "status": "review",
      "submitted_at": "2026-03-21T10:00:00Z"
    }
  ]
}
```

---

## Webhook Service (Phase 2)

For production use, a webhook service automates the bridge:

### Events Watched

| Git Event | Chain Action |
|-----------|-------------|
| PR opened | `SubmitContribution` (compute diff hash, store in vault) |
| PR updated (new commits) | Withdraw old contribution, submit new one with `supersedes` reference (per revision model) |
| PR review submitted (approve) | Notify reviewer to vote on-chain (reviewer signs own `VoteContribution`) |
| PR review submitted (request changes) | Notify reviewer to vote reject on-chain |
| PR merged | Verify contribution was accepted on-chain. If not, log warning. |
| PR closed without merge | `WithdrawContribution` if author has chain key configured |

### Architecture

```
GitHub Webhook → Bridge Service → Chain TX
                      ↓
                    Vault (store diff)
```

The bridge service is a Python process (consistent with existing MCP server and vault relay). It:
- Listens for GitHub webhooks on a configured port
- Maps GitHub users → chain keys (configured per repo)
- Signs and submits transactions using the mapped key
- Stores diffs in the vault
- Tracks PR ↔ contribution mappings in a local SQLite database

### Security

- Webhook payloads verified via GitHub's HMAC signature
- **The bridge service does NOT hold developer private keys.** Instead:
  - **Option A (preferred for Phase 1):** Developers use the CLI directly. The webhook sends notifications (e.g., GitHub comment, Slack) but does NOT create transactions. The developer runs `os-git submit` / `os-git vote` locally. Simple, no new trust surface.
  - **Option B (Phase 2):** The bridge creates unsigned transaction payloads signed with an HMAC by the bridge. Developers run `os-git agent` that polls, verifies the HMAC, displays the transaction details, and signs with their local key after explicit approval. The HMAC prevents payload tampering in transit.
  - For votes: developers always sign their own vote transactions via CLI or explorer. The webhook notifies them ("PR #42 needs your review") but doesn't vote on their behalf.
  - **No bot account for submissions.** The contract sets `author = info.sender` (the transaction signer). XP is minted to the author. There is no mechanism to specify a different author, so the developer must sign their own submission.
- The bridge service is a convenience layer, not a trust layer
- If the bridge goes down, developers use the CLI directly

---

## Canonical Diff Format

See Content Hashing section above for the single authoritative specification. The `os-git` reference implementation is the canonical source for the algorithm.

---

## How This Applies to Open Systems Itself

### Bootstrapping: Register the Project

```bash
# Create the opensystems project on-chain (already exists as project 0)
# Link the repo
os-git init --repo https://github.com/opensystems/opensystems --project 0
```

### Day-to-Day Development

```bash
# Developer writes code, opens PR
git checkout -b feature/expression-observation
# ... write code ...
git push origin feature/expression-observation
# Open PR on GitHub

# Submit to chain
os-git submit --pr https://github.com/opensystems/opensystems/pull/15

# Owner (during incubation) reviews and accepts
os-git accept 5

# Merge on GitHub
```

### Transition to Community

```bash
# When enough contributors exist, release the project
os-git release --project 0
# From now on, all contributions go through community vote

# Community member reviews a PR
os-git vote 12 --approve

# After review period, finalize
os-git finalize 12
# → Accepted → XP minted → merge the PR
```

---

## Required Contract Changes

Despite principle #5 ("no new contracts needed"), the critic chain revealed that the existing Projects contract has gaps that must be addressed for git governance to work securely:

### 1. WithdrawContribution (new message) + Withdrawn status

```rust
ExecuteMsg::WithdrawContribution { contribution_id: u64 }
```
- Author-only, only while status = Review
- Sets status to `Withdrawn` (new variant in `ContributionStatus` enum)
- Contribution record is preserved (not deleted) for audit trail and `supersedes` chain
- Required for the PR revision model (withdraw old → submit new)
- Also prevents abandoned contributions from polluting the review queue

```rust
pub enum ContributionStatus {
    Review,
    Accepted,
    Rejected,
    Withdrawn,  // NEW — author voluntarily withdrew
}
```

### 2. Content Hash Deduplication

Add uniqueness check in `execute_submit_contribution`: reject if the same `content_hash` already exists for this project in `Review` or `Accepted` status. **Withdrawn and Rejected contributions are excluded from the dedup check** — allowing legitimate resubmission after a fix-and-retry cycle. Prevents front-running and accidental duplicates.

### 3. XP-Weighted Voting with Quorum

The current `FinalizeContribution` uses simple majority (1-account-1-vote with `balance > 0` gate). This is sybil-vulnerable: free accounts + one small contribution = permanent voting rights.

**Fix:** Align contribution voting with the governance contract model:
- **Weight votes by XP** in the project's primary subject (the first subject in the project's subject list). Single-subject weighting avoids double-counting users with XP across multiple project subjects. If a project has subjects `[rust, cosmwasm]`, vote weight = XP in `rust`.
- **Quorum + approval:** Use the **same model as the governance contract** — snapshot `total_power` (total XP in primary subject) at contribution creation time. Quorum = 30% of `total_power` must vote. Approval = 70% weighted approval. This is consistent, already proven, and requires no new on-chain indexes.
- **Self-voting prevention:** Contribution author cannot vote on their own contribution. The contract rejects `VoteContribution` if `voter == contribution.author`.
- **XP minting scope:** Currently the projects contract mints +1 XP in ALL project subjects on contribution acceptance. This creates a gaming vector: a project with 5 subjects awards 5 XP per contribution, but voting only uses 1 subject. **Fix:** Mint XP only in the primary subject. If the project community wants to award XP in additional subjects, they can add that via governance parameter later.

This is a contract migration.

### 4. Contribution Submission Stake (Anti-Spam)

**Problem:** Zero-fee transactions + free accounts = unlimited contribution spam on released projects. Each spam contribution consumes reviewer attention for the full review period. Per-account rate limits are theater (Golden Rule: meaningless when accounts are free).

**Solution: XP stake on submission.** Submitting a contribution to a released project requires staking XP:

- **Stake amount:** Configurable per project (default: 1 XP in the project's primary subject)
- **On acceptance:** Stake returned to author + XP minted as reward (existing behavior)
- **On rejection:** Stake burned (cost of wasting the community's review time)
- **On withdrawal:** Stake returned (author self-corrected)
- **During incubation:** No stake required (owner filters spam directly)

This anchors the cost of submission to something scarce (verified work in the project's domain), not account identity. A sybil attacker must earn real XP in the project to spam it — the same XP they'd burn on each rejected submission.

**Dependency:** The projects contract must be an authorized caller on the experience contract for `LockExperience`, `UnlockExperience`, and `BurnLocked` internal messages (it's already authorized for `MintExperience`). After contract migration, the new projects contract address must be re-registered as an authorized caller via governance. This is a deployment step, not a code change.

**Edge case: newcomers.** A first-time contributor to a project has 0 XP and can't stake. Solutions:
- **Sponsor model:** An existing contributor can sponsor a newcomer's submission (stake their own XP on the newcomer's behalf). The sponsor's stake is at risk — they vouch for the newcomer.
- **Incubation exception:** During incubation, no stake needed. Most newcomers contribute during incubation when the owner is actively mentoring.

### 5. Contribution Supersession (optional, for tracking)

Add `supersedes: Option<u64>` field to `Contribution` struct. When a contribution supersedes another, the old one is automatically marked as withdrawn. Provides a clean revision chain for auditing.

---

## What We're NOT Building (Explicitly Out of Scope)

1. **On-chain git storage.** Git repos stay on GitHub/Gitea/wherever. Chain stores hashes only.
2. **Automatic merge.** The bridge doesn't auto-merge PRs. Developers merge manually after on-chain acceptance. (Auto-merge can be added later as a webhook feature.)
3. **New smart contracts.** We're building tooling, not new contracts. However, the existing Projects contract requires migration to add: WithdrawContribution, XP-weighted voting, quorum, self-vote prevention, and submission staking. These are modifications to an existing contract, not a new one.
4. **GitHub-specific features.** The CLI works with any git repo. The webhook service is GitHub-specific but could be extended to Gitea/GitLab.
5. **Branch protection.** Git hosting platforms handle branch protection. The chain handles contribution governance. They're separate concerns.
6. **Conflict resolution.** Git handles merge conflicts. The chain handles governance disputes.

---

## Implementation Plan

### Phase 1: CLI Tool (Minimum Viable Bridge)

Build `os-git` as a Python CLI (consistent with existing tooling):
- `init`, `submit`, `accept`, `reject`, `vote`, `finalize`, `status`, `list`
- Uses `lib/cli.py` for chain interaction
- Uses vault for diff storage
- Stores local state in `.os-git/`
- Manual workflow: developer runs commands explicitly

**Deliverable:** A working CLI that bridges git PRs to on-chain contributions. Enough to start managing Open Systems development through the chain.

### Phase 2: Webhook Service

Build automated bridge:
- GitHub webhook listener
- PR → contribution automation
- Review → vote mapping
- Status reporting back to GitHub (PR comments)

### Phase 3: Web Explorer Integration

Add git governance views to the web explorer:
- PR list with on-chain status
- Vote on contributions from the browser
- Contribution history with git diffs

---

## Open Questions

1. ~~PR updates~~ — **RESOLVED:** One contribution per revision. Old contribution withdrawn, new one submitted with `supersedes` reference. Votes don't carry over.

2. **Review period for incubation.** During incubation, the owner accepts/rejects instantly. Should there be a minimum review period even during incubation (to give the community time to flag concerns)?

3. **Cross-project contributions.** A PR might touch code that spans multiple on-chain projects. How to handle? Probably: one contribution per project, split by the developer. Canonical diff applies per-project scope.

4. **Key management.** Developers need chain keys to submit contributions and vote. Current approach: keys in local keyring (`opensystemsd keys`). Long-term: investigate key delegation or lightweight signing agents.

5. **Git hosting decentralization.** GitHub is centralized. Long-term, support self-hosted Gitea instances or bare repos on the vault relay network. CLI is hosting-agnostic from the start.

6. ~~Contribution spam defense~~ — **RESOLVED:** XP stake on submission (required change #4). Stake burned on rejection, returned on acceptance/withdrawal. Newcomers handled via sponsor model or incubation exception.

7. **Auditing integration.** The existing auditing contract is designed for forum posts (`Report` takes a `post_id`). Code contributions may need a parallel audit path. Defer to a future brainstorm — for now, the community vote on contributions IS the quality gate.

---

## Critic Chain Results

**5 rounds, 48 total issues (4 FATAL + 20 HIGH + 24 MODERATE). All FATAL and HIGH resolved.**

| Round | FATAL | HIGH | MOD | Key Fixes |
|-------|-------|------|-----|-----------|
| 1 | 2 | 5 | 6 | Deterministic diff (exact SHAs + normalization), PR revision model (withdraw+resubmit), reconciliation tool, hash dedup, webhook key custody, XP-weighted voting, WithdrawContribution |
| 2 | 1 | 6 | 6 | Binary exclusion fix (--text flag wrong), single diff spec, remove bot account, self-vote prevention, dedup excludes rejected, quorum requirement, webhook table consistency |
| 3 | 1 | 5 | 5 | XP stake anti-spam with sponsor model, remove minor-update tolerance, primary-subject voting, HMAC signing queue, quorum stall defense |
| 4 | 0 | 4 | 4 | Snapshot quorum (match governance model), primary-subject XP minting, authorized caller dependency, remove cross-subject staking |
| 5 | 0 | 0 | 3 | Converged. Remaining: total_power field, min_votes disposition, supersession atomicity |

### Key Architectural Decisions

1. **XP stake on submission** — anchors spam defense to verified work, not account identity
2. **Primary-subject-only** — voting weight AND XP minting scoped to first subject
3. **Snapshot quorum** — reuses governance contract's proven model
4. **Strict hash matching** — no tolerance for post-approval divergence
5. **CLI-first bridge** — Phase 1 avoids signing queue trust surface
6. **One contribution per revision** — withdraw old, submit new, votes don't carry over

### Remaining MODERATE Issues (for implementation)

1. Add `total_power: u64` to `Contribution` struct for quorum snapshot
2. Decide `min_votes` disposition (remove, repurpose, or keep as floor)
3. Clarify supersession atomicity (auto-withdraw in contract vs two-TX)
4. `.os-git/` should be `.gitignore`d
5. `os-git audit` fallback when local tracking missing
6. In-flight contributions during project release transition
7. `os-git release` and `os-git audit` missing from CLI commands list
8. `os-git` needs `sync` command to rebuild local state from chain

---

## References

- [Decision 004: Project-Level Governance First](../decisions/004-project-governance-before-global.md)
- [Decision 006: System Sovereignty](../decisions/006-system-sovereignty.md)
- [Brainstorm 006: Incubator Ownership Model](006-incubator-ownership-model.md)
- [Projects Contract](../../../opensystems/contracts/projects/src/msg.rs)
- [Archived Projects Spec v1](../../DATA-DUMP/Recent/From%20Open%20Systems%20Project%20in%20ChatGpt/open_projects_spec_v_1.md)
