# ---
# name: Low Profile Mod
# icon: slider.horizontal.3
# summary: An example that adjusts the built-in mechanical key style
# version: 1.0
# author: Clink
# ---

# This example modifies a built-in Swift style. For a cap drawn entirely
# in Python with cap(...) and cap_layer(...), see low-profile.py.
#
# Only the fields named here change when the style is applied, so the theme
# keeps its colours. Try changing the face inset, corner radius or lighting
# to see how the built-in mechanical cap responds.
def key_styles(state):
    return [
        key_style("low-profile-mod", "Low Profile Mod", icon="slider.horizontal.3",
                  material="3d", variant="mechanical",
                  inner_radius=18, face_inset=2, edges=True, raised=True,
                  light_angle=315),
    ]
