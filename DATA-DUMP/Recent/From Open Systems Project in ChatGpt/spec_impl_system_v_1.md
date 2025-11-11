# Spec→Implementation System (v1)

## 1. Specification File Format
Each feature or module should have its own specification file written in Markdown.

**Location:** `specs/<domain>/<feature>.spec.md`

**Front-matter (YAML):**
- `id`: unique spec ID
- `status`: draft | in-review | locked | stable
- `version`: semver (major/minor/patch)
- `stability`: low | medium | high
- `locked_sections`: list of AC IDs or section names
- `contracts`: references to contracts (smart or logical)
- `goals`: IDs linking to Open Project Goals

**Body structure:**
- User Story
- Acceptance Criteria (ACs with stable IDs, e.g., `AC-CHAT-001`)
- Non-Goals
- Notes

Each AC must have a unique ID. These IDs are used as anchors for code and test traceability.

**Traceability in code/tests:** Use `@trace(AC-...)` comments in implementation and test files.

---

## 2. Traceability Index
Generated automatically by CI as `specs/_trace.json` mapping each AC ID to its implementation and test references.

**Purpose:** Enables audit, coverage tracking, and inclusion in proof bundles.

---

## 3. Agent Generation Pipeline
Agents take a spec and generate the corresponding implementation and tests.

**Inputs:** Spec MD file + project context.

**Outputs:**
- Implementation stubs or diffs
- Test skeletons per AC
- Regeneration plan with change summary and lock respect

**Lock behavior:** Agents cannot alter locked ACs or code tied to them. They must adapt new code around existing locked behavior.

**Artifacts:** Generated in a feature branch and opened as a draft PR with AC checklist summary.

---

## 4. Refinement Loop
1. **Generate:** Agents create implementation and tests from the current spec.
2. **Review:** Product owner (PO) reviews, locks desired behaviors, updates spec.
3. **Regenerate:** Agents reprocess non-locked areas to improve or adjust.
4. **Promote:** When all ACs are satisfied, a Proof Bundle is generated and submitted for voting/release.

---

## 5. Tests Derived from Spec
Each Acceptance Criterion must have at least one test. Tests directly mirror AC IDs.

**Naming convention:** `test_AC-CHAT-001_handles_retry_logic`.

CI produces an AC pass/fail matrix for visibility in PRs and proof submissions.

---

## 6. Proof Bundle Structure
Upon submission, CI or Oracles compile a bundle for verification and voting.

**Contents:**
- Spec snapshot (with hash)
- Trace index (`_trace.json`)
- AC checklist (with test results)
- Build artifact hashes
- Signed tag of commit

Used for transparent validation and automated fund release via smart contracts.

---

## 7. Regeneration Semantics
**Source of Truth:** The Markdown spec.

Changing an AC or example increments spec version and triggers regeneration.

**Locked ACs:**
- Behavior must remain unchanged.
- If modification is required, PO explicitly unlocks it.

Agents must describe what changed and why in the PR body, listing AC diffs.

---

## 8. CI/CD Integration
- **Monorepo:** All apps share schemas and contracts.
- **Tests:** Run per changed package.
- **Checks:** PRs blocked until all ACs pass.
- **Badges:** Link to Open Projects page for real-time transparency.

---

## 9. Governance and Funding
- Each spec references a Project Goal ID.
- When all ACs are green, Proof Bundle is submitted for community voting.
- On success, escrow is released automatically.
- Failed or abandoned goals can enter bounty state for community pickup.

---

## 10. Open Systems Alignment
This process integrates tightly with Open Systems’ philosophy:
- **Transparency:** Every step (spec, code, proof) is visible and auditable.
- **Collaboration:** Anyone can propose changes or improvements.
- **Accountability:** Locked behaviors and AC-based tests make proof immutable.
- **Democracy:** Votes release funds and validate community progress.

---

## Example Structure
```
/specs/chat/retry-backoff.spec.md   # Contains AC-CHAT-001..008
/specs/_trace.json                  # Auto-generated mapping
/apps/web/...                       # Implementation
/apps/api/...                       # Tests (prefixed by AC IDs)
/.github/workflows/proof.yml        # Generates proof bundle
```

PR checklists mirror the spec AC list and mark completion when tests pass.

