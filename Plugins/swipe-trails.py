# ---
# name: Swipe Trails
# icon: scribble.variable
# summary: Six trails for swipe typing, from a candy ribbon to a line of hearts
# version: 1.0
# author: Clink
# ---

# Swipe trails for Gestures > Swipe typing, listed under From plugins.
#
# trails(state) returns trail(...) entries. Each is a stack of up to four
# layers, painted bottom to top, and up to eight colours. A colour is
# "#rrggbb" or "accent" for the theme's own accent. With no colours at all
# the whole trail is drawn in the accent.
#
# Widths and sizes are in thicknesses: 1 is the Thickness the person set
# under Edit, so their thickness, taper and "trail the finger" still apply.
#
# trail_line(...), a line along the glide:
#   width         thicknesses wide, and tail_width for the share of that
#                 left at the oldest end (0.2 tapers to a fifth)
#   opacity       0 to 1, and tail_opacity for the oldest end
#   color         which colour, or -1 to run them all along the glide
#   band          points of glide for one run through the colours; 0
#                 stretches them over the whole glide
#   flow          runs through the colours per second, toward the finger
#   dash, gap     a dashed line, both in thicknesses
#   glow          a halo, in thicknesses of blur
#
# trail_stamps(shape, ...), shapes set down along the glide:
#   shape         "dot", "ring", "square", "diamond", "star", "spark", "heart"
#   size          radius in thicknesses; size_range varies it, tail_size
#                 is the share left at the oldest end
#   spacing       points of glide between one and the next
#   scatter       how far off the path one may land, in points
#   spin          degrees one may be turned either way
#   twinkle       0 to 1, how much they flicker
#   opacity, tail_opacity, color, glow    as for a line
#
# trail_head(shape, ...), one shape under the finger:
#   size, opacity, color, glow    as above (-1 takes the newest colour)
#   pulse         0 to 1, how much it breathes
def trails(state):
    return [
        # A wide pastel band that keeps flowing toward the finger.
        trail("ribbon", "Candy Ribbon", icon="wand.and.rays",
              colors=["#ff6fb1", "#ffd166", "#7be0c3", "#6fb6ff", "#c58bff"], layers=[
            trail_line(width=1.7, tail_width=0.35, band=260, flow=0.35, opacity=0.95),
            trail_line(width=0.3, color=1, opacity=0.35),
        ]),

        # A faint thread with sparks twinkling around it.
        trail("stardust", "Stardust", icon="sparkles", colors=["accent", "#ffffff", "#ffe9a8"], layers=[
            trail_line(width=0.5, tail_width=0.2, color=0, opacity=0.5, tail_opacity=0.1),
            trail_stamps("spark", size=1.3, size_range=0.7, spacing=11, scatter=9, spin=45,
                         twinkle=0.8, color=2, tail_size=0.4, glow=0.6),
            trail_stamps("dot", size=0.35, size_range=0.5, spacing=7, scatter=12, color=0,
                         twinkle=0.5, tail_opacity=0.2),
            trail_head("spark", size=2.4, color=1, glow=1.5, pulse=0.6),
        ]),

        # Hearts, small at the start and full size under the finger.
        trail("hearts", "Love Letter", icon="heart.fill", colors=["#ff3b6b", "#ff8fb0", "#ffd1dc"], layers=[
            trail_line(width=0.35, color=2, opacity=0.5, tail_opacity=0),
            trail_stamps("heart", size=1.7, size_range=0.35, tail_size=0.45, spacing=20,
                         scatter=4, spin=25, tail_opacity=0.5),
            trail_head("heart", size=2.6, color=0, glow=1, pulse=0.5),
        ]),

        # A hot core inside a wide halo, in the theme's accent.
        trail("laser", "Laser", icon="bolt.fill", colors=["accent", "#ffffff"], layers=[
            trail_line(width=1.5, color=0, opacity=0.8, glow=2.4, tail_width=0.6),
            trail_line(width=0.45, color=1, tail_width=0.6),
            trail_head("dot", size=1.3, color=1, glow=2.5),
        ]),

        # Running stitches with a ring where the needle is.
        trail("stitches", "Stitches", icon="line.diagonal", colors=["accent"], layers=[
            trail_line(width=0.8, dash=2.2, gap=2.6, tail_opacity=0.35),
            trail_head("ring", size=2),
        ]),

        # A brush stroke: nothing at the start, swelling to a wet tip.
        trail("brush", "Ink Brush", icon="paintbrush.pointed.fill", colors=["accent", "#ffffff"], layers=[
            trail_line(width=2.6, tail_width=0.05, color=0, opacity=0.85),
            trail_line(width=0.5, tail_width=0, color=1, opacity=0.3),
        ]),
    ]
