# ---
# name: Haptic Strength
# icon: hand.tap.fill
# summary: A knob in the top bar that sets how strong your key presses feel
# version: 1.0
# author: Clink
# ---

# A haptic knob for the top bar, the feel counterpart of Switch Volume.
#
# bar_items(state) offers things for Layout > Top bar. A bar_knob(...) with
# setting= turns one of your settings itself and takes its range from it:
# drag up or right for a stronger tap, down or left for a lighter one. Every
# step buzzes at the new strength, so you feel where it is before you let go,
# and it saves when you do.
#
# on_action hears where the knob stopped. All the way down switches key
# haptics off for real, the way the volume knob switches sounds off, and
# turning it back up switches them on again. How sharp the tap is stays where
# you set it in Sound & Haptics; this knob is only how hard it hits.
def bar_items(state):
    return [
        bar_knob("strength", "Haptic strength", icon="hand.tap.fill", setting="haptics.intensity"),
    ]

def on_action(action, value, state):
    if action != "strength":
        return state
    # Always written: the keyboard may already have flipped the switch for
    # this drag, and this is what saves it.
    set_setting("haptics.enabled", value > 0)
    return state

def settings(state):
    return section("haptics.feel", [
        text("Add the knob in Layout > Top bar, then drag it to set how strong each key press feels. Turn it all the way down to switch haptics off."),
    ], title="Haptic Strength")
