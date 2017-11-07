from random import randint


def SignalSwapError(message,n):
    res=""
    for i in range(len(message)):
        if i==n:
            if message[i]=='-':
                res+='+'
            else:
                res+='-'
        else:
            res+=message[i]
    return res

def SignalSwapsError2(message,n):
    if n >= len(message):
        return message
    if message[n]=='+':
        mess=message[0:n]+message[n].replace("+","-")+message[n+1::]
    elif message[n]=='-':
        mess=message[0:n]+message[n].replace("-","+")+message[n+1::]
    return mess



def parityBit2(message):
    nb1=0
    res=''
    pack=0
    for i in range(len(message)):
        res+=message[i]
        if message[i]=='1':
            nb1+=1
        if (i+1)%7==0 and i != 0:
            res+=str(nb1%2)
            nb1=0
            pack+=1
    if len(message)-7*pack !=0:
        res+=str(nb1%2)
    return res

#Réaliser le test et comparer les résultats       
            
##print('=========================== TEST DE PARITY ========================')
##print(parityBit2("10101011011101"))
##print("\n\n")
    

def parityBit(message):
    nb1=0
    for i in range(len(message)):
        if message[i]=='1':
            nb1+=1
    if nb1%2==0:
        return message+'0'
    else:
        return message+'1'

def testParityBit(message): ## Inutile
    x=0
    messagedouverture='-++++++-'
    longO=len(messagedouverture)
    while message[x:x+longO]!=messagedouverture:
        x+=1
    long=int(couche1R(message[x+longO:x+(longO+8)]),2)-1 # -1 car on ne compte pas le bit de parité dans le message.
    print("Longueur du message: "+str(long))
    message_from_sender=message[x+longO+8:x+longO+8+long]
    print(message_from_sender)
    Bit=message[x+longO+8+long]
    nb1=0
    for i in range(len(message_from_sender)):
        if message_from_sender[i]=='+':
            nb1+=1
    Parity_supposed=""
    if nb1%2==0:
        Parity_supposed="-"
    else:
        Parity_supposed="+"
    if Bit != Parity_supposed:
        print("|!| Erreur de transfert |!|")
        return False
    else:
        return True

