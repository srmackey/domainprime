---
id: methodology/status-contract
title: Status contract
description: 'Every active project keeps a STATUS file in its `_status/` owner root:
  forefront, where we left off, next steps, open loops. Every line is closable by
  this chair. Nexus-usable one-line Forefront. Carries a settle contract at the digest
  tier.'
tags:
- methodology
- status
created: '2026-08-17'
updated: '2026-10-20'
---

# Status contract

Every active project carries a STATUS file at `_status/STATUS.md`: the uniform "where am I / what's next" surface. `_status/` is this doctrine's owner root under `methodology/owner-roots`, it holds nothing else, and it is chair overlay.

```markdown
# STATUS — <project>
updated: YYYY-MM-DD

## Forefront
The single thing to pick up next.

## Where I left off
2–4 lines of state, absolute dates.

## Next steps
Short ordered list.

## Open loops
Waiting-on items, pending decisions.
```

- **STATUS is state, AGENTS.md is doctrine.** Status never accretes in a constitution. Constitutions change rarely and deliberately.
- **Every line is closable by this chair.** Forefront, next steps, and open loops hold work this chair can do and can finish. A step another chair has to take is not a next step here, and a finding about another chair is not an open loop here. It leaves as an export under `methodology/envoy-mail` and comes off these books. A spec this chair holds is the board for that work (`methodology/plan-lifecycle`). Forefront may point at it. Do not recopy its slices here. Side work handed here from another chair's spec arrives as mail and is then this chair's. Sequencing on a spec this chair does not hold is not a line here. A duplicate ledger only ever diverges from its home, and the chair holding the copy is the one that cannot close the line.
- **Nexus-usable Forefront.** One line. The real next move. When a date exists, write it as ISO (`2026-08-08`). Do not turn STATUS into the focus board (`FOCUS.md` is that board).
- **Desk count.** When `desk/` exists at this chair's root, session start leads with the count of files there. Skip `README.md` and `_archive/`. One number. Omit it at zero. The filenames wait until he asks what is on the desk. The count does not replace Forefront, and it is not a reason to print the rest of STATUS.
- **Refresh:** making this file true is a settle run. `methodology/settle` holds the operation and says when it fires.
- **Exit ritual (mandatory):** before leaving a project after meaningful work, settle. Forefront first. The agent finishing the work is the one who knows what's next.
- **Status routing:** "what's next with X" / "where am I at in Y" → read that chair's `_status/STATUS.md` through the overlay home, or its published sitrep. No constitution load needed for a pure status question. "I want to work on Z" → read that file for the Forefront item, then run the entry ritual and start there. "Where am I at across everything" → on the nexus, compose the pack per `methodology/nexus-board` if that article is loaded; otherwise sweep published sitreps, not checkout paths.
- **STATUS summarizes, it doesn't own.** Projects with richer internal state keep that state. STATUS is the digest and points inward.
- A project without a STATUS file gets one created on first meaningful touch.
- **Absolute dates only.** Write `2026-08-08`, never "today".
- **Git.** `_status/` is chair overlay. Git treatment is the repo article this chair composed. Hosts do not auto-load this file.
- **One file, one place.** If a root-level `STATUS.md` appears in a project that already has `_status/STATUS.md`, it was written by a session running an older protocol. Do not merge them blind and do not assume the newer timestamp wins. Say so, and let that chair reconcile its own record.

## Settle contract

**Tier: digest.** STATUS summarises sources, so it settles after them and before anything published from it.

**Surface:** the four sections read together, plus whatever Forefront points at. Reading them one at a time is what lets the same item sit in two of them unnoticed.

**Settled means:** Forefront names the real next move for this chair; nothing in the four sections is landed, stale, or orphaned; no item appears in two of them; and no line belongs to another chair.

**What satisfies the gate here:** a landed paper, a commit, tag, or release, an archived inbox letter and its `_log.md` row, the file the line points at.

**Duplicate precedence.** This surface ranks its own sections, so it declares the ranking rather than leaving it to the orchestrator: a paper beats Forefront, Forefront beats next steps, next steps beat open loops. An item lives in exactly one of them.

**Not this chair's** is the closable rule above, enforced rather than merely stated. A line only another chair can close leaves as an export and comes off these books in the same run.

## Why it is not at the root

It used to be, and the reason was real: the nexus pack read each node's Forefront without stepping in, so the file had to sit somewhere the nexus could find without knowing anything about the node.

The bulletin replaced that. Nexus awareness reads published sitreps through Envoy plus the nexus inbox count, so nothing outside a project needs to locate that project's status file by guessing its path. Once that was true, STATUS became ordinary chair overlay, and chair overlay takes an owner root like anything else that maintains files in a project.

## Moving another chair's file

**The default: each chair moves its own.** A path that needs correcting is that chair's own work, on its next meaningful touch, as part of the exit ritual that was going to write the file anyway. A stale path is not a reason to step into a node.

**The exception: a chartered sweep.** The principal may charter the admin chair to change named projects directly. That charter is his to give and is never assumed. A sweep under it moves files, gitignore entries, and path strings only. It writes no content, runs no settle, and does not touch a project whose constitution asks for an extra check unless the charter names that project.

A dated record inside a constitution is not a path string. A line quoting a decision, with the date it was made, keeps the path it named at the time. Repoint the live pointer beside it instead.

A sweep is not a step-in and does not become one. If a node turns out to need judgment rather than a path change, it comes off the sweep and goes back to its own chair.

A chair with a live session in it is the one case where a sweep can destroy work rather than relocate it, because that session is running the protocol as it was when it loaded and will write to the old path. Name it and let the principal decide, rather than treating a recent write as a reason to skip quietly.

The move itself ran 2026-08-30 across all ten active chairs.
