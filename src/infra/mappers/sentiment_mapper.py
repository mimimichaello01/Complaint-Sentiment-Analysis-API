from infra.models.complaints import Sentiment


def map_external_sentiment(api_sentiment: str) -> Sentiment:
    mapping = {
        "positive": Sentiment.POSITIVE,
        "negative": Sentiment.NEGATIVE,
        "neutral": Sentiment.NEUTRAL,
    }

    return mapping.get(api_sentiment.lower(), Sentiment.UNKNOWN)
