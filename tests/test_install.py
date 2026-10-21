"""Installer checks. Run from the product root: py -3 -m unittest discover -s tests"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import install

FIXTURES = ROOT / "tests" / "fixtures" / "engines"


def fixture_fetch(repo: str, tag: str, dest: Path) -> None:
    name = repo.rstrip("/").rsplit("/", 1)[-1]
    if name.endswith(".git"):
        name = name[: -len(".git")]
    src = FIXTURES / name
    if not src.is_dir():
        raise install.InstallError(f"No fixture for {name}")
    shutil.copytree(src, dest)


def _ids(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    found: list[str] = []
    taking = False
    for line in lines:
        if line.startswith(heading + ":"):
            taking = True
            continue
        if taking and line.startswith("  - "):
            found.append(line[4:].strip())
            continue
        if taking and line and not line.startswith(" "):
            break
    return found


class InstallTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _install(self, top, update=False, brain_forge=False, fetch=None):
        install.install_tree(
            ROOT,
            top,
            update=update,
            brain_forge=brain_forge,
            fetch=fetch or fixture_fetch,
        )

    def test_install_writes_the_registry_and_the_three_roles(self):
        top = self.tmp / "garden"
        self._install(top)
        registry = (top / "nexus.md").read_text(encoding="utf-8")
        self.assertTrue(registry.startswith("# nexus: garden\n"))
        self.assertIn("admin: the principal", registry)
        self.assertNotIn("library:", registry)
        self.assertNotIn("focus:", registry)
        shelf = top / "shelf"
        for role in ("domainprime", "nexus", "node"):
            self.assertTrue((shelf / "roles" / f"{role}.yaml").is_file(), role)
            self.assertTrue(
                (shelf / "library" / "domainprime" / "0.1.0" / "roles" / f"{role}.yaml").is_file(),
                role,
            )
        self.assertTrue((shelf / "skills" / "weekly-pack" / "SKILL.md").is_file())
        pack = (
            shelf / "library" / "domainprime" / "0.1.0" / "pack.yaml"
        ).read_text(encoding="utf-8")
        self.assertEqual(_ids(pack, "roles"), ["domainprime", "nexus", "node"])
        global_map = (shelf / "projects" / "_global" / "map.yaml").read_text(encoding="utf-8")
        self.assertIn("include_global: false", global_map)
        for seed in (
            "methodology/principal-charter",
            "methodology/autonomy-gate-provenance",
            "methodology/context-moves",
        ):
            self.assertIn(seed, global_map)
        top_map = (shelf / "projects" / "garden" / "map.yaml").read_text(encoding="utf-8")
        self.assertEqual(_ids(top_map, "roles"), ["domainprime"])
        self.assertIn("include_global: true", top_map)
        self.assertNotIn("nexus", _ids(top_map, "roles"))
        lock = (shelf / "library" / "lock.yaml").read_text(encoding="utf-8")
        self.assertIn("source: copy", lock)
        version = (shelf / "library" / "domainprime" / "0.1.0" / "VERSION").read_text(
            encoding="utf-8"
        )
        self.assertEqual(version, "0.1.0\n")

    def test_update_keeps_a_sentinel_and_refreshes_roles(self):
        top = self.tmp / "garden"
        self._install(top)
        registry = top / "nexus.md"
        registry.write_text(registry.read_text(encoding="utf-8") + "SENTINEL\n", encoding="utf-8")
        role = top / "shelf" / "roles" / "node.yaml"
        original = role.read_text(encoding="utf-8")
        role.write_text("changed: true\n", encoding="utf-8")
        project = top / "shelf" / "projects" / "garden" / "map.yaml"
        project.write_text(project.read_text(encoding="utf-8") + "notes: keep\n", encoding="utf-8")
        extra = top / "shelf" / "library" / "example" / "0.1.0" / "pack.yaml"
        extra.parent.mkdir(parents=True)
        extra.write_text("id: example\n", encoding="utf-8")
        kept = top / "shelf" / "articles" / "notes.md"
        kept.write_text("leave this\n", encoding="utf-8")
        lock_path = top / "shelf" / "library" / "lock.yaml"
        lock_path.write_text(
            "example:\n  0.1.0:\n    source: harvest\n" + lock_path.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        self._install(top, update=True)
        self.assertIn("SENTINEL", registry.read_text(encoding="utf-8"))
        self.assertEqual(role.read_text(encoding="utf-8"), original)
        self.assertIn("notes: keep", project.read_text(encoding="utf-8"))
        self.assertTrue(extra.is_file())
        self.assertEqual(kept.read_text(encoding="utf-8"), "leave this\n")
        lock = install.parse_lock(lock_path.read_text(encoding="utf-8"))
        self.assertEqual(lock["example"]["0.1.0"]["source"], "harvest")
        self.assertEqual(lock["domainprime"]["0.1.0"]["source"], "copy")

    def test_bad_name_refuses(self):
        with self.assertRaises(install.InstallError):
            install.install_tree(ROOT, self.tmp / "Garden")
        self.assertFalse((self.tmp / "Garden").exists())

    def test_second_run_refuses(self):
        top = self.tmp / "garden"
        self._install(top)
        with self.assertRaises(install.InstallError):
            self._install(top)

    def test_nonempty_refuses(self):
        top = self.tmp / "garden"
        top.mkdir()
        (top / "notes.txt").write_text("keep\n", encoding="utf-8")
        with self.assertRaises(install.InstallError):
            install.install_tree(ROOT, top)
        self.assertFalse((top / "nexus.md").exists())

    def test_update_without_an_install_refuses(self):
        top = self.tmp / "garden"
        top.mkdir()
        with self.assertRaises(install.InstallError):
            install.install_tree(ROOT, top, update=True)

    def test_refuses_the_product_repo(self):
        with self.assertRaises(install.InstallError):
            install.install_tree(ROOT, ROOT)
        with self.assertRaises(install.InstallError):
            install.install_tree(ROOT, ROOT / "build")

    def test_member_path_cannot_leave_the_product(self):
        product = self.tmp / "product"
        (product / "provisions").mkdir(parents=True)
        (product / "provisions" / "pack.yaml").write_text(
            "id: sample\nname: Sample\nkind: capability\nversion: 0.1.0\n"
            "articles:\n  - id: identity/sample\n    path: ../outside.md\n"
            "global:\n  - identity/sample\n"
            "roles:\n  - id: sample\n    path: roles/sample.yaml\n"
            "skills:\n  - id: settle\n    path: skills/settle/SKILL.md\n",
            encoding="utf-8",
        )
        with self.assertRaises(install.InstallError) as caught:
            install.install_tree(product, self.tmp / "garden")
        self.assertIn("leaves the product", str(caught.exception))

    def test_created_shelf_has_no_personal_name(self):
        top = self.tmp / "garden"
        self._install(top)
        needle = "Sco" + "tt"
        other = "Mac" + "key"
        own = {str(top.resolve()), top.resolve().as_posix()}
        hits = []
        for path in top.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for item in own:
                text = text.replace(item, "")
            if needle in text or other in text:
                hits.append(str(path.relative_to(top)))
        self.assertEqual(hits, [])

    def test_engines_are_harvested_and_pointed_at_the_tree(self):
        top = self.tmp / "garden"
        self._install(top)
        shelf = top / "shelf"
        self.assertTrue(
            (
                shelf
                / "library"
                / "insitu-core"
                / "0.7.0"
                / "articles"
                / "methodology"
                / "insitu-orientation.md"
            ).is_file()
        )
        self.assertTrue(
            (
                shelf
                / "library"
                / "insitu-core"
                / "0.7.0"
                / "skills"
                / "protocol-audit"
                / "SKILL.md"
            ).is_file()
        )
        self.assertFalse((shelf / "library" / "insitu-core" / "0.7.0" / "roles").exists())
        self.assertTrue(
            (
                shelf
                / "library"
                / "envoy"
                / "0.2.3"
                / "articles"
                / "methodology"
                / "envoy-mail.md"
            ).is_file()
        )
        self.assertTrue(
            (
                shelf
                / "library"
                / "context-forge"
                / "0.4.1"
                / "articles"
                / "methodology"
                / "use-context-forge.md"
            ).is_file()
        )
        self.assertFalse(any(path.name == "product-provisions.md" for path in shelf.rglob("*.md")))
        lock = install.parse_lock((shelf / "library" / "lock.yaml").read_text(encoding="utf-8"))
        self.assertEqual(lock["insitu-core"]["0.7.0"]["source"], "harvest")
        self.assertEqual(lock["envoy"]["0.2.3"]["source"], "harvest")
        self.assertEqual(lock["context-forge"]["0.4.1"]["source"], "harvest")
        self.assertEqual(lock["domainprime"]["0.1.0"]["source"], "copy")
        global_map = (shelf / "projects" / "_global" / "map.yaml").read_text(encoding="utf-8")
        self.assertEqual(global_map.count("methodology/product-provisions"), 1)
        self.assertIn("pack: insitu-core", global_map)
        self.assertIn("version: 0.7.0", global_map)
        registry = (top / "nexus.md").read_text(encoding="utf-8")
        self.assertNotIn("| engines |", registry)
        servers = json.loads((top / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]
        self.assertEqual(Path(servers["insitu"]["env"]["INSITU_ROOT"]), top.resolve())
        self.assertEqual(Path(servers["insitu"]["env"]["INSITU_HOME"]), shelf.resolve())
        self.assertEqual(Path(servers["envoy"]["env"]["ENVOY_ROOT"]), top.resolve())
        self.assertEqual(
            Path(servers["contextforge"]["env"]["CONTEXTFORGE_ROOT"]), top.resolve()
        )
        self.assertEqual(servers["insitu"]["args"][-1], "insitu")
        self.assertTrue(servers["insitu"]["args"][-2].endswith("engines/insitu"))
        self.assertTrue(servers["envoy"]["args"][-2].endswith("engines/envoy"))
        self.assertTrue(servers["contextforge"]["args"][-2].endswith("engines/context-forge"))
        self.assertNotIn("platforms.yaml", (top / ".mcp.json").read_text(encoding="utf-8"))
        self.assertFalse((top / "engines" / "brain-forge").exists())
        self.assertNotIn("brain-forge", lock)
        self.assertFalse(any(path.name == "vault-drop.md" for path in shelf.rglob("*.md")))

    def test_update_reharvests_and_does_not_repeat_the_import(self):
        top = self.tmp / "garden"
        self._install(top)
        copied = (
            top
            / "shelf"
            / "library"
            / "envoy"
            / "0.2.3"
            / "articles"
            / "methodology"
            / "envoy-status.md"
        )
        copied.write_text("stale\n", encoding="utf-8")
        self._install(top, update=True)
        self.assertEqual(copied.read_text(encoding="utf-8"), "# Status\n\nA public contract line.\n")
        global_map = (top / "shelf" / "projects" / "_global" / "map.yaml").read_text(
            encoding="utf-8"
        )
        self.assertEqual(global_map.count("imports:"), 1)
        self.assertTrue((top / "engines" / "insitu" / "provisions" / "pack.yaml").is_file())

    def test_engine_missing_manifest_refuses(self):
        def fetch(repo, tag, dest):
            dest.mkdir(parents=True)
            (dest / "README.md").write_text("empty\n", encoding="utf-8")

        top = self.tmp / "garden"
        with self.assertRaises(install.InstallError) as caught:
            install.install_tree(ROOT, top, fetch=fetch)
        self.assertIn("provisions/pack.yaml", str(caught.exception))

    def test_pins_are_the_every_install_rows(self):
        rows = []
        optional = None
        for line in (ROOT / "README.md").read_text(encoding="utf-8").splitlines():
            if not line.startswith("| "):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if "every install" in line:
                rows.append((cells[1], cells[2]))
            if "only when" in line:
                optional = (cells[1], cells[2])
        self.assertEqual([(pin["repo"], pin["tag"]) for pin in install.PINS], rows)
        self.assertEqual((install.BRAIN_FORGE["repo"], install.BRAIN_FORGE["tag"]), optional)

    def test_including_brain_forge_adds_the_vault_and_the_theme_pack(self):
        top = self.tmp / "garden"
        self._install(top, brain_forge=True)
        self._assert_brain_forge(top)
        self.assertNotIn("library:", (top / "nexus.md").read_text(encoding="utf-8"))
        needle = "Sco" + "tt"
        other = "Mac" + "key"
        own = {str(top.resolve()), top.resolve().as_posix()}
        hits = []
        for path in top.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for item in own:
                text = text.replace(item, "")
            if needle in text or other in text:
                hits.append(str(path.relative_to(top)))
        self.assertEqual(hits, [])

    def test_second_run_adds_brain_forge_without_rebuilding(self):
        top = self.tmp / "garden"
        self._install(top)
        registry = top / "nexus.md"
        registry.write_text(registry.read_text(encoding="utf-8") + "SENTINEL\n", encoding="utf-8")
        marker = top / "engines" / "insitu" / "MARKER"
        marker.write_text("keep\n", encoding="utf-8")
        calls = []

        def fetch(repo, tag, dest):
            calls.append(repo.rstrip("/").rsplit("/", 1)[-1])
            fixture_fetch(repo, tag, dest)

        self._install(top, brain_forge=True, fetch=fetch)
        self.assertEqual(calls, ["brain-forge"])
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep\n")
        self.assertIn("SENTINEL", registry.read_text(encoding="utf-8"))
        self._assert_brain_forge(top)

    def test_update_adds_brain_forge_only_when_asked_and_then_keeps_it(self):
        top = self.tmp / "garden"
        self._install(top)
        self._install(top, update=True)
        self.assertFalse((top / "engines" / "brain-forge").exists())
        self._install(top, update=True, brain_forge=True)
        self._assert_brain_forge(top)
        theme = self._theme()
        copied = (
            top
            / "shelf"
            / "library"
            / theme["id"]
            / theme["version"]
            / "articles"
            / "methodology"
            / "vault-drop.md"
        )
        harvested = (
            top
            / "shelf"
            / "library"
            / "brain-forge"
            / "0.1.0"
            / "articles"
            / "methodology"
            / "capture-types.md"
        )
        copied.write_text("stale\n", encoding="utf-8")
        harvested.write_text("stale\n", encoding="utf-8")
        self._install(top, update=True)
        self.assertTrue(copied.read_text(encoding="utf-8").startswith("---"))
        self.assertEqual(
            harvested.read_text(encoding="utf-8"),
            "# Types\n\nA public contract line.\n",
        )

    def _theme(self):
        return install.parse_manifest(
            (ROOT / "provisions" / "theme" / "pack.yaml").read_text(encoding="utf-8")
        )

    def _assert_brain_forge(self, top):
        theme = self._theme()
        version = top / "shelf" / "library" / theme["id"] / theme["version"]
        for item in theme["articles"]:
            rel = Path("articles") / Path(*item["id"].split("/")).with_suffix(".md")
            self.assertTrue((version / rel).is_file(), item["id"])
        pack = (version / "pack.yaml").read_text(encoding="utf-8")
        self.assertIn("kind: theme", pack)
        self.assertNotIn("\nroles:", "\n" + pack)
        self.assertTrue(
            (
                top
                / "shelf"
                / "library"
                / "brain-forge"
                / "0.1.0"
                / "articles"
                / "methodology"
                / "capture-types.md"
            ).is_file()
        )
        self.assertTrue((top / "engines" / "brain-forge" / "provisions" / "pack.yaml").is_file())
        lock = install.parse_lock(
            (top / "shelf" / "library" / "lock.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(lock["brain-forge"]["0.1.0"]["source"], "harvest")
        self.assertEqual(lock[theme["id"]][theme["version"]]["source"], "copy")
        servers = json.loads((top / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]
        self.assertEqual(set(servers), {"insitu", "envoy", "contextforge"})
        for folder in ("projects", "roles"):
            for path in (top / "shelf" / folder).rglob("*"):
                if not path.is_file():
                    continue
                body = path.read_text(encoding="utf-8")
                for item in theme["articles"]:
                    self.assertNotIn(item["id"], body, str(path))

    def test_usage(self):
        self.assertEqual(install.main([]), 2)
        self.assertEqual(install.main(["--with-brain-forge"]), 2)


if __name__ == "__main__":
    unittest.main()
