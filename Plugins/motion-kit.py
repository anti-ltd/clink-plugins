# ---
# name: Motion Kit
# icon: wand.and.rays
# summary: An entrance, a key press, a letter bounce and a page switch
# version: 1.0
# author: Clink
# ---

# One of each animation a plugin can offer.
#
# animations(state) returns any mix of:
#   entrance(...)          how the keyboard arrives. Each number is where it
#                          starts (opacity, x, y, scale, tilt, spin), and it
#                          springs to rest with response and damping.
#   press_animation(...)   the shape a held key takes: scale (or scale_x and
#                          scale_y), x, y and rotation, all at full press.
#   letter_animation(...)  the one-shot a letter plays on each tap, on top of
#                          its key: the same numbers, at the peak of the kick.
#   transition(...)        the switch between letters, 123 and #+=: how far
#                          the old keys travel (x and y as a share of the
#                          keyboard), scale, tilt and whether they fade.
#
# They show up under From plugins next to the built-in choices on the Look
# page: Entrance, Reactions > Geometry, Reactions > Letters, and Transition.
def animations(state):
    return [
        entrance("swoop", "Swoop", icon="arrow.up.forward",
                 y=90, scale=0.94, tilt=-20, response=0.5, damping=0.72),
        press_animation("dip", "Dip", icon="arrow.down.to.line",
                        scale=0.93, y=2, response=0.18, damping=0.7),
        letter_animation("bounce", "Bounce", icon="arrow.up.and.down",
                         y=-7, scale=1.12, anchor="bottom"),
        transition("glide", "Glide", icon="rectangle.2.swap",
                   x=0.3, scale=0.96),
    ]
