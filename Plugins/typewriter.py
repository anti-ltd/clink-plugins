# ---
# name: Typewriter
# icon: keyboard.badge.ellipsis
# summary: Typewriter keys, a light and a dark theme, a typebar press and clacky haptics
# version: 3.1
# author: Clink
# ---

# An old typewriter, in four parts.
#
# key_styles(state) draws the key itself. A cap(...) is an outline and a stack
# of layers, painted bottom first, and the keyboard draws exactly what is
# listed here, so copying this file and changing the layers gives you your
# own key. The glass face and chrome ring follow the user's key dimensions
# and corner rounding, standing on a stem.
#
# Colours are written against the key they land on: "face" is the key's own
# colour, "text" its letter colour, "background" the keyboard behind it and
# "tint" the press colour. Add *0.8 to darken, +0.2 to lighten toward white,
# and @0.5 for opacity. A layer with when="pale" only draws on light keys and
# when="dark" on dark ones, which is how one cap suits ivory and black alike.
# gradient(...) is the same one key art uses: its colours top to bottom, with
# stops= placing them.
#
# popups(state) adds Typed Slip under Look > Popups: the letter you pressed,
# struck in ribbon ink on a slip of typing paper. Its body is a cap(...) too,
# painted the same way as the keys.
#
# themes(state) adds two themes to the Plugins tab of the theme gallery:
# Typewriter Ivory and Typewriter Noir, both with this key and the
# typewriter face for the letters.
#
# animations(state) adds Typebar under Look > Reactions > Geometry and Strike
# under Letters. haptics(state) makes the letters clack and gives return the
# thunk of a carriage coming back; its switch sits under Sound & Haptics.

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


# How wide the chrome ring is. The face and its glass sit inside it.
RING = 2.9


def typewriter_cap():
    return cap(outline="rect", travel=2.5, layers=[
        # The stem's shadow on the machine body. It stays put while the cap
        # drops, and pulls in under it when pressed.
        cap_layer("fill", "background*0.2@0.75", blur=1.8, y=5.8, pressed_y=2, moves=False),

        # The side of the ring, showing below the cap.
        cap_layer("fill", gradient("linear", ["#858585", "#333333", "#575757"], stops=[0, 0.7, 1]),
                  y=3.2, pressed_y=3.3),

        # The ring: bright sky over a dark horizon, then the ground light
        # coming back up, the way polished nickel reflects a room.
        cap_layer("fill", gradient("linear",
                                   ["#f7f7f7", "#d1d1d1", "#757575", "#4d4d4d", "#b3b3b3", "#e6e6e6"],
                                   stops=[0, 0.22, 0.46, 0.53, 0.78, 1])),
        cap_layer("stroke", "black@0.45", width=0.6),

        # The face, dished: in shadow under the top of the ring and catching
        # the light toward the bottom.
        cap_layer("fill", gradient("linear", ["face*0.8", "face", "face+0.18"], stops=[0, 0.42, 1]),
                  inset=RING, when="pale"),
        cap_layer("fill", gradient("linear", ["face*0.55", "face", "face+0.12"], stops=[0, 0.42, 1]),
                  inset=RING, when="dark"),
        cap_layer("inner", "black@0.35", width=1.1, blur=0.5, inset=RING, when="pale"),
        cap_layer("inner", "black@0.6", width=1.1, blur=0.5, inset=RING, when="dark"),

        # A pressed key, and a latched one like caps lock, take the tint.
        cap_layer("fill", "tint@0.24", inset=RING, when="pressed"),
        cap_layer("fill", "tint@0.16", inset=RING, when=["highlighted", "resting"]),

        # Glare on the glass: a soft sheet over the upper half and a bright
        # crescent tucked under the ring.
        cap_layer("fill", gradient("linear", ["white@0.55", "white@0.12", "white@0"], stops=[0, 0.4, 0.52]),
                  inset=RING + 0.8, when="pale"),
        cap_layer("fill", gradient("linear", ["white@0.26", "white@0.06", "white@0"], stops=[0, 0.4, 0.52]),
                  inset=RING + 0.8, when="dark"),
        cap_layer("stroke", "white@0.85", width=0.9, inset=RING + 0.7, fade="top", when="pale"),
        cap_layer("stroke", "white@0.5", width=0.9, inset=RING + 0.7, fade="top", when="dark"),
    ])


def keys():
    return key_style("typewriter", "Typewriter", icon="circle.circle",
                     cap=typewriter_cap(), shadow=0, outline=0)


def key_styles(state):
    return [keys()]


def paper_slip():
    return cap(outline="rect", corner=3, travel=0, layers=[
        # The slip lifts off the keys, so its shadow falls soft and low.
        cap_layer("fill", "black@0.32", blur=3, y=3.5),

        # The paper, warm and a touch darker toward the bottom. It is the same
        # paper whatever the theme, so the ink below is fixed too.
        cap_layer("fill", gradient("linear", ["#fcf8ee", "#f3ecda", "#e9dfc6"], stops=[0, 0.6, 1])),

        # A ruled line under the letter, and the red margin rule down the
        # left, drawn as gradients with hard stops.
        cap_layer("fill", gradient("linear", ["#8fa8c8@0", "#8fa8c8@0", "#8fa8c8@0.6",
                                              "#8fa8c8@0.6", "#8fa8c8@0", "#8fa8c8@0"],
                                   stops=[0, 0.8, 0.8, 0.83, 0.83, 1]), inset=3),
        cap_layer("fill", gradient("linear", ["accent@0", "accent@0", "accent@0.55",
                                              "accent@0.55", "accent@0", "accent@0"],
                                   stops=[0, 0.13, 0.13, 0.16, 0.16, 1],
                                   start=[0, 0.5], end=[1, 0.5])),

        # The paper's cut edge, and the light catching its top.
        cap_layer("stroke", "#b5a47c@0.8", width=0.8),
        cap_layer("stroke", "white@0.9", width=1, inset=0.8, fade="top"),
    ])


def popups(state):
    return [
        popup_style("slip", "Typed Slip", icon="doc.plaintext",
                    cap=paper_slip(), ink="#1b1916@0.94",
                    width=52, height=64, lift=46, font_size=34,
                    response=0.22, damping=0.72),
    ]


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


# A nickel bezel around a dark platen knob, with a turning ivory pointer.
# Normalized dimensions follow the top bar's available dial size. Clink turns
# the rotor natively during a drag; no Python work is needed per frame.
def bar_items(state):
    return [bar_knob("volume", "Typewriter", icon="speaker.wave.2.fill",
                    setting="sound.volume", art=art([
        shape("circle", unit="key", size=0.96,
              fill=gradient("linear", ["#f7f7f7", "#757575", "#4d4d4d", "#e6e6e6"],
                            stops=[0, 0.44, 0.55, 1]),
              stroke="#161514", line_width=0.6),
        shape("circle", unit="key", size=0.78,
              fill=gradient("linear", ["#57504a", "#262422", "#141312"])),
        shape("circle", unit="key", size=0.64, fill="#262422",
              stroke="#77716a", line_width=0.6),
    ]), rotor=art([
        shape("rect", unit="key", y=-0.23, width=0.07, height=0.24,
              corner=1, fill="#f3ecdb"),
        shape("circle", unit="key", size=0.12, fill="#b3b3b3"),
    ]))]
