# Ulauncher - Unicode Extension

Unicode Extension for Ulauncher.

- **Ulauncher**: [Ulauncher — Application launcher for Linux](https://ulauncher.io/)
- **Unicode**: [Unicode – The World Standard for Text and Emoji](https://home.unicode.org/) ([Unicode - Wikipedia](https://en.wikipedia.org/wiki/Unicode))

This is personal project.

## How to use

> **Note**
>
> If you are looking for an extension to search for and type emojis,
> i highly recommend to use Emoji Extension of Ulauncher.
>
> [Emoji — Ulauncher Extensions](https://ext.ulauncher.io/-/github-ulauncher-ulauncher-emoji) ([GitHub - Ulauncher/ulauncher-emoji: Emoji Extension](https://github.com/Ulauncher/ulauncher-emoji))

<!-- **TODO: Demo Gif** -->

![Main screenshot](./screenshots/demo-a.png)

Supported Features:

- Search Unicode character
- Convert letter to Unicode info

This extension supports 149,251 characters
(149,186 characters of Unicode Standard + 65 control characters)
of the latest Unicode 15.0.0.
[Unicode Character Count V15.0](https://www.unicode.org/versions/stats/charcountv15_0.html)

## How to Install

1. Ulauncher should installed
2. Install [RapidFuzz](https://github.com/maxbachmann/RapidFuzz)

   ```bash
   pip install rapidfuzz
   ```

3. Install Unicode Extension(this) on Ulauncher

   How to install Extension on Ulauncher: [About — Ulauncher Extensions](https://ext.ulauncher.io/about)

   > Ulauncher Preferences - Extensions - Add extension - Enter `https://github.com/yeoneer/ulauncher-unicode`

Detail about version requirements:

- Ulauncher: Tested with Ulauncher 5.15.0 (latest release)
- Python: Tested with Python 3.10.6(latest on Ubuntu 22.04).
  It may not work on lower versions.

## Troubleshooting

- **Unicode character icons do not shown properly**:

  The icon for a character depends on the fonts installed on your device
  and the 'Unicode Character Icon Font' preference.

  Ensure that you have the appropriate preference or font installed that is
  capable of displaying the character.

  If the icon is Block Icon(🛇, Prohibited Icon), it means that the character
  is a non-printable character. In Unicode, it's a Control Character.
  [Control character - Wikipedia](https://en.wikipedia.org/wiki/Control_character)

- **'Unicode Character Icon Font' preference changes not affected immediately**:

  This preference changes will not take effect properly
  until Ulauncher is restarted.

## License

> Unicode is a registered trademark of Unicode, Inc. in the United States
> and other countries. This application is not in any way associated with
> or endorsed or sponsored by Unicode, Inc. (aka The Unicode Consortium).

```text
Copyright (C) 2022 yeoneer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
```

See also Full GNU GPL v3.0: [LICENSE](./LICENSE)
