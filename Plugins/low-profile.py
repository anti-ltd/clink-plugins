# ---
# name: Low Profile
# icon: square.stack.3d.up
# summary: A low-profile mechanical key style for the theme editor
# version: 2.0
# author: Clink
# ---

# A key style for the theme editor.
#
# key_styles(state) hands the theme editor a list of key_style(...) entries.
# Each one is a set of finish choices laid over whatever theme is open: pick it
# under Design > Style > From plugins and only the fields it names change, so
# the theme keeps its colours. The theme holds on to the result with the
# plugin switched off. Edit the layers below to change the cap itself.
#
# The whole cap is drawn here, just like Typewriter: a shallow rectangular
# shell, a narrow bevel and a gently dished face. Colours follow the theme.
# The fixed foot stays on the keyboard while the cap and letter travel down.
def low_profile_cap():
    return cap(outline="rect", corner=5, travel=1.2, layers=[
        # A close contact shadow and the small foot underneath the shell.
        cap_layer("fill", "background*0.2@0.5", blur=0.8,
                  y=2.8, pressed_y=2.2, moves=False),
        cap_layer("fill", "face*0.38", inset=0.4, y=2.6, moves=False),

        # Shallow side walls. Their bottom stays put as the top drops.
        cap_layer("fill", gradient("linear", ["face*0.8", "face*0.48"]),
                  y=2, pressed_y=2.2),
        cap_layer("stroke", "black@0.22", width=0.5,
                  y=2, pressed_y=2.2),

        # The narrow bevel around the face, catching light at its top edge.
        cap_layer("fill", gradient("linear", ["face+0.28", "face", "face*0.72"],
                                   stops=[0, 0.3, 1])),
        cap_layer("stroke", "white@0.35", width=0.7, fade="top"),

        # A restrained dish, with enough reflected light on dark palettes.
        cap_layer("fill", gradient("linear", ["face*0.94", "face", "face+0.06"],
                                   stops=[0, 0.45, 1]), inset=1.3, when="pale"),
        cap_layer("fill", gradient("linear", ["face*0.82", "face", "face+0.08"],
                                   stops=[0, 0.45, 1]), inset=1.3, when="dark"),
        cap_layer("inner", "black@0.14", inset=1.3, width=0.6, blur=0.3, fade="top"),
        cap_layer("stroke", "white@0.12", inset=1.3, width=0.5, fade="bottom"),

        # Press feedback and latched keys such as caps lock.
        cap_layer("fill", "tint@0.22", inset=1.3, when="pressed"),
        cap_layer("fill", "tint@0.14", inset=1.3, when=["highlighted", "resting"]),
    ])


def key_styles(state):
    return [
        key_style("low-profile", "Low Profile", icon="keyboard",
                  cap=low_profile_cap(), shadow=0, outline=0),
    ]
