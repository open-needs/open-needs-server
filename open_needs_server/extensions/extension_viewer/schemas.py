from pydantic import BaseModel


class ExtensionBaseSchema(BaseModel):
    name: str
    description: str
    version: str
