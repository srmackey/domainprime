# Domain Prime

Domain Prime is the installable tree: a seed, an empty registry, and the engines a release pins.

A person clones this repo and runs its install. They get one top folder and one shelf. The top folder is one nexus with an empty roster.

## Install

Run this from a clone of the repo:

```
python install.py <top-folder>
```

The last part of `<top-folder>` is the nexus name. Use lowercase letters, digits, and hyphens, as in `garden`. The command writes `nexus.md` in that folder and creates `shelf/` beside it. The shelf is the vault for that tree. It holds the capability pack and the roles `domainprime`, `nexus`, and `node`. The top nexus wears `domainprime` only.

The same command clones the three engines in the pin table into `engines/` at those tags and harvests each `provisions/pack.yaml` onto the shelf. It writes `.mcp.json` at the top folder. A session opened there starts Insitu, Envoy, and Context Forge against that folder and that shelf. The file does not edit a user-level host config, and the install does not write `platforms.yaml`.

After Insitu is harvested, the new tree's `_global` map imports `methodology/product-provisions` from `insitu-core`. The article stays in the Insitu repository.

Brain Forge stays out unless the install asks for it:

```
python install.py <top-folder> --with-brain-forge
```

That clones Brain Forge at its pin into `engines/` and harvests its public contract onto the shelf. It also copies the theme pack `domainprime-theme` there: the vault door and the discreet mail pair. No map composes that pack, and `nexus.md` still has no `library:` line. `.mcp.json` does not gain a server.

The same flag on a folder that is already installed adds Brain Forge and the theme pack and leaves the registry, the maps, and the other engines as they are.

Refresh the shelf from a newer copy of this repo:

```
python install.py <top-folder> --update
```

The refresh replaces the generated pack, roles, articles, and skills, and harvests the engines again. It leaves `nexus.md` and the project maps as they are, apart from adding the `methodology/product-provisions` import when that import is missing. If Brain Forge is already in the tree, the refresh harvests it again and recopies the theme pack. To add it during a refresh, pass `--with-brain-forge` as well. If a clone fails, run the same command again with `--update`, and with `--with-brain-forge` when that choice was part of the install.

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
