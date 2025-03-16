from serial import Serial
from enum import IntEnum, auto
import struct
import time

class MessageFormat():
    CHECK_HEX = 0x6B
    ERROR_HEX = 0xEE
    DONE_HEX = 0xDD

    START_HEX_IDX = 0
    END_HEX_IDX = 7
    MSG_LEN_HEX_IDX = 1
    DATA_TYPE_HEX_IDX = 2
    DATA_START_HEX_IDX = 3
    
    MSG_LEN = 8

class MessageDataType(IntEnum):
    _int64   = 0
    _int32   = auto()
    _int16   = auto()
    _int8    = auto()
    _uint64  = auto()
    _uint32  = auto()
    _uint16  = auto()
    _uint8   = auto()
    _float32 = auto()
    _float64 = auto()
    _bool    = auto()
    _null    = auto()

class ErrorMessage(IntEnum):
    DATA_TYPE_ERROR  = 0
    DATA_VALUE_ERROR = auto()
    MSG_LENGTH_ERROR = auto()
    CHECK_HEX_ERROR  = auto()
    CMD_HEX_ERROR    = auto()
    BUSY_ERROR       = auto()

class ReturnMessage():
    ERROR    = "ERROR"
    DONE     = "DONE"
    NULL     = "NULL"
    MISMATCH = "MISMATCH"



def Receive_Message(serial_device : Serial, wait_sec = 0.05):
    data_raw = []
    delta_sec = 0
    start_sec = time.time()
    while(len(data_raw) < MessageFormat.MSG_LEN):
        delta_sec = time.time() - start_sec
        if(delta_sec > wait_sec):
            return None
        b = serial_device.read()
        if b != b'':
            data_raw.extend(b)
    return data_raw

def Transmit_Message(serial_device : Serial, cmd_hex : IntEnum, data = None, data_type = MessageDataType._null):
    message = [0 for i in range(MessageFormat.MSG_LEN)]
    message[MessageFormat.START_HEX_IDX] = cmd_hex.value
    message[MessageFormat.MSG_LEN_HEX_IDX] = MessageFormat.MSG_LEN
    message[MessageFormat.DATA_TYPE_HEX_IDX] = data_type.value

    data_list = Send_Data_Interpret(data, data_type)
    for i, d in enumerate(data_list):
        message[i + MessageFormat.DATA_START_HEX_IDX] = d
        
    message[MessageFormat.END_HEX_IDX] = MessageFormat.CHECK_HEX
    serial_device.write(message)
    return message
    
def Wait_Message(serial_device, cmd_hex, data_type = MessageDataType._null, wait_sec = 0.05):
    data_raw = Receive_Message(serial_device, wait_sec)
    if data_raw == None:
        return None ,ReturnMessage.NULL, None
    if data_raw[MessageFormat.START_HEX_IDX] != cmd_hex:
        return data_raw ,ReturnMessage.MISMATCH, None
    if data_raw[MessageFormat.END_HEX_IDX] == MessageFormat.ERROR_HEX:
        error_data = Error_Data_Interpret(data_raw)
        return data_raw ,ReturnMessage.ERROR, error_data
    if data_raw[MessageFormat.END_HEX_IDX] == MessageFormat.DONE_HEX:
        data = Receive_Data_Interpret(data_raw, data_type)
        return data_raw ,ReturnMessage.DONE, data
    
def Error_Data_Interpret(data):
    uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(4)]
    data = uint8_list_to_int32(*uint8_list)
    if data == ErrorMessage.DATA_TYPE_ERROR:
        return ErrorMessage.DATA_TYPE_ERROR
    elif data == ErrorMessage.DATA_VALUE_ERROR:
        return ErrorMessage.DATA_VALUE_ERROR
    elif data == ErrorMessage.MSG_LENGTH_ERROR:
        return ErrorMessage.MSG_LENGTH_ERROR
    elif data == ErrorMessage.CHECK_HEX_ERROR:
        return ErrorMessage.CHECK_HEX_ERROR
    elif data == ErrorMessage.CMD_HEX_ERROR:
        return ErrorMessage.CMD_HEX_ERROR
    elif data == ErrorMessage.BUSY_ERROR:
        return ErrorMessage.BUSY_ERROR

def Send_Data_Interpret(data, data_type : MessageDataType):
    if data_type == MessageDataType._int64:
        uint8_list = int64_to_uint8_list(data)
    elif data_type == MessageDataType._int32:
        uint8_list = int32_to_uint8_list(data)
    elif data_type == MessageDataType._int16:
        uint8_list = int16_to_uint8_list(data)
    elif data_type == MessageDataType._int8:
        uint8_list = int8_to_uint8_list(data)
    elif data_type == MessageDataType._uint64:
        uint8_list = uint64_to_uint8_list(data)
    elif data_type == MessageDataType._uint32:
        uint8_list = uint32_to_uint8_list(data)
    elif data_type == MessageDataType._uint16:
        uint8_list = uint16_to_uint8_list(data)
    elif data_type == MessageDataType._uint8:
        uint8_list = uint8_to_uint8_list(data)
    elif data_type == MessageDataType._float64:
        uint8_list = float64_to_uint8_list(data)
    elif data_type == MessageDataType._float32:
        uint8_list = float32_to_uint8_list(data)
    elif data_type == MessageDataType._bool:
        uint8_list = bool_to_uint8_list(data)
    elif data_type == MessageDataType._null:
        uint8_list = []
    return uint8_list

