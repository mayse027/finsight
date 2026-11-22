
from fastapi import FastAPI

from app.news import get_company_news

app = FastAPI(
    title="FinSight API",
    description="Financial news analysis platform",
    version="1.0.0"
)


@app.get("/")
async def home():
    return {
        "message": "Welcome to FinSight!"
    }


@app.get("/api/news/{symbol}")
async def company_news(symbol: str):

    articles = await get_company_news(symbol)

    return {
        "company": symbol.upper(),
        "article_count": len(articles),
        "articles": articles
    }
