# ---
# name: Spacebar Graph
# icon: chart.xyaxis.line
# summary: A sparkline of your recent typing speed, drawn on the space bar
# version: 1.2
# author: Clink
# ---

# A WPM sparkline on space, entirely chosen and drawn by Python.
# Requires a Clink build with graph(). Enable this plugin and grant typing
# statistics. The original WPM plugins remain independent and unchanged.
#
# graph() returns ordinary shapes: use it on any key, combine it with text,
# change its bounds or paint, or feed it another numeric series. This plugin
# chooses only "space". It never changes key actions, captions or settings.
#
# It fills the whole space bar rather than a corner of it, and the line it
# hands over is smoothed twice: a trailing average over the readings, then a
# spline through them onto a fixed grid of points. Both are here rather than
# in the host, so any plugin can draw a graph that moves the same way.
#
# Requires a Clink build that clips key art to the cap, which is what lets the
# graph reach the edges and still follow the key's rounded corners.

# Readings kept, oldest first. Two dozen is about half a minute of ticks, and
# less than that while words are landing between them.
POINTS = 24
# Points on the drawn curve. Fixed, so consecutive paths have the same shape
# for the host to ease between, and under graph()'s 60-value ceiling.
DRAWN = 60
# Readings each drawn point is averaged over. A rate read once a second steps
# by whole words, and that staircase is the graph's own noise, not anyone's
# typing.
AVERAGE = 3

# Reuses the release catalog's reviewed WPM unit in every supported UI locale.
UNITS = {'en': 'WPM', 'de': 'WPM', 'es': 'PPM', 'et': 'WPM', 'fr': 'MPM', 'hu': 'SZÓ/P', 'it': 'PPM', 'ja': 'WPM', 'ko': 'WPM', 'ms': 'PPM', 'pt': 'PPM', 'ru': 'ЗН/МИН', 'zh-Hans': 'WPM'}

def initial():
    return {"history": [], "active": False}

def events(state):
    return ["open", "close", "tick", "word"]

def on_open(state):
    state["history"] = []
    state["active"] = True
    return state

def on_close(state):
    state["history"] = []
    state["active"] = False
    return state

def on_tick(state):
    return sample(state)

def on_word(word, state):
    # A word lands between ticks, and taking a reading there is what keeps the
    # line moving at typing speed rather than at one step a second. The busy
    # per-keystroke event stays unasked for: this hook already runs on a path
    # that does much more work than a list append.
    return sample(state)

def on_event(name, info, state):
    # The normal hooks collect data. Hearing these events asks the host to
    # refresh the artwork after those hooks, without collecting twice.
    return state

def sample(state):
    if state["active"]:
        history = state["history"]
        history.append(stats()["wpm"])
        state["history"] = history[-POINTS:]
    return state

def averaged(values):
    out = []
    for i in range(len(values)):
        start = i - AVERAGE + 1
        if start < 0:
            start = 0
        window = values[start:i + 1]
        out.append(sum(window) / len(window))
    return out

def curved(values, count):
    # Catmull-Rom through the readings: the line bends between them instead of
    # turning a corner at each one. Overshoot past the ends of the range is
    # graph()'s to clamp.
    n = len(values)
    last = count - 1
    out = []
    for i in range(count):
        position = i * (n - 1) / last
        k = int(position)
        if k > n - 2:
            k = n - 2
        t = position - k
        p0 = values[k - 1] if k > 0 else values[0]
        p1 = values[k]
        p2 = values[k + 1]
        p3 = values[k + 2] if k + 2 < n else values[n - 1]
        out.append(0.5 * (2 * p1 + (p2 - p0) * t
                          + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                          + (3 * p1 - 3 * p2 + p3 - p0) * t * t * t))
    return out

def key_art(state):
    if not state["active"]:
        return {}
    history = state["history"]
    rate = int(history[-1]) if history else 0
    top = max(60, max(history) * 1.2 if history else 0)
    locale = context()["locale"].replace("_", "-")
    language = "zh-Hans" if locale.startswith("zh") else locale.split("-")[0]
    unit = UNITS.get(language, "WPM")
    drawing = []
    if len(history) > 1:
        # The whole key. The host clips key art to the cap, so the wash follows
        # the rounded corners rather than squaring them off, and the baseline
        # can sit on the bottom edge.
        drawing = graph(curved(averaged(history), DRAWN), min=0, max=top, unit="key",
                        x=0, y=0, width=1, height=1,
                        stroke=color("text", 0.8), line_width=1.3,
                        # Strongest along the bottom, so the area under the
                        # line reads at any height the line sits at.
                        fill=gradient("linear", [color("text", 0.04), color("text", 0.2)],
                                      start=[0, 0], end=[0, 1]))
    # Pinned to the right: a box of its own width, aligned in it to the side
    # the anchor names, and monospaced digits. Placed by its centre with its
    # own width instead, the reading would slide sideways every time it gained
    # a digit.
    drawing.append(shape("text", unit="key", anchor="right", x=-0.23, y=-0.22,
                         width=0.38, height=0.22, text=f"{rate} {unit}",
                         font_size=9, weight="semibold", mono=True, fill="text"))
    # A second: the beat the tick runs on, so the curve is still travelling
    # when the next reading arrives and never sits still between them.
    return {"space": art(drawing, animate=1.0)}
