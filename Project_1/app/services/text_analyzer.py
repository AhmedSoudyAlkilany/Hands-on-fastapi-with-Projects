import time
from typing import Tuple, List
from langdetect import detect, DetectorFactory
from textblob import TextBlob
from app.schemas import LanguageCode, SentimentType, SentimentResult, TextAnalysisResponse

DetectorFactory.seed = 0

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

        return SentimentResult(
            type=sentiment_type,
            score=round(polarity,3),
            confidence=round(min(abs(polarity)*2, 1.0),3)
        )
    def extract_keywords(self, text: str, max_count: int = 5) -> List[str]:
        """استخراج الكلمات المفتاحية"""
        blob = TextBlob(text)
        noun_phrases = list(blob.noun_phrases)
        
        if noun_phrases:
            return noun_phrases[:max_count]
        
        # fallback: الكلمات الطويلة
        words = [w.lower() for w in blob.words if len(w) > 3]
        word_freq = {}
        for w in words:
            word_freq[w] = word_freq.get(w, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in sorted_words[:max_count]]
    
    def generate_summary(self, text: str) -> str:
        """ملخص بسيط"""
        blob = TextBlob(text)
        sentences = list(blob.sentences)
        if len(sentences) <= 2:
            return text
        return " ".join(str(s) for s in sentences[:2])
    
    def get_stats(self, text: str) -> Tuple[int, int]:
        """إحصائيات"""
        blob = TextBlob(text)
        return len(blob.words), len(text)
    
    def analyze(
        self,
        text: str,
        include_keywords: bool = True,
        include_summary: bool = False,
        max_keywords: int = 5
    ) -> TextAnalysisResponse:
        """الدالة الرئيسية - تجمع كل التحليلات"""
        start_time = time.time()
        
        language = self.detect_language(text)
        sentiment = self.analyze_sentiment(text)
        word_count, char_count = self.get_stats(text)
        
        keywords = self.extract_keywords(text, max_keywords) if include_keywords else None
        summary = self.generate_summary(text) if include_summary else None
        
        processing_time = (time.time() - start_time) * 1000
        
        return TextAnalysisResponse(
            original_text=text,
            language=language,
            word_count=word_count,
            character_count=char_count,
            sentiment=sentiment,
            keywords=keywords,
            summary=summary,
            processing_time_ms=round(processing_time, 2)
        )


text_analyzer_service = TextAnalyzerService()