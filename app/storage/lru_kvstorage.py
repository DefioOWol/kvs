"""LRU Key-Value хранилище."""

from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any

from app.storage.kvstorage import IKeyValueStorage


class LRUKeyValueStorage(IKeyValueStorage):
    def __init__(self, maxsize: int | None = None):
        self._maxsize = maxsize
        self._data = OrderedDict[str, dict[str, Any]]()

    def put(self, data: dict[str, Any]) -> dict[str, Any]:
        key = data["key"]
        if ttl := data.get("ttl_seconds", 0):
            ttl = datetime.now() + timedelta(seconds=ttl)
        item = {"value": data["value"], "expired_at": None if ttl == 0 else ttl}

        if key in self._data:
            self._data.move_to_end(key)
        elif self._maxsize and len(self._data) == self._maxsize:
            self._data.popitem(last=False)
        self._data[key] = item

        return {"key": key, **item}

    def _is_expired(self, item: dict[str, Any]) -> bool:
        expired_at = item["expired_at"]
        return expired_at is not None and expired_at <= datetime.now()

    def get(self, key: str) -> dict[str, Any] | None:
        item = self._data.get(key)
        if item and not self._is_expired(item):
            self._data.move_to_end(key)
            return {"key": key, **item}
        return None

    def delete(self, key: str) -> bool:
        try:
            item = self._data.pop(key)
        except KeyError:
            return False
        return not self._is_expired(item)

    def get_by_prefix(
        self, *, prefix: str | None = None
    ) -> list[dict[str, Any]]:
        return [
            {"key": k, **v}
            for k, v in self._data.items()
            if not self._is_expired(v)
            and (prefix is None or k.startswith(prefix))
        ]
