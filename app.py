from fastapi import FastAPI
from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.models_mongo import Record, Note, Tag
from api.api_v1.router import router


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# uvicorn app:app --reload
@app.get('/')
async def hello():
    return {"messege": "Hello, world"}


@app.on_event("startup")
async def app_init():
    """
        initialize crucial application services
    """

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).MyHelperMongoDB

    await init_beanie(
        database=db_client,
        document_models= [
            Record, Note, Tag
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