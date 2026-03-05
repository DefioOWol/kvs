"""Точка входа приложения."""

import asyncio

import grpc

from app.config import GRPC_PORT, LRU_MAXSIZE
from app.servers.kvstore import KeyValueStore
from app.services.queue_kvstore import QueueKeyValueStoreService
from app.storage.lru_kvstorage import LRUKeyValueStorage
from protos.kvstore import kvstore_pb2_grpc


async def serve():
    storage = LRUKeyValueStorage(LRU_MAXSIZE)

    service = QueueKeyValueStoreService(storage)
    queue_task = asyncio.create_task(service.init_worker())

    server = grpc.aio.server()
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStore(service), server
    )
    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    await server.start()
    await server.wait_for_termination()

    queue_task.cancel()


if __name__ == "__main__":
    asyncio.run(serve())
