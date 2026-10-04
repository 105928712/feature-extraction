import csv
import os
#asks for file path on pc(just use downloads its easier) accepts file, creates new file in same path WITH HOPEFULLY CHANGED STUFF 🤑🤑🤑🤑
input_file = input("Enter the path to the CSV file: ").strip()

if not os.path.isfile(input_file):
    print("Error: File not found.")
    exit()

name, extension = os.path.splitext(input_file)
output_file = name + "_converted" + extension

with open(input_file, "r", encoding="utf-8-sig", newline="") as infile:
    reader = csv.DictReader(infile)

    # Check that the required columns exist
    if "url" not in reader.fieldnames or "type" not in reader.fieldnames:
        print("Error: CSV must contain 'url' and 'type' columns.")
        exit()

    rows = list(reader)

# Only change values in the "type" column
for row in rows:
    label = row["type"].strip().lower()

    if label == "legitimate":
        row["type"] = "benign"
    elif label == "phishing":
        row["type"] = "phishing"

# Write the converted CSV
with open(output_file, "w", encoding="utf-8", newline="") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Conversion complete!")
print("Output file:", output_file)


