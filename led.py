from command import LED_Command
from littletalk.message import *

def LED_Blink(serial_device : Serial, blink_num : int, wait_sec = 0.05):
    Transmit_Message(serial_device, LED_Command.LED_BLINK, blink_num, MessageDataType._uint32)
    return Wait_Message(serial_device, LED_Command.LED_BLINK, MessageDataType._null, wait_sec)

def LED_ON(serial_device : Serial, wait_sec = 0.05):
    Transmit_Message(serial_device, LED_Command.LED_ON)
    return Wait_Message(serial_device, LED_Command.LED_ON, MessageDataType._null, wait_sec)

def LED_OFF(serial_device : Serial, wait_sec = 0.05):
    Transmit_Message(serial_device, LED_Command.LED_OFF)
    return Wait_Message(serial_device, LED_Command.LED_OFF, MessageDataType._null, wait_sec)

def LED_Current_Enable(serial_device : Serial, wait_sec = 0.05):
    Transmit_Message(serial_device, LED_Command.LED_CURRENT_ENABLE, wait_sec)
    return Wait_Message(serial_device, LED_Command.LED_CURRENT_ENABLE, MessageDataType._bool, wait_sec)

def LED_Target_Enable(serial_device : Serial, wait_sec = 0.05):
    Transmit_Message(serial_device, LED_Command.LED_TARGET_ENABLE, wait_sec)
    return Wait_Message(serial_device, LED_Command.LED_TARGET_ENABLE, MessageDataType._bool, wait_sec)

def LED_Current_Blink_Num(serial_device : Serial, wait_sec = 0.05):
    Transmit_Message(serial_device, LED_Command.LED_CURRENT_BLINK_NUM, wait_sec)
    return Wait_Message(serial_device, LED_Command.LED_CURRENT_BLINK_NUM, MessageDataType._uint32, wait_sec)

def LED_Target_Blink_Num(serial_device : Serial, wait_sec = 0.05):
    Transmit_Message(serial_device, LED_Command.LED_TARGET_BLINK_NUM, wait_sec)
    return Wait_Message(serial_device, LED_Command.LED_TARGET_BLINK_NUM, MessageDataType._uint32, wait_sec)