---
id: methodology/envoy-mail-discreet
title: Envoy mail (discreet)
description: 'Mail contract for a chair in the sensitive operator class: receive like
  any chair. A letter is a write, so it has to pass the same test this chair''s constitution
  applies to saving a file. Carries a settle contract at the source tier. Use instead
  of methodology/envoy-mail, never beside it.'
tags:
- methodology
- envoy
- privacy
created: '2026-09-07'
updated: '2026-09-26'
---

# Envoy mail (discreet)

Mail contract for a chair in the `sensitive` operator class. Receive like any
chair. A letter is a write under this chair's constitution. Use instead of
`methodology/envoy-mail`, never beside it.

Every Envoy call sends `chair` as this chair's map name.

## Receive

Unchanged from any chair, and deliberately so. `inbox/` holds a README,
`_log.md`, `_archive/`, and pending letters. Only the nexus writes it. Process a
letter on command only: the user says `process the inbox`, or points at a file.
Never on session start, never because a file or note arrived.

A delivery into this chair crossed the nexus mail gate on its way, so it already
carried the principal's confirmation before it landed. Nothing about receiving is
narrowed here.

`note_list` acks `shown` when the calling chair is `intended_for` and the note
has no ack yet. Listing as that chair is awareness, which is settled work and
never a proposal. Acking is not sending, and the sender cannot clear their own
note until it happens.

## Send

A letter is a write. It has to pass the same test this chair's constitution
already applies to saving a file. That constitution is the home of the test.
This article does not restate it.

If the letter fails that test, do not send it. Say so the way a refused file
write is said.

If it passes, write the letter into the nexus inbox (`kind: export`) through
that chair's overlay home, path under `inbox/`. A title, the finding written
for the receiver, a pointer home, and why it was sent. Then `note_post` the
bell (`intended_for`, `inbox` path, `why`).

This chair does not write another node's inbox. The only outbound letter is to
the nexus.

Later, `note_list` own notes. On ack, persist anything still unpersisted, then
`note_remove`.

## Settle contract

**Tier: source.** The inbox file is the durable letter, so mail settles before
any digest that reads it.

**Surface:** open notes intended for this chair, and open notes this chair
authored.

**Settled means:** an unacked note intended for this chair is acked `shown`; a
note this chair authored whose letter is filed or archived is removed.

**What satisfies the gate here:** the inbox file. The note is the bell and the
letter is the record, so acking or removing a note can never destroy the only
copy.

**Not settled by this contract:** the letters. Processing an inbox stays on
command. A settle run clears bells, never mail.

Relation to `methodology/vault-drop-discreet`: that article is the vault door.
This one is the letter to the nexus. Both are writes, so both answer to this
chair's constitution.

Reason: The chair's constitution already decides what may be written down. Mail
to the nexus is that write. The channel stays open, and the constitution is the
guard on what the letter may say.
