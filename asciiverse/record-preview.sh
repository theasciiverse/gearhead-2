#!/bin/sh
# Records the 100x30 catalog preview, asciiverse/gearhead-2.cast
# (hub/RECORDING.md): a character made in Basic mode, a new RPG campaign,
# and a walk out of the first building, played by asciiverse/drive.py for
# 45 s. asciinema records a tmux pane (own socket, no status line, no user
# config) that drive.py reads and plays in. Characters are random, so
# takes differ.
# Needs asciinema 3 and tmux; run asciiverse/build.sh and stage.sh first.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
root=$(dirname "$here")
out=$here/gearhead-2.cast
home=$(mktemp -d)
trap 'tmux -L avrec-gh2 kill-server 2>/dev/null; rm -rf "$home"' EXIT
cp -R "$root/stage" "$home/game"
cd "$home"  # nothing in the recording names a local path
unset XDG_CONFIG_HOME
export HOME="$home" PATH="$home/game:$PATH" TERM=xterm-256color COLORTERM=truecolor LANG=C.UTF-8
tmux -L avrec-gh2 -f /dev/null new-session -d -s rec -x 100 -y 30 "gearhead2" \; set -g status off
python3 -I "$here/drive.py" avrec-gh2 rec 45 2>"$home/drive.log" &
drive=$!
asciinema rec --headless --overwrite -q \
  --window-size 100x30 --idle-time-limit 2 \
  --capture-env "TERM,COLORTERM,LANG" --title "GearHead 2" \
  --command "tmux -L avrec-gh2 attach -t rec" "$out" &
rec=$!
wait "$drive" || true
cat "$home/drive.log" >&2
sleep 2
# the title menu ignores Esc and its cursor position varies, so end the
# recording by closing the pane rather than by picking Quit Game
tmux -L avrec-gh2 kill-server 2>/dev/null || true
wait "$rec"
