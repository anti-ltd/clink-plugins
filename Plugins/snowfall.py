# ---
# name: Snowfall
# icon: snowflake
# summary: Snow drifting behind the keys, with a puff from every key you press
# version: 1.0
# author: Clink
# ---

# An animated background for Look > Background.
#
# backgrounds(state) returns background(...) entries, each a stack of up to
# four particles(...) layers and up to eight "#rrggbb" colours. A layer's
# keywords, all optional:
#   shape       "dot", "glow", "streak", "ring" or "square"
#   count       how many are on screen at once (up to 120)
#   size        radius in points, and size_range for how much that varies
#   speed       points per second, in direction ("up", "down", "left",
#               "right" or "none" for any way) give or take spread degrees
#   gravity     pulls down (or up, when negative) over a particle's life
#   wobble      sideways sway in points
#   life        seconds each one lasts; they fade in and out
#   twinkle     0 to 1, how much they flicker
#   opacity     0 to 1
#   color       which colour to use, or -1 to mix them all
#   burst       how many fly out of a pressed key, at burst_speed
#
# Snowfall: flakes drifting down with a gentle sway, and a small puff of
# glow from every key you press.
def backgrounds(state):
    return [
        background("snowfall", "Snowfall", icon="snowflake", colors=["#ffffff", "#cfe8ff"], layers=[
            particles(shape="dot", count=70, size=2.2, size_range=0.6, speed=28,
                      direction="down", spread=12, wobble=10, life=9, opacity=0.85),
            particles(shape="glow", count=0, size=3, life=1, opacity=0.7,
                      burst=8, burst_speed=90),
        ]),
    ]
