# Brainstorm 015a: Certification Scenarios — User Feedback & Open Design Questions

**Date:** 2026-03-23
**Status:** Brainstorm notes
**Relates to:** Brainstorm 015 (Certification Contract Design), Brainstorm 012 (Certification Anatomy)

---

## Scenario 1 Feedback: Maker Space XP Gate

### The Problem

The certification defines "15 XP in makerspaces subject to use the laser cutter." But a newcomer who just wants to learn hasn't created any value yet. They need training first, and training isn't "value creation" under the standard XP mechanism (post → review → approve → XP minted).

This is a **chicken-and-egg problem**: you need XP to use the equipment, but you need to use the equipment to create value that earns XP.

### Train of Thought: Sub-Cluster XP

Could the makerspace operate as its own sub-cluster with its own XP rules?

- Users earn "makerspace-internal credentials" from completing training modules
- These are NOT main-cluster XP because they weren't earned through the standard value-creation mechanism (post → community vote → XP)
- They are local to the organization — the owner defines what counts as training completion
- If the broader community later recognizes these credentials as legitimate... that creates a complex bridge mechanism (sub-cluster XP → main-cluster XP recognition)

**Conclusion:** This is an important design space but too complex to resolve now. The mechanisms for hierarchical clusters, sub-cluster XP, and cross-cluster recognition need their own brainstorm. Documenting the train of thought for future reference.

### Simpler Answer (For Now)

The XP gate in a certification is a **parameter** — it's configurable and context-dependent:

1. **During incubation**: The owner grants access however they want. Manual training sign-off, in-person assessment, whatever. The chain doesn't enforce the gate — the owner does.
2. **After release**: The community defines its own training→access pipeline. Training modules could be forum posts that earn XP when completed (reviewed and upvoted by the community).
3. **The certification says "15 XP required"** but what activities count toward that XP is the community's decision, not the certification's. A makerspace community might decide that documented training sessions = posts worth upvoting.

The deeper question — how do sub-communities create their own credentialing systems that interface with the main XP system — is deferred.

### Open Design Question

How do organizations create **internal credentials** (training certificates, skill assessments) that:
- Are meaningful within the organization
- May or may not be recognized by the broader network
- Don't conflate "completed training" with "created value for the community"
- Could potentially bridge to main-cluster XP through some recognition mechanism

This connects to: cross-entity certification recognition (open question from 015), hierarchical governance clusters, and the Knowledge Network's role in validating credential equivalence across communities.

---

## Scenario 2 Feedback: Farm Community Value Creation

### Resolution

Yes, value created within a community counts as main-cluster XP. The reasoning:

1. **Value is value regardless of origin.** If someone documents their planting process and posts it to the "gardening" subject, that's a real post. Anyone on the network can find value in it.
2. **The standard mechanism works.** Community members upvote, but the post is on the main network. Anyone can upvote or downvote. Auditing catches exploitation.
3. **AI-assisted documentation is fine.** An AI following a farmer, capturing data, creating a post on their behalf — that's a tool for creating the documentation, not a shortcut past quality review. The community still votes on the output.
4. **Cross-community value.** A documented planting process from a farm community is discoverable by every gardener on the network. The value transcends the originating community.

**Key insight:** The community's internal activities (planting, building, organizing) become value for the broader network when they're DOCUMENTED. The act of documentation — with the community's help — is the value creation that earns XP.

### Open Design Question

How does AI-assisted content creation interact with the auditing system? If an AI creates a post on behalf of a farmer:
- Who is the author? The farmer? The AI? The community that configured the AI?
- Does the AI's role need to be disclosed? (Probably yes — transparency principle)
- Can the AI accumulate XP? (No — XP is for humans. The human who directed the AI is the author.)

---

## Scenario 3 Feedback: Certification Immutability

### Correction

The brainstorm incorrectly implied that a cert creator might want to "change" an existing certification. **Published certifications are immutable.** Once published, a certification's content hash, parameters, and dimensions are fixed forever. This is by design:

- Adopters chose to adopt a specific, known set of rules
- Changing the cert under them would violate informed consent
- The creator can only publish a **new version** (v2, v3, etc.) linked via `previous_version`
- Each adopter independently chooses whether to re-adopt the new version
- The old version remains valid indefinitely for those who stay on it

The fork scenario (Scenario 3) doesn't require any special mechanism — it's just someone publishing a new certification. Whether it references the original via `previous_version` (if same creator) or starts a new lineage (different creator) is the only distinction.

**Design confirmation:** Anyone can publish certifications. Immutability is guaranteed by the content hash. No special "fork" mechanism needed — the ecosystem naturally allows parallel standards.

---

## Scenario 4: System Sovereignty

No feedback — approach is sound. The chain governs its own governance parameters through the expression system, with certifications as the declaration layer.

---

## References

- [Brainstorm 015: Certification Contract Design](015-certification-contract.md)
- [Brainstorm 012: Certification Anatomy & GER](012-certification-anatomy.md)
- [Brainstorm 011: Constitutional Governance Model](011-constitutional-governance-model.md)
