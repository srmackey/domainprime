#!/usr/bin/env python3
"""Create a Domain Prime top folder, its shelf, and its engines.

The shelf is Insitu's vault root for that tree. Insitu loads one role file from a
pack (roles/<pack id>.yaml) and loads every other role from the vault root.
The three roles are therefore written in both places. Harvest copies articles
and skills only, so a later harvest does not keep the role files inside the
library pack. --update puts them back, in the library pack and at the shelf root.

The same command clones Insitu, Envoy, and Context Forge at the pinned tags
into engines/, harvests each provisions/pack.yaml onto the shelf, and writes
.mcp.json so a session opened at the top folder starts those servers against
that folder. It does not edit a user-level host config.

--with-brain-forge also harvests Brain Forge and copies the theme pack onto
the shelf. The library itself is vault/ at the install root, with a library
row in the registry. The pin is cloned only long enough to seed that folder,
then removed. It is not left in engines/. No map composes the theme pack.
Passing the flag on an existing install adds the library and leaves the rest
of the tree alone.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from datetime import date
from pathlib import Path

SEGMENT = r"^[a-z0-9-]+$"
REQUIRED_ROLES = ("domainprime", "nexus", "node")
REQUIRED_GLOBAL = (
    "methodology/principal-charter",
    "methodology/autonomy-gate-provenance",
    "methodology/context-moves",
)
ROLE_LISTS = ("core", "on_demand", "skills")
PINS = (
    {"name": "insitu", "repo": "https://github.com/srmackey/insitu", "tag": "v0.26.0"},
    {"name": "envoy", "repo": "https://github.com/srmackey/envoy", "tag": "v0.4.1"},
    {
        "name": "context-forge",
        "repo": "https://github.com/srmackey/context-forge",
        "tag": "v0.4.0",
    },
)
BRAIN_FORGE = {
    "name": "brain-forge",
    "repo": "https://github.com/srmackey/brain-forge",
    "tag": "v0.2.9",
}
THEME_ARTICLES = (
    "methodology/vault-drop",
    "methodology/vault-drop-discreet",
    "methodology/envoy-status-discreet",
    "methodology/envoy-mail-discreet",
)
PROVISIONS_PACK = "insitu-core"
PROVISIONS_ARTICLE = "methodology/product-provisions"
Fetch = Callable[[str, str, Path], None]


class InstallError(Exception):
    """The install cannot proceed. The message is the whole report."""


def install_tree(
    product: Path,
    top: Path,
    update: bool = False,
    brain_forge: bool = False,
    fetch: Fetch | None = None,
) -> None:
    """Write or refresh one install. `product` is this repo. `top` is the new tree."""
    product = product.resolve()
    top = top.resolve()
    manifest = load_manifest(product / "provisions" / "pack.yaml")
    validate_manifest(product, manifest)
    if fetch is None:
        fetch = git_fetch
    name = top.name
    if not _segment(name):
        raise InstallError(
            "The last part of the top folder must be a lowercase name "
            "made of letters, digits, and hyphens."
        )
    if top == product or _is_inside(product, top) or _is_inside(top, product):
        raise InstallError("Refusing to install into the product repo.")
    installed = _is_install(top)
    if update:
        if not installed:
            raise InstallError("There is no install here to update.")
        _refresh(product, top, manifest)
        _place_engines(top, fetch)
        if brain_forge or _brain_forge_present(top):
            _place_brain_forge(product, top, fetch)
        return
    if installed:
        if brain_forge:
            _place_brain_forge(product, top, fetch)
            return
        raise InstallError(
            "That folder is already installed. Pass --update to refresh the shelf."
        )
    if top.exists() and any(top.iterdir()):
        raise InstallError("That folder is not empty.")
    top.mkdir(parents=True, exist_ok=True)
    _write_nexus(product, top, name)
    _write_maps(top, name, manifest)
    _refresh(product, top, manifest)
    _place_engines(top, fetch)
    if brain_forge:
        _place_brain_forge(product, top, fetch)


def load_manifest(path: Path) -> dict:
    if not path.is_file():
        raise InstallError("The product has no provisions/pack.yaml.")
    return parse_manifest(path.read_text(encoding="utf-8"))


def parse_manifest(text: str) -> dict:
    """Read the provisions shape this repo ships. Members are id and path."""
    data: dict = {
        "id": "",
        "name": "",
        "kind": "",
        "version": "",
        "articles": [],
        "global": [],
        "roles": [],
        "skills": [],
    }
    section: str | None = None
    current: dict | None = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if indent == 0 and not line.startswith("-") and ":" in line:
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            current = None
            if rest:
                data[key] = rest
                section = None
            else:
                section = key
                data.setdefault(key, [])
            continue
        if section in {"articles", "roles", "skills"} and line.startswith("- "):
            current = {}
            data[section].append(current)
            body = line[2:].strip()
            if ":" in body:
                field, _, value = body.partition(":")
                current[field.strip()] = value.strip()
            continue
        if section in {"articles", "roles", "skills"} and current is not None and ":" in line:
            field, _, value = line.partition(":")
            current[field.strip()] = value.strip()
            continue
        if section == "global" and line.startswith("- "):
            data["global"].append(line[2:].strip())
    return data


def validate_manifest(product: Path, manifest: dict) -> None:
    pack_id = str(manifest.get("id") or "")
    version = str(manifest.get("version") or "")
    if not _segment(pack_id):
        raise InstallError("The pack id is not a single lowercase name.")
    if not _version(version):
        raise InstallError("The pack version is not a dotted number.")
    if manifest.get("kind") != "capability":
        raise InstallError("The pack kind must be capability.")
    if not str(manifest.get("name") or "").strip():
        raise InstallError("The pack needs a name.")
    articles = _members(manifest, "articles", slashes=1)
    roles = _members(manifest, "roles", slashes=0)
    skills = _members(manifest, "skills", slashes=0)
    for group in (articles, roles, skills):
        for item in group:
            _checked_source(product, item["path"])
    article_ids = {item["id"] for item in articles}
    skill_ids = {item["id"] for item in skills}
    role_ids = [item["id"] for item in roles]
    for role_id in REQUIRED_ROLES:
        if role_id not in role_ids:
            raise InstallError(f"The pack is missing a role: {role_id}")
    global_ids = manifest.get("global") or []
    if not isinstance(global_ids, list):
        raise InstallError("The global seed must be a list.")
    for article_id in REQUIRED_GLOBAL:
        if article_id not in global_ids:
            raise InstallError(f"The global seed is missing {article_id}")
    for article_id in global_ids:
        if article_id not in article_ids:
            raise InstallError(f"The global seed names an article the pack does not carry: {article_id}")
    for role in roles:
        lists = _role_lists(product, role["path"])
        for article_id in lists["core"] + lists["on_demand"]:
            if article_id not in article_ids:
                raise InstallError(
                    f"The role {role['id']} names an article the pack does not carry: {article_id}"
                )
        for skill_id in lists["skills"]:
            if skill_id not in skill_ids:
                raise InstallError(
                    f"The role {role['id']} names a skill the pack does not carry: {skill_id}"
                )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    update = False
    brain_forge = False
    if "--update" in args:
        args.remove("--update")
        update = True
    if "--with-brain-forge" in args:
        args.remove("--with-brain-forge")
        brain_forge = True
    if len(args) != 1 or args[0].startswith("-"):
        print(
            "usage: python install.py <top-folder> [--update] [--with-brain-forge]",
            file=sys.stderr,
        )
        return 2
    product = Path(__file__).resolve().parent
    try:
        install_tree(product, Path(args[0]), update=update, brain_forge=brain_forge)
    except InstallError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


def _refresh(product: Path, top: Path, manifest: dict) -> None:
    shelf = top / "shelf"
    _copy_members(product, shelf, manifest)
    pack_root = shelf / "library" / manifest["id"]
    if pack_root.is_dir():
        shutil.rmtree(pack_root)
    version_root = pack_root / manifest["version"]
    _copy_members(product, version_root, manifest)
    (version_root / "pack.yaml").write_text(_shelf_pack(manifest), encoding="utf-8")
    (version_root / "VERSION").write_text(manifest["version"] + "\n", encoding="utf-8")
    _update_lock(shelf, manifest)


def _copy_members(product: Path, dest: Path, manifest: dict) -> None:
    for article in manifest["articles"]:
        src = _checked_source(product, article["path"])
        if not src.is_file():
            raise InstallError(f"The pack member is missing: {article['path']}")
        target = dest / "articles" / Path(*article["id"].split("/")).with_suffix(".md")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    for role in manifest["roles"]:
        src = _checked_source(product, role["path"])
        if not src.is_file():
            raise InstallError(f"The pack member is missing: {role['path']}")
        target = dest / "roles" / f"{role['id']}.yaml"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    for skill in manifest["skills"]:
        src = _checked_source(product, skill["path"])
        skill_dir = src.parent if src.is_file() else src
        if not (skill_dir / "SKILL.md").is_file():
            raise InstallError(f"The pack member is missing: {skill['path']}")
        target = dest / "skills" / skill["id"]
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(skill_dir, target)


def _write_nexus(product: Path, top: Path, name: str) -> None:
    template_path = product / "template" / "nexus.md"
    if not template_path.is_file():
        raise InstallError("The product has no template/nexus.md.")
    lines = template_path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# nexus:"):
        raise InstallError("template/nexus.md has no nexus heading.")
    lines[0] = f"# nexus: {name}"
    text = "\n".join(lines)
    if not text.endswith("\n"):
        text += "\n"
    (top / "nexus.md").write_text(text, encoding="utf-8")


def _write_maps(top: Path, name: str, manifest: dict) -> None:
    global_map = top / "shelf" / "projects" / "_global" / "map.yaml"
    top_map = top / "shelf" / "projects" / name / "map.yaml"
    global_map.parent.mkdir(parents=True, exist_ok=True)
    top_map.parent.mkdir(parents=True, exist_ok=True)
    seeds = "\n".join(f"  - {item}" for item in manifest["global"])
    global_map.write_text(
        "name: Global\ninclude_global: false\ncore:\n" + seeds + "\nroles: []\n",
        encoding="utf-8",
    )
    top_map.write_text(
        f"name: {name}\ninclude_global: true\nroles:\n  - domainprime\n",
        encoding="utf-8",
    )


def _update_lock(shelf: Path, manifest: dict, source: str = "copy") -> None:
    path = shelf / "library" / "lock.yaml"
    lock = parse_lock(path.read_text(encoding="utf-8")) if path.is_file() else {}
    lock[manifest["id"]] = {manifest["version"]: {"source": source}}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_lock(lock), encoding="utf-8")


def _shelf_pack(manifest: dict) -> str:
    lines = [
        f"id: {manifest['id']}",
        f"name: {manifest['name']}",
        f"kind: {manifest['kind']}",
        f"version: {manifest['version']}",
        "articles:",
    ]
    lines.extend(f"  - {item['id']}" for item in manifest["articles"])
    lines.append("roles:")
    lines.extend(f"  - {item['id']}" for item in manifest["roles"])
    lines.append("skills:")
    lines.extend(f"  - {item['id']}" for item in manifest["skills"])
    if manifest["global"]:
        lines.append("global:")
        lines.extend(f"  - {item}" for item in manifest["global"])
    lines.append("")
    return "\n".join(lines)


def parse_lock(text: str) -> dict:
    lock: dict = {}
    pack = None
    version = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if indent == 0 and line.endswith(":"):
            pack = line[:-1].strip()
            lock[pack] = {}
            version = None
            continue
        if indent == 2 and line.endswith(":") and pack is not None:
            version = line[:-1].strip()
            lock[pack][version] = {}
            continue
        if indent >= 4 and pack is not None and version is not None and ":" in line:
            key, _, value = line.partition(":")
            lock[pack][version][key.strip()] = value.strip()
    return lock


def git_fetch(repo: str, tag: str, dest: Path) -> None:
    """Clone one pinned tag. A failed clone leaves no directory behind."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", tag, repo, str(dest)],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        raise InstallError("git is not available, so the engines cannot be cloned.") from None
    except subprocess.CalledProcessError as exc:
        if dest.exists():
            shutil.rmtree(dest, ignore_errors=True)
        detail = (exc.stderr or exc.stdout or "").strip()
        raise InstallError(f"Could not clone {repo} at {tag}. {detail}") from None


