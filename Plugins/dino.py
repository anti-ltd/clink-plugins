# ---
# name: Dino
# icon: hare
# summary: A runner on the space bar: tap to jump the dino over the cacti
# version: 2.0
# author: Clink
# ---

# A side-scroller on one key.
#
# Type "dino" anywhere to start, or add the Dino button from Layout > Top bar.
# Tap the space bar to jump and hold it to jump higher; the letters you press
# during a run are taken back out of the field, so nothing you play gets typed.
# Delete leaves. Switched off, the script is never called at all.
#
# Needs a Clink build with layered key art: `key_art` here returns two `art()`
# entries for the space bar, and each one animates on its own. That is the
# whole reason the game works. The keyboard redraws a plugin's art about once
# a second, so everything between frames is the keyboard easing from the last
# drawing to this one — and a world that has to scroll smoothly over a second
# cannot also hold a dino that has to hop in a fifth of one.
#
#   the world layer   aimed HORIZON seconds ahead, moved there linearly, and
#                     re-aimed every second: no stalls, no gallop
#   the dino layer    a fifth of a second, eased out, so a tap is a hop
#
# The script tracks both the way the keyboard draws them (`world_at`, `lift_at`
# mirror linear and SwiftUI's ease-out), so a crash is decided against the
# picture rather than an ideal position nobody saw.
import random
import time

LETTERS = "abcdefghijklmnopqrstuvwxyz"
TRIGGER = "dino"

# The world is measured in the key itself: x in key widths, y in key heights.
# A space bar is not a fixed number of points — key height is a setting and the
# keyboard is a different size on every device — so points would put the ground
# line off a short key and the dino's head through the top of a tall one.
HORIZON = 1.3         # how far ahead the world is aimed, and its ease duration
JUMP_UP = 0.18        # the dino's own duration, leaving the ground
JUMP_DOWN = 0.65      # and coming back down, slower, so a tap stays up long
                      # enough to clear something
GROUND = 0.34         # the ground line, below the middle of the key
DINO_X = 0.15         # the dino's centre, from the left edge
DINO_W = 0.078
DINO_H = 0.36
DINO_HIT = 0.05       # narrower than the drawing: the tail is not a hitbox
LIFT_MAX = 0.46       # a held jump reaches the top of the key and no further
SPAWN = 1.60          # where a cactus is made, past the right edge
FIRST = 1.50          # and where the first one of a run waits
GONE = -0.25          # and where it is forgotten
BASE_SPEED = 0.31     # key widths a second at the start of a run
RAMP = 0.005          # and how much faster every second after that
GAP = [1.0, 1.8]      # the distance between cacti
CACTI = [0.16, 0.22]  # the two heights
CACTUS_W = [0.05, 0.065]
FORGIVE = 0.06        # how much of a clip counts as a clean jump
SCORE = 32.0          # score per key width covered

SKY = "text"


def initial():
    return {"on": True, "trigger": True, "playing": False, "over": False,
            "best": 0, "score": 0, "t0": 0.0, "last": 0.0, "held": False,
            "obstacles": [], "sc": [0.0, 0.0, 0.0, 0.0], "dy": [0.0, 0.0, 0.0, 0.0],
            "tail": ""}


def settings(state):
    return section("keys.spacebar", [
        toggle("Dino", state["on"], action="on"),
        toggle("Type dino to start", state["trigger"], action="trigger"),
        text("Type dino anywhere to start a run, or add the Dino button from "
             "Layout > Top bar. Tap the space bar to jump, hold it to jump "
             "higher. Delete leaves the game, and nothing you press while "
             "playing is typed. Best run so far: " + str(state["best"]) + ".",
             size=13, color="gray"),
    ], title="Dino")


def on_action(action, value, state):
    if action == "trigger":
        state["trigger"] = value
    elif action == "on":
        state["on"] = value
        if not value:
            state = stop(state)
    elif action == "play":
        if state["playing"]:
            state = stop(state)
        elif layered():
            state = start(state)
        else:
            banner("Dino needs a newer Clink")
    return state


def bar_items(state):
    return [bar_button("play", "Dino", icon="hare", title="Dino")]


def events(state):
    # Read once when the plugins load: with Dino off the keyboard never calls
    # this script, rather than calling it on every key and being told no.
    if not state["on"]:
        return []
    return ["key", "key_down", "key_up", "tick", "backspace", "open", "close", "field"]


