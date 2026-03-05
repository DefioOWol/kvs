"""Key-Value Store сервис с асинхронной очередью."""

import asyncio
from collections.abc import Callable
from typing import Any

from app.services.kvstore import IKeyValueStoreService
from app.services.utils import IAsyncWorker
from app.storage.kvstorage import IKeyValueStorage


class QueueKeyValueStoreService(IKeyValueStoreService, IAsyncWorker):
    def __init__(self, storage: IKeyValueStorage):
        self._storage = storage
        self._queue: asyncio.Queue[
            tuple[Callable[[asyncio.Future[Any]], None], asyncio.Future[Any]]
        ] = asyncio.Queue()

    async def init_worker(self):
        while True:
            op, fut = await self._queue.get()
            try:
                op(fut)
            except Exception as e:
                if not fut.done():
                    fut.set_exception(e)
            finally:
                if not fut.done():
                    fut.cancel()
                self._queue.task_done()

    async def _enqueue(self, op: Callable[[asyncio.Future[Any]], None]) -> Any:
        fut = asyncio.get_running_loop().create_future()
        await self._queue.put((op, fut))
        return await fut

    async def put(self, data: dict[str, Any]) -> dict[str, Any]:
        def op(fut):
            result = self._storage.put(data)
            fut.set_result(result)

        return await self._enqueue(op)

    async def get(self, key: str) -> dict[str, Any] | None:
        def op(fut):
            result = self._storage.get(key)
            fut.set_result(result)

        return await self._enqueue(op)

    async def delete(self, key: str) -> bool:
        def op(fut):
            result = self._storage.delete(key)
            fut.set_result(result)

        return await self._enqueue(op)

    async def get_by_prefix(self, prefix: str) -> list[dict[str, Any]]:
        def op(fut):
            result = self._storage.get_many(prefix=prefix)
            fut.set_result(result)

        return await self._enqueue(op)
