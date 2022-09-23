from multiprocessing import context
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
from schemas.note_schema import NoteAuth
from schemas.record_schema import RecordAuth
from schemas.user_schema import UserAuth
from services.record_service import RecordService
from services.user_service import UserService
from services.note_service import NoteService
from api.auth.forms import ContactDeleteForm, ContactUpdateForm, FileUploadForm, LoginForm, UserCreateForm, ContactCreateForm, NoteCreateForm, NoteDeleteForm, NoteUpdateForm
from api.auth.jwt import login
from api.deps.user_deps import get_current_user
from api.api_v1.hendlers.user import create_user
from fastapi.security.utils import get_authorization_scheme_param
import time
from threading import Thread
from scrap.scrap import scraping
from models.models_mongo import User
from api.api_v1.hendlers.record import delete, list, create_record, update
from api.api_v1.hendlers import note

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
noteService = NoteService()
templates = Jinja2Templates(directory="templates")

@api_router.post('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request):
    token = request._cookies.get("access_token").split(" ")[1]
    user = await get_current_user(token)
    x = await list(user)
    print(x)
    # rec = await Records.find(Records.owner.id == user.id).to_list()
    # print(rec)
    return templates.TemplateResponse("dashboard/dashboard.html", context={"request": request})




@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    
    if (request._cookies.get("access_token")) :
        token = request._cookies.get("access_token").split(" ")[1]
        user = await get_current_user(token)
        return  templates.TemplateResponse("index.html", {"request": request, "valute": valute, "news": news, "sport": sport, "weather": weather, "user":user.__dict__})
  

    return templates.TemplateResponse("index.html", {"request": request, "valute": valute, "news": news, "sport": sport, "weather": weather,})

@app.post('/',response_class=HTMLResponse)
async def home(request: Request):
    token = request._cookies.get("access_token").split(" ")[1]
    user = await get_current_user(token)
 
    x = await list(user)
    print(x)
    return templates.TemplateResponse("index.html", {"request": request, "valute": valute, "news": news, "sport": sport, "weather": weather, "user": user.__dict__})

@app.get('/signup', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get('/contacts', response_class=HTMLResponse)
async def contacts(request: Request):
    token = request._cookies.get("access_token").split(" ")[1]
    user = await get_current_user(token)

    if not user:
        return responses.RedirectResponse('/signup')

 
    list_records = await list(user)
    
    return templates.TemplateResponse("contacts/contacts.html", {"request": request, "user": user.__dict__, "list":list_records,})


# @app.get('/delete/{id}', response_class=HTMLResponse)
# async def contacts(request: Request):
#     print(id)
#     return


@app.post('/contacts', response_class=HTMLResponse)
async def contacts(request: Request):
    x = await (request.form())
    print(x)
    if (await request.form()).get("name"):
        form = ContactCreateForm(request)
    if (await request.form()).get("new_contact-id"):
        form = ContactUpdateForm(request)  
    if (await request.form()).get("contact-id"):
        form = ContactDeleteForm(request)
    await form.load_data()
    token = request._cookies.get("access_token").split(" ")[1]
    user = await get_current_user(token)
    if not user:
        return responses.RedirectResponse('/signup')
    if type(form) == ContactCreateForm:
        if await form.is_valid():
            data = RecordAuth(name=form.name, birth_date=form.birth_date, address=form.address, emails=[Emails(email=form.email)], phones=[Phones(phone=form.phones)])
            new_contact = await create_record(data=data ,current_user=user)
        else:
            pass 
    list_records = await list(user)
    if type(form) == ContactUpdateForm:
        print(type(form))
        print(form.__dict__)
        data = RecordAuth(name=form.name, birth_date=form.birth_date, address=form.address, emails=[Emails(email=form.email)], phones=[Phones(phone=form.phones)])
        await update(record_id=form.id, data=data, current_user=user) # form.id()
    if type(form) == ContactDeleteForm:
        await delete(record_id=form.id, current_user=user)
    list_records = await list(user)
    return templates.TemplateResponse("contacts/contacts.html", {"request": request, "user": user.__dict__, "list":list_records})


@app.get('/notes', response_class=HTMLResponse)
async def notes(request: Request):
    token = request._cookies.get("access_token").split(" ")[1]
    user = await get_current_user(token)
    if not user:
        return responses.RedirectResponse('/signup')
    notes = await noteService.list_notes(user) 
    return templates.TemplateResponse("notes/notes_dashboard.html", {"request": request, "user": user.__dict__,"notes":notes})

@app.post('/notes', response_class=HTMLResponse)
async def notes(request: Request):
    x = await request.form()
    print(x)
    if (await request.form()).get("note-has-title"):
        form = NoteCreateForm(request)
    if (await request.form()).get("new_note-id"):
        form = NoteUpdateForm(request)  
    if (await request.form()).get("note-id"):
        form = NoteDeleteForm(request)
    print(form)
    await form.load_data()
    token = request._cookies.get("access_token").split(" ")[1]
    user = await get_current_user(token)
    if not user:
        return responses.RedirectResponse('/signup')
    if type(form) == NoteCreateForm:
        data = NoteAuth(name=form.title, records=[Record(description=form.description)], tags=[Tag(name="")])
        new_note = await note.create_note(data=data, current_user=user)
    if type(form) == NoteUpdateForm:
        data = NoteAuth(name=form.title, records=[Record(description=form.description)])
        new_note = await note.update(note_id=form.id, data=data, current_user=user)
    if type(form) == NoteDeleteForm:
        print("delete form\n")
        print(form.__dict__)
        await note.delete(note_id=form.id, current_user=user)
    notes = await noteService.list_notes(user) 
    return templates.TemplateResponse("notes/notes_dashboard.html", {"request": request, "user": user.__dict__,})  

# @app.get("/delete_note/{note_id}", response_class=RedirectResponse)
# async def add(request: Request,response, note_id: int,):

#     token = request._cookies.get("access_token").split(" ")[1]
#     user = await get_current_user(token)
#     if not user:
#         return responses.RedirectResponse('/signup')
#     print(note_id)
#     # deleteNote = await noteService.delete_note(user, f'{note_id}')

#     print(deleteNote)
    
#     return response.RedirectResponse('/notes')  


@app.get('/files', response_class=HTMLResponse)
async def files(request: Request):
    
    token = request._cookies.get("access_token").split(" ")[1]
    user = await get_current_user(token)
    if not user:
        return responses.RedirectResponse('/signup')

    return templates.TemplateResponse("files/files.html", {"request": request,  "user": user.__dict__,})

@app.post('/files', response_class=HTMLResponse)
async def files(request: Request):
    
    token = request._cookies.get("access_token").split(" ")[1]
    user = await get_current_user(token)
    if not user:
        return responses.RedirectResponse('/signup')

    return templates.TemplateResponse("files/files.html", {"request": request,  "user": user.__dict__,})

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
            token = await login(response=response, form_data=form)
            redirectresponse = responses.RedirectResponse('/')
            redirectresponse.set_cookie(key="access_token", value=f'Bearer {token.get("access_token")}')
            return redirectresponse
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
    config = uvicorn.Config("app:app", port=8000, log_level="info", reload=True, host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()
