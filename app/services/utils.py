"""Вспомогательные функции сервисов."""

from typing import Protocol


class IAsyncWorker(Protocol):
    async def init_worker(self):
        pass
