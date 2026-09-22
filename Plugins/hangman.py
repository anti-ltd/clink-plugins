# ---
# name: Hangman
# icon: gamecontroller
# summary: Hangman on the space bar: the letter keys are your guesses
# version: 1.0
# author: Clink
# ---

# A game drawn on the keys.
#
# Nothing here is a game feature in Clink. The script keeps the word, the
# guesses and the misses in its own state, draws the board with key_art, and
# takes the letters out of the field again with backspace() so a guess types
# nothing. The keyboard supplies shapes, events and a caption; it knows
# nothing about hangman.
#
# How a round runs:
#   type "hangman" anywhere        deals a word (the seven letters come back out)
#   a letter key                   a guess, not a keystroke
#   space                          the next word, once a round is over
#   delete                         leave the game
#
# The board lives on the space bar: the gallows at the left, the word in the
# caption, a dot for every life left at the right. A correct letter washes
# its own key green, a wrong one red, and the figure gains a part per miss.
#
# The word is the caption rather than another drawn shape because the caption
# is already centred on that key and already themed, and because an empty
# caption hands the key back to the person's own text, which would then read
# under the board.
import random

LETTERS = "abcdefghijklmnopqrstuvwxyz"
TRIGGER = "hangman"
LIVES = 6

GREEN = "#35e06f"
RED = "#ff453a"

WORDS = {
    "Easy": [
        "apple", "bread", "chair", "cloud", "dance", "dream", "drive", "field",
        "flame", "ghost", "green", "heart", "honey", "lemon", "light", "mango",
        "money", "mouse", "music", "night", "ocean", "paper", "party", "piano",
        "pilot", "plant", "river", "robot", "sheep", "shore", "smile", "snake",
        "sound", "stone", "storm", "sugar", "table", "tiger", "train", "water",
    ],
    "Medium": [
        "anchor", "arcade", "auburn", "ballot", "basket", "beacon", "branch",
        "bridge", "candle", "canyon", "cinema", "circus", "clover", "compass",
        "copper", "cradle", "crimson", "custard", "dragon", "eclipse", "engine",
        "feather", "fossil", "garden", "granite", "harbour", "helmet", "island",
        "jungle", "kitten", "lantern", "library", "magnet", "marble", "meadow",
        "mirror", "orchard", "pebble", "pepper", "picnic", "pocket", "puzzle",
        "rocket", "silver", "summit", "thread", "violet", "walnut", "whisper",
        "window",
    ],
    "Hard": [
        "accordion", "albatross", "amplifier", "avalanche", "blueprint",
        "butterfly", "cathedral", "chandelier", "chocolate", "clockwork",
        "crocodile", "dandelion", "dartboard", "dinosaur", "fireworks",
        "flamingo", "gemstone", "gramophone", "harmonica", "helicopter",
        "hurricane", "invention", "jellyfish", "kaleidoscope", "landscape",
        "lighthouse", "manuscript", "marmalade", "mechanism", "microscope",
        "moonlight", "nightfall", "orchestra", "paperclip", "periscope",
        "porcupine", "pineapple", "saxophone", "submarine", "telescope",
        "thunderbolt", "trampoline", "turquoise", "typewriter", "umbrella",
        "volcano", "waterfall", "whirlwind", "windmill", "xylophone",
    ],
}

# The gallows is drawn in its own little box, in points from the left end of
# the space bar, so it keeps its shape whatever the key is doing: a share of
# the space bar would stretch it flat.
BOX_X = 21.0
BOX_W = 30.0
BOX_H = 38.0


def initial():
    return {"on": True, "level": "Medium", "trigger": True, "playing": False,
            "word": "", "found": "", "misses": "", "over": "", "tail": ""}


def settings(state):
    return section("keys.spacebar", [
        toggle("Hangman", state["on"], action="on"),
        segmented(["Easy", "Medium", "Hard"], value=state["level"], key="level"),
        toggle("Type hangman to deal", state["trigger"], action="trigger"),
        text("Type hangman anywhere to deal a word, or add the Hangman button "
             "from Layout > Top bar and tap it. While a round is running the "
             "letter keys are guesses, not typing: the space bar shows the word "
             "and the gallows, space deals the next word and delete leaves. "
             "Switched off, the plugin hears nothing you type.",
             size=13, color="gray"),
    ], title="Hangman")


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
        else:
            state = deal(state)
    return state


def bar_items(state):
    return [bar_button("play", "Hangman", icon="gamecontroller", title="Hangman")]


def events(state):
    # Read once when the plugins load, so this is the real off switch: with
    # Hangman off the script is never called on a keystroke at all, rather
    # than being called and returning.
    if not state["on"]:
        return []
    return ["key", "backspace", "open", "close", "field"]


def on_event(name, info, state):
    if not state["on"]:
        return state
    if name == "key":
        return typed(info["text"], state)
    if not state["playing"]:
        return state
    # A round belongs to the field it started in, and delete is the way out.
    # Neither can be caught before it happens, so both end the game rather
    # than leaving it swallowing letters somewhere else.
    if name in ("backspace", "open", "close", "field"):
        return stop(state)
    return state


def typed(t, state):
    if not state["playing"]:
        return watching(t, state)
    if state["over"] != "":
        # The round is finished: space deals again, and anything else is
        # somebody typing, so it leaves the game and keeps its keystroke.
        if t != " ":
            return stop(state)
        backspace(len(t))
        return deal(state)
    # Nothing typed during a round reaches the field: the key is pressed, the
    # sound and the popup happen, and the letter comes straight back out.
    if len(t) > 0:
        backspace(len(t))
    ch = t.lower()
    if len(ch) == 1 and ch in LETTERS:
        state = guess(ch, state)
        space_text(board(state))
    return state


