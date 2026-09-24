import sqlite3
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.database import get_db
from api.schemas import HealthResponse
from api.routes import overview_router, brands_router, products_router, analytics_router

app = FastAPI(
    title="Home Fragrance Market Intelligence API",
    description="""
Analytical REST API powering the Home Fragrance Market Intelligence and Brand Positioning dashboard.
Serves validated, factual product metrics, normalized unit pricing, and empirical distributions across 5 competitor brands.
    """,
    version="1.0.0"
)

# CORS Configuration for local React development
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route Registrations
app.include_router(overview_router)
app.include_router(brands_router)
app.include_router(products_router)
app.include_router(analytics_router)

@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
def health_check(db: sqlite3.Connection = Depends(get_db)):
    """Verifies that the analytical API and underlying SQLite database connection are operational."""
    cursor = db.cursor()
    cursor.execute("SELECT 1;").fetchone()
    return HealthResponse(status="ok", database="connected")
