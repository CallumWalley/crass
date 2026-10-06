# theme_ledger

A classic, single column serif layout (EB Garamond), with dates hanging in the margin. For when the vibe is 'formal'.
Sections without any dates (e.g. projects) and skills are set in two columns.

## Options

| Option | Default | Description |
| --- | --- | --- |
| `color_primary` | `#7b2d26` | Colour of rules, section titles and links. Any css colour. |
| `show_portrait` | `False` | Show `basics.image`, small and greyscale, in the header. |

## CV sections used

| Section | Fields used |
| --- | --- |
| `basics` | `name`, `label`, `summary`, `image`, `location` (every value), `contact` (every value) |
| `profiles` | `username`, `url` |
| `work`, `volunteer`, `education`, `projects` | `name`, `name_long` (shown instead of `name`), `start_date`, `end_date`, `position`, `description`, `highlights`, `url` (shown if there are no `highlights`) |
| `skills` | `name`, `description`, `highlights` |
| `languages` | `language`, `rating` (grouped by rating) |
| `qualifications` | `name`, `issuer`, `issuer_short` (shown instead of `issuer`) |
| `awards` | `name`, `awarder` |
| `interests` | `name`, `highlights` |
| `references` | `name`, `reference`, `contact` (every value) |

`work` and `volunteer` are shown together under 'Experience'.
Items are sorted newest first by `start_date`, items without one go last in the order given.
