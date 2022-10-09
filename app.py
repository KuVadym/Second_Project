import uvicorn
from http import server
from fastapi import FastAPI, Request, APIRouter, responses
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.models_mongo import *
from api.api_v1.router import router
from schemas.note_schema import NoteAuth
from schemas.record_schema import RecordAuth
from services.record_service import RecordService
from services.user_service import UserService
from services.note_service import NoteService
from api.auth.forms import *
from api.auth.jwt import login, refresh_token
from api.deps.user_deps import get_current_user
from api.api_v1.hendlers.user import create_user
import time
from threading import Thread
from scrap.scrap import scraping
from api.api_v1.hendlers.record import *
from api.api_v1.hendlers import note
from services.dbox import *

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
api_router = APIRouter()


app.mount("/static", StaticFiles(directory="static"), name="static")

@api_router.on_event("startup")
async def app_init():
    """
        initialize crucial application services
    """
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).MyHelperMongoDB
    await init_beanie(
        database=db_client,
        document_models= [Note, Tag, Record, Emails, Phones, Records, User])


app.include_router(router=api_router, prefix='', tags="")
app.include_router(router, prefix=settings.API_V1_STR)


# uvicorn app:app --reload
if __name__ == "__main__":
    config = uvicorn.Config("app:app", 
                            port=8000, 
                            log_level="info", 
                            reload=True, 
                            host="127.0.0.1")
    server = uvicorn.Server(config)
    server.run()
