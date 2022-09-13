from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.models_mongo import Emails, Record, Note, Tag, Phones, Records, User
from api.api_v1.router import router


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# uvicorn app:app --reload
@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
async def app_init():
    """
        initialize crucial application services
    """

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).MyHelperMongoDB

    await init_beanie(
        database=db_client,
        document_models= [
            Note, Tag, Record, Emails, Phones, Records, User
        ]
    )


app.include_router(router, prefix=settings.API_V1_STR)


# @app.get('/all')
# def show_all_notes():
#     result = db.note.find({}, {'_id': 0, 'name': 1},)
#     count_notes = db.note.estimated_document_count()
#     print (f'You have {count_notes} notes:')
#     if result:
#         for el in result:
#             print(str(el.values())[14:-3])
#     else:
#         print('not found data')