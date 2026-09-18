# ---
# name: Light Show
# icon: light.max
# summary: Two lighting effects for the Effects page
# version: 1.0
# author: Clink
# ---

# Two lighting effects for the Effects page.
#
# effects(state) hands the Effects page a list of light_effect(...) entries,
# each a stack of light_layer(...)s that apply top to bottom. Pick one under
# Effects > From plugins. Hold it there and choose Duplicate to get a copy you
# can change in the effect editor.
#
# While one of these is running and the keyboard is up, effects(state) runs
# again about once a second. Tempo uses that: its wave keeps pace with your
# typing, slow when you pause and quick when you get going.

def effects(state):
    # Rounded so the effect only changes when the pace really does.
    tempo = round(0.3 + min(stats()["wpm"], 120) / 40, 1)
    return [
        light_effect("aurora", "Aurora", icon="sparkles",
                     colors=["#00e5a0", "#00b3ff", "#8a5cff"], layers=[
            light_layer("solid", low=0.2, high=0.2),
            light_layer("wave", moves="both", speed=0.5, size=1.5, high=0.6),
            light_layer("twinkle", speed=0.8, size=1.5, high=0.45),
        ]),
        light_effect("tempo", "Tempo", icon="metronome",
                     colors=["#ff3d7f", "#ffb000"], layers=[
            light_layer("wave", moves="both", speed=tempo, direction="right", low=0.15),
        ]),
    ]

def settings(state):
    return text("Pick Aurora or Tempo under Effects > From plugins. "
                "Tempo's wave speeds up as you type faster.", size=13, color="gray")
