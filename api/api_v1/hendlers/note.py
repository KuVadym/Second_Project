from venv import create
from fastapi import APIRouter
from schemas.note_schema import NoteAuth
from services.note_service import NoteService
from models.models_mongo import Note


note_router = APIRouter()

@note_router.get('test')
async def test():
    return{"message": "user router working"}


@note_router.post('/create_note', summary="Create new note", response_model=Note)
async def create_note(data: NoteAuth):
    return await NoteService.create_note(data)





