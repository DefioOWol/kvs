"""Интерфейс Key-Value хранилища."""

from typing import Any, Protocol


class IKeyValueStorage(Protocol):
    def put(self, data: dict[str, Any]) -> dict[str, Any]:
        pass

    def get(self, key: str) -> dict[str, Any] | None:
        pass

    def delete(self, key: str) -> bool:
        pass

    def get_many(self, *, prefix: str | None = None) -> list[dict[str, Any]]:
        pass
