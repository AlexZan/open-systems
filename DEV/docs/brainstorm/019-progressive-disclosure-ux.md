# Brainstorm 019: Progressive Disclosure UX

**Date:** 2026-03-27
**Method:** Conversational brainstorm
**Status:** Captured — ready for implementation

---

## Problem

First-time visitors see a dashboard with stats, subjects, governance proposals — all meaningless without context. The UI leads with complexity. A friend opening the link has no idea what they're looking at.

## Insight

The system has no ego. It's not about itself — it's about whatever the community discusses. The app shouldn't explain itself with tutorials or onboarding flows. It should be **self-explanatory through progressive disclosure**. Understanding scales organically.

## Design: Progressive Disclosure Layers

### Layer 0 — First Visit (Feed)

The default view is a **feed of posts**. That's it. Looks like any social media feed. Scroll, read, tap to expand.

- No dashboard
- No stats
- No governance tab
- No subject filters (yet)
- Just content — titles, authors, snippets, tags

This is the only thing a first-time visitor sees. It should feel immediately familiar — like opening any social app.

### Layer 1 — Interest Develops (Tags → Subjects)

Posts have tags visible on them (rust, governance, gardening). User taps a tag → sees posts filtered by that tag. This is how subjects are discovered — not through a "Subjects" page, but through content.

- Tag taps filter the feed
- No need to explain "what is a subject" — it's just a tag filter
- Subject descriptions appear in the filtered view header (if they exist)

### Layer 2 — Wants to Participate (Identity)

User wants to upvote, reply, or post. "Join" is visible but unobtrusive (floating action button, or inline prompt on interaction attempt).

- Tap "Join" → create anonymous identity in 10 seconds (name + password)
- No email, no verification, no friction
- Immediately can post and upvote
- Identity persists in browser (encrypted localStorage)

### Layer 3 — Gets Invested (Governance Discovery)

User has been posting, getting upvotes, earning XP. Governance proposals start appearing in the feed (they ARE posts, just a different type — tagged with "proposal" or similar marker).

- User sees "Proposal: Add woodworking subject" in their feed
- Taps it, sees vote counts, description
- If they have XP, they can vote
- Governance is discovered through the feed, not through a separate tab

### Layer 4 — Power User (Full Navigation)

User who actively participates discovers the full nav organically:

- **Subjects** — browsing by topic, seeing community structure
- **Governance** — active proposals, voting, parameter changes
- **Projects** — ongoing development, contributions
- **Profile** — XP balances, activity history, device management
- **Vault** — what they're sharing, storage, connected peers

These are all accessible via nav, but the nav is **secondary** to the feed. Advanced features reveal themselves through participation, not through upfront navigation.

## Implementation Principles

1. **Feed is the entry point.** Default route `/` shows the feed, not a dashboard.
2. **Tags are the discovery mechanism.** No separate "subjects" page needed for new users. Tags on posts ARE the subject system.
3. **Join is contextual.** Show the join prompt when the user tries to do something that requires identity, not as a landing page CTA.
4. **Governance is content.** Proposals appear in the feed alongside posts. No separate governance tab needed for discovery.
5. **Nav is progressive.** Start with minimal nav (just a logo). Add tabs as the user's participation level increases. Or: full nav exists but isn't the focus — the feed is.
6. **No stats on first visit.** Stats (post count, proposal count, block height) are for power users. They mean nothing to newcomers.
7. **No tutorials, no tooltips, no modals.** If something needs explaining, the design is wrong.

## Current App vs. This Design

| Current | Progressive Disclosure |
|---|---|
| Dashboard with stats as landing page | Feed of posts as landing page |
| Subjects page with tag list | Tags on posts, tap to filter |
| Governance as separate tab | Proposals in the feed |
| Join button prominent on landing | Join prompt when user tries to interact |
| All nav visible immediately | Nav secondary to feed |
| Explanation through labels | Understanding through use |

## Open Questions

- Should the feed be chronological, or weighted by some signal (upvotes, recency, subject diversity)?
- How do governance proposals appear in the feed? Inline with different styling? Or only after the user has some XP?
- Should the nav tabs reveal progressively (e.g., governance tab appears only after first vote) or always be there but de-emphasized?
- How does the feed look when there are only 9 posts? Need enough content for the feed to feel alive.
