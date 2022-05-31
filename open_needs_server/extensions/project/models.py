from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from open_needs_server.database import Base


projects_domains_table = Table(
    "project_domain",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("domain_id", ForeignKey("domains.id"), primary_key=True ),
)


class ProjectModel(Base):
    __tablename__ = "projects"

    def __repr__(self) -> str:
        return self.title

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False, index=True)

    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("OrganizationModel", back_populates="projects")

    needs = relationship("NeedModel", back_populates="project", lazy='selectin')
    domains = relationship("DomainModel", secondary=projects_domains_table,
                           lazy='selectin')  #, lazy='selectin')
