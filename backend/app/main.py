
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.news import get_company_news
from app.sentiment import analyze_sentiment

app = FastAPI(
    title="FinSight API",
    description="Financial news analysis platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def home():
    return {"message": "Welcome to FinSight!"}


@app.get("/api/news/{symbol}")
async def company_news(symbol: str):
    articles = await get_company_news(symbol)

    for article in articles:
        headline = article.get("headline", "")
        summary = article.get("summary", "")
        text = headline + " " + summary
        article["sentiment_analysis"] = analyze_sentiment(text)

    return {
        "company": symbol.upper(),
        "article_count": len(articles),
        "articles": articles
    }
