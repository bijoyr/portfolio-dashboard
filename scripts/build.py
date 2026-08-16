#!/usr/bin/env python3
"""Inject the dataset into the app template and emit index.html.

The app ships as ONE self-contained file on purpose: no bundler, no node_modules,
no build server. This script is the entire build.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
tpl_path  = ROOT / "src" / "app.html"
data_path = ROOT / "data" / "portfolio_data.json"

tpl = tpl_path.read_text(encoding="utf-8")
if "/*__DATA__*/" not in tpl:
    sys.exit("ERROR: src/app.html is missing the /*__DATA__*/ placeholder")
if not data_path.exists():
    sys.exit("ERROR: data/portfolio_data.json not found - run scripts/gen_data.py first")

data = data_path.read_text(encoding="utf-8")
json.loads(data)                      # fail loudly on malformed data
out = ROOT / "index.html"
# Encoding and newline are both explicit: Windows defaults to cp1252, and app.html
# carries the RAG glyphs, so the default would break the build. Without newline="\n"
# Windows also rewrites every line ending, so each build shows as a full-file diff.
out.write_text(tpl.replace("/*__DATA__*/", data), encoding="utf-8", newline="\n")
print(f"built {out.name}  ({out.stat().st_size/1024:.0f} KB)")
