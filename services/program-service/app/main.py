from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Program Service",
    description="Microservice for managing event program sessions",
    version="1.0.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Program Service is running"}


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
    "/programs",
    response_model=schemas.ProgramResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_program(
    program: schemas.ProgramCreate,
    db: Session = Depends(get_db),
):
    return crud.create_program(db, program)


@app.get(
    "/programs",
    response_model=list[schemas.ProgramResponse],
)
def list_programs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_programs(db, skip, limit)


@app.get(
    "/programs/event/{event_id}",
    response_model=list[schemas.ProgramResponse],
)
def list_programs_for_event(
    event_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_programs_by_event(db, event_id)


@app.get(
    "/programs/{program_id}",
    response_model=schemas.ProgramResponse,
)
def read_program(
    program_id: int,
    db: Session = Depends(get_db),
):
    db_program = crud.get_program(db, program_id)

    if db_program is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found",
        )

    return db_program


@app.put(
    "/programs/{program_id}",
    response_model=schemas.ProgramResponse,
)
def update_program(
    program_id: int,
    program_update: schemas.ProgramUpdate,
    db: Session = Depends(get_db),
):
    db_program = crud.get_program(db, program_id)

    if db_program is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found",
        )

    try:
        return crud.update_program(
            db,
            db_program,
            program_update,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@app.delete(
    "/programs/{program_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_program(
    program_id: int,
    db: Session = Depends(get_db),
):
    db_program = crud.get_program(db, program_id)

    if db_program is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found",
        )

    crud.delete_program(db, db_program)

    return None