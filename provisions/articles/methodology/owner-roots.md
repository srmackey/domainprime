---
id: methodology/owner-roots
title: Owner roots
description: Anything that maintains files inside a project owns one folder at that
  project's root, named for itself, and writes only there. The class says who owns
  it; git treatment is the repo article this chair composed.
tags:
- methodology
- layout
created: '2026-08-30'
updated: '2026-09-17'
---

# Owner roots

Anything that maintains files inside a project owns **one folder at that project's root, named for itself**, and that folder is the only place it writes.

A pack, a Domain-wide tool, or a piece of doctrine that puts working files in a project takes `_name/`. Apart from that folder it writes only two things: the host-required paths a host discovers by name (`.claude/`, `.cursor/`, `.grok/`, `AGENTS.md`), and product files it names explicitly and the project would have anyway (`README.md`, `DESIGN.md`, and the like).

`_name/` is a variable. This article does not list the folders in use, and a new owner does not come back here to register one. That is what keeps this a convention rather than a table every pack has to edit.

## The class says who owns it

Two kinds, and the difference is ownership, not layout:

- **Pack instance root.** A pack maintains the folder inside each project that installs it. The pack's own doctrine says what goes there.
- **Chair overlay.** The folder holds this chair's working state, and a native article owns it rather than any pack. Overlay paths resolve through `methodology/overlay-home`.

Host-discovered paths stay on the checkout. Relative paths do not move.

## Git treatment is the repo article

The owner names the folder and that it is overlay. Git treatment is the repo article this chair composed, which asks `methodology/overlay-home` whether those paths are in the tree.

**An underscore implies nothing about git.** A pack instance root can be versioned or ignored. So can a chair overlay. Reading the leading underscore as "ignored" is how a folder ends up in the wrong state without anyone deciding.

Owner articles name the overlay paths. They do not declare whether those paths are gitignored.

## Folders that predate this

A folder that already has a name without the underscore keeps it until someone deliberately moves it. Renaming an owner root is a migration with its own cost, and it is never a side effect of tidying. The convention describes what a new owner should do and what an old one should become, not a defect list.
