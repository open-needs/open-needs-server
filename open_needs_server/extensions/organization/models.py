from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from open_needs_server.database import Base

organizations_users_table = Table(
    "organizations_users",
    Base.metadata,
    Column("organizations", ForeignKey("organizations.id"), primary_key=True),
    Column("user", ForeignKey("user.id"), primary_key=True),
)


class OrganizationModel(Base):
    __tablename__ = "organizations"

    def __repr__(self) -> str:
        return self.title

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)

    projects = relationship(
        "ProjectModel", back_populates="organization", lazy="selectin"
    )

    users = relationship(
        "UserModel", secondary=organizations_users_table, lazy="selectin"
    )  # selectin
