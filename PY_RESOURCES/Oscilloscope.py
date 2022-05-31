#!/bin/python3

#importa librerie per la creazione di una interfaccia grafica
from tkinter import *
from tkinter import ttk
import time
from sys import exit

#importa libreria funzioni di conversione tra moltiplicatori delle unità di misura e float
from src import *

WIDTH = 645
HEIGHT = 515
X = 10
Y = 35

MIN_F_CAMP=10
MAX_F_CAMP=100e3

MIN_TIGGET_LEVEL=1
MAX_TIGGET_LEVEL=256

FPS=60
TEMPO_AGGIORNAMENTO_DISPLAY_MS=(1/FPS)*1000

def disegna_grafico(punti):
    global CH1, CH2
    griglia.delete(CH1)
    griglia.delete(CH2)
    if type(punti)!="<class 'int'>":
    #    print(punti)
        stringa_linea_ch1=[]
        stringa_linea_ch2=[]
        indice_elemento_lista_punti=1
        for punto in punti:
            if indice_elemento_lista_punti > 0:
                if indice_elemento_lista_punti%2 == 0:
                    stringa_linea_ch1.append(int(indice_elemento_lista_punti/2) -0)
                    stringa_linea_ch1.append(255-punto)
                else:
                    stringa_linea_ch2.append(int((indice_elemento_lista_punti-1)/2) -0)
                    stringa_linea_ch2.append(255-punto)
                    
            indice_elemento_lista_punti+=1
        
        #print(stringa_linea_ch1)
        try:    #MIA AGGIUNTA TRY e EXCEPT O NON VA SE NULLA é ATTACCATO-----------------------------------------------------------------------------------------------------
            CH1 = griglia.create_line(stringa_linea_ch1, fill="white")
            CH2 = griglia.create_line(stringa_linea_ch2, fill="yellow")
        except:
            pass
        
    else:
        print("errore porta")

def esci():
    global uscita
    uscita=1
    if porta_scelta.get() == 'No Port':
        finestra.quit()
        finestra.destroy()


def set_port_funz():
    global porta_scelta
    global Select_COM
    com_nuova=porta_scelta.get()
    apri_porta_seriale(Select_COM, com_nuova)
    Select_COM=com_nuova
    #main_s(tipo_scelto, tempo_campionamento_scelto, Trigger_level_scelto)

    
    
def Set_type_funz():
    global tipo_scelto
    global Trigger_Type
    Trigger_Type_vecchio=Trigger_Type
    global stop
    Trigger_Type=tipo_scelto.get()
    if Trigger_Type=='Default' or Trigger_Type=='Auto':
        Trigger_Type='*TT00#'
    elif Trigger_Type=='Normal':
        Trigger_Type='*TT01#'
    elif Trigger_Type=='Single':
        Trigger_Type='*TT02#'
    elif Trigger_Type=='Stop':
        Trigger_Type='*TT03#'

    frame_da_inviare(Trigger_Type)
    
    if stop == 1 and Trigger_Type!='*TT03#':
        stop=0
        ricezione_periodica_messaggio()

    
    finestra.after(600, set_Trigger_Level_funz)
    


    
def set_T_camp_num_funz():
    global tempo_campionamento_scelto
    
    F_camp_scelto=F_camp.get()
    F_camp_scelto_num=float(conversione_moltiplicatori.multiplo_daLettera_aNumero(F_camp_scelto))
#controllo sul range del tempo di  campionamento inserito
    if F_camp_scelto_num < MIN_F_CAMP:
        F_camp_scelto_num=MIN_F_CAMP
        stringa_errore_tempo_camp.set('Out of range,\nminimum value set.')
        
    elif F_camp_scelto_num > MAX_F_CAMP:
        F_camp_scelto_num=MAX_F_CAMP
        stringa_errore_tempo_camp.set('Out of range,\nmaximum value set.')
        
    else:
        stringa_errore_tempo_camp.set('                                 ')
        
    
    tempo_campionamento_scelto=1/F_camp_scelto_num
    tempo_da_scale.set(tempo_campionamento_scelto)
    tempo_pannello.set(' → '+conversione_moltiplicatori.multiplo_daNumero_aLettera(tempo_campionamento_scelto)+'s')
