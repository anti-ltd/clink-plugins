<p align="center">
  <img src="https://raw.githubusercontent.com/anti-ltd/clink-language-packs/main/icon-1024.png" width="96" alt="Clink app icon">
</p>

<h1 align="center">Clink plugins</h1>

<p align="center">Open plugins for Clink: scripts that run alongside the keyboard.</p>

A plugin hooks into typing and can drive the keyboard's own controls. It draws its settings with the same builders a custom panel uses, can put a switch on a native settings screen, and gets a set of hooks the keyboard calls as you type. Plugins run only with a Clink Pro membership, and download only after the person using Clink explicitly trusts the repository.

## Official Clink repositories

[Language packs](https://github.com/anti-ltd/clink-language-packs) · [Layouts](https://github.com/anti-ltd/clink-layouts) · [Profiles](https://github.com/anti-ltd/clink-profiles) · [Themes](https://github.com/anti-ltd/clink-themes) · [Panels](https://github.com/anti-ltd/clink-panels) · [Actions](https://github.com/anti-ltd/clink-actions) · [Plugins](https://github.com/anti-ltd/clink-plugins) · [Fonts](https://github.com/anti-ltd/clink-fonts) · [Sounds](https://github.com/anti-ltd/clink-sounds)

## Included plugins

| Plugin | What it does |
|---|---|
| WPM Spacebar | Puts your live typing speed on the space bar. Its switch sits under Keys > Space bar in the app. |
| WPM Sparkline | A graph of the last half minute of your typing speed, as a layout element. |
| Clock | The time, with or without the date, as a layout element. 12- or 24-hour is set per element. |
| Light Show | Two lighting effects for the Effects page: Aurora, a slow wave through greens and blues with a twinkle on top, and Tempo, a wave that speeds up as you type faster. |
| Flick Gestures | Flicks anywhere on the letters, each with its own switch: left deletes a word, right types a space, up picks the middle suggestion and up-left or up-right the ones either side. The switches sit under Gestures > Swipe typing, and swipe typing is off while any of them is on. |
| Low Profile | A key drawn entirely in Python: shallow side walls, a narrow bevel, a dished face and a small fixed foot, with short press travel. Apply it to any theme from the theme editor's Style card. |
| Low Profile Mod | An example that modifies the built-in 3D mechanical style: tighter corners, an inset face, raised edges and angled lighting. Compare its settings with Low Profile's Python drawing layers. |
| Bubble Popups | A round key popup that floats a little higher than the built-in one and springs in. |
| Motion Kit | One of each animation: Swoop (entrance), Dip (key press), Bounce (letters) and Glide (switching between letters, 123 and #+=). |
| Snowfall | An animated background: snow drifting behind the keys, with a puff of light from every key you press. |
| Colemak-DH | The Colemak-DH layout, installed as an ordinary custom layout you can edit. |
| Heavy Space | A heavier haptic on the space bar, a crisp one on return and a light one on delete. Its switch sits under Sound & Haptics. |
| Caps Lock Light | A little green lamp in the top right of shift that lights while caps lock is on, and sits dark when it is off. Drawn entirely by the script with `key_art` and lit from `on_event`, so it doubles as the example for both. |
| Press Spark | A ring in the theme's accent colour around whichever key is down. The example for the `key_down` and `key_up` events. |
| Adaptive Hitbox | Learns where you actually tap each key and moves its target toward it. Its switch sits under Keys > Hitboxes. |
| Shorthand | Suggests "be right back" while you type brb (and a few more), can expand them on space, and keeps autocorrect off words in capitals and words with digits. |
| Switch Volume | A knob for the top bar that sets how loud your key presses are. Drag it and each step clicks at the new level. Add it from Layout > Top bar. |
| Swipe Trails | Six trails for swipe typing: Candy Ribbon (a pastel band that keeps flowing), Stardust, Love Letter (hearts), Laser, Stitches and Ink Brush. Pick one from Gestures > Swipe typing; your thickness, taper and trail-the-finger settings still shape it. |
| Typewriter | A key and a popup drawn entirely in Python: round glass faces in chrome rings on stems, with bars for the wide keys, and a Typed Slip popup that strikes your letter on typing paper. Two themes for the Plugins tab of the theme gallery, Typewriter Ivory and Typewriter Noir, the key on its own for any theme, a deep Typebar press, a Strike letter animation, and clacky haptics with a heavy return. The haptics switch sits under Sound & Haptics. |

The files live in [`Plugins/`](Plugins). Each one is an ordinary Python file, readable in one sitting, that starts with a short header:

```python
# ---
# name: Clock
# icon: clock
# summary: The time on a key, for a custom layout
# version: 1.1
# author: Clink
# ---
```

The file name is the plugin's id, and everything after the header is its script. `tools/build-manifest.py` packs each one into the `.clinkplugin` file Clink downloads, in `build/`. A plugin that offers a layout element is added from Layout > Arrange > Element in the app, not from a settings screen, and one that offers a top bar button or knob is added from Layout > Top bar.

## What a plugin can do

A plugin script may define any of these functions:

| Hook | When it runs |
|---|---|
| `initial()` | Once, to build the state the plugin starts with. |
| `settings(state)` | Whenever the app draws the plugin's controls. Returns a node tree built with the panel builders (`vstack`, `toggle`, `slider`, ...). Wrap part of it in `section("keys.spacebar", [...])` and it also appears on that screen in the app. |
| `on_action(action, value, state)` | A control was used. |
| `on_open(state)` / `on_close(state)` | The keyboard appeared or is going away. |
| `on_key(key, state)` | A key inserted text. Runs after the text is in, so `" "` means the space is already typed. |
| `on_word(word, state)` | A word was committed, with autocorrect already applied. |
| `on_backspace(state)` | Delete was pressed. |
| `on_suggestion(word, state)` | A suggestion bar word was tapped. |
| `on_language(code, state)` | The typing language changed, for example to `"de"`. |
| `on_field(kind, state)` | The keyboard moved to a different kind of field: `"default"`, `"email"`, `"url"`, `"number"`, `"phone"`, `"search"` or `"password"`. |
| `on_tick(state)` | Once a second while the keyboard is on screen, whether or not anything is being typed. |
| `on_swipe(direction, state)` | A flick that started on a letter key: `"left"`, `"right"`, `"up"`, `"up_left"` or `"up_right"`. Only while swipe typing is off. |
| `elements(state)` | What this plugin offers a custom layout. Return `element(id, name, icon=, width=, options=)` entries. |
| `draw(id, state)` | One element's face, as a node tree. `sparkline(values, min=, max=, fill=)` is the node built for a key. |
| `draw(id, options, state)` | The same, for an element with options: `options` holds what was picked on that key. |
| `effects(state)` | Lighting effects this plugin offers the Effects page. Return `light_effect(...)` entries; see Lighting effects below. |
| `key_styles(state)` | Key styles for the theme editor. Return `key_style(...)` entries; see Looks below. |
| `themes(state)` | Whole themes for the Plugins tab of the theme gallery. Return `theme(...)` entries. |
| `popups(state)` | Key popup styles. Return `popup_style(...)` entries. |
| `animations(state)` | Any mix of `entrance(...)`, `press_animation(...)`, `letter_animation(...)` and `transition(...)`. |
| `backgrounds(state)` | Animated backgrounds. Return `background(...)` entries made of `particles(...)` layers. |
| `trails(state)` | Swipe trails. Return `trail(...)` entries made of `trail_line(...)`, `trail_stamps(...)` and `trail_head(...)` layers. |
| `layouts(state)` | Keyboard layouts. Return `layout(...)` entries. |
| `haptics(state)` | A haptic per key, as a dict: `{"space": "heavy"}`. See Typing below. |
| `hitboxes(state)` | A hit area per key, as a dict: `{"a": hitbox(x=-0.1)}`. |
| `on_touch(key, x, y, state)` | After every tap: which key it went to and where on the key the finger landed. |
| `suggestions(word, state)` | Words for the suggestion bar while `word` is being typed. |
| `correct(word, fix, state)` | Space ended `word`. Return the word to commit, `False` to keep it as typed, or `None` for the keyboard's own `fix`. |
| `bar_items(state)` | Buttons and knobs this plugin offers the top bar. Return `bar_button(...)` and `bar_knob(...)` entries; see Top bar below. |
| `key_art(state)` | Draw on the keys: a dict from key names to lists of `shape(...)`. See Key art below. |
| `on_event(name, info, state)` | Anything that happens on the keyboard, in one hook. See Events below. |
| `events(state)` | The event names `on_event` wants. Leave it out for all but the busy ones. |

An element can let each placed copy decide something for itself with
`option(key, label, choices=["a", "b"])` or `option(key, label, default=False)`.
The editor draws those under the element in Layout > Arrange, so one layout can
carry a 24-hour clock and a 12-hour one, and `draw` reads the answers from its
`options` argument.

Every hook gets `state` last and may return it changed. State is kept between calls and between the app and the keyboard.

On top of the panel commands (`insert`, `replace`, `haptic`, ...) a plugin has:

- `space_text(text)` to caption the space bar (32 characters, `None` hands it back).
- `setting(name)` and `set_setting(name, value)` to read and change about a hundred of Clink's own settings, from `sound.enabled` to `theme` and `layout.one_handed`. Values are checked against the same ranges the app's controls use.
- `claim(id)` and `release(id)` to take over one of those settings. Its card in the app says which plugin manages it, and the space bar caption field locks while claimed.
- `suggest(words)` to put up to ten words in the suggestion bar, and `banner(text)` for a short message over it.
- `press(key)` to run the keyboard's own `"space"` or `"delete"` key. A pressed space autocorrects the word before it, which `insert(" ")` doesn't.
- `pick_suggestion(slot)` to take the suggestion chip under the `"left"`, `"center"` or `"right"` third of the bar, exactly as a tap on it would.
- `stats()` for the live typing rate and totals.

In the app, Home > More > Developer lists every id with what it accepts, and Show ids badges each settings card with the anchor `section(...)` takes.

### Lighting effects

`effects(state)` returns lighting effects, which show up in the app under
Effects > From plugins next to the built-in styles. Each is a stack of layers
that apply top to bottom:

```python
def effects(state):
    return [light_effect("tide", "Tide", colors=["#00e5ff", "#7c4dff"], layers=[
        light_layer("solid", low=0.2, high=0.2),
        light_layer("wave", moves="both", speed=0.8, size=1.5, direction="up"),
    ])]
```

A layer's `pattern` is one of `solid`, `pulse`, `wave`, `gradient`, `twinkle`,
`sweep`, `rain`, `flicker` or `checker`. The keywords, all optional:

| Keyword | Values | Meaning |
|---|---|---|
| `moves` | `"light"`, `"color"`, `"both"` | What the pattern changes. Default `"light"`. |
| `mix` | `"add"`, `"max"`, `"multiply"` | How its brightness meets the layers above. `"multiply"` masks. |
| `shape` | `"smooth"`, `"ramp"`, `"step"`, `"spike"` | The rise and fall of pulse, wave and gradient. |
| `direction` | `"right"`, `"left"`, `"down"`, `"up"`, `"out"` | Which way wave, gradient, sweep and rain travel. |
| `speed` | 0 to 4 | 0 holds it still. |
| `size` | 0.25 to 4 | How many times it repeats across the board (for twinkle, how many keys are lit). |
| `low`, `high` | 0 to 1 | The brightness it runs between. |
| `color_span`, `color_offset` | 0 to 1 | How far along the colors it moves, and where it starts. |

`colors` takes up to eight `"#rrggbb"` strings that the color loops through.
Leave it out and the effect uses the person's own Color setting. The person can
also hold an effect and choose Duplicate to get an editable copy of their own.

While a plugin's effect is running and the keyboard is up, `effects(state)`
runs again about once a second, so an effect can follow the state or `stats()`.
Change as little as you can each time: round a typing rate rather than passing
it straight through, or the effect is replaced every second for nothing.

### Looks

The look hooks hand the app things to pick, each one shown under From plugins
next to the built-in choices. Picking one copies it into your settings, so it
keeps working with the plugin switched off or removed. The script is never run
per frame: a look is only numbers and words.

| Builder | Where it shows | Keywords |
|---|---|---|
| `key_style(id, name)` | Theme editor, Style card. Applied to the theme being edited. | `cap`, a `cap(...)` that draws the whole key (see Drawn keys below), or `material` (`solid`, `empty`, `metal`, `3d`, `classic`, `slab`, `gamepad`, `liquidIce`, `molten`, `eink`), `variant` (`retro`, `modern`, `mechanical`, `mechanicalSwitches`, `berry`), `shape` (`rect`, `fret`, `berry`, `bevel`, `dome`), `glass`, `fan`, `inner_radius`, `face_inset`, `edges`, `raised`, `light_angle`, `shadow` (0 is flat), `shadow_radius`, `shadow_y`, `outline`, `outline_opacity` |
| `theme(id, name)` | Themes, Plugins tab. Installed as a theme of your own when picked. | `background`, `keys` and `key_text` (required), `background_bottom` to fade the background, `special`, `special_text`, `accent`, all `"#rrggbb"`; `dark`; `font` (`default`, `rounded`, `serif`, `monospaced`, `avenir`, `georgia`, `futura`, `typewriter`, `copperplate`, `chalkboard`, `marker`, `script`); `weight` (`thin` to `black`); `style`, a `key_style(...)` for the finish |
| `popup_style(id, name)` | Look > Popups | `shape` (`tile`, `round`, `balloon`), `width`, `height`, `lift`, `font_size`, `corner`, `opacity`, `response`, `damping`, or `cap=` to draw the body yourself with a `cap(...)` (see Drawn keys) and `ink=` for the letter's colour or gradient |
| `entrance(id, name)` | Look > Entrance | Where the keyboard starts: `opacity`, `x`, `y`, `scale`, `tilt`, `spin`, plus `anchor` (`bottom`, `center`, `top`), `response`, `damping` |
| `press_animation(id, name)` | Look > Reactions > Geometry | A held key: `scale` or `scale_x` and `scale_y`, `x`, `y`, `rotation`, `response`, `damping` |
| `letter_animation(id, name)` | Look > Reactions > Letters | A letter at the peak of its tap: `scale` or `scale_x` and `scale_y`, `x`, `y`, `rotation`, `anchor` |
| `transition(id, name)` | Look > Transition | How far the old keys leave: `x` and `y` as a share of the keyboard, `scale`, `tilt`, `fade`, `duration` |
| `background(id, name, layers=[...], colors=[...])` | Look > Background | Up to four `particles(...)` layers: `shape` (`dot`, `glow`, `streak`, `ring`, `square`), `count`, `size`, `size_range`, `speed`, `direction` (`none`, `up`, `down`, `left`, `right`), `spread`, `gravity`, `wobble`, `life`, `twinkle`, `opacity`, `color`, `burst`, `burst_speed` |
| `trail(id, name, layers=[...], colors=[...])` | Gestures > Swipe typing | Up to four layers, painted bottom to top, and up to eight colours (`"#rrggbb"`, or `"accent"` for the theme's accent). Widths and sizes are in units of the person's trail thickness. `trail_line`: `width`, `tail_width`, `opacity`, `tail_opacity`, `color` (-1 runs all the colours along the glide), `band` (points per run through the colours), `flow` (runs per second), `dash`, `gap`, `glow`. `trail_stamps(shape)`: `shape` (`dot`, `ring`, `square`, `diamond`, `star`, `spark`, `heart`), `size`, `size_range`, `tail_size`, `spacing`, `scatter`, `spin`, `twinkle`, `opacity`, `tail_opacity`, `color`, `glow`. `trail_head(shape)`: `shape`, `size`, `pulse`, `opacity`, `color`, `glow` |
| `layout(id, name, rows=[...])` | Layout > Arrangement. Installed as a custom layout. | Rows of keys: a string is a letter, `layout_key(glyph, action=, width=)` anything else. `left=[...]` and `right=[...]` put keys beside the space bar. |

Every look also takes `icon=` for its tile. A misspelt keyword, a word outside
its list or a string where a number goes is an error in the editor console,
and numbers are held to the same ranges the app's own controls use.

### Drawn keys

A `key_style` can draw the key itself instead of choosing a built-in material.
`cap(outline=, corner=, round_up_to=, travel=, layers=[...])` is an outline and
up to sixteen layers painted on it, bottom first. The keyboard draws exactly
what is listed, and its lighting effects follow the same outline, so a new key
needs nothing but Python. [`Plugins/typewriter.py`](Plugins/typewriter.py) is
a whole typewriter key written this way.

- `outline` is `"round"` (a circle on keys up to `round_up_to` times wider
  than tall, a pill on wider ones) or `"rect"` (rounded by `corner`, or the
  theme's own radius). The outline shrinks to leave room for every layer's
  offset and blur, so shadows never spill off the key.
- `travel` is how far a pressed key's layers and its letter move down.
- A popup takes the same `cap(...)` for its body, painted against the
  theme's letter keys, and `ink=` paints its letter.
- `cap_layer(kind, paint, ...)`: `kind` is `"fill"`, `"stroke"` (a line
  `width` wide inside the outline) or `"inner"` (a stroke blurred and kept
  inside, for a lip or a dished face). `inset` shrinks the outline for this
  layer, `x` and `y` move it, `blur`, `opacity`, and `fade` (`"top"` or
  `"bottom"`) fades it toward the middle. `moves=False` keeps a layer still
  while the key goes down, and `pressed_y=` says exactly where it sits then.
  `when=` is a word or list of words that must all hold: `"pale"` or `"dark"`
  (the key's own colour), `"pressed"`, `"resting"`, `"highlighted"`.
- `paint` is a colour, `color(value, opacity)`, or the same
  `gradient("linear" | "radial", colors, stops=, start=, end=, center=,
  radius=)` key art uses. A colour is written against the key it lands on:
  `"face"`, `"text"`, `"accent"`, `"background"`, `"tint"` (the press colour),
  `"white"`, `"black"`, `"#rrggbb"` or `"#rrggbbaa"`, then optionally `*0.8`
  to darken, `+0.2` to lighten toward white, and `@0.5` for opacity. So one
  design works on light keys and dark ones, and in any theme.

### Typing

`haptics(state)` and `hitboxes(state)` return tables keyed by key name: the
letter itself (`"a"`), `"space"`, `"delete"`, `"return"`, `"shift"`,
`"globe"`, `"letters"` for any letter the table doesn't name, and `"keys"` for
anything else. A haptic is a style (`"soft"`, `"light"`, `"medium"`,
`"heavy"`, `"rigid"`, `"off"`) or `feel(style, intensity=, sharpness=)`. A
hitbox is `hitbox(scale=, x=, y=)`: `x` and `y` move the key's target by that
share of its size (half a key at most) and `scale` grows or shrinks it. Both
tables are read when the keyboard opens and once a second after that, so
nothing runs per keystroke for them. `on_touch` does run per tap, after the
tap has been handled.

`suggestions(word, state)` runs each time the suggestion bar settles, not on
every key, and its words lead the bar. `correct(word, fix, state)` runs once
per word when space ends it, even with autocorrect off, and never in a
password field. The first plugin to answer something other than `None` wins.

### Key art

`key_art(state)` draws on the keys. It returns a dict from key names (the same
ones `haptics` uses, `"letters"` and `"keys"` included) to a list of shapes,
one shape, or `art([...], animate=seconds)` to ease between changes.

`shape(kind, ...)` is the one drawing builder. `kind` is `"circle"`, `"rect"`,
`"capsule"`, `"line"`, `"path"`, `"text"` or `"icon"`. A shape sits at an
`anchor` on the key (`"center"`, `"top_right"`, `"bottom"` and so on) and `x`
and `y` move it right and down from there, in points, or in shares of the key
with `unit="key"`. `size=` or `width=`/`height=` give its box; `points=` are a
line's or a path's points across that box, 0 to 1. `text=` is the words of a
text or the SF Symbol of an icon, with `font_size=` and `weight=`.

`fill=` and `stroke=` take `"#rrggbb"`, `"#rrggbbaa"`, `"text"` or `"accent"`
(the colours of the theme the key is on), `color(value, opacity)`, or
`gradient("linear" | "radial", colors, stops=, start=, end=, center=, radius=)`.
There is also `line_width`, `corner`, `trim_from`/`trim_to` (part of an
outline, so an arc is a trimmed circle), `rotation`, `opacity`, `blur`, and
`shadow=` with one `shadow(color, radius=, x=, y=)` or a list of up to three.
A key holds sixteen shapes.

### Events

`on_event(name, info, state)` hears what happens on the keyboard: `"open"`,
`"close"`, `"word"`, `"backspace"`, `"suggestion"`, `"language"`, `"field"`,
`"shift"` (`info["state"]` is `"off"`, `"on"` or `"locked"`) and `"plane"`
(`info["plane"]`). Four more are busy, running once a key press or once a
second, so you only get them by asking: `"key_down"` and `"key_up"`
(`info["key"]`), `"key"` (`info["text"]`) and `"tick"`. `events(state)` returns
the names you want; leave it out and you hear everything but the busy four.

The keyboard asks `key_art` again after every event you hear, so a drawing
reacts by changing `state` in `on_event` and drawing from it. `context()` also
has `"shift"` and `"plane"`, for reading where things stand when you open.
Caps Lock Light is the worked example: four circles, lit from the `shift`
event. Light a dot on whichever key is down, put a counter on space, underline
return in a search field: same two hooks.

### Top bar

`bar_items(state)` offers things someone can place in the bar above the keys,
from Layout > Top bar (a Pro feature). `bar_button(id, name, icon=, title=)` is
a tap target: `icon` is an SF Symbol and `title` is up to 12 characters drawn
beside it. `bar_knob(id, name, icon=, min=, max=, step=, value=, setting=, art=, rotor=)` is
a dial you drag up or right to turn up. A tap, or a knob let go, calls
`on_action(id, value, state)`: `value` is `None` for a button and the number
for a knob. Give a knob `setting=` (any number control, like `"sound.volume"`)
and it reads and writes that setting itself, with its range, so `min`, `max`,
`step` and `value` aren't needed; each step also plays a key click at the new
level. Without `setting=` the knob shows `value` and the plugin keeps it in its
state. Whoever places a knob picks how it's drawn in the builder: its authored
artwork, a ring, or one of the built-in finishes. `bar_items` is read when the
keyboard opens and again on the tick, so keep it as cheap as `draw`.

### Flicks

`on_swipe` gets a drag that starts on a letter and travels more than a key or
so. Its angle decides the direction: a 60 degree cone each for `"left"`,
`"right"` and `"up"`, and the 30 degrees between up and either side for
`"up_left"` and `"up_right"`. Anything leaning downward is never a flick,
since down is the quick accent. Swipe typing reads the same drags as words,
so flicks only arrive while swipe typing is off; a plugin built on them should
turn it off with `set_setting("gestures.swipe", False)` and put the person's
own value back when it's switched off. Predictive Flick owns upward flicks on
the keys showing its words, so a plugin that uses `"up"` should turn
`gestures.predictive_flick` off the same way. The space bar, delete, the
number and symbol pages and a custom key's own swipe faces keep their
gestures.

`pick_suggestion` goes by what is on screen. With scrollable suggestions it
takes the chip under that third of the bar wherever the bar is scrolled, and
a third with no chip in it picks nothing. Inside `on_swipe` it picks from the
bar as it was when the finger landed, before the flick's own letter changed
it.

The finger that starts a flick types its letter when it lands, like any tap.
If a plugin asks for anything in `on_swipe`, the keyboard takes that letter
back out and then runs what was asked for, so `delete_word()` removes the word
you were typing rather than a stray letter. If no plugin asks for anything, the
flick stays an ordinary keystroke. That is how a plugin with its switch off
stays out of the way: return `state` without calling anything. The letter is
still in `context()` while the hook runs.

The full reference is at [clinkkeys.app/docs/plugins](https://clinkkeys.app/docs/plugins/).

## Make your first plugin

1. Fork this repository.
2. Copy a file in [`Plugins/`](Plugins), rename it (the name is the id), and change the `name`, `summary` and `version` in its header.
3. Run `python3 tools/build-manifest.py`. It packs your plugin into `build/<id>.clinkplugin`, or says which header line is wrong.
4. Test it in Clink by importing that file before publishing. The in-app editor has a preview that fires each hook.
5. Push to `main`. GitHub Actions publishes the plugins and manifest to the `latest` release.

## Add your repository to Clink

Open **General > Repositories** in Clink and add `owner/repository`. Then open the **Plugins** tab and choose your repository. Clink asks for a separate trust decision before downloading plugin logic.

## Make a plugin with an AI agent

[`PROMPT.md`](PROMPT.md) is a ready-to-use brief for an AI coding agent. Fork the repository, open the fork in your agent, and say:

```text
Read PROMPT.md and create a plugin that [describe what it should do as you type].
```

Review and test the generated plugin before publishing; plugins require an explicit trust decision from people who install them.

## What Clink verifies

Clink accepts only public HTTPS GitHub release files from the repository you added. It verifies the manifest, SHA-256 hash, byte count, file type, and the source policy (size, line count, at least one hook, no escape hatches, imports limited to `math`, `random`, `time`, `json` and `re`) before installation.

Plugins run as you type, so adding a repository is a stronger trust decision than adding data-only packs. Only add repositories whose code and release process you trust.

## Publishing is automatic

Keep `Plugins/`, `tools/`, and `.github/workflows/` in your fork. Add or update a plugin and push to `main`. GitHub Actions refreshes the `latest` release.

### Drawing a custom top-bar knob

`bar_knob(..., art=art([...]), rotor=art([...]))` uses the key-art shape
vocabulary for a stationary body and a rotating face. Either part is optional;
use `unit="key"` for dimensions relative to the dial. A pointer drawn above
the centre rotates through a 270-degree sweep as the value changes. Clink
handles the drag, snapping, accessibility and `setting=` binding. Each part
supports up to 16 shapes. The builder defaults to the authored Custom finish
and also offers its built-in finishes. See `Plugins/typewriter.py` for a
nickel bezel and dark platen knob matching the Typewriter cap. That cap uses
`outline="rect"` without `corner=`, preserving the user's key dimensions and
rounding.
