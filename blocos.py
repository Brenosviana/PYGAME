import pygame as pg
import os
from configJogo import *

class bloco(pg.sprite.Sprite):
    
    def __init__(self, pos, grupos, tipo_png):
        super().__init__(grupos)
        
        self.tipo_png = tipo_png
        
        if self.tipo_png == 5:
            self.image = pg.image.load(os.path.join('sprites', 'asfalto.png')).convert_alpha()
            self.rect = self.image.get_rect(topleft = pos)

        