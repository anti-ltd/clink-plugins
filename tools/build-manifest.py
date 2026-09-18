#!/usr/bin/env python3
"""Packs Plugins/ into release files and writes manifest.json.

A plugin is written as a plain Python file, Plugins/<id>.py, that starts with
a header between two "# ---" lines:

    # ---
    # name: Clock
    # icon: clock
    # summary: The time on a key, for a custom layout
    # version: 1.1
    # author: Clink
    # ---

Everything after the header is the plugin's source. This script turns each one
into build/<id>.clinkplugin, the JSON file Clink downloads and imports. A
ready-made .clinkplugin dropped into Plugins/ is copied across unchanged.
"""
import hashlib, json, os, pathlib, sys

root = pathlib.Path(__file__).resolve().parents[1]
repo = os.environ.get("GITHUB_REPOSITORY", "anti-ltd/clink-plugins")
fields = ["name", "icon", "summary", "version", "author", "enabled"]


def fail(path, message):
    sys.exit(f"{path.relative_to(root)}: {message}")


def pack(path):
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "# ---":
        fail(path, 'must start with a "# ---" header')
    meta, end = {}, None
    for number, line in enumerate(lines[1:], start=1):
        text = line.strip()
        if text == "# ---":
            end = number
            break
        if not text.startswith("#") or ":" not in text:
            fail(path, f"line {number + 1} in the header should look like '# key: value'")
        key, value = text[1:].split(":", 1)
        key, value = key.strip(), value.strip()
        if key not in fields:
            fail(path, f"unknown header key '{key}' (use {', '.join(fields)})")
        meta[key] = value
    if end is None:
        fail(path, 'the header has no closing "# ---"')
    if "name" not in meta:
        fail(path, "the header needs a name")
    source = "".join(lines[end + 1:]).lstrip("\n")
    plugin = {
        "id": path.stem,
        "name": meta["name"],
        "icon": meta.get("icon", "puzzlepiece"),
        "summary": meta.get("summary", ""),
        "version": meta.get("version", "1.0"),
        "author": meta.get("author", ""),
        "enabled": meta.get("enabled", "true").lower() != "false",
        "source": source,
    }
    return (json.dumps(plugin, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


build = root / "build"
build.mkdir(exist_ok=True)
for old in build.iterdir():
    old.unlink(missing_ok=True)

files = [p for p in (root / "Plugins").iterdir() if not p.name.startswith("._")]
seen = {}
for path in sorted(files):
    if path.suffix == ".py":
        data = pack(path)
    elif path.suffix == ".clinkplugin":
        data = path.read_bytes()
    else:
        continue
    if path.stem in seen:
        fail(path, f"clashes with {seen[path.stem]}")
    seen[path.stem] = path.name
    (build / f"{path.stem}.clinkplugin").write_bytes(data)

plugins = []
for path in sorted(p for p in build.glob("*.clinkplugin") if not p.name.startswith("._")):
    data = path.read_bytes(); plugin = json.loads(data)
    plugins.append({"id": path.stem, "name": plugin["name"], "version": plugin.get("version", "latest"), "icon": plugin.get("icon", ""), "summary": plugin.get("summary", ""), "asset": {"path": path.name, "url": f"https://github.com/{repo}/releases/download/latest/{path.name}", "sha256": hashlib.sha256(data).hexdigest(), "byteCount": len(data)}})
(root / "manifest.json").write_text(json.dumps({"version": "latest", "plugins": plugins}, indent=2) + "\n")
print(f"Packed {len(plugins)} plugins into build/")
