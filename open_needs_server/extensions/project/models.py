from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from open_needs_server.database import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False, index=True)

    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("OrganizationModel", back_populates="projects")

    needs = relationship("NeedModel", back_populates="project", lazy='selectin')