def on_event(name, info, state):
    if not state["on"]:
        return state
    if name == "key":
        return typed(info["text"], state)
    if not state["playing"]:
        return state
    if name in ("backspace", "open", "close", "field"):
        return stop(state)
    now = time.monotonic()
    if name == "tick":
        return frame(state, now)
    if name in ("key_down", "key_up") and info["key"] == "space":
        state = frame(state, now)
        if state["over"]:
            return state
        state["held"] = name == "key_down"
        return aim(state, now)
    return state


def typed(t, state):
    if not state["playing"]:
        return watching(t, state)
    if state["over"]:
        # A finished run: space goes again, and anything else is somebody
        # typing, so it leaves the game and keeps its keystroke.
        if t != " ":
            return stop(state)
        backspace(len(t))
        return start(state)
    if len(t) > 0:
        backspace(len(t))
    return state


def watching(t, state):
    if not state["trigger"] or len(t) != 1 or t.lower() not in LETTERS:
        state["tail"] = ""
        return state
    tail = (state["tail"] + t.lower())[-len(TRIGGER):]
    state["tail"] = tail
    if tail != TRIGGER:
        return state
    if not layered():
        # Checked before the word is taken back, so a build that cannot run
        # the game leaves what you typed alone.
        banner("Dino needs a newer Clink")
        state["tail"] = ""
        return state
    backspace(len(TRIGGER))
    return start(state)


def layered():
    """Whether this build can give a key two layers that animate separately.
    Without it the world and the dino would share one duration, which is not a
    game, so the run is refused rather than played blind."""
    try:
        art([shape("circle", size=2, fill="text")], animate=0.1, curve="linear")
        return True
    except Exception:
        return False


def start(state):
    now = time.monotonic()
    state["playing"] = True
    state["over"] = False
    state["held"] = False
    state["score"] = 0
    state["tail"] = ""
    state["t0"] = now
    state["last"] = now
    state["obstacles"] = [FIRST, FIRST + random_gap()]
    state["sc"] = [0.0, 0.0, now, 0.0]
    state["dy"] = [0.0, 0.0, now, 0.0]
    space_text("0")
    return aim(state, now)


def stop(state):
    state["playing"] = False
    state["over"] = False
    state["held"] = False
    state["tail"] = ""
    space_text(None)
    return state


def random_gap():
    return GAP[0] + random.random() * (GAP[1] - GAP[0])


# --- where things are drawn -------------------------------------------------

def progress(track, t):
    if track[3] <= 0.0:
        return 1.0
    u = (t - track[2]) / track[3]
    if u <= 0.0:
        return 0.0
    if u >= 1.0:
        return 1.0
    return u


def world_at(t, state):
    """The world moves at a steady rate: its layer is drawn with curve="linear",
    so the keyboard covers its ground evenly and the script can say where."""
    track = state["sc"]
    return track[0] + (track[1] - track[0]) * progress(track, t)


def lift_at(t, state):
    """The dino's layer eases out, which is SwiftUI's .easeOut — near enough
    1-(1-u)**1.68 to decide a crash by."""
    track = state["dy"]
    u = progress(track, t)
    return track[0] + (track[1] - track[0]) * (1.0 - (1.0 - u) ** 1.68)


def travelled(state, t):
    """The distance the world should have covered by t, speeding up as it goes."""
    dt = t - state["t0"]
    return BASE_SPEED * dt + RAMP * dt * dt / 2.0


def aim(state, now):
    """Re-aim the world, and point the dino wherever the finger says. The
    world is aimed further ahead than a tick is long, so it never arrives and
    never stalls waiting for the next drawing."""
    state["sc"] = [world_at(now, state), travelled(state, now + HORIZON), now, HORIZON]
    lift = LIFT_MAX if state["held"] else 0.0
    state["dy"] = [lift_at(now, state), lift, now, JUMP_UP if state["held"] else JUMP_DOWN]
    return state


def frame(state, now):
    """Run the game up to now against what was on the screen along the way."""
    if state["over"]:
        return state
    steps = 12
    start_t = state["last"]
    for i in range(1, steps + 1):
        t = start_t + (now - start_t) * i / steps
        if hit(state, t):
            return crash(state, now)
    state["last"] = now
    scroll = world_at(now, state)
    state["score"] = int(scroll * SCORE)
    state["obstacles"] = [w for w in state["obstacles"] if w - scroll > GONE]
    while len(state["obstacles"]) < 3 or state["obstacles"][-1] - scroll < SPAWN:
        last = state["obstacles"][-1] if state["obstacles"] else scroll + SPAWN
        state["obstacles"].append(last + random_gap())
    space_text(str(state["score"]))
    return aim(state, now)


