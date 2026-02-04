from fastapi import APIRouter, HTTPException, status
from app.schemas import TextAnalysisRequest, TextAnalysisResponse
from app.services.text_analyzer import text_analyzer_service

router = APIRouter(prefix="/analyze", tags=["Analysis"])

@router.post("/", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """نقطة النهاية لتحليل النص"""
    try:
        analysis_result = text_analyzer_service.analyze(
            text=request.text,
            include_keywords=request.include_keywords,
            include_summary=request.include_summary,
            max_keywords=request.max_keywords
        )
        return analysis_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في تحليل النص: {str(e)}"
        )