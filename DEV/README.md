# Open Systems Development

**This folder contains the implementation of the Open Systems framework.**

**Source of Truth:** All specifications and requirements live in `../SPECS/`

This folder is for implementation code, and should be viewed as a working copy that references the specifications.

---

## Before You Start

### 1. Understand the System

Read these in order:
1. `../README.md` - Project overview
2. `../SPECS/INDEX.md` - Complete system design
3. `../SPECS/00-foundation/` - Vision and principles
4. `../AI-BOOK/All Chapters.md` - Philosophical context

### 2. Learn Your Domain

Pick the area you'll work on:
- **Frontend?** Read `/frontend/README.md` → `../SPECS/04-technical/frontend-architecture.md`
- **Backend?** Read `/backend/README.md` → `../SPECS/04-technical/backend-architecture.md`
- **Smart Contracts?** Read `/smart-contracts/README.md` → `../SPECS/04-technical/smart-contracts.md`

### 3. Understand the Development Process

Read `../SPECS/05-operations/spec-impl-system.md`

Key concepts:
- Specifications are source of truth
- Code is traced to acceptance criteria (AC)
- Proof bundles link spec → code → tests → deployment
- Community votes on proof bundles
- Funds released automatically on approval

---

## Project Structure

```
DEV/
├── README.md                    # This file
├── ROADMAP.md                   # Implementation phases & priorities
│
├── frontend/                    # Next.js + Expo
│   ├── README.md
│   ├── apps/
│   │   ├── web/                 # Next.js desktop web app
│   │   └── mobile/              # Expo React Native mobile
│   └── specs/                   # Symlink to ../SPECS
│
├── backend/                     # Supabase + tRPC
│   ├── README.md
│   ├── api/                     # tRPC router and procedures
│   ├── db/                      # Database schema and migrations
│   ├── lib/                     # Shared utilities
│   └── specs/                   # Symlink to ../SPECS
│
├── smart-contracts/             # Solidity smart contracts
│   ├── README.md
│   ├── contracts/               # Contract implementations
│   ├── test/                    # Contract tests
│   ├── deploy/                  # Deployment scripts
│   └── specs/                   # Symlink to ../SPECS
│
└── proof-bundles/               # Generated during development
    ├── phase-1/                 # Phase 1 completion proofs
    ├── phase-2/                 # Phase 2 completion proofs
    └── phase-3/                 # Phase 3 completion proofs
```

---

## Development Process Overview

### 1. Pick a Spec

Choose an unstarted item from `../SPECS/`:
- Has acceptance criteria (AC)
- Clearly defined requirements
- Testable outcomes

Example: `../SPECS/02-projects/overview.md`

### 2. Create a Feature Branch

```bash
git checkout -b feature/AC-PROJ-001-project-creation
```

Branch name format: `feature/AC-XXXX-YYY-description`

### 3. Implement with Traceability

Link code to acceptance criteria:

```typescript
// @trace(AC-PROJ-001): User can create a new project
export async function createProject(input: CreateProjectInput): Promise<Project> {
  // Implementation here
}
```

Every function should reference at least one AC.

### 4. Write Tests

Tests must mirror acceptance criteria:

```typescript
describe('AC-PROJ-001: User can create a new project', () => {
  it('should accept valid project metadata', () => {
    // test
  })

  it('should reject empty title', () => {
    // test
  })
})
```

Test naming: `test_AC-XXXX-YYY_description`

### 5. Generate Proof Bundle

When all AC tests pass:

```bash
npm run proof:generate -- --ac AC-PROJ-001
```

Output:
- Spec snapshot (hash)
- Trace index (AC → code → tests)
- AC checklist (pass/fail matrix)
- Build artifacts
- Commit hash

### 6. Submit for Review & Voting

Open a Pull Request:
- Title: `[AC-PROJ-001] Project Creation System`
- Description: Include proof bundle summary
- Checklist: Mark which ACs are satisfied
- Link to spec: Reference `../SPECS/02-projects/overview.md`

### 7. Community Voting

- Community reviews proof bundle
- Votes on acceptance (30% quorum, 70% approval)
- On approval: Funds released automatically
- Code merged to main
- Deployed to network

---

## Technology Stack

### Frontend
- **Web:** Next.js 15 + TypeScript
- **Mobile:** Expo + React Native + NativeWind
- **Styling:** Tailwind CSS + shadcn/ui
- **State Management:** React Query + Zustand
- **Blockchain:** wagmi + viem + WalletConnect

### Backend
- **Framework:** tRPC + Fastify (or Express)
- **Database:** Supabase (PostgreSQL + Realtime)
- **ORM:** Prisma
- **Authentication:** NextAuth.js
- **Deployment:** Vercel

### Smart Contracts
- **Language:** Solidity 0.8.x
- **Framework:** Hardhat with Foundry
- **Testing:** Hardhat + Foundry
- **Deployment:** Hardhat scripts
- **Network:** Ethereum L2 (Optimism/Base)

---

## Getting Started

### Clone & Setup

```bash
git clone <repo>
cd open-systems
cd DEV

# Frontend
cd frontend
npm install
npm run dev

# Backend (separate terminal)
cd backend
npm install
npm run dev

# Smart Contracts (separate terminal)
cd smart-contracts
npm install
npm test
npx hardhat node
```

### First Task

Start with Phase 1 foundations:

