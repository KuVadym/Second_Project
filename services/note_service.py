from schemas.note_schema import NoteAuth
from models.models_mongo import Note

class NoteService:
    @staticmethod
    async def create_note(note: NoteAuth):
        note_in = Note(
            name = note.name,
            records = note.records,
            tags = note.tags
        )
        await note_in.save()
        return note_in