#settaggio asse dei tempo del diplay
    scala=conversione_moltiplicatori.multiplo_daNumero_aLettera(float(conversione_moltiplicatori.multiplo_daLettera_aNumero(str(tempo_campionamento_scelto*256))))+'s'
    asse_orizzontale.itemconfigure(Asse_O_High, text=scala)
    scala=conversione_moltiplicatori.multiplo_daNumero_aLettera(float(conversione_moltiplicatori.multiplo_daLettera_aNumero(str(tempo_campionamento_scelto/2*256))))+'s'
    asse_orizzontale.itemconfigure(Asse_O_med, text=scala)
    Sampling_Period='*SP'+hex(int(tempo_campionamento_scelto*10e8))[2:].zfill(8)+'#' #deve essere in ns
    frame_da_inviare(Sampling_Period)
    

def set_tempo_camp_scale(*arg):
    global tempo_da_scale
    global tempo_campionamento_scelto
    tempo_campionamento_scelto=tempo_da_scale.get()
    global F_camp
    F_buff=1/tempo_campionamento_scelto
    F_camp_scelto=conversione_moltiplicatori.multiplo_daNumero_aLettera(F_buff)
    F_camp.set(F_camp_scelto)
    set_T_camp_num_funz()
    
def set_livello_scale(*arg):
    global Trigger_level_in
    Trigger_level_in.set(livello_da_scale.get())
    set_Trigger_Level_funz()
    
def set_Trigger_Level_funz():
    global Trigger_level_scelto
    Trigger_level_scelto=Trigger_level_in.get()
    livello_da_scale.set(Trigger_level_scelto)
#controllo sul range del tempo di  campionamento inserito
    if Trigger_level_scelto < MIN_TIGGET_LEVEL:
        Trigger_level_scelto=MIN_TIGGET_LEVEL
        stringa_errore_trigget_level.set('Out of range,\nminimum value set.')
        
    elif Trigger_level_scelto > MAX_TIGGET_LEVEL:
        Trigger_level_scelto=MAX_TIGGET_LEVEL
        stringa_errore_trigget_level.set('Out of range,\nmaximum value set.')
        
    else:
        stringa_errore_trigget_level.set('                                 ')
        

    trigger_in_V=Trigger_level_scelto/256*3.3

    livello_trig_pannello.set(' → %.3f V' %trigger_in_V)
    
    global trigger_grafico
    global Asse_V_trigger
    global trigger_grafico_tela_asse_V
    griglia.delete(trigger_grafico)
    asse_verticale.delete(Asse_V_trigger)
    asse_verticale.delete(trigger_grafico_tela_asse_V)
    livello_trigger_grafico=256-Trigger_level_scelto
    trigger_grafico = griglia.create_line( 0, livello_trigger_grafico+1, 384, livello_trigger_grafico+1, fill="blue", dash = (5, 2))
    trigger_grafico_tela_asse_V = asse_verticale.create_line( 37, livello_trigger_grafico+9, 50, livello_trigger_grafico+9, 45, livello_trigger_grafico+7, 45, livello_trigger_grafico+11, 50, livello_trigger_grafico+9,  fill="blue")
    
    if livello_trigger_grafico<8:
        scostamento_trigger_testo=3 + 9
    elif livello_trigger_grafico<=128 and livello_trigger_grafico>116:
        scostamento_trigger_testo=128 +3 - 11
    elif livello_trigger_grafico>128 and livello_trigger_grafico<138:
        scostamento_trigger_testo=128 +3 + 11
    elif livello_trigger_grafico>256-20:
        scostamento_trigger_testo=256 +3 - 19
    else:
        scostamento_trigger_testo=livello_trigger_grafico + 4
        
    Asse_V_trigger = asse_verticale.create_text(0, scostamento_trigger_testo , anchor=N+W,  text='    %.1fV' %trigger_in_V, width=40, fill="blue",  font='Helvetica 8')

    Trigger_Level='*TL'+hex(Trigger_level_scelto-1)[2:].zfill(2)+'#'
    frame_da_inviare(Trigger_Level)

    
