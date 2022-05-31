#ifndef HWMANAGE_H
#define HWMANAGE_H

#include "callBack.h"


void clear_UART();

//void findTL();

void SetTT(uint8_t TT);

uint8_t getTT();

uint8_t getTL();

void modeNormal();

uint8_t getFlagAuto();

void setFlagAuto();

void setTLacquired(uint8_t acquired);

char* getADCbuf();

void stampato();

int getStampa();

int getElapsedTime();

int getTTTime();

uint8_t getTLAutoMode();

void updateTLAutoMode();

void modeNormal();

void modeAutoSearch();

void SetTriggerLevel(int level);

void SetSamplePeriod(uint32_t periodo_ns);

void HAL_ADC_LevelOutOfWindowCallback(ADC_HandleTypeDef *hadc);

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim);

#endif
