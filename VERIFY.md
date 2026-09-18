# Verify this Clink plugins repository

Read `README.md`, `PROMPT.md`, each `Plugins/*.clinkplugin`, and `tools/build-manifest.py`. Audit without changing files unless asked to remediate a finding.

Parse every plugin JSON, then run:

```sh
python3 tools/build-manifest.py
```

Verify each plugin has a unique stable `id`, visible `name`, valid SF Symbol `icon`, concise `summary`, a `version`, an `enabled` state, and a `source` string defining at least one of the hooks (`initial`, `settings`, `on_action`, `on_open`, `on_close`, `on_key`, `on_word`, `on_backspace`, `on_suggestion`, `on_language`, `on_field`, `on_tick`, `on_swipe`, `elements`, `draw`). Inspect the source against the existing plugins. It must be small, offline and deterministic; it must import nothing beyond `math`, `random`, `time`, `json` and `re`, and must not use `open`, `eval`, `exec`, `compile` or double-underscore names. A plugin that calls `claim(...)` must call `release(...)` on the matching off path. Every id passed to `setting`, `set_setting`, `claim` or `release` must be a real control id, and a plugin that turns a setting off for a while must restore the person's previous value, not a hard-coded one. An `on_key` hook must do very little work, and so must `on_tick` and `draw`, which run about once a second on their own. A plugin that defines `on_swipe` must call nothing on the paths where it is switched off, must only pass `"space"` or `"delete"` to `press` and `"left"`, `"center"` or `"right"` to `pick_suggestion`, and if it turns swipe typing or Predictive Flick off it must restore the person's previous value. A plugin that defines `elements` must also define `draw`, and every id it offers must be one `draw` answers.

Confirm the regenerated `manifest.json` represents exactly the plugin files and check that release workflows and source-policy protections have not been weakened. Report commands, pass/fail status for every plugin, manifest status, and exact paths plus fixes for any finding. Never claim runtime testing unless it was actually done in Clink.
