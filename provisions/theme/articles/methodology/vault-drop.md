---
id: methodology/vault-drop
title: Vault drop
description: Hand a durable artifact to the library by writing a raw capture into
  its raw/ drop zone. The library is the registry field. Export to the nexus when
  the destination is not already the library. Privacy-sensitive chairs take the discreet
  variant instead.
tags:
- methodology
- vault
- inbox
created: '2026-09-08'
updated: '2026-10-02'
---

The library named by `library:` in the nexus registry holds durable knowledge and the graph over it. Any chair may hand it an artifact. This article is that door: what the library is for, and where a capture is written. What the file contains is `methodology/capture-types`.

A privacy-sensitive chair takes `methodology/vault-drop-discreet` instead. Never both in one core.

Unqualified "vault" means that library. Other stores take a qualifier: Insitu vault, Envoy vault. This article is the library door.

Look up the library in `nexus.md`. Start at this chair's nexus and walk to the parent. Use the first `library:` line. The node's Path on that row is the library folder.

## What the vault is for

Work in progress lives in the chair that owns it. The moment something becomes durable, meaning it would be worth having when this project is not the one you are sitting in, it belongs in the vault. Brainstorm the presentation in the node whose work it is, then file the result.

The vault is not an archive and not a backup. It holds what a future sitting in another chair would want to find.

## The door is `raw/`

Write a capture into the library folder's `raw/`. That is the drop zone, and it is not a new one: the library's own ingest skill calls `raw/` the drop zone, its processing log says new captures may land at the root for speed, and the library owner's own capture macro writes there. You are using the path the library already uses, from a different hand.

Land the file at `raw/` root. Do not place it in a dated subfolder yourself. Sorting a capture into `raw/YYYYMM/` happens during processing and is ingest's step, not the sender's.

`raw/` is immutable in the sense that nothing already there may be modified, moved, or deleted. Adding a new capture is not that. Never touch a file you did not just write.

You do not write the library's `inbox/`. That is that chair's own mail and only the nexus writes it. A letter about how that chair operates is not a capture, and the two must not arrive by the same door.

## When to use the door, and when to use the nexus

| You have | Route |
|---|---|
| A durable artifact, and the vault is where it goes | Write a capture to the library `raw/` |
| A finding about another chair | Export to the nexus, per `methodology/node-inbox` |
| Something whose destination you are not sure of | Export to the nexus |

The direct write exists only because the destination is already known. Where it is not known, the nexus hop is doing real triage and this article does not replace it.

## Shape of a capture

One file at `raw/` root, named `YYYYMMDD-slug.md`, matching what the library's own capture path produces.

Stamp and type table are `methodology/capture-types` (Brain Forge public contract). Do not copy that table here.

## Service

A chair on this contract declares `vault-drop` in its `project.yaml` services list, beside `status` and `mail`. The declaration is how the contract is visible without reading the map.

Until a vault MCP exists (program Phase 6), the door is a directory on the same disk and this contract is doctrine rather than an enforced boundary. Same posture as the read half. Do not write code against a server that is not there.

Relation to `methodology/capture-types`: that article is the stamp (types and body). This one is the door. Never both copies of the table.

**Class: composition, dependent.** Names the library (the registry's `library:` field) and Brain Forge (the types). The vault does not enforce that declaration.
