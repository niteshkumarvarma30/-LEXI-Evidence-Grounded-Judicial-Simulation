from pydantic import BaseModel


class IncidentIn(BaseModel):
    title: str
    description: str


class ClaimIn(BaseModel):
    case_id: int
    side: str
    text: str
