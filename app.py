import uvicorn
from http import server
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.models_mongo import Emails, Record, Note, Tag, Phones, Records, User
from api.api_v1.router import router
from schemas.user_schema import UserAuth
from services.record_service import RecordService
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

recordService = RecordService()

templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    print(router)
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/signup', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post('/signup')
async def signup(request: Request, form=Form(...)):
    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

@app.get('/dashboard')
async def dashboard(request: Request, current: str | None):
    if current == 'contacts':
        
        contacts =  await recordService.list_records(user) 
        print(contacts)
        pass
    elif current == 'notes':
        pass
    elif current == 'files':
        pass
    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

@app.get('/presentation', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("presentation.html", {"request": request})

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


# uvicorn app:app --reload


if __name__ == "__main__":
    config = uvicorn.Config("app:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()