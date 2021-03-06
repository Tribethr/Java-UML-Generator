import easygui as gui
import win32con as wc
import win32api as wa
import time
import pyperclip as p

encapsuladores = ["private","public","protected"]
simbolos = ["-","+","#"]
lector = ""

def encontrarClase(archivo):
    global lector
    while(True):
        lector = archivo.readline()
        if("class" in lector):
            if("{" in lector):
                if("extends" in lector):
                    return lector[lector.find("class")+5:lector.find("extends")].replace(" ", "")
                elif 'implements' in lector:
                    return lector[lector.find("class")+5:lector.find("implements")].replace(" ", "")
                else:
                    return lector[lector.find("class")+5:lector.find("{")].replace(" ", "")

def encontrarAtributos(archivo):
    global lector
    atributos = []
    while(True):
        lector = archivo.readline()
        if("(" in lector and "{" in lector):
            break
        if("=" in lector ):
            atributos.append(analizarAtributos(lector[:lector.find("=")]))
        elif(";" in lector):
            atributos.append(analizarAtributos(lector[:lector.find(";")]))
    return atributos

def analizarAtributos(atributo):
    global lector
    retorno = ""
    atributo = atributo.split()
    for i in range(len(simbolos)):
        if(encapsuladores[i] in atributo):
            retorno += simbolos[i]
            atributo.remove(encapsuladores[i])
            break
    retorno += "~" if retorno == "" else ""
    for i in range(2):
        retorno += atributo[-1:][0]
        retorno += ": " if i == 0 else ""
        atributo.remove(atributo[-1:][0])
    while(len(atributo)>0):
        retorno = retorno[:1]+atributo[0]+retorno[1:]
        atributo.remove(atributo[0])
    return retorno

def encontrarConstructores(archivo,clase):
    global lector
    constructores = []
    while(True):
        if(clase in lector and lector[lector.find(clase) - 1] == ' '):
            constructores.append(analizarConstructores((lector.replace("{","")).split()))
        elif(not(clase in lector) and "(" in lector and "{" in lector):
            break
        lector = archivo.readline()
    return constructores

def analizarConstructores(constructor):
    global lector
    retorno = simbolos[encapsuladores.index(constructor[0])] if constructor[0] in encapsuladores else "~"
    if(len(constructor)>2):
        for i in range(1, len(constructor)-1, 2):
            if('('in constructor[i]):
                retorno += constructor[i][:constructor[i].find('(') + 1]
                if ')' in constructor[i + 1]:
                    retorno += constructor[i + 1][:constructor[i + 1].find(')')]
                    retorno += ': ' + constructor[i][constructor[i].find('(') + 1:] + ')'
                else:
                    retorno += constructor[i + 1][:len(constructor[i + 1]) - 1]
                    retorno += ": " + constructor[i][constructor[i].find('(') + 1:] + ', '
            else:
                if ')' in constructor[i + 1]:
                    retorno += constructor[i + 1][:constructor[i + 1].find(')')]
                    retorno += ': ' + constructor[i] + ')'
                else:
                    retorno += constructor[i + 1][:len(constructor[i + 1]) - 1]
                    retorno += ': ' + constructor[i] + ', '
        return retorno
    return retorno + constructor[1]
    

def encontrarMetodos(archivo):
    global lector
    metodos = []
    while(lector != ""):
        if("(" in lector and "{" in lector and not("if" in lector or "while" in lector or "for" in lector  or ";" in lector or "try" in lector or "catch" in lector)):
            metodos.append(analizarMetodos((lector.replace("{","")).split()))
        lector = archivo.readline()
    return metodos

