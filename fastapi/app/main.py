from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1.router import router as api_v1_router


app = FastAPI(
    title="SlopEngine API",
    description="Video generation API using AI",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store frontend URL in app state for OAuth redirects
app.state.frontend_url = settings.FRONTEND_URL

# Include API routers
app.include_router(api_v1_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to SlopEngine API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
