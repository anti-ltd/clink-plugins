# ---
# name: Clock
# icon: clock
# summary: The time on a key, for a custom layout
# version: 1.1
# author: Clink
# ---

# A clock for a custom layout.
#
# Add it from Layout > Arrange > Element and pick Clock or Clock with date, then
# choose 12- or 24-hour on that key: the choice belongs to the element, so one
# layout can carry a 24-hour clock and a 12-hour one beside it.
#
# Elements redraw about once a second, so the minute turns over on its own and
# the plugin needs no hooks at all to stay current.

import time

def clock_options():
    return [
        option("time", "Time", ["24-hour", "12-hour"]),
        option("seconds", "Seconds", default=False),
    ]

def elements(state):
    return [
        element("clock", "Clock", icon="clock", width=2, options=clock_options()),
        element("clock_date", "Clock with date", icon="calendar", width=3,
                options=clock_options()),
    ]

def draw(id, options, state):
    if options["time"] == "12-hour":
        pattern = "h:mm:ss a" if options["seconds"] else "h:mm a"
    else:
        pattern = "HH:mm:ss" if options["seconds"] else "HH:mm"
    if id == "clock_date":
        return vstack([
            text(time.format(pattern), size=13, weight="semibold"),
            text(time.format("EEE d MMM"), size=9, color="gray"),
        ], spacing=1)
    return text(time.format(pattern), size=15, weight="semibold")

def settings(state):
    return text("Add a clock to a custom layout from Layout > Arrange > Element. "
                "12- or 24-hour is picked on the element itself, so two clocks "
                "can differ.", size=13, color="gray")
