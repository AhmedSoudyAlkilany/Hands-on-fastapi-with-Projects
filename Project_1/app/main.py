from fastapi import FastAPI

app = FastAPI(title="AI Text Analyzer")

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}