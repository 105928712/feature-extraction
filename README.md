# Phishing URL Feature Extraction

COS30049 - Computing Technology Innovation Project - Phishing Link Detection URL feature extraction

This list of features will be used to extract and separate parts of a given URL into information that can be read by a trained AI model to reach the conclusion of if the URL is safe or potentially unsafe.

## Installation

Depending on what OS you are running, you will need to use a different command for installation:

For Windows:
```bash
setup.bat
```
or
```bash
. .\setup.ps1
```

For macOS and Linux/Unix:
```bash
source setup.sh
```

## Usage



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