from typing import Dict, Union

from sqlalchemy.orm import Session

from open_needs_server import models


def filter_needs(db: Session, filters: Dict[str, Union[float, str]]):
    query = db.query(models.Need)
    for attr, value in filters['values'].items():
        if attr != "meta":
            query = query.filter(getattr(models.Need, attr) == value)
        else:
            for json_attr, json_value in value.items():
                query = query.filter(getattr(models.Need, attr)[json_attr].as_string() == json_value)

    return query.offset(filters.get('skip', 0)).limit(filters.get('limit', 100)).all()


class OnApiFilterException(BaseException):
    pass
