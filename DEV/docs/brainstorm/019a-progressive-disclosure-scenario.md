# Scenario: Jake's First Week on Isonomia

---

## Day 1 — Browsing

Jake's friend Maria sends him a link: `https://isonomia.app`

He opens it on his phone. He sees a feed — posts about rust programming, gardening, governance ideas, woodworking projects. It looks like any social feed. Dark theme, clean. He scrolls.

He taps a post titled "Async Rust Patterns for Beginners." It expands. He reads it. Good stuff. He notices a small tag that says `rust` at the bottom. He taps it. The feed filters to show only rust posts. He reads a few more.

There are no buttons he doesn't understand. No stats. No governance. No XP counters. No upvote arrows. Just posts and tags.

He closes the app.

---

## Day 2 — Joining

Jake comes back. He finds a post about a Rust CLI tool and wants to write something about it. He taps... but there's no way to post. A subtle inline message appears:

> *Create an identity to participate* — **join**

He taps "join." A simple form: pick a display name, set a password, confirm password. No email. No verification. No "what are you interested in?" questions. 15 seconds. Done.

The feed looks the same — still just posts and tags. But now there's a floating "+" button at the bottom right. He taps it. A simple post creation form: title, content, pick tags. He writes a short post about a CLI tool he built. Tags it `rust`. Submits.

His post appears in the feed immediately. No waiting period. No approval needed. It's just there, like posting on any platform.

Nothing else changed. No new buttons. No new features. He can browse and post. That's it.

---

## Day 5 — Someone Upvotes His Post

Jake opens the app. His post about the CLI tool has a small indicator: "3 upvotes." He didn't even know upvoting existed — he's never seen an upvote button because he has no XP.

He taps his name in the header. His profile shows something new:

> **rust** — 3 XP

A brief contextual note appears the first time he sees this:

> *Experience (XP) is earned when people with experience in a subject upvote your work. XP gives you more ways to participate.*

That's it. One sentence. He now understands XP because it happened to him, not because someone explained it in advance.

---

## Day 6 — New Capabilities Appear

Jake opens the feed. Something changed. On some posts tagged `rust`, he now sees a small upvote arrow that wasn't there before. It appeared because he has XP in `rust` now.

He taps it on a post he liked. A brief note: "Your endorsement carries weight — you have experience in this subject."

He gets it: he earned credibility, now his opinion counts. No one lectured him about "weighted voting" or "experience-based governance."

---

## Day 9 — Auditor Registration

Jake has been upvoting posts and earning a bit more XP. In his profile, he notices a new section that wasn't there before:

> **Review posts to earn XP**
> Sign up for subjects you know about. When posts need review, you may be randomly selected.
> [rust] [woodworking] [+ more subjects]

He taps `rust` and `woodworking`. He understands what this means because he already knows what XP is and why it matters. He's making an informed choice — opting in because he wants to, not because the app pushed him during onboarding.

---

## Day 11 — First Audit

Jake opens the app. There's a subtle notification:

> *A post in `rust` needs your review* — **Review**

He taps it. He sees a post someone else wrote — a tutorial about error handling. A simple question:

> **Does this post belong in `rust`? Does it violate any rules?**
> [Approve] · [Flag as violation]

Not "is this valuable?" — that's for upvotes. The audit asks: does it belong here, and does it follow the rules? Jake reads it. Legitimate rust content, no spam, no tag abuse. He taps "Approve."

A small animation: **+1 XP in rust** appears briefly and fades.

---

## Day 14 — Discovering Governance

Jake scrolls his feed and sees something different — a post with a subtle blue border:

> **Proposal: Reduce review period in `rust` from 24h to 12h**
> *Submitted by os1a7f...3e2d · 5 votes so far*

He taps it. Someone is proposing a change to how the rust subject works — shorter review windows for posts. He's been posting and reviewing in rust for two weeks. He has an opinion on this.

Jake has accumulated enough total XP across subjects that he's earned governance weight (every 100 subject XP = 1 governance XP, computed automatically). A "Vote" button is visible.

He votes yes. He thinks 12 hours is plenty.

He never navigated to a "Governance" tab. He never read a guide about how governance works. The proposal was just a post in his feed about something he cared about, and voting was just tapping a button.

---

## What Jake Never Had to Learn Upfront

- What XP is (he discovered it when someone upvoted his post)
- What auditing is (he opted in after understanding XP, did it before knowing the word)
- What governance is (proposals were just posts in his feed)
- What subjects are (they were just tags he tapped)
- How the blockchain works (he never saw block heights or chain IDs)
- What a vault is (his content just... existed)

Every concept was introduced **the moment it became relevant to him**, through action, not explanation. He gave informed consent at every step — not through a terms-of-service wall, but by understanding what he was opting into before he did it.

---

## What the System Knows About Jake

- He's a reliable reviewer in rust and woodworking (he opted in after understanding the system)
- He upvotes good content (his vote history)
- His identity is anonymous (just a keypair in his browser)
- His XP was earned through community upvotes and audit participation — no admin granted it, no algorithm guessed it
- His governance weight was computed from his participation, not assigned

---

## Design Principles This Scenario Demonstrates

1. **If you can't do it, you can't see it.** No upvote buttons at 0 XP. No governance voting without governance XP.
2. **No subject selection at signup.** That comes later, when the user understands what they're opting into.
3. **Informed consent at point of action.** XP is explained the first time you earn it. Auditing is explained when you opt in. Not before.
4. **Auditors are referees, not critics.** They check rule compliance and subject relevance. Value is decided by upvotes.
5. **Governance XP is derived.** 100 subject XP = 1 governance XP. No separate currency, no burning, no minting.
6. **No tutorials, no tooltips, no documentation pages.** If something needs explaining, the design is wrong — except for one-sentence contextual notes at the moment of discovery.
