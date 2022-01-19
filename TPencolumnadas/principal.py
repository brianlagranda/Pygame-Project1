#! /usr/bin/env python
import os
import random
import sys
import math

import pygame
import pygame_menu
from pygame.locals import *

from configuracion import *
from funcionesVACIAS import *
from extras import *


pygame.init()
surface = pygame.display.set_mode((800, 600))

DIFFICULTY=[1]
NOMBRE=['player']

def set_difficulty(value, difficulty):
    DIFFICULTY[0]=difficulty

def start_the_game():
    main()

def iniciarPantalla():
    pygame.init()

    IMAGEN_FONDO = pygame.image.load("fondo.jpg").convert_alpha()
    PANTALLA = pygame.display.set_mode((ANCHO , ALTO))
    SALIR = False

    while SALIR != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SALIR = True

        defaultFont= pygame.font.Font( pygame.font.get_default_font(), TAMANNO_LETRA)
        PANTALLA.blit(IMAGEN_FONDO,(0,0))

        # MUESTRA TABLA DE RECORDS

        record=[]
        records = open("records.txt","r")
        for linea in records.readlines():
            if "\n" in linea:
                record.append(linea[0:-1])
            else:
                record.append(linea)
        records.close()

        y=150
        ren1 = defaultFont.render("Puntajes Históricos", 1, COLOR_RECORDS)
        PANTALLA.blit(ren1, (ANCHO//2-100, 100))

        k=0
        for i in range(len(record)-1,0,-1):
            k=k+1
            if k<=10:
                ren2 = defaultFont.render(record[i], 1, COLOR_RECORDS)
                PANTALLA.blit(ren2, (ANCHO//2-100, y))
                y=y+35

        pygame.display.update()

def mostrarPuntajes():
    iniciarPantalla()

def MyTextValue(nombre):
    NOMBRE[0]=nombre

menu = pygame_menu.Menu('Apalabrados', 800, 600,
                    theme=pygame_menu.themes.THEME_BLUE)
menu.add.text_input('Nombre:', default='player', onchange=MyTextValue)
menu.add.selector('Difficulty :', [('Colores', 1), ('Animales', 2), ('Paises', 3)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Puntajes Historicos', mostrarPuntajes)
menu.add.button('Quit', pygame_menu.events.EXIT)



def main():

    # ASÍ RESETEA EL PYGAME Y EL CONTADOR DEL TIEMPO ARRANCA EN EL VALOR ASIGNADO A TIEMPO_MAX
    pygame.quit()
    # Centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    # MÚSICA DEL JUEGO
    SONIDO_JUEGO = pygame.mixer.Sound("juego.mp3")
    SONIDO_TECLA = pygame.mixer.Sound("tecla1.wav")

    SONIDO_JUEGO.play()


    # Preparar la ventana
    pygame.display.set_caption("Armar palabras...")
    screen = pygame.display.set_mode((ANCHO, ALTO))

    # FONDO DEL JUEGO
    IMAGEN_FONDO = pygame.image.load("fondo.jpg").convert_alpha()

    # tiempo total del juego
    gameClock = pygame.time.Clock()
    totaltime = 0
    segundos = TIEMPO_MAX
    fps = FPS_inicial

    puntos = 0
    vel=1
    cont=1
    candidata = ""
    listaIzq = []
    listaMedio = []
    listaDer = []
    posicionesIzq = []
    posicionesMedio = []
    posicionesDer = []
    lista = []
    candidatas = []

    lemario=""

    # CAMBIA EL LEMARIO DEPENDIENDO LA SELECCIÓN DE CATEGORÍA DEL USUARIO EN EL MENÚ.

    if DIFFICULTY[0]==1:
        lemario="lemarioColores.txt"
    elif DIFFICULTY[0]==2:
        lemario="lemarioAnimales.txt"
    elif DIFFICULTY[0]==3:
        lemario="lemarioPaises.txt"

    lectura(lista, lemario)

    cargarListas(lista, listaIzq, listaMedio, listaDer, posicionesIzq, posicionesMedio, posicionesDer)

    dibujar(screen, candidata, listaIzq, listaMedio, listaDer, posicionesIzq, posicionesMedio, posicionesDer, puntos, segundos)  

    while segundos > fps/1000:
        # 1 frame cada 1/fps segundos
        gameClock.tick(fps)
        totaltime += gameClock.get_time()

        if True:
            fps = 3

        # Buscar la tecla apretada del modulo de eventos de pygame
        for e in pygame.event.get():

            # QUIT es apretar la X en la ventana
            if e.type == QUIT:
                pygame.quit()
                return()

            # Ver si fue apretada alguna tecla
            if e.type == KEYDOWN:
                letra = dameLetraApretada(e.key)
                SONIDO_TECLA.play()
                candidata += letra
                if e.key == K_BACKSPACE:
                    candidata = candidata[0:len(candidata)-1]
                if e.key == K_RETURN:
                    puntos += procesar(lista, candidata, candidatas, listaIzq, listaMedio, listaDer)
                    candidata = ""

        segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000

        # Limpiar pantalla anterior
        screen.blit(IMAGEN_FONDO,(0,0))
        # screen.fill(COLOR_FONDO)

        # Dibujar de nuevo todo
        dibujar(screen, candidata, listaIzq, listaMedio, listaDer, posicionesIzq,
                posicionesMedio, posicionesDer, puntos, segundos)

        pygame.display.flip()
    
        actualizar(lista, listaIzq, listaMedio, listaDer, posicionesIzq,
        posicionesMedio, posicionesDer, vel)

    # CADA 10 SEGUNDOS AUMENTA LA VELOCIDAD DEL JUEGO:
        if int(segundos)%10==0 and cont==1:
            vel=vel+2
        cont=cont+1
        if cont==3:
            cont=1
    
    # FIN DEL JUEGO


    # SI PUNTOS ES DISTINTO DE 0, ENTONCES GUARDA EL NOMBRE Y EL PUNTAJE FINAL EN UN ARCHIVO DE RECORDS.

    records = open("records.txt", "a")
    records.write("\n")

    if puntos!=0:
        records.write(NOMBRE[0]+": "+str(puntos)+" puntos")
        records.close()


    while 1:
        # Esperar el QUIT del usuario
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return
    
# Programa Principal ejecuta Main
if __name__ == "__main__":
    menu.mainloop(surface)