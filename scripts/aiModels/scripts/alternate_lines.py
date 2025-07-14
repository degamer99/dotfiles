#!/usr/bin/env python3
import sys

def read_and_filter(path):
    """
    Reads all lines from 'path', strips trailing newlines,
    and returns a list with all non-empty lines.
    """
    with open(path, 'r', encoding='utf-8') as f:
        # Read and strip whitespace, filter out blank lines
        return [line.rstrip('\n') for line in f if line.strip()]

def alternate(list1, list2):
    """
    Yields lines alternately from list1 and list2.
    When one list is exhausted, yields the remainder of the other.
    """
    i, j = 0, 0
    len1, len2 = len(list1), len(list2)
    # Continue while either list has remaining items
    while i < len1 or j < len2:
        if i < len1:
            yield list1[i]
            i += 1
        if j < len2:
            yield list2[j]
            j += 1

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file1.txt> <file2.txt>", file=sys.stderr)
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]

    # Read and filter both files
    lines1 = read_and_filter(file1)  # :contentReference[oaicite:0]{index=0}
    lines2 = read_and_filter(file2)  # :contentReference[oaicite:1]{index=1}

    # Alternate and collect results
    result = list(alternate(lines1, lines2))  # :contentReference[oaicite:2]{index=2}

    # Print to console
    for line in result:
        print(line)

    # Write to output.txt
    with open('output.txt', 'w', encoding='utf-8') as out:
        out.write('\n'.join(result))

if __name__ == "__main__":
    main()

