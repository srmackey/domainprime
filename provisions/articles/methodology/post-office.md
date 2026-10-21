---
id: methodology/post-office
title: Post office
description: Inbox and mail doctrine for the orchestrating chair. Brief letters addressed
  here, send what names its own destination, propose where the rest goes, and stop
  at a sensitive chair's boundary. Deliver to nodes; never apply inside one. Carries
  a settle contract at the source tier.
tags:
- methodology
- inbox
created: '2026-09-18'
updated: '2026-10-05'
---

# Post office

You are the nexus: awareness and post office, not a container of work. You do not apply changes inside a node.

The library is the node named by `library:` in `nexus.md`. Start at this nexus and walk to the parent. Use the first line that sets it. `<library>` below is that node's Path. `<nexus>` is this nexus's inbox.

## Session start

After the nexus constitution is loaded, session start is `methodology/nexus-board`. Do not walk every node to rewrite STATUS. Do not settle a node from this chair.

## Write permissions

```
node         -->  <nexus>/inbox/         export (propose-only on their side)
node         -->  <library>/raw/         vault-drop, direct, destination known
library      -->  <nexus>/inbox/         delivery-request (when no live nexus caller)
nexus        -->  <library>/raw/         catalog hand, written as a capture
nexus        -->  <library>/inbox/       deliver (the library's own mail, like any node)
nexus        -->  <node>/inbox/          deliver
nexus        -->  nexus internals        doctrine, routing, nexus STATUS
```

Row two is the only path a chair writes into a sibling, and it is not an exception to the inbox rule: `raw/` is the library's drop zone, not an inbox. `methodology/vault-drop` governs the sending half and applies only where the destination is already the library. A privacy-sensitive chair holds `methodology/vault-drop-discreet` instead and writes its own capture once the user confirms in that chair. It does not pass through here.

Rows four and five are the same destination project and different doors on purpose. A capture is corpus material. A letter about how that chair operates is mail. Sending a letter to `raw/` would put this chair's own administrivia into the library's permanent record.

Inbox rows in that table (`<nexus>/inbox/`, `<node>/inbox/`) are overlay. Write them through the receiving chair's overlay home. `<library>/raw/` stays on the library checkout. It is not overlay.

You never process a node inbox. You never ingest the library from this chair. Invoke it only when asked (`catalog what's waiting`).

## Mail gate

When Envoy is available, list open mail notes (`note_list`, chair `nexus`) and open the letter.

**The gate fires on traffic that crosses a privacy-sensitive chair's boundary, in either direction:** a delivery going into one, and material coming out of one bound anywhere else. There, choose deliver, hold, or foul. The user decides holds and fouls. Then ack (`delivered`, `held`, or `ignored`). Which chairs are sensitive is the nexus registry, not this article.

Everywhere else the letter waiting in the receiving inbox is the durable copy, so the provenance test passes: deliver, report it, and ack under `methodology/envoy-mail` like any other note. Do not hold an ordinary delivery for a decision that has nothing to decide.

Envoy does not write node inboxes; this chair does.

Do not process inbox because a note arrived. Process on command still applies.

## Process the nexus inbox

Trigger: the user says `process the inbox` or points at a file. Never on session start. Never because a file or note arrived.

Processing is two jobs. Telling the user what a letter holds is a **briefing**. Sending it on, archiving it, logging it, and keeping the count true is **filing**. The user needs the first and should never have to watch the second.

A briefing says **what the letter says**, in plain statements that stand without the sender's context; **why it came here**; and **what to do**, as a recommendation, or "nothing, filed."

List pending files (skip `_log.md`, `README.md`, `_archive/`), then sort each letter:

| Letter | You do |
|---|---|
| Addressed to the nexus itself | Brief it, one at a time. The user's answer is the disposition. A letter that asks for nothing is filed without asking. |
| Names its destination, no sensitive chair involved | Send it. Report it in one line. |
| No clear destination | Brief it with a proposed destination. Wait. |
| Into or out of a sensitive chair | Stop. Brief it and wait for the user. |

When proposing a destination:

| Item looks like | Destination |
|---|---|
| Knowledge worth remembering | `catalog` handoff: a capture to the library `raw/` |
| Operational for one node | `deliver` to that node's `inbox/` |
| About the library's own operation | `deliver` to the library `inbox/`, never to `raw/` |
| Nexus doctrine, routing, cross-cutting todo | nexus internals |

Once a letter is dispositioned, write the handoff or nexus-internal change, move the inbox file to `_archive/`, and append `_log.md`. The archive copy, its log row, and the delivered letter are the second copy, so filing passes `methodology/autonomy-gate-provenance`. A hold leaves the file, or marks `status: hold` if it has frontmatter. List everything filed without asking in one line at the end of the run.

Catalog-worthy items are not ingested by writing them. A capture sits in `raw/` until the library is invoked, which is what makes the drop safe.

A write across the fence is a handoff: finding written for the receiver, pointer home, why it was sent. Not a dump of the source.

## Handoff kinds

- `catalog`: a capture written into the library's `raw/`. Shape and frontmatter are `methodology/vault-drop`.
- `deliver`: nexus to a node, the library included, into that chair's `inbox/`. Finding for that project to handle under its own constitution. You do not name file paths inside the node.
- `delivery-request`: the library to the nexus. Expand to one `deliver` per name in `nodes:`.
- `export`: node to nexus. Extra-project signal waiting here.

Material about a sensitive chair travels as summaries plus pointers. Material leaving one is the outbound direction of the mail gate, so a fan into a second node waits for the user. Stricter privacy rule wins.

## Catalog door

When the user says `catalog what's waiting`, step into the library (load its constitution; drop the nexus apply-lens) and run its own ingest path over unprocessed captures. It returns a node list. You write one `deliver` per node if not already delivered.

## Settle contract

**Tier: source.** The inbox is a durable store that this chair's digest reads.

**Surface:** pending files in nexus `inbox/`, and the disposition of what this chair already cleared.

**Settled means:** the pending count is current; a file whose handoff was written and archived is out of the pending set and has its `_log.md` row; and nothing already delivered still shows as pending anywhere.

**What satisfies the gate here:** the `_archive/` copy with its `_log.md` row, and at the far end the delivered letter itself.

**Not settled by this contract: processing.** Briefing a letter, sending one that names its destination, and filing one that asks for nothing all happen on command. A settle run reconciles what was already dispositioned and counts what is waiting. A growing pending count is a number to report, not a reason to start.

## Git

The nexus `inbox/` is this doctrine's owner root under `methodology/owner-roots`. It is chair overlay. Git treatment is the repo article this chair composed.

Same folder, same rule, one level up: `methodology/node-inbox` says this for a node's own inbox.
