#!/usr/bin/env python3
"""Convert hermes-skins-pack TUI skins into Hermes dashboard theme YAMLs.

Reads ~/github/hermes-skins-pack/skins/*.yaml (or --skins-dir) and writes one
dashboard theme per skin into themes/ (or --out-dir).

Mapping:
  colors.background            -> palette.background
  colors.ui_text / ui_label    -> palette.midground (readable text layer)
  palette.foreground           -> transparent overlay (alpha 0.0)
  colors.ui_accent/banner_accent -> warmGlow + colorOverrides accents
  colors.ui_ok/ui_warn/ui_error -> success/warning/destructive overrides
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("pyyaml required: python3 -m pip install pyyaml")

OVERRIDE_KEYS = {
    "card", "cardForeground", "popover", "popoverForeground",
    "primary", "primaryForeground", "secondary", "secondaryForeground",
    "muted", "mutedForeground", "accent", "accentForeground",
    "destructive", "destructiveForeground", "success", "warning",
    "border", "input", "ring",
}

HEX_RE = re.compile(r"^#?[0-9a-fA-F]{6}$")


def norm_hex(value: str) -> str:
    v = value.strip()
    if not HEX_RE.match(v):
        raise ValueError(f"not a 6-digit hex color: {value!r}")
    return v if v.startswith("#") else f"#{v}"


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def chan(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def labelize(name: str) -> str:
    return " ".join(w.capitalize() for w in name.split("-"))


def convert(skin_path: Path) -> dict:
    skin = yaml.safe_load(skin_path.read_text())
    if not isinstance(skin, dict):
        raise ValueError(f"{skin_path}: not a mapping")
    colors = skin.get("colors") or {}

    name = skin.get("name") or skin_path.stem
    description = skin.get("description") or f"Ported from the {name} TUI skin"

    background = norm_hex(colors.get("background", "#0e0e0e"))
    midground = norm_hex(colors.get("ui_text") or colors.get("ui_label") or "#e5e5e5")
    accent = norm_hex(colors.get("ui_accent") or colors.get("banner_accent") or "#e0a040")
    border = norm_hex(colors.get("ui_border") or colors.get("banner_border") or "#404040")
    ok = colors.get("ui_ok")
    warn = colors.get("ui_warn")
    err = colors.get("ui_error")

    dark = luminance(background) < 0.4
    glow_alpha = 0.35 if dark else 0.25

    fg_on_accent = "#1a1a1a" if luminance(accent) > 0.4 else "#ffffff"
    overrides = {
        "primary": accent,
        "primaryForeground": fg_on_accent,
        "accent": accent,
        "accentForeground": fg_on_accent,
        "border": border,
        "input": border,
        "ring": accent,
    }
    if ok:
        overrides["success"] = norm_hex(ok)
    if warn:
        overrides["warning"] = norm_hex(warn)
    if err:
        overrides["destructive"] = norm_hex(err)

    # Keep only schema-valid keys (all of the above are, but guard anyway).
    overrides = {k: v for k, v in overrides.items() if k in OVERRIDE_KEYS}

    return {
        "name": name,
        "label": labelize(name),
        "description": description,
        "palette": {
            "background": {"hex": background, "alpha": 1.0},
            "midground": {"hex": midground, "alpha": 1.0},
            "foreground": {"hex": "#ffffff", "alpha": 0.0},
            "warmGlow": rgba(accent, glow_alpha),
            "noiseOpacity": 0.6,
        },
        "colorOverrides": overrides,
    }


class _Dumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skins-dir", type=Path,
                    default=Path.home() / "github/hermes-skins-pack/skins")
    ap.add_argument("--out-dir", type=Path,
                    default=Path(__file__).resolve().parent.parent / "themes")
    args = ap.parse_args()

    skins = sorted(args.skins_dir.glob("*.yaml"))
    if not skins:
        sys.exit(f"no skins found in {args.skins_dir}")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for skin_path in skins:
        theme = convert(skin_path)
        out = args.out_dir / f"{theme['name']}.yaml"
        out.write_text(
            "# Ported from bchop-studio/hermes-skins-pack "
            f"(skins/{skin_path.name})\n"
            + yaml.dump(theme, Dumper=_Dumper, sort_keys=False,
                        default_flow_style=False, allow_unicode=True)
        )
        print(f"  {out.name}")
    print(f"converted {len(skins)} skins -> {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
