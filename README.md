# hermes-web-themes

Dashboard themes for the [Hermes Agent](https://github.com/NousResearch/hermes-agent)
web UI, ported from the 50 TUI skins in
[hermes-skins-pack](https://github.com/bchop-studio/hermes-skins-pack).

## Preview

![Theme grid — 12 of the 50 themes on the live dashboard](assets/theme-grid.png)

Short demo clip cycling themes on the real dashboard UI:
[assets/theme-demo.mp4](assets/theme-demo.mp4) (18s, 1600x900).

## Install

Copy or symlink the themes into your Hermes dashboard-themes directory:

```bash
mkdir -p ~/.hermes/dashboard-themes
cp themes/*.yaml ~/.hermes/dashboard-themes/
# or, to stay in sync with this repo:
ln -s "$PWD"/themes/*.yaml ~/.hermes/dashboard-themes/
```

Then pick a theme in the dashboard, or set it in config:

```bash
hermes config set dashboard.theme <name>
```

## Regenerate from the skins

Requires Python 3 with `pyyaml`.

```bash
python3 scripts/convert.py            # reads ~/github/hermes-skins-pack/skins
python3 scripts/validate.py           # validates all themes in themes/
```

`convert.py` accepts `--skins-dir` and `--out-dir` overrides.

## Theme format

One YAML per theme. Fields: `name`, `label`, `description`;
`palette` with `background` / `midground` / `foreground` layers
(each `{hex, alpha}`), `warmGlow` (rgba string) and `noiseOpacity`;
optional `typography` and `layout`; `colorOverrides` for shadcn token
accents (`primary`, `accent`, `border`, `success`, `warning`,
`destructive`, ...). The full schema is defined by
`_normalise_theme_definition` in `hermes_cli/web_server.py`.
