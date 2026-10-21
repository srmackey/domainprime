# Domain Prime

Domain Prime is the installable tree: a seed, an empty registry, and the engines a release pins.

A person clones this repo and runs its install. They get one top folder and one shelf. The top folder is one nexus with an empty roster. The installer is the next piece of this repo.

## Pins

| Engine | Repository | Version | When |
|---|---|---|---|
| Insitu | https://github.com/srmackey/insitu | v0.25.1 | every install |
| Envoy | https://github.com/srmackey/envoy | v0.4.1 | every install |
| Context Forge | https://github.com/srmackey/context-forge | v0.4.0 | every install |
| Brain Forge | https://github.com/srmackey/brain-forge | v0.2.9 | only when the install includes it |

A newer tag is a change to this table, written here.

## Seed

`provisions/pack.yaml` is the capability pack. It carries the roles `domainprime`, `nexus`, and `node`. `weekly-pack` is on `domainprime` and `nexus`. `methodology/tree-setup` is on demand on those two roles.

The `_global` seed is `methodology/principal-charter`, `methodology/autonomy-gate-provenance`, and `methodology/context-moves`.

## Template

`template/nexus.md` is the empty registry. No nodes, no `library:`, no `focus:`, no sensitivity marks.
