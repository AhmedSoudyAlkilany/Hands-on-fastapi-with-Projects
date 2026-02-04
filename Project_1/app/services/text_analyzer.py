from langdetect import detect
from app.schemas import LanguageCode

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
        
text_analyzer_service = TextAnalyzerService()