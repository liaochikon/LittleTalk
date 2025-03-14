from enum import IntEnum, auto

class LED_Command(IntEnum):
    LED_BLINK = 0
    LED_ON    = auto()
    LED_OFF   = auto()
    LED_CURRENT_ENABLE  = auto()
    LED_TARGET_ENABLE  = auto()
    LED_CURRENT_BLINK_NUM  = auto()
    LED_TARGET_BLINK_NUM  = auto()
    CMD_END   = auto()