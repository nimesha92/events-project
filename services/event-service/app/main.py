from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import Base, engine, get_db

app = FastAPI(
    title="Event Service",
    description="Microservice for managing event details",
    version="1.0.0",
)

router = APIRouter(prefix="/api/events")


@app.on_event("startup")
def create_database_tables() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        # Log the error, but allow Uvicorn to start.
        print(f"Database initialization failed: {exc}")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Event Service is running"}


# Liveness check: only confirms that the application process is alive.
@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "event-service",
    }


# Readiness check: confirms that the database is reachable.
@app.get("/ready")
def readiness_check(
    db: Session = Depends(get_db),
) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "database": "connected",
        }

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        ) from exc


@router.post(
    "",
    response_model=schemas.EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
):
    return crud.create_event(db, event)


@router.get(
    "",
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


@router.get(
    "/{event_id}",
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


@router.put(
    "/{event_id}",
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


@router.delete(
    "/{event_id}",
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


app.include_router(router)