# MCP-First Drafts (BYOB) — Plan

**Date**: 2026-04-19
**Design source**: effort `mcp-drafts-agent-composition` description
**Parent effort**: `mcp-drafts-agent-composition` (already created under `forum-launch`)

## Problem

Current forum UX assumes human-authored posts typed into the web UI. Most users will interact with their own LLM + MCP and compose via agent rather than hand-writing posts. Without a first-class agent-composition path, we optimize for a shrinking interaction mode and leave the dominant one to ad-hoc prompts. The forum should primarily be a *view + sign* surface; composition happens agent-side. Users should be able to paste screenshots (e.g. for bug posts) and have the image carried through to publication.

## Discovery

Grounded against `/data/Dev/Open Systems/`:

- **Vault posts**: `vault/src/posts.rs` + `vault/src/api.rs:62-64` — `POST /v1/posts`, `GET /v1/posts/:hash`, `GET /v1/posts`. `VaultPost` already has `promotion_auth` (pre-signed authorization, currently unused), `promoted` bool, `on_chain_post_id`, `auto_promote_attempts`. Storage: plaintext JSON at `data_dir/posts/<hash>.json`.
- **Content store**: vault already stores arbitrary blobs by content hash — images are just another blob. No changes needed to the content layer for image support.
- **MCP post tools** (`opensystems/mcp/src/os_mcp/server.py:226-350`): `os_create_post`, `os_create_post_with_content`, `os_store_content`, etc. — all publish immediately. No draft/presign state.
- **Frontend compose** (`opensystems/frontend/actions.js:54-88`, `identity.js:50`): modal → browser-side secp256k1 signing → `PUT /v1/posts`. Signing path is solid and reusable.
- **Auto-promote + review** (`vault/src/auto_promote.rs`, `contracts/forum/src/contract.rs`): vault daemon submits `AutoPromote` after review period. Draft → published-post flow reuses this pipeline entirely once the draft is signed.
- **Private partition / encryption** (`DEV/docs/brainstorm/017-vault-public-private-boundary.md`): **designed only, not implemented**. Full encryption scheme is out of scope for drafts MVP — local drafts can be plaintext on the user's own device, *provided replication code is explicitly segregated* so drafts don't leak to the DHT/GossipSub.
- **Subject rules via MCP**: `os_get_subject` returns minimal context (name, description, parent, counts). No certification/rules surface exists. Agents can technically still compose without this — subject rules surfacing is a quality gate, not a blocker.

**Discrepancy**: the effort description raised "drafts live in vault private partition" as an option. Reality: private partition isn't built. MVP plan treats drafts as a *segregated local directory* (not the encrypted private partition) — simpler, sufficient for single-device single-user, and doesn't block on the larger encryption effort.

## MVP Scope

### 1. Draft storage in vault
**Why MVP**: Smoke test — no feature without it. Core dependency for every other MVP item.
**Blocked by**: none
**Effort description**: Vault has no draft concept today. Add `data_dir/drafts/<draft_id>.json` storage with a `VaultDraft` struct: `draft_id` (UUID), `author_pubkey`, `title`, `content`, `tags`, `image_refs: Vec<String>` (content hashes), `created_at`, `updated_at`, `composed_by: Option<String>` (agent attribution string, optional). Explicit guarantee: draft store is **never** exposed to GossipSub, DHT, or any replication path — enforce via code review and a test that asserts the drafts directory is not walked by sync code.

### 2. Draft HTTP endpoints on vault
**Why MVP**: Smoke test — MCP tools + frontend both depend on this HTTP surface.
**Blocked by**: 1
**Effort description**: Add to `vault/src/api.rs`: `POST /v1/drafts` (create), `GET /v1/drafts` (list, filtered by author pubkey), `GET /v1/drafts/:id`, `PATCH /v1/drafts/:id` (edit title/content/tags/images), `DELETE /v1/drafts/:id`. Authentication: existing pattern (author signature on mutations, or local-only assumption for single-user vault — match whatever `/v1/posts` does).

### 3. Image support in drafts
**Why MVP**: User explicitly flagged as important — bug-post use case depends on pasting screenshots. Also the cleanest proof that agent-composed posts work end-to-end.
**Blocked by**: 1
**Effort description**: MCP tools accept image content as base64 + mime type (or array of such). On receipt: call existing `os_store_content` equivalent to hash-and-store each image in the vault content store, collect hashes into `image_refs`. Frontend renders images from `/v1/content/:hash` when displaying drafts and published posts. Post content format: reuse whatever inline-image convention the forum already uses (or Markdown `![](hash)`), ensuring it survives draft → publish unchanged.

### 4. MCP draft tools
**Why MVP**: The point of the whole effort. Without these, there's no agent-composition path.
**Blocked by**: 2, 3
**Effort description**: Add to MCP server: `os_create_draft(title, content, tags, images?, composed_by?)`, `os_list_drafts(author?)`, `os_get_draft(draft_id)`, `os_update_draft(draft_id, ...)`, `os_discard_draft(draft_id)`. **No `os_publish_draft` tool** — publishing requires the user's private key and must happen in the frontend. The MCP tool docstrings must clearly state this boundary and guide the agent to tell the user "draft ready, open the drafts tab to review and sign."

