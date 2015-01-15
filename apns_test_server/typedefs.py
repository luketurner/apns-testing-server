from collections import namedtuple as NamedTuple
from enum import Enum

Item = NamedTuple("Item", ["type", "length", "data"])
Frame = NamedTuple("Frame", ["length", "items"])

class ErrorCode(Enum):
    success = 0
    processing_error = 1
    missing_device_token = 2
    missing_topic = 3
    missing_payload = 4
    invalid_token_size = 5
    invalid_topic_size = 6
    invalid_payload_size = 7
    invalid_token = 8
    shutdown = 10
    unknown = 255

class ItemType(Enum):
    device_token = 1
    payload = 2
    notification_id = 3
    expiration_date = 4
    priority = 5

class ParseException(Exception):
    pass