def frame_da_inviare(frame):
    global frame_da_inviare_s
    frame_da_inviare_s=frame
    invia_carattere()
        
def invia_carattere():
    global frame_da_inviare_s
    global indice_frame
    #print(frame_da_inviare_s[indice_frame])
    invia_carattere_serial(frame_da_inviare_s[indice_frame])
    if frame_da_inviare_s[indice_frame] != '#':
        finestra.after(60, invia_carattere)
        indice_frame+=1
    else:
        indice_frame=0

def CommandStop():
    global tipo_scelto
    global stop
    tipo_scelto.set("Stop")
    stop=1
    Trigger_Type='*TT03#'
    frame_da_inviare(Trigger_Type)
            


def ricezione_periodica_messaggio():
    messaggio_ricevuto=ricevi_messaggio()
    global Select_COM
    if type(messaggio_ricevuto)!="<class 'int'>":
        global uscita
        
        try:
            if uscita==0:
                if stop == 0:
                    finestra.after(int(TEMPO_AGGIORNAMENTO_DISPLAY_MS), ricezione_periodica_messaggio)
                    if len(messaggio_ricevuto) > 0:
                        disegna_grafico(messaggio_ricevuto)
                #print("ricezione_periodica_messaggio", messaggio_ricevuto)

            else:
                finestra.after(200,finestra.quit())
                finestra.after(200,finestra.destroy())
            
        except:
            print("fine esecuzione")
    else:
        messaggio_ricevuto=0

        
    return messaggio_ricevuto
        
        
        
#creazione di una finestra
finestra = Tk()
finestra.title("SL oscilloscope")
finestra.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, X, Y))
uscita=0
indice_frame=0
Trigger_Type='*TT00#'

stop=0
F_camp=StringVar()
F_camp.set("1k")
F_camp_scelto=F_camp.get()
tempo_campionamento_scelto=1/float(conversione_moltiplicatori.multiplo_daLettera_aNumero(F_camp_scelto))

Trigger_level_in=IntVar()
Trigger_level_in.set(128)
Trigger_level_scelto=Trigger_level_in.get()
trigger_in_V=Trigger_level_scelto/256*3.3
stringa_errore_trigget_level=StringVar()
stringa_errore_trigget_level.set('                                 ')
frame_da_inviare_s=''

scala=tempo_campionamento_scelto*256
scala=conversione_moltiplicatori.multiplo_daNumero_aLettera(scala)+'s'

#creazione dei frame che contengono diversi componenti in base alle funzioni

box_sx = ttk.Frame(finestra, padding= "0 0 0 0")
box_sx.grid(column = 0, row = 0, rowspan=3, sticky=(N, W, E), padx=0, pady=0)
box_sx.columnconfigure(0, weight=1)
box_sx.rowconfigure(0, weight=1)

box_dx = ttk.Frame(finestra, padding= "0 0 0 0")
box_dx.grid(column = 1, row = 0, rowspan=3, sticky=(N, W, E), padx=0, pady=0)
box_dx.columnconfigure(0, weight=1)
box_dx.rowconfigure(0, weight=1)


box_display = ttk.Frame(box_sx, padding= "5 5 5 5", relief=RAISED)
box_display.grid(column = 0, row = 0, rowspan=3, sticky=(N, W, E), padx=10, pady=10)
box_display.columnconfigure(0, weight=1)
box_display.rowconfigure(0, weight=1)

box_porta_seriale = ttk.Frame(box_sx, padding= "5 5 5 5", relief=SUNKEN)
box_porta_seriale.grid(column = 0, row = 3, sticky=(N, E, W), padx=10, pady=10)
box_porta_seriale.columnconfigure(0, weight=1)
box_porta_seriale.rowconfigure(0, weight=1)

box_trigger_type = ttk.Frame(box_dx, padding= "5 5 5 5", relief=SUNKEN)
box_trigger_type.grid(column = 3, row = 0, sticky=(N, E, W), padx=10, pady=10)
box_trigger_type.columnconfigure(0, weight=1)
box_trigger_type.rowconfigure(0, weight=1)

