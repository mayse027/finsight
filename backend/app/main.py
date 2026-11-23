
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.news import get_company_news
from app.sentiment import analyze_sentiment
from app.database import engine, Base, get_db
from app import models, crud

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

Base.metadata.create_all(bind=engine)


class CompanyCreate(BaseModel):
    symbol: str
    name: str | None = None


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


@app.post("/api/companies")
def add_company(company: CompanyCreate, db: Session = Depends(get_db)):
    existing_company = crud.get_company(db, company.symbol)

    if existing_company:
        raise HTTPException(
            status_code=409,
            detail="Company already exists"
        )

    new_company = crud.create_company(
        db,
        company.symbol,
        company.name
    )

    return {
        "id": new_company.id,
        "symbol": new_company.symbol,
        "name": new_company.name
    }


@app.get("/api/companies")
def list_companies(db: Session = Depends(get_db)):
    companies = crud.get_companies(db)

    return [
        {
            "id": company.id,
            "symbol": company.symbol,
            "name": company.name
        }
        for company in companies
    ]


@app.delete("/api/companies/{symbol}")
def remove_company(symbol: str, db: Session = Depends(get_db)):
    company = crud.get_company(db, symbol)

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    crud.delete_company(db, company)

    return {
        "message": f"{symbol.upper()} removed successfully"
    }

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.news import get_company_news
from app.sentiment import analyze_sentiment
from app.database import engine, Base, get_db
from app import models, crud

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

Base.metadata.create_all(bind=engine)


class CompanyCreate(BaseModel):
    symbol: str
    name: str | None = None


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


@app.post("/api/companies")
def add_company(company: CompanyCreate, db: Session = Depends(get_db)):
    existing_company = crud.get_company(db, company.symbol)

    if existing_company:
        raise HTTPException(
            status_code=409,
            detail="Company already exists"
        )

    new_company = crud.create_company(
        db,
        company.symbol,
        company.name
    )

    return {
        "id": new_company.id,
        "symbol": new_company.symbol,
        "name": new_company.name
    }


@app.get("/api/companies")
def list_companies(db: Session = Depends(get_db)):
    companies = crud.get_companies(db)

    return [
        {
            "id": company.id,
            "symbol": company.symbol,
            "name": company.name
        }
        for company in companies
    ]
