from sqlalchemy import Integer, Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from fastapi_users.db import SQLAlchemyBaseUserTable

from open_needs_server.database import Base

roles_users_table = Table('roles_users', Base.metadata,
                          Column('role', ForeignKey('role.id'), primary_key=True),
                          Column('user', ForeignKey('user.id'), primary_key=True)
                          )


class UserModel(Base, SQLAlchemyBaseUserTable):
    def __repr__(self) -> str:
        return f"{self.email}"

    roles = relationship("RoleModel",
                         secondary=roles_users_table,
                         back_populates="users",
                         lazy='selectin')  # immediate


class RoleModel(Base):
    __tablename__ = "role"

    def __repr__(self) -> str:
        return f"{self.name}"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    users = relationship("UserModel",
                         secondary=roles_users_table,
                         back_populates="roles",
                         lazy='selectin')  # selectin
