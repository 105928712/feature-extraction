# merge_datasets.py
# 2026 Joey Manani & Anchorfish Team
#
# Labels are not touched, each process script already fixed its own labelling
# Same URL from two sources with the same label -> keep one; dedupe
# Same URL with different labels: drop it. Don't know whats right
#
# Usage (from the repo root):
#     python -m scripts.merge_datasets <output.csv> <cleaned1.csv> <cleaned2.csv> ...

import csv
import sys


def merge(rows):
    """rows: (url, type) pairs. Returns (kept rows, duplicates dropped, conflicting rows dropped)"""
    labels_by_url = {}  # dicts keep insertion order, so the output follows the input
    for url, label in rows:
        if url not in labels_by_url:
            labels_by_url[url] = []
        labels_by_url[url].append(label)

    kept = []
    duplicates = 0
    conflicts = 0
    for url in labels_by_url:
        labels = labels_by_url[url]
        if len(set(labels)) > 1:
            conflicts += len(labels)
        else:
            kept.append({"url": url, "type": labels[0]})
            duplicates += len(labels) - 1
    return kept, duplicates, conflicts


def read_rows(input_file):
    with open(input_file, "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames != ["url", "type"]:
            raise ValueError(f"{input_file} should have exactly 'url,type' columns, run its process script first.")
        count = 0
        for row in reader:
            count += 1
            yield row["url"], row["type"]
    print("Read", count, "rows from", input_file)


def main():
    if len(sys.argv) < 4:
        print("Usage: python -m scripts.merge_datasets <output.csv> <cleaned1.csv> <cleaned2.csv> ...")
        sys.exit(1)

    output_file = sys.argv[1]
    input_files = sys.argv[2:]

    all_rows = []
    for input_file in input_files:
        all_rows.extend(read_rows(input_file))

    kept, duplicates, conflicts = merge(all_rows)

    with open(output_file, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["url", "type"])
        writer.writeheader()
        writer.writerows(kept)

    counts = {}
    for row in kept:
        counts[row["type"]] = counts.get(row["type"], 0) + 1

    # worth quoting in the report's Data Processing section
    print("Wrote", len(kept), "rows to", output_file)
    print("Dropped:", {"duplicate": duplicates, "conflicting_label": conflicts})
    print("Kept:", counts)


if __name__ == "__main__":
    main()