def _place_engines(top: Path, fetch: Fetch) -> None:
    engines = top / "engines"
    engines.mkdir(parents=True, exist_ok=True)
    for pin in PINS:
        dest = engines / pin["name"]
        if not dest.exists():
            fetch(pin["repo"], pin["tag"], dest)
        manifest = _engine_manifest(dest)
        if pin["name"] == "insitu" and manifest["id"] != PROVISIONS_PACK:
            raise InstallError("The Insitu pin is not the insitu-core pack.")
        _harvest_checkout(dest, top / "shelf", manifest)
    insitu = _engine_manifest(engines / "insitu")
    _ensure_provisions_import(top, insitu["version"])
    _write_servers(top)


def _brain_forge_present(top: Path) -> bool:
    return (top / "vault" / "_brain-forge").is_dir()


def _place_brain_forge(product: Path, top: Path, fetch: Fetch) -> None:
    """Harvest Brain Forge, seed vault/ at the install root, and drop the clone."""
    theme_path = product / "provisions" / "theme" / "pack.yaml"
    if not theme_path.is_file():
        raise InstallError("The product has no provisions/theme/pack.yaml.")
    theme = parse_manifest(theme_path.read_text(encoding="utf-8"))
    _validate_theme(product, theme)
    scratch = Path(tempfile.mkdtemp(prefix="domainprime-brain-forge-"))
    try:
        dest = scratch / BRAIN_FORGE["name"]
        fetch(BRAIN_FORGE["repo"], BRAIN_FORGE["tag"], dest)
        manifest = _engine_manifest(dest)
        if manifest["id"] != BRAIN_FORGE["name"]:
            raise InstallError("The Brain Forge pin is not the brain-forge pack.")
        _harvest_checkout(dest, top / "shelf", manifest)
        _place_theme(product, top / "shelf", theme)
        _install_vault(dest, top / "vault")
        _ensure_library(top)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def _validate_theme(product: Path, manifest: dict) -> None:
    if manifest.get("kind") != "theme":
        raise InstallError("The theme pack kind must be theme.")
    pack_id = str(manifest.get("id") or "")
    version = str(manifest.get("version") or "")
    capability = load_manifest(product / "provisions" / "pack.yaml")
    if not _segment(pack_id):
        raise InstallError("The theme pack id is not a single lowercase name.")
    if pack_id == str(capability.get("id") or ""):
        raise InstallError("The theme pack cannot use the capability pack id.")
    if not _version(version):
        raise InstallError("The theme pack version is not a dotted number.")
    if not str(manifest.get("name") or "").strip():
        raise InstallError("The theme pack needs a name.")
    if manifest.get("roles"):
        raise InstallError("The theme pack composes no roles.")
    if manifest.get("global"):
        raise InstallError("The theme pack is not a global seed.")
    articles = _members(manifest, "articles", slashes=1)
    if [item["id"] for item in articles] != list(THEME_ARTICLES):
        raise InstallError("The theme pack is not the vault door and the discreet mail pair.")
    manifest["articles"] = articles
    manifest["skills"] = []
    for item in articles:
        src = _checked_source(product, item["path"])
        if not src.is_file():
            raise InstallError(f"The pack member is missing: {item['path']}")


