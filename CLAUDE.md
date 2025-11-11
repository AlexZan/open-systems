# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Open Systems** is a specification and architectural framework for decentralized collaboration, governance, and value creation. It defines systems for transparent, community-driven projects using blockchain smart contracts, decentralized governance, and experience-based participation.

**Current State**: This is a specification-phase project focused on design and architecture. Production implementation has not yet begun.

**Core Principle**: Value is earned through experience and contribution, not wealth or status. Governance emerges organically from transparent participation.

## RAG Documentation Search

**For AI Agents**: This project has 210 specification documents (500+ pages) indexed in a semantic search system.

**How to search**: Run the compact search script:
```bash
python scripts/search_compact.py "your query here"
```

**Example queries**:
- `python scripts/search_compact.py "governance voting mechanism"`
- `python scripts/search_compact.py "smart contract architecture"`
- `python scripts/search_compact.py "milestone funding process"`

**Output**: Top 3 results with similarity scores, section paths, and source file links (~200 tokens per query)

**When to use**: Before asking questions about Open Systems concepts, search first to get accurate context from specifications.

## Project Structure

```
d:\Dev\Open Systems/
├── data dump/
│   ├── AI Book -Relevant/              # Reference material
│   ├── Recent/                         # Current active specifications (Markdown)
│   │   └── From Open Systems Project in ChatGpt/
│   │       ├── Core Specifications
│   │       ├── Architecture Documents
│   │       └── Implementation Guides
│   └── Open Systems Shared/            # Archived comprehensive documentation
│       ├── Applications/               # Real-world use cases
│       ├── Technical/                  # Technical architecture
│       ├── Theory/                     # Philosophical foundations
│       ├── Plan/                       # Development roadmaps
│       ├── Rules/                      # Governance rules
│       └── [Other subsystems]
```

## Key Specifications (in `data dump/Recent/From Open Systems Project in ChatGpt/`)

### Core Systems

- **open_systems_projects_summary.md** - Overview of the Projects system (crowdfunded, milestone-driven)
- **open_projects_spec_v_1.md** - Detailed v1 specification with roles, objects, processes, and interfaces
- **open_systems_smart_contracts.md** - Blockchain architecture and contract design
- **open_ventures_poc_summary.md** - Proof of concept objectives and feature structure

### Specialized Subsystems

- **open_goals_and_tasks_system_v_1.md** - Task hierarchy: Goals → Objectives → Key Results → Milestones → Tasks
- **ai_collab_protocol.md** - Protocol for human-AI collaboration using "Knowledge Bag" and "Context Pipes"
- **review_queue_spec.md** - Workflow for AI-generated content staging and knowledge base integration
- **open_game_system_spec.md** - Application to decentralized game development
- **spec_impl_system_v_1.md** - Specification-to-implementation pipeline with traceability

### Architecture Documents

- **open_ventures_user_flow.md** - User experience and funding flow architecture
- **open_systems_conclusions.md** - Synthesis of all subsystems

## Development Workflow

When implementing features from specifications:

1. **Specification First**: All development starts from Markdown specifications with Acceptance Criteria (ACs)
2. **Traceability**: Use `@trace(AC-...)` comments in code to link implementations to specific acceptance criteria
3. **Proof Bundles**: Implementations should generate verification bundles (spec hash, trace index, AC checklist, build artifacts)
4. **AI-Assisted Generation**: Agents generate code from specs; product owners lock critical behaviors to prevent modification

## Proposed Technology Stack

**Phase 1 (MVP):**
- **Frontend**: Next.js 15 + Tailwind + shadcn/ui
- **Mobile**: Expo + NativeWind
- **Backend**: Supabase + tRPC
- **Blockchain**: Ethereum Layer 2 (Optimism/Base) with wagmi/viem
- **Smart Contracts**: Solidity with Hardhat/Foundry
- **Infrastructure**: Vercel + Supabase
- **Integration**: GitHub webhooks, WalletConnect

## Smart Contracts Architecture

Key contract types (from specifications):
- **Project Contract**: Metadata and goal lifecycle
- **Goal Contract**: Funding progress and proof state
- **Token Contract**: Non-transferable (soulbound) stake tokens
- **Proof Contract**: Immutable evidence hashes
- **Voting Contract**: Quorum (30%) and approval (70%) logic
- **Failover Contract**: Community takeover mechanism
- **GitHub Oracle**: Bridge commits/releases to on-chain verification

## Key Design Principles

1. **Experience = Power**: Voting power earned through contribution, not wealth
2. **Transparency Without Identity**: Immutable truth with preserved privacy
3. **Fluid Governance**: Representation emerges from contributions
4. **Crowdfunded Continuity**: Projects cannot die—community can take over
5. **Decentralized Enforcement**: Fairness maintained through smart contracts

## Voting & Governance Mechanics

- **Quorum**: 30% token participation minimum
- **Pass Threshold**: 70% approval required
- **Failover Triggers**: Inactivity OR 2 consecutive failed votes
- **Non-Transferable Tokens (Phase 1)**: Soulbound to prevent market speculation
- **Transferable Tokens (Phase 2)**: With experience-based voting power

## Phased Implementation

**Phase 1**: Core milestone funding, non-transferable tokens, simple voting
**Phase 2**: Experience-based governance, transferable tokens, forum integration
**Phase 3**: Full democracy protocol, expressive politics, global certification network

## Important Notes

- This is a **specification project**, not yet a code implementation
- Specifications are stored in Markdown format for AI-assisted generation workflows
- The **spec_impl_system_v_1.md** document defines how AI agents should approach code generation
- Use specification documents as the single source of truth for requirements
- Link all code implementations back to acceptance criteria in specifications
