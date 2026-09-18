# ---
# name: Bubble Popups
# icon: bubble.fill
# summary: A round popup that floats a little higher
# version: 1.0
# author: Clink
# ---

# A popup style for Look > Popups.
#
# popups(state) returns popup_style(...) entries. shape is "tile" (a rounded
# rectangle over the key), "round" (a circle, or a capsule when it's wider than
# tall) or "balloon" (the built-in balloon, with this style's spring and
# opacity). width, height, lift and font_size are in points; lift is how far
# the bubble's centre sits above the key.
#
# Bubble is a round popup that floats a little higher than the built-in one
# and springs in with a small overshoot.
def popups(state):
    return [
        popup_style("bubble", "Bubble", icon="bubble.fill",
                    shape="round", width=58, height=58, lift=44, font_size=32,
                    response=0.3, damping=0.6),
    ]
