# Open Systems Projects – Phase 1 Scope  
*(Proof of Concept Outline)*

## 1. Purpose
The initial proof of concept (POC) will validate the basic mechanics of Open Systems Projects in the simplest form:
- **Single Product Owner (PO)**  
- **Funded goals with escrow**  
- **Proof submission and voting**  
- **Fund release on consensus**  

This keeps the system minimal while demonstrating transparency, funding, and accountability.

---

## 2. Roles
- **Product Owner (PO):**  
  Creates project, defines goals, submits proofs. Has sole management responsibility in this phase.  
- **Funders:**  
  Contribute funds, receive non-transferable stake tokens, and vote on proof submissions.  
- **Community:**  
  May comment and vote on proofs, but cannot take over ownership in Phase 1.

---

## 3. Core Objects
- **Project:** Metadata (title, description, repo links, PO account).  
- **Goal:** Funding target, criteria, and lifecycle (Funding → Proof Submitted → Voting → Passed/Failed).  
- **Tokens:** Non-transferable stake tokens, 1 per funding unit.  
- **Proof:** Evidence bundle (commit SHA, build artifact hash, demo link).  
- **Vote:** Token-weighted, time-boxed decision (≥30% quorum, ≥70% Yes).  

---

## 4. Processes
1. **Creation:** PO defines project and goals.  
2. **Funding:** Funders back goals, minting stake tokens.  
3. **Proof Submission:** PO delivers commit + artifacts as evidence.  
4. **Voting:** Token-holders review and vote.  
   - Pass → funds released.  
   - Fail → PO may retry (max 2 times).  
5. **Closure:** On final goal completion, tokens are burned.  

---

## 5. GitHub Integration (Phase 1)
- **Inbound:** Webhooks for commits, tags, releases, and CI results.  
- **Outbound:** Bot posts comments when goals are funded or proofs pass, and adds status badges.  
- **No merge automation yet:** PO retains merge control in GitHub. Governance is demonstrated through voting, not enforced merges.

---

## 6. Security & Limitations
- **Escrow contract:** Ensures funds only move on successful vote.  
- **On-chain state:** Projects, tokens, votes, proofs.  
- **Off-chain state:** Artifacts (by hash reference).  
- **Limitations:**  
  - Only one PO (no community ownership).  
  - No experience/reputation scores.  
  - Failover and Open Project transitions not included.  
  - Forum limited to per-goal comments.  

---

## 7. Future Phases
- **Phase 2:** Introduce **failover** mechanism → projects can roll into **Open Projects** if PO is inactive or fails votes.  
- **Phase 3:** Open Projects and community ownership fully supported, with bounties, decentralized merge automation, and governance.

