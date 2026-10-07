# Create a Clink plugin

You are contributing one focused plugin for Clink. Read `README.md`, inspect the existing `Plugins/*.py` files, and inspect `tools/build-manifest.py` before editing. Create or update exactly one plugin file in `Plugins/`.

A plugin is a Python file, `Plugins/<id>.py`, whose file name is its stable id. It starts with a header between two `# ---` lines giving the visible `name`, SF Symbol `icon`, concise `summary`, `version` and `author` as `# key: value` lines, exactly like the existing files, plus `network` (comma-separated host names) only for a plugin whose pages fetch. Everything after the header is the source, which is PyMini (a Python subset) and defines one or more of the hooks: `initial()`, `settings(state)`, `on_action(action, value, state)`, `on_open(state)`, `on_close(state)`, `on_key(key, state)`, `on_word(word, state)`, `on_backspace(state)`, `on_suggestion(word, state)`, `on_language(code, state)`, `on_field(kind, state)`, `on_tick(state)`, `on_swipe(direction, state)` (or `on_swipe(key, direction, state)`), `elements(state)`, `draw(id, state)`, `effects(state)`, `key_styles(state)`, `themes(state)`, `popups(state)`, `animations(state)`, `backgrounds(state)`, `trails(state)`, `layouts(state)`, `haptics(state)`, `hitboxes(state)`, `on_touch(key, x, y, state)`, `suggestions(word, state)`, `correct(word, fix, state)`, `bar_items(state)`, `key_hints(state)` (declarative flick annotations; see On-key flick hints below), `key_art(state)` (a dict from key names to lists of `shape(kind, anchor=, x=, y=, size=, fill=, stroke=, shadow=, opacity=, ...)`, drawn on those keys; the script draws everything, see the README's Key art), `on_event(name, info, state)` (one hook for everything that happens: `shift`, `plane`, `open`, `word`, `field`, and on request `key_down`, `key_up`, `key`, `tick`; key art is re-read after each) and `events(state)` (the names it wants). Every hook takes `state` last. The ones that change something return it; the ones that answer a question (the look hooks, `haptics`, `hitboxes`, `suggestions`, `correct`) return their answer and may change `state` in place.

On Android, **Use system haptics** overrides the custom feels returned by `haptics(state)` with the device’s native keyboard tick. The key-haptics switch still applies. Cursor and explicit gesture haptics remain separate.

The look hooks offer things the app lists under From plugins beside its own choices, using the builders in the README's Looks table: `key_style` (which can draw the whole key with `cap`, `cap_layer` and `gradient`, as in the README's Drawn keys section), `theme`, `popup_style`, `entrance`, `press_animation`, `letter_animation`, `transition`, `background` with `particles`, `trail` with `trail_line`, `trail_stamps` and `trail_head`, and `layout` with `layout_key`. A look is data, never code that runs per frame, and picking one copies it into the person's settings. `haptics` and `hitboxes` return tables keyed by key name (`"a"`, `"space"`, `"delete"`, `"return"`, `"letters"`, `"keys"`) of `feel(...)` or style words and `hitbox(scale=, x=, y=)`; both are read about once a second. `on_touch` runs after every tap, so keep it as cheap as `on_key`. `suggestions` runs when the bar settles and returns a list of words. `bar_items` returns `bar_button(id, name, icon=, title=)` and `bar_knob(id, name, icon=, min=, max=, step=, value=, setting=)` entries for Layout > Top bar; a tap or a released knob calls `on_action(id, value, state)`, and a knob with `setting=` turns that number setting itself. `correct` runs when space ends a word and returns a word, `False` to keep the word as typed, or `None` to leave the keyboard's own fix.

