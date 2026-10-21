---
id: methodology/vault-drop-discreet
title: Vault drop (discreet)
description: Vault-drop contract for a privacy-sensitive chair. Warn about the material,
  get the user's confirmation in this chair, then write the capture yourself. The
  library path comes from the registry. No nexus hop. Use instead of methodology/vault-drop,
  never beside it.
tags:
- methodology
- vault
- inbox
- privacy
created: '2026-09-08'
updated: '2026-10-02'
---

The vault-drop contract for a privacy-sensitive chair. Take this instead of `methodology/vault-drop`, never beside it.

What the vault is for, the door (the library `raw/` root, resolved by `methodology/vault-drop`), and the capture shape are the same as for any chair. What changes is that nothing is written until the user has confirmed it here, with the risk in front of them.

## Warn, confirm, write

1. Tell the user what would go, which sender-table type (from `methodology/capture-types`), and why the library is the right home for it. Name the nature of the material: what about it is sensitive, and what the vault would make of it (see below). Do not copy the type table here.
2. Wait for the user's confirmation in this sitting. No confirmation, no drop.
3. On confirmation, write the capture to the library `raw/` yourself. Never touch a file you did not just write.

This chair holds the material and understands its constraints, so the judgment is made here, and the user's confirmation here is the approval. There is no second hop through the nexus.

## What does not go

- Names, quotes, and identifying detail. Summaries and pointers only, and the pointer stays inside this chair's own tree.
- Anything whose value depends on the identifying detail. If summarizing destroys the point, it does not go. Say so and stop, rather than sending a thinner version that still identifies.
- Case, clinical, financial, legal, and minor-related material, in any shape.
- Anything the principal has not seen in this sitting.

## Judge it by what the graph will make of it

The library is a corpus that gets synthesized and graphed, and that is read by whoever sits in the library or queries it from the nexus. Material that is safe as one file is not necessarily safe once it is linked to everything else, and a detail that identifies nobody on its own can identify someone the moment it sits beside a date and a place already in the corpus.

That risk is internal to the library and does not depend on any other chair reading across. No such path exists: domain-wide read was struck, and the library is queried by sitting in it. What sending material here does is make it permanent and connectable, which is enough on its own.

Judge what goes by what the graph can reassemble, not by what the file says alone. When you cannot tell, that is a reason to propose less, or nothing.

## Service

This chair declares `vault-drop` in `project.yaml` like any other. The declaration says this contract is held: the direct write, gated on the user's confirmation here.

Stricter rule wins. Where this chair's own constitution is tighter than this article, that governs, and `methodology/privacy-default` still applies over both.

Relation to `methodology/envoy-mail-discreet`: that article is the letter to the nexus, and the letter has to pass this chair's constitution. This one is the vault door, and it still waits for confirmation here before the capture is written. A letter's destination is the nexus inbox. A capture's destination is the library `raw/`.
