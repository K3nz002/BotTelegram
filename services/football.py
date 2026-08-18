import httpx
import feedparser

def get_latest_football_news(limit: int = 3) -> list:
    url = "https://www.espn.com.br/rss"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        with httpx.Client(timeout=10.0, headers=headers, follow_redirects=True) as client:
            resp = client.get(url)
            feed = feedparser.parse(resp.content)

            news = []
            for entry in feed.entries[:limit]:
                news.append({
                    "title": entry.title,
                    "link": entry.link
                })
            return news
    except Exception as e:
        print(f"Erro ao buscar notícias de futebol: {e}")
        return []