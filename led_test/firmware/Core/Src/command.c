/*
 * command.c
 *
 *  Created on: Mar 14, 2025
 *      Author: 90002283
 */

#include "command.h"
#include "usbd_cdc_if.h"

void (*Function_Array[CMD_END])(uint8_t* receive_msg, uint8_t* send_msg);

void error_return(uint8_t cmd_hex, uint32_t error_hex, uint8_t* send_msg)
{
	send_msg[START_HEX_IDX] = cmd_hex;
	send_msg[MSG_LEN_HEX_IDX] = MSG_LEN;
	send_msg[DATA_TYPE_HEX_IDX] = _null;
	memcpy(&send_msg[DATA_START_HEX_IDX], &error_hex, sizeof(uint32_t));
	send_msg[END_HEX_IDX] = ERROR_HEX;
}

void done_return(uint8_t cmd_hex, uint8_t* send_msg, void* data, MessageDataType data_type)
{
	send_msg[START_HEX_IDX] = cmd_hex;
	send_msg[MSG_LEN_HEX_IDX] = MSG_LEN;

	send_msg[DATA_TYPE_HEX_IDX] = data_type;
	for(uint8_t idx = DATA_START_HEX_IDX; idx < END_HEX_IDX; idx++)
		send_msg[idx] = 0;
	switch(data_type)
	{
		case _int64:
			memcpy(&send_msg[DATA_START_HEX_IDX], data, sizeof(int64_t));
			break;
		case _int32:
			memcpy(&send_msg[DATA_START_HEX_IDX], data, sizeof(int32_t));
			break;
		case _int16:
			memcpy(&send_msg[DATA_START_HEX_IDX], data, sizeof(int16_t));
			break;
		case _int8:
			memcpy(&send_msg[DATA_START_HEX_IDX], data, sizeof(int8_t));
			break;
		case _uint64:
			memcpy(&send_msg[DATA_START_HEX_IDX], data, sizeof(uint64_t));
			break;
		case _uint32:
			memcpy(&send_msg[DATA_START_HEX_IDX], data, sizeof(uint32_t));
			break;
		case _uint16:
			memcpy(&send_msg[DATA_START_HEX_IDX], data, sizeof(uint16_t));
			break;
		case _uint8:
			memcpy(&send_msg[DATA_START_HEX_IDX], data, sizeof(uint8_t));
			break;
		case _float64:
			memcpy(&send_msg[DATA_START_HEX_IDX], data, sizeof(double));
			break;
		case _float32:
			memcpy(&send_msg[DATA_START_HEX_IDX], data, sizeof(float));
			break;
		case _bool:
			memcpy(&send_msg[DATA_START_HEX_IDX], data, sizeof(bool));
			break;
		case _null:
			break;
	}

	send_msg[END_HEX_IDX] = DONE_HEX;
}

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

void led_current_enable(uint8_t* receive_msg, uint8_t* send_msg)
{
	if (receive_msg[DATA_TYPE_HEX_IDX] != _null)// Received message data type examination
	{
		error_return(LED_CURRENT_ENABLE, DATA_TYPE_ERROR, send_msg);
		return;
	}

	done_return(LED_CURRENT_ENABLE, send_msg, &LED_Handle.current_enable, _bool);
}

void led_target_enable(uint8_t* receive_msg, uint8_t* send_msg)
{
	if (receive_msg[DATA_TYPE_HEX_IDX] != _null)// Received message data type examination
	{
		error_return(LED_TARGET_ENABLE, DATA_TYPE_ERROR, send_msg);
		return;
	}

	done_return(LED_TARGET_ENABLE, send_msg, &LED_Handle.target_enable, _bool);
}

void led_current_blink_num(uint8_t* receive_msg, uint8_t* send_msg)
{
	if (receive_msg[DATA_TYPE_HEX_IDX] != _null)// Received message data type examination
	{
		error_return(LED_CURRENT_BLINK_NUM, DATA_TYPE_ERROR, send_msg);
		return;
	}

	done_return(LED_CURRENT_BLINK_NUM, send_msg, &LED_Handle.current_blink_nums, _uint32);
}

void led_target_blink_num(uint8_t* receive_msg, uint8_t* send_msg)
{
	if (receive_msg[DATA_TYPE_HEX_IDX] != _null)// Received message data type examination
	{
		error_return(LED_TARGET_BLINK_NUM, DATA_TYPE_ERROR, send_msg);
		return;
	}

	done_return(LED_TARGET_BLINK_NUM, send_msg, &LED_Handle.target_blink_nums, _uint32);
}

void State_Machine_Init()
{
	Function_Array[LED_BLINK]             =	led_blink;
	Function_Array[LED_ON]                =	led_on;
	Function_Array[LED_OFF]               =	led_off;
	Function_Array[LED_CURRENT_ENABLE]    =	led_current_enable;
	Function_Array[LED_TARGET_ENABLE]     =	led_target_enable;
	Function_Array[LED_CURRENT_BLINK_NUM] =	led_current_blink_num;
	Function_Array[LED_TARGET_BLINK_NUM]  =	led_target_blink_num;
}

void Command_State_Machine(uint8_t* receive_msg, uint32_t receive_msg_len)
{
	memcpy(USB_RX_Data, receive_msg, MSG_LEN);
	if (USB_RX_Data[END_HEX_IDX] != CHECK_HEX)// Received message check hex examination
	{
		error_return(CMD_END, CHECK_HEX_ERROR, USB_TX_Data);
		CDC_Transmit_FS(USB_TX_Data, MSG_LEN);
		return;
	}
	if (USB_RX_Data[MSG_LEN_HEX_IDX] != MSG_LEN || receive_msg_len != MSG_LEN)// Received message length examination
	{
		error_return(CMD_END, MSG_LEN_ERROR, USB_TX_Data);
		CDC_Transmit_FS(USB_TX_Data, MSG_LEN);
		return;
	}
	if(USB_RX_Data[0] >= CMD_END)// Received message command hex examination
	{
		error_return(CMD_END, CMD_HEX_ERROR, USB_TX_Data);
		CDC_Transmit_FS(USB_TX_Data, MSG_LEN);
		return;
	}

	uint8_t func_idx = USB_RX_Data[0];
	Function_Array[func_idx](USB_RX_Data, USB_TX_Data);
	CDC_Transmit_FS(USB_TX_Data, MSG_LEN);
}
