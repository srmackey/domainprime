---
id: methodology/node-inbox
title: Node inbox
description: 'Receive this project''s inbox: brief each letter and take the user''s
  answer as its disposition, file what needs nothing without asking, never write another
  project''s inbox. Owner root inbox/. Carries a settle contract at the source tier.'
tags:
- methodology
- inbox
created: '2026-08-18'
updated: '2026-09-26'
---

# Node inbox

You are standing in one project. This constitution applies. You receive `inbox/`
here. You do not run the nexus or Brain Vault from this chair.

## Inbox machine

`inbox/` holds a README, `_log.md`, `_archive/`, and pending letters. Only the
nexus writes it (`kind: deliver`). `inbox/` is overlay. Write and read it through
the overlay home.

Report the pending count when this chair is sat down in, skipping `_log.md`,
`README.md`, and `_archive/`. The count is the report. The files stay the work
until the user asks for them.

## Process this inbox

Trigger: the user says `process the inbox` or points at a file. Never on session
start. Never because a file or note arrived.

Processing is two jobs. Telling the user what a letter holds is a **briefing**.
Archiving it, logging it, acking it, and keeping the count true is **filing**. The
user needs the first and should never have to watch the second.

1. List pending files.
2. Brief each letter that needs an answer, **one at a time**:
   - **What it says,** in plain statements that stand without the sender's
     context.
   - **Why it came to this chair.**
   - **What to do,** as a recommendation in this project's terms.

   Then wait. The user's answer is the disposition. Do not offer a menu of
   destinations.
3. On the answer, do the write under this constitution, move the file to
   `inbox/_archive/`, and append `inbox/_log.md`. A hold leaves the file, or marks
   `status: hold` if it has frontmatter.
4. **A letter that asks for nothing** is filed without asking. List those in one
   line at the end of the run. The archive copy and its `_log.md` row are the
   second copy, so this passes `methodology/autonomy-gate-provenance`.
5. **A misdelivered letter:** the briefing says so, and the letter goes back to
   the nexus as an export under `methodology/envoy-mail`, then is archived here
   with its row. No menu. A chair that composes `methodology/envoy-mail-discreet`
   sends that export under that article, which applies this chair's constitution
   to the letter. If the letter fails that test, it stays pending and the refusal
   is said the way a refused file write is said.

A destination named inside a letter is a request. The sender does not choose the
path inside this project.

You never process another project's inbox. You never write another node's
`inbox/`. You never run nexus triage.

## Settle contract

**Tier: source.** The inbox is a durable store that this chair's digest reads.

**Surface:** pending files in this chair's `inbox/`, and the disposition of what
this chair already cleared.

**Settled means:** the pending count is current; a file that was processed is out
of the pending set and has its `_log.md` row; and nothing already dispositioned
still shows as pending.

**What satisfies the gate here:** the `_archive/` copy with its `_log.md` row,
and the write the letter asked for, in this project's own files.

**Not settled by this contract: the briefing.** Reading a letter to the user, and
filing a letter that asks for nothing, both happen on command. A settle run
reconciles what was already dispositioned and counts what is waiting. A growing
pending count is a number to report, not a reason to start.

## Git

`inbox/` is this doctrine's owner root under `methodology/owner-roots`. It is
chair overlay. Git treatment is the repo article this chair composed.

The name predates the underscore convention and keeps it. Do not read the missing
underscore as an exemption, and do not rename the tree as tidying: that is a
migration, and it needs its own decision.

Relation to `methodology/envoy-mail`: that article owns the bell, the ack, and
sending an export out of this chair. This one owns the folder and what happens to
a letter once it is in it. A chair on `methodology/envoy-mail-discreet` sends
under that article instead, and still composes this one for the folder.
