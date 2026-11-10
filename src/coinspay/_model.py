import copy
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

Decimalish = Union[str, Decimal]
"""An amount: a decimal string such as ``"49.90"`` or a ``Decimal``. Floats are refused."""

M = TypeVar("M", bound="Model")


class NotGiven:
    """Marks a parameter that was not passed, as opposed to one passed as ``None`` (sent as null)."""

    def __repr__(self) -> str:
        return "NOT_GIVEN"

    def __bool__(self) -> bool:
        return False


NOT_GIVEN = NotGiven()


@dataclass(frozen=True)
class Model:
    """
    Base of the API objects. Fields are named as in the API (snake_case); ``raw`` and
    ``to_dict()`` hold the object exactly as the API sent it, including fields this version
    of the library does not know yet.
    """

    raw: Dict[str, Any] = field(repr=False, compare=False)

    def to_dict(self) -> Dict[str, Any]:
        """The object as the API sent it."""
        return copy.deepcopy(self.raw)


def _value(data: Dict[str, Any], key: str) -> Any:
    return data.get(key)


def _one(data: Dict[str, Any], key: str, cls: Type[M]) -> Optional[M]:
    value = data.get(key)
    return cls.from_dict(value) if isinstance(value, dict) else None  # type: ignore[attr-defined]


def _list(data: Dict[str, Any], key: str, cls: Type[M]) -> Optional[List[M]]:
    value = data.get(key)
    if not isinstance(value, list):
        return None
    return [cls.from_dict(item) for item in value if isinstance(item, dict)]  # type: ignore[attr-defined]


def _one_required(data: Dict[str, Any], key: str, cls: Type[M]) -> M:
    # The API always sends it; if it is missing anyway, decoding still works and gives None.
    return cast(M, _one(data, key, cls))


def _list_required(data: Dict[str, Any], key: str, cls: Type[M]) -> List[M]:
    return _list(data, key, cls) or []