def watching(t, state):
    """Wait for the word that deals a round, one letter at a time."""
    if not state["trigger"] or len(t) != 1 or t.lower() not in LETTERS:
        state["tail"] = ""
        return state
    tail = (state["tail"] + t.lower())[-len(TRIGGER):]
    state["tail"] = tail
    if tail != TRIGGER:
        return state
    backspace(len(TRIGGER))
    return deal(state)


def deal(state):
    words = WORDS[state["level"]] if state["level"] in WORDS else WORDS["Medium"]
    state["word"] = random.choice(words)
    state["found"] = ""
    state["misses"] = ""
    state["over"] = ""
    state["tail"] = ""
    state["playing"] = True
    space_text(board(state))
    return state


def stop(state):
    state["playing"] = False
    state["tail"] = ""
    space_text(None)
    return state


def guess(ch, state):
    if ch in state["found"] or ch in state["misses"]:
        return state
    if ch in state["word"]:
        state["found"] = state["found"] + ch
        if solved(state):
            state["over"] = "won"
            banner("Solved: " + state["word"].upper())
    else:
        state["misses"] = state["misses"] + ch
        if len(state["misses"]) >= LIVES:
            state["over"] = "lost"
            banner("It was " + state["word"].upper())
    return state


def solved(state):
    for ch in state["word"]:
        if ch not in state["found"]:
            return False
    return True


def key_art(state):
    if not state["on"] or not state["playing"]:
        return {}
    ink = color("text", 0.75)
    if state["over"] == "lost":
        ink = color(RED, 0.9)
    shapes = [gallows(color("text", 0.5))]
    shapes = shapes + figure(len(state["misses"]), ink)
    shapes = shapes + lives(LIVES - len(state["misses"]))
    out = {"space": art(shapes, animate=0.22)}
    for ch in state["found"]:
        out[ch] = [wash(GREEN)]
    for ch in state["misses"]:
        out[ch] = [wash(RED)]
    return out


def lives(left):
    """A dot per life at the right end, counting in from the edge. Drawn rather
    than written: a shape is placed by its centre, so a caption of hearts that
    long would hang off the key and be clipped to the cap."""
    out = []
    for i in range(left):
        out.append(shape("circle", anchor="right", unit="pt",
                         x=-(8 + 7 * i), y=0, size=4.5, fill=color(RED, 0.85)))
    return out


def board(state):
    """The word for the caption: what has been found, blanks for the rest, and
    the whole of it once the round is over."""
    shown = []
    for ch in state["word"]:
        if ch in state["found"] or state["over"] != "":
            shown.append(ch.upper())
        else:
            shown.append("_")
    # A long word is spelled tight: the caption is framed to the key and
    # shrinks to fit, and a spaced-out twelve letters would shrink into the
    # gallows and the lives.
    line = " ".join(shown) if len(shown) <= 8 else "".join(shown)
    if state["over"] == "won":
        return line + "  ✓"
    if state["over"] == "lost":
        return line + "  ✗"
    return line


def wash(paint):
    return shape("rect", anchor="center", unit="key", width=1.04, height=1.04,
                 corner=8, fill=color(paint, 0.32))


def gallows(paint):
    """Base, post, beam and rope as one stroke: the run back along the base
    draws over itself, which costs nothing and saves three shapes."""
    return shape("path", anchor="left", unit="pt", x=BOX_X, y=0,
                 width=BOX_W, height=BOX_H, line_width=1.8, stroke=paint,
                 points=[[0.00, 1.0], [0.36, 1.0], [0.14, 1.0], [0.14, 0.02],
                         [0.62, 0.02], [0.62, 0.16]])


def figure(parts, paint):
    """Head, body, two arms and two legs, one per miss."""
    out = []
    if parts >= 1:
        out.append(shape("circle", anchor="left", unit="pt",
                         x=at_x(0.62), y=at_y(0.26), size=7.5,
                         stroke=paint, line_width=1.6))
    # Arms and legs hang, they don't stick out: a body on a rope is limp, and
    # the jumping-jack version reads as an arrow at this size.
    limbs = [[0.62, 0.36, 0.62, 0.68], [0.62, 0.41, 0.45, 0.62],
             [0.62, 0.41, 0.79, 0.62], [0.62, 0.68, 0.51, 0.97],
             [0.62, 0.68, 0.73, 0.97]]
    for i in range(min(parts - 1, len(limbs))):
        out.append(limb(limbs[i][0], limbs[i][1], limbs[i][2], limbs[i][3], paint))
    return out


# A shape is drawn inside a box of its own width and height, and a box with no
# thickness is not drawn at all: the body, being straight up and down, is
# exactly that. So every limb gets a box at least this wide, with the line
# down the middle of the side that has no length of its own.
THIN = 1.0


def limb(u1, v1, u2, v2, paint):
    x1 = at_x(u1)
    y1 = at_y(v1)
    x2 = at_x(u2)
    y2 = at_y(v2)
    px = 0.5 if abs(x2 - x1) < THIN else (0.0 if x1 < x2 else 1.0)
    py = 0.5 if abs(y2 - y1) < THIN else (0.0 if y1 < y2 else 1.0)
    return shape("line", anchor="left", unit="pt",
                 x=(x1 + x2) / 2, y=(y1 + y2) / 2,
                 width=max(abs(x2 - x1), THIN), height=max(abs(y2 - y1), THIN),
                 points=[[px, py], [1.0 - px, 1.0 - py]],
                 stroke=paint, line_width=1.8)


def at_x(u):
    return BOX_X + (u - 0.5) * BOX_W


def at_y(v):
    return (v - 0.5) * BOX_H
