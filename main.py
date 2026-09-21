# 2026 Joey Manani & Anchorfish Team
# Computing Technology Innovation Project
# Feature extraction script


"""
Given a CSV file with the link and the classification that its phishing or not, extract the features of the link and save it to a new CSV file.
The features are:
- Length of the link
- Number of subdomains
- Number of query parameters
- Number of path segments
- Number of dots in the link
- Number of slashes in the link
- Number of hyphens in the link
- Number of underscores in the link

Source these features from an actual source to justify this. Use even deeper features too. Each of the features beyond must justify further, particularly what its function is rather than if it classifies as phishing or not.

This script will be used to extract the features of the link and save it to a new CSV file.

Model will NOT be trained here. This repository is just for feature extraction.

As confirmed by Ricky, using unix commands to source metadata about the URL is allowed, but NO curling or wgetting to fetch the webpage itself. No HTTP headers either.
Use of dig, nslookup, host, etc. is allowed, and therefore will be added to the CSV file for training the model.
"""

import csv
import os
import sys
import requests
import json
import time
import random
import string
import hashlib
import base64
import urllib.parse
import urllib.request
import features

def main():
    url = "https://sub.dom.ain.domain.vic.gov.au/path/to/page?param1=value1&param2=value2#fragment"
    fl: dict = features.extract_features(url)
    for feature_name, feature_value in fl.items():
        print(f"{feature_name}: {feature_value}")

if __name__ == "__main__":
    main()
