"""Конфигурация приложения."""

import os

GRPC_PORT = int(os.getenv("GRPC_PORT", 50051))

LRU_MAXSIZE = int(os.getenv("LRU_SIZE", 10))
