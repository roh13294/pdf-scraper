# PDF Error Log & Config Scraper

This tool downloads PDFs from a target webpage and extracts **error codes** and **configuration parameters** into a clean CSV.  

It is designed for situations where engineers need to pull structured insights out of large technical documents (logs, firmware reports, config files) without manually reading through dozens of PDFs.

---

## Features
- Scrapes a target webpage for linked PDF files
- Downloads PDFs locally
- Extracts:
  - Error codes (e.g. `ERR1234`)
  - Config parameters in the format `PARAM=value`
- Saves all extracted results into `data/output.csv`

---

## Example Usage

Run the scraper by passing a URL that contains PDFs:

```bash
python scraper.py https://example.com/reports
