from sqlalchemy.orm import Session

from open_needs_server import models
from open_needs_server import schemas


def get_need(db: Session, need_id: int):
    return db.query(models.Need).filter(models.Need.id == need_id).first()


def get_needs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Need).offset(skip).limit(limit).all()


def create_need(db: Session, need: schemas.Need, project_id: int):
    db_need = models.Need(title=need.title, description=need.description, project_id=project_id)
    db.add(db_need)
    db.commit()
    db.refresh(db_need)
    return db_need
