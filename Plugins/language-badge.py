# ---
# name: Language Badge
# icon: globe
# summary: Show the active language in the corner of the space bar
# version: 1.2
# exclusiveResources: spacebar.language_badge
# author:
# ---

# Uses Clink's native plugin enable switch. No persistent settings are changed.
# Requires the space_language_text command; the main caption stays independent.
def _show(code):
    space_language_text(code.replace("-", "_").split("_")[0].upper())


def on_open(state):
    _show(setting("language"))
    return state


def on_language(code, state):
    _show(code)
    return state


def on_close(state):
    space_language_text(None)
    return state
