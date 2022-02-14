from open_needs_server.database import Base
from fastapi_users.db import SQLAlchemyBaseUserTable


class User(Base, SQLAlchemyBaseUserTable):
    pass
