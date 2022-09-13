from datetime import datetime
# from mongoengine import EmbeddedDocument, Document
# from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField, FileField
from typing import Optional
from beanie import Document, Indexed, Link
from pydantic import  BaseModel, EmailStr, Field
from uuid import UUID, uuid4


class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    first_name: Optional[str] = None 
    last_name: Optional[str] = None
    disabled: Optional[bool] = None
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False
    
    @property
    def create(self) -> datetime:
        return self.id.generation_time
    
    @classmethod
    async def by_email(self, email: str) -> "User":
        return await self.find_one(self.email == email)
    
    class Collection:
        name = "users"


class Tag(Document):
    id: UUID = Field(default_factory=uuid4, unique=True)
    name: str
    class Colltction:
        name = 'tag'

class Record(Document):
    id: UUID = Field(default_factory=uuid4, unique=True)
    description: str
    # done: bool
    class Colltction:
        name = 'record'

class Note(Document):
    id: UUID = Field(default_factory=uuid4, unique=True)
    name: str
    records: list[Optional[Link[Record]]]
    tags: list[Optional[Link[Tag]]]
    owner: Link[User]
    # created = DateTimeField(default=datetime.now()) # Now I don't know how do datatime in project. Try understand it.
    class Colltction:
        name = 'note'


class Emails(Document):
    id: UUID = Field(default_factory=uuid4, unique=True)
    email: EmailStr
    class Colltction:
        name = 'email'

class Phones(Document):
    id: UUID = Field(default_factory=uuid4, unique=True)
    phone: str
    class Colltction:
        name = 'phone'

class Records(Document):
    id: UUID = Field(default_factory=uuid4, unique=True)
    name = str
    # Now I don't know how do datatime in project. Try understand it.
    # birth_date: datetime = Field(default_factory=None) 
    address = str
    emails = list[Optional[Link[Emails]]]
    phones = list[Optional[Link[Phones]]]
    owner: Link[User]
    class Colltction:
        name = 'records'


class File(Document): # Now I don't know how it shoud work 
    file = str
