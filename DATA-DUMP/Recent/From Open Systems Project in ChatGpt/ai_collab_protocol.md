# Draft Proposal: Universal Protocol for Human–AI Collaboration

## 1. Problem Statement

Modern AI collaboration is fragmented. Users interact with multiple AI agents (ChatGPT, Claude, Gemini, local LLMs, etc.), each capable of producing highly valuable documents, specifications, or code. But every session is siloed. The user must manually export, copy, or reorganize outputs into some storage location before they can be reused by another agent. This breaks continuity and creates unnecessary friction.

The core challenge is **context management**. Every meaningful interaction with AI revolves around *building, curating, and maintaining a context*. A context defines what subset of knowledge is relevant to the current task. While humans intuitively manage this by copy-pasting, tagging, or handpicking files, the process is repetitive and error-prone. Currently:
- Rich outputs from one agent are not automatically available to others.
- Users must constantly shuffle documents into the right place.
- Context creation (deciding what data is relevant for a given task) is entirely manual.

This manual bottleneck contrasts with how AI now automates many other repetitive processes. With the correct protocol, context construction and sharing could also be automated, making collaboration seamless across agents.

---

## 2. Core Insight: Context as the Centerpiece

As we work with AI, we are always managing a **context**. All the data we possess—our documents, knowledge, code, personal information, or references—forms a vast pool. But when performing a specific task, we never want the entire pool. We need only the relevant slice: a curated context.

Key points:
- **AI requires context to perform well**. LLMs generate answers based on the input provided. The input must be the right scope and format.
- **Humans are already context curators**. Copy-pasting snippets, selecting documents, and describing goals are all manual ways of shaping a context.
- **Contexts are temporary by design**. They exist to serve the task at hand and can later be discarded or merged into the broader knowledge base.
- **Automation opportunity**. Instead of humans hand-assembling contexts, agents themselves could propose and construct them, following clear rules and boundaries.

Thus, the essence of this proposal is: **manage knowledge centrally, manage contexts explicitly, and let agents collaborate by plugging into those contexts in a standardized way.**

---

## 3. Analogy: Knowledge Bag and Context Pipes

To understand this system, it helps to use a physical analogy.

- Imagine your **knowledge base** as a **bag or box**. This bag contains all of your documents, code, notes, references, and anything your group has decided to keep. It is your **personal or group source of knowledge**. 
- This is distinct from the **global source of knowledge** that LLMs are trained on. AI companies train on massive, global-scale data. Your bag, however, is your personal or group’s private ledger of knowledge.
- A **context** is like a **pipe** that connects to the bag. Each pipe is defined by a specification: what subset of the bag should flow through.
- There can be many pipes (contexts) simultaneously, each with different filters and purposes. One pipe might be very granular (only design docs for one feature), another more general (all project planning notes).
- These pipes deliver the right slice of knowledge to agents, so they can work effectively without overwhelming them with irrelevant data.

This analogy makes clear that:
- The **bag/box** is stable and grows over time (your repository of knowledge).
- The **pipes** are dynamic and temporary (contexts tailored for tasks).
- Agents connect to pipes, not the whole bag.

---

## 4. User Experience Consideration

While Git and version control are ideal for managing this system under the hood, we cannot expect all users to think like programmers. Most users should never need to know about commits, branches, or repositories. These mechanics must remain invisible.

Instead:
- Users interact only with the **concepts of knowledge, context, and agents**.
- The platform automatically manages version control in the background.
- Interfaces are simple: users can create a new context, invite agents, and merge or archive results without knowing anything about Git.
- Advanced users or developers can still interact with the raw Git backend if desired.

This means the final platform must **wrap Git with a user-friendly layer**. For example:
- Creating a context = starting a new workspace.
- Merging context results = approving changes into the main knowledge base.
- Rolling back = undoing changes from a workspace.

Git provides the rigor, traceability, and audit trail, but users only see high-level concepts.

---

## 5. Use Case Example 1: Video Game Development

Consider a user starting a new video game project:

1. **Knowledge Source**: The user’s main knowledge source is Google Documents, where previous game design docs are stored.
2. **New Project**: The user creates a document describing the vision for the new game.
3. **Agent Query**: The user asks one AI agent to review the new game document and pull in all relevant past design documents from Google Docs.
4. **Proposed Context**: The agent proposes a set of references. The user reviews and handpicks which ones matter, since they are the product owner with final vision.
5. **Context Pipe Creation**: This selection becomes a new **context pipe** called, for example, *Video Game Development Context*.
6. **References, not copies**: The pipe doesn’t duplicate documents—it references them. If a document is updated in Google Docs, the context points to the new version, while still retaining access to history if needed.
7. **Agent Collaboration**:
   - Claude is used for drafting narrative and documentation.
   - OpenAI’s Codex is used for generating development tasks.
   - Local LLMs and Codex handle simultaneous coding tasks.
8. **Task List as Knowledge**: The task list generated by Codex becomes another document in the knowledge source, referenced in the context.
9. **Asynchronous Work**: Multiple agents work in parallel against the same context, producing coordinated outputs.
10. **Output Routing**: Code artifacts may be stored in GitHub, docs in Google Docs, or files in IPFS. The context pipe keeps track of references to each.
11. **Human Review**: The user ticks off completed items and approves changes as they flow back into the knowledge source.