Draw the plugin's controls in `settings(state)` with the panel builders (`vstack`, `hstack`, `text`, `toggle`, `slider`, `stepper`, `segmented`, `button`, `row`, `field`). A plugin can also offer a layout element: `elements(state)` returns `element(id, name, icon=, width=, options=)` entries and `draw(id, state)` returns that element's face, using the display nodes plus `sparkline(values, min=, max=, fill=)`. An element is display-only, redrawn about once a second, and must read at key size. Anything that belongs to the placed key rather than to the whole plugin (12- or 24-hour on a clock, say) is an `option(key, label, choices=[...])` picker or an `option(key, label, default=True/False)` switch listed in `options=`; the editor draws them under that element and `draw(id, options, state)` reads what was picked. Wrap the controls that belong on a native screen in `section(anchor, [...], title=...)`, where the anchor is a settings card id such as `keys.spacebar` or `sound.keysounds` (the full list is on the docs page). The commands a plugin has on top of a panel's are `space_text(text)`, `set_setting(name, value)`, `claim(name)`, `release(name)`, `suggest(words)`, `banner(text)` and `press(key)` (`"space"` or `"delete"`, the keyboard's own keys), `pick_suggestion(slot)` (`"left"`, `"center"` or `"right"`, the chip under that part of the bar), `select(start, end)` (two whole numbers counted in characters from where the selection starts, or the caret when nothing is selected: negative reaches back into `context()["before"]` and `len(context()["selected"])` is the selection's end, so `select(-3, 0)` takes the three characters before the caret and equal values just move it), `select_word()`, `select_all()` (everything `context()` can see; iOS selection creation is not reliable, including Notes: without host selection-extension support these calls leave the text, caret and existing selection unchanged. No claim or Full Access enables missing support. On iOS, use text the person manually selected in the receiving app, and never assume select-then-cut/replace created a highlight; Android uses its native editor selection API), `cut()` (copies the selection and deletes it; needs Clipboard access, and does nothing without a selection) and `open_panel(panel)` (a built-in panel by its Tools id, such as `"layouts"`, `"emoji"` or `"calculator"`, or one of the person's own panels as `"custom:<id>"`, using the Plugin ID set in that panel's editor; only from `on_action`, and a panel that is switched off stays shut); the reads are `stats()` (a dict with `wpm`, `peak_wpm`, `keystrokes`, `words`, `streak`) and `setting(name)`. `setting`, `set_setting`, `claim` and `release` take the same control ids, listed at https://clinkkeys.app/docs/plugins/. A plugin that claims a control must release it when its switch is turned off, and a plugin that changes a setting for a while must put the person's own value back afterwards.

A plugin can add full-screen pages to the app (see the README's Pages section): `pages(state)` returns `page(id, title, icon=, summary=, anchor=, listed=)` entries for every page (`listed=False` for one reached only by `navigate`), `page_view(id, params, state)` returns that page's UI, usually rooted in `screen(children, title=, search=, toolbar=, refresh=)` and built with `grid`, `tile`, `image`, `spinner`, `empty` and `loader` as well as the settings builders, and `on_page(id, params, state)` runs when a page opens. `navigate(page, params)`, `back()`, `open_url(url)`, `install_theme(theme(...), apply=)` and `import_theme(url, format="clink"|"nukey")` only work from `on_action`. A plugin that needs the internet lists host names in a `# network:` header line and uses `fetch(id, url, ...)`, which returns nothing; the result arrives in `on_response(id, response, state)`. Keep fetched data in state keys starting with `_`, which are never saved.

For graphs drawn on existing keys, use `graph(values, min=, max=, anchor=, unit=, x=, y=, width=, height=, stroke=, fill=, line_width=, opacity=)`. It returns a list of ordinary shapes; concatenate labels or other artwork and pass the list to `art(...)` or return it for any key from `key_art`. Python chooses the metric and destination. See `Plugins/spacebar-graph.py` for a WPM example that draws only on space. Keep sampling in hooks; `graph` only draws the samples supplied to it.

Keep the plugin small, offline (unless it has pages that declare `network` hosts) and deterministic. `on_key` runs on every keystroke, so keep that hook cheap or leave it out, and prefer `on_word` when a word at a time is enough. `on_swipe` gets `"left"`, `"right"`, `"up"`, `"up_left"` or `"up_right"` for a flick on the letters, only while swipe typing is off, so a plugin that relies on it turns `gestures.swipe` off with `set_setting` (and `gestures.predictive_flick` too if it uses upward flicks) and restores the person's values when switched off; it must call nothing when it has nothing to do, because a flick no plugin acts on stays an ordinary keystroke. Declare it as `on_swipe(key, direction, state)` instead to be told which key the flick started on, as a lowercase letter (the spelling `on_touch` and `key_art` use), so one hook can give each letter its own gesture. Inside `on_swipe`, the prospective letter has not been inserted and `context()` sees the original selection; queued commands consume the held tap without replacing that selection, so `copy(context()["selected"])`, `cut()` and `insert(...)` act on what the person had selected; guard each branch on there being something to act on, so a flick with nothing to do stays a keystroke. Ordinary flicks start on letter keys; delete and return retain their native gestures — and there is no downward direction, because a downward drag is the quick accent's. `on_tick` runs once a second with no keystroke behind it; use it only for something that has to change while nobody is typing, and keep it just as cheap. Use no imports beyond `math`, `random`, `time`, `json` and `re`; never `open`, `eval`, `exec`, `compile` or names with double underscores. Treat everything it inserts as user-facing text and preserve Unicode.

Use a unique id and a descriptive kebab-case filename. Check that the header is complete and think through the empty, first-word and long-session cases. Then run:

```sh
python3 tools/build-manifest.py
```

It packs the plugin into `build/` (which is not committed) and stops with the file and line if the header is wrong. Include the regenerated `manifest.json` if changed. Do not alter the release workflow or the source policy. Finish by explaining which hooks the plugin defines, what it puts on the keyboard, and the checks performed.


### On-key flick hints

`key_hints(state)` returns a dictionary of lowercase key names to `key_hint(...)`
or a list of up to five hints. `letters` and `keys` are fallbacks. This is a
pure provider: it declares annotations and never runs the actions to discover them.
A plugin must also define `on_swipe` and have Typing data access; its hints hide
while swipe typing is enabled. Only letter keys show these annotations.

```python
def initial():
    return {"hints": True, "style": "capsule", "position": "top_left"}

def key_hints(state):
    return {"c": key_hint("Copy", direction="left", style=state["style"],
                          position=state["position"], visible=state["hints"])}

def on_swipe(key, direction, state):
    if key == "c" and direction == "left":
        copy(context()["selected"])
    return state
```

`text` defaults to empty (an arrow only); up to 40 characters are fitted to the key.
`direction`: `left`, `right`, `up`, `up_left`, `up_right` (default `up`).
`style`: `plain` (text), `symbol` (arrow and text), `capsule` (arrow and text
inside a capsule, default). `position`: `top_left`, `top`, `top_right` (default),
`bottom_left`, `bottom`, `bottom_right`; these are physical positions, also in RTL.
`visible=False` or an empty list explicitly suppresses a key's fallback. The
highest priority plugin owns a given key's hints. Give different directions
different positions to avoid overlap. Native predictive flick owns the upward
hint when that key has an assigned suggestion.

Expose visibility, style and position in `settings(state)` and update them in
`on_action`; the hints refresh from that state. Hooks/events/ticks refresh them
alongside key artwork. Disabling the plugin clears its hints. Hints never create
hit targets or alter tap/flick behavior.

Predictive flick uses the same styles through
`settings.predictiveFlickHintStyle` (`plain`, `symbol`, `capsule`), retains its word
in every style, and keeps the existing `settings.predictiveFlickSuggestionPosition`
(`off` hides) and `settings.predictiveFlickSuggestionsSeparate` controls.


### Direct native tool functions

These commands execute in the keyboard; app editors only log them.
The existing `on_action`, `on_key`, `on_touch` and `on_swipe` hooks can call
`translate(language)`, `ai_tools(action)`, `clipboard_copy(item)` and
`clipboard_paste(item)`. These are commands returning `None`, never result text.
They install no bindings; add a binding only when requested. Lifecycle, timer,
`on_event`, automation and rendering hooks cannot invoke them.

`translate("en")` takes an enabled Translate target's BCP-47 ID. `ur` selects
Urdu script and `ur-Latn` selects Roman Urdu (Latin letters); both require AI
translation on iOS. Android supports `ur` offline and both scripts through an
explicitly configured cloud provider with AI translation enabled; `ur-Latn`
requires AI. The selected model must support Urdu. `ai_tools`
takes an enabled built-in ID (`proofread`, `rewrite`, `paraphrase`, `grammar`,
`shorten`, `expand`, `summarize`, `tone_casual`, `tone_professional`,
`tone_friendly`, `tone_confident`, `emojify`, `reply`) or the exact installed
custom action ID, preserving user prompt overrides and provider selection.
`polish` aliases `rewrite`; `fun` is not a built-in ID. Never invent a custom ID.
On Android, Gemini Nano writing uses the foreground Clink screen and does not implement
`ai_tools(action)` or custom prompts. `open_panel("ai")` opens the enabled launcher;
the person must open Clink, choose an action, then copy or explicitly return the result.
Do not promise automatic AI replacement from an Android plugin.
Both act on the selection, otherwise the visible document. Their native progress
and errors remain visible, but successful transforms replace the captured text
automatically and compose AI actions insert. A changed field/text, dismissed
operation, revoked approval or lost entitlement prevents delayed application.

Clipboard item numbers start at 1 in the full saved history (pinned first), not a
filtered group. Copy copies text/original image data; paste inserts text or copies
an image for manual paste, honoring native delete/close preferences. Missing or
disabled targets do nothing. All functions require Pro, enabled plugins and the
enabled target tool. AI/Translate require Typing data; clipboard functions require
Clipboard access plus Full Access. Clipboard variables in AI prompts need the
Clipboard grant. Native provider setup, Pro and Full Access gates still apply.
Never enable or emulate a locked tool to evade its gate.

## Exported artifact APIs

An installed custom panel, Python action or plugin can publish named functions.
Declare the names in `api_exports` and implement `on_api(name, arguments)`:

```python
api_exports = ["uppercase", "type_uppercase"]

def on_api(name, arguments):
    result = arguments["text"].upper()
    if name == "type_uppercase":
        insert(result)
    return {"text": result}
```

A panel still supplies its normal `view(state)` and an action its `transform(text)`.
A plugin can consist solely of exports. Exports are opt-in: declaring `on_api`
without a valid list does not expose anything, and callers cannot invoke private
hooks. Names are unique ASCII letters, digits, `_` or `-`, do not start with `_`,
and are at most 64 bytes (1–32 exports per artifact).

A calling plugin uses `call_api(target, function, arguments)` from an existing
`on_action`, `on_key`, `on_touch` or `on_swipe` handler. All arguments are positional;
the third argument is an optional dictionary, defaulting to `{}`. The return value
is `{"ok": True, "value": ..., "error": ""}` on success or
`{"ok": False, "value": None, "error": "code"}` on failure. Check `ok` before using
`value`. Returning text does not insert it; an export can return data, queue an
operation, or do both. This API creates no bindings.

Targets are `panel:<handle>` (the panel's Plugin ID), `action:<installed-id>`
(the Python action's ID in its exported `.clinkext` file), or
`plugin:<installed-id>` (the installed plugin ID, which may differ from its
repository package ID). Take the exact ID from the user or configuration; display
names are not IDs. Reimporting an action creates a new installed ID. Missing,
ambiguous, disabled or unapproved targets fail closed. The target's feature must
be enabled, and Clink Pro is checked for each call. App editors return
`unavailable`; they do not execute installed exports.

Every export runs in a fresh isolated module. It receives explicit arguments,
not the target's saved state or the caller's state. It does not run `initial` or
`on_open`; `context`, stats and settings have no live data. Module globals reset
on each invocation. There is no network access or nested API resolver. This keeps
another artifact's retained private data out of a call. Pass required input in
`arguments` and return changed data to the caller.

Values must be JSON data: `None`, booleans, finite numbers, strings, lists and
dictionaries with string keys. Arguments and results are copied, limited to 64 KB,
16 levels and 4096 nodes. Cyclic values are rejected. Each hook can make at most
eight calls; each export's loader and handler have a 20,000-step/20ms budget.

Exports may queue `insert`, `backspace`, `delete_word`, `replace`, `move_cursor`,
`copy` and `haptic`. Plugin exports may also queue the native tool functions
`translate`, `ai_tools`, `clipboard_copy` and `clipboard_paste`. The batch is
limited to 16 effects and 64 KB. Operations retain the caller's and target's grants;
clipboard effects also require iOS Full Access. Native tool availability, provider
setup and Pro checks still apply. Exports cannot change settings, navigate, open
panels, run automations or delegate further API calls.

A failed export, invalid result or denied effect discards that export's entire
batch. Successful operations join the caller's command queue, so a subsequent
caller error discards them too. Swipe effects run after the host consumes the held tap. Never backspace to
remove its landing letter; the original selection remains available. `ok` confirms successful computation and accepted operations;
it does not report completion of asynchronous AI or Translate work.

Failure codes: `unavailable`, `input_required`, `call_limit`, `invalid_arguments`,
`load_failed`, `not_exported`, `execution_failed`, `invalid_result`, `effect_limit`,
`effect_denied`. Invalid `call_api` argument shapes raise a script error.

Vietnamese input controls: `settings.vietnameseQuickWEnabled` is an opt-in boolean for the Telex `w → ư` shortcut (`tw → tư`, `nhw → như`, `ww → w`). It takes priority over initial teencode `w`; leave it false to type `was → wá` with `settings.vietnameseTeencodeEnabled` true. The z/k chat spellings still work with both switches enabled. Composition requires Vietnamese to be the sole active typing language.

Tools menu layout shortcuts: settings.oneHandedInToolsMenu, settings.splitKeyboardInToolsMenu and settings.numberRowInToolsMenu are opt-in booleans that show immediate layout toggles in the Tools menu, independently of layout.one_handed, layout.split and layout.number_row. They do not turn the layout features on. The shortcuts return to the keys after toggling; one-handed retains the selected side. Form hides the one-handed and split shortcuts; non-text layouts hide the number-row shortcut. These shortcuts are not open_panel targets.

Paired theme imports: `import_theme(..., format="clink")` accepts a theme document with `pairedVariants`: exactly two complete, non-nested theme documents, one `isDark: false` and one `isDark: true`. The parent holds the shared design and single library identity. Automatic appearance selects the matching variant. Preserve `pairedOverrides` from exports: its light/dark arrays record customized field paths; when omitted, Clink infers them from variant differences. These are theme document fields, not `theme(...)` builder arguments.

Space-bar gestures: `space_swipes(state)` is a command-free provider returning a list of `left`, `right`, `up`, `up_left`, `up_right`. It requires Typing data access and `on_swipe(key, direction, state)`; only opted-in plugins receive `key="space"`. When any direction is selected, the first 200 ms after touch-down are reserved for a quick flick. Beyond 36 points, the first selected direction reached within that window fires once, including diagonal starts. After 200 ms, an unconsumed touch becomes native cursor control, respecting a longer cursor activation delay. Sustained dragging needs no stationary hold first. An unselected quick flick inserts nothing; continuing the drag after the window moves the cursor. A consumed language flick cannot move the cursor during that touch. With no selected directions, native cursor timing is unchanged. An active cursor drag and iOS Shift selection retain native behavior. Queue nothing to decline. A tap still inserts a space on release, so a space flick has no provisional letter to undo. `setting("settings.keyboardLanguages")` gives enabled language IDs in order. Use `set_setting("language", code)` for an enabled ID and its assigned layout; preserve the person’s Language Mode unless they ask to change it. Force a temporary language badge using `space_language_text(code)` on open and language changes, then clear with `None` on close; this overrides a hidden native badge without changing the saved preference. Never issue commands from `space_swipes`.

For a preferred starting language, call `set_setting("language", code)` from `on_open(state)` only, choosing an enabled ID from `setting("settings.keyboardLanguages")`. The host opens an unchanged runtime once per keyboard appearance, not for ordinary settings or manual-language reloads. Do not force the language in `on_language`, `on_key` or `on_tick`: manual language switching must remain available until the next opening.

Glyph sizing: `keys.glyph_scale` (letters) and `settings.longPressGlyphScale` (long-press hints) accept 0.5–1.4 in steps of 0.05, with a default of 1.0. These are keyboard-wide settings, separate from theme glyph placement.

Punctuation controls: `text.space_after_punctuation` opts into a space after prose punctuation; `text.punctuation_spacing` removes a preceding space, and `text.double_space_period` controls two Space presses. These are independent Boolean controls. `settings.topBarRowSpacing` accepts 0–20 points, `settings.oneHandedEmojiCount` accepts Auto (0) or an even count from 2–12, and `settings.oneHandedEmojiScale` accepts 0.5–2.0. `layout.one_handed_glyph_scale` accepts 0.5–1.4 (default 0.82); it controls key glyphs independently of `layout.one_handed_width` while Scale spacing and glyphs is on.

Theme document preview placement: `import_theme(..., format="clink")` accepts `longPressPreviewPosition` (`topLeading|top|topTrailing|leading|center|trailing|bottomLeading|bottom|bottomTrailing|custom`) and `longPressPreviewCustomPosition` (`{"x": 0.5, "y": 0.5}`, normalized 0...1). Omit the position to inherit the main long-press preview setting. The same fields inside `keyPaint[keyID]` or `groupPaint[group]` override only that key or group; omit both there to inherit its group or theme placement. They move the small hold hint independently of `glyphPosition` and `glyphCustomPosition`. These fields never enable previews; `keys.long_press_hint` controls visibility. They are document fields, not `theme(...)` builder arguments.

Toolbar visibility: `setting("settings.toolsHiddenFromToolbar")` is a list of tool IDs hidden from the resting toolbar (AI uses `ai`). `set_setting("settings.toolsHiddenFromToolbar", ids)` changes only this extra filter; `[]` restores the default. It does not enable tools, change Tools menu visibility, or change when toolbar icons appear.

Lighting paint targets: people can combine Faces, Letters, Glow, Bar and Two-tone in Effects > Paints. Two-tone lights opposite key corners from the selected color source: Spectrum and effect palettes animate both tones half a palette cycle apart, theme colors use opposing hues, and Custom exposes Light color and Secondary color. It works with plugin effects; do not invent target or secondary-color arguments for `light_effect(...)` or `light_layer(...)`.

The `pet.species` control includes `android`, the green Android pet. It renders on Android, in debug builds, or on iOS with verified private-account pairing to an Android device. The `apple` choice is the silver Apple pet: it renders on iOS, or on Android with a verified Apple device paired to the same private account. A website link alone does not qualify. A setting write or imported profile never grants platform pet access: ineligible devices show Blob. Normal Pets feature access still applies.

Plugin suggestions from `suggestions(word, state)` and `suggest(words)` also appear in the Chinese candidate rail. During composition, the leading native conversion stays first. Choosing a plugin completion ends composition and follows the ordinary word-completion behavior; native candidates keep partial-conversion behavior.

Key surfaces: `key_style(..., material="3d", variant="retro", surface="gloss")` combines a key style with a surface. `surface` accepts `normal`, `gloss`, `grain`, or `glass` on every style and finish. It takes precedence over the supported legacy `glass` Boolean; omit both to keep the current surface. Imported Clink theme documents use `keySurfaceMaterial` for the same choice, including within `keyPaint` and `groupPaint`; when absent, existing `liquidGlass` and legacy 3D glass flags keep their original appearance.

Retro finishes: `key_style(..., material="3d", variant="retro", retro_finish="soft", surface="grain")` uses a narrower bevel, flatter face and tighter shadows. `retro_finish` accepts `classic` or `soft`; omitting it preserves the current finish. Imported theme documents use `retroFinish`, including in `keyPaint` and `groupPaint`. An absent theme field keeps Classic Retro. Finish and surface material are independent.

Material tuning: `key_style(...)` accepts `grain_density` (0...1), `grain_size` (0.25...2 points), `grain_strength` (0...0.3), `gloss_strength` (0...1) and `gloss_spread` (0.1...0.9). Omit a field to keep the current value. Theme documents and Canvas paint use `grainDensity`, `grainSize`, `grainStrength`, `glossStrength` and `glossSpread`; absent theme values default to 1, 0.5, 0.025, 1 and 0.42 respectively. These tune appearance only.

Brick keys: `key_style(..., material="3d", variant="brick")` selects a molded phone-keypad crown with a dark socket rim. It supports every keyboard layout, including T9; use `shape="capsule"` for classic rounded phone keys. The normal, gloss, grain and glass surfaces remain independent. Theme documents use `threeDVariant: "brick"`.

The Tools button style control `settings.toolsButtonStyle` accepts `plain`, `flat`, `realistic`, `mechanical`, `transparent` and `dots`. The dot matrix plays a brief opening wave using the theme accent. `settings.toolsButtonTypingReaction` is a Boolean, off by default, enabling subtle typing pulses with the dots style. Reduced motion disables moving waves. Restore the person’s original choices when a temporary effect ends.
