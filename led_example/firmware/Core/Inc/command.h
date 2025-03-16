/*
 * command.h
 *
 *  Created on: Mar 14, 2025
 *      Author: 90002283
 */

#ifndef INC_COMMAND_H_
#define INC_COMMAND_H_

#include "main.h"
#include "string.h"
#include "stdbool.h"
#include "stdint.h"

typedef enum
{
	LED_BLINK = 0U,
	LED_ON,
	LED_OFF,
	LED_CURRENT_ENABLE,
	LED_TARGET_ENABLE,
	LED_CURRENT_BLINK_NUM,
	LED_TARGET_BLINK_NUM,
	CMD_END
} LED_Command;

typedef enum
{
	_int64 = 0U,
	_int32,
	_int16,
	_int8,
	_uint64,
	_uint32,
	_uint16,
	_uint8,
	_float64,
	_float32,
	_bool,
	_null
} MessageDataType;

typedef enum
{
	DATA_TYPE_ERROR = 0U,
	DATA_VALUE_ERROR,
	MSG_LEN_ERROR,
	CHECK_HEX_ERROR,
	CMD_HEX_ERROR,
	BUSY_ERROR
} ErrorMessage;

#define CHECK_HEX 0x6B
#define ERROR_HEX 0xEE
#define DONE_HEX 0xDD

#define START_HEX_IDX 0
#define END_HEX_IDX 7
#define MSG_LEN_HEX_IDX 1
#define DATA_TYPE_HEX_IDX 2
#define DATA_START_HEX_IDX 3

#define MSG_LEN 8

void State_Machine_Init();
void Command_State_Machine(uint8_t* receive_msg, uint32_t receive_msg_len);

#endif /* INC_COMMAND_H_ */
