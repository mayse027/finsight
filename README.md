# FinSight

**A financial news analysis platform that helps users track companies and understand market sentiment through financial news.**

## Overview

FinSight is a full-stack application designed to make financial news easier to explore and analyze. Users can retrieve company-specific news and, as development progresses, identify sentiment trends and follow companies they are interested in.

## Tech Stack

### Backend
- Python
- FastAPI
- Finnhub API
- HTTPX

### Frontend
- React (planned)

### Database
- MongoDB (planned)
- SQL / SQLite (planned)

## Current Features

- Retrieve company-specific financial news using stock ticker symbols
- Fetch recent articles from the Finnhub API
- REST API built with FastAPI
- Interactive API documentation through Swagger UI

## Planned Features

- News sentiment analysis
- Company watchlists and tracking
- Financial news dashboard
- Sentiment trend visualizations
- AI-powered article summaries

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/mayse027/finsight.git
cd finsight
```

### 2. Set Up the Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside the `backend` directory:

```env
FINNHUB_API_KEY=your_api_key_here
```

Obtain an API key from [Finnhub](https://finnhub.io/).

### 5. Start the Backend

From the `backend` directory, run:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## Example API Endpoint

Retrieve recent news for a company:

```http
GET /api/news/{symbol}
```

Example:

```http
GET /api/news/NVDA
```

## Project Status

FinSight is currently under active development. New features and improvements are being added.
