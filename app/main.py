import logging

from workers.rss_worker import fetch_articles
from workers.scraper import scrape_article
from workers.enricher import categorize, tag
from workers.embeddings import generate_embedding
from services.supabase_client import upsert_article

logger = logging.getLogger(__name__)


def run_pipeline():
    articles = fetch_articles()

    for article in articles:
        try:
            article["content"] = scrape_article(article["url"])
            article["category"] = categorize(article)
            article["tags"] = tag(article)

            article["embedding"] = generate_embedding(
                article["title"] + " " + article.get("summary", "")
            )

            upsert_article(article)
        except Exception as exc:
            logger.error(
                "Failed to process article '%s': %s", article.get("url"), exc
            )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()
