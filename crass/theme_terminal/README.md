# theme_terminal

Your CV as a terminal session, in JetBrains Mono. Sections are drawn like the output of `tree`, and contact details as yaml.

## Options

| Option | Default | Description |
| --- | --- | --- |
| `color_primary` | `#3fb950` | Prompt and name colour. Any css colour. |
| `dark` | `True` | Dark background. `False` for a light one (kinder to printers). |
| `show_portrait` | `False` | Show `basics.image` in the header, as a duotone in `color_primary`, with scanlines. |

## CV sections used

| Section | Fields used |
| --- | --- |
| `basics` | `name` (the first name is also the prompt's user), `label`, `summary`, `image`, `location` (every value), `contact` (every value) |
| `profiles` | `network`, `username`, `url` |
| `work`, `volunteer`, `education`, `projects`, `skills` | `slug` (shown as the directory name), `name`, `name_long`, `position`, `start_date`, `end_date`, `description`, `url`, `highlights` |
| `languages` | `language`, `rating` (grouped by rating) |
| `qualifications` | `slug`, `name`, `issuer`, `issuer_short` |
| `awards` | `slug`, `name`, `awarder` |
| `interests` | `name` |
| `references` | `name`, `reference`, `contact` (every value) |

`work` and `volunteer` are shown together under 'experience'.
Items are sorted newest first by `start_date`, items without one go last in the order given.
