# Open Systems Specifications

**Master Reference for the Open Systems Book and Development Framework**

This document is the authoritative source of truth. Every specification, architectural decision, and implementation requirement stems from this structure.

---

## Overview

Open Systems is a comprehensive framework for decentralized governance, collaboration, and value creation. It consists of five interdependent systems, all unified by core principles and transparent, blockchain-backed processes.

---

## Complete Book Structure

### Part 1: Foundation & Vision
Philosophical grounding, principles, and the vision that guides everything.

| Chapter | Spec File | Purpose |
|---------|-----------|---------|
| 1 | `00-foundation/emergence-and-complexity.md` | How complexity emerges; foundation for intelligence |
| 2 | `00-foundation/why-open-systems.md` | Problems with current systems; why we need decentralization |
| 3 | `00-foundation/core-principles.md` | The five core principles that guide all decisions |
| 4 | `00-foundation/our-vision.md` | What Open Systems enables; the future we're building |

---

### Part 2: Open Democracy
How voting power is earned through contribution, and how communities make decisions together.

| Chapter | Spec File | Purpose |
|---------|-----------|---------|
| 5 | `01-governance/overview.md` | Introduction to Open Democracy |
| 6 | `01-governance/experience-and-voting-power.md` | Experience: earned, not purchased; voting power mechanics |
| 7 | `01-governance/voting-mechanisms.md` | How votes are counted, quorum, consensus thresholds |
| 8 | `01-governance/expressive-politics.md` | Beyond binary votes: nuanced expression of preferences |
| 9 | `01-governance/freedoms-and-fundamental-rules.md` | Freedom as the foundational principle; deriving all laws from freedom |
| 10 | `01-governance/local-global-rulesets.md` | How local and global rules interact; gradient maps and compatibility |
| 11 | `01-governance/conflict-resolution.md` | Resolving rule conflicts; when communities disagree |

---

### Part 3: Open Projects (Unified System)
Crowdfunding, collaboration, milestone-driven development, and the flexible project system that unifies all work.

| Chapter | Spec File | Purpose |
|---------|-----------|---------|
| 12 | `02-projects/overview.md` | Introduction; Projects as the implementation layer |
| 13 | `02-projects/core-principles.md` | Why this design; how Projects implement Open Systems principles |
| 14 | `02-projects/roles-and-responsibilities.md` | Roles: Product Owner, Funders, Contributors, Community |
| 15 | `02-projects/project-types.md` | Three project types: Closed, Open, Venture-style; when to use each |
| 16 | `02-projects/funding-and-tokens.md` | Crowdfunding mechanics; stake tokens; token lifecycle |
| 17 | `02-projects/proof-and-voting.md` | How work is proven; how community validates progress |
| 18 | `02-projects/failover-mechanism.md` | What happens when a project owner disappears; community takeover |
| 19 | `02-projects/features/bidding-system.md` | Optional: Task bidding and negotiation |
| 20 | `02-projects/features/sweat-equity.md` | Optional: Equity multipliers for high-value contributions |
| 21 | `02-projects/features/profit-sharing.md` | Optional: Revenue distribution templates |
| 22 | `02-projects/features/compensation-models.md` | Optional: Payment structures (salary, equity, hourly, outcome-based) |

---

### Part 4: Open Forum
Transparent discussion, debate, and narrative preservation that grounds all decisions in evidence.

| Chapter | Spec File | Purpose |
|---------|-----------|---------|
| 23 | `03-forum/overview.md` | Introduction; why a forum layer is essential |
| 24 | `03-forum/discussion-structure.md` | How discussions are organized; threading and categorization |
| 25 | `03-forum/information-packages.md` | Bundling reasoning with decisions; preserved context |
| 26 | `03-forum/narrative-preservation.md` | Making the forum immutable; blockchain backing |

---

### Part 5: Technical Architecture
How Open Systems is built; the stack, contracts, and technical integration.

| Chapter | Spec File | Purpose |
|---------|-----------|---------|
| 27 | `04-technical/system-overview.md` | Architecture overview; layers and responsibilities |
| 28 | `04-technical/architecture-layers.md` | Frontend, backend, blockchain; how they integrate |
| 29 | `04-technical/smart-contracts.md` | Smart contracts: Projects, Goals, Tokens, Voting, Failover |
| 30 | `04-technical/frontend-architecture.md` | Next.js + Expo; UI/UX for governance and collaboration |
| 31 | `04-technical/backend-architecture.md` | Supabase + tRPC; API design and data management |
| 32 | `04-technical/blockchain-integration.md` | How blockchain is used; proof of work/contribution |
| 33 | `04-technical/github-oracle.md` | Connecting to GitHub; proof automation via CI/CD |
| 34 | `04-technical/database-schema.md` | Data structures and relationships |
| 35 | `04-technical/api-design.md` | API endpoints for all Open Systems functions |

---

### Appendix: Operations & Development
How to build Open Systems; the process for specification to implementation.

| Chapter | Spec File | Purpose |
|---------|-----------|---------|
| A1 | `05-operations/spec-impl-system.md` | How specs become code; acceptance criteria and traceability |
| A2 | `05-operations/ai-collaboration-protocol.md` | How AI agents collaborate with humans on development |
| A3 | `05-operations/review-queue-process.md` | Code review and proof validation workflow |
| A4 | `05-operations/proof-bundle-structure.md` | What a proof bundle contains; immutable verification |
| A5 | `05-operations/goals-and-tasks-system.md` | Hierarchical goal structure; objectives, key results, milestones |
| A6 | `05-operations/game-system-spec.md` | Gamification and engagement mechanics |

---

## Concept Dependencies

```
Foundation (00)
    ↓
Governance (01) ← Determines voting rules and experience
    ↓
Projects (02) ← Uses voting to approve work
    ↓
Forum (03) ← Records reasoning behind decisions
    ↓
Technical (04) ← Implements all of the above
```

All development follows the operations process (05).

---

## For Book Writers

Each spec file is structured to be readable as a book chapter:

1. **Overview** - What this system does and why it matters
2. **Core Concepts** - Key ideas explained
3. **How It Works** - Mechanics and processes
4. **Examples** - Real-world application
5. **Integration** - How this system connects to others

Files are agent-friendly (structured markdown) but human-readable for book publishing.

---

## For Developers

Each spec file includes:

- **Acceptance Criteria (AC)** - Testable requirements (AC-ID-001, etc.)
- **Technical Details** - Implementation guidance
- **Contracts** - Smart contract requirements
- **Dependencies** - What this depends on

Follow `/05-operations/spec-impl-system.md` for the development process.

Generate code with `@trace(AC-...)` comments to link implementations to requirements.

---

## Glossary

See `GLOSSARY.md` for consistent terminology across all specs.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | [Date] | Initial specification from 20+ years of research |

---

## Status Indicators

Each spec file has a status:

- **draft** - Still being developed; may change significantly
- **review** - Ready for feedback; core structure stable
- **stable** - Locked in; changes require team discussion
- **implementation-ready** - Can be built; AC criteria defined

---

## How This Document is Used

1. **Book outline** - Chapters follow this structure
2. **Development roadmap** - Specs are built in dependency order
3. **Verification** - Proof bundles link back to specs and AC
4. **Community governance** - Voting references specific specs when proposing changes

---

## Next Steps

After reading this overview:

1. **Understand the vision** → Read Part 1 (Foundation)
2. **Learn how it works** → Read Parts 2-4 (Systems)
3. **Understand implementation** → Read Part 5 (Technical)
4. **Get involved in development** → Read Appendix (Operations)

Start with `00-foundation/why-open-systems.md` to understand the problems we're solving.
