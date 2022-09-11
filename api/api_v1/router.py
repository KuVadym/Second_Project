from fastapi import APIRouter
from .hendlers import note

router = APIRouter()

router.include_router(note.note_router, prefix='/notes', tags=['notes'])