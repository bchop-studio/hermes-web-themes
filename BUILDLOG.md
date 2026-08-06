# BUILDLOG

Reverse-chronological build log for hermes-web-themes.

## 2026-08-05 — feat/theme-demo-titles: title cards on demo clip

- Built opening card ("hermes-web-themes" / "50 themes. One dashboard.")
  and closing card ("Install in one step" / copy-to-`~/.hermes/dashboard-themes/`
  one-liner) as 1600x900 PNGs via ffmpeg drawtext on a #0d0f14 background
  (DejaVu Sans / Sans Mono).
- Rendered each card to 1.5s h264 (libx264, crf 18, 25fps, yuv420p, 0.25s
  fade in/out), re-encoded the raw demo with a matching fade-in, and
  concat-demuxed to `assets/theme-demo-titles.mp4`.
- ffprobe verified: h264, 1600x900, 20.6s. Extracted 3 frames (0.75s / 10s /
  20s); card text confirmed legible on both cards.
- README: linked the titled trailer next to the raw demo clip.

## 2026-08-05 — chore/preview-assets: screenshots + demo clip

- Captured 12 theme screenshots (1600x900) on the live dashboard at
  localhost:9119 with Playwright, driving the sidebar theme switcher
  (`div[role="listbox"] button[role="option"]`, labels are title-case).
  Themes: Hermes Teal, Nous Blue, Midnight, Cyberpunk, Rosé, Ember,
  Obsidian, Vaporwave Mall, Commodore 64, Glitch Punk, Rice Paper,
  Void Sunset.
- Assembled `assets/theme-grid.png` (2448x2060 contact sheet, PIL,
  3 columns with labels).
- Recorded a 17.6s demo clip (Playwright video -> ffmpeg
  `setpts=PTS/1.45`, h264 yuv420p, 1600x900) cycling 7 themes; saved as
  `assets/theme-demo.mp4`.
- README: preview section with grid embedded and clip linked.

## 2026-08-05 — feat/dashboard-themes-50: initial 50-theme port

- Cloned empty repo; bootstrapped remote `main` with an empty root commit
  (one-time setup), then branched `feat/dashboard-themes-50`.
- `scripts/convert.py`: converts all 50 skins from
  `~/github/hermes-skins-pack/skins/*.yaml` into dashboard theme YAMLs.
  Mapping: `colors.background` -> `palette.background`;
  `ui_text`/`ui_label` -> `palette.midground`; foreground transparent
  (alpha 0.0); `ui_accent` -> `warmGlow` + primary/accent/ring overrides;
  `ui_border` -> border/input; `ui_ok/ui_warn/ui_error` ->
  success/warning/destructive. warmGlow alpha 0.35 on dark backgrounds,
  0.25 on light; accent foreground picked by accent luminance.
- `scripts/validate.py`: schema-checks every theme against the fields
  `_normalise_theme_definition` consumes. Result: `OK: 50/50 themes valid`.
- Spot-check: copied alabaster, obsidian, vaporwave-mall into
  `~/.hermes/dashboard-themes/` and confirmed they appear in
  `GET http://localhost:9119/api/dashboard/themes`.
- README with install + regenerate instructions; `.hermes.md` lifecycle
  rules; `.gitignore`; `requirements.txt` (pyyaml).
