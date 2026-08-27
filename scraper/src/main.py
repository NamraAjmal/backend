import requests
import time
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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


def main():
    current_url = URL
    discovered_books = set()

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

            discovered_books.add(book_url)

        next_link = soup.select_one("li.next a")

        if next_link:
            href = next_link["href"]

            current_url = urljoin(current_url, href)
        else:
            break

    print(f"\ncatalogue_pages={page_number}")
    print(f"discovered={len(discovered_books)}")


if __name__ == "__main__":
    main()
