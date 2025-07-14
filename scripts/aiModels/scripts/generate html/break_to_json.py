#!/usr/bin/env python3
import sys
import json

def read_and_filter(filepath):
    """
    Read lines from filepath (UTF-8), strip newline and whitespace,
    remove blank lines, then remove '.' and ',' from each line.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        cleaned = []
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            # Remove periods and commas
            line = line.replace('.', '').replace(',', '')  # :contentReference[oaicite:2]{index=2}
            cleaned.append(line)
        return cleaned

def split_to_words(lines):
    """
    Given a list of cleaned lines, split each on whitespace.
    Returns a list of word-lists.
    """
    return [line.split() for line in lines]

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input_file.txt>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        lines = read_and_filter(input_file)
    except FileNotFoundError:
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    word_lists = split_to_words(lines)

    # Print JavaScript-style array to console
    print(json.dumps(word_lists, ensure_ascii=False, indent=2))  # :contentReference[oaicite:3]{index=3}

    # Write out as JSON
    with open('output.json', 'w', encoding='utf-8') as out:
        json.dump(word_lists, out, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()

