
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    # Calculate sentiment scores for the text
    scores = analyzer.polarity_scores(text)

    # Get the overall compound score
    compound = scores["compound"]

    # Classify the sentiment
    if compound >= 0.05:
        sentiment = "positive"
    elif compound <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # Return the sentiment and its score
    return {
        "sentiment": sentiment,
        "score": compound
    }

