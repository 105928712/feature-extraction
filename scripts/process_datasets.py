# process_datasets.py
# 2026 Joey Manani & Anchorfish Team
# Dataset cleaning script
#
# Cleans malicious_phish.csv (url, type) into a CSV for extract_datasets.py
# Output is sorted by type, so shuffle before splitting
# Lots of the urls in the source set were legitimate when they were marked phishing, we clean it
#
# Usage (from the repo root):
#     python -m scripts.process_datasets <malicious_phish.csv> <output.csv>

import csv
import sys

from features.utils import canonical_url, get_host, is_readable, normalise_url, psl

# map
LABELS = {
    "benign": "Legitimate",
    "phishing": "Phishing",
    "malware": "Malware",
    "defacement": "Defacement",
}
TYPE_ORDER = ["Legitimate", "Phishing", "Malware", "Defacement"] # sort it because why not

# every "phishing" row on these domains is actually legit
MISLABELLED_PHISHING_DOMAINS = ["ietf.org", "wikipedia.org"]

def is_known_mislabel(url, label):
    """Checks if a URL is a known mislabeled *phishing* URL"""
    if label != "Phishing": # only check for known mislabeled phishing URLs, we can't reliably judge a legit URL is phishing though
        return False

    domain = psl.privatesuffix(get_host(normalise_url(url)))
    if domain in MISLABELLED_PHISHING_DOMAINS:
        return True
    return False


def main():
    if len(sys.argv) != 3:
        print("Usage: python -m scripts.process_datasets <malicious_phish.csv> <output.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # count how many invalids
    dropped = {
        "unknown_label": 0,
        "unreadable_url": 0,
        "known_mislabel": 0,
        "conflicting_label": 0,
        "duplicate": 0,
    }

    # canonical urls
    labels_by_url = {}

    # Read and filter
    with open(input_file, "r", encoding="utf-8", errors="replace", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        columns = reader.fieldnames or []
        if "url" not in columns or "type" not in columns:
            raise ValueError("Input CSV must contain 'url' and 'type' columns.")
            # we will need to make this compatible with other new data sets including new conversion map (line 18)

        for row in reader:
            url = row["url"] or ""
            raw_label = (row["type"] or "").strip().lower()

            # check if the label is one of phishing, malware, defacement, benign (only this set uses them, validate anyways)
            if raw_label not in LABELS:
                dropped["unknown_label"] += 1
                continue
            label = LABELS[raw_label]

            if not is_readable(url):
                # cannot read, continue loop
                dropped["unreadable_url"] += 1
                continue

            if is_known_mislabel(url, label):
                # found one that is marked phishing but shouldnt be
                dropped["known_mislabel"] += 1
                continue

            clean_url = canonical_url(url)
            if clean_url not in labels_by_url:
                labels_by_url[clean_url] = []
            labels_by_url[clean_url].append(label)
            # it looks like: {clean_url: [label1, label2]} here
            # if a URL has multiple labels, this'll catch it btw

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
    print("Dropped:", dropped)
    print("Kept:", kept)


if __name__ == "__main__":
    main()