OWNER_FRAMEWORK = (
    "eval.md",
    "system-log.md",
    "skills/forge-synthesis-engine/preferences.md",
    "skills/forge-synthesis-engine/tweaks-log.md",
)
SEEDED_PRIMERS = ("distill.md", "_system.md", "_me.md")
LIBRARY_ROW = "| vault | vault/ | node | active | no | no |  |  |"


def _install_vault(checkout: Path, vault: Path) -> None:
    """Copy the framework into vault/ and create the layout Brain Forge expects."""
    source = checkout / "_brain-forge"
    if not source.is_dir():
        raise InstallError("The Brain Forge pin has no _brain-forge folder.")
    vault.mkdir(parents=True, exist_ok=True)
    if (vault / "_brain-forge").is_dir():
        _refresh_framework(source, vault)
    else:
        shutil.copytree(source, vault / "_brain-forge")
        _write_if_absent(vault / "_brain-forge" / "eval.md", "# Eval\n")
        _write_if_absent(vault / "_brain-forge" / "system-log.md", "# System log\n")
    _seed_layout(vault)


def _refresh_framework(source: Path, vault: Path) -> None:
    """Replace the shipped framework and put the owner's own files back."""
    framework = vault / "_brain-forge"
    kept: list[tuple[Path, bytes]] = []
    for rel in OWNER_FRAMEWORK:
        path = framework / rel
        if path.is_file():
            kept.append((path.relative_to(framework), path.read_bytes()))
    shutil.rmtree(framework)
    shutil.copytree(source, framework)
    for rel, payload in kept:
        dest = framework / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(payload)


