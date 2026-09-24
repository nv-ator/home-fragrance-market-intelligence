"""API routes initialization."""
from .overview import router as overview_router
from .brands import router as brands_router
from .products import router as products_router
from .analytics import router as analytics_router

__all__ = ["overview_router", "brands_router", "products_router", "analytics_router"]
