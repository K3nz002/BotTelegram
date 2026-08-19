import logging
import httpx
import feedparser

logger = logging.getLogger(__name__)

def get_latest_football_news(rss_url: str, limit: int = 3) -> list:
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}
    try:
        with httpx.Client(timeout=10.0, headers=headers, follow_redirects=True) as client:
            response = client.get(rss_url)
            feed = feedparser.parse(response.text)
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    "title": getattr(entry, "title", "").strip(),
                    "link": getattr(entry, "link", "").strip()
                })
            return articles
    except Exception as e:
        logger.error("Erro ao buscar notícias do mundo: %s", e)
        return []
