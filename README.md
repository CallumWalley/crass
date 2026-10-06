# crass

Build several variants ('vibes') of your CV from a single file, so you can stay up to date with all the fads with minimal effort.

- Your CV lives in one yaml or json file.
- A vibes file describes each variant: what to include, what to change, which theme to use.
- `crass build` renders every vibe, plus an `index.html` for flicking between them. Handy for GitHub Pages.

See [SPECIFICATION.md](SPECIFICATION.md) for the file formats, and [theme_metro](crass/theme_metro/README.md) for the default theme.

## Setup

```sh
pip install git+https://github.com/CallumWalley/crass.git
```

Or for development:

```sh
git clone https://github.com/CallumWalley/crass.git
cd crass
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```sh
crass build CurriculumVitae.yaml vibes.yaml --out docs   # build everything into docs/
crass serve CurriculumVitae.yaml vibes.yaml --port 8000  # build, then serve at localhost:8000
```

The CV and vibes files default to `CurriculumVitae.yaml` and `vibes.yaml`.

Or from python:

```python
from crass import CurriculumVitae, build_site

build_site("CurriculumVitae.yaml", "vibes.yaml", "docs")

# Or a single vibe.
cv = CurriculumVitae("CurriculumVitae.yaml")
cv.generate_vibe(outputs=["docs/engineering.html"], mask={"basics": True, "work": True})
```

For a real example, see [CallumWalley/cv](https://github.com/CallumWalley/cv).
