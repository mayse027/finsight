
import { useState } from 'react'
import './App.css'

function App() {
  const [ticker, setTicker] = useState('NVDA')
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function searchCompany() {
    if (!ticker.trim()) return

    setLoading(true)
    setError('')
    setArticles([])

    try {
      const response = await fetch(
        `http://localhost:8000/api/news/${encodeURIComponent(ticker.trim())}`
      )

      if (!response.ok) {
        throw new Error('Could not retrieve company news.')
      }

      const data = await response.json()
      setArticles(data.articles)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const positiveCount = articles.filter(
    article => article.sentiment_analysis?.sentiment === 'positive'
  ).length

  const negativeCount = articles.filter(
    article => article.sentiment_analysis?.sentiment === 'negative'
  ).length

  const neutralCount = articles.filter(
    article => article.sentiment_analysis?.sentiment === 'neutral'
  ).length

  const total = articles.length

  const percentage = count =>
    total === 0 ? 0 : Math.round((count / total) * 100)

  const positivePercentage = percentage(positiveCount)
  const negativePercentage = percentage(negativeCount)
  const neutralPercentage = percentage(neutralCount)

  const overallSentiment =
    total === 0 ? 'Awaiting data' :
    positiveCount > negativeCount && positiveCount > neutralCount ? 'Mostly positive' :
    negativeCount > positiveCount && negativeCount > neutralCount ? 'Mostly negative' :
    'Mixed coverage'

  const formatDate = timestamp => {
    if (!timestamp) return 'Date unavailable'
    return new Date(timestamp * 1000).toLocaleDateString()
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">finsight<span>.</span></div>
        <nav>
          <a className="active" href="#">Overview</a>
          <a href="#">Markets</a>
          <a href="#">Watchlist</a>
        </nav>
        <div className="topbar-right">Financial News & Analysis</div>
      </header>

      <main className="dashboard">
        <section className="page-heading">
          <div>
            <p className="eyebrow">MARKET RESEARCH</p>
            <h1>Company overview</h1>
            <p className="subtitle">
              Follow the latest news and market sentiment.
            </p>
          </div>

          <div className="search">
            <input
              value={ticker}
              onChange={e => setTicker(e.target.value.toUpperCase())}
              onKeyDown={e => e.key === 'Enter' && searchCompany()}
              placeholder="Enter ticker"
            />
            <button onClick={searchCompany} disabled={loading}>
              {loading ? 'Loading...' : 'Search'}
            </button>
          </div>
        </section>

        <section className="company-heading">
          <div>
            <p className="eyebrow">CURRENTLY VIEWING</p>
            <h2>{ticker || 'Company'}</h2>
          </div>
          <span className="market-label">US MARKET</span>
        </section>

        <section className="overview-grid">
          <div className="metric">
            <p>Articles analyzed</p>
            <h3>{total}</h3>
            <span>Articles retrieved</span>
          </div>

          <div className="metric">
            <p>Positive coverage</p>
            <h3>{positiveCount}</h3>
            <span>{positivePercentage}% of articles</span>
          </div>

          <div className="metric">
            <p>Negative coverage</p>
            <h3>{negativeCount}</h3>
            <span>{negativePercentage}% of articles</span>
          </div>
        </section>

        <section className="sentiment-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">SENTIMENT ANALYSIS</p>
              <h2>News sentiment distribution</h2>
            </div>
            <span>{total} articles analyzed</span>
          </div>

          <div className="sentiment-content">
            <div className="sentiment-summary">
              <p>Overall coverage</p>
              <h3>{overallSentiment}</h3>
            </div>

            <div className="distribution-bar">
              <div
                className="distribution-positive"
                style={{ width: `${positivePercentage}%` }}
              />
              <div
                className="distribution-neutral"
                style={{ width: `${neutralPercentage}%` }}
              />
              <div
                className="distribution-negative"
                style={{ width: `${negativePercentage}%` }}
              />
            </div>

            <div className="distribution-legend">
              <div>
                <span className="legend-dot positive-dot" />
                <span>Positive</span>
                <strong>{positivePercentage}%</strong>
              </div>

              <div>
                <span className="legend-dot neutral-dot" />
                <span>Neutral</span>
                <strong>{neutralPercentage}%</strong>
              </div>

              <div>
                <span className="legend-dot negative-dot" />
                <span>Negative</span>
                <strong>{negativePercentage}%</strong>
              </div>
            </div>
          </div>
        </section>

        <section className="news-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">LATEST COVERAGE</p>
              <h2>Company news</h2>
            </div>
            <span>Powered by Finnhub</span>
          </div>

          {loading && <p className="status-message">Loading news...</p>}

          {error && <p className="status-message error">{error}</p>}

          {!loading && !error && articles.length === 0 && (
            <div className="empty-state">
              <h3>Search for a company</h3>
              <p>
                Enter a stock ticker above to retrieve financial news
                and analyze its sentiment.
              </p>
            </div>
          )}

          <div className="article-list">
            {articles.map((article, index) => (
              <article className="article" key={article.id || index}>
                <div className="article-meta">
                  <span>{article.source || 'News source'}</span>
                  <span>{formatDate(article.datetime)}</span>
                </div>

                <h3>
                  {article.url ? (
                    <a href={article.url} target="_blank" rel="noreferrer">
                      {article.headline}
                    </a>
                  ) : article.headline}
                </h3>

                <p>{article.summary}</p>

                <div className="article-bottom">
                  <span className={`sentiment ${article.sentiment_analysis?.sentiment || 'neutral'}`}>
                    {article.sentiment_analysis?.sentiment || 'neutral'}
                  </span>

                  <span className="score">
                    Sentiment score: {article.sentiment_analysis?.score?.toFixed(2) ?? 'N/A'}
                  </span>
                </div>
              </article>
            ))}
          </div>
        </section>

        <footer>
          <span>FINSIGHT</span>
          <span>Financial news, made easier to understand.</span>
        </footer>
      </main>
    </div>
  )
}

export default App
