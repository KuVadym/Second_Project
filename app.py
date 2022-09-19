import uvicorn
from http import server
from fastapi import FastAPI, Request, Form, Response, Depends, APIRouter
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
from api.auth.forms import LoginForm, UserCreateForm
from api.auth.jwt import login
from api.deps.user_deps import get_current_user
from api.api_v1.hendlers.user import create_user
from fastapi.security.utils import get_authorization_scheme_param

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
api_router = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")

recordService = RecordService()

templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/signup', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post('/signup')
async def signup(response: Response, request: Request):
    if (await request.form()).get("registerName"):
        form = UserCreateForm(request)
    if (await request.form()).get("loginEmail"):
        form = LoginForm(request) 
    await form.load_data()
    if await form.is_valid():
        if type(form) == LoginForm:
            await login(form_data=form)
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("dashboard/dashboard.html", form.__dict__)
            return response
        elif type(form) == UserCreateForm:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("dashboard/dashboard.html", form.__dict__)
            await create_user(data=form)
            return response
    return templates.TemplateResponse("/signup", {"request": request})

@api_router.get('/dashboard')
async def dashboard(request: Request, user: User = Depends(get_current_user)):
    print('\n\n')
    print(user)
    print(user.id)
    print('\n')
    rec_list = await recordService.list_records(user)
    print(rec_list)
    print('\n\n')
    try:
        if request.get("current") == 'contacts':
            print('\n\n')
            print(user)
            print(user.id)
            contacts =  await recordService.list_records(user) 
            print(contacts)
            pass
        elif current == 'notes':
            pass
        elif current == 'files':
            pass
        return current_user, templates.TemplateResponse("dashboard/dashboard.html", {"request": request})
    except Exception as e:
        print(e)
        

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
app.include_router(api_router, prefix=settings.API_V1_STR)

# uvicorn app:app --reload


if __name__ == "__main__":
    config = uvicorn.Config("app:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()