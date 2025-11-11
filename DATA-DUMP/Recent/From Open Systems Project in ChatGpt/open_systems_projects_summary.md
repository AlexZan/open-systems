# Open Systems Projects Summary (Merged from Open Ventures)

## Overview
Projects (previously referred to as *Open Ventures*) are the **crowdfunded, milestone-driven collaboration system** in Open Systems.  
They allow individuals or groups to **create, fund, and manage ventures** with transparent rules, shared ownership, and built-in trust through decentralized validation.

Projects can be:
- **Closed Projects** — one or more defined owners (Product Owners) who set the rules and goals.  
- **Open Projects** — community-run projects with no single owner; all goals are bounties anyone can achieve.  
- **Venture-style Projects** — practical, small-group implementations (e.g. fixing up a camper or bulk resale venture) that use bidding, deposits, and profit-sharing presets.

---

## Core Principles
- **Decentralized:** No central authority; projects run through consensus and smart contracts.  
- **Transparent:** Every transaction, proof, and vote is visible on-chain.  
- **Fair and Open:** All participants can create, fund, and verify work equally.  
- **Continuous Ownership:** If a project fails or is abandoned, it can convert into an Open Project for community continuation.

---

## Core Components
### 1. Roles
- **Product Owner (PO)** – defines goals, funding, and rules.  
- **Funders** – contribute capital, receive non-transferable stake tokens.  
- **Contributors** – complete goals, submit proofs, earn payouts or shares.  
- **Community** – reviews, votes, and can trigger failover to open mode.  

### 2. Objects
- **Projects** – overarching container of all goals and metadata.  
- **Goals** – discrete, fundable milestones with proof and payout conditions.  
- **Tokens** – non-transferable “stake tokens” grant voting rights on goal verification.  
- **Proofs** – evidence submissions tied to commits, builds, or deliverables.  
- **Votes** – democratic approval mechanism for proof validation and fund release.  

---

## Processes
1. **Project Creation** – PO defines metadata, goals, and proof criteria.  
2. **Funding** – Funders send capital and receive stake tokens per goal.  
3. **Proof & Voting** – Contributors submit proof bundles; funders vote (≥30% quorum, ≥70% approval).  
4. **Failover** – If PO is inactive or fails consecutive votes, token holders can vote to convert the project to open status.  
5. **Completion** – Upon final goal approval, tokens are burned and profits distributed.  

---

## Bidding and Venture Mechanics
Originally part of *Open Ventures*, the bidding system is now a **feature** that can be enabled within Projects:
- Members **bid** for tasks by offering better terms (cost, time, or equity).  
- **Task Locking** prevents new bids once accepted.  
- **Deposits** ensure accountability: a member’s liability equals or exceeds the consumer value of the task.  
- **Sweat Equity Multipliers** reward early contributors or higher-risk tasks.  
- **Profit Sharing** uses configurable templates (e.g. 40% founders / 40% members / 10% expenses / 10% warehouse).  

This turns Open Projects into dynamic, self-managed **micro-ventures**.

---

## Funding and Tokens
- **Stake Tokens:** Non-transferable voting tokens tied to specific goals.  
- **Proof Voting:** Determines if milestones meet agreed criteria.  
- **Profit or Token Returns:** Depending on project rules, contributors and backers can receive proportional returns or revenue shares.  
- **Failover Mechanism:** Prevents stagnation—if a project owner disappears or fails goals twice, it transitions into an open, bounty-driven format.  

---

## Rule Sets and Certifications
Projects can adopt rule sets via the **Open Certification Network**, defining behavior for fairness, transparency, and human rights.  
Violations can lead to **community-imposed sanctions**, ensuring ethical compliance across ventures.

---

## Technical Architecture
- **Smart Contracts:** Modular contracts handle Projects, Goals, Tokens, Voting, and Failover.  
- **Funding Escrow:** Holds contributions until proof approval.  
- **GitHub Oracle:** Syncs commits, releases, and CI data into proof bundles.  
- **Frontend Stack:** Next.js + Expo mobile clients with WalletConnect and on-chain integration for funding and voting.  

---

## Templates / Presets
### Venture Preset (Local Collaboration)
Preset designed for small, in-person ventures (e.g. restoring a camper, equipment resale):
- Co-owned by a small group.  
- Uses task bidding for fair workload distribution.  
- Shared deposit pool to mitigate liability.  
- Default profit split template.  

### Open Project Preset (Community Collaboration)
Preset for online, public collaboration:
- Fully open membership.  
- All goals as bounties.  
- Profit or credit distributed via contribution tokens.  

### Traditional Project Preset
For single-owner ventures with funders and clear milestone voting.

---

## Unified Definition
**Projects in Open Systems** are collaborative, crowdfunded, and verifiable ventures where tasks, funding, and decisions are governed through transparent smart contracts and community validation.  
They can range from local physical ventures to global open-source initiatives, all sharing the same foundation of fairness, accountability, and openness.