def Receive_Data_Interpret(data, data_type : MessageDataType):
    if data_type == MessageDataType._int64:
        uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(8)]
        data = uint8_list_to_int64(*uint8_list)
    elif data_type == MessageDataType._int32:
        uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(4)]
        data = uint8_list_to_int32(*uint8_list)
    elif data_type == MessageDataType._int16:
        uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(2)]
        data = uint8_list_to_int16(*uint8_list)
    elif data_type == MessageDataType._int8:
        uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(1)]
        data = uint8_list_to_int8(*uint8_list)
    elif data_type == MessageDataType._uint64:
        uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(8)]
        data = uint8_list_to_uint64(*uint8_list)
    elif data_type == MessageDataType._uint32:
        uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(4)]
        data = uint8_list_to_uint32(*uint8_list)
    elif data_type == MessageDataType._uint16:
        uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(2)]
        data = uint8_list_to_uint16(*uint8_list)
    elif data_type == MessageDataType._uint8:
        uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(1)]
        data = uint8_list_to_uint8(*uint8_list)
    elif data_type == MessageDataType._float64:
        uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(8)]
        data = uint8_list_to_float64(*uint8_list)
    elif data_type == MessageDataType._float32:
        uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(4)]
        data = uint8_list_to_float32(*uint8_list)
    elif data_type == MessageDataType._bool:
        uint8_list = [data[MessageFormat.DATA_START_HEX_IDX + idx] for idx in range(1)]
        data = uint8_list_to_bool(*uint8_list)
    elif data_type == MessageDataType._null:
        data = None
    return data

def Print_Message(message):
    [print(hex(n), end=" ") for n in message]
    print()

def int64_to_uint8_list(i):
    packed_bytes = struct.pack('<q', i)
    uint8_list = list(packed_bytes)
    return uint8_list

def int32_to_uint8_list(i):
    packed_bytes = struct.pack('<i', i)
    uint8_list = list(packed_bytes)
    return uint8_list

def int16_to_uint8_list(i):
    packed_bytes = struct.pack('<h', i)
    uint8_list = list(packed_bytes)
    return uint8_list

def int8_to_uint8_list(i):
    packed_bytes = struct.pack('<b', i)
    uint8_list = list(packed_bytes)
    return uint8_list

def uint64_to_uint8_list(i):
    packed_bytes = struct.pack('<Q', i)
    uint8_list = list(packed_bytes)
    return uint8_list

def uint32_to_uint8_list(i):
    packed_bytes = struct.pack('<I', i)
    uint8_list = list(packed_bytes)
    return uint8_list

def uint16_to_uint8_list(i):
    packed_bytes = struct.pack('<H', i)
    uint8_list = list(packed_bytes)
    return uint8_list

def uint8_to_uint8_list(i):
    packed_bytes = struct.pack('<B', i)
    uint8_list = list(packed_bytes)
    return uint8_list

def float64_to_uint8_list(f):
    packed_bytes = struct.pack('<d', f)
    uint8_list = list(packed_bytes)
    return uint8_list

def float32_to_uint8_list(f):
    packed_bytes = struct.pack('<f', f)
    uint8_list = list(packed_bytes)
    return uint8_list

def bool_to_uint8_list(i):
    packed_bytes = struct.pack('<?', i)
    uint8_list = list(packed_bytes)
    return uint8_list



def uint8_list_to_int64(i1, i2, i3, i4, i5, i6, i7, i8):
    i = struct.unpack("<q", bytes([i1, i2, i3, i4, i5, i6, i7, i8]))[0]
    return i

def uint8_list_to_int32(i1, i2, i3, i4):
    i = struct.unpack("<i", bytes([i1, i2, i3, i4]))[0]
    return i

def uint8_list_to_int16(i1, i2):
    i = struct.unpack("<h", bytes([i1, i2]))[0]
    return i

def uint8_list_to_int8(i1):
    i = struct.unpack("<b", bytes([i1]))[0]
    return i

def uint8_list_to_uint64(i1, i2, i3, i4, i5, i6, i7, i8):
    i = struct.unpack("<Q", bytes([i1, i2, i3, i4, i5, i6, i7, i8]))[0]
    return i

def uint8_list_to_uint32(i1, i2, i3, i4):
    ui = struct.unpack("<I", bytes([i1, i2, i3, i4]))[0]
    return ui

def uint8_list_to_uint16(i1, i2):
    ui = struct.unpack("<H", bytes([i1, i2]))[0]
    return ui

def uint8_list_to_uint8(i1):
    ui = struct.unpack("<B", bytes([i1]))[0]
    return ui

def uint8_list_to_float64(i1, i2, i3, i4, i5, i6, i7, i8):
    f = struct.unpack("<d", bytes([i1, i2, i3, i4, i5, i6, i7, i8]))[0]
    return f

def uint8_list_to_float32(i1, i2, i3, i4):
    f = struct.unpack("<f", bytes([i1, i2, i3, i4]))[0]
    return f

def uint8_list_to_bool(i1):
    b = struct.unpack("<?", bytes([i1]))[0]
    return b