def hit(state, t):
    scroll = world_at(t, state)
    lift = lift_at(t, state)
    for w in state["obstacles"]:
        x = w - scroll
        if abs(x - DINO_X) < (DINO_HIT + cactus_width(w)) / 2.0:
            if lift < cactus_height(w) - FORGIVE:
                return True
    return False


def crash(state, now):
    state["over"] = True
    state["last"] = now
    state["held"] = False
    if state["score"] > state["best"]:
        state["best"] = state["score"]
        banner("New best: " + str(state["score"]))
    else:
        banner(str(state["score"]) + " — best " + str(state["best"]))
    space_text(str(state["score"]) + "  best " + str(state["best"]))
    # Freeze the world where it stands and drop the dino.
    here = world_at(now, state)
    state["sc"] = [here, here, now, 0.0]
    state["dy"] = [lift_at(now, state), 0.0, now, JUMP_DOWN]
    return state


def cactus_kind(w):
    """Which of the two cacti this one is. Its own position picks it, so it
    never changes under the player and nothing has to be remembered."""
    return int(w * 100) % len(CACTI)


def cactus_height(w):
    return CACTI[cactus_kind(w)]


def cactus_width(w):
    return CACTUS_W[cactus_kind(w)]


# --- drawing ----------------------------------------------------------------

# The dino, facing right, as one closed outline in its own box.
DINO = [[0.00, 0.16], [0.18, 0.28], [0.32, 0.30], [0.44, 0.22], [0.50, 0.10],
        [0.58, 0.00], [0.88, 0.00], [1.00, 0.07], [1.00, 0.21], [0.76, 0.26],
        [0.62, 0.30], [0.58, 0.42], [0.56, 0.62], [0.52, 0.72], [0.52, 1.00],
        [0.40, 1.00], [0.40, 0.74], [0.32, 0.74], [0.32, 1.00], [0.20, 1.00],
        [0.20, 0.70], [0.14, 0.56], [0.10, 0.46]]

# A saguaro: trunk, one arm up each side.
CACTUS = [[0.36, 1.00], [0.36, 0.74], [0.12, 0.74], [0.12, 0.32], [0.24, 0.32],
          [0.24, 0.62], [0.36, 0.62], [0.36, 0.06], [0.62, 0.06], [0.62, 0.44],
          [0.76, 0.44], [0.76, 0.20], [0.88, 0.20], [0.88, 0.58], [0.62, 0.58],
          [0.62, 1.00]]


def key_art(state):
    if not state["on"] or not state["playing"]:
        return {}
    # Two layers on the one key: the ground and the cacti scroll for a second
    # and a bit at a steady rate, the dino hops in a fifth of a second. One
    # layer could only do one of those.
    return {"space": [art(world(state), animate=HORIZON, curve="linear"),
                      art([dino(state)], animate=state["dy"][3])]}


def world(state):
    ink = color(SKY, 0.85)
    # The ground's box needs a thickness of its own: a shape is drawn inside
    # its width and height, and a flat one paints nothing. The line runs down
    # the middle of it.
    shapes = [shape("line", anchor="center", unit="key", x=0.0, y=GROUND,
                    width=1.0, height=0.03, points=[[0.0, 0.5], [1.0, 0.5]],
                    stroke=color(SKY, 0.3), line_width=1.0)]
    for w in state["obstacles"]:
        # Where it is aimed, not where it is: the keyboard eases from what it
        # has to what the script asks for, so the target is what to hand it.
        x = w - state["sc"][1]
        if x < GONE or x > SPAWN:
            continue
        h = cactus_height(w)
        shapes.append(shape("path", anchor="left", unit="key", closed=True,
                            x=x, y=GROUND - h / 2.0, points=CACTUS,
                            width=cactus_width(w), height=h, fill=ink))
    return shapes


def dino(state):
    return shape("path", anchor="left", unit="key", closed=True,
                 x=DINO_X, y=GROUND - DINO_H / 2.0 - state["dy"][1],
                 width=DINO_W, height=DINO_H, points=DINO,
                 fill=color(SKY, 0.9))
