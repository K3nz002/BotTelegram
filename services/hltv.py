import httpx
import feedparser

def get_latest_hltv_news(rss_url: str, limit: int = 3) -> list:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        with httpx.Client(timeout=10.0, headers=headers, follow_redirects=True) as client:
            response = client.get(rss_url)
            feed = feedparser.parse(response.content)
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    "title": entry.title,
                    "link": entry.link
                })
            return articles
    except Exception as e:
        return f"Erro ao buscar notícias: {e}"