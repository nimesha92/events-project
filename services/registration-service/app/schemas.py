from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegistrationBase(BaseModel):
    event_id: int = Field(gt=0)
    attendee_name: str = Field(min_length=2, max_length=200)
    email: EmailStr
    ticket_count: int = Field(gt=0, le=10)


class RegistrationCreate(RegistrationBase):
    pass


class RegistrationResponse(RegistrationBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)