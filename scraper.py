import requests
import os
from bs4 import BeautifulSoup
import pdfplumber
import pandas as pd
import re
import sys

# Step 1: Take URL from command line (or default if none given)
url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/pdfs"

# Step 2: Create folders for PDFs and output
os.makedirs("data/pdfs", exist_ok=True)

print(f"Starting PDF scrape from: {url}")

# Step 3: Scrape webpage for PDF links
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

pdf_files = []

for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.endswith(".pdf"):
        pdf_url = href if href.startswith("http") else url + href
        pdf_file = os.path.join("data/pdfs", os.path.basename(href))
        print(f"Downloading: {pdf_url}")
        r = requests.get(pdf_url)
        with open(pdf_file, "wb") as f:
            f.write(r.content)
        print(f"Saved: {pdf_file}")
        pdf_files.append(pdf_file)

# Step 4: Extract text from PDFs and find structured info
rows = []
for file in pdf_files:
    print(f"Extracting from: {os.path.basename(file)}")
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

        # Example extraction: error codes like ERR1234
        error_codes = re.findall(r"(ERR\d+)", text)
        # Example extraction: config params like PARAM=value
        config_params = re.findall(r"([A-Z_]+)\s*=\s*([\w\d.-]+)", text)

        rows.append({
            "file": os.path.basename(file),
            "error_codes": ", ".join(error_codes) if error_codes else "None",
            "config_params": "; ".join([f"{k}={v}" for k,v in config_params]) if config_params else "None"
        })

# Step 5: Save extracted data to CSV
df = pd.DataFrame(rows)
os.makedirs("data", exist_ok=True)
df.to_csv("data/output.csv", index=False)

print(" Done! Extracted data saved to data/output.csv")
