"""KeyValueStore сервер."""

import grpc

from app.servers.utils import GrpcParser
from app.services.kvstore import IKeyValueStoreService
from protos.kvstore import kvstore_pb2
from protos.kvstore.kvstore_pb2_grpc import KeyValueStoreServicer


class KeyValueStore(KeyValueStoreServicer):
    def __init__(self, service: IKeyValueStoreService):
        self._service = service

    async def Put(
        self, request: kvstore_pb2.PutRequest, context: grpc.ServicerContext
    ) -> kvstore_pb2.PutResponse:
        if not request.key.strip():
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Key cannot be empty"
            )
        if request.ttl_seconds < 0:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "TTL cannot be negative"
            )

        await self._service.put(GrpcParser.msg_to_dict(request))
        return kvstore_pb2.PutResponse()

    async def Get(
        self, request: kvstore_pb2.GetRequest, context: grpc.ServicerContext
    ) -> kvstore_pb2.GetResponse:
        item = await self._service.get(request.key)
        if not item:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Key not found")
        return GrpcParser.dict_to_msg(item, kvstore_pb2.GetResponse())

    async def Delete(
        self, request: kvstore_pb2.DeleteRequest, context: grpc.ServicerContext
    ) -> kvstore_pb2.DeleteResponse:
        if not await self._service.delete(request.key):
            await context.abort(grpc.StatusCode.NOT_FOUND, "Key not found")
        return kvstore_pb2.DeleteResponse()

    async def List(
        self, request: kvstore_pb2.ListRequest, context: grpc.ServicerContext
    ) -> kvstore_pb2.ListResponse:
        items = await self._service.get_by_prefix(request.prefix)
        return kvstore_pb2.ListResponse(
            items=[
                GrpcParser.dict_to_msg(item, kvstore_pb2.KeyValue())
                for item in items
            ]
        )
