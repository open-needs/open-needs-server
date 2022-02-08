from sqlalchemy.orm import Session

from open_needs_server import models
from open_needs_server import schemas


def get_organization(db: Session, organization_id: int):
    return db.query(models.Organization).filter(models.Organization.id == organization_id).first()


def get_organization_by_title(db: Session, organization_title: int):
    return db.query(models.Organization).filter(models.Organization.title == organization_title).first()


def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organization).offset(skip).limit(limit).all()


def create_organization(db: Session, organization: schemas.organization):
    db_organization = models.Organization(title=organization.title)
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization
