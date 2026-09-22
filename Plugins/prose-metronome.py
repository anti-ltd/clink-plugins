# ---
# name: Prose Metronome
# icon: metronome
# summary: A bar across the space key that fills as a sentence runs long
# version: 1.0
# author: Clink
# ---

# A metronome for sentence length.
#
# Set a target, and a thin bar along the bottom of the space key fills as the
# sentence goes on. Reach the target and it turns; run well past it and it
# grows a second bar above the first. You find out you are writing a
# paragraph-long sentence while you are still in it, which is the only time
# the information is any use.
#
# It counts committed words, not keystrokes, and a sentence ends the moment
# you type . ! ? or a new line. Everything is drawn as key art on "space",
# so it sits on top of whatever the space bar already says and gives nothing
# back to put right afterwards. It never claims the space bar caption, so it
# lives happily beside WPM Spacebar.
#
# The target has two homes. There is a slider on Keys > Space bar, and
# bar_items offers a knob for Layout > Top bar so you can move it mid-draft
# without leaving what you are writing. Both write the same number.
#
# Why the average is here: a target you set once and never look at is a
# rule, and rules about sentence length are usually wrong. The last few
# sentences are shown under the slider so you can set the target to the
# writing you are actually doing.

# Sentence lengths kept for the average, newest last.
HISTORY = 12
# How far past the target the bar turns and the overshoot appears, as a share
# of the target. A third over is where a sentence stops being long and starts
# being two sentences.
OVER_AT = 0.3
# Where the overshoot bar reaches full width: double the target.
OVERSHOOT_FULL = 1.0

TRACK_HEIGHT = 0.075
TRACK_INSET = 0.035
GAP = 0.03

# Under target, at target, and well past it.
CALM = "#8ea2b8"
REACHED = "#f0a33c"
OVER = "#ff5a6e"

ENDINGS = ".!?\n"


def initial():
    return {"on": True, "target": 18, "words": 0, "called": False,
            "history": [], "nudge": False}


def settings(state):
    return section("keys.spacebar", [
        toggle("Show sentence length on the space bar", state["on"], action="on"),
        slider(state["target"], min=6, max=45, step=1,
               label=f"Target: {int(state['target'])} words", action="target"),
        text(recent(state), size=12, color="gray"),
        divider(),
        toggle("Say something when I run over", state["nudge"], action="nudge"),
        text("A short banner, once per sentence. Off by default, because a keyboard that talks back while you write is its own kind of interruption.",
             size=12, color="gray"),
    ], title="Prose Metronome")


def recent(state):
    history = state["history"]
    if not history:
        return "Finish a few sentences and their lengths show up here."
    total = 0
    for length in history:
        total = total + length
    average = total / len(history)
    recent_list = []
    for length in history[-6:]:
        recent_list.append(str(length))
    return f"Last few: {', '.join(recent_list)} — averaging {round(average)} words."


def on_action(action, value, state):
    if action == "on":
        state["on"] = value
    elif action == "nudge":
        state["nudge"] = value
    elif action == "target":
        state["target"] = int(value)
    return state


def bar_items(state):
    return [
        bar_knob("target", "Sentence target", icon="metronome",
                 min=6, max=45, step=1, value=state["target"]),
    ]


def events(state):
    # "key" is a busy event and has to be asked for by name. It is worth it:
    # the sentence ends on a punctuation mark, and hearing the keystroke is
    # what redraws the bar at the moment it empties rather than a word later.
    return ["word", "key", "open", "close"]


def on_event(name, info, state):
    # The counting is done by on_word and on_key. Hearing the same events
    # here is what asks the host to redraw the artwork afterwards.
    return state


def on_open(state):
    state["words"] = 0
    state["called"] = False
    return state


def on_word(word, state):
    if state["on"]:
        state["words"] = state["words"] + 1
        if state["nudge"] and not state["called"] and over(state) >= OVER_AT:
            state["called"] = True
            banner(f"{state['words']} words. Somewhere here a full stop would help.")
    return state


def on_key(text_typed, state):
    if not state["on"]:
        return state
    for ch in text_typed:
        if ch in ENDINGS:
            state = finish(state)
    return state


# There is deliberately no on_backspace. It says a character went away, not a
# word, so decrementing on it would walk the count down every time a typo is
# fixed mid-word. A count that is occasionally one high after heavy editing is
# the better of the two wrong answers.


def finish(state):
    if state["words"] > 0:
        history = state["history"]
        history.append(state["words"])
        state["history"] = history[-HISTORY:]
    state["words"] = 0
    state["called"] = False
    return state


def over(state):
    # How far past the target this sentence is, as a share of the target.
    target = max(1, int(state["target"]))
    return (state["words"] - target) / target


def track(fraction, paint, lift):
    # anchor="bottom_left" puts the origin on the bottom left corner, and x/y
    # place the shape's CENTRE, so a bar that grows rightwards from that
    # corner sits at half its own width. y counts downward, so lifting it off
    # the bottom edge is negative.
    return shape("rect", unit="key", anchor="bottom_left",
                 x=fraction / 2, y=-(TRACK_INSET + TRACK_HEIGHT / 2 + lift),
                 width=fraction, height=TRACK_HEIGHT, corner=1.5, fill=paint)


def key_art(state):
    if not state["on"]:
        return {}
    target = max(1, int(state["target"]))
    words = state["words"]
    if words == 0:
        return {}

    filled = min(1.0, words / target)
    if words >= target:
        paint = OVER if over(state) >= OVER_AT else REACHED
    else:
        paint = CALM

    shapes = [
        # The track. Always the full width, so the bar reads as a share of
        # something rather than as a line that happens to be that long.
        track(1.0, color("text", 0.10), 0),
        track(filled, paint, 0),
    ]
    # Past the target the first bar has nowhere left to go, so the overshoot
    # gets a shorter bar of its own above it.
    spill = over(state)
    if spill > OVER_AT:
        # Measured from where the overshoot starts rather than from the target,
        # so the second bar grows out of nothing instead of appearing a third
        # of the way along.
        grown = (spill - OVER_AT) / (OVERSHOOT_FULL - OVER_AT)
        shapes.append(track(min(1.0, grown), OVER, TRACK_HEIGHT + GAP))
    # Half a second: fast enough to land with the word, slow enough that the
    # bar is seen travelling rather than found in a new place.
    return {"space": art(shapes, animate=0.5)}
