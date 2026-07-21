from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProgramBase(BaseModel):
    event_id: int = Field(gt=0)
    day: str = Field(min_length=1, max_length=50)
    track: str = Field(min_length=1, max_length=100)
    session_title: str = Field(min_length=1, max_length=200)
    speaker_name: str = Field(min_length=1, max_length=200)
    room: str = Field(min_length=1, max_length=100)
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")

        return self


class ProgramCreate(ProgramBase):
    pass


class ProgramUpdate(BaseModel):
    event_id: int | None = Field(default=None, gt=0)
    day: str | None = Field(default=None, min_length=1, max_length=50)
    track: str | None = Field(default=None, min_length=1, max_length=100)
    session_title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    speaker_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    room: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    start_time: datetime | None = None
    end_time: datetime | None = None


class ProgramResponse(ProgramBase):
    id: int

    model_config = ConfigDict(from_attributes=True)