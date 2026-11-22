
from fastapi import FastAPI

from app.news import get_company_news
from app.sentiment import analyze_sentiment

# Create the FastAPI application
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

    # Analyze the sentiment of each article
    for article in articles:
        headline = article.get("headline", "")
        summary = article.get("summary", "")

        # Combine headline and summary
        text = headline + " " + summary

        # Add sentiment results
        article["sentiment_analysis"] = analyze_sentiment(text)

    return {
        "company": symbol.upper(),
        "article_count": len(articles),
        "articles": articles
    }
