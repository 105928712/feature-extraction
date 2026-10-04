import csv
import os



# CONFIGURATION


URL_HEADERS = [
    "url",
    "domain",
]

LABEL_HEADERS = [
    "type",
    "label",
]



# LABEL CONVERSION


BENIGN_LABELS = [
    "legitimate",
    "benign",
    "0",
]

PHISHING_LABELS = [
    "phishing",
    "malicious",
    "1",
]



# CLEAN DATASET


input_file = input("Enter the path to the CSV file: ").strip()

if not os.path.isfile(input_file):
    print("Error: File not found.")
    exit()


# Create output filename
name, extension = os.path.splitext(input_file)
output_file = name + "_cleaned" + extension



# Read CSV


try:
    with open(input_file, "r", encoding="utf-8-sig", newline="") as infile:
        reader = csv.DictReader(infile)

        if reader.fieldnames is None:
            print("Error: Could not find CSV headers.")
            exit()

        # Remove spaces and make headers lowercase
        headers = [header.strip().lower() for header in reader.fieldnames]

except UnicodeDecodeError:
    print("UTF-8 encoding failed. Trying Windows-1252...")

    with open(input_file, "r", encoding="cp1252", newline="") as infile:
        reader = csv.DictReader(infile)

        if reader.fieldnames is None:
            print("Error: Could not find CSV headers.")
            exit()

        headers = [header.strip().lower() for header in reader.fieldnames]



# FIND URL COLUMN


url_header = None

for header in headers:
    if header in URL_HEADERS:
        url_header = header
        break



# FIND LABEL COLUMN


label_header = None

for header in headers:
    if header in LABEL_HEADERS:
        label_header = header
        break


# CHECK THAT BOTH COLUMNS WERE FOUND


if url_header is None:
    print("Error: Could not find a URL/domain column.")
    print("Accepted headers:", URL_HEADERS)
    exit()

if label_header is None:
    print("Error: Could not find a type/label column.")
    print("Accepted headers:", LABEL_HEADERS)
    exit()


print("URL column found:", url_header)
print("Label column found:", label_header)



# RE-READ FILE WITH THE CORRECT ENCODING


try:
    infile = open(
        input_file,
        "r",
        encoding="utf-8-sig",
        newline=""
    )
    reader = csv.DictReader(infile)

except UnicodeDecodeError:
    infile = open(
        input_file,
        "r",
        encoding="cp1252",
        newline=""
    )
    reader = csv.DictReader(infile)



# PROCESS DATA


cleaned_rows = []

for row in reader:

    url = row.get(url_header, "").strip()
    label = row.get(label_header, "").strip().lower()

    # Convert labels to standard format
    if label in BENIGN_LABELS:
        label = "benign"

    elif label in PHISHING_LABELS:
        label = "phishing"

    else:
        print("Warning: Unknown label:", row.get(label_header))
        continue

    # Keep ONLY URL and type
    cleaned_rows.append({
        "url": url,
        "type": label
    })


infile.close()



# WRITE CLEANED CSV


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
    writer.writerows(cleaned_rows)



# FINISHED


print()
print("Cleaning complete!")
print("Original file:", input_file)
print("Cleaned file:", output_file)
print("Rows kept:", len(cleaned_rows))
