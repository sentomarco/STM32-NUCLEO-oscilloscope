/*
 * dataMnage.c
 *
 *  Created on: 28 gen 2021
 *      Author: sento
 */
#include "dataManage.h"

#define buf_dim 12
#define ADC_BUF_LEN 766
#define UNTIL_TL 384
#define SECONDHALF 191

static volatile uint8_t inputRecived=0;
static char RxBuf[buf_dim];
static uint8_t indiceBuf=0;

void bin2hex(uint8_t binNum, char *ris)
{
    char hexNum[2]="00";
    int i=1;
    uint8_t aux;

    if(binNum<256){
        if(binNum<16){
            hexNum[0]='0';
        }
        while(binNum>0){
            aux=binNum%16;
            binNum=binNum/16;

            if(aux<10){
                hexNum[i]=aux+48;
            }else{
                hexNum[i]=aux-10+65;
            }

            i--;
        }
    }
    ris[0]=hexNum[0];
    ris[1]=hexNum[1];
}


uint8_t charTOint(char ch){

	uint8_t res=5;

	switch(ch){
	case '0':
		res=0;
		break;
	case '1':
		res=1;
		break;
	case '2':
		res=2;
		break;
	case '3':
		res=3;
		break;
	default:
		break;
	}
	return res;
}

void provideOutput(){


	char txBuff[ADC_BUF_LEN*2+2];	//x2 perche ora ogni valore int diventa sue caratteri hex
	char exa[2]="";

	int indice=0;
	txBuff[indice++]='*';

	int last=0, overRange=0, underRange=0;

	last=(ADC_BUF_LEN - 1 - getTLPointer()) + SECONDHALF*2;	//non è detto che sia all'interno dei 766 valori e non dia ovflw....

	if( last >= ADC_BUF_LEN ) {	//dato che ho overflow non avro underflow

		overRange= abs(ADC_BUF_LEN - 1 - last);

		for(int k = overRange - 1 ; k>=0; k-- ) {

			bin2hex(getADCbuf()[k],exa); //riempio da MSB (ultima conversione) verso LSB
			txBuff[indice++]=exa[0]; //MSB
			txBuff[indice++]=exa[1]; //LSB

		}

		for(int k = ADC_BUF_LEN - 1 ; k>(ADC_BUF_LEN - 1 - getTLPointer()) - UNTIL_TL; k-- ) {	//così dovrei aver coperto 191 coppie di valori fino al TL+2 incluso

			bin2hex(getADCbuf()[k],exa); //riempio da MSB (ultima conversione) verso LSB
			txBuff[indice++]=exa[0]; //MSB
			txBuff[indice++]=exa[1]; //LSB

		}


	}

	else{	//Ora se non ho avuto overflow vado tranquillo nella senca metà ma probebilmente avrò underflow


		for(int k = last; k> (ADC_BUF_LEN - 1 - getTLPointer()) ; k-- ) {	//così dovrei aver coperto 191 coppie di valori fino al TL+2 incluso

			bin2hex(getADCbuf()[k],exa); //riempio da MSB (ultima conversione) verso LSB
			txBuff[indice++]=exa[0]; //MSB
			txBuff[indice++]=exa[1]; //LSB

		}

		underRange= UNTIL_TL - (ADC_BUF_LEN - 1 - getTLPointer()) -1; //-1 finale perche si va ad es da 50 a 0 (51 val) e poi da 765 a 433 (333 valori, da 765 a  433)

		for(int k = (ADC_BUF_LEN - 1 - getTLPointer()) ; k>=0  ; k-- ) {	//così dovrei aver coperto 191 coppie di valori fino al TL+2 incluso

			bin2hex(getADCbuf()[k],exa); //riempio da MSB (ultima conversione) verso LSB
			txBuff[indice++]=exa[0]; //MSB
			txBuff[indice++]=exa[1]; //LSB

		}

		for(int k = ADC_BUF_LEN - 1; k> ADC_BUF_LEN - 1 - underRange; k-- ) {

			bin2hex(getADCbuf()[k],exa); //riempio da MSB (ultima conversione) verso LSB
			txBuff[indice++]=exa[0]; //MSB
			txBuff[indice++]=exa[1]; //LSB
		}

	}
	txBuff[indice]='#';

	HAL_UART_Transmit(&huart2, &txBuff, ADC_BUF_LEN*2+2 ,150);
}


uint8_t fillRxBuf(char carattere){


	RxBuf[indiceBuf]=carattere;
	indiceBuf++;
	if(carattere=='#' || indiceBuf==buf_dim){
		indiceBuf=0;
		return 1;	//finita la stringa
	}

	return 0;
}




void analizzaRxBUf(){


  //analizzo il buffer completo
  if(RxBuf[0] == '*'){

	  if (RxBuf[1]=='S' && RxBuf[2]=='P'){

		  if (RxBuf[buf_dim-1]=='#') SetSamplePeriod(hex2dec(RxBuf,8));

	  }else if (RxBuf[1]=='T' && RxBuf[2]=='L'){

		  if (RxBuf[5]=='#') SetTriggerLevel(hex2dec(RxBuf,2));	//setto TL user

	  }else if (RxBuf[1]=='T' && RxBuf[2]=='T'){

		  if (RxBuf[5]=='#') {

			  uint8_t TT_tmp=charTOint(RxBuf[4]);

			  if(RxBuf[3]=='0' && TT_tmp<=3){
				  if(getTT()!=TT_tmp)  SetTT(TT_tmp);

			  	 }
		  	 }
	  	  }

  	  }
}


int hex2dec(char hex[], int valHexSize){

    int val, pos=valHexSize-1, decimal = 0;

    for(int i=3; i<valHexSize+3; i++){

        /* Find the decimal representation of hex[i] */
        if(hex[i]>='0' && hex[i]<='9')
        {
            val = hex[i] - 48;
        }
        else if(hex[i]>='a' && hex[i]<='f')
        {
            val = hex[i] - 97 + 10;
        }
        else if(hex[i]>='A' && hex[i]<='F')
        {
            val = hex[i] - 65 + 10;
        }
        //printf("(%d * 16^%d) + ", val, pos);
        decimal = decimal + (val * pow(16, pos));
        pos--;
    }

    return decimal;
}

uint8_t getStatusRx(){
	return inputRecived;
}

void rstStatusRx(){
	inputRecived=0;
}


//SI ASPETTA ARRIVI UN NUMERO DI CARATTERI PARI A SIZEOF(RXBUF) PRIMA DI ANALIZZARE
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)	//Non riparte da sola fin che non richiamo HAL_UART_Receive_IT
{
	inputRecived=1;
	clear_UART();
}
