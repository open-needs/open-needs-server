from sqlalchemy.orm import Session

from open_needs_server import models
from open_needs_server import schemas


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_project_by_title(db: Session, project_title: int):
    return db.query(models.Project).filter(models.Project.title == project_title).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.Project):
    db_project = models.Project(title=project.title)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


# Orga specific

def get_organization_project_by_title(db: Session, organization_id: int, project_title: int):
    return db.query(models.Project).filter(models.Project.title == project_title,
                                           models.Project.organization_id == organization_id).first()


def create_organization_project(db: Session, project: schemas.Project):
    db_project = models.Project(title=project.title, organization_id=project.organization_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

