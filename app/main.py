from fastapi import FastAPI

app = FastAPI(title="Lab1 - Fastapi User Api")

@app.get("/health")
def health():
    return{"status": "ok"}

@app.get("/hello")
def hello():
    return{"status": "Good Morning World"}
