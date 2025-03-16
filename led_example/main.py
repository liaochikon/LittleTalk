from littletalk.device import Get_Serial_Device
from led_command import *

bulepill = Get_Serial_Device("COM3", 115200)

LED_ON(bulepill)

Target_Blink_Num = 200
Current_Blink_Num = 0
LED_Blink(bulepill, Target_Blink_Num)
while Current_Blink_Num < 200:
    _, _, _, Current_Blink_Num = LED_Current_Blink_Num(bulepill)
    print("Current_Blink_Num : {}".format(Current_Blink_Num))

LED_OFF(bulepill)