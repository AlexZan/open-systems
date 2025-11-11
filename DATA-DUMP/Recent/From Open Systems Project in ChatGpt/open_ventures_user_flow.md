## Open Ventures User Experience and Smart Contract Architecture

### 1. Overview
This document unifies the user experience (UX) flow for funding Open Ventures projects with the underlying smart contract design. The goal is to ensure seamless participation for users unfamiliar with crypto while maintaining full on-chain transparency and decentralization.

---

### 2. Fiat-to-Crypto User Flow

#### 2.1 Discovery
- A user finds a project page (via Open Systems, social links, or embeds).
- The project page clearly shows:
  - Description and goals.
  - Funding progress bars.
  - Community discussions and proof submissions.
  - A single, prominent **“Fund this Project”** button.

#### 2.2 Funding Options
When clicked, the user is offered two methods:

1. **Credit / Debit Card (Recommended)**  
   - Handled via a fiat-to-crypto provider (e.g., MoonPay, Paybis, Ramp Network).  
   - User enters amount and pays through Apple Pay, Google Pay, or bank transfer.  
   - Provider automatically converts fiat → stablecoin (e.g., USDC) → deposits to the project escrow.

2. **Crypto Wallet (Advanced Users)**  
   - User connects a Web3 wallet (MetaMask, Rainbow, Brave Wallet, etc.).  
   - Sends crypto directly to the project contract.

#### 2.3 Wallet Generation (for new users)
If the user funds via fiat and has no wallet:
- A **light wallet** is auto-generated using MPC or Web3Auth.  
- Recovery options (email/social login) provided.
- The wallet address becomes the **beneficiary address** for stake token issuance.

#### 2.4 Stake Tokens Issuance
Once payment clears:
- Smart contracts mint **non-transferable (soulbound) stake tokens**.  
- 1 token = 1 unit of funding.  
- Tokens grant **voting power** to accept or reject submitted work.  
- Tokens cannot be sold or transferred.

#### 2.5 Engagement Post-Funding
- Users can view their stake tokens in their dashboard.  
- When a project milestone (goal) proof is submitted, the system notifies them to vote.  
- Votes are cast directly in-app (gasless via meta-transactions).  
- Users can also track project updates and discussion threads.

---

### 3. Smart Contract System Design

#### 3.1 Contract Overview
Each Open Venture (Project) is composed of modular smart contracts with single responsibilities:

| Contract | Purpose |
|-----------|----------|
| **Project Contract** | Stores project metadata, manages goal lifecycle, interacts with failover and goal contracts. |
| **Goal Contract** | Handles goal-specific funding, proof submissions, and voting logic. |
| **Token Contract** | Mints non-transferable stake tokens to funders. |
| **Voting Contract** | Records votes, enforces quorum and approval thresholds. |
| **Proof Contract** | Stores proof bundles (build artifacts, commits, demo links). |
| **Failover Contract** | Detects inactivity or failed votes and converts the project to an Open Project. |
| **Funding Escrow** | Holds funds until successful proof approval. |
| **GitHub Oracle** | Verifies commits, releases, and CI status for proof authenticity. |

---

#### 3.2 Funding Lifecycle
1. **Project Creation**: Product Owner (PO) defines project metadata and goals.
2. **Funding Phase**:
   - Fiat/crypto contributions are received.
   - Stake tokens minted to funders (soulbound).
   - Escrow holds funds per goal.
3. **Proof Submission**:
   - PO submits a proof bundle (commit hash, artifact, demo link).
   - Proof Contract logs and timestamps submission.
4. **Voting Phase**:
   - 72-hour window for funders to vote.
   - Pass condition: ≥70% Yes votes, ≥30% quorum.
   - If passed → Escrow releases funds to PO.
   - If failed twice → triggers **Failover vote**.
5. **Failover**:
   - If inactivity or consecutive failure occurs, token holders can vote to convert project to **Open Project**.
   - Remaining goals become public bounties.

---

#### 3.3 Voting and Stake Token Rules
- **One Vote per Token**: Each token = 1 vote.
- **Non-Transferable**: Tokens cannot be moved or sold.
- **Purpose-Limited**: Only used to vote on proofs (task submissions).
- **Gasless Voting**: Meta-transaction relayers cover gas for novice users.
- **Snapshot Enforcement**: Token balances locked at vote start to prevent double voting.

---

### 4. Fiat On-Ramp Integration Models

#### Model A: Provider-First (MVP)
- Integrate a provider like **MoonPay or Paybis** directly into the front-end.
- Provider executes on-chain contract call `contributeFor(projectId, beneficiary)`.
- Tokens are minted automatically.

#### Model B: Custodial Pool (Later Phase)
- Fiat funds collected off-chain via Open Systems custodial account.
- Converted in bulk to stablecoin and deposited to escrow.
- Allows micro-donations and lower fees.

---

### 5. UX Simplification Highlights
- **No crypto jargon**: Use terms like *"Project Shares"* instead of *"Stake Tokens."*
- **One-click funding** via card or wallet.
- **Auto-wallet creation** for newcomers.
- **Transparent progress tracking** through visual timelines.
- **Simple vote prompts**: *“Approve milestone?”* Yes/No.

---

### 6. Security and Transparency
- **Immutable Ledger**: All funding, votes, and proofs recorded on-chain.
- **Escrow Protection**: Funds released only through successful votes.
- **Failover Mechanism**: Prevents stagnation if PO abandons project.
- **Off-chain Data Integrity**: Hashes ensure authenticity of large files (GitHub oracle).

---

### 7. Example Flow Summary
1. User discovers a solar microgrid project.  
2. Clicks *Fund this Project* → pays with card via MoonPay.  
3. Fiat converted → escrowed on-chain.  
4. User gets non-transferable stake tokens.  
5. When milestone proof is submitted, user receives a push/email to vote.  
6. If approved, funds are released; project continues to next goal.

---

### 8. Next Steps
- Deploy contracts on testnet (Polygon or Base).  
- Integrate MoonPay API for fiat conversion and direct contract calls.  
- Build Web3Auth onboarding for walletless users.  
- Launch MVP UI using Next.js stack defined in **Open Projects Stack**【43†Open Projects Stack†L1-L20】.  
- Verify contract logic with the **Smart Contracts Architecture** reference【44†Smart Contracts Architecture†L1-L60】.

