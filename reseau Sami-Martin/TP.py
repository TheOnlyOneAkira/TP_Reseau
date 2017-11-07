from random import randint

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
    message=trame_de_bits[x+(longO+8):x+(longO+8)+long+1]##le +1 a la fin permet de prendre le bit de parité
    print('======================================================== ',message)
    return message


def SignalSwapError(message,n):
    res=""
    for i in range(len(message)):
        if i==n:
            if message[i]=="-":
                res+="+"
            elif message[i]=="+":
                res+="-"
        else:
            res+=message[i]
    return res

def parityBit(m):
    n=0
    for i in range(len(m)):
        if m[i]=='1':
            n+=1
    if n%2!=0:
        n=1
    else:
        n=0
    return str(n)



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

    trame_de_bits_envoyee+=parityBit(trame_de_bits_envoyee)
    print("avec parity bit:"+trame_de_bits_envoyee)
    
    trame_de_bits_envoyee=etendreCouche2(trame_de_bits_envoyee)###rajoute le bordel
    print("trame a envoyer:"+trame_de_bits_envoyee)
    signal_envoye = couche1(trame_de_bits_envoyee)### transforme 0 1 en - +
    print("signal envoye:"+signal_envoye)
    return signal_envoye

def reception(signal_sur_canal):
    longueurNonModifiee=len(signal_sur_canal)
    print("signal entendu, avec le bruit:"+signal_sur_canal)
    bits_recus = couche1R(signal_sur_canal)
    print("bits recus par le recepteur:"+bits_recus)
    message_recu=etendreCouche2R(bits_recus)
    print("bits recus par le recepteur - bruit - modif:"+message_recu)

    if (parityBit(message_recu)!=message_recu[len(message_recu)-1]):
        print('erreur de parityBit')
        return None
    print("pas d'erreur")

    message_recu=message_recu[0:len(message_recu)-1]
        
    message_recu = couche2R(message_recu)
    print("message recu par le recepteur:"+message_recu)
    longueurModifiee=len(message_recu)
    longDeDiff=longueurNonModifiee-longueurModifiee
    return message_recu,longDeDiff




def simulation(message_from_sender):
    signal_envoye = emission(message_from_sender)
    test_e= SignalSwapError(signal_envoye,16) ## >=16
    signal_sur_canal = transmission(test_e)
    print(test_e,"qgvhskjfhlqsgfckqefvhgvghccchg")
    return reception(signal_sur_canal)
#print(simulation("oooiii"))
print(simulation("iiiioiiiooooioiioio"))

def AddIdentification(message_from_sender):
    ## Machine 1= 0001 et Machine 3= 0011
    message= "00010011"+message_from_sender
    return message
##print("L'ID du message: "+AddIdentification("00100"))

def WhoIsTheSender(message):
    return message[0:4]
##print("Le message est envoyé par: " + WhoIsTheSender("0001001100100"))

def IsAddressedToMe(message_from_sender):
    if message_from_sender[4:8]=="0011":
        return True
    else:
        return str("Message ignoré")

def doubleParityBit(m):

    taillePackage=4
    
    res=''
    longMsg=len(m)
    nbParityBit=longMsg/taillePackage
    if (nbParityBit//1 < nbParityBit):
        nbParityBit=1+(nbParityBit//1)
    for i in range(nbParityBit):
        count=0
        temp=[]
        while count<taillePackage:
            temp+=[m[4*i+count],]
            count+=1
        j=0
        while j 

##IsAddressedToMe("00010001000000000010")
##IsAddressedToMe("00010010000000000010")

