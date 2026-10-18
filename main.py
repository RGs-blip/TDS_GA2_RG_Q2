from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uuid

ALLOWED_ORIGIN = "https://dash-c8f9km.example.com"
YOUR_EMAIL = "23f1001344@ds.study.iitm.ac.in"

app = FastAPI()

# Strict CORS: only this exact origin is allowed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Every response gets a unique request ID and processing time.
@app.middleware("http")
async def add_required_headers(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    elapsed = time.perf_counter() - start
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{max(elapsed, 0):.6f}"
    return response


@app.get("/stats")
def get_stats(values: str = Query(...)):
    try:
        numbers = [int(x.strip()) for x in values.split(",") if x.strip() != ""]
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "values must be comma-separated integers"},
        )

    if not numbers:
        return JSONResponse(
            status_code=400,
            content={"error": "values must contain at least one integer"},
        )

    count = len(numbers)
    total = sum(numbers)

    return {
        "email": YOUR_EMAIL,
        "count": count,
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / count,
    }