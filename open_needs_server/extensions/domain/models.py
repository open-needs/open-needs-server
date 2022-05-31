from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from open_needs_server.database import Base


class DomainModel(Base):
    __tablename__ = "domains"

    def __repr__(self) -> str:
        return f"[{self.id}]{self.title}"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False, index=True)
    description = Column(String, unique=False, index=False)

    jsonschema = Column(JSON, unique=False, nullable=True, index=True)
