# ---
# name: Adaptive Hitbox
# icon: scope
# summary: Moves each key's target toward where you actually tap it
# version: 1.0
# author: Clink
# ---

# A hitbox that learns where you actually tap.
#
# on_touch(key, x, y, state) runs after every tap with the key it went to and
# where on that key the finger came down: x and y run from -0.5 to 0.5 across
# the key, 0 at its centre, y growing downwards. hitboxes(state) returns a
# dict from key names to hitbox(scale=, x=, y=): x and y move the key's target
# by that share of its size, scale grows or shrinks it around its centre. The
# keyboard reads hitboxes(state) when it opens and once a second after that.
#
# This keeps a running average of each key's landings and moves its target
# part of the way there once it has seen enough taps, so a key you always hit
# low and to the left starts listening low and to the left. The landings are
# measured against the drawn key, not the moved target, so the shift can't
# feed on itself.
MIN_TAPS = 12
LIMIT = 0.25

def initial():
    return {"on": True, "strength": 0.6, "keys": {}}

def settings(state):
    learned = len([k for k in state["keys"] if state["keys"][k][0] >= MIN_TAPS])
    return section("keys.hitboxes", [
        toggle("Learn where I tap", state["on"], action="on"),
        slider("Strength", state["strength"], min=0.2, max=1, step=0.1, key="strength"),
        text(f"{learned} keys learned"),
        button("Forget what it learned", action="reset"),
    ], title="Adaptive Hitbox")

def on_action(action, value, state):
    if action == "on":
        state["on"] = value
    elif action == "reset":
        state["keys"] = {}
    return state

def on_touch(key, x, y, state):
    if not state["on"] or len(key) != 1:
        return state
    seen = state["keys"].get(key, [0, 0.0, 0.0])
    count = min(seen[0] + 1, 200)
    # A running mean for the first taps, then a slow moving average, so the
    # target follows a change in grip without jumping on one stray tap.
    weight = 1 / count if count < 50 else 0.02
    seen[1] += (x - seen[1]) * weight
    seen[2] += (y - seen[2]) * weight
    seen[0] = count
    state["keys"][key] = seen
    return state

def hitboxes(state):
    if not state["on"]:
        return {}
    out = {}
    for key in state["keys"]:
        count, x, y = state["keys"][key]
        if count < MIN_TAPS:
            continue
        dx = max(-LIMIT, min(LIMIT, x * state["strength"]))
        dy = max(-LIMIT, min(LIMIT, y * state["strength"]))
        if abs(dx) > 0.01 or abs(dy) > 0.01:
            out[key] = hitbox(x=round(dx, 3), y=round(dy, 3))
    return out
