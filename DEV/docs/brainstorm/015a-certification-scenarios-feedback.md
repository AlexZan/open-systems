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

### Resolution: XP Gates vs Certification Gates

The initial design conflated two fundamentally different things:

- **XP** = "you've created value in this domain" (posts, contributions, auditing, curation)
- **Training certification** = "you've demonstrated competence" (completed training, passed assessment)

These are different questions. A brilliant engineer with 500 XP in rust has zero business using a laser cutter without training. A newcomer who just completed laser safety training should have access even with 0 XP.

**The maker space gates should be certification requirements, not XP requirements:**

```
- laser_cutter_access: requires adoption of "Laser Operation v2" (not 15 XP)
- cnc_mill_access: requires adoption of "CNC Machining v1"
- 3d_printer_access: requires adoption of "3D Printing Basics v1"
```

Training certifications are published standards. The training process:
1. Trainer publishes "Laser Operation v2" certification (defines competency requirements)
2. Newcomer completes training (in person, at the makerspace)
3. Trainer attests competency — the newcomer adopts "Laser Operation v2" with trainer attestation
4. The makerspace's "Maker Space Safety" cert checks: does this person hold "Laser Operation v2"? If yes → access granted.

This is exactly how real-world certifications work: you take a course, the instructor signs off, you're certified. No value creation required. No chicken-and-egg problem.

### Two Types of Gates

This creates a clean distinction:

| Gate Type | What It Checks | Examples |
|-----------|---------------|----------|
| **XP gate** | Has this person created verified value? | Governance voting, proposal submission, auditor eligibility |
| **Certification gate** | Has this person demonstrated competence? | Equipment access, role eligibility, training prerequisites |

Both are on-chain. Both are verifiable. But they measure different things and should never be confused.

### Attestation Model

Training certification adoption needs an **attestation** — someone vouching that you meet the requirements. This is a new mechanism for the certification contract:

```rust
AdoptCertification {
    cert_id: u64,
    parameter_overrides: Vec<ParameterOverride>,
    attestor: Option<String>,  // address of the person attesting competency
}
```

When `attestor` is Some:
- The cert must be marked as `requires_attestation: true`
- The attestor must themselves hold the cert (or be registered as a trainer)
- The attestor's address is recorded in the adoption record
- The attestor is accountable — if the person they attested for causes a safety incident, the attestor's track record is affected

When `attestor` is None:
- Self-adoption (for governance certifications, org-level standards)
- No competency gate — the adopter declares their own commitment

### What This Means for the Certification Contract

The certification struct needs:
- `requires_attestation: bool` — if true, adoption requires an attestor
- The adoption struct needs: `attestor: Option<Addr>` — who attested competency

This is a small addition to brainstorm 015 that resolves the XP-gate chicken-and-egg problem entirely.

### Open Design Questions (Deferred)

1. **Trainer registration.** Who can attest? Anyone who holds the cert? Or a separate "trainer" role? Probably: anyone who holds the cert at a higher level (or longer tenure) can attest for newcomers.
2. **Attestation revocation.** Can an attestor revoke their attestation? (e.g., "I no longer vouch for this person's competency after seeing them misuse equipment")
3. **Cross-entity certification recognition.** "Laser certified at MakerSpace A → recognized at MakerSpace B." This is the `Requirement` mechanism: MakerSpace B's safety cert can require "Laser Operation v2" — if you hold it from MakerSpace A, the requirement is satisfied regardless of where you got it.
4. **Sub-cluster XP.** The hierarchical cluster question remains for future brainstorming, but it's now clearly SEPARATE from the certification/training question. XP = value creation. Certs = competency. They don't need to mix.

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
