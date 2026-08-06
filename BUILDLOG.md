# BUILDLOG

Reverse-chronological build log for hermes-web-themes.

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
