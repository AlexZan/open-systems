# Voting-Experience System v1 Specification

**Status:** Draft
**Version:** 1.0.0
**Last Updated:** 2025-01-11

## Overview

The Voting-Experience System is the foundational layer of Open Systems governance. It defines how value creation is measured, how voting power is earned and used, and how the system prevents gaming while maintaining fairness and transparency.

**Core Principle:** Value is earned through verified contribution, not wealth or status. Voting power emerges organically from transparent participation.

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Experience Creation & Transfer](#2-experience-creation--transfer)
3. [Linear Scaling Voting Power](#3-linear-scaling-voting-power)
4. [Subject-Based Experience](#4-subject-based-experience)
5. [Auditing & Verification](#5-auditing--verification)
6. [Appeals & Disputes](#6-appeals--disputes)
7. [Anti-Gaming & Security](#7-anti-gaming--security)
8. [API & Integration](#8-api--integration)
9. [Data Model & Storage](#9-data-model--storage)
10. [Implementation Notes](#10-implementation-notes)

---

## 1. Core Concepts

### 1.1 Experience

**Definition:** Experience is a non-transferable measure of verified value creation within specific subjects/domains.

**Properties:**
- **Subject-scoped:** Experience is earned in specific subjects (tags/domains)
- **Non-transferable (Phase 1):** Cannot be bought, sold, or given away
- **Audited creation:** Only created through verified value creation
- **Linear voting power:** 1 experience = 1 vote (no plutocracy)
- **Immutable history:** All creation/usage is permanently recorded

**Example:**
```
User Alice has:
- 150 experience in #programming
- 80 experience in #design
- 20 experience in #writing

Each experience point gives 1 vote in its respective subject.
```

### 1.2 Value Creation

**Definition:** An action that creates verifiable value for the community, as determined by the auditing system.

**Sources of value creation:**
1. **Contributions:** Posts, comments, code, designs, research
2. **Curation:** Quality upvotes that align with community consensus
3. **Moderation:** Accurate auditing decisions
4. **Project deliverables:** Completed goals with proof bundles

### 1.3 Voting Power

**Definition:** The ability to influence decisions within a specific subject, derived directly from experience.

**Formula:**
```
voting_power(user, subject) = experience(user, subject)
```

**No diminishing returns, no quadratic scaling, no plutocracy.**

---

## 2. Experience Creation & Transfer

### 2.1 Creation Sources

**Issue #1 Checklist Item:** Experience creation sources

Experience is created through:

#### A. Audit Approval
- User submits contribution (post, code, etc.)
- Contribution enters audit queue
- Auditors review and vote
- If approved: User earns experience in relevant subject(s)

#### B. Upvote Rewards (Verified)
- User receives upvote on contribution
- Upvote must be verified by auditors
- User earns experience proportional to upvoter's experience
- Prevents fake upvote farming

#### C. Auditor Rewards
- Auditor votes with majority consensus
- Earns +1 experience in audited subject
- Incentivizes honest auditing

#### D. Project Milestone Completion
- Contributor completes project goal
- Submits proof bundle
- Stake token holders vote (≥70% approval)
- Contributor earns experience in project subjects

### 2.2 Transfer Mechanics

**Issue #1 Checklist Item:** Transfer API and permissions

**Phase 1:** Non-transferable (Soulbound)
- Experience cannot be transferred between users
- Prevents market speculation and wealth-based power

**Phase 2:** Restricted Transfer (Future)
- Allow gifting experience for mentorship
- Require auditor approval
- Track provenance chain

**Transfer API (Phase 2):**
```typescript
interface TransferRequest {
  from: UserId;
  to: UserId;
  amount: number;
  subject: SubjectTag;
  reason: string;
  approval_required: boolean;
}

// API endpoint
POST /api/experience/transfer
{
  "to": "user_456",
  "amount": 10,
  "subject": "#programming",
  "reason": "mentorship reward"
}

// Returns
{
  "transaction_id": "tx_789",
  "status": "pending_approval",
  "approval_deadline": "2025-01-18T00:00:00Z"
}
```

### 2.3 Transaction Validation

**Issue #1 Checklist Item:** Transaction validation and atomicity

**Validation Rules:**
1. **Balance constraint:** User must have sufficient experience
2. **Subject match:** Transfer subject must match user's experience subjects
3. **Non-negative:** Cannot transfer to negative balance
4. **Atomic:** All-or-nothing transaction (no partial transfers)
5. **Immutable:** Once committed, transaction cannot be reversed (only appealed)

**Transaction Flow:**
```
1. Validate: Check balance, subject, permissions
2. Lock: Temporarily lock sender's experience
3. Record: Write transaction to blockchain/database
4. Execute: Update both balances atomically
5. Emit: Fire webhook event for integrations
6. Unlock: Release lock on success, rollback on failure
```

### 2.4 Balance Constraints

**Issue #1 Checklist Item:** Balance constraints

```typescript
interface ExperienceBalance {
  user_id: UserId;
  subject: SubjectTag;
  balance: number; // Must be >= 0
  locked: number; // Amount locked in pending operations
  available: number; // balance - locked
}

// Constraint checks
function canTransfer(user: UserId, subject: SubjectTag, amount: number): boolean {
  const balance = getBalance(user, subject);
  return balance.available >= amount;
}
```

### 2.5 Transfer History & Provenance

**Issue #1 Checklist Item:** Transfer history and provenance tracking

**Transaction Record:**
```typescript
interface ExperienceTransaction {
  id: TransactionId;
  type: 'creation' | 'transfer' | 'audit_reward' | 'penalty';
  from: UserId | null; // null for creation
  to: UserId;
  amount: number;
  subject: SubjectTag;
  source: {
    type: 'audit' | 'upvote' | 'project' | 'transfer';
    source_id: string; // audit_id, post_id, project_id, etc.
    metadata: object;
  };
  timestamp: DateTime;
  block_hash: string | null; // If on blockchain
  immutable: boolean;
}

// Query API
GET /api/experience/history?user=alice&subject=programming&limit=50

// Returns chronological list of all experience changes
```

**Provenance Chain:**
- Every experience point traceable to original creation event
- Enables reputation analysis and fraud detection
- Supports appeals with full audit trail

---

## 3. Linear Scaling Voting Power

### 3.1 Model Definition

**Issue #2: Linear scaling voting power model**

**Formula:**
```
voting_power = experience_balance
```

**No transformations, no diminishing returns.**

**Why Linear?**
1. **No plutocracy:** 100 people with 1 exp = 1 person with 100 exp
2. **Safe free transfer:** No incentive to split/merge accounts
3. **Transparent:** Easy to understand and audit
4. **Fair:** New contributors can catch up through merit

### 3.2 Voting Weight Calculation

```typescript
interface VoteWeight {
  user_id: UserId;
  subject: SubjectTag;
  weight: number; // Equal to experience balance
}

function calculateVoteWeight(user: UserId, subject: SubjectTag): number {
  const balance = getExperienceBalance(user, subject);
  return balance.available; // 1:1 mapping
}
```

### 3.3 Comparison with Other Models

**Quadratic Voting (NOT used):**
```
voting_power = sqrt(tokens)
```
- **Problem:** Incentivizes splitting accounts
- **Problem:** Wealthier users still have disproportionate power
- **Open Systems:** Rejected in favor of linear

**Reputation-Weighted (NOT used):**
```
voting_power = f(reputation, wealth, status)
```
- **Problem:** Complex, opaque, gameable
- **Open Systems:** Rejected in favor of transparent linear model

---

## 4. Subject-Based Experience

### 4.1 Subject Taxonomy

**Issue #3: Subject/hashtag taxonomy and scope**

**Definition:** Subjects are hierarchical tags that categorize contributions and experience.

**Structure:**
```
#technology
  #technology/programming
    #technology/programming/rust
    #technology/programming/python
  #technology/design
    #technology/design/ui
    #technology/design/branding
#science
  #science/physics
  #science/biology
```

**Properties:**
- **Hierarchical:** Child tags inherit parent context
- **User-created:** Anyone can propose new tags
- **Community-curated:** Popular tags persist, unused tags fade
- **Experience propagation:** Experience in child contributes to parent

**Example:**
```
Alice has 100 exp in #technology/programming/rust

When voting on #technology/programming proposals:
- Her rust experience counts: 100 votes
- She can also earn general programming experience

When voting on #technology proposals:
- Her rust experience counts partially: 50 votes (50% weight)
```

### 4.2 Subject Scope

**Scope Rules:**
1. **Specific > General:** More specific experience has higher weight in specific contexts
2. **Inheritance:** Experience in child tags partially counts for parent tags
3. **No negative inheritance:** Bad reputation in one subject doesn't affect others
4. **Cross-subject proposals:** Use weighted average of relevant subjects

**Weighting Example:**
```typescript
interface SubjectWeight {
  subject: SubjectTag;
  weight: number; // 0.0 - 1.0
}

// For a proposal tagged #technology/programming
const weights: SubjectWeight[] = [
  { subject: '#technology/programming', weight: 1.0 },
  { subject: '#technology/programming/rust', weight: 1.0 },
  { subject: '#technology/programming/python', weight: 1.0 },
  { subject: '#technology', weight: 0.5 },
  { subject: '#science', weight: 0.0 } // Irrelevant
];
```

### 4.3 Subject Creation & Governance

**Proposal Process:**
1. User proposes new subject tag
2. Provide: name, parent tag, description, examples
3. Community votes using parent subject experience
4. If approved (≥70%): Tag activated
5. If usage < threshold after 6 months: Tag deprecated

---

## 5. Auditing & Verification

**Related Issues:** #6, #7, #8, #9, #10, #11

### 5.1 Auditor Selection

**Issue #6: Auditor eligibility and selection algorithm**

**Eligibility:**
- Must have ≥10 experience in the contribution's subject
- Good standing (no recent penalties)
- Not the contribution author
- Not colluding with author (detected by pattern analysis)

**Selection Algorithm:**
```typescript
function selectAuditors(contribution: Contribution): Auditor[] {
  const subject = contribution.subject;
  const pool = getEligibleAuditors(subject);

  // Weighted random selection
  const weights = pool.map(auditor => ({
    auditor,
    weight: getExperienceBalance(auditor.id, subject)
  }));

  // Select 3-7 auditors (depends on contribution value)
  const count = Math.max(3, Math.min(7, Math.floor(contribution.value / 100)));
  return weightedRandomSample(weights, count);
}
```

**Why Random?**
- Prevents auditor shopping (gaming specific auditors)
- Distributes auditing work fairly
- Harder to collude with unknown auditors

### 5.2 Subject-Based Matching

**Issue #7: Subject-based auditor matching**

Auditors are matched to contributions based on:
1. **Primary subject:** Must have experience in main subject
2. **Related subjects:** Bonus if experience in related subjects
3. **Specialization:** Prefer deep experience over broad experience

**Matching Score:**
```typescript
function calculateAuditorMatch(auditor: Auditor, contribution: Contribution): number {
  let score = 0;

  // Primary subject experience (required)
  const primaryExp = getExperience(auditor.id, contribution.primary_subject);
  if (primaryExp < 10) return 0; // Ineligible
  score += primaryExp * 1.0;

  // Related subjects (bonus)
  contribution.related_subjects.forEach(subject => {
    const exp = getExperience(auditor.id, subject);
    score += exp * 0.3;
  });

  // Specialization bonus (deep > broad)
  const specialization = calculateSpecialization(auditor.id);
  score *= (1.0 + specialization * 0.2);

  return score;
}
```

### 5.3 Consensus Mechanisms

**Issue #8: Consensus mechanisms**

**Majority Vote:**
```
approval_ratio = approve_votes / total_votes
if approval_ratio >= 0.7:
  contribution.status = 'approved'
  author.experience += contribution_value
elif approval_ratio <= 0.3:
  contribution.status = 'rejected'
else:
  contribution.status = 'disputed' // Requires more auditors or appeal
```

**Auditor Rewards/Penalties:**

**Issue #9: Experience penalties/rewards for auditors**

```typescript
function calculateAuditorOutcome(auditor: Auditor, audit: Audit): ExperienceChange {
  const consensus = audit.consensus_vote; // 'approve' or 'reject'
  const auditorVote = auditor.vote;

  if (auditorVote === consensus) {
    // Voted with majority
    return {
      type: 'reward',
      amount: 1,
      subject: audit.subject,
      reason: 'accurate_audit'
    };
  } else {
    // Voted against majority
    const deviationCount = auditor.recent_deviations.length;
    const penalty = Math.min(5, deviationCount); // Max -5 exp

    return {
      type: 'penalty',
      amount: -penalty,
      subject: audit.subject,
      reason: 'inaccurate_audit'
    };
  }
}
```

**Why Penalties?**
- Incentivizes honest, careful review
- Prevents random voting
- Self-correcting: Bad auditors lose voting power

### 5.4 Audit Queue & Timeline

**Issue #10: Audit queue and timeline requirements**

**Queue Management:**
```typescript
interface AuditQueue {
  pending: Contribution[];
  in_progress: Contribution[];
  completed: Contribution[];

  priority_score(contribution: Contribution): number {
    // Higher value = higher priority
    let score = contribution.value;

    // Urgency bonus
    const age = now() - contribution.submitted_at;
    score += age / (24 * 60 * 60 * 1000); // +1 per day waiting

    // Author reputation bonus
    const authorExp = getTotalExperience(contribution.author);
    score += Math.log(authorExp + 1) * 10;

    return score;
  }
}
```

**Timeline Requirements:**
- **Assignment:** Within 24 hours of submission
- **Auditor response:** 7 days to review
- **Consensus:** Determined when all auditors vote OR 7 days pass
- **Timeout:** If <50% auditors respond, reassign to new auditors

**SLA Tracking:**
```typescript
interface AuditSLA {
  avg_time_to_assignment: Duration;
  avg_time_to_consensus: Duration;
  auditor_response_rate: number; // % who respond within 7 days
  appeal_rate: number; // % of audits appealed
}
```

### 5.5 Blockchain Integration

**Issue #11: Blockchain integration for immutability**

**What Goes On-Chain:**
1. **Audit decisions:** Final approve/reject with auditor signatures
2. **Experience changes:** All creation/transfer transactions
3. **Appeal outcomes:** Final resolution of disputes
4. **Subject governance:** Tag creation/deprecation votes

**What Stays Off-Chain:**
1. **Contribution content:** Too large, use content hash on-chain
2. **Audit comments:** Store in database, reference on-chain
3. **User profiles:** Mutable data, use off-chain with hash on-chain

**Smart Contract Structure:**
```solidity
contract ExperienceAudit {
  struct AuditDecision {
    bytes32 contributionHash;
    address author;
    string subject;
    uint256 experienceAwarded;
    address[] auditors;
    bool approved;
    uint256 timestamp;
  }

  mapping(bytes32 => AuditDecision) public audits;

  event AuditCompleted(
    bytes32 indexed contributionHash,
    address indexed author,
    string subject,
    uint256 experienceAwarded,
    bool approved
  );

  function recordAudit(
    bytes32 contributionHash,
    address author,
    string memory subject,
    uint256 experienceAwarded,
    address[] memory auditors,
    bool approved
  ) external onlyAuthorized {
    // Record immutable audit decision
    audits[contributionHash] = AuditDecision({
      contributionHash: contributionHash,
      author: author,
      subject: subject,
      experienceAwarded: experienceAwarded,
      auditors: auditors,
      approved: approved,
      timestamp: block.timestamp
    });

    emit AuditCompleted(contributionHash, author, subject, experienceAwarded, approved);
  }
}
```

---

## 6. Appeals & Disputes

**Related Issues:** #12, #13, #14, #15, #16, #17

### 6.1 Multi-Round Appeal Process

**Issue #12: Multi-round appeal process**

**Appeal Rounds:**
```
Round 1: Original audit (3-7 auditors)
  ↓ (if appealed)
Round 2: New auditor pool (5-9 auditors, none from Round 1)
  ↓ (if appealed again)
Round 3: Jury process (11-15 high-reputation auditors)
  ↓ (if still disputed)
Final: Emergency escalation (see 6.5)
```

**Appeal Conditions:**
- Author disagrees with rejection
- Author believes auditors were biased/colluding
- Evidence of procedural errors
- Must appeal within 7 days of decision

**Appeal Cost:**
- **Round 2:** Lock 10 experience in appeal subject
- **Round 3:** Lock 25 experience in appeal subject
- **Refunded if appeal succeeds**
- **Forfeited if appeal fails (prevents spam)**

### 6.2 Evidence Submission

**Issue #13: Evidence submission requirements**

**Appellant Must Provide:**
```typescript
interface AppealEvidence {
  appeal_reason: 'bias' | 'error' | 'collusion' | 'procedural';
  description: string; // Max 1000 chars
  supporting_evidence: {
    type: 'link' | 'document' | 'data' | 'witness';
    content: string;
    hash: string; // Content hash for verification
  }[];
  requested_outcome: 'reaudit' | 'overturn' | 'penalty';
}
```

**Evidence Review:**
- New auditors review original decision + appeal evidence
- Cannot see original auditor identities (prevent bias)
- Must provide written justification for decision

### 6.3 New Auditor Pool Selection

**Issue #14: New auditor pool selection for appeals**

**Pool Constraints:**
- **No overlap:** Cannot include original auditors
- **Higher experience:** Require 2x minimum experience threshold
- **Geographic diversity:** (Future) Select from different regions
- **No social connections:** (Future) Use social graph analysis

```typescript
function selectAppealAuditors(
  original_auditors: Auditor[],
  subject: SubjectTag,
  round: number
): Auditor[] {
  const pool = getEligibleAuditors(subject)
    .filter(a => !original_auditors.includes(a))
    .filter(a => getExperience(a.id, subject) >= MIN_EXP * 2);

  const count = 3 + (round * 2); // More auditors each round
  return weightedRandomSample(pool, count);
}
```

### 6.4 Jury Process for Small User Bases

**Issue #15: Jury process for small user bases**

**Problem:** New communities may not have enough auditors for multi-round appeals.

**Solution: Jury Boosting**
```typescript
interface JuryConfig {
  min_local_auditors: number; // Try to use 60% local
  cross_subject_allowed: boolean; // Can jury from related subjects?
  external_jury_allowed: boolean; // Can jury from other communities?
  reputation_threshold: number; // Minimum experience required
}

function selectJury(appeal: Appeal, config: JuryConfig): Auditor[] {
  let jury: Auditor[] = [];

  // Phase 1: Local auditors
  const local = selectLocalAuditors(appeal.subject, 7);
  jury.push(...local);

  // Phase 2: Cross-subject (if needed)
  if (jury.length < config.min_local_auditors && config.cross_subject_allowed) {
    const related = selectRelatedSubjectAuditors(appeal.subject, 3);
    jury.push(...related);
  }

  // Phase 3: External jury (if needed)
  if (jury.length < 5 && config.external_jury_allowed) {
    const external = selectExternalJury(appeal, 5 - jury.length);
    jury.push(...external);
  }

  return jury;
}
```

**External Jury:**
- High-reputation auditors from other subjects
- Must review subject documentation before voting
- Receive bonus experience if decision is upheld

### 6.5 Emergency Appeal Mechanisms

**Issue #16: Emergency appeal mechanisms**

**Triggers:**
- Round 3 jury still split (40-60% vote)
- Evidence of systemic corruption
- Technical failure in audit process
- Legal/safety concerns

**Emergency Escalation:**
```typescript
interface EmergencyAppeal {
  case_id: string;
  escalation_reason: 'deadlock' | 'corruption' | 'technical' | 'legal';
  previous_rounds: AuditRound[];
  evidence: AppealEvidence;

  // Emergency jury
  jury_type: 'founder' | 'council' | 'random_global';
}
```

**Emergency Jury Types:**
1. **Founder jury (Phase 1):** Project founders make final call
2. **Council jury (Phase 2):** Elected council of high-rep users
3. **Random global jury (Phase 3):** Truly random sample from all users

**Emergency Decision is Final:**
- Cannot be appealed further
- Becomes precedent for similar cases
- Published with full reasoning

### 6.6 Decision Finality & Escalation Paths

**Issue #17: Decision finality and escalation paths**

**Finality Conditions:**
```
Round 1: Final if ≥90% consensus (not appealable)
Round 2: Final if ≥80% consensus
Round 3: Final if ≥70% consensus
Emergency: Always final
```

**Escalation Path:**
```
Author submits contribution
  ↓
Round 1 audit (3-7 auditors)
  ↓ < 90% consensus → Appeal within 7 days
Round 2 audit (5-9 new auditors)
  ↓ < 80% consensus → Appeal within 7 days
Round 3 jury (11-15 high-rep auditors)
  ↓ < 70% consensus → Emergency escalation
Emergency jury → FINAL DECISION
```

**No Further Appeals After:**
- Emergency decision
- Author fails to appeal within 7 days
- Author cannot lock required experience for appeal
- Round 3 reaches ≥70% consensus

---

## 7. Anti-Gaming & Security

**Related Issues:** #18, #19, #20, #21, #22, #23

### 7.1 Sybil Resistance

**Issue #18: Sybil resistance through verification layer**

**Problem:** Users create multiple fake accounts to gain more voting power.

**Defenses:**

**A. Verification Layer**
```typescript
interface UserVerification {
  user_id: UserId;
  verification_level: 'unverified' | 'email' | 'phone' | 'kyc' | 'web3';
  verification_methods: VerificationMethod[];
  trust_score: number; // 0-100
}

const EXPERIENCE_CAPS = {
  unverified: 10, // Can earn max 10 exp before verification
  email: 50,
  phone: 200,
  kyc: 1000,
  web3: Infinity // Decentralized identity
};
```

**B. Social Graph Analysis**
```typescript
function detectSybilCluster(users: UserId[]): boolean {
  // Check for suspicious patterns:
  // - Created at same time
  // - Always vote together
  // - Same IP addresses
  // - Circular upvoting
  // - Shared wallet addresses

  const suspicionScore = calculateSuspicion(users);
  return suspicionScore > THRESHOLD;
}
```

**C. Proof of Humanity (Phase 2)**
- Integration with Proof of Humanity registry
- Biometric verification (optional)
- Social vouching (users vouch for each other)

### 7.2 Collusion Detection

**Issue #19: Collusion detection (fake upvote pairs)**

**Detection Patterns:**
```typescript
interface CollusionPattern {
  type: 'circular' | 'reciprocal' | 'coordinated' | 'farm';
  users: UserId[];
  confidence: number; // 0-1
  evidence: {
    vote_correlation: number; // How often they vote together
    timing_correlation: number; // How quickly they vote after each other
    content_similarity: number; // Are they upvoting low-quality content?
    network_distance: number; // Social graph distance
  };
}

function detectCollusion(votes: Vote[]): CollusionPattern[] {
  const patterns: CollusionPattern[] = [];

  // Check for circular upvoting
  const circular = findCircularVoting(votes);
  if (circular.length > 0) {
    patterns.push({
      type: 'circular',
      users: circular,
      confidence: 0.9,
      evidence: { /* ... */ }
    });
  }

  // Check for reciprocal upvoting (A always upvotes B, B always upvotes A)
  const reciprocal = findReciprocalVoting(votes);
  // ... more checks

  return patterns;
}
```

**Penalties for Collusion:**
```typescript
function penalizeCollusion(pattern: CollusionPattern) {
  pattern.users.forEach(user => {
    // Revoke ill-gotten experience
    revokeExperience(user, pattern.evidence.amount);

    // Temporary audit suspension
    suspendFromAuditing(user, duration = 30 * DAYS);

    // Flag for manual review
    flagForReview(user, pattern);
  });
}
```

### 7.3 Gaming Penalty Framework

**Issue #20: Gaming penalty framework**

**Penalty Tiers:**
```typescript
enum GamingViolation {
  MINOR_SPAM = 'minor_spam', // -5 exp
  FAKE_UPVOTES = 'fake_upvotes', // -20 exp + suspension
  SYBIL_ATTACK = 'sybil_attack', // Ban all accounts
  AUDIT_MANIPULATION = 'audit_manipulation', // -50 exp + permanent audit ban
  COLLUSION = 'collusion', // Revoke all related experience
}

interface Penalty {
  user_id: UserId;
  violation: GamingViolation;
  experience_penalty: number;
  suspension_days: number;
  permanent_bans: string[]; // e.g., ['auditing', 'project_creation']
  appeal_allowed: boolean;
}

function applyPenalty(user: UserId, violation: GamingViolation): Penalty {
  const penalty = PENALTY_RULES[violation];

  // Apply experience penalty
  deductExperience(user, penalty.amount, reason = violation);

  // Apply suspensions
  if (penalty.suspension_days > 0) {
    suspendUser(user, penalty.suspension_days);
  }

  // Apply permanent bans
  penalty.permanent_bans.forEach(action => {
    permanentlyBan(user, action);
  });

  // Log immutably
  recordPenalty(user, penalty);

  return penalty;
}
```

**Escalating Penalties:**
- First offense: Warning + small penalty
- Second offense: Larger penalty + suspension
- Third offense: Account suspension
- Fourth offense: Permanent ban

### 7.4 Vote Revocation for False Validation

**Issue #21: Vote revocation for false validation**

**Scenario:** Auditor approves low-quality contribution, community appeals, appeal succeeds.

**Consequences:**
```typescript
function revokeApproval(audit: Audit, appeal_decision: AppealDecision) {
  // 1. Revoke experience from author
  revokeExperience(
    audit.author,
    audit.experience_awarded,
    reason = 'overturned_on_appeal'
  );

  // 2. Penalize approving auditors
  audit.auditors.filter(a => a.vote === 'approve').forEach(auditor => {
    deductExperience(auditor.id, 5, reason = 'false_approval');
    recordIncorrectAudit(auditor.id);
  });

  // 3. Reward appeal auditors
  appeal_decision.auditors.forEach(auditor => {
    awardExperience(auditor.id, 2, reason = 'successful_appeal');
  });

  // 4. Update contribution status
  audit.contribution.status = 'rejected';
  audit.contribution.appeal_outcome = 'overturned';
}
```

**Prevention of Abuse:**
- Revocation requires strong consensus (≥80% in appeal)
- Original auditors can defend their decision
- Repeated revocations trigger investigation of appellant (spam appeals)

### 7.5 Proof of Value Creation

**Issue #22: Proof of value creation requirements**

**Types of Proof:**

**A. Contribution Proof**
```typescript
interface ContributionProof {
  type: 'post' | 'code' | 'design' | 'research';
  content_hash: string; // Immutable content reference
  metadata: {
    lines_of_code?: number;
    word_count?: number;
    file_sizes?: number[];
    external_links?: string[];
  };
  validation: {
    plagiarism_check: boolean;
    originality_score: number; // 0-1
    quality_metrics: object;
  };
}
```

**B. Project Deliverable Proof**
```typescript
interface ProofBundle {
  goal_id: GoalId;
  deliverables: {
    type: 'code' | 'document' | 'design' | 'binary';
    artifact_hash: string;
    artifact_url: string;
    sbom?: SBOM; // Software Bill of Materials
  }[];
  acceptance_criteria: {
    criterion_id: string;
    status: 'pass' | 'fail';
    evidence: string;
  }[];
  build_verification: {
    build_logs: string;
    test_results: string;
    coverage_report?: string;
  };
}
```

**C. Upvote Proof**
```typescript
interface UpvoteProof {
  contribution_id: ContributionId;
  upvoter_id: UserId;
  upvoter_experience: number; // At time of upvote
  upvote_reason?: string; // Optional justification
  verified: boolean; // Has auditor confirmed upvote is legitimate?
}
```

**Proof Validation:**
- Content hash must match stored content
- Plagiarism check must pass (≥80% original)
- External links must be accessible and relevant
- Build verification must succeed (for code)
- Auditors validate all proofs before awarding experience

### 7.6 Attack Vectors & Mitigations

**Issue #23: Attack vectors and mitigations**

| Attack | Description | Mitigation |
|--------|-------------|------------|
| **Sybil Attack** | Create multiple fake accounts | Verification caps, social graph analysis, Proof of Humanity |
| **Collusion** | Coordinate to upvote each other | Pattern detection, vote correlation analysis, penalties |
| **Vote Buying** | Pay others to vote a certain way | Non-transferable experience (Phase 1), audit trails |
| **Spam Submissions** | Submit low-quality contributions for experience | Audit queue, auditor penalties, spam detection |
| **Auditor Bribery** | Bribe auditors to approve | Random selection, stake requirements, immutable records |
| **Appeal Spam** | Appeal every rejection to slow system | Appeal cost (locked experience), escalating fees |
| **Whale Dominance** | High-exp users control decisions | Linear voting (prevents plutocracy), subject-scoped experience |
| **Experience Farming** | Game system to accumulate experience | Proof of value, auditor verification, pattern detection |
| **Content Plagiarism** | Submit others' work as own | Plagiarism detection, content hashing, provenance tracking |
| **Sockpuppet Defense** | Use fake accounts to defend decision | Social graph analysis, IP tracking, timing analysis |

**Defense-in-Depth Strategy:**
1. **Prevention:** Verification, proof requirements, random selection
2. **Detection:** Pattern analysis, anomaly detection, community reporting
3. **Response:** Penalties, suspensions, experience revocation
4. **Recovery:** Appeals process, manual review, precedent setting

---

## 8. API & Integration

**Related Issues:** #24, #25, #26, #27, #28, #29

### 8.1 REST API Endpoints

**Issue #24: REST API endpoints specification**

**Base URL:** `https://api.opensystems.io/v1`

#### Experience Endpoints

```typescript
// Get user experience balance
GET /experience/:userId
Response: {
  user_id: string;
  balances: {
    subject: string;
    balance: number;
    locked: number;
    rank: number; // Rank among users in this subject
  }[];
  total_experience: number;
}

// Get experience history
GET /experience/:userId/history?subject=&limit=&offset=
Response: {
  transactions: ExperienceTransaction[];
  total_count: number;
  has_more: boolean;
}

// Transfer experience (Phase 2)
POST /experience/transfer
Body: TransferRequest
Response: {
  transaction_id: string;
  status: 'pending' | 'approved' | 'rejected';
}
```

#### Contribution Endpoints

```typescript
// Submit contribution for audit
POST /contributions
Body: {
  title: string;
  content: string;
  subject: string;
  related_subjects?: string[];
  proof: ContributionProof;
}
Response: {
  contribution_id: string;
  status: 'pending_audit';
  estimated_audit_time: number; // seconds
}

// Get contribution status
GET /contributions/:contributionId
Response: {
  contribution_id: string;
  status: 'pending' | 'auditing' | 'approved' | 'rejected' | 'appealed';
  audit: {
    auditors: number; // Count, not identities
    votes: { approve: number; reject: number };
    consensus: number; // 0-1
    estimated_completion: DateTime;
  };
}
```

#### Audit Endpoints

```typescript
// Get assigned audits (for auditors)
GET /audits/assigned
Response: {
  audits: {
    audit_id: string;
    contribution_id: string;
    subject: string;
    submitted_at: DateTime;
    deadline: DateTime;
    content_preview: string; // First 200 chars
  }[];
}

// Submit audit vote
POST /audits/:auditId/vote
Body: {
  vote: 'approve' | 'reject';
  reason?: string;
  confidence: number; // 0-1
}
Response: {
  audit_id: string;
  your_vote: 'approve' | 'reject';
  consensus_reached: boolean;
}
```

#### Appeal Endpoints

```typescript
// Submit appeal
POST /appeals
Body: {
  contribution_id: string;
  evidence: AppealEvidence;
  locked_experience: number; // Must match appeal round requirement
}
Response: {
  appeal_id: string;
  round: number;
  new_auditors_count: number;
  estimated_decision: DateTime;
}

// Get appeal status
GET /appeals/:appealId
Response: {
  appeal_id: string;
  round: number;
  status: 'pending' | 'in_review' | 'decided';
  outcome?: 'upheld' | 'overturned';
  locked_experience_returned: boolean;
}
```

### 8.2 Webhook/Event System

**Issue #25: Webhook/event system for integrations**

**Event Types:**
```typescript
enum EventType {
  EXPERIENCE_CREATED = 'experience.created',
  EXPERIENCE_TRANSFERRED = 'experience.transferred',
  CONTRIBUTION_SUBMITTED = 'contribution.submitted',
  AUDIT_ASSIGNED = 'audit.assigned',
  AUDIT_COMPLETED = 'audit.completed',
  APPEAL_SUBMITTED = 'appeal.submitted',
  APPEAL_DECIDED = 'appeal.decided',
  PENALTY_APPLIED = 'penalty.applied',
  SUBJECT_CREATED = 'subject.created',
}

interface WebhookEvent {
  event_id: string;
  event_type: EventType;
  timestamp: DateTime;
  data: object; // Event-specific payload
  signature: string; // HMAC signature for verification
}
```

**Webhook Registration:**
```typescript
POST /webhooks
Body: {
  url: string;
  events: EventType[];
  secret: string; // For signature verification
  active: boolean;
}
Response: {
  webhook_id: string;
  url: string;
  events: EventType[];
  created_at: DateTime;
}

// Example event payload
{
  "event_id": "evt_123",
  "event_type": "audit.completed",
  "timestamp": "2025-01-11T12:00:00Z",
  "data": {
    "contribution_id": "contrib_456",
    "author_id": "user_789",
    "subject": "#programming",
    "decision": "approved",
    "experience_awarded": 50,
    "consensus": 0.85
  },
  "signature": "sha256=abc123..."
}
```

**Webhook Delivery:**
- Retry up to 3 times with exponential backoff
- Timeout after 10 seconds
- Log all delivery attempts
- Deactivate webhook after 10 consecutive failures

### 8.3 Authentication & Authorization

**Issue #26: Authentication & authorization model**

**Authentication Methods:**

**A. API Keys (Server-to-Server)**
```typescript
POST /auth/api-keys
Headers: {
  Authorization: Bearer <user_jwt>
}
Body: {
  name: string;
  scopes: string[]; // e.g., ['read:experience', 'write:contributions']
  expires_at?: DateTime;
}
Response: {
  api_key: string; // Only shown once
  key_id: string;
  scopes: string[];
}

// Usage
GET /experience/:userId
Headers: {
  X-API-Key: os_key_abc123...
}
```

**B. JWT (User Authentication)**
```typescript
POST /auth/login
Body: {
  method: 'wallet' | 'email' | 'passkey';
  credentials: object;
}
Response: {
  access_token: string; // JWT, expires in 1 hour
  refresh_token: string; // Expires in 30 days
  user_id: string;
}

// JWT payload
{
  "sub": "user_123",
  "iat": 1704988800,
  "exp": 1704992400,
  "scopes": ["read:own", "write:own", "audit:assigned"]
}
```

**C. Wallet Signature (Web3)**
```typescript
POST /auth/challenge
Body: {
  wallet_address: string;
}
Response: {
  challenge: string; // Random nonce
  message: string; // Formatted message to sign
}

POST /auth/verify
Body: {
  wallet_address: string;
  signature: string;
  challenge: string;
}
Response: {
  access_token: string;
  user_id: string;
}
```

**Authorization Scopes:**
```typescript
const SCOPES = {
  // Read scopes
  'read:own': 'Read own experience and contributions',
  'read:any': 'Read any user experience (public data)',
  'read:audits': 'Read assigned audits',

  // Write scopes
  'write:contributions': 'Submit contributions',
  'write:audits': 'Submit audit votes',
  'write:appeals': 'Submit appeals',

  // Transfer scopes (Phase 2)
  'transfer:experience': 'Transfer experience to others',

  // Admin scopes
  'admin:penalties': 'Apply penalties',
  'admin:subjects': 'Manage subject taxonomy',
};
```

### 8.4 Rate Limiting & Abuse Prevention

**Issue #27: Rate limiting and abuse prevention**

**Rate Limits:**
```typescript
const RATE_LIMITS = {
  // Public endpoints (no auth)
  'public': {
    requests_per_minute: 60,
    requests_per_hour: 1000,
  },

  // Authenticated users
  'user': {
    requests_per_minute: 300,
    requests_per_hour: 10000,

    // Specific actions
    'POST /contributions': { per_day: 20 },
    'POST /appeals': { per_week: 5 },
    'POST /audits/:id/vote': { per_day: 50 },
  },

  // API keys
  'api_key': {
    requests_per_minute: 600,
    requests_per_hour: 50000,
  },
};

// Rate limit headers in response
Headers: {
  'X-RateLimit-Limit': '300',
  'X-RateLimit-Remaining': '287',
  'X-RateLimit-Reset': '1704992400',
}

// 429 Too Many Requests
Response: {
  error: 'rate_limit_exceeded',
  message: 'You have exceeded the rate limit',
  retry_after: 42, // seconds
}
```

**Abuse Detection:**
```typescript
interface AbusePattern {
  type: 'spam' | 'scraping' | 'bruteforce' | 'dos';
  severity: 'low' | 'medium' | 'high';
  action: 'warn' | 'throttle' | 'block';
}

function detectAbuse(user: UserId, requests: Request[]): AbusePattern | null {
  // Check for spam patterns
  if (detectSpamSubmissions(requests)) {
    return { type: 'spam', severity: 'medium', action: 'throttle' };
  }

  // Check for scraping patterns
  if (detectScraping(requests)) {
    return { type: 'scraping', severity: 'low', action: 'warn' };
  }

  // Check for brute force
  if (detectBruteForce(requests)) {
    return { type: 'bruteforce', severity: 'high', action: 'block' };
  }

  return null;
}
```

### 8.5 Example Integrations

**Issue #28: Example integrations**

**A. Forum Integration**
```typescript
// When user posts in forum
async function onForumPost(post: ForumPost) {
  // Submit to Open Systems for audit
  const contribution = await opensystems.contributions.create({
    title: post.title,
    content: post.content,
    subject: post.category,
    proof: {
      type: 'post',
      content_hash: hash(post.content),
      metadata: { word_count: post.word_count },
    },
  });

  // Listen for audit completion
  opensystems.webhooks.on('audit.completed', async (event) => {
    if (event.data.contribution_id === contribution.id) {
      if (event.data.decision === 'approved') {
        // Update forum post with badge
        await forum.posts.update(post.id, {
          badges: [...post.badges, 'verified'],
          experience_earned: event.data.experience_awarded,
        });
      }
    }
  });
}
```

**B. GitHub Integration**
```typescript
// When PR is merged
async function onPRMerged(pr: PullRequest) {
  // Submit code contribution
  const contribution = await opensystems.contributions.create({
    title: pr.title,
    content: pr.description,
    subject: '#programming',
    related_subjects: pr.labels.map(l => `#${l}`),
    proof: {
      type: 'code',
      content_hash: pr.merge_commit_sha,
      metadata: {
        lines_of_code: pr.additions + pr.deletions,
        files_changed: pr.changed_files,
      },
      validation: {
        build_status: pr.checks.conclusion,
        test_results: pr.checks.test_results,
      },
    },
  });

  // Award experience when audited
  opensystems.webhooks.on('audit.completed', async (event) => {
    if (event.data.contribution_id === contribution.id && event.data.decision === 'approved') {
      await github.issues.createComment({
        owner: pr.base.repo.owner.login,
        repo: pr.base.repo.name,
        issue_number: pr.number,
        body: `✅ This contribution has been verified and earned ${event.data.experience_awarded} experience in ${event.data.subject}!`,
      });
    }
  });
}
```

**C. Discord Bot Integration**
```typescript
// Discord bot commands
bot.command('experience', async (interaction) => {
  const userId = interaction.user.id;
  const linkedAccount = await getLinkedAccount(userId);

  if (!linkedAccount) {
    return interaction.reply('Please link your Open Systems account with `/link`');
  }

  const experience = await opensystems.experience.get(linkedAccount.opensystems_id);

  const embed = new Discord.MessageEmbed()
    .setTitle(`${interaction.user.username}'s Experience`)
    .setDescription(experience.balances.map(b =>
      `**${b.subject}**: ${b.balance} exp (Rank #${b.rank})`
    ).join('\n'))
    .setFooter(`Total: ${experience.total_experience} experience`);

  return interaction.reply({ embeds: [embed] });
});
```

### 8.6 SDK/Client Library Design

**Issue #29: SDK/client library design**

**TypeScript SDK:**
```typescript
import { OpenSystems } from '@opensystems/sdk';

// Initialize
const client = new OpenSystems({
  apiKey: process.env.OPENSYSTEMS_API_KEY,
  environment: 'production', // or 'sandbox'
});

// Experience operations
const balance = await client.experience.get('user_123');
const history = await client.experience.history('user_123', {
  subject: '#programming',
  limit: 50,
});

// Contribution operations
const contribution = await client.contributions.create({
  title: 'How to implement RAG',
  content: '...',
  subject: '#programming',
  proof: { /* ... */ },
});

// Real-time events
client.on('audit.completed', (event) => {
  console.log('Audit completed:', event.data);
});

// Error handling
try {
  await client.contributions.create(/* ... */);
} catch (error) {
  if (error instanceof RateLimitError) {
    console.log(`Rate limited. Retry after ${error.retryAfter} seconds`);
  }
}
```

**Python SDK:**
```python
from opensystems import OpenSystems

client = OpenSystems(api_key=os.environ['OPENSYSTEMS_API_KEY'])

# Get experience
balance = client.experience.get('user_123')
print(f"Total experience: {balance.total_experience}")

# Submit contribution
contribution = client.contributions.create(
    title='Machine Learning Tutorial',
    content='...',
    subject='#ai',
    proof={'type': 'post', ...}
)

# Wait for audit (blocking)
result = client.audits.wait_for_decision(contribution.id, timeout=3600)
if result.decision == 'approved':
    print(f"Earned {result.experience_awarded} experience!")
```

**REST Client (Generic)**
```bash
# Get experience
curl https://api.opensystems.io/v1/experience/user_123 \
  -H "X-API-Key: os_key_..."

# Submit contribution
curl -X POST https://api.opensystems.io/v1/contributions \
  -H "X-API-Key: os_key_..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tutorial",
    "content": "...",
    "subject": "#programming",
    "proof": { ... }
  }'
```

---

## 9. Data Model & Storage

**Related Issues:** #30, #31, #32, #33, #34

### 9.1 Database Schema

**Issue #30: Database schema design**

**Users Table:**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  wallet_address TEXT UNIQUE,
  email TEXT UNIQUE,
  username TEXT UNIQUE NOT NULL,
  verification_level TEXT NOT NULL DEFAULT 'unverified',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_wallet ON users(wallet_address);
CREATE INDEX idx_users_email ON users(email);
```

**Experience Balances Table:**
```sql
CREATE TABLE experience_balances (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  subject TEXT NOT NULL,
  balance BIGINT NOT NULL DEFAULT 0 CHECK (balance >= 0),
  locked BIGINT NOT NULL DEFAULT 0 CHECK (locked >= 0),

  UNIQUE(user_id, subject)
);

CREATE INDEX idx_experience_user ON experience_balances(user_id);
CREATE INDEX idx_experience_subject ON experience_balances(subject);
CREATE INDEX idx_experience_balance ON experience_balances(balance DESC);

-- View for available balance
CREATE VIEW experience_available AS
SELECT
  user_id,
  subject,
  balance,
  locked,
  (balance - locked) AS available
FROM experience_balances;
```

**Experience Transactions Table:**
```sql
CREATE TABLE experience_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  transaction_type TEXT NOT NULL, -- 'creation', 'transfer', 'penalty', 'reward'
  from_user_id UUID REFERENCES users(id), -- NULL for creation
  to_user_id UUID NOT NULL REFERENCES users(id),
  amount BIGINT NOT NULL,
  subject TEXT NOT NULL,
  source_type TEXT NOT NULL, -- 'audit', 'upvote', 'project', 'transfer'
  source_id TEXT NOT NULL, -- Reference to source entity
  metadata JSONB,
  block_hash TEXT, -- If on blockchain
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_transactions_from ON experience_transactions(from_user_id);
CREATE INDEX idx_transactions_to ON experience_transactions(to_user_id);
CREATE INDEX idx_transactions_subject ON experience_transactions(subject);
CREATE INDEX idx_transactions_created ON experience_transactions(created_at DESC);
CREATE INDEX idx_transactions_source ON experience_transactions(source_type, source_id);
```

**Contributions Table:**
```sql
CREATE TABLE contributions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id UUID NOT NULL REFERENCES users(id),
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  content_hash TEXT NOT NULL UNIQUE,
  primary_subject TEXT NOT NULL,
  related_subjects TEXT[],
  proof JSONB NOT NULL, -- ContributionProof
  status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'auditing', 'approved', 'rejected', 'appealed'
  experience_value INTEGER, -- Determined after audit
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_contributions_author ON contributions(author_id);
CREATE INDEX idx_contributions_status ON contributions(status);
CREATE INDEX idx_contributions_subject ON contributions(primary_subject);
CREATE INDEX idx_contributions_created ON contributions(created_at DESC);
```

**Audits Table:**
```sql
CREATE TABLE audits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contribution_id UUID NOT NULL REFERENCES contributions(id),
  round INTEGER NOT NULL DEFAULT 1, -- Appeal round
  status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'in_progress', 'completed'
  consensus_decision TEXT, -- 'approved', 'rejected', NULL if no consensus
  consensus_ratio FLOAT, -- 0-1
  experience_awarded INTEGER, -- Final amount if approved
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

  UNIQUE(contribution_id, round)
);

CREATE INDEX idx_audits_contribution ON audits(contribution_id);
CREATE INDEX idx_audits_status ON audits(status);
```

**Audit Assignments Table:**
```sql
CREATE TABLE audit_assignments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  audit_id UUID NOT NULL REFERENCES audits(id),
  auditor_id UUID NOT NULL REFERENCES users(id),
  vote TEXT, -- 'approve', 'reject', NULL if not yet voted
  reason TEXT,
  confidence FLOAT, -- 0-1
  voted_at TIMESTAMPTZ,
  assigned_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  deadline TIMESTAMPTZ NOT NULL,

  UNIQUE(audit_id, auditor_id)
);

CREATE INDEX idx_assignments_audit ON audit_assignments(audit_id);
CREATE INDEX idx_assignments_auditor ON audit_assignments(auditor_id);
CREATE INDEX idx_assignments_status ON audit_assignments(vote) WHERE vote IS NULL;
```

**Appeals Table:**
```sql
CREATE TABLE appeals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contribution_id UUID NOT NULL REFERENCES contributions(id),
  appellant_id UUID NOT NULL REFERENCES users(id),
  previous_audit_id UUID NOT NULL REFERENCES audits(id),
  round INTEGER NOT NULL, -- 2, 3, or 4 (emergency)
  reason TEXT NOT NULL,
  evidence JSONB NOT NULL, -- AppealEvidence
  locked_experience INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'in_review', 'decided'
  outcome TEXT, -- 'upheld', 'overturned'
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  decided_at TIMESTAMPTZ
);

CREATE INDEX idx_appeals_contribution ON appeals(contribution_id);
CREATE INDEX idx_appeals_appellant ON appeals(appellant_id);
CREATE INDEX idx_appeals_status ON appeals(status);
```

**Subjects Table:**
```sql
CREATE TABLE subjects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tag TEXT NOT NULL UNIQUE, -- e.g., '#programming'
  parent_tag TEXT REFERENCES subjects(tag),
  name TEXT NOT NULL,
  description TEXT,
  total_users INTEGER NOT NULL DEFAULT 0,
  total_experience BIGINT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  deprecated_at TIMESTAMPTZ
);

CREATE INDEX idx_subjects_tag ON subjects(tag);
CREATE INDEX idx_subjects_parent ON subjects(parent_tag);
CREATE INDEX idx_subjects_active ON subjects(deprecated_at) WHERE deprecated_at IS NULL;
```

**Penalties Table:**
```sql
CREATE TABLE penalties (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  violation_type TEXT NOT NULL,
  experience_penalty INTEGER NOT NULL,
  suspension_until TIMESTAMPTZ,
  permanent_bans TEXT[], -- ['auditing', 'project_creation']
  evidence JSONB NOT NULL,
  appeal_id UUID REFERENCES appeals(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_penalties_user ON penalties(user_id);
CREATE INDEX idx_penalties_violation ON penalties(violation_type);
CREATE INDEX idx_penalties_created ON penalties(created_at DESC);
```

### 9.2 Blockchain vs Off-Chain Storage

**Issue #31: Blockchain vs off-chain storage decisions**

| Data Type | Storage | Rationale |
|-----------|---------|-----------|
| **Experience balances** | Blockchain | Immutable, trustless verification |
| **Experience transactions** | Blockchain | Permanent audit trail, provenance |
| **Audit decisions** | Blockchain | Tamper-proof, transparency |
| **Subject definitions** | Blockchain | Community consensus, permanence |
| **Contribution content** | Off-chain (IPFS/DB) | Too large for blockchain |
| **Contribution hashes** | Blockchain | Content integrity verification |
| **User profiles** | Off-chain (DB) | Mutable, personal data |
| **Audit comments** | Off-chain (DB) | Large text, searchable |
| **Vote reasoning** | Off-chain (DB) | Large text, optional |
| **Appeal evidence** | Off-chain (IPFS) + hash on-chain | Large files, integrity check |

**Hybrid Storage Pattern:**
```typescript
// Off-chain: Full contribution
database.contributions.insert({
  id: 'contrib_123',
  author: 'user_456',
  content: '... 5000 words ...',
  // ... other fields
});

// On-chain: Hash + decision
blockchain.recordAudit({
  contributionHash: sha256(contribution.content),
  author: contribution.author,
  subject: contribution.subject,
  approved: true,
  experienceAwarded: 50,
  auditors: ['0x123...', '0x456...'],
  timestamp: Date.now()
});

// Verification: Anyone can verify integrity
const stored = database.contributions.get('contrib_123');
const hash = sha256(stored.content);
const onChain = blockchain.getAudit('contrib_123');
assert(hash === onChain.contributionHash); // Integrity verified
```

**Blockchain Cost Optimization:**
- Batch audit decisions (record 10-100 at once)
- Use Layer 2 (Optimism, Base) for lower fees
- Compress data with zk-rollups (Phase 3)
- Periodic checkpoints to mainnet

### 9.3 Indexing Strategy

**Issue #32: Indexing strategy for performance**

**Critical Indexes:**
```sql
-- User experience leaderboards
CREATE INDEX idx_exp_leaderboard
ON experience_balances(subject, balance DESC);

-- User's recent activity
CREATE INDEX idx_user_activity
ON experience_transactions(to_user_id, created_at DESC);

-- Pending audits for auditor
CREATE INDEX idx_auditor_queue
ON audit_assignments(auditor_id, assigned_at DESC)
WHERE vote IS NULL;

-- Contribution search
CREATE INDEX idx_contribution_search
ON contributions USING GIN(to_tsvector('english', title || ' ' || content));

-- Recent contributions by subject
CREATE INDEX idx_contributions_recent
ON contributions(primary_subject, created_at DESC)
WHERE status = 'approved';
```

**Composite Indexes:**
```sql
-- Appeals by user and status
CREATE INDEX idx_user_appeals
ON appeals(appellant_id, status, created_at DESC);

-- Audit assignments by subject and deadline
CREATE INDEX idx_audits_subject_deadline
ON audits(primary_subject, deadline)
WHERE status = 'pending';
```

**Partial Indexes (Space Optimization):**
```sql
-- Only index active contributions
CREATE INDEX idx_active_contributions
ON contributions(created_at DESC)
WHERE status IN ('pending', 'auditing');

-- Only index pending audits
CREATE INDEX idx_pending_audits
ON audits(created_at)
WHERE status = 'pending';
```

**Query Performance Targets:**
- Experience balance lookup: <10ms
- Transaction history (50 items): <50ms
- Leaderboard (top 100): <100ms
- Audit queue: <50ms
- Full-text search: <200ms

### 9.4 Audit Trail & Provenance

**Issue #33: Audit trail and provenance tracking**

**Immutable Event Log:**
```sql
CREATE TABLE event_log (
  id BIGSERIAL PRIMARY KEY,
  event_type TEXT NOT NULL,
  entity_type TEXT NOT NULL, -- 'contribution', 'audit', 'appeal', 'transaction'
  entity_id UUID NOT NULL,
  actor_id UUID REFERENCES users(id),
  action TEXT NOT NULL, -- 'created', 'updated', 'deleted', 'approved', etc.
  before_state JSONB,
  after_state JSONB,
  metadata JSONB,
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- This table is append-only, never updated or deleted
CREATE INDEX idx_event_log_entity ON event_log(entity_type, entity_id);
CREATE INDEX idx_event_log_actor ON event_log(actor_id);
CREATE INDEX idx_event_log_created ON event_log(created_at DESC);

-- Prevent updates and deletes
CREATE RULE event_log_no_update AS
ON UPDATE TO event_log DO INSTEAD NOTHING;

CREATE RULE event_log_no_delete AS
ON DELETE TO event_log DO INSTEAD NOTHING;
```

**Provenance Tracking:**
```typescript
// Trace experience back to original creation
async function traceExperienceProvenance(
  userId: UserId,
  subject: SubjectTag,
  amount: number
): Promise<ProvenanceChain> {
  const transactions = await db.experience_transactions
    .where({ to_user_id: userId, subject })
    .orderBy('created_at', 'desc')
    .limit(amount);

  const chain: ProvenanceChain = [];

  for (const tx of transactions) {
    if (tx.transaction_type === 'creation') {
      // Reached original source
      chain.push({
        type: 'creation',
        source: tx.source_type, // 'audit', 'upvote', 'project'
        source_id: tx.source_id,
        amount: tx.amount,
        timestamp: tx.created_at,
      });
    } else if (tx.transaction_type === 'transfer') {
      // Follow transfer chain
      chain.push({
        type: 'transfer',
        from: tx.from_user_id,
        amount: tx.amount,
        timestamp: tx.created_at,
      });

      // Recurse to find source
      const upstream = await traceExperienceProvenance(
        tx.from_user_id,
        subject,
        tx.amount
      );
      chain.push(...upstream);
    }
  }

  return chain;
}

// Example output
[
  {
    type: 'creation',
    source: 'audit',
    source_id: 'audit_789',
    amount: 50,
    timestamp: '2025-01-01T00:00:00Z'
  },
  {
    type: 'transfer',
    from: 'user_abc',
    amount: 30,
    timestamp: '2025-01-05T00:00:00Z'
  },
  {
    type: 'creation',
    source: 'project',
    source_id: 'project_xyz',
    amount: 30,
    timestamp: '2024-12-15T00:00:00Z'
  }
]
```

### 9.5 Backup & Recovery

**Issue #34: Backup and recovery procedures**

**Backup Strategy:**

**A. Database Backups**
```bash
# Daily full backups
0 2 * * * pg_dump opensystems_prod | gzip > /backups/opensystems_$(date +\%Y\%m\%d).sql.gz

# Hourly incremental backups (WAL archiving)
archive_mode = on
archive_command = 'cp %p /backups/wal/%f'
```

**B. Blockchain Sync**
```typescript
// Continuous sync from blockchain to database
async function syncBlockchainToDatabase() {
  const lastSyncedBlock = await db.metadata.get('last_synced_block');
  const latestBlock = await blockchain.getLatestBlock();

  for (let blockNum = lastSyncedBlock + 1; blockNum <= latestBlock; blockNum++) {
    const events = await blockchain.getBlockEvents(blockNum);

    for (const event of events) {
      if (event.type === 'AuditCompleted') {
        await db.audits.update(event.data.audit_id, {
          block_hash: event.blockHash,
          blockchain_synced: true
        });
      }
      // ... handle other event types
    }

    await db.metadata.set('last_synced_block', blockNum);
  }
}
```

**C. IPFS Content Backup**
```typescript
// Pin important content to multiple IPFS nodes
async function backupToIPFS(contribution: Contribution) {
  // Pin to primary node
  const cid = await ipfs.add(contribution.content);

  // Pin to backup nodes
  await Promise.all([
    ipfs.pin.remote.add(cid, { service: 'pinata' }),
    ipfs.pin.remote.add(cid, { service: 'nftstorage' }),
    ipfs.pin.remote.add(cid, { service: 'web3storage' }),
  ]);

  // Record CID in database
  await db.contributions.update(contribution.id, {
    ipfs_cid: cid.toString(),
    backup_pins: ['pinata', 'nftstorage', 'web3storage']
  });
}
```

**Recovery Procedures:**

**Scenario 1: Database Corruption**
```bash
# Restore from daily backup
gunzip /backups/opensystems_20250110.sql.gz
psql opensystems_prod < opensystems_20250110.sql

# Replay WAL files to get to latest state
pg_waldump /backups/wal/ | psql opensystems_prod
```

**Scenario 2: Blockchain Fork**
```typescript
// Detect fork and re-sync from canonical chain
async function detectAndRecoverFromFork() {
  const dbBlockHash = await db.metadata.get('latest_block_hash');
  const chainBlockHash = await blockchain.getBlock('latest').hash;

  if (dbBlockHash !== chainBlockHash) {
    console.warn('Fork detected! Re-syncing...');

    // Find common ancestor
    let blockNum = await db.metadata.get('last_synced_block');
    while (blockNum > 0) {
      const dbHash = await db.blocks.get(blockNum).hash;
      const chainHash = await blockchain.getBlock(blockNum).hash;

      if (dbHash === chainHash) {
        // Found common ancestor
        console.log(`Common ancestor at block ${blockNum}`);
        break;
      }

      blockNum--;
    }

    // Rollback database to common ancestor
    await db.rollbackToBlock(blockNum);

    // Re-sync from common ancestor
    await syncBlockchainToDatabase();
  }
}
```

**Scenario 3: Data Loss (IPFS)**
```typescript
// Recover content from backup pins
async function recoverFromIPFS(contributionId: string) {
  const contribution = await db.contributions.get(contributionId);

  if (!contribution.content && contribution.ipfs_cid) {
    // Content missing, fetch from IPFS
    try {
      const content = await ipfs.cat(contribution.ipfs_cid);

      // Restore to database
      await db.contributions.update(contributionId, {
        content: content.toString()
      });

      console.log(`Recovered contribution ${contributionId} from IPFS`);
    } catch (error) {
      console.error(`Failed to recover ${contributionId}:`, error);

      // Try backup pins
      for (const service of contribution.backup_pins) {
        try {
          const content = await ipfs.pin.remote.get(contribution.ipfs_cid, { service });
          await db.contributions.update(contributionId, { content: content.toString() });
          console.log(`Recovered from ${service}`);
          break;
        } catch (e) {
          console.error(`${service} also failed:`, e);
        }
      }
    }
  }
}
```

**Disaster Recovery Plan:**
1. **RPO (Recovery Point Objective):** 1 hour (hourly WAL backups)
2. **RTO (Recovery Time Objective):** 4 hours (time to restore and verify)
3. **Redundancy:** 3 database replicas (1 primary, 2 standby)
4. **Geographic distribution:** Primary (US), Standby (EU), Standby (Asia)
5. **Automated failover:** If primary down >5 minutes, promote standby
6. **Blockchain source of truth:** If all databases lost, rebuild from blockchain events

---

## 10. Implementation Notes

### 10.1 Phase 1 Priorities

**MVP Scope (First 3 months):**
1. Experience creation through auditing only (no transfers)
2. Simple auditor selection (random from eligible pool)
3. Basic appeal process (1 additional round)
4. Manual penalty application (no automated detection yet)
5. REST API with authentication
6. PostgreSQL for all data (no blockchain yet)
7. Single subject hierarchy (no complex taxonomy)

**What to Build First:**
```
Week 1-2: Database schema + core API
Week 3-4: User authentication + experience balance API
Week 5-6: Contribution submission + audit assignment
Week 7-8: Audit voting + consensus logic
Week 9-10: Experience rewards + transaction history
Week 11-12: Appeal process + frontend MVP
```

### 10.2 Phase 2 Enhancements

**Advanced Features (Months 4-6):**
1. Blockchain integration (Layer 2)
2. Automated gaming detection
3. Advanced auditor matching (subject expertise)
4. Subject taxonomy governance
5. Webhook system for integrations
6. SDK libraries (TypeScript, Python)
7. Multi-round appeals with juries

### 10.3 Phase 3 Future Vision

**Long-term (6+ months):**
1. Experience transfers (restricted, auditor-approved)
2. Cross-subject voting weights
3. Reputation-based auditor priority
4. Proof of Humanity integration
5. zkSNARK privacy for audit votes
6. Global subject taxonomy (cross-community)
7. AI-assisted audit quality scoring

### 10.4 Open Questions

**To be decided:**
1. Should experience decay over time (to prevent immortal whales)?
2. Should auditors be required to stake experience?
3. Should there be subject-specific appeal juries?
4. Should upvotes grant fractional experience before audit?
5. Should there be a cap on total experience per user?

### 10.5 Success Metrics

**System Health:**
- Audit completion time: <48 hours average
- Appeal rate: <5% of all audits
- Auditor response rate: >80% within 7 days
- Gaming detection accuracy: >90% true positives
- API uptime: >99.9%

**Community Health:**
- Monthly active contributors: growing
- Experience distribution: Gini coefficient <0.6 (not too concentrated)
- Subject diversity: >50 active subjects
- User retention: >60% return after 30 days

**Governance Quality:**
- Consensus strength: >80% average
- Audit overturn rate: <2% (appeals successful)
- Penalty rate: <1% of users
- Subject creation rate: steady growth

---

## Acceptance Criteria Summary

This specification addresses all issues in Objective 1-6:

### Objective 1: Core Experience Economy ✅
- [x] #1: Experience creation & transfer mechanics
- [x] #2: Linear scaling voting power model
- [x] #3: Subject/hashtag taxonomy and scope
- [x] #4: Balance queries and transaction history API
- [x] #5: Genesis experience bootstrapping (see 10.1)

### Objective 2: Auditing & Verification ✅
- [x] #6: Auditor eligibility and selection algorithm
- [x] #7: Subject-based auditor matching
- [x] #8: Consensus mechanisms
- [x] #9: Experience penalties/rewards for auditors
- [x] #10: Audit queue and timeline requirements
- [x] #11: Blockchain integration for immutability

### Objective 3: Appeals & Disputes ✅
- [x] #12: Multi-round appeal process
- [x] #13: Evidence submission requirements
- [x] #14: New auditor pool selection for appeals
- [x] #15: Jury process for small user bases
- [x] #16: Emergency appeal mechanisms
- [x] #17: Decision finality and escalation paths

### Objective 4: Anti-Gaming & Security ✅
- [x] #18: Sybil resistance through verification layer
- [x] #19: Collusion detection (fake upvote pairs)
- [x] #20: Gaming penalty framework
- [x] #21: Vote revocation for false validation
- [x] #22: Proof of value creation requirements
- [x] #23: Attack vectors and mitigations

### Objective 5: API & Integration ✅
- [x] #24: REST API endpoints specification
- [x] #25: Webhook/event system for integrations
- [x] #26: Authentication & authorization model
- [x] #27: Rate limiting and abuse prevention
- [x] #28: Example integrations
- [x] #29: SDK/client library design

### Objective 6: Data Model & Storage ✅
- [x] #30: Database schema design
- [x] #31: Blockchain vs off-chain storage decisions
- [x] #32: Indexing strategy for performance
- [x] #33: Audit trail and provenance tracking
- [x] #34: Backup and recovery procedures

---

## Next Steps

1. Review this specification with stakeholders
2. Prioritize Phase 1 features for MVP
3. Create detailed technical design docs for each component
4. Set up development environment (DB, blockchain testnet)
5. Begin implementation with core experience & audit systems

---

**Document Status:** Draft v1.0
**Last Updated:** 2025-01-11
**Next Review:** After stakeholder feedback
