# Contributing

Hermes Web Themes is generated from the palettes in
[`bchop-studio/hermes-skins-pack`](https://github.com/bchop-studio/hermes-skins-pack).
Add or change the source skin there first, then regenerate this pack.

## Regenerate

```bash
python3 scripts/convert.py --skins-dir ../hermes-skins-pack/skins
```

The converter must not rewrite an unchanged theme differently. Review the diff
and keep changes limited to the source skins being added or changed.

## Validate

Keep both repositories next to each other, then run:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The tests require the checked-in theme names to match the source skin names and
require every generated theme to match the converter output.

Do not commit credentials, local Hermes files, build logs, or generated work
that is unrelated to this pack.
