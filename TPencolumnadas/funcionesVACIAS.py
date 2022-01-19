from principal import *
import configuracion

import random
import math

# Funciones - Auxiliares :

def lectura(lista, lemario):
    # LEE EL LEMARIO Y LO CARGA EN UNA LISTA, LUEGO CIERRA EL ARCHIVO
    archivo = open(lemario,"r", encoding = "latin-1")
    for linea in archivo.readlines():
    # SI HAY UN SALTO DE LINEA AL FINAL DE LA PALABRA, LO OMITE Y AGREGA LA PALABRA A LA LISTA SIN EL ESPACIO.        
        if "\n" in linea:
            lista.append(linea[0:-1])
        else:
            lista.append(linea)
    archivo.close()
    return lista

# Funciones - Principales :



def cargarListas(lista, listaIzq, listaMedio, listaDer, posicionesIzq, posicionesMedio, posicionesDer):
    # elige una palabra al azar de la lista y la carga en las 3 listas
    # y les inventa una posicion a cada letra para que aparezca en la columna correspondiente
    palabraAlAzar = random.choice(lista)
    columnaAlAzar = 1
    for letra in palabraAlAzar: # SELECCIONA UNA LETRA Y LA ENVIA A UNA COLUMNA AL AZAR (RESPETANDO LAS REGLAS DEL JUEGO)
        y=25           
        if columnaAlAzar==1:
            columnaAlAzar = random.randint(1,2)
            x=random.randint(35,250)
            while estaCerca(x, posicionesIzq):
                x=random.randint(35,250)
            pos=[x,y]
            listaIzq.append(letra)
            posicionesIzq.append(pos)
        elif columnaAlAzar==2:
            columnaAlAzar = random.randint(2,3)
            x=random.randint(280,520)
            while estaCerca(x, posicionesMedio):
                x=random.randint(280,520)
            pos=[x,y]
            listaMedio.append(letra)
            posicionesMedio.append(pos)
        elif columnaAlAzar==3:
            x=random.randint(540,755)
            while estaCerca(x, posicionesDer):
                x=random.randint(540,755)
            pos=[x,y]
            listaDer.append(letra)
            posicionesDer.append(pos)


def bajar(lista, posiciones, vel):
    # hace bajar las letras y elimina las que tocan el piso
        i=0
        while i<len(lista):
            posiciones[i][1]=posiciones[i][1]+configuracion.velocidad+vel
            if posiciones[i][1]>=535:
                lista.pop(i)
                posiciones.pop(i)
            i+=1
            


def actualizar(lista, listaIzq, listaMedio, listaDer, posicionesIzq , posicionesMedio, posicionesDer, vel):
    # llama a otras funciones para bajar las letras, eliminar las que tocan el piso y
    # cargar nuevas letras a la pantalla (esto puede no hacerse todo el tiempo para que no se llene de letras la pantalla)
    if random.randrange(100) < 10:
        cargarListas(lista, listaIzq, listaMedio, listaDer, posicionesIzq, posicionesMedio, posicionesDer)
    bajar(listaIzq , posicionesIzq, vel)
    bajar(listaMedio , posicionesMedio, vel)
    bajar(listaDer , posicionesDer, vel)


def estaCerca(elem, lista):
    for i in range(len(lista)):
        xDeLista=lista[i][0]
        if lista[i][1]>=25 and lista[i][1]<=40 and xDeLista-10 <= elem <= xDeLista+10:
            return True
    return False


def Puntos(candidata):
    #devuelve el puntaje que le corresponde a candidata
    vocales="aeiou"
    consdif="jkqwxyz"
    puntos=0
    for letra in candidata:
        if letra != " ":
            if letra in vocales:
                puntos+=1
            elif letra in consdif:
                puntos+=5
            else:
                puntos+=2
    return puntos


def procesar(lista, candidata, candidatas, listaIzq, listaMedio, listaDerecha):
    #chequea que candidata sea correcta en cuyo caso devuelve el puntaje y 0 si no es correcta
    if esValida(lista, candidata , candidatas, listaIzq, listaMedio, listaDerecha):
        candidatas.append(candidata)
        puntos = Puntos(candidata)
        SONIDO_ACIERTO = pygame.mixer.Sound("acierto.mp3")
        SONIDO_ACIERTO.play()
        return puntos
    else:
        SONIDO_ERROR= pygame.mixer.Sound("error.mp3")
        SONIDO_ERROR.play()
        return 0

def esValida(lista, candidata, candidatas, listaIzq, listaMedio, listaDerecha):
    if candidata in lista and candidata not in candidatas:
        contizq=0
        contmed=0
        contder=0
        for letra in candidata:
            if letra in listaIzq and contmed==0 and contder==0:
                contizq=contizq+1
            elif letra in listaMedio and contder==0:
                contmed=contmed+1
            elif letra in listaDerecha:
                contder=contder+1
        cont=contder+contmed+contizq
                    
        if cont==len(candidata):
            return True
    return False