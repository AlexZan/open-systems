# Open Systems Glossary

Consistent terminology across all specifications and implementations.

---

## Core Concepts

### Experience
**Earned voting power derived from meaningful contribution to the system.**

- Not purchasable; cannot be transferred or inherited
- Consumed when casting votes (voting has a cost)
- Represents track record of creating value for the community
- Rewards both creators and validators of good work
- Can be earned through projects, governance participation, forum engagement, etc.

*Example: Alice completes a project goal successfully. The community votes to approve. She earns experience. Later, she uses that experience to vote on another goal's proof.*

---

### Stake Token
**Non-transferable voting right tied to a specific project goal.**

- Represents financial investment in a goal
- Grants voting rights on proof validation for that specific goal
- Burned (destroyed) upon project completion
- Cannot be sold, traded, or transferred to another person
- Ensures funders have skin in the game and incentive to vote fairly

*Example: Bob funds a project goal with 10 tokens. The goal is completed. Bob receives 1 stake token per 10 tokens invested. He votes yes/no on whether the proof meets criteria. His vote is weighted by his stake tokens.*

---

### Open Project
**Milestone-driven, community-governed venture with transparent funding and voting.**

Core characteristics:
- **Crowdfunded** - Community contributes capital; receives stake tokens
- **Milestone-based** - Progress tracked through discrete, provable goals
- **Transparent** - All transactions, proofs, and votes visible on-chain
- **Democratic** - Community votes to approve proofs and release funds
- **Fair** - Profits/rewards distributed according to transparent rules
- **Resilient** - Can convert to community ownership if owner abandons project

Project Types:
- **Closed Project** - Single or defined owner sets rules and goals
- **Open Project** - Community-run; all goals are bounties; anyone can contribute
- **Venture-style Project** - Local, physical ventures with task bidding and profit-sharing

---

### Proof
**Immutable evidence that a goal has been achieved.**

- Linked to code commits, builds, test results, or deliverables
- Bundle includes: spec hash, trace index, AC checklist, build artifacts
- Submitted by contributors; reviewed by community
- Cannot be altered; all changes create new versions
- GitHub Oracle automatically generates some proofs from CI/CD

*Example: A developer completes a goal. The GitHub Oracle automatically creates a proof bundle showing: which commits were made, which tests passed, which acceptance criteria were met. The proof is immutable.*

---

### Proof Bundle
**Complete package of evidence linking specification to implementation.**

Contents:
- **Spec Snapshot** - Hash of the spec at time of implementation
- **Trace Index** - Mapping of each AC to code implementation and tests
- **AC Checklist** - Pass/fail status for all acceptance criteria
- **Build Artifacts** - Binaries, packages, or deployment records
- **Commit Hash** - Signed reference to code repository

Purpose:
- Transparent verification of work
- Basis for community voting
- Automatic fund release via smart contracts
- Immutable record of what was delivered

---

### Voting
**Community approval mechanism for proof validation.**

Mechanics:
- **Quorum requirement** - Minimum 30% of stake token holders must vote
- **Approval threshold** - Minimum 70% of votes must be "yes" to approve
- **Vote cost** - Voting consumes experience from the voter
- **Finality** - Once threshold reached, decision is final and binding
- **Automation** - Fund release triggers automatically on approval

Voting happens on:
- Project proof approval (did we deliver what we promised?)
- Policy changes (should we modify project rules?)
- Failover decisions (should community take over this project?)

---

### Experience System
**The mechanism for earning and spending voting power.**

Earning Experience:
- **Create value** - Start projects, complete goals, contribute to community
- **Validate work** - Vote on proofs; accurate voting earns bonus experience
- **Participate** - Engage in governance and forum discussions
- **Risk-taking** - Higher-value contributions earn more experience

Spending Experience:
- **Voting** - Cost scales with decision importance
- **Governance** - Proposing changes costs experience
- **Forum** - Posting, moderating, and reputation actions
- **Appeals** - Challenging decisions costs experience

*Design principle: Experience spending prevents spam while rewarding engaged participants.*

---

### Failover Mechanism
**Automatic transition of abandoned projects to community governance.**

Triggers:
- Project owner inactive for X period
- Project fails consecutive votes on proofs
- Community votes to initiate failover

