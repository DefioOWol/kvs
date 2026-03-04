"""KeyValueStore сервер."""

import grpc

from protos.kvstore import kvstore_pb2
from protos.kvstore.kvstore_pb2_grpc import KeyValueStoreServicer


class KeyValueStore(KeyValueStoreServicer):
    async def Put(
        self, request: kvstore_pb2.PutRequest, context: grpc.ServicerContext
    ) -> kvstore_pb2.PutResponse:
        pass

    async def Get(
        self, request: kvstore_pb2.GetRequest, context: grpc.ServicerContext
    ) -> kvstore_pb2.GetResponse:
        pass

    async def Delete(
        self, request: kvstore_pb2.DeleteRequest, context: grpc.ServicerContext
    ) -> kvstore_pb2.DeleteResponse:
        pass

    async def List(
        self, request: kvstore_pb2.ListRequest, context: grpc.ServicerContext
    ) -> kvstore_pb2.ListResponse:
        pass
