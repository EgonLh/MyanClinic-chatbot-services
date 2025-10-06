from fastapi import APIRouter
from app.api import chatbot, medicine

api_router = APIRouter()

# Register all sub-routers
api_router.include_router(chatbot.router)
api_router.include_router(medicine.router)
