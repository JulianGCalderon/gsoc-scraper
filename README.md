# GSOC Scraper

Scrapes organizations from GSoC.

# Usage

The script takes an URL to the organizations list, and outputs the data in JSONL format.

```bash
uv run main.py https://summerofcode.withgoogle.com/programs/2025/organizations | tee data.json
```
