"""
DevFolio Backend - Main Server
FastAPI application serving portfolio data and cached screenshots to the frontend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.fetch_data import get_portfolio_data

app = FastAPI(title="DevFolio API", description="Serves developer portfolio data for the DevFolio gallery.")

# Allow the frontend (any origin for now) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/portfolios")
def read_portfolios():
    """
    Returns all developer portfolios with cleaned names and parsed roles.
    Response format: { count: int, portfolios: list[dict] }
    """
    data = get_portfolio_data()
    return {"count": len(data), "portfolios": data}
