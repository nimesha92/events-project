from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EventBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    venue: str = Field(min_length=1, max_length=200)
    event_datetime: datetime
    ticket_price: float = Field(ge=0)
    capacity: int = Field(gt=0)
    seats_available: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_seats(self):
        if self.seats_available > self.capacity:
            raise ValueError(
                "seats_available cannot be greater than capacity"
            )

        return self


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    venue: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    event_datetime: datetime | None = None
    ticket_price: float | None = Field(default=None, ge=0)
    capacity: int | None = Field(default=None, gt=0)
    seats_available: int | None = Field(default=None, ge=0)


class EventResponse(EventBase):
    id: int

    model_config = ConfigDict(from_attributes=True)