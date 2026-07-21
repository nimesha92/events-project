from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Registration Service",
    description="Microservice for attendee registration",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")


@app.get("/")
def root():
    return {"message": "Registration Service is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@router.post(
    "/registrations",
    response_model=schemas.RegistrationResponse,
)
def create_registration(
    registration: schemas.RegistrationCreate,
    db: Session = Depends(get_db),
):
    return crud.create_registration(db, registration)


@router.get(
    "/registrations",
    response_model=list[schemas.RegistrationResponse],
)
def list_registrations(
    db: Session = Depends(get_db),
):
    return crud.get_registrations(db)


@router.get(
    "/registrations/{registration_id}",
    response_model=schemas.RegistrationResponse,
)
def get_registration(
    registration_id: int,
    db: Session = Depends(get_db),
):
    registration = crud.get_registration(db, registration_id)

    if registration is None:
        raise HTTPException(
            status_code=404,
            detail="Registration not found",
        )

    return registration


@router.delete("/registrations/{registration_id}")
def delete_registration(
    registration_id: int,
    db: Session = Depends(get_db),
):
    registration = crud.get_registration(db, registration_id)

    if registration is None:
        raise HTTPException(
            status_code=404,
            detail="Registration not found",
        )

    crud.delete_registration(db, registration)

    return {"message": "Registration deleted"}


app.include_router(router)