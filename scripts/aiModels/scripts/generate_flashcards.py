#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Flashcards</title>
<style>
  body {{ font-family: sans-serif; padding: 1em; }}
  .line-block {{ margin-bottom: 2em; }}
  .foreign-line, .english-line {{ margin: 0.5em 0; font-size: 1.1em; }}
  .word-row {{ display: flex; flex-wrap: wrap; gap: 1em; margin: 0.5em 0 1em; }}
  .word-pair {{
    display: flex; flex-direction: column;
    border: 1px solid #ccc; padding: 0.5em; border-radius: 4px;
    min-width: 5em; text-align: center;
  }}
  .foreign-word {{ font-weight: bold; }}
  .translation {{ color: #555; font-size: 0.9em; }}
</style>
</head>
<body>
<h1>Flashcards</h1>
{content}
</body>
</html>"""

def read_lines(path):
    """Read UTF-8 lines, strip, drop blanks."""
    with open(path, encoding='utf-8') as f:
        return [ln.strip() for ln in f if ln.strip()]

def main():
    p = argparse.ArgumentParser(description="Generate flashcard HTML from text + JSON pairs.")
    p.add_argument('--foreign', '-f', required=True, help="Foreign language text file")
    p.add_argument('--english', '-e', required=True, help="English translation text file")
    p.add_argument('--pairs',   '-p', required=True, help="JSON file with nested word-meaning pairs")
    p.add_argument('--output',  '-o', default='flashcards.html', help="Output HTML file")
    args = p.parse_args()

    foreign_lines = read_lines(args.foreign)
    english_lines = read_lines(args.english)

    # Load JSON
    try:
        with open(args.pairs, encoding='utf-8') as jf:
            pairs = json.load(jf)
    except Exception as err:
        print(f"Error loading JSON '{args.pairs}': {err}", file=sys.stderr)
        sys.exit(1)

    n = len(foreign_lines)
    if len(english_lines) != n or len(pairs) != n:
        print("Error: line-count mismatch among inputs:", file=sys.stderr)
        print(f"  foreign lines: {n}", file=sys.stderr)
        print(f"  english lines: {len(english_lines)}", file=sys.stderr)
        print(f"  JSON groups:    {len(pairs)}", file=sys.stderr)
        sys.exit(1)

    # Build HTML blocks
    blocks = []
    for i in range(n):
        fl = foreign_lines[i]
        el = english_lines[i]
        wp = pairs[i]
        row_items = []
        for word, meaning in wp:
            row_items.append(f"""
      <div class="word-pair">
        <div class="foreign-word">{word}</div>
        <div class="translation">{meaning if meaning is not None else ''}</div>
      </div>""")
        blocks.append(f"""
  <div class="line-block">
    <p class="foreign-line">{fl}</p>
    <div class="word-row">{''.join(row_items)}
    </div>
    <p class="english-line">{el}</p>
  </div>""")

    content = "\n".join(blocks)
    html = HTML_TEMPLATE.format(content=content)

    # Write output
    outpath = Path(args.output)
    outpath.write_text(html, encoding='utf-8')
    print(f"Wrote flashcards to {outpath}")

if __name__ == '__main__':
    main()

