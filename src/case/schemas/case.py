from typing import List
import uuid

from pydantic import BaseModel


class CaseBase(BaseModel):
    title: str
    description: str
    price: float

class CaseRead(CaseBase):
    id: uuid.UUID
    images: List[str]

class CaseCreate(CaseBase):
    ...

class CaseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None