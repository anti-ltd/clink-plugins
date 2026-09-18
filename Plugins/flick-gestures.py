# ---
# name: Flick Gestures
# icon: hand.draw
# summary: Flick to delete a word, type a space or pick a suggestion
# version: 2.0
# author: Clink
# ---

# Fleksy-style flicks on the letters, each with its own switch:
#   flick left      deletes the last word
#   flick right     types a space (autocorrect included, like the space bar)
#   flick up        takes the middle suggestion; up-left and up-right take
#                   the left and right ones, whatever the bar is showing
#
# The switches sit under Gestures > Swipe typing in the app. Swipe typing reads
# the same drags as words, so it is off while any switch is on and comes back
# the way it was when they are all off. Predictive Flick puts its own words on
# upward flicks, so it gets the same treatment while flick up is on.
#
# A flick whose switch is off does nothing here, and the keyboard then treats
# it as the ordinary keystroke it started as.

SWITCHES = ["left", "right", "up"]

def initial():
    return {"left": False, "right": False, "up": False,
            "swipe_before": False, "predictive_before": False}

def settings(state):
    ready(state)
    return section("gestures.swipe", [
        toggle("Flick left to delete a word", state["left"], action="left"),
        toggle("Flick right for a space", state["right"], action="right"),
        toggle("Flick up to pick a suggestion", state["up"], action="up"),
        text("Flick anywhere on the letters. Up picks the middle suggestion, up-left and up-right the ones either side. Swipe typing is off while any of these is on.", size=12, color="gray"),
    ], title="Flick Gestures")

def on_action(action, value, state):
    ready(state)
    if action not in SWITCHES or state[action] == value:
        return state
    was_on = any_on(state)
    state[action] = value
    if any_on(state) and not was_on:
        # Remember the person's own choice so the last switch off restores it.
        state["swipe_before"] = setting("gestures.swipe")
        set_setting("gestures.swipe", False)
        claim("gestures.swipe")
    elif was_on and not any_on(state):
        release("gestures.swipe")
        set_setting("gestures.swipe", state["swipe_before"])
    if action == "up":
        if value:
            state["predictive_before"] = setting("gestures.predictive_flick")
            set_setting("gestures.predictive_flick", False)
            claim("gestures.predictive_flick")
        else:
            release("gestures.predictive_flick")
            set_setting("gestures.predictive_flick", state["predictive_before"])
    return state

def on_swipe(direction, state):
    ready(state)
    if direction == "left" and state["left"]:
        delete_word()
    elif direction == "right" and state["right"]:
        # The space bar's own path, so the word before it still autocorrects.
        press("space")
    elif state["up"]:
        if direction == "up":
            pick_suggestion("center")
        elif direction == "up_left":
            pick_suggestion("left")
        elif direction == "up_right":
            pick_suggestion("right")
    return state

def any_on(state):
    return state["left"] or state["right"] or state["up"]

def ready(state):
    # State saved by 1.0, which had one switch for both flicks.
    if "left" not in state:
        on = state.get("on", False)
        state["left"] = on
        state["right"] = on
        state["up"] = False
        state["predictive_before"] = False
        state.setdefault("swipe_before", False)
