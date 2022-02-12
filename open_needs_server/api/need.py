from sqlalchemy.orm import Session

from open_needs_server import models
from open_needs_server import schemas
from open_needs_server.api import project

def get_need(db: Session, need_id: int):
    return db.query(models.Need).filter(models.Need.id == need_id).first()


def get_needs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Need).offset(skip).limit(limit).all()


def create_need(db: Session, need: schemas.Need):
    project_id = need['project_id']
    db_project = db.query(models.Project).filter(models.Project.id == need['project_id']).first()

    if not db_project:
        raise OnApiNeedException(f"Referenced project_id {project_id} not found")

    db_need = models.Need(**need)
    db.add(db_need)
    db.commit()
    db.refresh(db_need)
    return db_need


class OnApiNeedException(BaseException):
    pass
