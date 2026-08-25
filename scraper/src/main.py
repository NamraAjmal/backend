import requests
from pathlib import Path

URL = "http://books.toscrape.com/"
CACHE_FILE = Path("cache/catalogue-page-1.html")

HEADERS = {
    "User-Agent": "FlyRankInternship A9/1.0 (+https://github.com/NamraAjmal/backend)"
}


def main():
    if CACHE_FILE.exists():
        html = CACHE_FILE.read_text(encoding="utf-8")
        print("CACHE HIT")
        print(f"Response size: {len(html.encode('utf-8'))} bytes")
        return
    print("FETCH")
    response = requests.get(URL, headers=HEADERS, timeout=5)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch with status code {response.status_code}")

    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(response.text, encoding="utf-8")

    print(f"Response size: {len(response.content)} bytes")


if __name__ == "__main__":
    main()
