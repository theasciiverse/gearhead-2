# GearHead 2 (Asciiverse packaging)

Joseph Hewitt's GearHead 2 (Free Pascal, LGPL-2.1-or-later), the second
roguelike mecha RPG in the series, packaged for the Asciiverse catalog (id
`gearhead-2`, binary `gearhead2`) in its ASCII version (`fpc -dASCII`), the
way GearHead: Arena and DRL are packaged. Not our code: keep changes small
and list every one in PATCHES.md.

- `upstream` is github.com/jwvhewitt/gearhead-2 (branch `master`); ours is
  branch `asciiverse`, `origin` github.com/theasciiverse/gearhead-2.
- Release: tag `v0.701+20241110-av.<n>` and push it;
  `.github/workflows/release.yml` builds Linux (static), macOS and
  .deb/.rpm/.apk/Arch packages. No Windows build.
- Build: `sh asciiverse/build.sh` (fpc 3.2.2), then `sh asciiverse/stage.sh`;
  run `stage/gearhead2`. The game reads gamedata/series/design/doc from the
  current folder; settings and saves go to ~/.config/gearhead2.
- Preview: `asciiverse/record-preview.sh` (asciinema 3, tmux, own socket
  `avrec-gh2`), about 45 s; characters and towns are random. The driver
  makes a character, starts a campaign, explores the first building and
  walks out into the town in a mecha. Conversations end with [Goodbye]
  (Down from the first reply); the title menu ignores Esc, so the script
  ends the recording by closing the pane after Q. `drive.py ... debug`
  logs each step.
- GearHead: Arena is packaged the same way in ../gearhead-1.
