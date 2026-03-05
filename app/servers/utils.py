"""Вспомогательные функции серверов."""

from typing import Any

from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.message import Message


class GrpcParser:
    @staticmethod
    def msg_to_dict(msg: Message) -> dict[str, Any]:
        return MessageToDict(
            msg,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
        )

    @staticmethod
    def dict_to_msg(
        data: dict[str, Any], msg: Message, ignore_unknown_fields: bool = True
    ) -> Message:
        return ParseDict(data, msg, ignore_unknown_fields=ignore_unknown_fields)
