import requests
import os
from bs4 import BeautifulSoup
import pdfplumber
import pandas as pd
import re

# Step 1: Create folders for PDFs and output
os.makedirs("data/pdfs", exist_ok=True)

# Step 2: Scrape a webpage for PDF links
url = "https://example.com/pdfs"  # <-- replace with your target URL
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

pdf_files = []

for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.endswith(".pdf"):
        pdf_url = href if href.startswith("http") else url + href
        pdf_file = os.path.join("data/pdfs", os.path.basename(href))
        r = requests.get(pdf_url)
        with open(pdf_file, "wb") as f:
            f.write(r.content)
        print(f"Saved {pdf_file}")
        pdf_files.append(pdf_file)

# Step 3: Extract text from PDFs and find structured info
rows = []
for file in pdf_files:
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

        # Example extraction: error codes like ERR1234 or CONFIG_PARAM=value
        error_codes = re.findall(r"(ERR\d+)", text)
        config_params = re.findall(r"([A-Z_]+)\s*=\s*([\w\d.-]+)", text)

        rows.append({
            "file": os.path.basename(file),
            "error_codes": ", ".join(error_codes) if error_codes else "None",
            "config_params": "; ".join([f"{k}={v}" for k,v in config_params]) if config_params else "None"
        })

# Step 4: Save extracted data to CSV
df = pd.DataFrame(rows)
df.to_csv("data/output.csv", index=False)
print("Saved extracted data to data/output.csv")
