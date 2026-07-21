from sqlalchemy.orm import Session

from . import models, schemas


def create_program(
    db: Session,
    program: schemas.ProgramCreate,
) -> models.Program:
    db_program = models.Program(**program.model_dump())

    db.add(db_program)
    db.commit()
    db.refresh(db_program)

    return db_program


def get_programs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Program]:
    return (
        db.query(models.Program)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_program(
    db: Session,
    program_id: int,
) -> models.Program | None:
    return (
        db.query(models.Program)
        .filter(models.Program.id == program_id)
        .first()
    )


def get_programs_by_event(
    db: Session,
    event_id: int,
) -> list[models.Program]:
    return (
        db.query(models.Program)
        .filter(models.Program.event_id == event_id)
        .all()
    )


def update_program(
    db: Session,
    db_program: models.Program,
    program_update: schemas.ProgramUpdate,
) -> models.Program:
    update_data = program_update.model_dump(exclude_unset=True)

    new_start = update_data.get(
        "start_time",
        db_program.start_time,
    )

    new_end = update_data.get(
        "end_time",
        db_program.end_time,
    )

    if new_end <= new_start:
        raise ValueError("end_time must be later than start_time")

    for field, value in update_data.items():
        setattr(db_program, field, value)

    db.commit()
    db.refresh(db_program)

    return db_program


def delete_program(
    db: Session,
    db_program: models.Program,
) -> None:
    db.delete(db_program)
    db.commit()