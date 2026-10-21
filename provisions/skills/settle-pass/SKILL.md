---
name: settle-pass
description: 'Use when asked to settle a nexus, settle all, or settle everything,
  or when a settle-wait report is waiting at session start. One argument: a nexus
  name or all. Conventions live in methodology/settle-pass.'
---

# Settle pass

Thin front. The rules are `methodology/settle-pass`. Each chair follows `methodology/settle`. Do not restate either.

## Run

1. **Argument.** A nexus name, or `all`. If it is missing, ask once.
2. **Scope.** `map_list` for this chair. Active rows only. `all` is this chair plus every active descendant. A nexus name is that nexus plus its active descendants. Refuse a name this chair does not contain. Skip superseded and parked.
3. **Order.** The nexus, then its nodes. Step into a child nexus before its nodes.
4. **Each chair.** Announce the step-in, load that constitution, and run settle. Keep only what the gate could not prove and could not house. Do not ask. Do not start the work. Do not edit the board.
5. **Sensitive chairs.** Record the address and the count. Leave the lines on that chair.
6. **Write** `settle-wait.md` on this chair with `write_working`, replacing the whole file. If nothing is left, delete the overlay file. The next search reindexes the gap. Do not leave a stub.
7. **Then stop.** Settled lines per chair, then the waiting items.

## File

```markdown
---
title: Settle wait
target: <nexus or all>
date: YYYY-MM-DD
---

# Settle wait

## <chair>
- surface: <section>
- line: <the line>
- why: <only copy, or no home>

## <sensitive chair>
- waiting: <count>
```

## When the file is already there

Search this workspace for `settle-wait`. Drop an item whose line is gone from that chair's status. Drop a sensitive count the principal has called resolved. Rewrite the file, or delete it when empty. If items remain, present them and wait.
