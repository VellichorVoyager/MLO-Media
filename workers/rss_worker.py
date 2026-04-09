import logging

import feedparser

FEEDS = {
    "National Mortgage News": "https://www.nationalmortgagenews.com/feed",
    "HousingWire": "https://www.housingwire.com/feed",
    "MPA": "https://www.mpamag.com/us/rss",
}

logger = logging.getLogger(__name__)


def fetch_articles():
    articles = []

    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries:
                articles.append(
                    {
                        "title": entry.title,
                        "url": entry.link,
                        "published_at": entry.get("published", None),
                        "source": source,
                        "summary": entry.get("summary", ""),
                    }
                )
        except Exception as exc:
            logger.error("Failed to fetch feed '%s' (%s): %s", source, url, exc)

    return articles
