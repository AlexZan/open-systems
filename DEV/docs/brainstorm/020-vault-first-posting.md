# Brainstorm 020: Vault-First Posting

**Date:** 2026-03-30
**Method:** Brainstorm → Critic Chain (5 rounds, 3 FATAL + 13 HIGH + 18 MODERATE, all FATAL/HIGH resolved)
**Status:** Converged
**Supersedes:** Direct-to-chain posting as the only path. Extends brainstorm 005 (on-chain vs off-chain boundaries).

---

## Executive Summary

Posts start in the vault (free, off-chain). They only go on-chain when someone with XP upvotes them. The upvote IS the promotion — no separate action. The chain is the value layer (only community-valued content). The vault is the content layer (everything, freely). This removes posting friction (no gas, no PoW for posting, no subject restrictions) while keeping chain state clean.

---

## Historical Lineage

This idea was brainstormed years ago in multiple forms:

**"Thoughts on forum staging.md" (DATA-DUMP, ~2020-2021):**
> "Form staging is the thought that before a post makes it on the block chain, it can be posted in a staging area which will only be on the gossip network."
- Posts in staging, no XP flow, move to chain after consensus group approval
- Author manually requests posting out of staging after 1 day

**Brainstorm 005: On-Chain vs Off-Chain Boundaries (2026-03):**
> "Tags start as metadata on the off-chain post, but become on-chain data when they're part of an experience transaction."
- Post lifecycle: content off-chain → hash on-chain → XP flows
- Chain = truth and consensus. Off-chain = content and bulk data.

**Decision 011: Vault-Local Tags (2026-03):**
- Two-tier tags: soft (vault) and hard (on-chain subjects)
- Novel tags live off-chain until community demonstrates they deserve on-chain status

### Why This Version Instead of the Old Ones

| Old (forum staging) | New (vault-first) | Why better |
|---|---|---|
| Author manually requests "post out of staging" after 1 day | Upvote from XP-holder triggers on-chain registration automatically | No manual step. The community decides, not the author. |
| Consensus group can block promotion | No blocking — upvote is the quality signal | Simpler. No gatekeeping committee. One person with XP saying "this is worth it" is enough. |
| Staging is a separate concept from the forum | Vault IS the staging area | No new infrastructure. The vault already exists as the content layer. |
| Separate "promote" action | Upvote = promotion (same button, same action) | Zero additional UX complexity. User doesn't need to learn a new concept. |

---

## Final Design

### Core Principle

**Vault = content layer. Chain = value layer.** Posts live in the vault by default. The chain only stores content that the community has valued (via upvote from an XP-holder).

### Flow

1. **Post (vault-only):** User creates a post → vault requires PoW (~2s, difficulty anchored to on-chain parameter) → stored with content hash, title, author pubkey, tags (any tags, normalized, no subject validation), timestamp, author signature, PoW proof, and pre-signed promotion authorization. No chain TX. Announced on GossipSub `posts/<tag>` topics + `posts/new`.

2. **Discovery:** Vault feed API (`/v1/posts`) aggregates local posts + posts from subscribed GossipSub topics from multiple peers. Content verifiable via hash + author signature + PoW proof (difficulty verified against chain parameter).

3. **Upvote = Promotion:** When an XP-holder upvotes a vault-only post, the upvote TX also creates the on-chain forum record. Same button as upvoting an on-chain post — the system handles the difference. The upvoter stakes 1 XP (returned unless post ruled spam/fraud — same as vouch rules). The post's pre-signed promotion authorization (embedded at creation) authorizes any XP-holder to promote without needing the author online. Idempotent — if content_hash already on-chain, just adds upvote.

4. **Direct-to-chain (fallback):** Existing `create_post` path remains. Requires existing subject tags + PoW for 0-XP accounts. This is for users who want to go directly on-chain with established subjects.

5. **Tags:** Free at vault level (normalized: lowercase, alphanumeric + hyphens). On promotion, tags matching on-chain subjects become hard tags. Unmatched tags stored as soft tags in vault content blob. No seed XP until matching subjects exist.

