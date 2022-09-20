import uvicorn
from http import server
from fastapi import FastAPI, Request, Form, Response, Depends, APIRouter, responses
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.models_mongo import Emails, Record, Note, Tag, Phones, Records, User
from api.api_v1.router import router
from schemas.user_schema import UserAuth
from services.record_service import RecordService
from services.user_service import UserService
from api.auth.forms import LoginForm, UserCreateForm
from api.auth.jwt import login
from api.deps.user_deps import get_current_user
from api.api_v1.hendlers.user import create_user
from fastapi.security.utils import get_authorization_scheme_param
import time
from threading import Thread
from scrap.scrap import scraping

valute = {}
news = {}
sport = {}
weather = {}

def main_scrap():
    while True:
        global valute, news, sport, weather
        valute, news, sport, weather = scraping()
        time.sleep(900)  # перезапуск каждые 15 минут

Thread(target=main_scrap, args=()).start()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
api_router = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")

recordService = RecordService()
userService = UserService()
templates = Jinja2Templates(directory="templates")




@app.post('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request):
    user = await get_current_user(token=(request._cookies.get('access_token')).split(' ')[1])
    print(user)
    return templates.TemplateResponse("dashboard/dashboard.html", context={"request": request})

# @app.get('/dashboard', response_class=HTMLResponse)
# async def dashboard(request: Request):
#     print(request)
#     print(request.headers)
#     rec_list = await recordService.list_records(current_user)
#     print(rec_list)
#     return templates.TemplateResponse("dashboard/dashboard.html", context={"request": request})



@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "valute": valute, "news": news, "sport": sport, "weather": weather})

@app.get('/signup', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get('/dashboard')
async def dashboard(request: Request, response: Response,):

    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request})


@app.post('/signup')
async def signup(request: Request):
    if (await request.form()).get("registerName"):
        form = UserCreateForm(request)
    if (await request.form()).get("loginEmail"):
        form = LoginForm(request) 
    await form.load_data()
    if await form.is_valid():
        if type(form) == LoginForm:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("dashboard/dashboard.html", form.__dict__)
            await login(response=response, form_data=form)
            return responses.RedirectResponse('/api/v1/dashboard')
        elif type(form) == UserCreateForm:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("dashboard/dashboard.html", form.__dict__)
            await create_user(data=form)
            return response
    return templates.TemplateResponse("/signup", context={"request": request})


        

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
web_router = APIRouter()
web_router.include_router(router=api_router, prefix='', tags=["web-app"])
app.include_router(web_router, prefix=settings.API_V1_STR)
app.include_router(router, prefix=settings.API_V1_STR)


# uvicorn app:app --reload
if __name__ == "__main__":
    config = uvicorn.Config("app:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()
    
