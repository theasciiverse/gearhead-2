#!/usr/bin/env python3
"""drive.py SOCKET SESSION SECONDS: plays the start of GearHead 2 in a tmux
pane. Create Character in Basic mode with a name typed in, then Start RPG
Campaign with that character, the opening message, and a walk: each step
goes along the shortest path to the nearest map cell next to unexplored
ground, so the character explores the building and the streets outside.
A conversation is left with [Goodbye], reached with Down from the first
reply; when nothing is left to explore it steps off the edge of the area,
out onto the world map; a message or window that hides the map is
dismissed with Enter or Space, taking turns. After SECONDS it
quits to the title menu with Q (the game saves), and record-preview.sh
closes the pane. Run by record-preview.sh under asciinema."""
import collections, random, subprocess, sys, time

SOCK, S, SECONDS = sys.argv[1], sys.argv[2], float(sys.argv[3])
DEBUG = len(sys.argv) > 4
MAP_COLS, MAP_ROWS = 54, 20          # the map view, left of the info panel
BLOCK = set("#|") | set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz%&")
MOVES = {(-1, 0): "Up", (1, 0): "Down", (0, -1): "Left", (0, 1): "Right"}

def tmux(*a): return subprocess.run(["tmux", "-L", SOCK, *a], capture_output=True, text=True).stdout
def key(*k): tmux("send-keys", "-t", S, *k)
def screen(): return tmux("capture-pane", "-p", "-t", S).split("\n")

def wait_for(text, timeout=10):
    end = time.time() + timeout
    while time.time() < end:
        if any(text in l for l in screen()):
            return True
        time.sleep(0.2)
    return False

target = None
walls = set()          # cells a step into was refused ("Blocked!")
last = (None, None)    # where we were and the move we sent

def step(rows, visited):
    """The next arrow key: towards the current target, a cell beside unexplored
    ground, kept until reached so the walk does not dither."""
    global target, last
    g = [r.ljust(MAP_COLS)[:MAP_COLS] for r in (rows + [""] * MAP_ROWS)[:MAP_ROWS]]
    me = next(((y, x) for y in range(MAP_ROWS) for x in range(MAP_COLS) if g[y][x] == "@"), None)
    if not me:
        return None
    visited[me] = visited.get(me, 0) + 1
    msgs = [l for l in rows[MAP_ROWS:] if l.startswith("> ")]
    if last[0] == me and last[1] and msgs and msgs[-1].startswith("> Blocked"):
        walls.add((me[0] + last[1][0], me[1] + last[1][1]))
        target = None
    def free(y, x): return 0 <= y < MAP_ROWS and 0 <= x < MAP_COLS and g[y][x] not in BLOCK and g[y][x] != " " and (y, x) not in walls
    def go(d):
        global last
        last = (me, d)
        return MOVES[d]
    def frontier(y, x):
        return any(0 <= y + dy < MAP_ROWS and 0 <= x + dx < MAP_COLS and g[y + dy][x + dx] == " "
                   for dy, dx in MOVES) or x in (0, MAP_COLS - 1) or y in (1, MAP_ROWS - 1)
    if me == target:
        target = None
    prev, todo = {me: None}, collections.deque([me])
    while todo:
        c = todo.popleft()
        if c != me and (c == target or (target is None and frontier(*c) and c not in visited)):
            target = c
            while prev[c] != me:
                c = prev[c]
            return go((c[0] - me[0], c[1] - me[1]))
        for d in MOVES:
            n = (c[0] + d[0], c[1] + d[1])
            if n not in prev and free(*n):
                prev[n] = c
                todo.append(n)
    # all explored: step off the edge of the area into the unknown, out to
    # the next map, or walk to the nearest place where that can be done
    for d, k in MOVES.items():
        y, x = me[0] + d[0], me[1] + d[1]
        if 0 <= y < MAP_ROWS and 0 <= x < MAP_COLS and g[y][x] == " " and (y, x) not in walls:
            return go(d)
    prev, todo = {me: None}, collections.deque([me])
    while todo:
        c = todo.popleft()
        if c != me and frontier(*c):
            target = c
            while prev[c] != me:
                c = prev[c]
            return go((c[0] - me[0], c[1] - me[1]))
        for d in MOVES:
            n = (c[0] + d[0], c[1] + d[1])
            if n not in prev and free(*n):
                prev[n] = c
                todo.append(n)
    target = None
    last = (me, None)
    return None

start = time.time()
wait_for("Create Character")
time.sleep(2.0); key("Enter")                        # Create Character
wait_for("Select Mode"); time.sleep(1.5); key("Enter")     # Basic Mode
wait_for("Select Gender"); time.sleep(1.2); key("Enter")
wait_for("Romantic"); time.sleep(2.5); key("Enter")
wait_for("Enter a name"); time.sleep(0.8)
for c in "Rook":
    key("-l", c); time.sleep(0.25)
time.sleep(0.6); key("Enter")
wait_for("Start RPG Campaign"); time.sleep(2.0)
key("Down"); time.sleep(0.7); key("Down"); time.sleep(0.9); key("Enter")
if not wait_for("Select character file"):
    sys.exit("did not reach Start RPG Campaign")
time.sleep(1.0); key("Enter")
time.sleep(3.5); key("Enter")                        # the opening message
time.sleep(1.0)

visited, hidden, last_area = {}, 0, None
rng = random.Random(2)
while time.time() - start < SECONDS:
    rows = screen()
    opts = [l.strip(" |") for l in rows if l.strip(" |").startswith("[")]
    if "[Goodbye]" in opts:
        # the first reply is selected; step down to [Goodbye]
        time.sleep(2.5)
        for _ in range(opts.index("[Goodbye]")):
            key("Down"); time.sleep(0.3)
        key("Enter"); time.sleep(1.0)
        continue
    if not any("@" in l[:MAP_COLS] for l in rows[:MAP_ROWS]):
        if DEBUG:
            print(round(time.time() - start, 1), "NO @\n" + "\n".join(rows[:24]), file=sys.stderr)
        hidden += 1
        key("Enter" if hidden % 2 else "Space"); time.sleep(0.8)   # a message or window over the map
        continue
    area = rows[1][54:] if len(rows) > 1 else ""
    if area != last_area:       # a new area (the info panel changes): start afresh
        visited.clear(); walls.clear(); last_area = area
    k = step(rows, visited)
    if not k:
        k = rng.choice(list(MOVES.values()))   # boxed in: try any way
    key(k)
    time.sleep(0.3)
    if DEBUG:
        print(round(time.time() - start, 1), k, file=sys.stderr)
key("Q"); time.sleep(1.0)
print("\n".join(screen()), file=sys.stderr)
