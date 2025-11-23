import re
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download required NLTK data
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

def get_sentiment_score(transcript: str) -> float:
    """
    Get sentiment score using VADER
    Returns positive sentiment probability (0 to 1)
    """
    try:
        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(transcript)
        # Return the positive compound score
        positive_score = max(0, scores['compound'])  # Normalize to 0-1
        return positive_score
    except:
        return 0.5  # Neutral fallback

def score_engagement(transcript: str) -> dict:
    """
    Score engagement based on sentiment analysis (0-15 points)
    >=0.9: 15 pts (Excellent)
    0.7-0.89: 12 pts (Very Good)
    0.5-0.69: 9 pts (Good)
    0.3-0.49: 6 pts (Fair)
    <0.3: 3 pts (Poor)
    """
    sentiment_score = get_sentiment_score(transcript)
    
    if sentiment_score >= 0.9:
        score = 15
        level = "Excellent"
        sentiment_level = "Very Positive/Enthusiastic"
    elif sentiment_score >= 0.7:
        score = 12
        level = "Very Good"
        sentiment_level = "Positive/Confident"
    elif sentiment_score >= 0.5:
        score = 9
        level = "Good"
        sentiment_level = "Mostly Positive"
    elif sentiment_score >= 0.3:
        score = 6
        level = "Fair"
        sentiment_level = "Neutral/Mixed"
    else:
        score = 3
        level = "Poor"
        sentiment_level = "Negative/Disinterested"
    
    feedback = f"Engagement: {level} - Sentiment: {sentiment_level} (Score: {sentiment_score:.3f})"
    
    return {
        'sentiment': score,
        'total': score,
        'feedback': feedback,
        'metrics': {
            'sentiment_score': sentiment_score,
            'sentiment_level': sentiment_level
        }
    }
