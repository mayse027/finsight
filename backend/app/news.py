
from datetime import date, timedelta

import httpx
from fastapi import HTTPException

from app.config import FINNHUB_API_KEY, BASE_URL


async def get_company_news(symbol: str):

    # Check that the API key exists
    if not FINNHUB_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Finnhub API key is missing"
        )

    # Get today's date and calculate the date 30 days ago
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    # Prepare the parameters for the Finnhub request
    params = {
        "symbol": symbol.upper(),
        "from": start_date.isoformat(),
        "to": end_date.isoformat()
    }

    # Add the API key to the request headers
    headers = {
        "X-Finnhub-Token": FINNHUB_API_KEY
    }

    try:
        # Create an HTTP client and request company news
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                f"{BASE_URL}/company-news",
                params=params,
                headers=headers
            )

            # Check whether the API returned an error
            response.raise_for_status()

            # Convert the response into Python data
            articles = response.json()

            # Return at most 20 articles
            return articles[:20]

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail="Financial news provider returned an error"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to financial news provider"
        )
