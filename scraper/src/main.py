import requests
import time
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone

URL = "http://books.toscrape.com/"

HEADERS = {
    "User-Agent": "FlyRankInternship A9/1.0 (+https://github.com/NamraAjmal/backend)"
}


def get_page(url, cache_file):
    if cache_file.exists():
        html = cache_file.read_text(encoding="utf-8")
        print("CACHE HIT")
        print(f"Response size: {len(html.encode('utf-8'))} bytes")
        return html

    print("FETCH")
    time.sleep(0.5)

    response = requests.get(url, headers=HEADERS, timeout=5)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch with status code {response.status_code}")

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(response.text, encoding="utf-8")

    print(f"Response size: {len(response.content)} bytes")

    return response.text


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
    current_url = URL
    discovered_books = {}

    for page_number in range(1, 4):
        print(f"\nCatalogue page {page_number}")

        cache_file = Path(f"cache/catalogue-page-{page_number}.html")

        html = get_page(current_url, cache_file)

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

        html = get_page(book_url, cache_file)

        record = extract_book(html, book_url, source_page)

        records.append(record)

    print("\nRAW RECORD:")
    print(records[0])

    print(f"\nunique_urls={len(discovered_books)}")
    print(f"records={len(records)}")


if __name__ == "__main__":
    main()
