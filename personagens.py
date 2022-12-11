import pygame as pg

class Personagem:
    def __init__(self, escolhido, tela) :
        self.personagem = escolhido
        self.tela = tela
    
    #área para acertar o boneco
    def stats(self):
        
        #TRILHA_REDE MELEE
        if self.personagem == 1:
            
            VELOCIDADE = 0.8
            VIDA = 55
            VELOCIDADE_ATQ = 6
            DANO = 4
            self.status = (VELOCIDADE, VIDA, 1, VELOCIDADE_ATQ, DANO)
          
        #CYBORG DANO EM AREA COM MOUSE
        elif self.personagem == 2:
            
            VELOCIDADE = 1.0
            VIDA = 15
            VELOCIDADE_ATQ = 2
            DANO = 8
            self.status = (VELOCIDADE, VIDA, 2, VELOCIDADE_ATQ, DANO)
          
        #TRON MISSEL
        elif self.personagem == 3:
            
            VELOCIDADE = 1.5
            VIDA = 35
            VELOCIDADE_ATQ = 4
            DANO = 5
            self.status = (VELOCIDADE, VIDA, 3, VELOCIDADE_ATQ, DANO)
          
        #ATIRADOR 
        elif self.personagem == 4:
            
            VELOCIDADE = 1.0
            VIDA = 30
            VELOCIDADE_ATQ = 1.4
            DANO = 4
            self.status = (VELOCIDADE, VIDA, 4, VELOCIDADE_ATQ, DANO)
    