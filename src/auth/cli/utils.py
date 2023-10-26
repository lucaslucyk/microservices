from typing import Any, Type, TypeVar
from pydantic import TypeAdapter, BaseModel


KindType = TypeVar("KindType", bound=BaseModel)


def parse_object_as(kind: Type[KindType], data: Any, **kwargs) -> KindType:
    """Parse python object to pydantic model type

    Args:
        kind (Any): Pydantic model type
        data (Any): Python object

    Returns:
        Any: Pydantic model type instance
    """

    return TypeAdapter(kind).validate_python(data, **kwargs)
