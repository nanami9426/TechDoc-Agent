from fastapi import FastAPI

app = FastAPI(title="TechDoc Agent API")

@app.get("/")
def root():
    return {"message": "TechDoc Agent"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}