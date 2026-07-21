from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Event Service",
    description="Microservice for managing event details",
    version="1.0.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "Event Service is running"
    }


@app.get("/health")
def health_check(
    db: Session = Depends(get_db),
) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        ) from exc


@app.post(
    "/events",
    response_model=schemas.EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
):
    return crud.create_event(db, event)


@app.get(
    "/events",
    response_model=list[schemas.EventResponse],
)
def list_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_events(
        db,
        skip=skip,
        limit=limit,
    )


@app.get(
    "/events/{event_id}",
    response_model=schemas.EventResponse,
)
def read_event(
    event_id: int,
    db: Session = Depends(get_db),
):
    db_event = crud.get_event(db, event_id)

    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    return db_event


@app.put(
    "/events/{event_id}",
    response_model=schemas.EventResponse,
)
def update_event(
    event_id: int,
    event_update: schemas.EventUpdate,
    db: Session = Depends(get_db),
):
    db_event = crud.get_event(db, event_id)

    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    try:
        return crud.update_event(
            db,
            db_event,
            event_update,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@app.delete(
    "/events/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
):
    db_event = crud.get_event(db, event_id)

    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    crud.delete_event(db, db_event)

    return None

