from pydantic import BaseModel
from typing import Dict, Union

from open_needs_server.extensions.need.schemas import NeedFilterSchema


class FilterSchema(BaseModel):
    values: NeedFilterSchema
    skip: int = 0
    limit: int = 100
