from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

# PUBLIC_INTERFACE
class EventBase(BaseModel):
    """Base data model for event input and output."""
    title: str = Field(..., description="Title of the event")
    description: Optional[str] = Field(None, description="Event description")
    start_time: datetime = Field(..., description="Start time of the event")
    end_time: datetime = Field(..., description="End time of the event")
    location: Optional[str] = Field(None, description="Location of the event")

# PUBLIC_INTERFACE
class EventCreate(EventBase):
    """Data model for creating a new event."""

# PUBLIC_INTERFACE
class EventUpdate(BaseModel):
    """Data model for updating an event (partial update allowed)."""
    title: Optional[str] = Field(None, description="Title of the event")
    description: Optional[str] = Field(None, description="Event description")
    start_time: Optional[datetime] = Field(None, description="Start time of the event")
    end_time: Optional[datetime] = Field(None, description="End time of the event")
    location: Optional[str] = Field(None, description="Location of the event")

# PUBLIC_INTERFACE
class Event(EventBase):
    """Data model representing an event (with ID)."""
    id: int = Field(..., description="Unique identifier for the event")

    class Config:
        orm_mode = True
