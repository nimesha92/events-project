from sqlalchemy.orm import Session
from .notifications import trigger_low_seat_notification

from . import models, schemas


def create_event(
    db: Session,
    event: schemas.EventCreate,
) -> models.Event:
    db_event = models.Event(**event.model_dump())

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event


def get_events(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Event]:
    return (
        db.query(models.Event)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_event(
    db: Session,
    event_id: int,
) -> models.Event | None:
    return (
        db.query(models.Event)
        .filter(models.Event.id == event_id)
        .first()
    )


def update_event(
    db: Session,
    db_event: models.Event,
    event_update: schemas.EventUpdate,
) -> models.Event:
    update_data = event_update.model_dump(
        exclude_unset=True
    )

    new_capacity = update_data.get(
        "capacity",
        db_event.capacity,
    )

    new_seats = update_data.get(
        "seats_available",
        db_event.seats_available,
    )

    if new_seats > new_capacity:
        raise ValueError(
            "seats_available cannot be greater than capacity"
        )

    for field, value in update_data.items():
        setattr(db_event, field, value)

    db.commit()
    db.refresh(db_event)

# Trigger serverless notification if seats are low
    if  db_event.seats_available < 10:
        trigger_low_seat_notification(
        db_event.id,
        db_event.seats_available
    )

    return db_event


def delete_event(
    db: Session,
    db_event: models.Event,
) -> None:
    db.delete(db_event)
    db.commit()