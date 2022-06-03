from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from open_needs_server.database import Base


class NeedModel(Base):
    __tablename__ = "needs"

    def __repr__(self) -> str:
        return f"[{self.id}]{self.title}"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(Integer, unique=False, index=True)
    type = Column(Integer, unique=False, index=True)
    title = Column(String, unique=False, index=True)
    description = Column(String, unique=False, index=False)
    format = Column(String, unique=False, index=False)

    meta = Column(JSON, unique=False, nullable=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("ProjectModel", back_populates="needs")
