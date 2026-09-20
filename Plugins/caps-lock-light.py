# ---
# name: Caps Lock Light
# icon: capslock
# summary: A little green lamp on shift that lights while caps lock is on
# version: 1.2
# author: Clink
# ---

# Drawing on a key, and reacting to the keyboard.
#
# key_art(state) returns a dict from key names to what's drawn on them: a list
# of shape(...)s, or art([...], animate=seconds) to ease between changes. Key
# names are the ones haptics uses: "shift", "delete", "space", "return",
# "globe", a letter like "a", "letters" for every letter, "keys" for anything.
#
# A shape is a "circle", "rect", "capsule", "line", "path", "text" or "icon".
# It sits at an anchor on the key ("top_right", "center", ...), moved right and
# down by x and y, in points (or in shares of the key with unit="key"). fill
# and stroke take "#rrggbb", "#rrggbbaa", "text" or "accent" (the theme's own
# colours), a color(value, opacity) or a gradient(...). shadow= takes one
# shadow(...) or a list, trim_from/trim_to draw part of an outline, and there
# is opacity, blur, rotation, corner and line_width.
#
# on_event(name, info, state) hears what happens on the keyboard: "shift"
# (info["state"] is "off", "on" or "locked"), "plane", "open", "close", "word",
# "language", "field", and, if events(state) asks for them, the busy ones:
# "key_down", "key_up", "key" and "tick". The keyboard asks key_art again after
# every event you hear, so change your state there and draw from it.
#
# Nothing here is special to a caps lock lamp. Copy it and draw something else.
COLORS = {
    "Green": "#35e06f",
    "Amber": "#ffb224",
    "Red": "#ff453a",
    "Blue": "#3b9dff",
    "White": "#f5f7ff",
}

SIZE = 5      # the lamp's diameter, in points
INSET = 5     # how far it sits from the key's top and right edges

def initial():
    return {"on": True, "color": "Green", "glow": True, "caps": False,
            "shift": False, "light_shift": False, "light_caps": True}

def settings(state):
    return section("keys.faces", [
        toggle("Caps lock light", state["on"], action="on"),
        toggle("Shift", state.get("light_shift", False), action="light_shift"),
        toggle("Caps Lock", state.get("light_caps", True), action="light_caps"),
        segmented(list(COLORS.keys()), value=state["color"], key="color"),
        toggle("Glow", state["glow"], action="glow"),
    ], title="Caps Lock Light")

def on_action(action, value, state):
    if action in ("on", "glow", "light_shift", "light_caps"):
        state[action] = value
    return state

def events(state):
    return ["open", "shift"]

def on_event(name, info, state):
    if name == "shift":
        state["caps"] = info["state"] == "locked"
        state["shift"] = info["state"] == "on"
    elif name == "open":
        current = context()["shift"]
        state["caps"] = current == "locked"
        state["shift"] = current == "on"
    return state

def mix(a, b, t):
    # Blend two "#rrggbb" colours, t of the way from a to b.
    out = "#"
    for i in (1, 3, 5):
        x = int(a[i:i + 2], 16)
        y = int(b[i:i + 2], 16)
        out += "%02x" % round(x + (y - x) * t)
    return out

def key_art(state):
    if not state["on"]:
        return {}
    # Missing preferences keep saved states from earlier versions caps-only.
    lit = (state.get("light_caps", True) and state["caps"]) or (state.get("light_shift", False) and state.get("shift", False))
    hue = COLORS.get(state["color"], COLORS["Green"])
    # The lamp's centre, measured from the key's top right corner.
    x = -(INSET + SIZE / 2)
    y = INSET + SIZE / 2

    glow = []
    if state["glow"]:
        glow = [shadow(color(hue, 0.75), radius=SIZE * 0.45),
                shadow(color(hue, 0.28), radius=SIZE * 1.1)]

    return {"shift": art([
        # The hole in the cap, darker at the top where the rim shades it.
        shape("circle", size=SIZE, fill=gradient("linear", ["#0000009e", "#0000006b"]), anchor="top_right", x=x, y=y),
        # Unlit, the diffuser is smoky plastic with no colour in it.
        shape("circle", size=SIZE - 1.2, fill=color("#ffffff", 0.1),
              opacity=0 if lit else 1, anchor="top_right", x=x, y=y),
        # Lit, it glows evenly and only a little hotter dead centre, the way
        # light comes through frosted plastic. No glossy highlight.
        shape("circle", size=SIZE - 1.2,
              fill=gradient("radial", [mix(hue, "#ffffff", 0.32), hue, mix(hue, "#000000", 0.18)],
                            stops=[0, 0.55, 1]),
              shadow=glow, opacity=1 if lit else 0, anchor="top_right", x=x, y=y),
        # The well's lower lip catching the light.
        shape("circle", size=SIZE, stroke=color("#ffffff", 0.22), line_width=0.4,
              trim_from=0.05, trim_to=0.45, anchor="top_right", x=x, y=y),
    ], animate=0.16)}