box_time_sample = ttk.Frame(box_dx, padding= "5 5 5 5", relief=SUNKEN)
box_time_sample.grid(column = 3, row = 1, sticky=(N, E, W), padx=10, pady=10)
box_time_sample.columnconfigure(0, weight=1)
box_time_sample.rowconfigure(0, weight=1)

box_trigger_level = ttk.Frame(box_dx, padding= "5 5 5 5", relief=SUNKEN)
box_trigger_level.grid(column = 3, row = 2, sticky=(N, E, W), padx=10, pady=10)
box_trigger_level.columnconfigure(0, weight=1)
box_trigger_level.rowconfigure(0, weight=1)

#---------------------selezione porta seriale e pulsante uscita
lista_porte_disponibili=porte_seriali_disponibili()
#lista_porte_disponibili.append("/dev/ttyACM0")  #MIA AGGIUNTA per forzare il get del dispo-----------------------------------------------------------------------------------------------------
if(len(lista_porte_disponibili)<1): #CI VA---------------------------------------------------------------------------------
    exit("Non è stato possibile identificare il dispositivo.\nIl programma verrà terminato.") #--------------------------------------------------
    
#print('uscito dalla funzione porte seriali disponibili')
porta_scelta=StringVar()
porta_scelta.set(lista_porte_disponibili[0])
opzione_porte = ttk.Combobox(box_porta_seriale, textvariable = porta_scelta, height=60, width=15)
opzione_porte['value'] = lista_porte_disponibili
opzione_porte.grid(row=0,column=1, sticky=(), padx=5, pady=15)

Label(box_porta_seriale, text="Serial Port", justify=CENTER, font='Helvetica 12 bold').grid(row=0,column=0, sticky=(W), padx=5, pady=15)

Set_com = Button(box_porta_seriale, text= "Set", command=set_port_funz, justify=CENTER)
Set_com.grid(row=0,column=2, sticky=(NE), padx=15, pady=15)
Select_COM=porta_scelta.get()

#-----------------pulsante uscita
quit_butt = Button(box_porta_seriale, text= "Quit", command=esci, justify=CENTER)
quit_butt.grid(row=1,column=0, columnspan=3, sticky=(N+E+W), padx=15, pady=15)

#-----------------------------------------------------------------display oscilloscopio
asse_verticale = Canvas(box_display, height=265, width=50)
asse_verticale.grid(row=0,column=0, padx = 0, pady = 5)

griglia = Canvas(box_display, bg="black", height=256, width=256, scrollregion=(0,0,384,256))
hbar=Scrollbar(box_display, orient=HORIZONTAL)
hbar.grid(row=10, column=0, columnspan=10, sticky = S+W+E)
hbar.config(command=griglia.xview)
griglia.config(width=256, height=256)
griglia.config(xscrollcommand=hbar.set)
griglia.grid(row=0, column=1, padx = 5, pady = 5, sticky = SW)


asse_orizzontale = Canvas(box_display, height=40, width=318)
asse_orizzontale.grid(row=1,column=0, columnspan=2, padx = 0, pady = 5, sticky = SW)

#assi
Asse_V = asse_verticale.create_line(45, 6, 45, 265, fill="black")
Asse_V_freccia = asse_verticale.create_line(45, 1, 50, 6, 40, 6, 45, 1, fill="black")
Asse_O = asse_orizzontale.create_line(55, 6, 314, 6, fill="black")
Asse_O_freccia = asse_orizzontale.create_line(318, 6, 313, 11, 313, 1, 318, 6, fill="black")

#indice assi
#Y
Asse_V_High = asse_verticale.create_text(5, 0, anchor=NW,  text="3.3V")
Asse_V_Med = asse_verticale.create_text(0, 130, anchor=NW,  text="1.65V", width=40)
Asse_V_Low = asse_verticale.create_text(5, 265, anchor=SW,  text="   0V")
#X