def doubleParity(message):
    long=4
    parity=""
    res=""
    nb1Hor=0
    nb1Ver=0
    lpack=[]
    last= len(message)-((len(message)//long)*long)
    for i in range (len(message)):
        res+=message[i]
        lpack.append(message[i])
        if message[i]=='1':
            nb1Hor+=1
        if len(res) == long:
            if nb1Hor%2 == 0:
                parity+='0'
            else:
                parity+='1'
            nb1Hor=0
            res=""
    if len(lpack)%long != 0:
        while len(lpack)%long != 0:
            lpack.append('0')
    ### Verticalement
    print(len(lpack))
    for i in range(long):
        for y in range(len(lpack)):
            if (y%(i+long)==0 and lpack[y]=='1'):
                print('Oui')
                nb1Ver+=1
        print("nombre de 1: "+str(nb1Ver))
        if nb1Ver%2==0:
            parity+='0'
        else:
            parity+='1'
        nb1Ver=0
    print(lpack,parity)
        
message="110100110111"
doubleParity(message)

def crc(message):
    nb1=0
    for i in range(len(message)):
        if str(bin(nb1))[0] == '1' and message[i] != '1' or str(bin(nb1))[0] != '1' and message[i] == '1':
            nb1=nb1*2
        else:
            pass
            


#cette fonction traduit un message en une trame/sequence de bits. Cette fonction est maintenant simple, mais elle est insuffisante (elle ne permet pas de trouver le debut du message par exemple) le but de ce TP est de la completer.
def couche2(message_from_sender):
    return message_from_sender.replace("o","0").replace("i","1")

#cette fonction traduit une sequence de bits en un message. Cette fonction est maintenant simple, mais elle est insuffisante (elle ne permet pas de trouver le debut du message par exemple) le but de ce TP est de la completer.
def couche2R(message_from_sender):
    return message_from_sender.replace("0","o").replace("1","i")


#cette fonction represente la tradution faite par le codage NRZ
def couche1(trame_de_bits):
    return trame_de_bits.replace("0","-").replace("1","+")

#cette fonction represente la tradution faite par le codage NRZ
def couche1R(trame_de_bits):
    return trame_de_bits.replace("-","0").replace("+","1")

def etendreCouche2(message_from_sender):
    long=bin(len(message_from_sender))[2:]
    while len(long)<8:
        long='0'+long
    message="01111110"+long+message_from_sender
    print('========================================================= ',message)
    return message

def etendreCouche2R(trame_de_bits):
    x=0
    messagedouverture='01111110'
    longO=len(messagedouverture)
    while trame_de_bits[x:x+longO]!=messagedouverture:
        x+=1
    long=int(trame_de_bits[x+longO:x+(longO+8)],2)
    message=trame_de_bits[x+(longO+8):x+(longO+8)+long]
    print('======================================================== ',message)
    return message

#cette fonction simule le canal. Le canal contient initialement du bruit: le recepteur etait a l'ecoute avant que l'emetteur n'envoie son message. 
#Il contient aussi un bruit final, car le recepteur sera aussi a l'ecoute apres l'envoi du message. 
#Le defi de la couche 2 est de permettre au recepteur de determiner ou commence et ou termine le message envoye.
def transmission(signal_from_sender):### recois - +

    #bruit initial
    for x in range (0,randint(4, 10)):
        if randint(0,1) == 1:
            signal_from_sender = "-" + signal_from_sender
        else:
            signal_from_sender = "+" + signal_from_sender

    #bruit final
    for x in range (0,randint(4, 10)):
        if randint(0,1) == 1:
            signal_from_sender = signal_from_sender + "-"
        else:
            signal_from_sender = signal_from_sender + "+"

    return signal_from_sender


def emission(message_from_sender):###recois  o i
    print("message a envoyer:"+message_from_sender)
    trame_de_bits_envoyee = couche2(message_from_sender)###transforme o i  en  0 1
    print("message a envoyer + modif:"+trame_de_bits_envoyee)
    trame_de_bits_envoyee=parityBit(trame_de_bits_envoyee)
    print("Application ParityBit :"+trame_de_bits_envoyee)
    trame_de_bits_envoyee=etendreCouche2(trame_de_bits_envoyee)###rajoute le bordel
    print("trame a envoyer:"+trame_de_bits_envoyee+" | ouverture/taille/message")
    signal_envoye = couche1(trame_de_bits_envoyee)### transforme 0 1 en - +
    print("signal envoye:"+signal_envoye)
    return signal_envoye

def reception(signal_sur_canal):
    longueurNonModifiee=len(signal_sur_canal)
    print("signal entendu, avec le bruit:"+signal_sur_canal)
    if testParityBit(signal_sur_canal):
        bits_recus = couche1R(signal_sur_canal)
        print("bits recus par le recepteur:"+bits_recus)
        message_recu=etendreCouche2R(bits_recus)
        print("bits recus par le recepteur - bruit - modif:"+message_recu)
        message_recu = couche2R(message_recu[:-1]) #On retire le bit de parité du message
        print("message recu par le recepteur:"+message_recu)
        longueurModifiee=len(message_recu)
        longDeDiff=longueurNonModifiee-longueurModifiee
        return message_recu,longDeDiff


def simulation(message_from_sender):
    signal_envoye = emission(message_from_sender)
    print("Signal avec Bit de parité: "+signal_envoye)
    signal_envoye=SignalSwapsError2(signal_envoye,30)
    signal_sur_canal = transmission(signal_envoye)
    return reception(signal_sur_canal)
print(simulation("iiiioiiiooooioiioio"))
##print("====================================================================================================")
##print("====================================================================================================")
##print(simulation("oooiii"))

def AddIdentification(message_from_sender):
    #Machine1: 0001 | Machine3: 0011
    messagewithadd="00010011"+message_from_sender
    return messagewithadd

def WhoIsSender(message):
    print(str("Le message est envoyé par ")+message[0:4])
    return message[0:4]

def IsAdressedToMe(message_from_sender):
    if message_from_sender[4:8] == '0011':
        return True
    else:
        return "Message ignoré"

##def SignalSwapError(message,n):
##    res=""
##    for i in range(len(message)):
##        if i==n:
##            if message[i]=='0':
##                res+='1'
##            else:
##                res+='0'
##        else:
##            res+=message[i]
##    return res

        
    
##print("#########################################")
##message=AddIdentification('001101010')
##Sender=WhoIsSender(message)   
##print(Sender)
##IsAdressedToMe(message)
##message2='000100100011010'
##print(WhoIsSender(message2))
##print(IsAdressedToMe(message2))
##print(SignalSwapError(message,4))


