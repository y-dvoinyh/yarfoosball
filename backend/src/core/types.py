from typing import TypeVar
from pydantic import BaseModel as BaseScheme

from .model import BaseModel


ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseScheme)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseScheme)
PartialSchemaType = TypeVar("PartialSchemaType", bound=BaseScheme)

