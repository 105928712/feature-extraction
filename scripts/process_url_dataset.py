# process_url_dataset.py
# 2026 Joey Manani & Anchorfish Team
# Dataset cleaning script
#
# Cleans "URL dataset.csv" (url, type) into the same format as process_kaggle.py outputs
#
# Usage (from the repo root):
#     python -m scripts.process_url_dataset "<URL dataset.csv>" <output.csv>

import csv
import sys

from features.utils import canonical_url, is_readable

# map
LABELS = {
    "legitimate": "Legitimate",
    "phishing": "Phishing",
}


def main():
    if len(sys.argv) != 3:
        print('Usage: python -m scripts.process_url_dataset "<URL dataset.csv>" <output.csv>')
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    dropped = {"unknown_label": 0, "unreadable_url": 0}
    rows = []

    with open(input_file, "r", encoding="utf-8", errors="replace", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        columns = reader.fieldnames or []
        if "url" not in columns or "type" not in columns:
            raise ValueError("Input CSV must contain 'url' and 'type' columns.")

        for row in reader:
            raw_label = (row["type"] or "").strip().lower()
            if raw_label not in LABELS:
                dropped["unknown_label"] += 1
                continue

            clean_url = canonical_url(row["url"] or "")
            if not is_readable(clean_url):
                dropped["unreadable_url"] += 1
                continue

            rows.append({"url": clean_url, "type": LABELS[raw_label]})

    with open(output_file, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["url", "type"])
        writer.writeheader()
        writer.writerows(rows)

    print("Wrote", len(rows), "rows to", output_file)
    print("Dropped:", dropped)


if __name__ == "__main__":
    main()
