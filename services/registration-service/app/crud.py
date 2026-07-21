from sqlalchemy.orm import Session

from . import models, schemas


def create_registration(
    db: Session,
    registration: schemas.RegistrationCreate,
) -> models.Registration:
    db_registration = models.Registration(
        **registration.model_dump()
    )

    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)

    return db_registration


def get_registrations(
    db: Session,
) -> list[models.Registration]:
    return db.query(models.Registration).all()


def get_registration(
    db: Session,
    registration_id: int,
) -> models.Registration | None:
    return (
        db.query(models.Registration)
        .filter(models.Registration.id == registration_id)
        .first()
    )


def delete_registration(
    db: Session,
    db_registration: models.Registration,
) -> None:
    db.delete(db_registration)
    db.commit()

