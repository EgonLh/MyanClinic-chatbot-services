from fastapi import FastAPI
from app.api.router import api_router
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title="RAG + Medicine Identifier API",
    version="1.0.0",
    description="Backend for customer support chatbot and medicine identifier",
)

# Include API routes
app.include_router(api_router)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok", "app_name": settings.APP_NAME}
