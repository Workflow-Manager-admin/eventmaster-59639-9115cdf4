from typing import List, Dict, Optional
from threading import Lock
from .models import Event, EventCreate, EventUpdate
from datetime import datetime

# Thread-safe, in-memory event storage
class EventService:
    """Handles business logic for event management (in-memory)."""

    def __init__(self):
        self._events: Dict[int, Event] = {}
        self._id_counter: int = 1
        self._lock = Lock()

    # PUBLIC_INTERFACE
    def list_events(self) -> List[Event]:
        """Return all events."""
        with self._lock:
            return list(self._events.values())

    # PUBLIC_INTERFACE
    def get_event(self, event_id: int) -> Optional[Event]:
        """Return a specific event by ID."""
        with self._lock:
            return self._events.get(event_id)

    # PUBLIC_INTERFACE
    def create_event(self, event_create: EventCreate) -> Event:
        """Create a new event and return it with its ID."""
        with self._lock:
            event = Event(
                id=self._id_counter,
                **event_create.model_dump()
            )
            self._events[self._id_counter] = event
            self._id_counter += 1
            return event

    # PUBLIC_INTERFACE
    def update_event(self, event_id: int, event_update: EventUpdate) -> Optional[Event]:
        """Update an event by ID. Supports partial update."""
        with self._lock:
            event = self._events.get(event_id)
            if not event:
                return None
            update_data = event_update.model_dump(exclude_unset=True)
            updated_event_values = event.model_dump()
            updated_event_values.update(update_data)
            updated_event = Event(**updated_event_values)
            self._events[event_id] = updated_event
            return updated_event

    # PUBLIC_INTERFACE
    def delete_event(self, event_id: int) -> bool:
        """Delete an event by ID."""
        with self._lock:
            if event_id in self._events:
                del self._events[event_id]
                return True
            return False


# Singleton instance
event_service = EventService()
