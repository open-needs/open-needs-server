from pydantic import BaseModel
from typing import Dict, Union
from open_needs_server import schemas


class Filter(BaseModel):
    values: schemas.NeedFilter
    skip: int = 0
    limit: int = 100






