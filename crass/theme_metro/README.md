# theme_metro

The default crass theme. A one page, print friendly layout, with a 'metro line' tree in `color_primary`.

## Options

| Option | Default | Description |
| --- | --- | --- |
| `color_primary` | `#ca6200ef` | Colour of lines and bullets. Any css colour. |
| `show_portrait` | `True` | Show `basics.image` in the header. |

## CV sections used

Any other sections (e.g. `awards`, `interests`) are ignored.

| Section | Fields used |
| --- | --- |
| `basics` | `name`, `label`, `image`, `location` (every value), `contact` (every value) |
| `profiles` | `username`, `url`, `fa_icon_class` ([Font Awesome 4](https://fontawesome.com/v4/icons/) class, e.g. `fa fa-github`) |
| `education`, `work`, `volunteer`, `projects`, `skills` | `name`, `name_long` (shown instead of `name`), `start_date`, `end_date`, `position`, `description`, `highlights`, `url` (shown if there are no `highlights`) |
| `languages` | `language`, `rating` (languages are grouped by rating) |
| `qualifications` | `name`, `issuer`, `issuer_short` (shown instead of `issuer`) |
| `references` | `name`, `reference`, `contact` (every value; `phone` and `email` get their own icons) |

`work` and `volunteer` are shown together under 'Employment'.
