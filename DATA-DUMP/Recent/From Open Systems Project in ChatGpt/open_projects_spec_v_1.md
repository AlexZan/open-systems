# Open Systems Projects Specification
**Version:** 1.0

---

## 1. Overview
Projects (previously referred to as Open Ventures) are a **crowdfunded, milestone-driven collaboration system** within Open Systems. They allow a Product Owner (PO) to raise funds in stages, with community oversight and accountability through voting. Projects can evolve into Open Projects if abandoned, ensuring continuity.

This specification defines:
- Roles and responsibilities.
- Core objects (Projects, Goals, Tokens, Proofs, Votes).
- Processes (Creation, Funding, Proof, Voting, Failover).
- Interfaces and GitHub integration points.
- Security model and limitations for Phase 1.

---

## 2. Roles
- **Product Owner (PO):** Creates and manages the project, defines goals, submits proofs.
- **Funders:** Provide capital, receive non-transferable stake tokens tied to goals, vote on proofs.
- **Community:** Can comment, suggest improvements, and take over via failover if PO is inactive.

---

## 3. Core Objects

### 3.1 Project
- **Fields:**
  - Title
  - Description
  - Repository links (e.g., GitHub)
  - Owner (wallet + account)
  - Goals[]

### 3.2 Goal
- **Fields:**
  - Title
  - Funding requirement (amount)
  - Stake token ledger (per goal)
  - Proof criteria (defined by PO)
  - Status: Funding / Proof Submitted / Voting / Passed / Failed

### 3.3 Token
- **Type:** Non-transferable stake token.
- **Issuance:** 1 token per unit funded (per goal).
- **Utility:** Voting rights on proof submissions for that goal.
- **Expiry:** Burned at project closure or conversion to Open Project.

### 3.4 Proof Submission
- **Fields:**
  - Evidence bundle (Git commit, build artifact hash, demo links, checklist).
  - Submission date.
  - Associated Goal ID.

### 3.5 Vote
- **Fields:**
  - Goal ID
  - Token holder address
  - Vote: Yes / No
  - Weight: Tokens staked

---

## 4. Processes

### 4.1 Project Creation
1. PO submits metadata (title, description, repo links).
2. Defines goals with funding asks and proof criteria.
3. System deploys project contract with empty token ledgers.

### 4.2 Funding
1. Funder selects goal(s) to support.
2. Sends funds → receives stake tokens tied to that goal.
3. System updates funding progress bar.
4. When funding target met → goal moves to “Ready for Proof.”

### 4.3 Proof & Voting
1. PO submits proof bundle for a goal.
2. Voting window opens (default 72h).
   - Quorum: 30% of tokens.
   - Pass condition: ≥70% Yes votes.
3. If passed → funds released to PO.
4. If failed → PO may resubmit (max 2 attempts).

### 4.4 Failover
- Triggered if:
  - PO inactive (time threshold defined).
  - 2 consecutive failed votes on the same goal.
- Token holders start **Failover Vote**.
  - Pass condition: ≥60% Yes, 30% quorum.
- If passed → project converts to **Open Project**.
  - Remaining goals become bounties.
  - Any developer can submit proofs.
  - Rewards distributed via successful votes.

---

## 5. Interfaces

### 5.1 User Dashboard
- **Funders:**
  - Funding progress per goal.
  - Token balance per goal.
  - Active votes with countdown.
  - Proof bundles with evidence and checklist.

- **PO:**
  - Create/edit goals.
  - Submit proof bundles.
  - View vote results & payout status.

### 5.2 Comments
- Threaded comments on each goal and project root.
- Used for feedback, suggestions, bug reports.
- No experience/reputation system in Phase 1.

---

## 6. GitHub Integration

### Inbound (GitHub ➜ Projects)
- Webhooks: `push`, `release`, `workflow_run`.
- Signed tags & release data.
- CI status capture for required checks.
- Artifact digests and hashes.
- Optional: SBOM, SLSA attestations, perf reports.

### Outbound (Projects ➜ GitHub)
- Bot posts comments on releases when goals pass.
- Status badge in README linking to project page.
- Optional: issue mirroring for goal discussions.

### Proof Bundle Contents
- Repo + commit SHA.
- Signed tag metadata.
- Required checks + outcomes.
- Artifact hashes.
- Checklist mapping criteria → evidence.

---

## 7. Security & Integrity
- On-chain: project data, token balances, votes, payouts, failover triggers.
- Off-chain: large files (builds, videos) stored by hash reference.
- Immutability: if a tag or artifact is changed, proof auto-invalidates until corrected.

---

## 8. Limitations (Phase 1 Scope)
- Single PO only.
- No transferable tokens (pre-purchase in Phase 2).
- No experience-based voting.
- No full forum; only goal-based comments.
- Fixed rule sets (no templates yet).

---

## 9. Example Workflow (Game Project)
1. Alice pledges $500, Bob $2000, Carla $1000.
2. Goal 1 fully funded at $8,000.
3. PO submits v0.1 build proof.
4. Vote passes (85% Yes, quorum met) → $8k released.
5. Goal 2 first vote fails (bugs) → resubmitted → passes.
6. If PO abandoned, failover vote converts project to Open Project.

---

## 10. Versioning
- **Version 1.0 (Current):**
  - Defines single-PO Projects.
  - Funding, tokens, proof-based voting.
  - Failover protection.
  - GitHub inbound/outbound proof integration.
  - Comment-only discussion.
  - Excludes transferable tokens, experience, and forum features.

