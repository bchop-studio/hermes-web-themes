#!/usr/bin/env python3
"""Validate dashboard theme YAMLs against the Hermes web server schema.

Mirrors _normalise_theme_definition() in hermes_cli/web_server.py:
every theme in themes/ must parse as YAML, have a non-empty name, valid
palette layers, and only known colorOverrides keys.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

OVERRIDE_KEYS = {
    "card", "cardForeground", "popover", "popoverForeground",
    "primary", "primaryForeground", "secondary", "secondaryForeground",
    "muted", "mutedForeground", "accent", "accentForeground",
    "destructive", "destructiveForeground", "success", "warning",
    "border", "input", "ring",
}
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
TYPO_KEYS = {"fontSans", "fontMono", "fontDisplay", "fontUrl",
             "baseSize", "lineHeight", "letterSpacing"}
DENSITIES = {"compact", "comfortable", "spacious"}


def check_layer(theme_file: str, key: str, spec, errors: list[str]) -> None:
    if isinstance(spec, str):
        if not HEX_RE.match(spec):
            errors.append(f"{theme_file}: palette.{key} bad hex {spec!r}")
        return
    if not isinstance(spec, dict):
        errors.append(f"{theme_file}: palette.{key} must be hex or mapping")
        return
    hexv = spec.get("hex")
    if not isinstance(hexv, str) or not HEX_RE.match(hexv):
        errors.append(f"{theme_file}: palette.{key}.hex bad {hexv!r}")
    alpha = spec.get("alpha", 1.0)
    if not isinstance(alpha, (int, float)) or not 0.0 <= alpha <= 1.0:
        errors.append(f"{theme_file}: palette.{key}.alpha bad {alpha!r}")


def validate(path: Path, errors: list[str]) -> None:
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        errors.append(f"{path.name}: YAML parse error: {exc}")
        return
    if not isinstance(data, dict):
        errors.append(f"{path.name}: top level must be a mapping")
        return

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append(f"{path.name}: missing name")
    elif path.stem != name:
        errors.append(f"{path.name}: name {name!r} does not match filename")

    palette = data.get("palette")
    if not isinstance(palette, dict):
        errors.append(f"{path.name}: missing palette mapping")
        return
    for key in ("background", "midground", "foreground"):
        if key not in palette:
            errors.append(f"{path.name}: palette.{key} missing")
        else:
            check_layer(path.name, key, palette[key], errors)

    glow = palette.get("warmGlow")
    if glow is not None and not isinstance(glow, str):
        errors.append(f"{path.name}: warmGlow must be a string")
    noise = palette.get("noiseOpacity")
    if noise is not None:
        try:
            float(noise)
        except (TypeError, ValueError):
            errors.append(f"{path.name}: noiseOpacity not a number")

    typo = data.get("typography", {})
    if not isinstance(typo, dict):
        errors.append(f"{path.name}: typography must be a mapping")
    else:
        for key, val in typo.items():
            if key not in TYPO_KEYS:
                errors.append(f"{path.name}: unknown typography key {key!r}")
            elif not isinstance(val, str) or not val.strip():
                errors.append(f"{path.name}: typography.{key} must be a string")

    layout = data.get("layout", {})
    if not isinstance(layout, dict):
        errors.append(f"{path.name}: layout must be a mapping")
    else:
        density = layout.get("density")
        if density is not None and density not in DENSITIES:
            errors.append(f"{path.name}: bad density {density!r}")
        radius = layout.get("radius")
        if radius is not None and (not isinstance(radius, str) or not radius.strip()):
            errors.append(f"{path.name}: radius must be a string")

    overrides = data.get("colorOverrides", {})
    if not isinstance(overrides, dict):
        errors.append(f"{path.name}: colorOverrides must be a mapping")
    else:
        for key, val in overrides.items():
            if key not in OVERRIDE_KEYS:
                errors.append(f"{path.name}: unknown colorOverrides key {key!r}")
            elif not isinstance(val, str) or not val.strip():
                errors.append(f"{path.name}: colorOverrides.{key} must be a string")


def main() -> int:
    themes_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path(__file__).resolve().parent.parent / "themes")
    files = sorted(themes_dir.glob("*.yaml"))
    if not files:
        print(f"no theme files in {themes_dir}")
        return 1
    errors: list[str] = []
    for f in files:
        validate(f, errors)
    if errors:
        print(f"FAILED: {len(errors)} problem(s) across {len(files)} themes")
        for e in errors:
            print(f"  {e}")
        return 1
    print(f"OK: {len(files)}/{len(files)} themes valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