def _seed_layout(vault: Path) -> None:
    """First-install files only. Anything already there belongs to the owner."""
    today = date.today().isoformat()
    for name in ("raw", "wiki", "primers"):
        (vault / name).mkdir(parents=True, exist_ok=True)
    _write_if_absent(vault / "raw" / "_log.md", "# Raw log\n")
    _write_if_absent(
        vault / "wiki" / "_index.md",
        "---\n"
        "type: reference\n"
        "signal: true\n"
        "status: active\n"
        f"created: {today}\n"
        "---\n\n"
        "# Wiki index\n\n"
        "## Pages\n\n"
        "## Recent activity\n",
    )
    ignore = vault / "_brain-forge" / ".graphifyignore"
    if ignore.is_file():
        _copy_if_absent(ignore, vault / ".graphifyignore")
    for name in SEEDED_PRIMERS:
        src = vault / "_brain-forge" / "primers" / name
        if src.is_file():
            _copy_if_absent(src, vault / "primers" / name)
    _write_if_absent(vault / "primers" / "_index.md", _primer_index(vault, today))
    _write_if_absent(
        vault / "AGENTS.md",
        "# AGENTS.md — vault\n\n"
        "This folder is the library for this install. Kind: node.\n\n"
        "How the vault operates is `_brain-forge/constitution.md`.\n\n"
        "Insitu is not subscribed here. The first working session asks what to subscribe.\n",
    )


