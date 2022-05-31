#ifndef DATAMANAGE_H
#define DATAMANAGE_H

#include "HWManage.h"

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);

int hex2dec(char hex[], int size);

uint8_t charTOint(char ch);

void bin2hex(uint8_t binNum, char *ris);

void provideOutput();

void analizzaRxBUf();

uint8_t fillRxBuf(char carattere);

uint8_t getStatusRx();

void rstStatusRx();

#endif
