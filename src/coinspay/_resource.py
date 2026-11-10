from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, Generic, Iterator, List, Optional, TypeVar

from ._model import NOT_GIVEN

if TYPE_CHECKING:  # pragma: no cover
    from ._client import Client

T = TypeVar("T")


@dataclass(frozen=True)
class Page(Generic[T]):
    """One page of a list, newest first."""

    data: List[T]
    next_cursor: Optional[str]
    """Pass it as ``cursor`` to get the next page; ``None`` when there are no more pages."""

    @property
    def has_more(self) -> bool:
        return self.next_cursor is not None

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)


class Resource:
    """Base of the API resources: ``client.invoices``, ``client.payouts`` and others."""

    def __init__(self, client: "Client") -> None:
        self._client = client

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"

    def _call(
        self,
        operation: str,
        id: Optional[str],
        params: Dict[str, Any],
        extra: Optional[Dict[str, Any]],
        idempotency_key: Optional[str],
        *,
        timeout: Optional[float],
        max_retries: Optional[int],
        headers: Optional[Dict[str, str]],
    ) -> Any:
        return self._client._call(operation, id, params, extra, idempotency_key, timeout=timeout, max_retries=max_retries, headers=headers)

    def _iterate(
        self,
        operation: str,
        params: Dict[str, Any],
        extra: Optional[Dict[str, Any]],
        *,
        timeout: Optional[float],
        max_retries: Optional[int],
        headers: Optional[Dict[str, str]],
    ) -> Iterator[Any]:
        params = dict(params)
        cursor = params.get("cursor") or None
        while True:
            params["cursor"] = cursor if cursor is not None else NOT_GIVEN
            page = self._call(operation, None, params, extra, None, timeout=timeout, max_retries=max_retries, headers=headers)
            yield from page.data
            cursor = page.next_cursor
            if not cursor:
                return
