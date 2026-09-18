# ---
# name: WPM Sparkline
# icon: waveform.path.ecg
# summary: A live graph of your typing speed, as a layout element
# version: 1.4
# author: Clink
# ---

# A sparkline of your typing speed, drawn on a key.
#
# This plugin has no settings of its own: it offers a layout element instead.
# Add it from Layout > Arrange > Element and pick "WPM sparkline". The plugin
# samples the live rate once a second and draws the last half minute of it.

POINTS = 30

def initial():
    return {"history": []}

def elements(state):
    return [element("sparkline", "WPM sparkline", icon="waveform.path.ecg", width=3)]

def on_open(state):
    # Each session draws its own line; yesterday's speed is not news.
    state["history"] = []
    return state

def on_tick(state):
    history = state["history"]
    history.append(stats()["wpm"])
    state["history"] = history[-POINTS:]
    return state

def draw(id, state):
    history = state["history"]
    rate = history[-1] if history else 0
    # A ceiling of at least 60 keeps a slow line looking slow instead of
    # filling the key, and a fifth of headroom above the fastest reading keeps
    # the line off the top edge, where it stops reading as a line at all.
    top = max(60, int(max(history) * 1.2) if history else 0)
    # Three monospaced digits, so the number keeps its width and the line
    # beside it never shifts as the rate crosses ten or a hundred.
    return hstack([
        # No fill: on a key the wash reads as a block of colour rather than as
        # a chart, and the line alone says the same thing.
        sparkline(history, min=0, max=top),
        text(f"{rate:>3}", size=12, weight="semibold", mono=True),
    ], spacing=5, align="center")