### 5. Frontend drafts view
**Why MVP**: Smoke test — the user's review-and-sign moment has to exist somewhere.
**Blocked by**: 2, 3
**Effort description**: New `/drafts` route (or tab). Lists drafts (newest first) with title, tags, timestamp, `composed_by` badge if present. Click → detail view showing full content + inline images. Two actions: **Sign & Publish** (reuses existing signing + `PUT /v1/posts` flow, then `DELETE /v1/drafts/:id`), **Discard**. Edit is a nice-to-have within this effort — defer inline editing UI if it adds scope; users can update via MCP or delete+recreate.

### 6. Half-screen compose UX affordance (lightweight)
**Why MVP**: The UX framing the user identified — forum on one side, agent on the other. No new UI surface; just ensure nothing breaks at narrow viewport widths and the `/drafts` route is prominent.
**Blocked by**: 5
**Effort description**: Audit the feed, post-detail, and drafts views at ~720px-wide viewport (half a 1440 screen). Fix any broken layouts. Surface drafts count in the nav when > 0. This is a polish pass, not a new UI mode.

## Deferred Scope

### Efforts

#### Private-partition encryption for drafts
**Why deferred**: Optimization — drafts are local to the user's own vault; plaintext-with-replication-segregation is sufficient for single-device MVP. Encryption matters when vault is hosted or shared.
**Origin**: design doc (vault-public-private-boundary brainstorm, effort open question)
**Promotion trigger**: Hosted vault ships, OR multi-device sync ships, OR a real threat model emerges (device shared with untrusted users).
**Effort description**: Wire drafts into the vault private partition once implemented. Encrypt `VaultDraft` bodies per-blob with CEK, store metadata in encrypted index. Inherits from the broader vault-public-private-boundary effort.

#### Subject-rules surfacing for MCP
**Why deferred**: Configurable behavior for a scale not yet reached. `os_get_subject` returns enough for the agent to caution the user; deep rule surfacing matters when certifications actually exist and gate posting.
**Origin**: effort description (open question: rule-aware composition)
**Promotion trigger**: Certification registry ships with real certifications attached to subjects, OR the first audit-caused slash against an agent-composed post.
**Effort description**: Extend `os_get_subject` (or add `os_get_subject_rules`) to return attached certifications, XP thresholds, and any moderation policies so agents can warn users about specific risks (flag probability, required competence, etc.) before drafting.

#### Agent-attribution signal ("drafted by agent" marker)
**Why deferred**: Adversarial origin — the homogenization-risk concern was raised during the preceding chat discussion, not in the user's core problem statement. Can add later without data migration (`composed_by` field is already in MVP draft schema, just not surfaced on published posts).
**Origin**: chat discussion (my own flag, not user-originated)
**Promotion trigger**: Observed homogenization in real posts (feed reads like one voice), OR community asks for an "AI-composed" filter/disclosure.
**Effort description**: Propagate `composed_by` from draft → published on-chain post (either as a post field or via a parallel attestation). Design the UI surface (badge? filter? opt-in?).

#### Diff-highlighting in sign-and-publish review
**Why deferred**: Edge case — users will read drafts regardless of whether diffs are highlighted. Valuable only if we see real "agent drafted, user edited, user signed without noticing edits reverted" problems.
**Origin**: effort description (open question)
**Promotion trigger**: Report of user confusion around what they signed vs. what the agent drafted.
**Effort description**: When user edits a draft in the frontend review view, compute a diff against the agent's original draft and highlight changes before the Sign button is enabled.

#### Read-before-sign friction nudges
**Why deferred**: Configurable behavior; start with the simplest sign button and see whether rubber-stamping becomes a real problem.
**Origin**: effort description (open question)
**Promotion trigger**: Audit cases where the signer clearly didn't read what they signed; OR a community governance request for attestation friction.
**Effort description**: Nudges like scroll-to-bottom-before-sign, per-tag confirmation for sensitive subjects, summary-of-changes at top. Add iteratively based on evidence.

### Notes (one-shot details within other efforts)

| Item | Why deferred | Promotion trigger |
|------|-------------|-------------------|
| Draft expiration / GC | Optimization — disk is cheap, users discard themselves | Drafts dir grows unbounded in practice |
| Multi-device draft sync | Edge case — single-device MVP is fine | Vault sync protocol ships AND users ask for cross-device drafts |
| Drafts search / filter in UI | Optimization — list is short at MVP scale | Users have >20 drafts and complain |
| Inline draft editing in frontend (vs. MCP-only edit) | Edge case — users will edit in their agent pane | Friction reports from users who want to tweak without pinging the agent |
| `os_get_post` reply-context completeness | Probably already sufficient | Agent-drafted replies routinely miss thread context |

## Triage Rationale

Six MVP items, five deferred efforts, five notes — roughly 55% deferred. The pattern: the core pipeline (storage → endpoints → MCP tools → frontend review → existing signing reuse) is small and linear because the frontend already signs, the vault already stores, and the auto-promote path already works. Most "good ideas" that surfaced in design thinking — encryption, attribution UX, anti-homogenization, signing friction — are genuine improvements but are either (a) optimizations for scale we haven't reached or (b) depend on unbuilt systems (private partition, certifications). They live in deferred efforts with specific promotion triggers so the reasoning isn't lost. The user's explicit "images are important" ask promoted image support from "nice" to MVP on the spot — it's central to the bug-report scenario that makes agent-composition valuable in the first place.
