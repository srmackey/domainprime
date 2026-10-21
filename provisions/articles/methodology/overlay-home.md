---
id: methodology/overlay-home
title: Overlay home
description: Chair overlay resolves through a mount. Owner articles name the path.
  The chair composes at most one implementor. Default is the project folder.
tags:
- methodology
- layout
created: '2026-09-17'
updated: '2026-09-17'
---

# Overlay home

Chair overlay resolves through a mount. Owner articles name the path and that it is overlay. They do not name the door, and they do not pick a target.

**Overlay-home names no system.** A chair's overlay behaviour is whatever overlay-home implementor its map composed. A chair that composes none mounts overlay on the project folder.

## What an owner article registers

A surface that is chair overlay names its relative path, and that the path is overlay under `methodology/owner-roots`. That composition is the registration.

This article does not list the paths. A new owner does not come back here to add one.

The chair has one mount. Every overlay path goes there. A writer does not choose a store or a folder for itself.

## How to write and read

Resolve overlay paths through the composed implementor.

- Write and read with that implementor's doors.
- Do not open the git checkout for an overlay path when an implementor is present. Checkout absence is then expected, not a miss, and not a reason to offer init.
- If no implementor is composed, the project folder is the home. Read and write the relative path there.

Implementors may exist side by side in the catalog. A chair composes at most one. Different chairs may compose different implementors. Two implementors on one chair: stop and say so. One mount. No concurrent homes on one chair.

## What an implementor declares

An implementor announces itself with a section headed `Overlay home` that says it is one, names its doors, and says whether overlay paths exist in the git checkout.

It does not name owner paths. It does not restate STATUS grain, inbox triage, or spec shape.

## What this is not

Pack instance roots and host-discovered paths stay on the checkout. `methodology/owner-roots` holds that split.

Git treatment of a path that is in the tree is the repo article. Git treatment of a path the mount says is not in the tree is also the repo article, asking this mount first.

**Class: composition, opportunistic.** Acts on whatever implementor is present and degrades to the project folder when there is none.

Relation to `methodology/settle`: same shape. The operation names no system. Presence in the composed protocol is the registration.

Relation to `methodology/owner-roots`: that article is who owns the folder. This one is where the overlay class is mounted.

Relation to `methodology/use-context-forge`: that article is one implementor.

Reason: a surface that names a store will have to be rewritten when the store changes. A store that names every surface will have to be rewritten when a surface is added. The mount is the one fact both sides were restating.
