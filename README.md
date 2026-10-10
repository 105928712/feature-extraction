# Phishing URL Feature Extraction

COS30049 Computing Technology Innovation Project

Cleans the raw URL datasets and turns each URL into the 54 features the models train on

## Installation

The datasets in `datasets/` are zips stored with Git LFS

**Automatic** (venv): create the environment, install the packages, download the LFS files and unzip them into `datasets/`:
- Windows: `setup.bat` (Command Prompt) or `. .\setup.ps1` (PowerShell)
- macOS / Linux: `source setup.sh`

**Manual** (Conda):
```bash
conda create -n phishing-features python=3.13 -y
conda activate phishing-features
pip install -r requirements.txt
git lfs install
git lfs pull
```
Then unzip `datasets/Final Tree.zip` and `datasets/Extra Data.zip` inside `datasets/`

## Data

This repo builds the Final Tree that all three repos use. Each step's output is the next step's input:

```
├── Final Tree.zip
├── Extra Data.zip
├── Final Tree/
│   ├── 1 Raw Data/          malicious_phish.csv (Kaggle), Phishing URLs.csv + URL dataset.csv (Mendeley)
│   ├── 2. Cleaned Data/     kaggle_clean.csv, phish_clean.csv, urlds_clean.csv
│   ├── 3. Merged Data/      cleaned.csv
│   └── 4. Final Data/       features.csv   (what the models train on)
└── Extra Data/              tranco_1m, tranco_processed, urlset
```

(The real folder names are longer, such as `1 Raw Data - Run These Through Cleaning Scripts`. The commands below use them in full for reproducibility)

Sources: 

Siddhartha, M. (2021) *Malicious URLs dataset.* Kaggle. Available at: [Malicious URLs Dataset](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset) (Accessed: 7 September 2026). (CC0: Public Domain)

KAITHOLIKKAL, JISHNU K S; B, Arthi  (2024), *Phishing URL dataset.* Mendeley Data, V1, doi: 10.17632/vfszbj9b36.1 (Accessed: 7 September 2026). (CC BY 4.0)

## Usage

### Rebuild the Final Tree from the raw files

Run from the repo root. Each step writes the next folder of the Final Tree. The provided Final Tree on LFS already has this structure, so this is only for reproducibility.

Expects the raw dataset files to be present in the `datasets/Final Tree/1 Raw Data - Run These Through Cleaning Scripts` directory.

```bash
# 1 -> 2: clean each source into [url,type] (canonical URLs, labels unified , unreadable rows dropped)
python -m scripts.process_kaggle "datasets/Final Tree/1 Raw Data - Run These Through Cleaning Scripts/malicious_phish.csv" "datasets/Final Tree/2. Cleaned Data - Already Processed With Cleaning Scripts/kaggle_clean.csv"
python -m scripts.process_phishing_urls "datasets/Final Tree/1 Raw Data - Run These Through Cleaning Scripts/Phishing URLs.csv" "datasets/Final Tree/2. Cleaned Data - Already Processed With Cleaning Scripts/phish_clean.csv"
python -m scripts.process_url_dataset "datasets/Final Tree/1 Raw Data - Run These Through Cleaning Scripts/URL dataset.csv" "datasets/Final Tree/2. Cleaned Data - Already Processed With Cleaning Scripts/urlds_clean.csv"

# 2 -> 3: merge (duplicates kept once, conflicting labels dropped)
python -m scripts.merge_datasets "datasets/Final Tree/3. Merged Data - Ran The Cleaned Data Through Merge Datasets Script/cleaned.csv" "datasets/Final Tree/2. Cleaned Data - Already Processed With Cleaning Scripts/kaggle_clean.csv" "datasets/Final Tree/2. Cleaned Data - Already Processed With Cleaning Scripts/phish_clean.csv" "datasets/Final Tree/2. Cleaned Data - Already Processed With Cleaning Scripts/urlds_clean.csv"

# 3 -> 4: extract the 54 features for every url in merged data
python -m scripts.extract_features "datasets/Final Tree/3. Merged Data - Ran The Cleaned Data Through Merge Datasets Script/cleaned.csv" "datasets/Final Tree/4. Final Data - Run Through Feature Extractor Script/features.csv"
```

`scripts/process_tranco.py` is kept for reference only because Tranco was tried as a legit source and dropped (see `data-visualisations/eda_merged.ipynb`). No need to run it.

### Features for one URL

```python
import features
from features.utils import canonical_url

features.extract_features(canonical_url("http://www.paypal.com.secure-login.example.com/webscr?cmd=login"))
```

Always use `canonical_url(url)` which is in the same pipeline on how the training data was cleaned.

### Tests

```bash
python -m unittest discover tests
```

## Feature Extraction Masterlist

### Our Implemented Features

Data types:
- Integer
- Boolean
- String
- Float

### Brand (brand.py)

**Integer:**

