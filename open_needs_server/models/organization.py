from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from open_needs_server.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)

    projects = relationship("Project", back_populates="organization")

