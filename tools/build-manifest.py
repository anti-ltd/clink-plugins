#!/usr/bin/env python3
import hashlib, json, os, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
repo = os.environ.get("GITHUB_REPOSITORY", "anti-ltd/clink-plugins")
plugins = []
for path in sorted(p for p in (root / "Plugins").glob("*.clinkplugin") if not p.name.startswith("._")):
    data = path.read_bytes(); plugin = json.loads(data)
    plugins.append({"id": path.stem, "name": plugin["name"], "version": plugin.get("version", "latest"), "icon": plugin.get("icon", ""), "summary": plugin.get("summary", ""), "asset": {"path": path.name, "url": f"https://github.com/{repo}/releases/download/latest/{path.name}", "sha256": hashlib.sha256(data).hexdigest(), "byteCount": len(data)}})
(root / "manifest.json").write_text(json.dumps({"version": "latest", "plugins": plugins}, indent=2) + "\n")
