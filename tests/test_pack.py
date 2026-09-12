from __future__ import annotations

import runpy
import unittest
from pathlib import Path
from typing import Any, Callable

import yaml

ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = ROOT / "themes"
SOURCE_SKINS_DIR = ROOT.parent / "hermes-skins-pack" / "skins"
EXPECTED_SOURCE_COUNT = 101
validate_theme: Callable[[Path, list[str]], Any] = runpy.run_path(
    str(ROOT / "scripts" / "validate.py")
)["validate"]


class ThemePackTests(unittest.TestCase):
    def test_pack_matches_every_source_skin(self) -> None:
        files = sorted(THEMES_DIR.glob("*.yaml"))
        source_skins = sorted(SOURCE_SKINS_DIR.glob("*.yaml"))
        self.assertEqual(
            len(source_skins),
            EXPECTED_SOURCE_COUNT,
            "source skin checkout is missing or not the pinned 101-theme release",
        )
        self.assertEqual(
            {path.stem for path in files},
            {path.stem for path in source_skins},
        )

        names: list[str] = []
        errors: list[str] = []
        for path in files:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            names.append(data["name"])
            validate_theme(path, errors)

        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(errors, [])

    def test_converter_reproduces_the_checked_in_pack(self) -> None:
        convert_theme = runpy.run_path(str(ROOT / "scripts" / "convert.py"))["convert"]
        source_skins = sorted(SOURCE_SKINS_DIR.glob("*.yaml"))
        self.assertEqual(len(source_skins), EXPECTED_SOURCE_COUNT)

        for skin_path in source_skins:
            theme = convert_theme(skin_path)
            checked_in = yaml.safe_load(
                (THEMES_DIR / f"{theme['name']}.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(checked_in, theme, skin_path.name)


if __name__ == "__main__":
    unittest.main()
