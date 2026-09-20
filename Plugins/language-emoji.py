# ---
# name: Language Emoji
# icon: face.smiling
# summary: Show the active language as a flag emoji on the space bar
# version: 1.1
# exclusiveResources: spacebar.language_badge
# author:
# ---

# Uses the native plugin enable switch and the space bar corner picker.
# No settings or claims are changed. Requires Clink's space_language_emoji command.
def on_open(state):
    space_language_emoji(setting("language"))
    return state


def on_language(code, state):
    space_language_emoji(code)
    return state


def on_close(state):
    space_language_emoji(None)
    return state
