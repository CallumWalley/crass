# Specification

A build takes three inputs:

- a **CV file**, containing all of your CV info;
- a **vibes file**, describing each variant of the CV to build;
- a **theme**, which turns the (filtered) CV into HTML.

`crass build CurriculumVitae.yaml vibes.yaml --out docs` builds every vibe, plus an `index.html` for flicking between them.

## CV file

A yaml or json mapping. Loosely follows [JSON Resume](https://jsonresume.org/schema/), but crass itself only cares about the shape:

- Each top-level key is a **section**.
- A section is either a mapping (e.g. `basics`), or a list of mappings (e.g. `work`, `skills`).
- Every item in a list section gets a `slug`, used to select it from a vibe's `mask`.
  The slug is the slugified value of the first of these keys the item has:
  `slug`, `name`, `network`, `organization`, `institution`, `title`, `language`.
  e.g. `name: Auckland Rescue Helicopter Trust` gets the slug `auckland-rescue-helicopter-trust`.

Which sections and fields actually appear is up to the theme, see the theme's README.

## Vibes file

A yaml or json list. Each item is one vibe, with the following keys.

| Key | Required | Description |
| --- | --- | --- |
| `name` | no | Name of this vibe, used in the index page (and its URL, `index.html?name`). Defaults to the output's file name. |
| `outputs` | yes | List of output files. Supports `.html` and `.pdf` (`.pdf` needs [wkhtmltopdf](https://wkhtmltopdf.org/), and is currently unreliable). |
| `theme` | no | Path to a theme directory. Defaults to the bundled `theme_metro`. |
| `theme_options` | no | Mapping that overrides the theme's `options`. |
| `includes` | no | Directory whose contents are copied next to the outputs, e.g. images referenced by the CV. |
| `mask` | no | What to include from the CV, see below. Defaults to everything. |
| `overwrite` | no | A mapping mirroring the CV file. Values here replace CV values for this vibe only. Keys not already in the CV are ignored. |

When building with `crass build`, `outputs` are relative to `--out`, and `includes` and `theme` are relative to the vibes file.

### Mask

The mask mirrors the shape of the CV.

- `true` / `false`: include all / none of this.
- A mapping: include only the listed keys, applying each key's value as a mask. Keys not listed are dropped.
- A list of slugs: include only these items, in this order.

```yaml
- name: engineering
  outputs:
    - engineering.html
  theme_options:
    color_primary: rgb(0, 100, 8)
  overwrite:
    basics:
      label: Engineer
  mask:
    basics: true      # all of basics
    work: true        # every job
    skills:           # only these skills, in this order
      - cad
      - hpc
                      # anything not listed, e.g. 'references', is dropped
```

## Theme

A directory containing a `theme.yaml`, and the jinja templates it names.

### `theme.yaml`

| Key | Required | Description |
| --- | --- | --- |
| `env` | yes | Directory containing all templates, relative to the theme directory. Can be `.`. |
| `base` | yes | The template to render, relative to `env`. |
| `options` | no | Default options, available to templates as `options`. Vibes can override them with `theme_options`. |
| `includes` | no | Directory whose contents are copied next to the outputs, e.g. fonts or css. Nest assets in a directory named after the theme, so they don't clash with a vibe's `includes`. |

### Templates

The base template is rendered with:

- `cv`: the CV, after the vibe's `mask` and `overwrite` are applied.
- `options`: the theme's `options`, updated with the vibe's `theme_options`.

A theme should document which CV sections and fields it uses, and its `options`, in a `README.md`.

```tree
my-theme/
├── theme.yaml
├── README.md
├── includes/
│   └── my-theme/
│       └── img1.png
└── templates/
    ├── main.html.jinja
    └── header.html.jinja
```
