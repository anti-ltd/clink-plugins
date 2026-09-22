# ---
# name: Mood Ring
# icon: drop.halffull
# summary: The keys take on the colour of what you are writing
# version: 1.0
# author: Clink
# ---

# A mood ring for the keyboard.
#
# Every word you finish moves a running mood between cold and warm, and
# key_art washes that colour over the keys. Nothing is picked, nothing is
# saved, and nothing of yours is changed: the wash is artwork the plugin
# draws, so switching the plugin off puts the keyboard back exactly as it
# was. Your theme is never touched.
#
# That is why this does not offer themes(). A plugin theme is something you
# choose in Look > Themes, and driving one from here would mean rewriting
# your theme setting every few words and putting it back afterwards. Artwork
# costs nothing to undo, so artwork is what this uses.
#
# How it reads a word. WARM and COLD are ordinary word lists; a word in one
# of them nudges the mood, everything else leaves it alone. A word in NEGATE
# flips whichever word comes next ("not great" reads cold), and a word in
# LOUD doubles it ("really awful" reads colder than "awful"). The mood decays
# toward the middle on its own, so a paragraph that starts angry and ends
# calm finishes calm.
#
# The colour is mixed here rather than chosen from a list of five, so the
# drift is continuous: there is no step where the keyboard visibly repaints.
# art(..., animate=...) eases each change over the best part of a second,
# which turns a per-word jump into a slow bloom.

# How much of the old mood survives each word. Lower forgets faster.
DECAY = 0.86
# What one plain warm or cold word is worth before sensitivity is applied.
STEP = 0.30
# Strongest wash, at either end of the range. Key art draws over the legends,
# so this stays low enough to read the letters through.
MAX_TINT = 0.17
# The space bar gets a little more, because it is one big surface and reads
# as the mood indicator.
MAX_SPACE = 0.26
# Seconds the colour takes to travel to its new value.
EASE = 0.9

WARM = {
    "love", "loved", "lovely", "great", "good", "better", "best", "happy",
    "glad", "excited", "excellent", "wonderful", "brilliant", "beautiful",
    "perfect", "nice", "kind", "thanks", "thank", "grateful", "proud",
    "delighted", "pleased", "fun", "funny", "enjoy", "enjoyed", "enjoying",
    "win", "won", "winning", "congratulations", "congrats", "yes", "yay",
    "amazing", "awesome", "fantastic", "superb", "smooth", "easy", "clear",
    "calm", "safe", "warm", "bright", "hope", "hopeful", "lucky", "sweet",
    "cheers", "welcome", "well", "fine", "solid", "strong", "ready", "sure",
    "agree", "agreed", "helpful", "friend", "friends", "please", "sorted",
    "done", "finished", "works", "working", "worked", "fixed", "passed",
}

COLD = {
    "hate", "hated", "bad", "worse", "worst", "sad", "angry", "upset",
    "annoyed", "annoying", "terrible", "awful", "horrible", "rubbish",
    "broken", "breaks", "broke", "failed", "fails", "failing", "failure",
    "wrong", "error", "errors", "bug", "bugs", "crash", "crashed", "crashes",
    "stuck", "slow", "late", "lost", "lose", "losing", "miss", "missed",
    "sorry", "afraid", "worried", "worry", "scared", "tired", "exhausted",
    "sick", "hurts", "hurt", "pain", "painful", "hard", "difficult", "mess",
    "no", "nope", "cold", "dark", "dead", "stop", "stopped", "problem",
    "problems", "issue", "issues", "wait", "waiting", "still", "again",
    "confused", "confusing", "unclear", "impossible", "useless", "pointless",
}

NEGATE = {
    "not", "never", "no", "none", "nothing", "cant", "wont", "dont",
    "doesnt", "didnt", "isnt", "arent", "wasnt", "werent", "hardly",
    "barely", "without",
}

LOUD = {
    "very", "really", "so", "such", "extremely", "totally", "completely",
    "absolutely", "utterly", "incredibly", "deeply", "seriously", "properly",
}

# Cold end, middle, warm end. The wash is mixed between them.
CHILL = [70, 150, 255]
EVEN = [150, 160, 175]
BLAZE = [255, 110, 90]

DIGITS = "0123456789abcdef"


def initial():
    # mood runs -1 (cold) to 1 (warm); flip and loud carry over one word.
    return {"on": True, "mood": 0.0, "sensitivity": 1.0, "flip": False,
            "loud": 1.0, "space": True}


