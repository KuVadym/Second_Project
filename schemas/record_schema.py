from typing import List
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from models.models_mongo import Emails, Phones



class RecordAuth(BaseModel):
    id: UUID = Field(...,)
    name: str = Field(...,)
    # birth_date: datetime
    address: str = Field(...,)
    emails: List[Emails]
    phones: List[Phones]

    