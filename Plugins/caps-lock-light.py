# ---
# name: Caps Lock Light
# icon: capslock
# summary: A little green lamp on shift that lights while caps lock is on
# version: 1.0
# author: Clink
# ---

# A lamp on a key.
#
# key_lights(state) returns a dict from key names to lamps. A lamp is
# key_light(color, off_color=, when=, corner=, size=, inset=, glow=), or just
# a colour string for a caps lock lamp in that colour. The keys that can carry
# one are "shift", "delete", "space", "return" and "globe".
#
# `when` says what lights it: "caps_lock" (the default), "shift" for shift in
# either state, or "always". The keyboard works that out itself, so the lamp
# follows caps lock the moment it changes and this script never runs for it.
# While it's dark the lamp is still there as a dark, colourless well, like the LED on a
# desktop board. Pass off_color= to pick the dark colour yourself.
#
# The table is read when the keyboard loads its plugins, so a change made in
# the app shows up the next time the keyboard opens.
COLORS = {
    "Green": "#35e06f",
    "Amber": "#ffb224",
    "Red": "#ff453a",
    "Blue": "#3b9dff",
    "White": "#f5f7ff",
}

def initial():
    return {"on": True, "color": "Green", "glow": True}

def settings(state):
    return section("keys.faces", [
        toggle("Caps lock light", state["on"], action="on"),
        segmented(list(COLORS.keys()), value=state["color"], key="color"),
        toggle("Glow", state["glow"], action="glow"),
    ], title="Caps Lock Light")

def on_action(action, value, state):
    if action in ("on", "glow"):
        state[action] = value
    return state

def key_lights(state):
    if not state["on"]:
        return {}
    color = COLORS.get(state["color"], COLORS["Green"])
    return {"shift": key_light(color, when="caps_lock", corner="top_right",
                               size=5, inset=5, glow=state["glow"])}
