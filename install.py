#!/usr/bin/env python3
"""Create a Domain Prime top folder and its shelf.

The shelf is the vault root for that tree. Insitu loads one role file from a
pack (roles/<pack id>.yaml) and loads every other role from the vault root.
The three roles are therefore written in both places. Harvest copies articles
and skills only, so a later harvest does not keep the role files inside the
library pack. --update puts them back, in the library pack and at the shelf root.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

SEGMENT = r"^[a-z0-9-]+$"
REQUIRED_ROLES = ("domainprime", "nexus", "node")
REQUIRED_GLOBAL = (
    "methodology/principal-charter",
    "methodology/autonomy-gate-provenance",
    "methodology/context-moves",
)
ROLE_LISTS = ("core", "on_demand", "skills")


class InstallError(Exception):
    """The install cannot proceed. The message is the whole report."""


def install_tree(product: Path, top: Path, update: bool = False) -> None:
    """Write or refresh one install. `product` is this repo. `top` is the new tree."""
    product = product.resolve()
    top = top.resolve()
    manifest = load_manifest(product / "provisions" / "pack.yaml")
    validate_manifest(product, manifest)
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
        return
    if installed:
        raise InstallError(
            "That folder is already installed. Pass --update to refresh the shelf."
        )
    if top.exists() and any(top.iterdir()):
        raise InstallError("That folder is not empty.")
    top.mkdir(parents=True, exist_ok=True)
    _write_nexus(product, top, name)
    _write_maps(top, name, manifest)
    _refresh(product, top, manifest)


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
    if "--update" in args:
        args.remove("--update")
        update = True
    if len(args) != 1 or args[0].startswith("-"):
        print("usage: python install.py <top-folder> [--update]", file=sys.stderr)
        return 2
    product = Path(__file__).resolve().parent
    try:
        install_tree(product, Path(args[0]), update=update)
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


def _update_lock(shelf: Path, manifest: dict) -> None:
    path = shelf / "library" / "lock.yaml"
    lock = parse_lock(path.read_text(encoding="utf-8")) if path.is_file() else {}
    lock[manifest["id"]] = {manifest["version"]: {"source": "copy"}}
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


def _checked_source(product: Path, rel: str) -> Path:
    if not rel or rel.startswith(("/", "\\")) or ".." in Path(rel).parts:
        raise InstallError(f"Member path leaves the product: {rel}")
    src = (product / rel).resolve()
    try:
        src.relative_to(product.resolve())
    except ValueError:
        raise InstallError(f"Member path leaves the product: {rel}") from None
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
