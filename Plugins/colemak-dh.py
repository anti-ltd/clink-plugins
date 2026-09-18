# ---
# name: Colemak-DH
# icon: keyboard
# summary: The Colemak-DH layout, installed as a custom layout
# version: 1.0
# author: Clink
# ---

# A layout for Layout > Arrangement.
#
# layouts(state) returns layout(id, name, rows=[...]) entries. Each row is a
# list of keys: a plain string is a letter key, and layout_key(glyph,
# action=, width=) is anything else. action is one of insert, spacer, shift,
# delete, space, return, numbers, emoji, globe, tab, left, right, undo, redo
# or dismiss. left=[...] and right=[...] put up to three keys either side of
# the space bar. Shift and delete are added for you unless a row places its
# own. The 123 and #+= pages come from the stock ones.
#
# Picking a layout installs it as an ordinary custom layout, so it can be
# edited like any other and stays with the plugin removed.
def layouts(state):
    return [
        layout("colemak-dh", "Colemak-DH", icon="keyboard",
               rows=[list("qwfpbjluy"), list("arstgmneio"), list("zxcdvkh")],
               right=[layout_key(".")]),
    ]
