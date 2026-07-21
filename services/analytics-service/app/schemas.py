from pydantic import BaseModel, Field


class AnalyticsEvent(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    event_type: str = Field(min_length=1, max_length=100)
    page: str = Field(min_length=1, max_length=200)
    element: str = Field(min_length=1, max_length=200)
    user_agent: str = Field(min_length=1, max_length=500)


class AnalyticsResponse(BaseModel):
    message: str