from __future__ import annotations

import runpy
import unittest
from pathlib import Path
from typing import Any, Callable

import yaml

ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = ROOT / "themes"
validate_theme: Callable[[Path, list[str]], Any] = runpy.run_path(
    str(ROOT / "scripts" / "validate.py")
)["validate"]


class ThemePackTests(unittest.TestCase):
    def test_pack_contains_100_unique_valid_themes(self) -> None:
        files = sorted(THEMES_DIR.glob("*.yaml"))
        self.assertEqual(len(files), 100)

        names: list[str] = []
        errors: list[str] = []
        for path in files:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            names.append(data["name"])
            validate_theme(path, errors)

        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
