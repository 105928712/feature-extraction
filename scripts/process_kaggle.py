# process_kaggle.py
# 2026 Joey Manani & Anchorfish Team
# Dataset cleaning script
#
# Cleans malicious_phish.csv (url, type) into a CSV for extract_features.py
# Output is sorted by type, so shuffle before splitting
# Turns out some blocks at the end of the file have their labels swapped, we flip them back (see below)
#
# Usage (from the repo root):
#     python -m scripts.process_kaggle <malicious_phish.csv> <output.csv>

import csv
import sys

from features.utils import canonical_url, is_readable

# map
LABELS = {
    "benign": "Legitimate",
    "phishing": "Phishing",
    "malware": "Malware",
    "defacement": "Defacement",
}
TYPE_ORDER = ["Legitimate", "Phishing", "Malware", "Defacement"] # sort it because why not

# The Kaggle file is shuffled up to row 520,330

# The last two blocks have their labels swapped so flip them back by POSITION, not by label:
# rows 555,186 - 603,181 say benign but are phishing (paypal, wp-content logins, battle.net)
# rows 603,182 - 651,190 say phishing but are legit (w3.org, gnu.org, ibm.com, every IETF RFC, Wikipedia)
TOTAL_ROW_COUNT = 651191
ACTUALLY_PHISHING = range(555186, 603182)
ACTUALLY_LEGITIMATE = range(603182, 651191)


def main():
    if len(sys.argv) != 3:
        print("Usage: python -m scripts.process_kaggle <malicious_phish.csv> <output.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # count how many invalids
    dropped = {
        "unknown_label": 0,
        "unreadable_url": 0,
        "conflicting_label": 0,
        "duplicate": 0,
    }
    relabelled = {
        "Legitimate -> Phishing": 0,
        "Phishing -> Legitimate": 0,
    }
    rows_read = 0

    # canonical urls
    labels_by_url = {}

    # Read and filter
    with open(input_file, "r", encoding="utf-8", errors="replace", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        columns = reader.fieldnames or []
        if "url" not in columns or "type" not in columns:
            raise ValueError("Input CSV must contain 'url' and 'type' columns.")
            # we will need to make this compatible with other new data sets including new conversion map (line 18)

        for row_number, row in enumerate(reader):
            rows_read += 1
            url = row["url"] or ""
            raw_label = (row["type"] or "").strip().lower()

            # check if the label is one of phishing, malware, defacement, benign (only this set uses them, validate anyways)
            if raw_label not in LABELS:
                dropped["unknown_label"] += 1
                continue
            label = LABELS[raw_label]

            # flip the swapped blocks back (the 92 real phishing rows inside the first block are left as they are)
            if row_number in ACTUALLY_PHISHING and label == "Legitimate":
                label = "Phishing"
                relabelled["Legitimate -> Phishing"] += 1
            elif row_number in ACTUALLY_LEGITIMATE and label == "Phishing":
                label = "Legitimate"
                relabelled["Phishing -> Legitimate"] += 1

            clean_url = canonical_url(url)
            if not is_readable(clean_url):
                # cannot read, continue loop
                dropped["unreadable_url"] += 1
                continue
            if clean_url not in labels_by_url:
                labels_by_url[clean_url] = []
            labels_by_url[clean_url].append(label)
            # it looks like: {clean_url: [label1, label2]} here
            # if a URL has multiple labels, this'll catch it btw

    # the row numbers above only line up with the original Kaggle file
    # checks for errors that might mangle out
    if rows_read != TOTAL_ROW_COUNT:
        raise ValueError(f"Expected the Kaggle malicious_phish.csv ({TOTAL_ROW_COUNT} rows) but read {rows_read} rows. "
                         "The swapped-block fix only works on that exact file.")

    # remove duplicates and conflicting labels
    rows = []
    for url in labels_by_url:
        labels = labels_by_url[url]
        first_label = labels[0] # compare every label against this one; if any differ, the url is dropped

        conflict = False
        for label in labels:
            if label != first_label:
                conflict = True
                # has >1 uh oh

        if conflict:
            dropped["conflicting_label"] += len(labels)
        else:
            rows.append({"url": url, "type": first_label})
            dropped["duplicate"] += len(labels) - 1 # so we are just keeping the first result we found, the rest are dropped here removing dupes

    # sort by type
    sorted_rows = []
    for type_name in TYPE_ORDER:
        for row in rows: # slow sort who cares
            if row["type"] == type_name:
                sorted_rows.append(row)

    # Write output
    with open(output_file, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["url", "type"])
        writer.writeheader()
        writer.writerows(sorted_rows)

    # Count what we kept
    kept = {}
    for type_name in TYPE_ORDER:
        kept[type_name] = 0
    for row in sorted_rows:
        kept[row["type"]] += 1

    # worth quoting in the report's Data Processing section
    print("Wrote", len(sorted_rows), "rows to", output_file)
    print("Relabelled:", relabelled)
    print("Dropped:", dropped)
    print("Kept:", kept)


if __name__ == "__main__":
    main()