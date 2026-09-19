# ---
# name: Press Spark
# icon: sparkle
# summary: A ring in the theme's accent colour around whichever key is down
# version: 1.0
# author: Clink
# ---

# Reacting to key presses.
#
# "key_down" and "key_up" are busy events: they run this script on every
# press, so on_event only gets them because events(state) asks. info["key"] is
# the key's name, the same one key_art uses, so the key that went down is the
# key that gets drawn on.
#
# The ring is sized in shares of the key (unit="key"), so it fits the space
# bar as well as a letter, and it is stroked in "accent", so it follows
# whatever theme it lands on. See Caps Lock Light for the rest of shape().
def initial():
    return {"on": True, "down": ""}

def settings(state):
    return section("keys.faces", [
        toggle("Ring the pressed key", state["on"], action="on"),
    ], title="Press Spark")

def on_action(action, value, state):
    if action == "on":
        state["on"] = value
    return state

def events(state):
    return ["key_down", "key_up", "close"]

def on_event(name, info, state):
    if name == "key_down":
        state["down"] = info["key"]
    elif name == "close" or info["key"] == state["down"]:
        state["down"] = ""
    return state

def key_art(state):
    if not state["on"] or state["down"] == "":
        return {}
    return {state["down"]: [
        shape("rect", unit="key", width=0.86, height=0.82, corner=6,
              stroke="accent", line_width=1.5,
              shadow=shadow(color("accent", 0.6), radius=4)),
    ]}
