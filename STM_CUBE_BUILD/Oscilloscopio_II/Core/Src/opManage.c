/*
 * opManage.c
 *
 *  Created on: 28 gen 2021
 *      Author: sento
 */

#include "opManage.h"
#define ADC_BUF_LEN 766
static volatile char RxData[1];

void HWInit(){

	  HAL_ADC_Start_DMA(&hadc1, (uint8_t*)getADCbuf(), ADC_BUF_LEN);
	  HAL_TIM_Base_Start_IT(&htim3);
	  HAL_UART_Receive_IT(&huart2, &RxData, sizeof(RxData));
}


void opLoop(){

	  if(getStampa()==1){

		  provideOutput();
		  stampato();

		  if(getTT()==2) SetTT(3);
	  }

	  // getElapsedTime(),getTTTime() resettati a ogni stampa
	  //chiamata ogni volta che in modalità automatica si perde Trigger su un buffer
	  if(getTT()==0 && getElapsedTime()-getTTTime() > ADC_BUF_LEN/2){	//quando siamo ad ADC_BUF_LEN/2 in realtà ha gia acquisito ADC_BUF_LEN valori

		  SetTriggerLevel(0);	//resetta anche i tempi
		  setFlagAuto(); //resettato quando viene trovato il trigger level in modalità automatica

	  }
	  if(getTT()==2 && getElapsedTime()-getTTTime() > ADC_BUF_LEN/2) SetTT(3);

	  if(getTLAutoMode()==1) updateTLAutoMode();	//eseguita quando viene trovato il trigger level in modalità automatica

	  /////////////////ricezione//////////////////

		if(getStatusRx()==1){	//così sono sicuro che tra un IR e l'altro eseguo il loop

			rstStatusRx();
			//operazione sul dato

			if(fillRxBuf(RxData[0])==1) analizzaRxBUf();

			//abilito IR per nuovo dato
			HAL_UART_Receive_IT(&huart2, &RxData, sizeof(RxData));
		}

}

