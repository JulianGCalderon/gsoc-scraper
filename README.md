# GSOC Scraper

Scrapes organizations from GSoC.

# Usage

The script takes an URL to the organizations list, and outputs the data in JSONL format.

```bash
uv run main.py https://summerofcode.withgoogle.com/programs/2026/organizations | tee data.json
```

To convert JSONL to CSV, we can use `jq`.

<!-- https://unix.stackexchange.com/a/754939 -->
```bash
jq '[first|keys_unsorted] + map([.[]]) | .[] | @csv' -rs data.json > data.csv
```