Outcome:
- Project converts to Open Project status
- All goals become bounties
- Community takes governance role
- Original owner loses exclusive control
- Project can continue without interruption

*Purpose: Prevents project death due to owner unavailability.*

---

### Smart Contract
**Autonomous code that enforces rules without human intervention.**

In Open Systems:
- **Project Contract** - Manages project metadata and state
- **Goal Contract** - Handles funding, proofs, and voting for each goal
- **Token Contract** - Manages stake tokens (non-transferable)
- **Voting Contract** - Enforces quorum and approval thresholds
- **Failover Contract** - Triggers community takeover when needed
- **Funds Contract** - Escrows funds until proof approval

Key property: **Deterministic** - Same inputs always produce same outputs; no favoritism.

---

### Open Democracy
**Governance system where voting power is earned through contribution.**

Principles:
- **Meritocratic** - Power earned, not inherited or purchased
- **Transparent** - All votes and reasoning visible
- **Participatory** - Anyone can propose and vote
- **Accountable** - Decisions recorded immutably
- **Expressive** - Citizens express nuanced preferences, not binary votes

Components:
- Experience system (voting power)
- Expressive politics (nuanced expression)
- Local-global rulesets (distributed governance)
- Forum (debate and reasoning)
- Automation (smart contracts enforce decisions)

---

### Expressive Politics
**Governance model where citizens express nuanced preferences rather than voting yes/no.**

Mechanism:
- Citizens express opinions with parameters and weightings
- Multiple issues/policies have different expression types
- AI/Community aggregates expressions into actionable policies
- Gradient maps show geographic/demographic distribution of opinions
- Compatible expressions create natural "communities"

Example:
- Instead of "death penalty: yes or no?"
- Citizens express: "Death penalty should be allowed only for X crime, after Y appeals, with Z oversight"
- System aggregates and finds consensus where it exists
- Incompatible expressions create natural policy boundaries

---

### Open Forum
**Blockchain-backed discussion and debate layer.**

Features:
- **Immutable** - All discussions permanently recorded
- **Threaded** - Organized conversations with context
- **Traceable** - Links decisions back to reasoning
- **Referenceable** - Future policies can cite past debates
- **Information Packages** - Bundle reasoning with decisions

Purpose:
- Preserve collective reasoning
- Prevent revisionism
- Enable learning from past mistakes
- Create institutional memory

---

### Open Certification Network
**Decentralized system for ethical standards and community sanctions.**

How it works:
- Communities vote on rule sets (fairness, transparency, human rights, etc.)
- Projects adopt rule sets to signal values
- Violations can be reported and reviewed
- Community votes on sanctions (warnings, temporary suspension, permanent ban)
- Appeals process ensures fairness

Purpose:
- Maintain ethical standards
- Prevent exploitation
- Enable community moderation
- Create accountability

---

### Acceptance Criteria (AC)
**Specific, testable requirements that define when a goal is complete.**

Format:
- Unique ID (e.g., AC-PROJ-001)
- Clear description of what must be true
- Measurable conditions
- Examples when helpful

Example:
```
AC-CHAT-001: User can send a message in a public channel
- Given: User is authenticated and in a channel
- When: User types a message and hits send
- Then: Message appears in channel within 2 seconds for all members
```

Purpose:
- Clear, objective definition of "done"
- Basis for testing
- Used in proof bundles to verify completion

---

### Quorum
**Minimum participation required for a vote to be valid.**

In Open Systems:
- **30% quorum** - At least 30% of relevant stake token holders must vote
- Prevents small minorities from controlling outcomes
- Requires broad consensus

Rationale:
- Forces majority engagement
- Prevents tyranny of the few
- Ensures legitimacy

---

### Approval Threshold
**Percentage of votes required for a decision to pass.**

In Open Systems:
- **70% approval** - At least 70% of votes cast must be "yes"
- Requires supermajority, not simple majority
- Prevents close calls

Rationale:
- Ensures strong consensus
- Prevents 51% tyranny
- Guarantees broad support

---

### Product Owner (PO)
**Role responsible for defining project vision, goals, and rules.**

