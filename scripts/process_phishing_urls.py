# process_phishing_urls.py
# 2026 Joey Manani & Anchorfish Team
# Dataset cleaning script
#
# Cleans "Phishing URLs.csv" (url, Type) into the same format as process_kaggle.py
#
# Usage (from the repo root):
#     python -m scripts.process_phishing_urls "<Phishing URLs.csv>" <output.csv>

import csv
import sys

from features.utils import canonical_url, is_readable

# map (this file only has one label, and the column is "Type" with a capital T)
LABELS = {
    "phishing": "Phishing",
}


def main():
    if len(sys.argv) != 3:
        print('Usage: python -m scripts.process_phishing_urls "<Phishing URLs.csv>" <output.csv>')
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    dropped = {"unknown_label": 0, "unreadable_url": 0}
    rows = []

    with open(input_file, "r", encoding="utf-8", errors="replace", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        columns = reader.fieldnames or []
        if "url" not in columns or "Type" not in columns:
            raise ValueError("Input CSV must contain 'url' and 'Type' columns.")

        for row in reader:
            raw_label = (row["Type"] or "").strip().lower()
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
