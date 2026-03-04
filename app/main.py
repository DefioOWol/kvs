"""Точка входа приложения."""

import asyncio

import grpc

from app.config import GRPC_PORT
from app.servers.kvstore import KeyValueStore
from protos.kvstore import kvstore_pb2_grpc


async def serve():
    server = grpc.aio.server()
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStore(), server
    )
    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
