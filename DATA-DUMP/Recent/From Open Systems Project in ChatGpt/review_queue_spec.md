# Review Queue (Staging Area) — Spec

## Objects
- **Draft**: any AI-generated file (doc/code/note) not yet in the knowledge base (KB).
- **Review Package**: a Draft plus metadata (source agent, pipe, confidence, hashes, embeddings, suggested tags/links).
- **Decision**: Accept → Merge, Request changes, Archive, or Discard.

## Lifecycle & States
1. **Captured** → 2. **Classified** (tags, similarity, dedupe) → 3. **Proposed** (appears in the queue) → 4. **Reviewed** (human sign-off and optional edits) → 5. **Merged** (versioned into KB) → 6. **Linked** (to zero or more context pipes).  
All transitions are immutably logged and auditable.

## Core UX
- **Queue view**: sortable list (newest, agent, pipe, size, confidence, last activity). Bulk actions supported.
- **Inspector** (right panel):
  - provenance (agent, time, prompts), content preview, diffs against similar KB items, auto-suggested tags & context links, “duplicate/overlap” score.
  - buttons: Accept & Merge, Link to…, Edit before merge, Send back to agent, Archive, Discard.
- **Merge preview**: shows where it lands in KB, diffs, backlinks that will update, and any conflicts.
- **Context linker**: pick one or more pipes; choose link type (reference, include, fork as pipe asset).

## Governance & Integrity
- **Roles**: Owner, Maintainer, Reviewer (lightweight—kept human-centric).  
- **Policies** (toggle per workspace/pipe):
  - single vs multi-reviewer required
  - sensitive tags require 2 reviewers
  - auto-merge under confidence ≥ X when author = owner (optional)  
- **Audit trail**: every decision forms a signed entry; edits store before/after + reason. This mirrors the “proof + vote + release” discipline from Open Projects (tokenized in Projects, human-review here).

## Storage Model
- **KB = append-only, versioned** (Git-like): every Merge creates a commit with tree hash; Drafts live in an **inbox** namespace.  
- **Provenance**: content hash, source prompt hash, agent id, optional repo commit refs (for code).  
- **Similarities**: embeddings + locality-sensitive hashing to suggest duplicates/merges.  
- **Snapshots**: context pipes store pointers to KB versions, not raw copies, to keep a single source of truth.

## Context Pipes Integration
- From the queue you can:
  - **Link** the merged doc into one or more pipes (as read-only reference, as included chapter/asset, or as a forked working copy).
  - **Gate** pipe runs so agents **see only Accepted/Merged** materials (no leakage from drafts).  
This matches the “bag of knowledge” + “pipes” model and keeps every agent on the same curated context.

## Actions & Automations
- **Accept & Merge** → write to KB, create backlinks, optionally open a **Project Goal** proof if the doc is a deliverable (bridges to Open Projects’ “proof + vote” flow).
- **Request changes** → returns to the originating agent with inline comments; new revision replaces the Draft while preserving lineage.
- **Archive** (kept, not in KB search), **Discard** (kept as tombstone for audit).
- **Rules** (optional): route by tag to specific reviewers; auto-tag from pipe; auto-subscribe watchers; escalate stale Drafts.

## Dedupe & Conflict Handling
- **Soft dedupe**: show “Possible overlaps” with similarity score and inline diff; you can “Merge into existing” (amend) or “Keep separate” (fork).
- **Conflicts** during merge: 3-way diff; pick sections or prefer target/source; result becomes new KB version (previous versions always readable).

## Notifications
- Daily or per-pipe digest (“3 new Drafts awaiting review; 1 requires your tag”).  
- Mentions & assignments ping reviewers; merge events post to pipe activity.

## APIs & Schema (Minimal)
- `POST /drafts` (payload, agent_id, pipe_id?, metadata)  
- `GET /review-queue?filters`  
- `POST /drafts/{id}:decision { accept|archive|discard|request_changes }`  
- `POST /merge { draft_id, kb_path, links:[pipe_id], commit_message }`  
- Webhooks: `draft.created`, `draft.similar_found`, `merge.completed`  
These live alongside the Open Projects endpoints (funding, proof, vote) but are separate; you can optionally wire “merge.completed” to open a Goal proof.

## Security & Trust
- **Sign-in**: passkeys or SIWE; every action is signed and attributed.  
- **Transparency without identity bias**: surface reasoning and references, not personal identity—aligned with Open Systems’ transparency and creation-centric principles.
- **Immutability envelope**: Draft, decision, and merge metadata are sealed with content hashes; edits never overwrite history.

## Why This Aligns with Open Systems
- **Transparent, auditable flows** and **community-style review** without turning every step into a token vote.
- When a Draft is actually a **deliverable**, you can escalate to an Open Projects **Goal proof** and let stakeholders vote to release funds or declare done.
- Frontend fits neatly into the proposed stack (Next.js/Expo, Tailwind/shadcn, tRPC, SIWE), sharing types and tokens across web and mobile.

## MVP Cut
1. Inbox + Queue + Inspector with Accept/Merge and Link to pipe.  
2. Versioned KB storage + diffs + backlinks.  
3. Basic dedupe + similarity.  
4. Minimal roles and audit log.  
5. Optional bridge: “Open as Project Goal proof” for deliverables.

