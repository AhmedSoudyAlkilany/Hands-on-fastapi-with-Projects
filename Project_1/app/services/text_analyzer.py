from langdetect import detect
from textblob import TextBlob
from app.schemas import LanguageCode, SentimentType, SentimentResult

class TextAnalyzerService:
    LANGUAGE_MAP = {
        'ar': LanguageCode.ARABIC,
        'en': LanguageCode.ENGLISH,
        'fr': LanguageCode.FRENCH,

    }
    def detect_language(self, text:str) -> LanguageCode:
        try:
            detected = detect(text)
            return self.LANGUAGE_MAP.get(detected, LanguageCode.UNKNOWN)
        except:
            return LanguageCode.UNKNOWN
        
    def analyze_sentiment(self, text:str) -> SentimentResult:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiment_type = SentimentType.POSITIVE
        elif polarity < -0.1:
            sentiment_type = SentimentType.NEGATIVE
        else:
            sentiment_type = SentimentType.NEUTRAL

        confidence = min(abs(polarity) *2, 1.0)


text_analyzer_service = TextAnalyzerService()