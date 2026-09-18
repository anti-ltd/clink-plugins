# ---
# name: Typewriter
# icon: keyboard.badge.ellipsis
# summary: Typewriter keys, a light and a dark theme, a typebar press and clacky haptics
# version: 2.0
# author: Clink
# ---

# An old typewriter, in four parts.
#
# themes(state) adds two themes to the Plugins tab of the theme gallery:
# Typewriter Ivory, cream keys on a tan body, and Typewriter Noir, black glass
# keys on black enamel. Both use the typewriter key finish and the
# typewriter face for the letters.
#
# key_styles(state) offers the same key finish on its own, for any theme,
# under Design > Style > From plugins. The keys become round glass caps in a
# chrome ring, standing on stems, and the wide keys become bars.
#
# animations(state) adds Typebar under Look > Reactions > Geometry, a key that
# goes a long way down and comes back stiff, and Strike under Letters, the
# letter jumping up at the paper.
#
# haptics(state) makes the letters clack, and gives return the thunk of a
# carriage coming back. Its switch sits under Sound & Haptics.

def initial():
    return {"on": True}


def settings(state):
    return section("haptics.feel", [
        toggle("Typewriter haptics", state["on"], action="on"),
    ], title="Typewriter")


def on_action(action, value, state):
    if action == "on":
        state["on"] = value
    return state


def keys():
    return key_style("typewriter", "Typewriter", icon="circle.circle",
                     material="typewriter", shadow=0, outline=0)


def themes(state):
    return [
        theme("ivory", "Typewriter Ivory", icon="sun.max",
              background="#dcd2ba", background_bottom="#c9bea4",
              keys="#f3ecdb", key_text="#2a2521",
              special="#3b3531", special_text="#f3ecdb",
              accent="#b3261e",
              font="typewriter", weight="semibold",
              style=keys()),
        theme("noir", "Typewriter Noir", icon="moon",
              dark=True,
              background="#262422", background_bottom="#161514",
              keys="#141312", key_text="#f1e9d6",
              special="#2d2a27", special_text="#f1e9d6",
              accent="#c0392b",
              font="typewriter", weight="semibold",
              style=keys()),
    ]


def key_styles(state):
    return [keys()]


def animations(state):
    return [
        press_animation("typebar", "Typebar", icon="arrow.down.to.line",
                        scale_x=0.97, scale_y=0.9, y=5, response=0.12, damping=0.9),
        letter_animation("strike", "Strike", icon="arrow.up.to.line",
                         y=-6, scale=1.08, anchor="bottom"),
    ]


def haptics(state):
    if not state["on"]:
        return {}
    return {
        "letters": feel("rigid", intensity=0.8, sharpness=1),
        "space": feel("medium", intensity=0.6, sharpness=0.4),
        "return": feel("heavy", intensity=1, sharpness=0.2),
        "delete": feel("rigid", intensity=0.5, sharpness=0.8),
    }
