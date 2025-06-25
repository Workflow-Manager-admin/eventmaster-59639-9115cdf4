from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from typing import List

from .models import Event, EventCreate, EventUpdate
from .event_service import event_service

openapi_tags = [
    {
        "name": "events",
        "description": "Event CRUD operations",
    },
    {
        "name": "health",
        "description": "Health check endpoint",
    }
]

app = FastAPI(
    title="EventMaster Backend API",
    version="1.0.0",
    description="API for managing events, including CRUD operations.",
    openapi_tags=openapi_tags
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()


# PUBLIC_INTERFACE
@api_router.get(
    "/events/",
    response_model=List[Event],
    summary="List events",
    description="Retrieve all events.",
    tags=["events"],
    response_description="List of events"
)
def list_events():
    """
    Retrieve and return all events.
    """
    return event_service.list_events()


# PUBLIC_INTERFACE
@api_router.get(
    "/events/{event_id}",
    response_model=Event,
    summary="Get an event",
    description="Retrieve an event by its unique ID.",
    tags=["events"],
    response_description="Event details"
)
def get_event(event_id: int):
    """
    Get an event by its unique identifier.

    - **event_id**: ID of the event to retrieve.
    """
    event = event_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found.")
    return event


# PUBLIC_INTERFACE
@api_router.post(
    "/events/",
    response_model=Event,
    status_code=status.HTTP_201_CREATED,
    summary="Create an event",
    description="Create a new event and return it.",
    tags=["events"],
    response_description="Created event"
)
def create_event(event_create: EventCreate):
    """
    Create a new event.

    - **title**: Title of the event.
    - **description**: Description of the event.
    - **start_time**: Start time of the event.
    - **end_time**: End time of the event.
    - **location**: Location of the event.

    Returns the full event with its assigned unique ID.
    """
    return event_service.create_event(event_create)


# PUBLIC_INTERFACE
@api_router.put(
    "/events/{event_id}",
    response_model=Event,
    summary="Update an event",
    description="Update an existing event by ID (full update).",
    tags=["events"],
    response_description="Updated event"
)
def update_event(event_id: int, event_update: EventUpdate):
    """
    Update an event by its unique identifier.

    - **event_id**: ID of the event to update.
    - EventUpdate payload can include one or more fields to update.

    Returns the updated event.
    """
    event = event_service.update_event(event_id, event_update)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found.")
    return event


# PUBLIC_INTERFACE
@api_router.delete(
    "/events/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an event",
    description="Delete an event by its unique ID.",
    tags=["events"]
)
def delete_event(event_id: int):
    """
    Delete an event by its unique identifier.

    - **event_id**: ID of the event to delete.

    Returns 204 No Content on success.
    """
    success = event_service.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found.")


@app.get("/", tags=["health"], summary="Health check")
def health_check():
    """Simple health check endpoint."""
    return {"message": "Healthy"}

app.include_router(api_router)
