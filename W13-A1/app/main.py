"""FastAPI application for LLM-powered CV feedback and optimization."""

from __future__ import annotations

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.config import get_settings
from app.schemas import AnalyzeRequest, CVFeedback, OptimizeRequest, OptimizeResponse
from app.services.cv_document import build_cv_docx_bytes
from app.services.cv_feedback import CVFeedbackService
from app.services.cv_parser import extract_text_from_file

settings = get_settings()
feedback_service = CVFeedbackService(settings)

app = FastAPI(
    title=settings.app_name,
    description="Analyze a CV, generate constructive feedback, and produce an optimized CV.",
    version="1.0.0",
)


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "llm_mode": settings.llm_mode,
        "model": settings.gemini_model,
    }


@app.post("/api/cv/analyze", response_model=CVFeedback)
async def analyze_cv(payload: AnalyzeRequest) -> dict:
    try:
        return await feedback_service.analyze(payload.cv_text, payload.target_role)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/api/cv/analyze-file", response_model=CVFeedback)
async def analyze_cv_file(
    file: UploadFile = File(...),
    target_role: str = Form("Software Engineer"),
) -> dict:
    try:
        content = await file.read()
        cv_text = extract_text_from_file(file.filename or "cv.txt", content)
        return await feedback_service.analyze(cv_text, target_role)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/api/cv/optimize", response_model=OptimizeResponse)
async def optimize_cv(payload: OptimizeRequest) -> dict:
    try:
        return await feedback_service.optimize(payload.cv_text, payload.target_role)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/api/cv/optimize-docx")
async def optimize_cv_docx(payload: OptimizeRequest) -> StreamingResponse:
    try:
        result = await feedback_service.optimize(payload.cv_text, payload.target_role)
        document_bytes = build_cv_docx_bytes(result["optimized_cv_text"])
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    headers = {"Content-Disposition": 'attachment; filename="optimized_cv.docx"'}
    return StreamingResponse(
        iter([document_bytes]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers,
    )