Responsibilities:
- Define project mission and milestones
- Set proof criteria (what counts as done?)
- Set payout/reward structure
- Manage project budget
- Answer clarifying questions from contributors

Authority:
- Define goals (but community approves proofs)
- Set rules (but community can override via governance)
- Subject to failover if abandoned project

---

### Contributor
**Role that completes work and submits proofs.**

Responsibilities:
- Deliver promised work
- Submit quality proofs showing completion
- Explain work in community forum
- Accept feedback from community

Rewards:
- Direct payment (if project allows)
- Equity share (if project allows)
- Experience (from community approval)
- Reputation

---

### Funder
**Role that provides capital to projects.**

Contributions:
- Capital investment in project goals
- Receives stake tokens proportional to investment

Voting Power:
- Votes on proof approval for funded goals
- Voting power weighted by stake tokens
- Can participate in failover decisions

Rewards:
- Return on investment (project-dependent)
- Experience (from community governance participation)

---

### Community
**Everyone who participates in voting and governance.**

Powers:
- Vote on proof approval
- Vote on failover decisions
- Participate in forum discussions
- Propose policy changes
- Challenge decisions

Responsibility:
- Vote thoughtfully and fairly
- Participate in governance
- Contribute to collective reasoning in forum
- Maintain ethical standards

---

### Blockchain
**Distributed ledger that records transactions immutably.**

In Open Systems:
- Records all funding contributions
- Records all votes
- Records all proofs
- Enables smart contracts
- Prevents falsification
- Ensures transparency

Technology:
- Ethereum Layer 2 (Optimism or Base)
- Lower gas fees than mainnet
- High throughput
- Compatible with existing tools

---

### Non-Transferable Token
**Digital asset that cannot be sold, traded, or transferred.**

Purpose:
- Ensures voting power cannot be concentrated through money
- Prevents market speculation
- Ties power to actual participation
- Prevents wealth accumulation without contribution

Examples in Open Systems:
- Stake tokens (funding votes)
- Experience (voting power)
- Reputation

---

### Decentralization
**Distribution of power and decision-making across network participants.**

In Open Systems:
- No central authority makes decisions
- Decisions made by community consensus
- No single point of failure
- Rules enforced by smart contracts, not institutions
- Data distributed across network

Benefit:
- Prevents corruption
- Ensures fairness
- Increases resilience
- Enables scale

---

### Transparency
**All actions, transactions, and reasoning are visible and traceable.**

In Open Systems:
- All funding visible on blockchain
- All votes recorded and linked to voter
- All reasoning preserved in forum
- All code and contracts auditable
- All proofs immutable

Exceptions:
- Personal privacy preserved via cryptography
- Private keys protect identity
- Pseudonymous participation allowed

---

### Emergence
**Complex behaviors arising from simple interactions.**

In Open Systems Context:
- Order emerges from decentralized decisions
- Communities coalesce around compatible values
- Rules evolve from local expressions
- Intelligence arises from diverse perspectives

Related to physics foundation that explains why intelligence emerges.

---

## System-Specific Terms

### Project-Specific

**Goal** - Discrete, fundable milestone with defined proof criteria
**Bidding** - Competing proposals for how to complete a task
**Sweat Equity** - Rewards for non-monetary contributions
**Profit Sharing** - Templates for revenue distribution
**Deposit** - Security held to ensure accountability

### Governance-Specific

**Ruleset** - Collection of policies for a community
**Local-Global Ruleset** - How local rules interact with global policies
**Gradient Map** - Visual representation of opinion distribution
**Policy** - Rule that governs behavior
**Sanction** - Consequence for violating rules

### Technical-Specific

**Smart Contract** - Self-executing agreement on blockchain
**GitHub Oracle** - Automated link between GitHub CI/CD and proofs
**Acceptance Criteria (AC)** - Testable requirement with unique ID
**Trace** - Link from acceptance criteria through code to tests
**Proof Bundle** - Package of evidence for work completion

---

## See Also

- For system overviews: `/SPECS/INDEX.md`
- For detailed specs: Individual files in `/SPECS/`
- For technical details: `/SPECS/04-technical/`
- For governance details: `/SPECS/01-governance/`
- For project details: `/SPECS/02-projects/`
