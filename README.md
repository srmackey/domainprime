# Domain Prime

Domain Prime is the installable tree: a seed, an empty registry, and the engines a release pins.

A person clones this repo and runs its install. They get one top folder and one shelf. The top folder is one nexus with an empty roster.

## Install

Run this from a clone of the repo:

```
python install.py <top-folder>
```

The last part of `<top-folder>` is the nexus name. Use lowercase letters, digits, and hyphens, as in `garden`. The command writes `nexus.md` in that folder and creates `shelf/` beside it. The shelf is the vault for that tree. It holds the capability pack and the roles `domainprime`, `nexus`, and `node`. The top nexus wears `domainprime` only.

Refresh the shelf from a newer copy of this repo:

```
python install.py <top-folder> --update
```

The refresh replaces the generated pack, roles, articles, and skills. It leaves `nexus.md` and the project maps as they are. Engines and the Brain Forge choice come later.

## License

MIT. The terms are in `LICENSE`.

## Pins

| Engine | Repository | Version | When |
|---|---|---|---|
| Insitu | https://github.com/srmackey/insitu | v0.25.1 | every install |
| Envoy | https://github.com/srmackey/envoy | v0.4.1 | every install |
| Context Forge | https://github.com/srmackey/context-forge | v0.4.0 | every install |
| Brain Forge | https://github.com/srmackey/brain-forge | v0.2.9 | only when the install includes it |

A newer tag is a change to this table, written here.

## Seed

`provisions/pack.yaml` is the capability pack. The roles, articles, and skills live beside that file under `provisions/`. It carries the roles `domainprime`, `nexus`, and `node`. `weekly-pack` is on `domainprime` and `nexus`. `methodology/tree-setup` is on demand on those two roles.

The `_global` seed is `methodology/principal-charter`, `methodology/autonomy-gate-provenance`, and `methodology/context-moves`.

## Template

`template/nexus.md` is the empty registry. No nodes, no `library:`, no `focus:`, no sensitivity marks.
