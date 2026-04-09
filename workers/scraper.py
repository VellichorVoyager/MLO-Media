import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

MAX_CONTENT_LENGTH = 5000


def scrape_article(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text() for p in paragraphs])

        return content[:MAX_CONTENT_LENGTH]

    except Exception as exc:
        logger.warning("Failed to scrape %s: %s", url, exc)
        return ""
