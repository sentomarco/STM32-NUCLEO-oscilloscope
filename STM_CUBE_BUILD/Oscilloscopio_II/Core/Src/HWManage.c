/*
 * HWManage.c
 *
 *  Created on: 28 gen 2021
 *      Author: sento
 */
#include "HWManage.h"

#define ADC_BUF_LEN 766
#define SECONDHALF 191

static volatile int punt_TL=0, punt_TLAuto=0;
static volatile char adc_buf[ADC_BUF_LEN];
static volatile int TLacq=0, stampa=0;
static volatile int  conv_count=0; //elapsed time
static volatile int  TTTime=0; //Trigger Type setup time
static volatile uint8_t trigger_type=0, TL=205;	//TL= HIGH Treshold + 5 per avere margine nella verifica dello slope
static volatile uint8_t flag_TLAutoMode=0, flag_AUTO=0;

void SetSamplePeriod(uint32_t periodo_ns){

	HAL_TIM_Base_Stop(&htim3);
	HAL_TIM_Base_DeInit(&htim3);

	if(periodo_ns<=100000 && periodo_ns>=10000){

		float autoreload=(periodo_ns*21.0/250.0 -1.0);
		htim3.Init.Prescaler = 0;
		htim3.Init.Period = round(autoreload);

	}else if(periodo_ns<=100000000 && periodo_ns>100000){

		float autoreload=(periodo_ns*3.0/25000.0 -1.0);
		htim3.Init.Prescaler = 700;
		htim3.Init.Period = round(autoreload);

	}

	  htim3.Instance = TIM3;
	  htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
	  htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
	  htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
	  HAL_TIM_Base_Init(&htim3);
	  HAL_TIM_Base_Start(&htim3);

}



void SetTriggerLevel(int level){



	if(level<0) level=0;
	else if(level>255) level=250;

	ADC_AnalogWDGConfTypeDef AnalogWDGConfig = {0};
	AnalogWDGConfig.WatchdogMode = ADC_ANALOGWATCHDOG_SINGLE_REG;
    AnalogWDGConfig.Channel = ADC_CHANNEL_0;
    AnalogWDGConfig.ITMode = ENABLE;

	AnalogWDGConfig.HighThreshold = level;
	AnalogWDGConfig.LowThreshold = 0;
	HAL_ADC_AnalogWDGConfig(&hadc1, &AnalogWDGConfig);

	//cambiato il TL si deve rincominciare a riempire metà buffer
	if(level!=TL){
	if(trigger_type==0 )TL=level;
	else TL=level+5;	//Soglia per la corretta acquisizione del TL in modalità non automatica
	TTTime=0;
	conv_count=0;
	TLacq=0;
	}

}



void SetTT(uint8_t TT){

	//SetTriggerLevel(TL_USER);

	switch(TT){
	case 0:	//AUTO
		TTTime=conv_count;
		break;
	case 1:	//NORMAL abilito AWD
		flag_AUTO=0;
		break;
	case 2:	//SINGLE
		TTTime=conv_count;
		break;
	case 3:	//STOP magari far finire il buffer.........................
		HAL_ADC_Stop_DMA(&hadc1);
		HAL_ADC_Stop(&hadc1);
		break;
	default:
		break;
	}

	if(trigger_type==3 && TT!=3){	//solo in questo caso o rischio di resettare buffer
	HAL_ADC_Start(&hadc1);
	HAL_ADC_Start_DMA(&hadc1, (uint8_t*)adc_buf, ADC_BUF_LEN);
	}

	trigger_type=TT;


}

uint8_t getTT(){
	return trigger_type;
}

int getTLPointer(){
	return punt_TL;
}



void setTLPointer(uint16_t TLpunt){
//	puntTL = TLpunt;
}
uint8_t getTL(){
	return 0;
}

uint8_t getTLacquired(){
	return 0;
}

void setTLacquired(uint8_t acquired){
	//TL_acquired=acquired;
}

