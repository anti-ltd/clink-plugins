# ---
# name: Spacebar Graph
# icon: chart.xyaxis.line
# version: 1.0
# author: Clink
# ---

# A WPM sparkline on space, entirely chosen and drawn by Python.
# Requires a Clink build with graph(). Enable this plugin and grant typing
# statistics. The original WPM plugins remain independent and unchanged.
#
# graph() returns ordinary shapes: use it on any key, combine it with text,
# change its bounds or paint, or feed it another numeric series. This plugin
# chooses only "space". It never changes key actions, captions or settings.

POINTS = 30

# Reuses the release catalog's reviewed WPM unit in every supported UI locale.
UNITS = {'en': 'WPM', 'de': 'WPM', 'es': 'PPM', 'et': 'WPM', 'fr': 'MPM', 'hu': 'SZÓ/P', 'it': 'PPM', 'ja': 'WPM', 'ko': 'WPM', 'ms': 'PPM', 'pt': 'PPM', 'ru': 'ЗН/МИН', 'zh-Hans': 'WPM'}

def initial():
    return {"history": [], "active": False}

def events(state):
    return ["open", "close", "tick"]

def on_open(state):
    state["history"] = []
    state["active"] = True
    return state

def on_close(state):
    state["history"] = []
    state["active"] = False
    return state

def on_tick(state):
    if state["active"]:
        state["history"].append(stats()["wpm"])
        state["history"] = state["history"][-POINTS:]
    return state

def on_event(name, info, state):
    # The normal hooks collect data. Hearing these events asks the host to
    # refresh the artwork after those hooks, without collecting twice.
    return state

def key_art(state):
    if not state["active"]:
        return {}
    history = state["history"]
    rate = int(history[-1]) if history else 0
    top = max(60, max(history) * 1.2 if history else 0)
    locale = context()["locale"].replace("_", "-")
    language = "zh-Hans" if locale.startswith("zh") else locale.split("-")[0]
    unit = UNITS.get(language, "WPM")
    drawing = graph(history, min=0, max=top, unit="key",
                    x=0.23, y=0.28, width=0.44, height=0.22,
                    stroke=color("text", 0.75), line_width=1.2,
                    fill=gradient("linear", [color("text", 0.16), color("text", 0)],
                                  start=[0, 0], end=[0, 1]))
    drawing.append(shape("text", unit="key", x=0.27, y=-0.22,
                         width=0.38, height=0.22, text=f"{rate} {unit}",
                         font_size=9, weight="semibold", fill="text"))
    return {"space": art(drawing, animate=0.35)}
