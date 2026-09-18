# ---
# name: Heavy Space
# icon: iphone.radiowaves.left.and.right
# summary: A heavier haptic on space, and its own feel for return and delete
# version: 1.0
# author: Clink
# ---

# Haptics per key.
#
# haptics(state) returns a dict from key names to feels. A feel is a style
# ("soft", "light", "medium", "heavy", "rigid", or "off" for none) or
# feel(style, intensity=, sharpness=) with numbers from 0 to 1. Key names are
# the letter itself ("a"), "space", "delete", "return", "shift", "globe",
# "letters" for every letter, and "keys" for anything not named. Keys the
# plugin leaves out keep your own haptic from Sound & Haptics.
#
# The table is read when the keyboard opens and once a second after that, so
# a change here reaches the keyboard without reopening it.
def initial():
    return {"on": True, "space": 1.0}

def settings(state):
    return section("haptics.feel", [
        toggle("Heavier space bar", state["on"], action="on"),
        slider("Space strength", state["space"], min=0.5, max=1, step=0.05, key="space"),
    ], title="Heavy Space")

def on_action(action, value, state):
    if action == "on":
        state["on"] = value
    return state

def haptics(state):
    if not state["on"]:
        return {}
    return {
        "space": feel("heavy", intensity=state["space"]),
        "return": "rigid",
        "delete": feel(intensity=0.45, sharpness=0.9),
    }
