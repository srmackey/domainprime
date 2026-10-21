---
id: methodology/envoy-status-discreet
title: Envoy status (discreet)
description: 'Envoy status subscriber for a chair in the guarded class: publish a
  thin sitrep, never a copy of local STATUS. Carries a settle contract at the publication
  tier that never widens what is published. Use when project.yaml lists status and
  this chair is guarded.'
tags:
- methodology
- envoy
created: '2026-08-25'
updated: '2026-09-14'
---

# Envoy status (discreet)

This chair opted into Envoy `status` in `project.yaml`, and this contract is the `guarded` publish rule. Local STATUS may be richer than what Envoy may hold.

Every Envoy call sends `chair` as this chair's map name.

## Local vs published

The local digest at `_status/STATUS.md` (`methodology/status-contract`) is this node's record. It may contain detail that belongs only here.

The vault sitrep is not a copy of that file. Nexus reads the vault. Anything you `status_put` can be read from a nexus chair.

## Publish

After a real change, and on exit from a sitting that changed it: write the local file, then `status_put` a **thin** sitrep:

- Forefront: one line of substance. No names, quotes, or identifying keywords. No facts that do not belong on the nexus.
- `repo:` only if it is already on the local file. Do not invent.
- Where I left off: only what nexus needs to reconcile a ranked board line, at the same grain as Forefront. Prefer one line. Empty is allowed if nothing on the board needs a trail.
- Next steps: empty list.
- Open loops: empty list.

Do not summarize the local Next steps or Open loops into the vault. Omit them.

Do not enqueue status events. Do not expect an ack. Do not read sibling STATUS files as an API.

A chair takes this contract because it holds the `guarded` class.

## Settle contract

**Tier: publication.** The sitrep is derived from the local digest, so it settles last, after that digest is true.

**Surface:** the published sitrep.

**Settled means:** the published Forefront still answers to the local one at the grain above, `repo:` matches the local file or is absent, and Next steps and Open loops are still empty. A run that corrected the local digest republishes rather than waiting for the next real change.

**What satisfies the gate here:** `_status/STATUS.md`. The published sitrep is a thinned derivative of it, so republishing can never destroy the only copy.

**The thinning is never settled work.** What may leave this chair is the Publish rule above, and a settle run applies it exactly as a hand write would. Settle never widens what is published. A local line with no publishable form is not published, and that is a settled outcome rather than something to raise.