6. **Post-promotion:** Enters current XP pipeline (whichever model is active). Promotion counts as vouch #1 (the upvoter vouched for quality by staking XP). Standard review period applies.

### What This Solves

- **Zero-friction posting:** No gas, no subject restrictions, any tags
- **Pizza recipe problem:** Jake can post about cooking without a "cooking" subject existing on-chain
- **Chain stays clean:** Only community-valued content on-chain
- **Subject emergence:** If enough people post about "cooking" in vault, the community can create the subject through governance — driven by real demand
- **Aligns with vault architecture:** Vault is already the content layer (brainstorm 017), this makes it the posting layer too

### Spam Defense

- Vault PoW per post (~2s, chain-anchored difficulty)
- Asymmetric PoW version acceptance: harder-than-current always accepted, easier only during brief grace period after difficulty increase
- GossipSub peers reject announcements without valid PoW
- Author vault never GCs own posts; peer caches have configurable TTL
- Upvoter/promoter stakes 1 XP (lost on spam/fraud)
- Random announcement jitter (1-10 seconds) mitigates activity-pattern correlation

### Self-Promotion Prevention

- Enforced via 90-day first-degree on-chain interaction exclusion between promoter and author (same as vouch independence)
- Best-effort sybil defense, not categorical guarantee — determined sybils with separate accounts that avoid on-chain interaction for 90 days can circumvent
- Real defense is downstream: audit pipeline catches bad content regardless of who promoted it

### Content Availability

- Author's vault never GCs their own posts (canonical source)
- Peer caches are ephemeral (TTL-based)
- If content unavailable at audit time → "content unavailable" resolution: no XP awarded, post flagged, promoter stake returned
- Pre-signed promotion authorization embedded at creation → author doesn't need to be online for promotion

---

## Critic Chain Scorecard

| Round | FATAL | HIGH | MODERATE | Key Fixes |
|-------|-------|------|----------|-----------|
| 1 | 2 | 5 | 5 | Vault PoW for spam, PromotePost idempotent, author signature verification, tag resolution, GossipSub metadata, multi-peer feed |
| 2 | 1 | 4 | 3 | Self-promotion fallback (7d + PoW), tag normalization, promoter stakes XP, author vault never GCs, PoW chain-anchored |
| 3 | 0 | 2 | 4 | Removed self-promotion (unnecessary), promotion = vouch rules (stake returned unless spam/fraud) |
| 4 | 0 | 2 | 3 | Pre-signed promotion auth (offline author support), promotion counts as vouch #1, two paths have different vouch states (intentional) |
| 5 | 0 | 0 | 3 | Converged |
| **Total** | **3** | **13** | **18** | **All FATAL/HIGH resolved** |

## Remaining MODERATE Issues (Implementation Notes)

1. Pre-signed promotion authorization has no expiry — accept as immutability norm or add optional expiry field
2. "90-day interaction exclusion" scoped to on-chain interactions only (vault interactions not visible to chain)
3. GossipSub announcement jitter: uniform random 1-10 seconds
4. Multi-topic announcements may enable activity correlation on low-traffic tags
5. Per-vault storage quotas are local-only, no network enforcement
6. `posts/new` catch-all topic may bottleneck under high volume

## Key Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Where posts live | Vault first, chain on upvote | Zero friction posting, chain stays clean |
| Upvote = promotion | Single action, no separate "promote" | No additional UX complexity |
| PoW for vault posts | Yes, ~2s, chain-anchored | Spam defense that survives Golden Rule (compute is scarce) |
| Self-promotion | Removed | If no XP-holder thinks it's worth it, vault is fine. Direct-to-chain exists as fallback. |
| Author online for promotion | Not required | Pre-signed authorization at post creation |
| Promotion = vouch #1 | Yes | Promotion IS a quality signal, should count toward vouch pipeline |
| Two posting paths | Vault-first + direct-to-chain | Vault-first for freedom, direct for established subjects |
