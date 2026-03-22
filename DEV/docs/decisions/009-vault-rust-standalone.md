# Decision 009: Vault as Standalone Rust Daemon

**Date:** 2026-03-22
**Status:** Accepted
**Context:** The vault needs to be shared infrastructure (Open Systems chain, Knowledge Network, os-git, future apps), not coupled to any single project.

---

## Decision

Build the vault as a **standalone Rust daemon** using Automerge (CRDTs) + libp2p + Axum. Start fresh, using the Open-Intelligence prototype (`C:\Dev-backup\Open-Intelligence\vault\`) as reference only.

## Why Standalone

The vault is general-purpose content-addressed storage. Multiple systems depend on it:
- **Open Systems chain** — forum content, certification text, diffs
- **Knowledge Network** — knowledge graphs, sources, reasoning chains
- **os-git** — canonical diffs, PR metadata, revision history
- **Future apps** — any content that needs hash-verified, decentralized storage

Coupling it to `opensystems/` (current Python vault location) prevents other projects from using it independently.

## Why Rust

- **Performance:** Content hashing, P2P networking, CRDT merging are all CPU-bound
- **Reliability:** Long-running daemon needs memory safety without GC
- **Ecosystem:** Automerge and libp2p have mature Rust implementations
- **Consistency:** The chain contracts are already Rust (CosmWasm)
- **AI dev:** Development speed is not a constraint — build it right the first time

## Why Fresh (Not Fork)

The Open-Intelligence vault prototype validates the tech stack (Automerge + libp2p + Axum compiles, runs, syncs). But:
- It's a personal data sync tool (key-value store, notifications, app sandboxing)
- Open Systems needs content-addressed governance storage (SHA-256 keyed, relay semantics)
- Refactoring would mean gutting most of the 562 lines
- Starting fresh with the same dependencies gets the proven stack without wrong abstractions

**Reference patterns from prototype:**
- libp2p swarm setup with GossipSub + mDNS
- Incremental Automerge sync over P2P
- tokio::select! event loop for async multiplexing
- Axum REST API structure

## Architecture

```
vault-daemon (Rust)
├── Content store (SHA-256 keyed, git-style object layout)
├── Automerge documents (for CRDT-capable data like KN graphs)
├── libp2p networking (GossipSub + Kademlia DHT, per Decision 003)
├── HTTP API (Axum — same endpoints as current Python relay)
└── Chain-agnostic (no chain dependencies in core)
```

Python tools (os-git, MCP server, web explorer, scripts) are **clients** that talk to the vault daemon over HTTP. The API surface matches the current Python relay endpoints (`/v1/content`, `/v1/has`, `/v1/catalog`, `/v1/stats`, `/v1/health`, `/v1/peers`, `/v1/sync`).

## What Happens to the Python Vault

The Python vault (`opensystems/vault/`) becomes deprecated once the Rust daemon is operational. The chain verification layer (`vault/chain.py`) moves into the MCP server or web explorer as client-side logic. The Python `RelayClient` continues to work — it talks HTTP to whatever is behind the endpoint.

## Location

`/data/Dev/Open Systems/vault/` — top-level, not inside opensystems/. Own git repo.

---

## References

- Brainstorm 004: Vault Local-First Apps
- Decision 003: Content Discovery via libp2p
- Open-Intelligence prototype: `C:\Dev-backup\Open-Intelligence\vault/` (reference only)
