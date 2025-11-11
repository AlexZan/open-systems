# Goal
A contributor finishes refining a canvas document with a ChatGPT agent and wants to save it into the shared knowledge base. This flow describes how the platform accepts the document, validates it, versions it, indexes it, and publishes it for both humans and agents.

# Actors
1. Author using ChatGPT canvas
2. Platform control plane
3. Knowledge base service
4. Search and vector indexers
5. Reviewers and approvers
6. Audit and analytics

# Preconditions
1. The author is authenticated and mapped to an organization account and project scope.
2. The canvas has a stable document id in the chat workspace.
3. The knowledge base has namespaces, for example org, project, and collection.

# Step by step flow
1. Author chooses Push to Knowledge Base in the canvas.
2. Client sends a push request through MCP to the platform control plane with the canvas id and requested destination namespace.
3. Control plane fetches the canvas content and attachments and snapshots them.
4. Content normalization runs. The system converts rich text to canonical Markdown and JSON, fixes headings, removes empty blocks, resolves images to files, and standardizes internal links.
5. Metadata capture runs. The system builds a record with title, summary, tags, taxonomy paths, privacy level, owner, contributors, source canvas id, source agent, model and version, and timestamps.
6. Provenance and integrity are stamped. The system computes a content hash, signs a provenance record with the user identity and the platform identity, and attaches both to the document.
7. Policy checks run. The system evaluates rules for secrets, PII, license compliance for embedded code, profanity filters if required, and file size limits. Warnings can be allowed by policy or upgraded to blocking errors.
8. Diff and review are prepared. If a document with the same slug or id exists, a structured diff is generated. The system creates a change request and routes it to required reviewers based on namespace and sensitivity. If the policy for the target namespace allows direct publish for the author role, the system skips review.
9. Storage write occurs. The normalized content is stored in immutable object storage under the content hash path. The metadata record is written to the knowledge base database. A human readable mirror is committed to a Git repository to provide simple history and external portability.
10. Indexing begins. The search indexer tokenizes the document and updates the inverted index. The embedding service chunks the text, computes embeddings, and writes them to the vector index with pointers back to the exact section ids. A knowledge graph pass extracts entities, relations, and links to existing nodes.
11. Cross links and backlinks are updated. The system rewrites internal references to stable slugs and records backlinks for discovery.
12. Publication happens. The active pointer for that slug moves to the new version when approved. Static site and API caches are invalidated.
13. Notifications and webhooks fire. Subscribers receive an event with title, summary, link, author, diff summary, and tags. Optional webhooks notify external systems.
14. Audit and analytics are stored. Every stage emits events to the telemetry pipeline for later inspection, including who pushed, what changed, and how policy gates were applied.
15. Rollback is always available by moving the active pointer to a prior version, since content objects are immutable.

# Data model essentials
1. Document id which is a stable uuid
2. Canonical slug per namespace
3. Version which is a monotonic integer
4. Content object address which is the content hash path
5. Metadata which includes title, summary, tags, taxonomy, owner, contributors, privacy level, created at, updated at, and source canvas id
6. Provenance which includes user id, agent id, model id, signatures, content hash, and timestamps
7. Attachments which are stored as separate objects and referenced by id and path

# MCP surface for agents
1. kb.push accepts content, metadata, and target namespace and returns a change request id and the computed hashes
2. kb.status accepts an id and returns current state such as pending review, published, or rejected with reasons
3. kb.get accepts a slug or id and returns the latest published version or a specified version
4. kb.search accepts a query and optional filters for namespace, tags, owner, and time ranges
5. kb.diff accepts two versions and returns a structured diff with section level granularity

# Review modes
1. Direct publish for low risk namespaces and trusted roles
2. One reviewer for normal risk documents
3. Two reviewers for sensitive documents with secret scanning or PII warnings

# Policy gates
1. Secrets scanner
2. PII classifier
3. License checker for code blocks
4. Size limits and media type whitelist
5. Namespace specific rules such as mandatory tags

# Indexing details
1. Text is chunked by heading and paragraph and given stable section ids
2. Embeddings include section id, heading path, and document id
3. Search index stores token positions to support snippet previews
4. Knowledge graph stores entity nodes with links to sections that assert those relations

# Publication targets
1. Human reader portal
2. Agent facing API and MCP resources
3. Static export and Git mirror for offline use

# Error handling and retry
1. Every stage is idempotent using the content hash as the key
2. Failed stages schedule retries with backoff and emit alerts
3. Partial success never publishes, and the system keeps the change request open until all stages succeed

# Roles and permissions
1. Author can push and update within allowed namespaces
2. Reviewer can approve or reject with comments
3. Admin can manage namespaces, policies, and roles

# Minimal MVP plan
1. Implement kb.push and kb.get
2. Store normalized Markdown and metadata in object storage and a simple table
3. Create a basic search index and embedding pipeline
4. Provide a one step direct publish path
5. Emit provenance and audit events

# Example end to end
1. Author presses Push to Knowledge Base
2. System normalizes, stamps provenance, runs policy checks, writes storage, and indexes
3. If direct publish is allowed the document appears in the portal and is immediately queryable by agents
4. If review is required the document waits for approval and then publishes automatically

