#!/bin/sh
# Lays out the av archive in stage/: the start script at the top, and the
# game in lib/ with the data it reads at run time. image/ is left out: it
# is only for the SDL version (the ASCII build does not check for it).
set -eu
rm -rf stage && mkdir -p stage/lib
cp asciiverse/gearhead2 stage/gearhead2
cp gearhead2 stage/lib/
cp -R gamedata series design doc stage/lib/
cp license.txt readme.txt history.txt PATCHES.md stage/
