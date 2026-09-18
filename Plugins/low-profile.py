# ---
# name: Low Profile
# icon: square.stack.3d.up
# summary: A low-profile mechanical key style for the theme editor
# version: 1.0
# author: Clink
# ---

# A key style for the theme editor.
#
# key_styles(state) hands the theme editor a list of key_style(...) entries.
# Each one is a set of finish choices laid over whatever theme is open: pick it
# under Design > Style > From plugins and only the fields it names change, so
# the theme keeps its colours. The theme holds on to the result with the
# plugin switched off, and every part of it stays editable.
#
# Low Profile is the 3D mechanical cap pressed flat: a tight inner face, sharp
# side walls and a small foot, the way a low-profile switch keyboard looks.
def key_styles(state):
    return [
        key_style("low-profile", "Low Profile", icon="keyboard",
                  material="3d", variant="mechanical",
                  inner_radius=18, face_inset=2, edges=True, raised=True,
                  light_angle=315),
    ]
