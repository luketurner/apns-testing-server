import asyncio
from struct import unpack, pack
from typedefs import ErrorCode, ItemType, Item, Frame, ParseException
from settings import RESPONSE_TIME_MS

# RESPONSE GENERATION

@asyncio.coroutine
def delay_response(frame, writer):

    yield from asyncio.sleep(RESPONSE_TIME_MS / 1000)
    
    print("BEGIN RESPONSE")
    status_code = ErrorCode.success

    if ItemType.notification_id in frame.items:
        notification_id = frame.items[ItemType.notification_id].data
    else:
        notification_id = 0
        
    data = pack(">BB4s", 8, status_code.value, notification_id)
    print("  Response code:", status_code.name)
    print("  Response id:", notification_id)
    print("  Response raw data:", data)
    writer.write(data)
    print("END RESPONSE")

# REQUEST PARSING

@asyncio.coroutine
def read_item(stream):
    item_header = yield from stream.read(3)
    
    if len(item_header) != 3:
        return None
    
    item_type, item_length = unpack(">Bh", item_header)
    item_data = yield from stream.read(item_length)

    print()
    print("\tItem type:", item_type)
    print("\tItem length:", item_length)
    print("\tItem data:", item_data)
    
    return Item(ItemType(item_type), item_length, item_data)

@asyncio.coroutine
def read_frame(stream):
    print("BEGIN FRAME")
    frame_header = yield from stream.read(5)
    command_byte, frame_length = unpack(">Bl", frame_header)

    print("  Command byte:", command_byte)
    print("  Frame length:", frame_length)

    frame = Frame(frame_length, {})

    if command_byte != 2:
        raise ParseException("Command byte", command_byte, "was not 2")

    item = yield from read_item(stream)
    while item:
        frame.items[item.type] = item
        item = yield from read_item(stream)

    if frame_length != sum(item.length + 3 for item in frame.items.values()):
        raise ParseException("Invalid frame length", frame_length);

    print("END FRAME")
    return frame

@asyncio.coroutine
def request_handler(reader, writer):
    print("BEGIN COMM from", writer.get_extra_info('peername'))

    while not reader.at_eof():
        frame = yield from read_frame(reader) 
        yield from delay_response(frame, writer)

    print("END COMM")
    print()
    writer.close()
