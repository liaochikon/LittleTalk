# LittleTalk - A simple STM32 & Python communication framework

## Introduction
LittleTalk is a simple framework for efficiently define and establish communication between PC and STM32. Includes various data type transfer and error handling.

LittleTalk used Python for the PC side programming. You can control STM32 in a straightforward way, like:

``` python
bulepill = Get_Serial_Device("COM3", 115200)

Target_Blink_Num = 200
Current_Blink_Num = 0

LED_ON(bulepill)
LED_Blink(bulepill, Target_Blink_Num)
LED_OFF(bulepill)
```

Functions like **LED_ON**, **LED_Blink**, **LED_OFF** were all define in a very simple style, like:

``` python
class LED_Command(IntEnum):
    LED_BLINK = 0
    LED_ON    = auto()
    LED_OFF   = auto()

def LED_Blink(serial_device : Serial, blink_num : int, wait_sec = 0.05):
    send_msg = Transmit_Message(serial_device, LED_Command.LED_BLINK, blink_num, MessageDataType._uint32)
    return send_msg, *Wait_Message(serial_device, LED_Command.LED_BLINK, MessageDataType._null, wait_sec)

def LED_ON(serial_device : Serial, wait_sec = 0.05):
    send_msg = Transmit_Message(serial_device, LED_Command.LED_ON)
    return send_msg, *Wait_Message(serial_device, LED_Command.LED_ON, MessageDataType._null, wait_sec)

def LED_OFF(serial_device : Serial, wait_sec = 0.05):
    send_msg = Transmit_Message(serial_device, LED_Command.LED_OFF)
    return send_msg, *Wait_Message(serial_device, LED_Command.LED_OFF, MessageDataType._null, wait_sec)

``` 

Simply define transmit/receive message's **command name**, **data** and **data type**, you can establish various communication behaviors for STM32.

And STM32's code looks like:

``` c
typedef enum
{
	LED_BLINK = 0U,
	LED_ON,
	LED_OFF,
} LED_Command;

void led_blink(uint8_t* receive_msg, uint8_t* send_msg)
{
	if (receive_msg[DATA_TYPE_HEX_IDX] != _uint32)// Received message data type examination
	{
		error_return(LED_BLINK, DATA_TYPE_ERROR, send_msg);
		return;
	}
	uint32_t value = 0;
	memcpy(&value, &receive_msg[DATA_START_HEX_IDX], sizeof(uint32_t));
	if (LED_Handle.target_blink_nums > value)// Received message data value examination
	{
		error_return(LED_BLINK, DATA_VALUE_ERROR, send_msg);
		return;
	}
	LED_Handle.target_blink_nums = value;
	done_return(LED_BLINK, send_msg, NULL, _null);
}

void led_on(uint8_t* receive_msg, uint8_t* send_msg)
{
	if (receive_msg[DATA_TYPE_HEX_IDX] != _null)// Received message data type examination
	{
		error_return(LED_ON, DATA_TYPE_ERROR, send_msg);
		return;
	}
	LED_Handle.target_enable = true;
	done_return(LED_ON, send_msg, NULL, _null);
}

void led_off(uint8_t* receive_msg, uint8_t* send_msg)
{
	if (receive_msg[DATA_TYPE_HEX_IDX] != _null)// Received message data type examination
	{
		error_return(LED_OFF, DATA_TYPE_ERROR, send_msg);
		return;
	}
	LED_Handle.target_enable = false;
	done_return(LED_OFF, send_msg, NULL, _null);
}
``` 

## Example

The example is in **led_example** folder. It used a STM32F103C8T6 (BluePill) development board.

In this example you can use simple python code in **main.py** to control the  LED on BluePill.

<img src="image\bluepill.jpg">


### 1. firmware

First, you'll need to upload the firmware code to BluePill.

STM32's code is in **led_test/firmware** folder, you'll need [STM32CubeIDE](https://www.st.com/en/development-tools/stm32cubeide.html) to open **.project** file and upload the code.

The example uses USBCDC as the way to communicate with PC, so a mircoUSB cable is needed.

### 2. Software

Open **main.py** and run it, the LED should start blinking, and the terminal will also shows the total blink number.

``` python
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
``` 

**Done!**