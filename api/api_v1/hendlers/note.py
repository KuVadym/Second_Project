from venv import create
from fastapi import APIRouter
from schemas.note_schema import NoteAuth
from services.note_service import NoteService


note_router = APIRouter()

@note_router.get('test')
async def test():
    return{"message": "user router working"}


@note_router.post('/create', summary="Create new note")
async def create_note(data: NoteAuth):
    return await NoteService.create_note(data)




