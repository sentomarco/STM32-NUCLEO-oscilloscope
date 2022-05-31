#ifndef CALLBACK_H
#define CALLBACK_H

#include "main.h"
#include <string.h>
#include <stdio.h>
#include <math.h>

extern ADC_HandleTypeDef hadc1;
extern DMA_HandleTypeDef hdma_adc1;
extern TIM_HandleTypeDef htim3;
extern UART_HandleTypeDef huart2;

extern HAL_StatusTypeDef HAL_ADC_AnalogWDGConfig(ADC_HandleTypeDef* hadc, ADC_AnalogWDGConfTypeDef* AnalogWDGConfig);

#endif
