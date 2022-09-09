from datetime import datetime
from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField, FileField


# For notes 
class Tag(EmbeddedDocument):
    name = StringField()


# For notes
class Record(EmbeddedDocument):
    description = StringField()
    done = BooleanField(default=False)


# For notes
class Note(EmbeddedDocument):
    name = StringField()
    records = ListField(EmbeddedDocumentField(Record))
    tags = ListField(EmbeddedDocumentField(Tag))
    meta = {'allow_inheritance': True}
    created = DateTimeField(default=datetime.now())


# For records
class Emails(EmbeddedDocument):
    email = StringField()
    created = DateTimeField(default=datetime.now())


# For records
class Phones(EmbeddedDocument):
    phone = StringField()
    created = DateTimeField(default=datetime.now())


# For records
class Records(EmbeddedDocument):
    name = StringField()
    birth_date = DateTimeField(default=None)
    address = StringField()
    emails = ListField(EmbeddedDocumentField(Emails))
    phones = ListField(EmbeddedDocumentField(Phones))
    created = DateTimeField(default=datetime.now())


# For files
class File(EmbeddedDocument):
    file = FileField()
    created = DateTimeField(default=datetime.now())


# For user registration
class Genders(EmbeddedDocument):
    gender = StringField()
    created = DateTimeField(default=datetime.now())


# For user registration
class MaritalStastus(EmbeddedDocument):
    status = StringField() 
    created = DateTimeField(default=datetime.now())


# For user registration
class Users(EmbeddedDocument):
    given_name = StringField()
    surname = StringField()
    gender = ListField(EmbeddedDocumentField(Genders)) # (male, famale)
    address = StringField()
    email = StringField()
    phone = StringField()
    marital_status = ListField(EmbeddedDocumentField(MaritalStastus))  # (single, maried)
    created = DateTimeField(default=datetime.now())
    

# For authorization
class User(Document):
    name = StringField()
    # password = StringField()
    records = ListField(EmbeddedDocumentField(Records))
    notes = ListField(EmbeddedDocumentField(Note))
    files = ListField(EmbeddedDocumentField(File))
    created = DateTimeField(default=datetime.now())


# For news
class News(Document):
    title = StringField()
    text = StringField()
    link = StringField()
    date = DateTimeField()
    created = DateTimeField(default=datetime.now())
