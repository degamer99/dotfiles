#!/usr/bin/env python3
import argparse
import json
import csv
import sys

def load_dictionary(csv_path):
    """
    Load CSV mapping words to meanings into a dict.
    Expects CSV lines like: "word","meaning"
    """
    d = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                word = row[0].strip()
                meaning = row[1].strip()
                d[word] = meaning
    return d

def pair_word_lists(nested_words, dictionary):
    """
    Given nested list of words, return nested list of [word, meaning] pairs.
    If a word not found, meaning is set to None.
    """
    paired = []
    for sublist in nested_words:
        paired_sub = []
        for w in sublist:
            mean = dictionary.get(w, None)
            paired_sub.append([w, mean])
        paired.append(paired_sub)
    return paired

def main():
    parser = argparse.ArgumentParser(
        description="Pair each word in input JSON with meanings from CSV."
    )
    parser.add_argument('--json', '-j', required=True,
                        help="Path to input JSON file containing nested word lists.")
    parser.add_argument('--csv', '-c', required=True,
                        help="Path to CSV file mapping words to meanings.")
    parser.add_argument('--output', '-o', default='output.json',
                        help="Output JSON filename (default: output.json)")
    args = parser.parse_args()

    # Load input JSON
    try:
        with open(args.json, 'r', encoding='utf-8') as jf:
            nested = json.load(jf)
    except FileNotFoundError:
        print(f"Error: JSON file '{args.json}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Load CSV dictionary
    try:
        dictionary = load_dictionary(args.csv)
    except FileNotFoundError:
        print(f"Error: CSV file '{args.csv}' not found.", file=sys.stderr)
        sys.exit(1)

    # Pair words with meanings
    paired = pair_word_lists(nested, dictionary)

    # Write output JSON
    with open(args.output, 'w', encoding='utf-8') as out:
        json.dump(paired, out, ensure_ascii=False, indent=2)

    # Also print to console
    print(json.dumps(paired, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

