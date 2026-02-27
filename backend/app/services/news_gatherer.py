import httpx
from bs4 import BeautifulSoup

class NewsGathererService:
    @staticmethod
    async def get_company_news(symbol):
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, features="xml")
                    items = soup.find_all('item')
                    news = []
                    for item in items[:5]:
                        news.append({
                            "title": item.title.text,
                            "link": item.link.text,
                            "description": item.description.text
                        })
                    return news
            except Exception:
                pass
        return []