Asse_O_High = asse_orizzontale.create_text(314, 13, anchor=NE,  text=scala)
#scala=scala/4*3
#Asse_O_High_med = asse_orizzontale.create_text(314/4*3-(len(str(scala))*7)/3, 25, anchor=NW,  text=str(scala)+'s')
scala=tempo_campionamento_scelto*256/2
scala=conversione_moltiplicatori.multiplo_daNumero_aLettera(scala)+'s'
Asse_O_med = asse_orizzontale.create_text(314/2, 13, anchor=NW,  text=scala)
#scala=scala/4
#Asse_O_Low_med = asse_orizzontale.create_text(314/4-(len(str(scala))*6)/4, 25, anchor=NW,  text=str(scala)+'s')
Asse_O_Low = asse_orizzontale.create_text(40, 13, anchor=NW,  text="   0s")

#--------------------------------------------------------------------griglia display
Gr1v = griglia.create_line(64, 0, 64, 256, fill="grey")
Gr2v = griglia.create_line(128, 0, 128, 256, fill="grey")
Gr3v = griglia.create_line(192, 0, 192, 256, fill="grey")
Gr3v = griglia.create_line(256, 0, 256, 256, fill="grey")
Gr3v = griglia.create_line(320, 0, 320, 256, fill="grey")
Gr1o = griglia.create_line( 0, 64, 384, 64, fill="grey")
Gr2o = griglia.create_line( 0, 128+1, 384, 128+1, fill="grey")
Gr3o = griglia.create_line( 0, 192, 384, 192, fill="grey")
#canali visualizzati
CH1 = griglia.create_line(0, 0, 0, 0, fill="white")
CH2 = griglia.create_line(0, 0, 0, 0, fill="yellow")
#------------------------------------selezione tipo di trigger

#selezione scelta tipo trigger con una combo box, di default la variabile della combobox vale "Default"
typeTrigger = (
                "Auto",
                "Normal",
                "Single"
              )
tipo_scelto=StringVar()
tipo_scelto.set("Default")
opzione = ttk.Combobox(box_trigger_type, textvariable = tipo_scelto, height=20, width=6)
opzione['value'] = typeTrigger
opzione.grid(row=0,column=2, sticky=(NW), padx=5, pady=11)

Label(box_trigger_type, text="Trigger Type", justify=CENTER, font='Helvetica 18 bold').grid(row=0,column=0, columnspan=2, sticky=(NW), padx=5, pady=5)

Stop_Button = Button(box_trigger_type, text= "Stop", command=CommandStop, justify=CENTER)
Stop_Button.grid(row=1,column=0, sticky=(NW), padx=15, pady=8)

Set_type = Button(box_trigger_type, text= "Set", command=Set_type_funz, justify=CENTER)
Set_type.grid(row=1,column=1, sticky=(NW), padx=15, pady=8)

#--------------------------------------------tempo di campionamento

tempo_pannello=StringVar()
stringa_errore_tempo_camp=StringVar()
tempo_da_scale=DoubleVar()
tempo_pannello.set(' → '+conversione_moltiplicatori.multiplo_daNumero_aLettera(tempo_campionamento_scelto)+'s')
stringa_errore_tempo_camp.set('                                 ')
#titolo
Label(box_time_sample, text="Sampling Period", justify=CENTER, font='Helvetica 18 bold').grid(row=0,column=0, columnspan=3, sticky=(NW), padx=5, pady=5)
#entry frequenza di campionamento
numero_periodo_camp = Entry(box_time_sample, textvariable = F_camp,  width=7, justify=RIGHT)
numero_periodo_camp.grid(row=1,column=0, sticky=(), padx=3, pady=5)
Label(box_time_sample, text="sample/s", justify=LEFT, font='Helvetica 10').grid(row=1,column=1, sticky=(NW), pady=5, padx=0)
Label(box_time_sample, textvariable=tempo_pannello, justify=LEFT, font='Helvetica 10').grid(row=1,column=2, sticky=(N+E), pady=5, padx=0)
#pulante per settare il tempo e la frequenza di campionamento
set_T_camp_num = Button(box_time_sample, command=set_T_camp_num_funz, text="Set")
set_T_camp_num.grid(row=2,column=0, sticky=(NW), padx=15, pady=5)
#label errore fuoriscala
Label(box_time_sample, textvariable=stringa_errore_tempo_camp, justify=LEFT, font='Helvetica 8', fg='red').grid(row=2,column=1, columnspan=2, pady=5, padx=5)
#scale
scale_tempo = Scale( box_time_sample, variable = tempo_da_scale, from_=0.00001, to_=0.1,
                     resolution=0.00001, showvalue=0, label='Time bar', orient=HORIZONTAL, command=set_tempo_camp_scale)
