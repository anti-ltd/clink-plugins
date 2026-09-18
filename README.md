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
| Flick Gestures | Flick left anywhere on the letters to delete a word, right for a space. Its switch sits under Gestures > Swipe typing, and it turns swipe typing off while it's on. |

The files live in [`Plugins/`](Plugins). Each one is a small JSON file with the script inside, readable in one sitting. A plugin that offers a layout element is added from Layout > Arrange > Element in the app, not from a settings screen.

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
| `on_swipe(direction, state)` | A sideways flick that started on a letter key, `"left"` or `"right"`. Only while swipe typing is off. |
| `elements(state)` | What this plugin offers a custom layout. Return `element(id, name, icon=, width=, options=)` entries. |
| `draw(id, state)` | One element's face, as a node tree. `sparkline(values, min=, max=, fill=)` is the node built for a key. |
| `draw(id, options, state)` | The same, for an element with options: `options` holds what was picked on that key. |

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
- `stats()` for the live typing rate and totals.

In the app, Home > More > Developer lists every id with what it accepts, and Show ids badges each settings card with the anchor `section(...)` takes.

### Flicks

`on_swipe` gets a drag across the letters that is clearly sideways and longer
than a key or so. Swipe typing reads the same drag as a word, so flicks only
arrive while swipe typing is off; a plugin built on them should turn it off
with `set_setting("gestures.swipe", False)` and put the person's own value back
when it's switched off. The drag has to start on a letter: the space bar,
delete, the number and symbol pages and a custom key's own swipe faces keep
their gestures.

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
2. Copy a file in [`Plugins/`](Plugins), rename it, and change its `id`, `name`, `summary` and `version`.
3. Test it in Clink by importing the file before publishing. The in-app editor has a preview that fires each hook.
4. Run `python3 tools/build-manifest.py`.
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
