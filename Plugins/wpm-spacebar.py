# ---
# name: WPM Spacebar
# icon: speedometer
# summary: Show your typing speed on the space bar
# version: 1.3
# author: Clink
# ---

# Shows your live typing speed on the space bar.
#
# The switch appears under Keys > Space bar in the app. While it is on, the
# plugin owns the space bar caption and keeps it current three ways: on_key
# while you type, on_word as each word lands, and on_tick once a second so the
# number still falls back to zero after you stop.

def initial():
    return {"on": False}

def settings(state):
    return section("keys.spacebar", [
        toggle("Show typing speed", state["on"], action="toggle"),
        text("Replaces the space bar text with your words per minute while you type.", size=12, color="gray"),
    ], title="WPM Spacebar")

def on_action(action, value, state):
    if action == "toggle":
        state["on"] = value
        if value:
            claim("spacebar.text")
            show(state)
        else:
            release("spacebar.text")
            space_text(None)
    return state

def on_open(state):
    show(state)
    return state

def on_key(key, state):
    # The rate moves with every character, so the caption should too. This
    # hook stays two lines for that reason: it runs on every keystroke.
    show(state)
    return state

def on_word(word, state):
    show(state)
    return state

def on_tick(state):
    show(state)
    return state

def show(state):
    if state["on"]:
        space_text(f"{stats()['wpm']} wpm")