def _primer_index(vault: Path, today: str) -> str:
    folder = vault / "_brain-forge" / "primers"
    names = []
    if folder.is_dir():
        for path in sorted(folder.glob("*.md")):
            if _signal(path):
                names.append(path.name)
    lines = [
        "---",
        "type: reference",
        "signal: true",
        "status: active",
        f"created: {today}",
        "---",
        "",
        "# Primers",
        "",
    ]
    lines.extend(f"- `primers/{name}`" for name in names)
    lines.append("")
    return "\n".join(lines)


def _signal(path: Path) -> bool:
    """True when the frontmatter says signal: true. Body text does not count."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end == -1:
        return False
    return any(line.strip() == "signal: true" for line in text[3:end].splitlines())


def _write_if_absent(path: Path, text: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _copy_if_absent(src: Path, dest: Path) -> None:
    if dest.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def _ensure_library(top: Path) -> None:
    path = top / "nexus.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    named = [line.strip() for line in lines if line.startswith("library:")]
    if any(line != "library: vault" for line in named):
        raise InstallError("The registry already names a library.")
    if "library: vault" not in named:
        out: list[str] = []
        inserted = False
        for line in lines:
            out.append(line)
            if not inserted and line.startswith("admin:"):
                out.append("library: vault")
                inserted = True
        if not inserted:
            raise InstallError("The registry has no admin line.")
        lines = out
    if not any(line.startswith("| vault |") for line in lines):
        sep = next((i for i, line in enumerate(lines) if line.startswith("|---")), None)
        if sep is None:
            raise InstallError("The registry has no node table.")
        at = sep + 1
        while at < len(lines) and lines[at].startswith("|"):
            at += 1
        lines.insert(at, LIBRARY_ROW)
    text = "\n".join(lines)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def _place_theme(product: Path, shelf: Path, manifest: dict) -> None:
    version_root = shelf / "library" / manifest["id"] / manifest["version"]
    if version_root.exists():
        shutil.rmtree(version_root)
    version_root.mkdir(parents=True)
    _copy_contract(product, version_root, manifest)
    (version_root / "pack.yaml").write_text(_theme_pack(manifest), encoding="utf-8")
    (version_root / "VERSION").write_text(manifest["version"] + "\n", encoding="utf-8")
    _update_lock(shelf, manifest, source="copy")


def _engine_manifest(checkout: Path) -> dict:
    path = checkout / "provisions" / "pack.yaml"
    if not path.is_file():
        raise InstallError(f"engines/{checkout.name} has no provisions/pack.yaml.")
    manifest = parse_manifest(path.read_text(encoding="utf-8"))
    pack_id = str(manifest.get("id") or "")
    version = str(manifest.get("version") or "")
    if not _segment(pack_id):
        raise InstallError(f"engines/{checkout.name} has no pack id.")
    if not _version(version):
        raise InstallError(f"engines/{checkout.name} has no pack version.")
    if not str(manifest.get("name") or "").strip():
        manifest["name"] = pack_id
    if not str(manifest.get("kind") or "").strip():
        raise InstallError(f"engines/{checkout.name} has no pack kind.")
    articles = manifest.get("articles") or []
    skills = manifest.get("skills") or []
    if not articles:
        raise InstallError(f"engines/{checkout.name} lists no articles.")
    manifest["articles"] = _members({"articles": articles}, "articles", slashes=1)
    manifest["skills"] = (
        _members({"skills": skills}, "skills", slashes=0) if skills else []
    )
    for group in (manifest["articles"], manifest["skills"]):
        for item in group:
            _checked_source(checkout, item["path"], "the checkout")
    return manifest


def _harvest_checkout(checkout: Path, shelf: Path, manifest: dict) -> None:
    version_root = shelf / "library" / manifest["id"] / manifest["version"]
    if version_root.exists():
        shutil.rmtree(version_root)
    version_root.mkdir(parents=True)
    _copy_contract(checkout, version_root, manifest)
    (version_root / "pack.yaml").write_text(_theme_pack(manifest), encoding="utf-8")
    (version_root / "VERSION").write_text(manifest["version"] + "\n", encoding="utf-8")
    _update_lock(shelf, manifest, source="harvest")


def _copy_contract(root: Path, dest: Path, manifest: dict) -> None:
    for article in manifest["articles"]:
        src = _checked_source(root, article["path"], "the checkout")
        if not src.is_file():
            raise InstallError(f"The pack member is missing: {article['path']}")
        target = dest / "articles" / Path(*article["id"].split("/")).with_suffix(".md")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    for skill in manifest["skills"]:
        src = _checked_source(root, skill["path"], "the checkout")
        skill_dir = src.parent if src.is_file() else src
        if not (skill_dir / "SKILL.md").is_file():
            raise InstallError(f"The pack member is missing: {skill['path']}")
        target = dest / "skills" / skill["id"]
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(skill_dir, target)


def _theme_pack(manifest: dict) -> str:
    lines = [
        f"id: {manifest['id']}",
        f"name: {manifest['name']}",
        f"kind: {manifest['kind']}",
        f"version: {manifest['version']}",
        "articles:",
    ]
    lines.extend(f"  - {item['id']}" for item in manifest["articles"])
    lines.append("skills:")
    lines.extend(f"  - {item['id']}" for item in manifest["skills"])
    lines.append("")
    return "\n".join(lines)


def _ensure_provisions_import(top: Path, version: str) -> None:
    path = top / "shelf" / "projects" / "_global" / "map.yaml"
    text = path.read_text(encoding="utf-8")
    if PROVISIONS_ARTICLE in text and f"pack: {PROVISIONS_PACK}" in text:
        return
    if "imports:" in text:
        raise InstallError(
            "The global map already has imports, and it does not include "
            "methodology/product-provisions."
        )
    if not text.endswith("\n"):
        text += "\n"
    text += (
        "imports:\n"
        f"- pack: {PROVISIONS_PACK}\n"
        f"  version: {version}\n"
        "  articles:\n"
        f"  - {PROVISIONS_ARTICLE}\n"
    )
    path.write_text(text, encoding="utf-8")


def _write_servers(top: Path) -> None:
    root = top.resolve()
    shelf = root / "shelf"
    engines = root / "engines"

    def posix(path: Path) -> str:
        return path.resolve().as_posix()

    payload = {
        "mcpServers": {
            "insitu": {
                "command": "uv",
                "args": ["run", "--directory", posix(engines / "insitu"), "insitu"],
                "env": {
                    "INSITU_ROOT": posix(root),
                    "INSITU_HOME": posix(shelf),
                },
            },
            "envoy": {
                "command": "uv",
                "args": ["run", "--directory", posix(engines / "envoy"), "envoy"],
                "env": {"ENVOY_ROOT": posix(root)},
            },
            "contextforge": {
                "command": "uv",
                "args": [
                    "run",
                    "--directory",
                    posix(engines / "context-forge"),
                    "contextforge",
                ],
                "env": {"CONTEXTFORGE_ROOT": posix(root)},
            },
        }
    }
    (root / ".mcp.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def dump_lock(lock: dict) -> str:
    lines: list[str] = []
    for pack_id, versions in lock.items():
        lines.append(f"{pack_id}:")
        if not isinstance(versions, dict):
            continue
        for version, row in versions.items():
            lines.append(f"  {version}:")
            if isinstance(row, dict):
                for key, value in row.items():
                    lines.append(f"    {key}: {value}")
    lines.append("")
    return "\n".join(lines)


def _members(manifest: dict, key: str, slashes: int) -> list[dict]:
    items = manifest.get(key) or []
    if not isinstance(items, list) or not items:
        raise InstallError(f"The pack needs a {key} list.")
    seen: set[str] = set()
    out: list[dict] = []
    for item in items:
        if not isinstance(item, dict) or "id" not in item or "path" not in item:
            raise InstallError(f"Each {key} member needs an id and a path.")
        member_id = str(item["id"])
        if not _identity(member_id, slashes):
            raise InstallError(f"The pack has a {key} id that is not allowed: {member_id}")
        if member_id in seen:
            raise InstallError(f"The pack repeats a {key} id: {member_id}")
        seen.add(member_id)
        out.append({"id": member_id, "path": str(item["path"])})
    return out


def _role_lists(product: Path, rel: str) -> dict[str, list[str]]:
    src = _checked_source(product, rel)
    if not src.is_file():
        raise InstallError(f"The pack member is missing: {rel}")
    found = {name: [] for name in ROLE_LISTS}
    section: str | None = None
    for raw in src.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if indent == 0 and not line.startswith("-") and ":" in line:
            key, _, rest = line.partition(":")
            key = key.strip()
            section = key if key in ROLE_LISTS and not rest.strip() else None
            continue
        if section and line.startswith("- "):
            found[section].append(line[2:].strip())
    return found


def _checked_source(root: Path, rel: str, label: str = "the product") -> Path:
    if not rel or rel.startswith(("/", "\\")) or ".." in Path(rel).parts:
        raise InstallError(f"Member path leaves {label}: {rel}")
    src = (root / rel).resolve()
    try:
        src.relative_to(root.resolve())
    except ValueError:
        raise InstallError(f"Member path leaves {label}: {rel}") from None
    return src


def _is_install(top: Path) -> bool:
    return (top / "nexus.md").is_file() and (
        top / "shelf" / "projects" / "_global" / "map.yaml"
    ).is_file()


def _is_inside(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return child != parent


def _segment(value: str) -> bool:
    import re

    return bool(re.fullmatch(SEGMENT, value))


def _version(value: str) -> bool:
    import re

    return bool(re.fullmatch(r"\d+(\.\d+)*", value))


def _identity(value: str, slashes: int) -> bool:
    parts = value.split("/")
    return len(parts) == slashes + 1 and all(_segment(part) for part in parts)


if __name__ == "__main__":
    raise SystemExit(main())
