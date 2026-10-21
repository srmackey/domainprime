---
id: methodology/insitu-vault-steward
title: Insitu vault steward
description: The Insitu vault is a git repo no node owns. The admin chair carries
  its line and settles what a sitting dirtied.
tags:
- insitu
- git
- admin
created: '2026-09-08'
updated: '2026-09-08'
---

The Insitu vault is a git repo that no node owns. Every chair writes it through mutating tools, and no node's repo doctrine reaches it: the Insitu vault is a store, not a node, so it has no map, no STATUS, and no sit-down.

It is versioned to keep its own history, not to develop in. There is no remote, no branch flow, and no review, so nothing here is pushed and nothing waits on a PR. It carries no `repo:` line at sit-down, and a dirty tree is not leftover work blocking anything. `methodology/repo-provenance` is that posture stated in general; this article states it here so a steward who does not compose that article can still act. What this article adds is who carries the Insitu vault, and one tightening: a sitting that mutates it settles before leaving, rather than waiting for a logical group of work to be done.

Without a steward, whatever a sitting dirties there sticks to whichever chair happened to be sitting, which is a chair that is not watching the Insitu vault and cannot close the line.

The admin chair stewards it. Which chair that is comes from the Insitu vault's operator config, not from this article.

**How to follow**

1. **Carry the Insitu vault's line.** When this chair writes its own STATUS, read live `git status --porcelain` in the Insitu vault and record one line under `updated:`:

   `insitu vault: <branch> · clean|dirty`

   Dirty means a tracked file modified, staged, deleted, or unmerged, or an untracked path under `articles/`, `projects/`, `provenance/`, `config/`, or `library/`. Live git wins over the line. This is the Insitu vault's state and never a substitute for this checkout's own `repo:` line.

2. **Settle what this sitting dirtied.** A sitting that authored, linked, installed, or materialized has changes waiting in the Insitu vault. Commit them here, in this sitting, with a subject saying what is now true of that vault and why it mattered. Do not list files. Do not leave a mutating sitting behind an uncommitted Insitu vault.

3. **Do not settle what you did not do.** An edit from another session belongs to that session, and a stale working tree may be work in progress. Name it and wait. Never `git add -A` in the Insitu vault: it stages another chair's unfinished writes and anything a tool left half-written.

4. **Node chairs report, they do not hold.** A chair that dirties the Insitu vault as a side effect of its own work says so and exports it under `methodology/envoy-mail`. It does not carry the Insitu vault's git state, or an Insitu authoring decision, in its own STATUS. Those lines are not closable there.

Reason: the Insitu vault holds every chair's standing guidance, so its history is the one record that no node can reconstruct. It was also the one repo the system never named an owner for.
