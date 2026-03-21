# Brainstorm 013: Expression UX & Gate Refinements

**Date:** 2026-03-21
**Status:** Accepted — refinements to Brainstorm 011 and Decision 007
**Relates to:** Brainstorm 011 (Constitutional Governance Model), Decision 007 (Expressive Politics)

---

## Refinement 1: Expression Fading, Not Nagging

**Problem:** Brainstorm 011 specifies 26-epoch expression aging. The naive UX is push notifications: "You expressed on X. Still feel the same?" This is intrusive and trains users to ignore the system.

**Resolution:** Expressions fade passively like ink fading on paper. The system NEVER prompts or reminds users to renew.

- Expressions are visible in the user's profile/dashboard, subtly dimming as they age
- If the user is actively using the system, they encounter their expressions naturally
- Re-signing is a deliberate act: the user sees their fading position and chooses to reaffirm (one action) or lets it expire
- Expiry means "I no longer care enough to weigh in" — a valid, respected outcome
- The system observes absence of renewal; it does not demand attention

**Principle:** The system watches. It does not chase.

**Exception:** Policy enactment events (Scenario 3 — reconfirmation window, policy about to take effect) ARE worth surfacing as notifications/events. These are real events with real consequences. Users can disable these notifications if they choose.

---

## Refinement 2: 1 XP = Participation at Subject Level

**Problem:** Brainstorm 011 specifies "10 subject-scoped XP gate" for subject-level expression. Decision 007 says "default 10 XP, configurable per subject."

**Resolution:** At subject level, **1 XP is sufficient to participate.** No higher gate.

**Reasoning:**
- Subject-level voting is XP-weighted — if Alice has 1 XP and Bob has 3 XP, Bob has 3x the voting power. The weighting IS the sybil defense.
- A sybil attacker with 100 accounts each holding 1 XP has 100 total vote weight. A single real contributor with 100 XP matches them. XP weighting naturally defends against sybil.
- 1 XP = 1 verified contribution = real work. The person showed up, contributed, got approved. They're a participant.
- The 10 XP gate was solving a problem that doesn't exist when voting is weighted.

**Contrast with GER:** The GER track uses 1-person-1-vector (equal voice). There, a sybil attacker with 100 qualified accounts gets 100 equal votes. That's why GER needs the HIGH qualification gate (100+ XP across 3 subjects). The gate matters when voice is equal; it's redundant when voice is weighted.

**Supersedes:** Decision 007 line 41 ("10 subject-scoped XP to express") and line 130 ("Default 10 XP"). Replace with: 1 XP = participation.

---

## Refinement 3: No Configurable Gates at Launch

**Problem:** Decision 007 specifies "Expression gate: configurable per subject. Default 10 XP, but governance can lower it to 1-5 XP for early subjects."

**Resolution:** Do not ship configurable gates per subject at launch. 1 XP for all subjects, no configuration.

**Reasoning:**
- Configurable gates raise the question: who decides? At bootstrap, there's no community to make that call.
- Don't build complexity to solve problems that don't exist yet.
- If real problems emerge (spam, gaming), the community can propose adding configurable gates through governance later.
- Start simple, add complexity only when evidence demands it.

**This does NOT affect GER/CEP gates:** Those remain at the HIGH qualification thresholds defined in Brainstorm 011 (100+ XP across 3 subjects). The GER/CEP gates are justified by the 1-person-1-vector equal-voice model.

---

## Summary of Changes

| What | Before | After |
|------|--------|-------|
| Expression aging UX | Unspecified (implied reminder) | Passive fading, no prompts |
| Subject-level gate | 10 XP default, configurable | 1 XP, not configurable |
| GER/CEP gate | 100+ XP, 3+ subjects | Unchanged |
| Policy enactment notifications | Unspecified | Events are okay, user can disable |
| Configurable gates per subject | At launch | Deferred — add via governance if needed |
