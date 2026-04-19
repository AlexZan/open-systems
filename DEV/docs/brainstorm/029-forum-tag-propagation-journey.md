# 029 — Forum Tag Propagation Journey (Retrospective)

**Date:** 2026-04-19
**Status:** Documented for the record. No implementation. Related efforts closed.
**Related docs:** 027, 027-critic-chain, 028, 028-critic-chain, 027-028-implementation-plan.

---

## Outcome (read this first)

**Decision: ship nothing. Current flat explicit tagging is sufficient for MVP.**

Authors pick their tags at post time. Each tag earns 1 XP on auto-promote. Existing FlagPost handles misattribution. No propagation, no hierarchy, no automation. The tag network grows organically through posting behavior; when enough co-occurrence data accumulates, later phases can add vector-embedding-based triangular-blob propagation, LLM-assisted tagging, or other automation layers on top of the existing substrate.

**What NOT to build:**
- Tag hierarchy with parent-chain propagation (027)
- Geometric-decay XP math (critic-chain artifact, not the original ask)
- Activation flag + bootstrap window + AdminSeedParent (defense-in-depth against a threat model that doesn't exist at MVP scale)
- ReportTagMisattribution stake-based jury (existing FlagPost is sufficient)
- ProposeParent challenge windows (no tree means no parents to propose)
- BURN_DEBT, 24h cooldowns, abandonment penalties, triple-keyed cooldowns (all defenses against tree-based attacks that don't apply)

**What to carry forward** as known-good thinking for later:
- Tags are the author's contractual declaration of value, not discovery metadata
- Real bugs are cross-cutting; trees systematically under-credit cross-domain work
- The triangular-blob model (3+ vertices in vector space) is the right long-term propagation shape
- Organic co-occurrence-based network emergence > governance-decreed hierarchy
- LLM-assisted tagging is a strategic paradigm shift worth its own brainstorm, not a tactical feature

---

## How this conversation arrived here

### Act 1: The original ask (simple)

Effort `forum-tag-tree-xp-propagation` was opened with a clear ask: when someone posts tagged `#waybar`, they should also earn some XP in `#gui`, `#os`, `#linux` — the ancestors. Without this, the incentive loop collapses to one-XP-per-bug and reporters have no reason to tag well. Curator-audit at approval time was mentioned as the abuse defense.

Implicit in the ask: use existing FlagPost as the curator-audit gate, keep everything else simple.

### Act 2: The over-engineering spiral (what the critic chains did)

Two designs were drafted (027 for semantics, 028 for the audit gate) and put through adversarial critic chains totaling 9 rounds.

Round 1 of 027 flagged "bounded issuance" as a HIGH concern. I accepted the framing and designed geometric decay (`N >> k` per level). That immediately broke the original ask: at N=1 with integer math, only the leaf earns XP — the propagation becomes invisible, which is the opposite of what was wanted. Subsequent rounds never questioned this assumption and instead built elaborate defense-in-depth around it: activation flags, bootstrap windows, ProposeParent with challenge juries, BURN_DEBT queues, triple-keyed cooldowns, abandonment penalties, target-subject jury exclusion.

By the time both chains converged (4 + 5 rounds, 11 + 20 HIGH issues resolved), the design had grown to 9 MVP efforts plus 10 deferred efforts. None of it was wrong in isolation — each fix correctly addressed its critic's finding. The problem was cumulative: the system I designed was solving a threat model much larger than the one that exists at the project's actual scale.

**Key failure mode:** I treated the critic chain's adversarial questions as requirements instead of as threat-model stress-tests to negotiate. When the critic asked "is issuance bounded?", the right answer was "no, and that's fine because XP is reputation, not currency." I instead answered "yes, bounded under `2N`," and that cascade drove the whole over-engineering.

### Act 3: The course correction

User pushback pointed out the divergence: "this is different than what we were trying to build... kind of the opposite of what we said should happen, the original spec was to just use the existing pathway for exp, always 1 exp."

The diagnosis: I had adopted the critic chain's framing ("bound the issuance") as a constraint, which turned the simple "1 XP per ancestor" into "decay to zero, then invent tiers to make it visible, then defend the tiers against abuse." Every layer above "1 XP flat to ancestors" was unnecessary for the ask.

### Act 4: The reframe (brainstorm, not implementation)

Rather than just reverting to flat-1-XP-per-ancestor tree propagation, the conversation opened up the whole question of tag structure:

- **Network vs hierarchy:** Tags aren't naturally hierarchical. `#waybar` relates to `#linux`, `#hyprland`, `#wayland`, `#gui`, `#bar` — many neighbors, no single "parent." Wikipedia categories are a DAG for this reason. Forcing a tree creates political choices ("who's the parent?") that the network model side-steps.

- **Organic emergence:** The tag network could form from co-occurrence of tags on auto-promoted posts, rather than being decreed by governance. If 3+ authors co-tag `#waybar` and `#linux` over time, the system learns they're related. No explicit seeding needed.

- **LLM-assisted tagging:** A more radical paradigm shift. Instead of users picking tags, an LLM reads the post and assigns tags from the shared network. Same model for everyone = same taxonomy for everyone = fairness by construction. Auditors verify the LLM's output when confidence is low. This is probably where the long-term system should go, but it requires answering hard questions about compute economics, determinism, and model governance — not MVP scope.

- **The triangulation insight:** Author picks 3+ "vertices" in the tag network representing the poles of their contribution. These get full XP. Tags inside the "triangular blob" (interior + halos around each vertex) get fractional XP based on vector distance. Self-limiting: big-spread vertices = thin fractional XP (honest tagging is incentivized); small-spread vertices = concentrated credit in a tight domain.

- **The reframe that matters most:** Tags aren't for discovery or grouping. They're the author's signed declaration of where they claim contribution value. Everything else (propagation, networks, triangles, decay) is the *system's response* to that declaration. Separating those two concerns is the actual insight.

### Act 5: The grounding

Two real bugs from the effort graph were walked through each proposed model:

- **`fix-waybar-power-profile-cpu-spin`** — touches waybar, D-Bus, GLib, Python, power management. None of those share a parent chain. Tree model would credit only waybar's parent chain (gui → os → linux), missing the D-Bus and power-management dimensions entirely.

- **`query-knowledge-new-nodes-invisible`** — touches knowledge-network, embeddings, search, Rust, MCP, voyage-4 vs nomic-embed-text. Also no single parent chain fits. `#knowledge-network` has no obvious parent; embeddings and search are parallel concerns, not ancestors.

**Both bugs are inherently cross-cutting.** Trees under-credit both. Networks are closer but require accumulated co-occurrence data to work well. Triangular blobs are the right long-term shape but require vector embeddings, which require model governance.

### Act 6: Landing

The conclusion from the ground-truth exercise: **flat explicit tagging is the real MVP.** Author picks 3–5 tags, each gets 1 XP, FlagPost gates misattribution. Dead simple. No automation (the original ask's automation goal is deferred until the tag network has real co-occurrence data to drive it), no propagation, no new contract logic. The existing forum already does this — essentially, the MVP is "change nothing."

The automation goal gets revisited when enough posts exist for a real network to have emerged. At that point, a follow-up effort can add network-aware propagation (vector embeddings + triangular-blob math, co-occurrence-based, or LLM-assisted) on top of a substrate that's already been populated by real user behavior.

---

## Preserved insights (carry forward)

### Tags as contractual value declaration, not discovery metadata

This is the most load-bearing insight of the conversation. Tags aren't metadata for search or grouping — they're the author's explicit declaration of "these are the subjects I'm claiming to have contributed value to." Dispute resolution (FlagPost, or future more-elaborate audit) checks whether that claim is honest. The author's list of tags is a signed statement, not a search aid. Discovery and grouping are downstream concerns that can be solved separately (e.g., via vector similarity over post content, independent of the author's declared tags).

### Real bugs are cross-cutting; trees systematically under-credit them

Two concrete examples prove this: a waybar bug that's also a D-Bus/Python/power-management bug has no single parent chain. A KG bug that's also an embedding/search/model-versioning bug has no single parent chain. Any tag-propagation model that assumes a single parent will systematically under-credit contributions that span domains — which is most real bugs.

### Triangular-blob in vector space is the right long-term propagation shape

Three vertices picked by the author define a 2-simplex in the tag embedding space. Interior tags get fractional XP proportional to barycentric position or vector distance to nearest vertex. Halo effects extend influence outside the strict triangle. Big-spread vertices → thin XP (incentivizes honest, specific tagging); small-spread vertices → concentrated XP (rewards narrow-deep contributions accurately). Self-limiting, gameable only by sacrificing the author's own XP gain.

### Organic network emergence beats governance-decreed hierarchy

The tag network should grow from co-occurrence of tags on auto-promoted posts, not from governance deciding in advance that `#waybar` is under `#gui`. Political choices about parent relationships are unnecessary when the network just observes what subjects actually co-occur in real contributions.

### LLM-assisted tagging is strategically interesting, tactically not ready

Removing the author's agency from tag-picking kills the misattribution attack entirely (you can't pick wrong tags if you don't pick). But it requires answering hard questions about compute economics (who runs inference?), determinism (how does a non-deterministic LLM reach chain consensus?), model governance (who picks and upgrades the model?), and fallback (what happens when compute is unavailable?). Worth its own brainstorm effort at some point; not MVP scope.

### Critic-chain lessons

- Treat adversarial questions as stress-tests to negotiate, not as requirements to satisfy. "Yes, but at our scale that doesn't apply" is a legitimate answer.
- Bounded issuance concerns apply to currency, not to reputation. XP is reputation; bounding it misapplies token economics.
- When a fix requires inventing tiers or sub-systems to make the original mechanic visible again, the fix is probably wrong at the foundation.
- Ship-and-throw-away-for-MVP is a design smell. If the shape is going to change fundamentally later, building the wrong shape now is wasted effort AND carries switching cost.

---

## What was committed to disk

- `027-forum-tag-tree-xp-propagation.md` — converged design for tree-based propagation. Preserved as a record of the over-engineering journey and the specific technical ideas (activation flag, bootstrap window, tree-cut on deprecation) that could be revived for different future problems.
- `027-forum-tag-tree-xp-propagation-critic-chain.md` — 4-round critic chain record.
- `028-forum-tag-curator-audit-gate.md` — converged design for the audit gate.
- `028-forum-tag-curator-audit-gate-critic-chain.md` — 5-round critic chain record.
- `027-028-implementation-plan.md` — MVP-vs-deferred triage that preceded the strategic reset.
- This document (`029-forum-tag-propagation-journey.md`) — the retrospective.

All preserved for future reference. None implemented.