scale_tempo.grid(row=3,column=0, columnspan=3, sticky=(N+W+E), padx=5, pady=5)


#-------------------------------------------livello di trigger, selezione in 1:256

livello_trig_pannello=StringVar()
livello_da_scale=IntVar()
stringa_errore_livello_trigger=StringVar()
livello_trig_pannello.set(' → %.3f V' %trigger_in_V)
stringa_errore_livello_trigger.set('                                 ')
#titolo
Label(box_trigger_level, text="Trigger Level", justify=CENTER, font='Helvetica 18 bold').grid(row=0,column=0, columnspan=3, sticky=(NW), padx=5, pady=5)
#entry frequenza di campionamento
livello_trigger_entry = Entry(box_trigger_level, textvariable = Trigger_level_in,  width=3, justify=RIGHT)
livello_trigger_entry.grid(row=1,column=0, sticky=(), padx=3, pady=5)
Label(box_trigger_level, text="samples", justify=LEFT, font='Helvetica 10').grid(row=1,column=1, sticky=(W+W), pady=5, padx=0)
Label(box_trigger_level, textvariable=livello_trig_pannello, justify=LEFT, font='Helvetica 10').grid(row=1,column=2, sticky=(N+E), pady=5, padx=10)
#pulante per settare il tempo ela frequenza di campionamento
set_T_camp_num = Button(box_trigger_level, command=set_Trigger_Level_funz, text="Set")
set_T_camp_num.grid(row=2,column=0, sticky=(N+W), padx=15, pady=5)
#label errore fuoriscala
Label(box_trigger_level, textvariable=stringa_errore_trigget_level, justify=LEFT, font='Helvetica 8', fg='red').grid(row=2,column=1, columnspan=2, pady=5, padx=5)

#scale
scale_livello = Scale( box_trigger_level, variable = livello_da_scale, from_=1, to_=256,
                     showvalue=0, label='Level bar', orient=HORIZONTAL, command=set_livello_scale)
scale_livello.grid(row=3,column=0, columnspan=3, sticky=(N+W+E), padx=5, pady=5)
#trigger grafico
livello_trigger_grafico=256-Trigger_level_in.get()
scostamento_trigger_testo=livello_trigger_grafico+3
trigger_grafico = griglia.create_line( 0, livello_trigger_grafico+1, 384, livello_trigger_grafico+1, fill="blue", dash = (5, 2))
Asse_V_trigger = asse_verticale.create_text(0, scostamento_trigger_testo-11, anchor=N+W,  text='    %.1fV' %trigger_in_V, width=40, fill="blue",  font='Helvetica 8')
trigger_grafico_tela_asse_V = asse_verticale.create_line( 37, livello_trigger_grafico+9, 50, livello_trigger_grafico+9, 45, livello_trigger_grafico+7, 45, livello_trigger_grafico+11, 50, livello_trigger_grafico+9,  fill="blue")


apri_porta_seriale(Select_COM, Select_COM)

##buff_type=tipo_scelto.get()
##if buff_type=='Default' or buff_type=='Auto':
##    Trigger_Type='*TT00#'
##elif buff_type=='Normal':
##    Trigger_Type='*TT01#'
##elif buff_type=='Single':
##    Trigger_Type='*TT02#'
##elif buff_type=='Stop':
##    Trigger_Type='*TT03#'
##
##Sampling_Period='*SP'+hex(int(tempo_campionamento_scelto*10e9))[2:].zfill(8)+'#' #deve essere in ns
##          
##Trigger_Level='*TL'+hex(Trigger_level_scelto-1)[2:].zfill(2)+'#' #deve essere in samples
##
##invia_messaggio(Trigger_Type, Sampling_Period, Trigger_Level)

#main_s(tipo_scelto, tempo_campionamento_scelto, Trigger_level_scelto)

disegna_grafico(ricezione_periodica_messaggio())


Sampling_Period='*SP00002710#' #deve essere in ns
frame_da_inviare(Sampling_Period)

finestra.mainloop()
