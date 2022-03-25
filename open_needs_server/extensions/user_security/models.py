from fastapi_users.db import SQLAlchemyBaseUserTable

from open_needs_server.database import Base


class UserModel(Base, SQLAlchemyBaseUserTable):
    pass
