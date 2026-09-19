# ---
# name: Switch Volume
# icon: speaker.wave.2.fill
# summary: A knob in the top bar that sets how loud your key presses are
# version: 1.1
# author: Clink
# ---

# A volume knob for your key sounds, in the top bar.
#
# bar_items(state) offers things for Layout > Top bar. A bar_knob(...) with
# setting= turns one of your settings itself, and takes its range from it:
# drag up or right to turn the key press volume up, down or left to turn it
# down. Every step clicks at the new level, so you hear where it is, and it
# saves when you let go.
#
# on_action hears where the knob stopped. All the way down turns key sounds
# off for real, so the keyboard stops loading and playing them, not just
# playing them silently. Turning it back up switches them on again.
def bar_items(state):
    return [
        bar_knob("volume", "Switch volume", icon="speaker.wave.2.fill", setting="sound.volume"),
    ]

def on_action(action, value, state):
    if action != "volume":
        return state
    # Always written: the keyboard may already have flipped the switch for
    # this drag, and this is what saves it.
    set_setting("sound.enabled", value > 0)
    return state

def settings(state):
    return section("sound.keysounds", [
        text("Add the knob in Layout > Top bar, then drag it to set how loud each key press is."),
    ], title="Switch Volume")
