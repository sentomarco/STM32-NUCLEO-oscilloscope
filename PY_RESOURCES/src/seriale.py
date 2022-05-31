import serial
import time
import random
from serial.tools import list_ports
from sys import exit

def porte_seriali_disponibili():
    '''
    suffissi = "S", "USB", "ACM", "AMA"
    lista_nomi = ["COM"] + ["/dev/tty%s" % suffisso for suffisso in suffissi]
    
    lista_porte = []
    #lista_porte.append('COM5')
    for nome in lista_nomi:
        for numero_porta in range(48, 0, -1):
            nome_porta = "%s%s" % (nome, numero_porta)
            
            try:
                serial.Serial(nome_porta).close()
                if nome_porta!="/dev/ttyAMA0":
                    lista_porte.append(nome_porta)
            except IOError:
                pass
    '''
    lista_porte = list(list_ports.comports())
    i=0
    for nome in lista_porte:
        lista_porte[i]=str(nome).split(" ")[0]
        i+=1
    '''if len(lista_porte)==0:
        #lista_porte.append("No Port")
        if(len(lista_porte_disponibili)<1): 
            exit("Non è stato possibile identificare il dispositivo.\nIl programma verrà terminato.")
    '''
    
    return lista_porte

def invia_messaggio(Trigget_Type, Sampling_Period, Trigger_Level):
    
    global porta_seriale_aperta
    
    try:
        for char in Trigget_Type+Sampling_Period+Trigger_Level:
            porta_seriale_aperta.write(char.encode('ascii'))
            #time.sleep(0.045)
            #print(char)
        
#         print(porta_seriale_aperta.write(Trigget_Type.encode('ASCII')))    
#         print(porta_seriale_aperta.write(Sampling_Period.encode('ASCII')))    
#         print(porta_seriale_aperta.write(Trigger_Level.encode('ASCII')))
    except:
        print("messaggi non inviati")

def apri_porta_seriale(vecchia_com, com_nuova):
    global porta_seriale_aperta
    try:
        porta_seriale_aperta = serial.Serial(com_nuova, 115200, timeout=1000)
    except:
        print(com_nuova, "non aperta")
        if(vecchia_com!=com_nuova):
            porta_seriale_aperta = serial.Serial(vecchia_com, 115200) 
        else:
            exit("Non è stato possibile comunicare con il dispositivo.\nIl programma verrà terminato.")
    
def risposta_presente():
    global porta_seriale_aperta
    char_b = porta_seriale_aperta.read()
    if char_b!='':
        return False
    else:
        return True

    
def ricevi_messaggio():
    list_byte=[]
    
    #porta_seriale_aperta = serial.Serial('/dev/ttyUSB0', 115200)
    global porta_seriale_aperta
    
    #message = porta_seriale_aperta.read(1026)
    #print(message)
    
    flag=0
    message='00'


    
    if porta_seriale_aperta.inWaiting() > 0:
        while(str(message)[-2]!='#'):
            char_b = porta_seriale_aperta.read()
            #print(char_b)
            #for char in data:
            char=char_b
            #type(char)
            #print("\t\t\t\t", char)
            if char == b'*':
                flag=1
                message=char
            if char == b'#' and flag == 1:
                message+=char
                flag=0
                #print('message:\n',str(message))
            if flag==1:
                message+=char
        porta_seriale_aperta.flush()
    else:
        return list_byte
#         else:
#             for i in range(1026):
#                 if i == 0:
#                     message='*'
#                 elif i == 1025:
#                     message+='#'
#                 else:
#                     message+='130'
        #print(message)
        
    #--------------------------------simulazione messaggio ricavuto da seriale
#     try:
#         #global porta_seriale_aperta
#         message = porta_seriale_aperta.read(1026)
#         print(message)
# 
#     except:
        

    #--------------------------------messaggio non ricavuto da seriale
    try:
        message=str(message)
        if message[3]=='*' and message[-2]=='#':
            message=message[4:-2]
            #print(message)
            for i in range(len(message)):
                if (i+1)%2==0:
                    num=int(message[i-1]+message[i],16)
                    #print(num)
                    list_byte.append(num)
        else:
            print("error message\n")
            message_sim=''
            #random simulate message
            for i in range(256):
                message_sim+=hex(random.randint(0,i))[2:].zfill(2)+hex(random.randint(0,255-i))[2:].zfill(2)

            for i in range(len(message_sim)):
                if (i+1)%2==0:
                    list_byte.append(int(message_sim[i-1]+message_sim[i],16)) 

    except:
            print("error message\n")
            message_sim=''
            #random simulate message
            for i in range(256):
                message_sim+=hex(random.randint(0,i))[2:].zfill(2)+hex(random.randint(0,255-i))[2:].zfill(2)

            #message_sim=message_sim[1:-1]
            for i in range(len(message_sim)):
                if (i+1)%2==0:
                    list_byte.append(int(message_sim[i-1]+message_sim[i],16))
    list_byte=inverti(list_byte)
        
    return list_byte

def inverti(dati):
    dati_inv=[]
    for dato in dati:
        dati_inv.insert(0, dato)
    
    return dati_inv


def main_s(tipo_scelto, tempo_campionamento_scelto, Trigger_level_scelto):
    #costruzione delle  stringhe da inviare tramite seriale
    buff_type=tipo_scelto.get()
    if buff_type=='Default' or buff_type=='Auto':
        Trigget_Type='*TT00#'
    elif buff_type=='Normal':
        Trigget_Type='*TT01#'
    elif buff_type=='Single':
        Trigget_Type='*TT02#'
    elif buff_type=='Stop':
        Trigget_Type='*TT03#'

    Sampling_Period='*SP'+hex(int(tempo_campionamento_scelto*10e9))[2:].zfill(8)+'#' #deve essere in ns
      
    Trigger_Level='*TL'+hex(Trigger_level_scelto-1)[2:].zfill(2)+'#' #deve essere in samples

    invia_messaggio(Trigget_Type, Sampling_Period, Trigger_Level)

def invia_carattere_serial(carattere_da_inviare):
    global porta_seriale_aperta
    print(carattere_da_inviare)
    porta_seriale_aperta.write(carattere_da_inviare.encode('ascii'))
        
        
        
        
        
        
        
