import re

with open("input.csv", "r", encoding="utf-8") as file:
    content = file.read()

content = re.sub(r"legitimate", "benign", content, flags=re.IGNORECASE)
content = re.sub(r"phishing", "phishing", content, flags=re.IGNORECASE)

with open("output.csv", "w", encoding="utf-8") as file:
    file.write(content)
