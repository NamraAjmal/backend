# Scraper

## Target classification

### Target

Books to Scrape

https://books.toscrape.com/

### Why this site?

Books to Scrape is a sandbox site created for people to practise web scraping.

### Scope

This assignment will scrape only the first 3 catalogue pages.

### Data to collect

The scraper will collect book information from the catalogue pages, including:

- Book title
- Price
- Availability
- Rating
- Book URL
- Description
- Source catalogue page
- Fetch timestamp

### Robots.txt

Checked:

https://books.toscrape.com/robots.txt

Result:

404 Not found

### Why this is appropriate

The target is specifically provided as a scraping practice sandbox, and the scraper is limited to the first three catalogue pages.

I will not reuse this code on another site without checking its rules and terms first.

## Lane

Python / BeautifulSoup

### Installation

This project uses `uv` for Python environment and dependency management.

Install the dependencies with:

```bash
uv sync
```

### Run

From the scraper directory, run:

```bash
uv run python src/main.py
```

The scraper writes its results to the `output/` directory.

## Record schema

Each valid record contains:

- `title`: string
- `product_url`: string
- `price_text`: string
- `price_gbp`: number
- `availability_text`: string
- `rating_text`: string
- `description`: string or null
- `source_page`: string
- `fetched_at`: string

Records are validated with Pydantic before they are stored.

## Output

The scraper produces:

- `output/books.json` — validated and normalized book records.
- `output/errors.json` — records that fail validation, with the reason.
- `output/run-report.json` — statistics about the run.

The scraper discovers 60 unique books from the first three catalogue pages.

## Politeness rules

The scraper follows these rules:

- Sends a descriptive User-Agent.
- Waits at least 0.5 seconds before real requests.
- Uses a 5-second request timeout.
- Caches fetched pages locally in `cache/`.
- Cached pages require no delay because they do not make a network request.
- Retries a timeout or 5xx server error once.
- Does not retry 403 or 404 responses.
- Processes each book page separately so one failed page does not stop the entire run.

## Idempotency

Each book uses its absolute `product_url` as its identity.

Duplicate URLs are removed before records are stored, so running the scraper twice does not create duplicate records. A normal run produces 60 unique valid records.

## Run report

A real run produced the following report:

```json
{
  "start_time": "2026-08-28T07:57:58.481967+00:00",
  "duration_seconds": 1.32,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0
}
```

## Why no browser?

This assignment does not need a browser because the required data is already present in the HTML sent by the server. A browser would only add unnecessary cost and complexity.

## Limitation

The scraper depends on the website's current HTML structure and CSS selectors. If the site's markup changes, the selectors may need to be updated.

## Ethics

I use an official API when one exists. I never bypass logins, paywalls, or blocks, and I collect only what I need.