1. Backend: Project CRUD operations
   - Reference: `../SPECS/02-projects/overview.md`
   - Start: `AC-PROJ-001` through `AC-PROJ-010`

2. Smart Contract: Project creation contract
   - Reference: `../SPECS/04-technical/smart-contracts.md`
   - Start: `AC-SC-001` through `AC-SC-005`

3. Frontend: Project listing and creation UI
   - Reference: `../SPECS/04-technical/frontend-architecture.md`
   - Start: `AC-UI-PROJ-001` through `AC-UI-PROJ-010`

---

## Key References

### Specs for Each Domain

**Project Management & Collaboration:**
- `../SPECS/02-projects/` - How projects work
- `../SPECS/05-operations/goals-and-tasks-system.md` - Hierarchical task structure

**Governance & Voting:**
- `../SPECS/01-governance/voting-mechanisms.md` - Voting rules
- `../SPECS/01-governance/experience-and-voting-power.md` - Experience tokens

**Technical Implementation:**
- `../SPECS/04-technical/smart-contracts.md` - Contract architecture
- `../SPECS/04-technical/frontend-architecture.md` - UI structure
- `../SPECS/04-technical/backend-architecture.md` - API design

**Development Process:**
- `../SPECS/05-operations/spec-impl-system.md` - How to build from specs
- `../SPECS/05-operations/proof-bundle-structure.md` - Proof format

### Terminology

Not sure what a term means? → `../SPECS/GLOSSARY.md`

### For Help

1. Is your question about **what to build?** → Read the relevant spec in `../SPECS/`
2. Is your question about **how to build it?** → Check domain READMEs
3. Is your question about **why this design?** → Read `../AI-BOOK/All Chapters.md`
4. Is your question about a **technical detail?** → Read `../SPECS/04-technical/`

---

## Development Phases

See `ROADMAP.md` for detailed phase breakdown.

**Phase 1: Core Infrastructure**
- Basic project CRUD
- Funding and token system
- Simple voting
- GitHub integration

**Phase 2: Advanced Governance**
- Experience system
- Expressive politics
- Failover mechanism
- Forum integration

**Phase 3: Scale & Polish**
- Performance optimization
- Advanced features
- Community tools
- Mobile optimization

---

## Code Standards

### Traceability

Every function/component should be traceable:

```typescript
// Every meaningful piece of code should have a @trace comment
// @trace(AC-ID-001): Description of what acceptance criterion this satisfies
```

### Testing

- Unit tests for business logic
- Integration tests for API/contract interactions
- Test naming mirrors acceptance criteria
- Aim for 80%+ coverage on critical paths

### Documentation

- README in each domain folder
- Comments for non-obvious logic
- Specs are the detailed requirements
- Code should be self-documenting where possible

### Commits

```
[AC-PROJ-001] Implement project creation endpoint

- Accepts project metadata
- Validates required fields
- Returns project ID and creation timestamp
- Linked to spec: SPECS/02-projects/overview.md
```

---

## Deployment & Verification

### Local Testing

```bash
# Start local blockchain
npx hardhat node

# Deploy contracts locally
npx hardhat run scripts/deploy.ts --network localhost

# Run full integration test
npm run test:integration
```

### Testnet Deployment

```bash
# Deploy to Optimism/Base testnet
npm run deploy:testnet

# Verify on block explorer
npm run verify:testnet
```

### Generating Proof Bundle

```bash
# Generate when all ACs pass
npm run proof:generate -- --spec-path ../SPECS/02-projects/overview.md

# Proof bundle output
# └── proof-bundle-{timestamp}.json
#     ├── spec_snapshot: {hash}
#     ├── trace_index: {AC → code → tests}
#     ├── ac_checklist: {pass/fail matrix}
#     ├── build_artifacts: {hashes}
#     └── commit_hash: {signed ref}
```

### Community Voting

Proof bundle is submitted for community voting. On approval (≥70%), funds are released and code deployed to production.

---

## Troubleshooting

### Tests Failing?

1. Check that specs are correctly understood
2. Verify acceptance criteria in code match spec
3. Run `npm run lint` to check code quality
4. Check that @trace comments link to real ACs

### Can't Find a Requirement?

1. Check `../SPECS/INDEX.md` for navigation
2. Use `../SPECS/GLOSSARY.md` for terminology
3. Ask: Is this in the spec, or in my assumptions?
4. Reference the AI book for philosophical context

### Unsure About Design?

1. Specs explain the **what** and **why**
2. Read related specs for context
3. Check `../DATA-DUMP/` for historical thinking
4. Ask in team discussions

---

## Contributing

Development follows the Open Systems principles:

✅ **Transparent** - All code on GitHub, all decisions traceable
✅ **Fair** - Proof bundles ensure objective verification
✅ **Democratic** - Community votes on major milestones
✅ **Accountable** - All changes traced to acceptance criteria

---

## Next Steps

1. Read `ROADMAP.md` to understand development priorities
2. Pick a domain (frontend/backend/contracts)
3. Read the domain README
4. Start with Phase 1 acceptance criteria
5. Reference specs as you build
6. Generate proof bundles when complete
7. Submit for community review

---

**Questions?** See `../SPECS/GLOSSARY.md` or read the relevant spec section.

**Ready to contribute?** Pick a task from `ROADMAP.md` and start building!
