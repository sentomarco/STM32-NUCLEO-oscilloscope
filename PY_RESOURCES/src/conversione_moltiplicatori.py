def multiplo_daLettera_aNumero(stringa_numero):
    caratteri_numerici="0123456789."
    numero_stringa=''
    fine=0
    
    for carattere in stringa_numero:
        
        if carattere in caratteri_numerici:
            numero_stringa+=carattere
        else:
            if carattere=='p':
                numero_stringa+="e-12"
            elif carattere=='n':
                numero_stringa+="e-9"
            elif carattere=='u':
                numero_stringa+="e-6"
            elif carattere=='m':
                numero_stringa+="e-3"
            elif carattere=='k' or carattere=='K':
                numero_stringa+="e+3"
            elif carattere=='M':
                numero_stringa+="e+6"
            elif carattere=='G':
                numero_stringa+="e+9"
#             else:
#                 print("non è presente una lettera che è un multiplo")

            fine=1
            return numero_stringa
    return numero_stringa

#viene dato come parametro un numero float e si ricava la corrispondente stringa con un moltiplicatore letterale
def multiplo_daNumero_aLettera(float_numero):
    if type(float_numero)=="<class 'int'>" or type(float_numero)=="<class 'str'>":
         float_numero=float(float_numero)
        
    unita_di_misura= {1e-12:'p', 1e-9:'n', 1e-6:'u', 1e-3:'m', 1:' ', 1000:'k', 1000000:'M', 1000000000:'G'}
        
    for divisore in unita_di_misura.keys():
        risultato=float(float_numero)/divisore
        if risultato < 1000 and risultato >= 1:
            uscita_stringa=str(risultato)[:6]+unita_di_misura.get(divisore)
            diff=7-len(uscita_stringa)
            if diff>0:
                for i in range(diff+1):
                    uscita_stringa=uscita_stringa[:-2]+'0'+uscita_stringa[-2:]
                
            
    return uscita_stringa



# while(1):       
#     numero=input("inserisci numero in lettere:\n")
#     print(numero)
#     print("uscita funz:  ", multiplo_daLettera_aNumero(numero))
#     print("conv float: ", float(multiplo_daLettera_aNumero(numero)))
#     ingresso=str(float(multiplo_daLettera_aNumero(numero)))
#     print("conv float to str: ", ingresso)
# 
#     print("uscita numero-lettere:\n", multiplo_daNumero_aLettera(ingresso))
#     
#     print(multiplo_daLettera_aNumero(multiplo_daNumero_aLettera(ingresso)))