char* getADCbuf(){
	return &adc_buf;
}


void clear_UART(){
    __HAL_UART_CLEAR_FLAG(&huart2, UART_FLAG_IDLE);
	__HAL_UART_CLEAR_OREFLAG(&huart2);
	__HAL_UART_CLEAR_NEFLAG(&huart2);
	__HAL_UART_CLEAR_FEFLAG(&huart2);
}

int getStampa(){
	return stampa;
}

void stampato(){

	stampa=0;
	TTTime=0;
	conv_count=0;
	TLacq=0;
	HAL_ADC_Start_DMA(&hadc1, &adc_buf, ADC_BUF_LEN);
	HAL_ADC_Start(&hadc1);
}

void setFlagAuto(){
	flag_AUTO=1;
}

int getElapsedTime(){
	return conv_count;
}

int getTTTime(){
	return TTTime;
}

uint8_t getTLAutoMode(){
	return flag_TLAutoMode;
}

void updateTLAutoMode(){	//per "spezzare" l'interrupt

	SetTriggerLevel(adc_buf[ADC_BUF_LEN - 1 - punt_TLAuto]);
	punt_TL=punt_TLAuto;
	TLacq=1;
	conv_count=0;
	flag_AUTO=0;
	flag_TLAutoMode=0;
}

void HAL_ADC_LevelOutOfWindowCallback(ADC_HandleTypeDef *hadc){


	if(TLacq==0 && conv_count>= (SECONDHALF+2)) {	//ho acquisito già sufficienti valori prima del primo trigger

		if(flag_AUTO==1) modeAutoSearch();
		else modeNormal();
	}

}

void modeNormal(){

	int tmp = (int) DMA2_Stream0->NDTR-1;


	//check sui valori del puntatore
	if(tmp> ADC_BUF_LEN - 1) tmp=ADC_BUF_LEN - 2;
	else if(tmp<0)  tmp=0;

	//check su possibile underflow
	if(ADC_BUF_LEN - 1 - tmp - 2 >= 0){

		//check sullo slope e che abbia passato il TL (Potrebbero essere val sì a slope+ ma entrambi al di sopra del TL)
		if(adc_buf[ADC_BUF_LEN - 1 - tmp - 2] < TL){


			punt_TL=tmp;
			TLacq=1;
			conv_count=0;
		}

	//check sullo slope in caso di underflow
	}else if(adc_buf[ ( (ADC_BUF_LEN - 1)*2 - tmp - 2) +1 ] < TL ){

		punt_TL=tmp;
		TLacq=1;
		conv_count=0;

	}

}

void modeAutoSearch(){

	int tmp = (int) DMA2_Stream0->NDTR-1;

		//check sui valori del puntatore
		if(tmp> ADC_BUF_LEN - 1) tmp=ADC_BUF_LEN - 2;
		else if(tmp<0)  tmp=0;

		//check su possibile underflow
		if(ADC_BUF_LEN - 1 - tmp - 2 >= 0){

			//check sullo slope
			if(adc_buf[ADC_BUF_LEN - 1 - tmp - 2] < adc_buf[ADC_BUF_LEN - 1 - tmp]){

				flag_TLAutoMode=1;
				punt_TLAuto=tmp;
			}

		//check sullo slope in caso di underflow
		}else if(adc_buf[ ( (ADC_BUF_LEN - 1)*2 - tmp - 2) +1 ] < adc_buf[ADC_BUF_LEN - 1 - tmp] ){

			flag_TLAutoMode=1;
			punt_TLAuto=tmp;
		}
}


void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim){	//In teoria chiamata prima di ADC_outOfWindow

	conv_count++;
	if(conv_count==SECONDHALF && TLacq==1){	//conto 191 coppie di valori dopo la coppia del TL

		HAL_ADC_Stop(&hadc1);
		HAL_ADC_Stop_DMA(&hadc1);
		stampa=1;

	}

}
