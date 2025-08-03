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

## Example Output
| file          | error_codes       | config_params                    |
|---------------|------------------|----------------------------------|
| log1.pdf      | ERR1023, ERR2045 | MAX_SPEED=250; TIMEOUT=30s       |
| firmware.pdf  | None             | VERSION=1.2.0; BUILD=release     |

---

## How to Use
1. Clone this repository  
   ```bash
   git clone https://github.com/your-username/pdf-error-scraper.git
   cd pdf-error-scraper
