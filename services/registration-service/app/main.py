from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Registration Service",
    description="Microservice for attendee registration",
    version="1.0.0",
)

# Must be added immediately after app = FastAPI(...)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Routes are mounted under /api/registrations to match the ALB ingress path
# rule. The ALB ingress controller does not rewrite/strip the matched
# prefix, so the service must expose routes at the same path the ingress
# forwards.
router = APIRouter(prefix="/api/registrations")


@app.get("/")
def root():
    return {"message": "Registration Service is running"}


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


@router.post(
    "",
    response_model=schemas.RegistrationResponse,
)
def create_registration(
    registration: schemas.RegistrationCreate,
    db: Session = Depends(get_db),
):
    return crud.create_registration(db, registration)


@router.get(
    "",
    response_model=list[schemas.RegistrationResponse],
)
def list_registrations(
    db: Session = Depends(get_db),
):
    return crud.get_registrations(db)


@router.get(
    "/{registration_id}",
    response_model=schemas.RegistrationResponse,
)
def get_registration(
    registration_id: int,
    db: Session = Depends(get_db),
):
    registration = crud.get_registration(
        db,
        registration_id,
    )

    if registration is None:
        raise HTTPException(
            status_code=404,
            detail="Registration not found",
        )

    return registration


@router.delete("/{registration_id}")
def delete_registration(
    registration_id: int,
    db: Session = Depends(get_db),
):
    registration = crud.get_registration(
        db,
        registration_id,
    )

    if registration is None:
        raise HTTPException(
            status_code=404,
            detail="Registration not found",
        )

    crud.delete_registration(db, registration)

    return {"message": "Registration deleted"}

app.include_router(router)
