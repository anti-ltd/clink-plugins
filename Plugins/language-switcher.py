# ---
# name: Language Switcher
# icon: globe
# summary: Swipe the space bar to switch languages with a visible language code
# version: 1.0
# exclusiveResources: spacebar.language_badge
# author: Clink
# ---

# Idea 137. A temporary badge leaves the saved language-code preference intact.
# Direction controls use universal arrows; the heading reuses reviewed catalog copy.
LANGUAGES = {'en': 'Languages', 'af': 'Tale', 'de': 'Sprachen', 'es': 'Idiomas', 'et': 'Keeled', 'fr': 'Langues', 'hu': 'Nyelvek', 'it': 'Lingue', 'ja': '言語', 'ko': '언어', 'ms': 'Bahasa', 'pt': 'Idiomas', 'ru': 'Языки', 'zh-Hans': '语言', 'ro': 'Limbi', 'nl': 'Talen', 'zh-Hant': '語言', 'pl': 'Języki', 'uk': 'Мови', 'tr': 'Diller', 'cs': 'Jazyky', 'sk': 'Jazyky', 'el': 'Γλώσσες', 'sv': 'Språk', 'da': 'Sprog', 'nb': 'Språk', 'fi': 'Kielet', 'id': 'Bahasa', 'vi': 'Ngôn ngữ'}
DIRECTIONS = ["left", "right", "up", "up_left", "up_right"]
ARROWS = ["←", "→", "↑", "↖", "↗"]


def initial():
    return {"left": True, "right": True, "up": False,
            "up_left": False, "up_right": False}


def settings(state):
    locale = context()["locale"].replace("_", "-")
    label = LANGUAGES.get(locale, LANGUAGES.get(locale.split("-")[0], "Languages"))
    controls = []
    for i in range(len(DIRECTIONS)):
        direction = DIRECTIONS[i]
        controls.append(toggle(ARROWS[i], state.get(direction, False), action=direction))
    return section("languages.switch", controls, title=label)


def on_action(action, value, state):
    if action in DIRECTIONS:
        state[action] = bool(value)
    return state


def space_swipes(state):
    if len(setting("settings.keyboardLanguages")) < 2:
        return []
    return [direction for direction in DIRECTIONS if state.get(direction, False)]


def on_swipe(key, direction, state):
    if key != "space" or direction not in space_swipes(state):
        return state
    languages = setting("settings.keyboardLanguages")
    current = setting("language")
    index = 0
    for i in range(len(languages)):
        if languages[i] == current:
            index = i
    step = -1 if direction in ["left", "up_left"] else 1
    code = languages[(index + step) % len(languages)]
    set_setting("language", code)
    show(code)
    return state


def show(code):
    space_language_text(code.replace("-", "_").split("_")[0].upper())


def on_open(state):
    show(setting("language"))
    return state


def on_language(code, state):
    show(code)
    return state


def on_close(state):
    space_language_text(None)
    return state
