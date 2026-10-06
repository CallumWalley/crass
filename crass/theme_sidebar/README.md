# theme_sidebar

A modern two column layout. A coloured sidebar holds contact details, education and the short lists, and the main column has a timeline of experience and projects (a nod to `theme_metro`'s lines).

## Options

| Option | Default | Description |
| --- | --- | --- |
| `color_primary` | `#20515f` | Sidebar and accent colour. Any css colour, dark enough for white text. |
| `show_portrait` | `True` | Show `basics.image`, as a circle at the top of the sidebar. |

## CV sections used

| Section | Fields used |
| --- | --- |
| `basics` | `name`, `label`, `summary`, `image`, `location` (every value), `contact` (every value; `email` and `phone` get their own icons and links) |
| `profiles` | `username`, `url`, `fa_icon_class` ([Font Awesome 6](https://fontawesome.com/search?o=r&m=free) class, e.g. `fa-brands fa-github`) |
| `work`, `volunteer`, `projects` | `name`, `name_long` (shown instead of `name`), `start_date`, `end_date`, `position`, `description`, `highlights`, `url` (shown if there are no `highlights`) |
| `education` | `name`, `name_long`, `position`, `start_date`, `end_date` |
| `skills` | `name`, `highlights` |
| `languages` | `language`, `rating` (grouped by rating) |
| `qualifications` | `name`, `issuer`, `issuer_short` (shown instead of `issuer`) |
| `awards` | `name`, `awarder` |
| `interests` | `name` |
| `references` | `name`, `reference`, `contact` (every value) |

`work` and `volunteer` are shown together under 'Experience'.
Items are sorted newest first by `start_date`, items without one go last in the order given.
