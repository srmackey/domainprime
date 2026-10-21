"""Installer checks. Run from the product root: py -3 -m unittest discover -s tests"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import install


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

    def test_install_writes_the_registry_and_the_three_roles(self):
        top = self.tmp / "garden"
        install.install_tree(ROOT, top)
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
        install.install_tree(ROOT, top)
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
        install.install_tree(ROOT, top, update=True)
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
        install.install_tree(ROOT, top)
        with self.assertRaises(install.InstallError):
            install.install_tree(ROOT, top)

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
        install.install_tree(ROOT, top)
        needle = "Sco" + "tt"
        other = "Mac" + "key"
        hits = []
        for path in top.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if needle in text or other in text:
                hits.append(path)
        self.assertEqual(hits, [])

    def test_usage(self):
        self.assertEqual(install.main([]), 2)


if __name__ == "__main__":
    unittest.main()