def analizarMetodos(metodo):
    retorno = simbolos[encapsuladores.index(metodo[0])] if metodo[0] in encapsuladores else "~"
    for i in range(2, len(metodo), 1):
        if '()' in metodo[2]:
            retorno += metodo[i]
            break
        else:
            if '(' in metodo [i]:
                retorno += metodo[i][:metodo[i].find('(') + 1]
                if ',' in metodo[i + 1]:
                    retorno += metodo[i + 1][:-1] + ': '
                    retorno += metodo[i][metodo[i].find('(') + 1:] + ', '
                elif ')' in metodo[i + 1]:
                    retorno += metodo[i + 1][:-1] + ': '
                    retorno += metodo[i][metodo[i].find('(') + 1:] + ')'
            else:
                if ',' in metodo[i + 1]:
                    retorno += metodo[i + 1][:-1] + ': '
                    retorno += metodo[i] + ', '
                elif ')' in metodo[i + 1]:
                    retorno += metodo[i + 1][:-1] + ': '
                    retorno += metodo[i] + ')'
            if i + 2 >= len(metodo):
                break
            else:
                i += 2
    if (metodo[1] != "void"):
        return retorno+": "+metodo[1]
    return retorno
    
    
def analizarJava():
    global lector
    archivo = open(gui.fileopenbox(title = "Seleccione el archivo java"))
    clase = encontrarClase(archivo)
    atributos = encontrarAtributos(archivo)
    constructores = encontrarConstructores(archivo,clase)
    metodos = encontrarMetodos(archivo)
    return [clase, atributos, constructores, metodos]




def flechaArriba():
    wa.keybd_event(0x26,0 ,0 ,0)
    wa.keybd_event(0x26,0 ,wc.KEYEVENTF_KEYUP ,0)
    
def cambiarVentana():
    wa.keybd_event(0x12,0 ,0 ,0)
    wa.keybd_event(0x09,0 ,0 ,0)
    wa.keybd_event(0x09,0 ,wc.KEYEVENTF_KEYUP ,0)
    wa.keybd_event(0x12,0 ,wc.KEYEVENTF_KEYUP ,0)

def flechaAbajo():
    wa.keybd_event(0x28,0 ,0 ,0)
    wa.keybd_event(0x28,0 ,wc.KEYEVENTF_KEYUP ,0)

def pegar():
    wa.keybd_event(0x11,0 ,0 ,0)
    wa.keybd_event(0x56,0 ,0 ,0)
    wa.keybd_event(0x11,0 ,wc.KEYEVENTF_KEYUP ,0)
    wa.keybd_event(0x56,0 ,wc.KEYEVENTF_KEYUP ,0)

def enter():
    wa.keybd_event(0x11,0 ,0 ,0)
    wa.keybd_event(0x0D,0 ,0 ,0)
    wa.keybd_event(0x11,0 ,wc.KEYEVENTF_KEYUP ,0)
    wa.keybd_event(0x0D,0 ,wc.KEYEVENTF_KEYUP ,0)

a = analizarJava()
input("Presione enter para comenzar")
time.sleep(0.5)
cambiarVentana()
p.copy(a[0])
time.sleep(0.5)
pegar()
time.sleep(0.5)
cambiarVentana()
time.sleep(0.5)
cambiarVentana()
time.sleep(0.5)
flechaAbajo()
time.sleep(0.5)
cont = 0
for i in a[1]:
    cambiarVentana()
    time.sleep(0.5)
    cambiarVentana()
    time.sleep(0.5)
    if(cont != 0):
        enter()
    p.copy(i)
    time.sleep(0.5)
    pegar()
    print(i)
    cont += 1
time.sleep(0.5)
cambiarVentana()
time.sleep(0.5)
cambiarVentana()
time.sleep(0.5)
flechaAbajo()
time.sleep(0.5)
cont = 0
for i in a[2]:
    cambiarVentana()
    time.sleep(0.5)
    cambiarVentana()
    time.sleep(0.5)
    if(cont != 0):
        enter()
    p.copy(i)
    time.sleep(0.5)
    pegar()
    print(i)
for i in a[3]:
    cambiarVentana()
    time.sleep(0.5)
    cambiarVentana()
    time.sleep(0.5)
    enter()
    p.copy(i)
    time.sleep(0.5)
    pegar()
    print(i)
input("Presione enter para terminar")

