"""Интерфейс Key-Value Store сервиса."""

from typing import Any, Protocol


class IKeyValueStoreService(Protocol):
    async def put(self, data: dict[str, Any]) -> dict[str, Any]:
        pass

    async def get(self, key: str) -> dict[str, Any] | None:
        pass

    async def delete(self, key: str) -> bool:
        pass

    async def get_by_prefix(self, prefix: str) -> list[dict[str, Any]]:
        pass