def settings(state):
    reading = describe(state["mood"])
    return section("themes.background", [
        toggle("Colour the keys by mood", state["on"], action="on"),
        text("Warm words warm the keys, cold words cool them. It reads what you type to do it, and writes nothing down.",
             size=12, color="gray"),
        slider(state["sensitivity"], min=0.3, max=2.0, step=0.1,
               label="Sensitivity", action="sensitivity"),
        toggle("Stronger on the space bar", state["space"], action="space"),
        divider(),
        text(f"Right now: {reading}", size=13, weight="medium"),
        button("Back to the middle", action="reset", icon="arrow.counterclockwise"),
    ], title="Mood Ring")


def describe(mood):
    if mood > 0.55:
        return "Warm"
    if mood > 0.18:
        return "Leaning warm"
    if mood < -0.55:
        return "Cold"
    if mood < -0.18:
        return "Leaning cold"
    return "Even"


def on_action(action, value, state):
    if action == "on":
        state["on"] = value
    elif action == "space":
        state["space"] = value
    elif action == "sensitivity":
        state["sensitivity"] = value
    elif action == "reset":
        state["mood"] = 0.0
        state["flip"] = False
        state["loud"] = 1.0
    return state


def events(state):
    # The mood moves on whole words, so "word" is the only busy event worth
    # asking for. Hearing it is also what refreshes the artwork after the
    # hook below has moved the colour.
    return ["word", "open"]


def on_event(name, info, state):
    # on_word does the reading. This hook exists so the events above are
    # heard at all, and so the wash is redrawn once they have been.
    return state


def on_open(state):
    # A fresh keyboard starts even rather than wherever the last message
    # left off. A mood that carried between apps would be a mood about
    # nothing.
    state["mood"] = 0.0
    state["flip"] = False
    state["loud"] = 1.0
    return state


def on_word(word, state):
    if not state["on"]:
        return state
    clean = letters_only(word)
    if clean == "":
        return state

    if clean in NEGATE:
        state["flip"] = True
        state["loud"] = 1.0
        return state
    if clean in LOUD:
        state["loud"] = 2.0
        return state

    score = 0.0
    if clean in WARM:
        score = STEP
    elif clean in COLD:
        score = -STEP

    if score != 0.0:
        score = score * state["loud"] * state["sensitivity"]
        if state["flip"]:
            # "not bad" is mild praise, not the opposite of awful, so a
            # flipped word lands softer than it would on its own.
            score = -score * 0.6
    # A word with no feeling in it still lets the mood settle: this is where
    # a paragraph of ordinary prose slowly comes back to the middle.
    state["mood"] = clamp(state["mood"] * DECAY + score, -1.0, 1.0)
    state["flip"] = False
    state["loud"] = 1.0
    return state


def letters_only(word):
    out = ""
    for ch in word.lower():
        if ch.isalpha():
            out = out + ch
    return out


def clamp(value, low, high):
    return max(low, min(high, value))


def mix(a, b, t):
    return [a[0] + (b[0] - a[0]) * t,
            a[1] + (b[1] - a[1]) * t,
            a[2] + (b[2] - a[2]) * t]


def hex2(value):
    n = int(clamp(value, 0, 255))
    return DIGITS[n // 16] + DIGITS[n % 16]


def hex_color(rgb, opacity):
    # #RRGGBBAA. Three-digit shorthand is not supported, and opacity has to
    # ride in the string here because a plain hex is what fill= wants.
    return ("#" + hex2(rgb[0]) + hex2(rgb[1]) + hex2(rgb[2])
            + hex2(clamp(opacity, 0.0, 1.0) * 255))


def wash(mood, strength):
    # Warm and cold are mixed from the middle outwards, so an even mood is a
    # colour nobody notices rather than an abrupt absence of one.
    if mood >= 0:
        rgb = mix(EVEN, BLAZE, mood)
    else:
        rgb = mix(EVEN, CHILL, -mood)
    return hex_color(rgb, abs(mood) * strength)


def key_art(state):
    if not state["on"]:
        return {}
    mood = state["mood"]
    if abs(mood) < 0.04:
        # Under a twentieth the wash is invisible anyway, and returning it
        # would keep the host easing artwork nobody can see.
        return {}
    faces = {"keys": art([
        shape("rect", unit="key", width=1, height=1, corner=5,
              fill=wash(mood, MAX_TINT)),
    ], animate=EASE)}
    if state["space"]:
        faces["space"] = art([
            shape("rect", unit="key", width=1, height=1, corner=5,
                  fill=wash(mood, MAX_SPACE)),
        ], animate=EASE)
    return faces
