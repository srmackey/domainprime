---
id: methodology/nexus-board
title: Nexus board
description: 'FOCUS.md at this nexus root. The principal ranks. A focus: child leads
  the pack. Session-start pack is on request. Outside todos, weekly review. Not a
  node reckoning.'
tags:
- methodology
- nexus
- board
created: '2026-08-18'
updated: '2026-10-20'
---

# Nexus board

The nexus keeps one board: `FOCUS.md` at this nexus's root. The principal ranks. The agent does not invent priority. This is awareness, not a container of node work.

`focus:` in this nexus's `nexus.md` names one direct child. When it is set, that child's board leads the pack, and that chair is left out of the chair lines. The lines stay in the child's file. This session may edit that one file and nothing else in that chair.

The board stays at the root. Owner roots governs chair overlay, and the board is not that: it is the one surface the principal reads directly.

## Board file

```markdown
# FOCUS
updated: YYYY-MM-DD

## This week
The principal's rank. 3-5 items. First item is the default next move.

1. **<one line>** · due: YYYY-MM-DD or none · node: <name> or none

## Later
Everything else still wanted visible: dated or not, node-backed or outside.
One line each.

- **<one line>** · due: YYYY-MM-DD or none · node: <name> or none
```

## Rules

- One line of substance. If it needs a paragraph, it needs a node (or it stays a one-liner until it does).
- `node: none` means outside: no project yet. Not nexus-OS work. That stays in the nexus STATUS.
- When `node:` is set, the pointer is that node's published sitrep via Envoy (or that node's local STATUS if Envoy is down) unless the principal names a tighter path. Do not paste the node's list onto the board.
- Sensitive nodes: one-line only. No names, quotes, or facts. Which nodes those are is local registry, not this article.
- Outside personal/family items: one-line only at nexus root. Same grain.
- The principal adds, reorders, and drops **This week**. The agent may propose a change and wait.
- **Always-on nodes** are the rows marked always-on in this nexus's `nexus.md`. This week always has at least one line from each. Do not drop the last line from any of them unless the principal says so. The agent does not invent the lines.
- Empty **This week** is valid. The pack says so and lists dated **Later** items plus node Forefronts. It does not invent a week. If an always-on node is missing from This week, say so in the pack (and in weekly review, propose that node's Forefront as a one-liner and wait).
- If the board and a node Forefront disagree, follow Envoy reconcile: do not flag when the trail accounts for the ranked line. Flag `unaccounted`. Do not silently pick a winner.
- When the registry changes (new sibling, disposition, inbox added), `map_upsert` in that same sitting.

## Session start (the pack)

The pack is given when he asks. It does not gate the session. It is not a settle of every node.

On the first turn, if he did not ask, do not read the board and do not print the week, the Forefronts, or the inbox count. One sentence offering to check status is the whole readout. When `desk/` exists at this nexus's root and the count is not zero, that sentence leads with the count. A waiting mail note is still one line, and an empty list is silence. Naming a task is not an ask.

Asking is a request for status, the board, or the Forefronts with no chair named, or one of `where am I at across everything`, `what's on the board`, `meta pack`. A named chair stays on `methodology/status-contract`.

When he asks, compose the pack:

1. Read the board via Envoy `now_view` (chair is this nexus) when Envoy is available. Otherwise read this nexus's `FOCUS.md`, and the child's `FOCUS.md` when `focus:` is set. Chair lines fall back to each direct chair's `_status/STATUS.md` through that chair's overlay home.
2. Use `now_view` reconcile: do not flag when the trail accounts for a ranked line. Flag `unaccounted`. Do not paste Next steps or Open loops. Print `repo:` under a Forefront when present.
3. List open mail notes (`note_list`). That is the bell. Do not process inbox because a note arrived.
4. Inbox count still comes from the nexus `inbox/` files through the overlay home (skip `_log.md`, `README.md`, `_archive/`).
5. Compose, in this order:
   a. Overdue, or due within 7 days, from the borrowed board when `focus` is present, then from this nexus's board. Also mention a Forefront that itself contains an ISO date in that window and is not on either board. Mark those "on STATUS, not on the board."
   b. When the result includes `focus`, that board first, in its order. Item 1 is the default next move. The file is that chair's `FOCUS.md`.
   c. This nexus's week. When `focus` is absent, item 1 is the default next move. Flag `always_on_missing`. If a ranked item's node has a `repo:` line, print it indented under the item.
   d. Forefronts on the result, one line each. They are this nexus's direct chairs. The chair named by `focus:` is not among them. Chairs under a child nexus are not in this pack. If that sitrep has `repo:`, print it as the next indented line.
   e. Inbox count. Waiting mail notes are the bell, not a reason to process.
   f. Desk count, when `desk/` exists at this nexus's root. Count the files. Skip `README.md` and `_archive/`. One line, the number. Omit the line when the count is zero. The filenames wait until he asks what is on the desk.
6. Ask nothing mandatory. Do not step into a node. Do not start item 1 unless the principal says to. Do not settle any node from this chair.

If a published sitrep `updated` date is older than 7 days, or its Forefront contains an ISO date that is already past, the pack may add one word: `stale`. That is a flag, not a trigger to open the node.

## Weekly review

Trigger: `weekly review` or `update the board`.

Show this nexus's `FOCUS.md`. When `focus:` is set, show that chair's board first. Print each direct-chair Forefront (one line) and any `stale` flags. Print a node's `repo:` line when present. Propose date callouts. If an always-on row has no This week line, propose that node's Forefront as a one-liner. Wait. The principal sets the 3-5. Write the file. Do not open nodes or settle them unless the principal names them.

If the pack is composed and the board is empty or stale, say so and fall back to Forefronts plus any dates it can see.

## Outside todos, then a project

Life items with no node live on `FOCUS.md` (`node: none`) until done, dropped, or promoted. Do not grow domain notes at nexus root. When a cluster is clearly a domain, propose a node under the nexus it belongs to and wait.
