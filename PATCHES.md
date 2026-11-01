# Changes from upstream

This is the Asciiverse packaging of [GearHead 2](https://github.com/jwvhewitt/gearhead-2)
by Joseph Hewitt, the second game in the GearHead roguelike mecha RPG
series, built in its ASCII mode (`fpc -dASCII`, no SDL). Upstream is the
`upstream` remote; this build is upstream's `master` at `2f1f38b`
(2024-11-10), release 0.701 plus the commits since. The `asciiverse`
branch carries the changes below.

## Licence

LGPL-2.1-or-later: the source files say "either version 2.1 of the
License, or (at your option) any later version", and `license.txt` holds
the LGPL 2.1 text. The GearHead universe is copyright 2005 Joseph Hewitt.

## Code

- **Settings folder made in full.** On first start the game makes its
  settings folder (`~/.config/gearhead2`) and the `savegame` folder in it
  with `MkDir`, which makes one level only: with no `~/.config` yet it
  stopped with "EInOutError: File not found". `gears.pp` now uses
  `ForceDirectories`, which makes the missing parents too.

## Packaging (new files)

- `asciiverse/build.sh`: the ASCII build with Free Pascal 3.2; fully
  static on Linux (Free Pascal's own runtime, no libc).
- `asciiverse/gearhead2`, `asciiverse/stage.sh`: av's start script and
  the archive layout (binary and its data folders in `lib/`; the game reads
  them from the current folder, so the start script changes into `lib/`).
  `image/` is left out: only the SDL version uses it.
- `asciiverse/nfpm.yaml`: .deb, .rpm, .apk and Arch packages, installed in
  `/usr/lib/gearhead2` with `/usr/bin/gearhead2` a link to the start script.
- `asciiverse/record-preview.sh`, `asciiverse/drive.py`: the catalog
  preview, played by a script in a tmux pane.
- `.github/workflows/release.yml`: builds all of it on a tag.

## Not built

- Windows.
- The SDL (graphical) version.
