from schemas.note_schema import NoteAuth
from models.models_mongo import Note, Tag, Record


class NoteService:
    print('here')
 

    @staticmethod
    async def create_note(note: NoteAuth):
        async def create_tag(note: NoteAuth):
            tag_list = []
            for tag in note.tags:
                print(tag.name)
                tag_list.append(Tag(name = tag.name))
            return tag_list
        async def create_record(note: NoteAuth):
            rec_list = []
            for rec in note.records:
                rec_list.append(Record(description = rec.description))
            return rec_list 
        tags,records = await create_tag(note), await create_record(note)
        print(note.dict())
        print(type(tags))
        print(type(records))
        note_in = Note(
            name = note.name,
            records = records,
            tags = tags
        )
        return await note_in.save()