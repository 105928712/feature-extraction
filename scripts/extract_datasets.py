# extract_dataset.py
# 2026 Joey Manani & Anchorfish Team
# Dataset feature extraction script

"""
Reads a CSV dataset containing URLs and their classifications,
runs the feature extraction system on each URL, and saves the
results to a new CSV file.

Expected input columns:
- url
- type

The output CSV contains:
- url
- type
- all extracted URL features
"""

import csv
import sys

import features


def extract_dataset(input_file: str, output_file: str) -> None:
    """Extract features from every URL in a CSV dataset."""

    with open(input_file, "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        if "url" not in reader.fieldnames:
            raise ValueError("Input CSV must contain a 'url' column.")

        if "type" not in reader.fieldnames:
            raise ValueError("Input CSV must contain a 'type' column.")

        rows = list(reader)

    if not rows:
        print("The input CSV contains no data.")
        return

    feature_names = [feature.name for feature in features.FEATURES]

    output_fieldnames = ["url", "type"] + feature_names

    with open(output_file, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=output_fieldnames
        )

        writer.writeheader()

        for row_number, row in enumerate(rows, start=1):
            url = row["url"]
            url_type = row["type"]

            try:
                extracted_features = features.extract_features(url)

                output_row = {
                    "url": url,
                    "type": url_type,
                    **extracted_features
                }

                writer.writerow(output_row)

            except Exception as error:
                print(
                    f"Warning: Could not process row {row_number}: "
                    f"{error}",
                    file=sys.stderr
                )


def main() -> None:
    """Run dataset feature extraction."""

    if len(sys.argv) != 3:
        print(
            "Usage: python extract_dataset.py "
            "<input.csv> <output.csv>"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    extract_dataset(input_file, output_file)

    print(f"Feature extraction complete.")
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    main()