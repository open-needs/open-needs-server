from typing import Dict, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from open_needs_server.extensions.need.models import NeedModel


async def filter_needs(db: AsyncSession, filters: Dict[str, Union[float, str]]):
    query = select(NeedModel)
    for attr, value in filters["values"].items():
        if attr != "meta":
            query = query.filter(getattr(NeedModel, attr) == value)
        else:
            for json_attr, json_value in value.items():
                query = query.filter(
                    getattr(NeedModel, attr)[json_attr].as_string() == json_value
                )

    query = query.offset(filters.get("skip", 0))
    query = query.limit(filters.get("limit", 100))

    result = await db.execute(query)
    return result.scalars().all()


class OnApiFilterException(BaseException):
    pass
