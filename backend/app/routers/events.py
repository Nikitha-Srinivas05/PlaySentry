from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event
from app.schemas import EventCreate, EventOut

router = APIRouter(prefix="/v1", tags=["events"])


@router.post("/events", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def ingest_event(payload: EventCreate, db: Session = Depends(get_db)):
    event = Event(
        timestamp=payload.timestamp,
        source=payload.source,
        event_type=payload.event_type,
        src_ip=str(payload.src_ip) if payload.src_ip else None,
        username=payload.username,
        details=payload.details,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event