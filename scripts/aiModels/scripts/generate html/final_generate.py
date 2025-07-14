#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="light" data-dir="ltr">
<head>
  <meta charset="UTF-8">
  <title>Flashcards</title>
  <style>
    /* 1. CSS Custom Properties & Themes */
    :root {{
      --bg: #f8f9fa;          /* page background */
      --fg: #333;             /* text color */
      --card-bg: #fff;        /* word card bg */
      --card-fg: #000;        /* word card text */
      --accent: #2b7a78;      /* accent color */
      --flow: row;            /* flex flow (ltr) */
      --font-main: Arial, sans-serif;
    }}
    [data-theme="dark"] {{
      --bg: #121212; --fg: #ddd;
      --card-bg: #1e1e1e; --card-fg: #fff;
      --accent: #66d9ef;
    }}
    [data-dir="rtl"] {{
      --flow: row-reverse;    /* reverse flex order for RTL */
    }}

    /* 2. Global Styles */
    body {{
      margin:0; padding:1em;
      font-family: var(--font-main);
      background: var(--bg);
      color: var(--fg);
    }}
    header {{
      display:flex; gap:1em; align-items:center;
      margin-bottom:1em; 
    }}
    header label {{ font-weight:bold; }}

    /* 3. Flashcard Layout */
    .line-block {{ margin-bottom:2em; }}
    .foreign-line, .english-line {{ margin:0.5em 0; font-size:1.1em; }}
    .word-row {{
      display:flex; flex-wrap:wrap; gap:1em;
      justify-content:center;
      flex-direction: var(--flow);      /* <-- uses custom property */ 
    }}
    .word-pair {{
      background: var(--card-bg);
      color: var(--card-fg);
      border:1px solid var(--accent);
      border-radius:4px;
      padding:0.5em;
      min-width:6rem;
      text-align:center;
    }}
    .foreign-word {{ font-weight:bold; color:var(--accent); }}
    .translation {{ font-style:italic; color:var(--fg); }}
  </style>
</head>
<body>
  <header>
    <label for="theme-select">Theme:</label>
    <select id="theme-select">
      <option value="light">Light</option>
      <option value="dark">Dark</option>
    </select>

    <label for="dir-select">Direction:</label>
    <select id="dir-select">
      <option value="ltr">LTR</option>
      <option value="rtl">RTL</option>
    </select>
  </header>

  {content}

  <script>
  (function() {{
    const html = document.documentElement;
    const themeSelect = document.getElementById('theme-select');
    const dirSelect   = document.getElementById('dir-select');

    // Initialize from localStorage or system prefs :contentReference[oaicite:4]{{index=4}} :contentReference[oaicite:5]{{index=5}}
    const storedTheme = localStorage.getItem('flash_theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initTheme = storedTheme || (prefersDark ? 'dark' : 'light');
    html.setAttribute('data-theme', initTheme);
    themeSelect.value = initTheme;

    const storedDir = localStorage.getItem('flash_dir') || 'ltr';
    html.setAttribute('data-dir', storedDir);
    dirSelect.value = storedDir;

    // Event listeners to save changes :contentReference[oaicite:6]{{index=6}}
    themeSelect.addEventListener('change', e => {{
      html.setAttribute('data-theme', e.target.value);
      localStorage.setItem('flash_theme', e.target.value);
    }});
    dirSelect.addEventListener('change', e => {{
      html.setAttribute('data-dir', e.target.value);
      localStorage.setItem('flash_dir', e.target.value);
    }});
  }})();
  </script>
</body>
</html>
"""

def read_lines(path):
    with open(path, encoding='utf-8') as f:
        return [ln.strip() for ln in f if ln.strip()]

def main():
    p = argparse.ArgumentParser(description="Generate themed, RTL/LTR flashcards.")
    p.add_argument('-f','--foreign', required=True, help="Foreign text file")
    p.add_argument('-e','--english', required=True, help="English text file")
    p.add_argument('-p','--pairs',   required=True, help="JSON of word-meaning pairs")
    p.add_argument('-o','--output',  default='flashcards.html', help="Output HTML filename")
    args = p.parse_args()

    foreign = read_lines(args.foreign)
    english = read_lines(args.english)
    try:
        pairs = json.load(open(args.pairs, encoding='utf-8'))
    except Exception as err:
        print(f"Error loading JSON: {err}", file=sys.stderr)
        sys.exit(1)

    n = len(foreign)
    if len(english)!=n or len(pairs)!=n:
        print("Line-count mismatch", file=sys.stderr)
        sys.exit(1)

    blocks = []
    for fl, el, wp in zip(foreign, english, pairs):
        items = ''.join(f"""
      <div class="word-pair">
        <div class="foreign-word">{w}</div>
        <div class="translation">{m or ''}</div>
      </div>""" for w,m in wp)
        blocks.append(f"""
  <div class="line-block">
    <p class="foreign-line">{fl}</p>
    <div class="word-row">{items}
    </div>
    <p class="english-line">{el}</p>
  </div>""")

    html = HTML_TEMPLATE.format(content="\n".join(blocks))
    Path(args.output).write_text(html, encoding='utf-8')
    print(f"Wrote {args.output}")

if __name__=='__main__':
    main()

