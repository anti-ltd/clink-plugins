# ---
# name: Shorthand
# icon: text.badge.plus
# summary: Suggests and expands shorthand, and keeps autocorrect off capitals and numbers
# version: 1.0
# author: Clink
# ---

# Suggestions and corrections of your own.
#
# suggestions(word, state) runs as you type and returns words for the bar,
# ahead of the keyboard's own. word is the one being typed, empty between
# words; context() has the text around it.
#
# correct(word, fix, state) runs when space ends a word. fix is what the
# keyboard was about to change it to, or None. Return a word to commit that
# instead, False to leave the word exactly as typed, or None to let the
# keyboard decide. Backspace right after still undoes it, like any
# autocorrect.
#
# Shorthand offers the expansion of a few abbreviations while you type them,
# expands them on space if you want, and keeps autocorrect off words in capitals
# and words with digits in them.
SHORT = {
    "brb": "be right back",
    "omw": "on my way",
    "idk": "I don't know",
    "tbh": "to be honest",
    "afaik": "as far as I know",
    "imo": "in my opinion",
}

def initial():
    return {"expand": False, "guard": True}

def settings(state):
    return section("text.corrections", [
        toggle("Expand shorthand on space", state["expand"], action="expand"),
        toggle("Leave capitals and numbers alone", state["guard"], action="guard"),
    ], title="Shorthand")

def on_action(action, value, state):
    if action in ("expand", "guard"):
        state[action] = value
    return state

def suggestions(word, state):
    long = SHORT.get(word.lower())
    return [long] if long else []

def correct(word, fix, state):
    long = SHORT.get(word.lower())
    if long and state["expand"]:
        return long
    if state["guard"]:
        if len(word) > 1 and word.isupper():
            return False
        if any(c.isdigit() for c in word):
            return False
    return None
