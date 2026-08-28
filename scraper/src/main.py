import requests
import time
import json
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from pydantic import BaseModel
from requests.exceptions import Timeout

URL = "https://books.toscrape.com/"

HEADERS = {
    "User-Agent": "FlyRankInternship A9/1.0 (+https://github.com/NamraAjmal/backend)"
}


class Book(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: str | None
    source_page: str
    fetched_at: str


def get_page(url, cache_file, stats):
    if cache_file.exists():
        html = cache_file.read_text(encoding="utf-8")
        print("CACHE HIT")
        print(f"Response size: {len(html.encode('utf-8'))} bytes")
        stats["cache_hits"] += 1
        return html

    for attempt in range(2):
        print("FETCH")
        time.sleep(0.5)

        try:
            response = requests.get(url, headers=HEADERS, timeout=5)

            if response.status_code == 404:
                raise RuntimeError(f"404 Not Found: {url}")

            if response.status_code == 403:
                raise RuntimeError(f"403 Forbidden: {url}")

            if 500 <= response.status_code <= 599:
                if attempt == 0:
                    print("Server error, retrying...")
                    continue
                raise RuntimeError(
                    f"Failed to fetch with status code {response.status_code}"
                )

            if response.status_code != 200:
                raise RuntimeError(
                    f"Failed to fetch with status code {response.status_code}"
                )

            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(response.text, encoding="utf-8")

            stats["pages_fetched"] += 1

            print(f"Response size: {len(response.content)} bytes")

            return response.text

        except Timeout:
            if attempt == 0:
                print("Timeout, retrying...")
                continue
            raise RuntimeError(f"Request timed out: {url}")


def extract_book(html, product_url, source_page):
    soup = BeautifulSoup(html, "html.parser")

    product = soup.select_one("article.product_page")

    title = product.select_one("h1")
    price = product.select_one(".price_color")
    availability = product.select_one(".availability")
    rating = product.select_one(".star-rating")
    description = product.select_one("#product_description + p")

    rating_text = None
    if rating:
        rating_text = next(
            (
                class_name
                for class_name in rating.get("class", [])
                if class_name != "star-rating"
            ),
            None,
        )

    return {
        "title": title.get_text(strip=True) if title else None,
        "product_url": product_url,
        "price_text": price.get_text(strip=True) if price else None,
        "availability_text": (
            availability.get_text(" ", strip=True) if availability else None
        ),
        "rating_text": rating_text,
        "description": description.get_text(strip=True) if description else None,
        "source_page": source_page,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    start_time = time.time()

    stats = {
        "pages_fetched": 0,
        "cache_hits": 0,
        "valid_records": 0,
        "invalid_records": 0,
        "failed_pages": 0,
    }
    current_url = URL
    discovered_books = {}

    for page_number in range(1, 4):
        print(f"\nCatalogue page {page_number}")

        cache_file = Path(f"cache/catalogue-page-{page_number}.html")

        html = get_page(current_url, cache_file, stats)

        soup = BeautifulSoup(html, "html.parser")

        links = soup.select("article.product_pod h3 a")

        print(f"Books on page {page_number}: {len(links)}")

        for link in links:
            href = link["href"]

            book_url = urljoin(current_url, href)

            discovered_books[book_url] = current_url

        next_link = soup.select_one("li.next a")

        if next_link:
            href = next_link["href"]

            current_url = urljoin(current_url, href)
        else:
            break

    print(f"\ncatalogue_pages={page_number}")
    print(f"discovered={len(discovered_books)}")

    records = []

    for index, (book_url, source_page) in enumerate(discovered_books.items(), start=1):
        print(f"\nBook {index}/{len(discovered_books)}")

        cache_file = Path(f"cache/books/{index}.html")

        try:
            html = get_page(book_url, cache_file, stats)

            record = extract_book(html, book_url, source_page)

            records.append(record)

        except Exception as error:
            print(f"FAILED: {book_url}")
            print(f"Reason: {error}")

            stats["failed_pages"] += 1

    good_records = []
    errors = []
    seen_urls = set()

    for record in records:
        try:
            price_gbp = float(
                record["price_text"].replace("£", "").replace("Â", "").strip()
            )

            record["price_gbp"] = price_gbp

            book = Book.model_validate(record)

            if book.product_url in seen_urls:
                continue

            seen_urls.add(book.product_url)

            good_records.append(book.model_dump())
            stats["valid_records"] += 1

        except Exception as error:
            errors.append({"record": record, "reason": str(error)})
            stats["invalid_records"] += 1

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "books.json").write_text(
        json.dumps(good_records, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    duration = time.time() - start_time

    run_report = {
        "start_time": datetime.fromtimestamp(start_time, timezone.utc).isoformat(),
        "duration_seconds": round(duration, 2),
        "pages_fetched": stats["pages_fetched"],
        "cache_hits": stats["cache_hits"],
        "valid_records": stats["valid_records"],
        "invalid_records": stats["invalid_records"],
        "failed_pages": stats["failed_pages"],
    }

    (output_dir / "run-report.json").write_text(
        json.dumps(run_report, indent=2), encoding="utf-8"
    )

    (output_dir / "errors.json").write_text(
        json.dumps(errors, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\nunique_urls={len(discovered_books)}")
    print(f"valid_records={len(good_records)}")
    print(f"errors={len(errors)}")


if __name__ == "__main__":
    main()