This workflow highlights:
- Centralized knowledge with no duplication.
- Context pipes as reusable, composable subsets.
- Multiple agents collaborating seamlessly through the same context.
- User sovereignty over vision and approval.

---

## 6. Use Case Example 2: Legal Case Preparation

Now imagine a law firm working on a case:

1. **Knowledge Source**: The firm’s internal knowledge source contains all prior case files, legal memos, and research notes.
2. **New Case**: The firm creates a document describing the specifics of the current case.
3. **Agent Query**: AI agents review the case description and search both internal documents and external sources, such as government repositories of historic cases.
4. **Proposed Context**: Agents propose relevant past cases, precedents, and legal references. The lawyers manually review and approve which to include, since they define the legal strategy.
5. **Context Pipe Creation**: A new **context pipe** is built for this case, referencing approved documents and external sources.
6. **Agent Collaboration**:
   - Research agents continue scanning external legal databases for updates.
   - Drafting agents generate potential arguments, counterarguments, and supporting evidence.
   - Analysis agents highlight potential weaknesses or contradictions.
7. **Human Specification**: Lawyers decide which AI-generated drafts to accept, refine, or reject.
8. **Output Routing**: Arguments, filings, and strategy notes are stored back in the firm’s knowledge source, ensuring all updates remain traceable.

This workflow shows how:
- Legal teams can leverage their private knowledge source alongside public repositories.
- Context pipes create focused workspaces specific to cases.
- Agents augment, but do not replace, human judgment.
- Provenance and history ensure that no critical precedent or argument is lost.

---

## 7. Core Components

### 7.1 Knowledge Repository
- Version-controlled (Git or equivalent under the hood).
- Holds canonical documents, code, specifications, and metadata.
- `main` branch is the authoritative ledger, but invisible to most users.

### 7.2 Context Branches
- Each project or task creates its own branch (hidden from non-technical users).
- Defined by `.context.yaml` but presented as a simple workspace or project view.
- Serves as a curated viewport into the main repository.

### 7.3 Agent Contracts
- Each context contains a contract file per agent.
- Technical users see full YAML/Markdown specs.
- Non-technical users see simplified permissions ("Claude can draft documents," "ChatGPT can edit specs").

---

## 8. Protocol Operations

### 8.1 Read
- Agents load allowed context materials.
- Users only see "documents included in this workspace."

### 8.2 Write
- Agents propose edits as draft contributions.
- Users see "AI has suggested an update" with accept/reject buttons.

### 8.3 Organize
- Agents propose grouping, tagging, or restructuring.
- Users see "AI suggests moving these notes into a new folder."

### 8.4 Context Automation
- Agents can propose new contexts automatically.
- Example: "Create a workspace with all Event Horizon MVP design docs plus new drafts." Or: "Create a workspace with all cases relevant to intellectual property disputes in Ontario."
- For the user, this is just a one-click confirmation.

### 8.5 Human Review
- Humans approve or reject merges.
- No Git vocabulary is exposed; only clear actions like *approve*, *archive*, *restore*.

---

## 9. Repository Structure (Under the Hood)

```
/docs/                 Human-authored artifacts
/specs/                Formal specifications and APIs
/src/                  Code
/assets/               Media and binaries
/contexts/             Shared resources for contexts
/.agents/              Agent contracts, manifests, policies, keys
/.knowledge/           Indexes, graphs, embeddings
/.policies/            Compliance and redaction rules
```

End users only see **Projects**, **Workspaces**, and **AI Collaborators**. The raw structure is abstracted away.

---

## 10. Validation Pipeline

- Runs automatically in the background.
- Users only see the results: pass/fail, suggested fixes, or warnings.
- Advanced logs are available for technical users.

---

## 11. Example Agent Contract (Simplified View for Users)

**Agent:** Claude (Writer)  
**Permissions:** Can draft documentation in the Event Horizon workspace  
**Restrictions:** Cannot edit code  
**Expires:** Dec 31, 2025

---

## 12. Benefits

- **Seamless collaboration**: Multiple AI vendors can work together in one platform.
- **Automated context building**: AI proposes contexts; users confirm with one click.
- **User-friendly**: Non-programmers don’t need to understand Git or repositories.
- **User sovereignty**: Final approval always rests with the human.
- **Auditability**: Under the hood, version control ensures traceability.
- **Clarity through analogy**: Users can think in terms of bags (knowledge) and pipes (contexts), instead of abstract software concepts.
- **No duplication of truth**: Contexts reference existing sources rather than copying them.
- **Cross-domain flexibility**: The system works equally well for software projects, legal cases, research, or creative work.

---

## 13. End Goal

This system aims to evolve into a **universal protocol for AI collaboration**. By standardizing knowledge, contexts, and agents, and by hiding technical complexity from the user, the platform enables:
- Accessible collaboration for non-technical users.
- Rigorous version control and provenance for advanced users.
- Interoperability across AI ecosystems.

A name is still to be chosen, but the key conceptual triad could be **Knowledge – Context – Agent**. The protocol should feel intuitive to any user while remaining technically robust underneath. This is what will allow AI companies to adopt and integrate it at scale.

