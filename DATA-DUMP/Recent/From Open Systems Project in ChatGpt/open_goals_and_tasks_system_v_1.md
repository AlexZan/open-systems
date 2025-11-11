# Open Goals and Tasks System v1

## Purpose
Turn broad intentions into granular, linked, and verifiable work that any agent can pick up, continue, and prove complete. Persist everything as structured knowledge for private entities or groups, while remaining compatible with Open Projects and future Open Democracy features.

## Core Concepts

### 1. Goal
A declarative outcome statement owned by an Entity. Attributes:
- Title, Intent, Rationale
- Scope: private entity, private group, or public
- Timeframe: horizon and target date
- Dependencies: other Goals
- Tags: subjects, domains
- Success Criteria: measurable acceptance tests or KPIs

### 2. Objective, Key Results, Milestones
- Objective: sub-intent under a Goal
- Key Results: measurable targets that prove Objective movement
- Milestones: proof-gated checkpoints that release funds or unlock next work

### 3. Task
Atomic unit of work linked to a Milestone or KR. Attributes:
- Definition of Done checklist
- Inputs required and outputs expected
- Estimation and priority
- Assigned agent or pool
- Evidence links produced on completion

### 4. Evidence Bundle
Immutable record proving completion of a Task or Milestone:
- Artifact hashes, commit SHAs, document links, screenshots
- Demo notes and verifier checklist
- Verifier signatures and timestamps

### 5. Context Capsule
A compact, machine-readable packet that any agent can ingest to start or resume work. Contains:
- Goal → Objective → Milestone → Task lineage
- Constraints, assumptions, glossary
- Current state, known issues, risk log
- References to Knowledge Items

### 6. Knowledge Item
Canonical notes, decisions, diagrams, research results. Versioned and linkable. Serves both humans and agents.

### 7. Handoff Record
A structured summary for continuity when switching agents:
- What was done, what remains, next best step
- Local environment state, credentials pointers, reproducible commands
- Open questions and blockers

### 8. Progress Ledger
Time-ordered immutable log of state changes: created, updated, blocked, proof submitted, verified, failed, reopened. Enables analytics and audit.

## End-to-End Flow

1. Capture Broad Intent
User writes a high-level Goal. The system suggests Objectives, KRs, and initial Milestones by querying the Knowledge Base and templates.

2. Refinement Loop
AI proposes a first cut of Tasks under each Milestone. User accepts or edits. Definitions of Done and Evidence templates are auto-attached per task type.

3. Context Packaging
A Context Capsule is generated for each Task and Milestone so any agent can start with the right constraints and references.

4. Assignment and Work
- Private mode: owner assigns or opens a pool for eligible agents
- Open mode: tasks can be bid on by members with the required certifications or trust level

5. Proof and Verification
Agent submits an Evidence Bundle. Verifiers run the checklist. Pass or fail updates the Progress Ledger. Milestones release funds or unlock follow-on tasks.

6. Handoffs
At any moment, an agent can generate a Handoff Record. Incoming agents read the Capsule and Handoff to continue without context loss.

7. Knowledge Consolidation
Accepted proofs and notes auto-extract Knowledge Items with backlinks to originating Goals, enabling reuse by future agents.

## Data Model Sketch

### Entity
- id, name, members, permissions

### Goal
- id, entity_id, title, intent, rationale, scope, timeframe, dependencies[], tags[], success_criteria[], status

### Objective
- id, goal_id, statement

### KeyResult
- id, objective_id, metric, target, current_value, due

### Milestone
- id, goal_id, title, acceptance_criteria[], due, status, funding_pointer?

### Task
- id, milestone_id, title, dod[], inputs[], outputs[], estimate, priority, assignee?, status

### Evidence
- id, task_or_milestone_id, artifact_hashes[], links[], demo_notes, verifier_ids[], result, timestamp

### ContextCapsule
- id, target_ref, serialized_payload, version

### KnowledgeItem
- id, title, body, type, links[], tags[], version, provenance

### Handoff
- id, task_id, summary, env_notes, next_steps[], open_questions[], attachments

### ProgressEvent
- id, target_ref, type, actor, payload, timestamp

## Agent Interfaces

### Context Pipe
- `GET /context/{ref}` returns the Context Capsule and minimal working set of Knowledge Items
- `POST /handoff` submits a Handoff Record
- `POST /evidence` submits an Evidence Bundle
- `GET /next` returns the next best action for a given Goal or Task, with justification

### Continuity Guarantees
- Every Task and Milestone has a fresh Capsule upon state change
- Handoffs are mandatory on idle timeout or reassignment

## Verification and Trust

- Default: internal verifiers with role-based access
- Optional: auditor pool for high-stakes work
- All verification steps produce signed ProgressEvents

## Linking Work

- GitHub, GitLab, or local repos: commit SHAs and release artifacts referenced in Evidence
- Docs: Canvas docs, Google Docs, or Markdown files hashed and linked
- Issues: cross-links to trackers preserved in Knowledge Items

## Compatibility with Open Projects

- Milestone maps to Goal in Open Projects
- Evidence Bundle maps to Proof Bundle
- Verification mirrors token-based voting later, starting with role verifiers
- Failover: on inactivity, convert private project to an Open Project template if enabled

## Roles

- Owner: defines Goals, sets verification requirements
- Member: contributes and verifies
- Auditor: optional external review role
- Agent: automated worker operating via the Context Pipe

## Templates

- Goal templates for common domains
- Definition of Done checklists by task type
- Evidence templates for code, design, research, ops
- Handoff templates to standardize continuity

## Minimal UI

1. Goals view with Objectives, KRs, and Milestones
2. Task board with Capsule preview and Handoff button
3. Evidence review queue for verifiers
4. Knowledge graph view showing backlinks and provenance

## Example

- Broad Goal: Publish MVP of autonomous-robot game loop
- Objectives: resource extraction loop, salvage loop, basic combat loop
- KRs: complete 3 internal playtests with >20 minutes median session
- Milestone: Resource extraction prototype pass with bots
- Tasks: implement mining yield model, hook up sensors, record playtest, analyze telemetry
- Evidence: commit SHA, video demo, telemetry CSV, verifier checklist
- Capsule: includes design doc excerpts, API stubs, accepted assumptions
- Handoff: notes that telemetry parser is 80 percent done, next step add error handling

## Analytics

- Burndown and burnup by Goal and Milestone
- Evidence quality score by domain
- Mean time to verification, number of handoffs per Task

## Security

- All artifacts referenced by content hash
- Private scopes default to end-to-end encryption for notes and attachments
- Fine-grained permissions per Entity and per Goal

## Phase 1 Scope

- Private entities and groups only
- Role verifiers, no token voting yet
- Evidence via links and hashes, no SBOM required
- Minimal APIs for Context, Handoff, Evidence

## Phase 2 Preview

- Integrate Open Projects tokenized voting for public milestones
- Auditor pools and subscriptions
- SBOM and attestations in Evidence templates
- Automated Capsule generation from accepted Knowledge Items

## Success Criteria

- Any agent can resume a Task within 10 minutes using the Capsule and Handoff
- Zero orphaned tasks, all have lineage and Knowledge backlinks
- Verification median under 24 hours for Phase 1