- Brand Edit Distance
How close the root domain is to a known brand name

### Char (char.py)

#### **Integer:**

- **Question Mark Count:** How many question mark characters (` ? `) are in the URL
- **Ampersand Count:** How many ampersand characters (` & `) are in the URL
- **Dot Count:** How many period characters (` . `) are in the URL
- **Slash Count:** How many forward slash characters (` / `) are in the URL
- **Hyphen Count:** How many hyphen characters (` - `) are in the URL
- **Underscore Count:** How many underscore characters (` _ `) are in the URL
- **Hash Count:** How many hash characters (` # `) are in the URL
- **At Symbol Count:** How many at characters (` @ `) are in the URL
- **Tilde Symbol Count:** How many tilde characters (` ~ `) are in the URL
- **Percent Symbol Count:** How many percent characters (` % `) are in the URL
- **URL Length:** Total character count of the URL

#### **Float:**

- **Digit Ratio:** Fraction of the URL that are digits
- **Special Character Ratio:** Fraction of the URL that are special characters

### Entropy (entropy.py)

#### **Float:**

- **Extract Entropy:** Overall entropy of the URL
- **Host Entropy:** Entropy of the host
- **Path Entropy:** Entropy of the path
- **Query Entropy:** Entropy of the query

### Host (host.py)

#### **Boolean:**

- **Host has At Symbol Check:** Checking the existence of an at character (` @ `) in the host
- **Is IP Host Check:** Checking if an IP is the host
- **Host has Non Standard Port Check:** Checking if the host has a non-standard port
- **HTTPS in Hostname Check:** Checking if HTTPS is disordered in the host
- **Domain Has Punycode Check:** Checking the existence of Punycode in the host

#### **Integer:**

- **Host Length:** Total characters of the host

### Path (path.py)

#### **Integer:**

- **Path Level:** Total levels of the path
- **Path Length:** Total characters of the path

#### **Boolean:**

- **Double Slash Path Check:** Checking the existence of a double forward slash characters (` // `) in the path

### Query (query.py)

#### **Integer:**

- **Query Length:** Total characters of the query
- **Number of Query Components:** Total count of query components

### Root Domain (rootdomain.py)

#### **String:**

- **Extract Root Domain:** Extract the URL root domain

#### **Integer:**

- **Root Length:** Total characters of the root domain
- **Root Hyphen Count:** Total hyphen characters (` - `) of the root domain
- **Root Number Count:** Total amount of digits in the root domain

#### **Boolean:**

- **Root Hyphen Check:** Checking the existence of hyphen characters (` - `) in the root domain
- **Root Number Check:** Checking the existence of digits in the root domain
- **Root Punycode Check:** Checking the existence of Punycode within the root domain

#### **Float:**

- **Root Entropy:** Entropy of the root domain
- **Root Digit Ratio:** Fraction of the root domain that are digits

### Scheme (scheme.py)

#### **String:**

- **Extract scheme:** Extract the URL scheme

**Boolean:**

- **HTTPS check:** Check the existence of a HTTPS scheme
- **Obscure scheme check:** Check the existence of an obscure scheme

### Sensitive Words (sense_words.py)

#### **Integer:**

- **Path and Query Sensitive Words Count:** Total sensitive words within the path and query

### Shortener

#### **Boolean:**

- **Is Known Shortener:** Checking if domain is a known link-shortening service check

### Subdomain (subdomain.py)

#### **String:**

- **Extract Subdomain:** Extract the URL subdomain

#### **Boolean:**

- **HasWWW Check:** Checking the existence of a WWW subdomain
- **Subdomain Punycode Check:** Checking the existence of Punycode within the subdomain
- **Subdomain Embedded TLD Check:** Checking the existence of a TLD within the subdomain

#### **Integer:**

- **Subdomain Count:** How many subdomains exist in the URL
- **Subdomain Length:** How many characters make up the subdomain
- **Subdomain Max Label Length:** How many characters make up the longest subdomain
- **Subdomain Hyphen Count:** How many hyphen characters (` - `) exist within the subdomain

#### **Float:**

- **Subdomain Entropy:** Entropy of the subdomain
- **Subdomain Digit Ratio:** Fraction of the subdomain that are digits

### TLD (tld.py)

#### **String:**

- **Extract TLD:** Extract the URL top-level domain

#### **Integer:**

- **TLD Count:** How many top-level domain parts exist inside the URL
- **TLD Length:** How many characters exist in the top-level domain

#### **Boolean:**

- **TLD Obscure Check:** Checking the existence of a top-level domain that is obscure/commonly abused
- **TLD Common Check:** Checking the existence of a common top-level domain

### Wordstats (wordstats.py)

#### **Integer:**

- **Longest Word Length:** Total characters that make up the longest word in the URL

#### **Float:**

- **Average Word Length:** The average word length within the URL

## License

[MIT](https://choosealicense.com/licenses/mit/)