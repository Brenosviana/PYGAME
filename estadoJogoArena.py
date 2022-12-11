from pygame import Surface
import pygame as pg

from configJogo import ConfigJogo
from cronometroArena import Cronometro 

from telaPrincipal import telaPrincipal

class EstadoJogo:
    def __init__(self):
        self.cronometro = Cronometro()
        self.resetar()

    def resetar(self):
        self.cronometro.reset()

    def fim_de_jogo(self):
        if (telaPrincipal.p1Vida <= 0) or (telaPrincipal.p2Vida <= 0):
            quit
        