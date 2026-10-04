import csv
import os


# CONFIGURATION
# Add new possible headers here when needed

URL_HEADERS = [
    "url",
    "domain",
]

LABEL_HEADERS = [
    "type",
    "label",
]


BENIGN_LABELS = [
    "legitimate",
    "benign",
    "safe",
    "0",
]

PHISHING_LABELS = [
    "phishing",
    "malicious",
    "dangerous",
    "1",
]


# FIND A HEADER


def find_header(headers, accepted_headers):

    for header in headers:
        if header.strip().lower() in accepted_headers:
            return header

    return None


# CLEAN ONE CSV

def clean_csv(input_file):

    # Try UTF-8 first
    try:
        infile = open(
            input_file,
            "r",
            encoding="utf-8-sig",
            newline=""
        )
        reader = csv.DictReader(infile)

        headers = reader.fieldnames

    except UnicodeDecodeError:
        infile = open(
            input_file,
            "r",
            encoding="cp1252",
            newline=""
        )
        reader = csv.DictReader(infile)

        headers = reader.fieldnames


    if headers is None:
        print("ERROR: No headers found in:", input_file)
        infile.close()
        return []


    # Find URL and label columns
    url_header = find_header(headers, URL_HEADERS)
    label_header = find_header(headers, LABEL_HEADERS)


    if url_header is None:
        print("ERROR: No URL/domain column found in:", input_file)
        infile.close()
        return []


    if label_header is None:
        print("ERROR: No type/label column found in:", input_file)
        infile.close()
        return []


    print("Processing:", input_file)
    print("  URL column:", url_header)
    print("  Label column:", label_header)


    cleaned_rows = []


    for row in reader:

        url = row.get(url_header, "").strip()
        label = row.get(label_header, "").strip().lower()


        # Convert labels
        if label in BENIGN_LABELS:
            label = "benign"

        elif label in PHISHING_LABELS:
            label = "phishing"

        else:
            print("  WARNING: Unknown label:", label)
            continue


        # Ignore empty URLs
        if url == "":
            continue


        # Only keep the standard columns
        cleaned_rows.append({
            "url": url,
            "type": label
        })


    infile.close()

    print("  Rows kept:", len(cleaned_rows))
    print()

    return cleaned_rows


# MAIN PROGRAM

print("======================================")
print(" URL DATASET CLEANER AND MERGER")
print("======================================")
print()


# Ask how many files
number_of_files = int(
    input("How many CSV files do you want to merge? ")
)


all_rows = []


# Get each CSV
for i in range(number_of_files):

    print()
    file_path = input(
        f"Enter path for CSV {i + 1}: "
    ).strip()

    if not os.path.isfile(file_path):
        print("ERROR: File not found:", file_path)
        continue

    rows = clean_csv(file_path)

    all_rows.extend(rows)



# WRITE MERGED DATASET

output_file = input(
    "Enter the name for the merged CSV "
    "(example: merged_dataset.csv): "
).strip()


with open(
    output_file,
    "w",
    encoding="utf-8",
    newline=""
) as outfile:

    writer = csv.DictWriter(
        outfile,
        fieldnames=["url", "type"]
    )

    writer.writeheader()
    writer.writerows(all_rows)


# SUMMARY

benign_count = 0
phishing_count = 0


for row in all_rows:

    if row["type"] == "benign":
        benign_count += 1

    elif row["type"] == "phishing":
        phishing_count += 1


print()
print("======================================")
print(" MERGE COMPLETE")
print("======================================")
print("Total rows:", len(all_rows))
print("Benign:", benign_count)
print("Phishing:", phishing_count)
print("Output:", output_file)
