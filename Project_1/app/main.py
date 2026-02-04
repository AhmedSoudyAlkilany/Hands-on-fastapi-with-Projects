import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import analyze


app = FastAPI(
    title="AI Text Analyzer",
    description= "API لتحيل النصوص",
    version="1.0.0"
    )
# إعدادات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Middleware لقياس الوقت
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{(time.time() - start) * 1000:.2f}ms"
    return response

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )


# تسجيل Router
app.include_router(analyze.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

@app.get("/health")
def health():
    return {"status": "healthy"}