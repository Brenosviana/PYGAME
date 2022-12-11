import pygame as pg
import sys
import os
import math
import time
from configJogo import ConfigJogo
from selecaoPersonagem import telaSelecao
from personagens import Personagem
from cooldownCast import CooldownCast
from time import time
from blocos import bloco

class telaPrincipal():
    def __init__(self, tela, escolhidos):
        self.tela = tela
        self.encerrada = False
        self.mirado = False
        self.primeiroCastE = True
        self.primeiroCastQ = True
        self.primeiroCastM = True
        self.primeiroCastN = True
        
        self.posicaoAdquirida = False
        self.mouse_pos = ()
        
        p1 = Personagem(escolhidos[0], self.tela)
        p2 = Personagem(escolhidos[1], self.tela)
        
        self.CastE = CooldownCast()
        self.CastQ = CooldownCast()
        
        self.CastM = CooldownCast()
        self.CastN = CooldownCast()
        
        p1.stats()
        p2.stats()
        
        self.p1AtaqueE = False
        self.p1AtaqueQ = False
        
        self.p2AtaqueM = False
        self.p2AtaqueN = False
        
        
        self.p1Velocidade = p1.status[0]
        self.p2Velocidade = p2.status[0]
        self.p1VelocidadePadrao = p1.status[0]
        self.p2VelocidadePadrao = p2.status[0]
        
        self.v_Flecha = 0.8
        
        self.xP1FlechaEsquerda = 0
        self.xP1FlechaDireita = 0
        self.yP1FlechaCima = 0
        self.yP1FlechaBaixo = 0
        
        self.xP2FlechaEsquerda = 0
        self.xP2FlechaDireita = 0
        self.yP2FlechaCima = 0
        self.yP2FlechaBaixo = 0
        
        self.p1Vida = p1.status[1]
        self.p2Vida = p2.status[1]
        self.p1VidaAntes = p1.status[1]
        self.p2VidaAntes = p2.status[1]
        self.p1VidaTotal = p1.status[1]
        self.p2VidaTotal = p2.status[1]
        
        self.p1 = p1.status[2]
        self.p2 = p2.status[2]
        
        self.p1VelocidadeAtq = p1.status[3]
        self.p2VelocidadeAtq = p2.status[3]
        
        self.p1Dano = p1.status[4]
        self.p2Dano = p2.status[4]
        self.p1DanoPadrao = p1.status[4]
        self.p2DanoPadrao = p2.status[4]
        
        self.xP1 = ConfigJogo.LARGURA_TELA * (1/3)
        self.yP1 = ConfigJogo.ALTURA_TELA // 2
        self.v_xP1 = 0
        self.v_yP1 = 0
        
        self.v_missel = 0.6
        self.xP1missel = 0
        self.yP1missel = 0
        self.xP2missel = 0
        self.yP2missel = 0
        
        self.xP2 = ConfigJogo.LARGURA_TELA * (2/3)
        self.yP2 = ConfigJogo.ALTURA_TELA // 2
        self.v_xP2 = 0
        self.v_yP2 = 0
    
        self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'TRILHAREDE.png'))
        self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'CYBORG.png'))
        self.sprite3_tamanho = pg.image.load(os.path.join('sprites', 'TRON.png'))
        self.sprite4_tamanho = pg.image.load(os.path.join('sprites', 'ATIRADORA.png'))
        
        self.imagerect = self.sprite1_tamanho.get_rect()
        
        self.display_surface = pg.display.get_surface()
        self.sprites_visiveis = pg.sprite.Group()
        self.sprites_obstaculos = pg.sprite.Group()
        self.criar_mapa()

        self.raioATQGiratorio = 50
        self.raioATQProjetil = 5

    def criar_mapa(self):
        for row_index, row in enumerate(ConfigJogo.MAPA_JOGO):
            for col_index, col in enumerate(row):
                x = col_index * 32
                y = row_index * 32

                if col == 8:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 8)
                if col == 5:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 5)
                if col == 4:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 4)
                if col == 9:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 9)
                if col == 1:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 1)
                if col == 0:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 0)
          
    def rodar(self):
        while not self.encerrada:
            self.tela.fill((102, 255, 51))
            self.sprites_visiveis.draw(self.display_surface)
            self.tratamentoEventos()
            self.ataques()
            self.movimento()
            self.carregarPersonagem()

            pg.display.flip()
            
    def tratamentoEventos(self):
        events = pg.event.get()
            
        for event in events:
            #Personagem W A S D
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_a)) or (pg.key.get_pressed()[pg.K_a]):
                self.v_xP1 = -self.p1Velocidade

            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_d)) or (pg.key.get_pressed()[pg.K_d]):
                self.v_xP1 = self.p1Velocidade
                
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_w)) or (pg.key.get_pressed()[pg.K_w]):
                self.v_yP1 = -self.p1Velocidade

            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_s)) or (pg.key.get_pressed()[pg.K_s]):
                self.v_yP1 = self.p1Velocidade
                
            if ((event.type == pg.KEYUP) and (event.key == pg.K_a)) or \
                        ((event.type == pg.KEYUP) and (event.key == pg.K_d)):
                self.v_xP1 = 0
                
            if ((event.type == pg.KEYUP) and (event.key == pg.K_w)) or \
                        ((event.type == pg.KEYUP) and (event.key == pg.K_s)):
                self.v_yP1 = 0
                   
            #Ataque E
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_e)) or (pg.key.get_pressed()[pg.K_e]):
                cooldownCastE = self.CastE.diferenca()
                
                if (cooldownCastE > self.p1VelocidadeAtq) or self.primeiroCastE:
                    self.p1AtaqueE = True
                    self.CastE.resetar()
                    self.duracaoCastE = time()
                    self.primeiroCastE = False
                    
                    self.posicaoAdquirida = False
                    self.clique = False
                    
                    self.p1Vidamissel = 3
                    
                    self.xP1FlechaEsquerda = self.xP1+20
                    self.xP1FlechaDireita = self.xP1+20
                    self.yP1FlechaCima = self.yP1+25
                    self.yP1FlechaBaixo = self.yP1+25
                    
                    self.xP1Flecha = self.xP1+20
                    self.yP1Flecha = self.yP1+25
                    
                    self.xP1missel = self.xP1
                    self.yP1missel = self.yP1

            #Personagem 2 ijkl
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_j)) or (pg.key.get_pressed()[pg.K_j]):
                self.v_xP2 = -self.p2Velocidade

            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_l)) or (pg.key.get_pressed()[pg.K_l]):
                self.v_xP2 = self.p2Velocidade
                
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_i)) or (pg.key.get_pressed()[pg.K_i]):
                self.v_yP2 = -self.p2Velocidade

            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_k)) or (pg.key.get_pressed()[pg.K_k]):
                self.v_yP2 = self.p2Velocidade
                
            if ((event.type == pg.KEYUP) and (event.key == pg.K_j)) or \
                        ((event.type == pg.KEYUP) and (event.key == pg.K_l)):
                self.v_xP2 = 0
                
            if ((event.type == pg.KEYUP) and (event.key == pg.K_i)) or \
                        ((event.type == pg.KEYUP) and (event.key == pg.K_k)):
                self.v_yP2 = 0
                  
            #Ataque u
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_u)) or (pg.key.get_pressed()[pg.K_u]):
                cooldownCastM = self.CastM.diferenca()
                
                if (cooldownCastM > self.p2VelocidadeAtq) or self.primeiroCastM:
                    self.p2AtaqueM = True
                    self.CastM.resetar()
                    self.duracaoCastM = time()
                    self.primeiroCastM = False
                    self.posicaoAdquirida = False
                    self.clique = False
                    
                    self.xP2Flecha = self.xP2+20
                    self.yP2Flecha = self.yP2+25
                    
                    
                    self.xP2FlechaEsquerda = self.xP2+20
                    self.xP2FlechaDireita = self.xP2+20
                    self.yP2FlechaCima = self.yP2+25
                    self.yP2FlechaBaixo = self.yP2+25
                    
                    self.xP2missel = self.xP2
                    self.yP2missel = self.yP2
                      
            #Mouse
            if event.type == pg.MOUSEBUTTONUP:
                
                self.mouse_pos = pg.mouse.get_pos()
                self.clique = True
                self.P1primeiroCastFlecha = True
              
        #saida
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            sys.exit(0)
    
    def movimento(self):
        
        if ((self.xP1 + self.v_xP1 < 0) or (self.xP1 + self.v_xP1 > ConfigJogo.LARGURA_TELA-50)):
            self.v_xP1 = 0
        if ((self.yP1 + self.v_yP1 < 0) or (self.yP1 + self.v_yP1 > ConfigJogo.ALTURA_TELA-50)):
            self.v_yP1 = 0
            
        if ((self.xP2 + self.v_xP2 < 0) or (self.xP2 + self.v_xP2 > ConfigJogo.LARGURA_TELA-50)):
            self.v_xP2 = 0
        if ((self.yP2 + self.v_yP2 < 0) or (self.yP2 + self.v_yP2 > ConfigJogo.ALTURA_TELA-50)):
            self.v_yP2 = 0
        

        self.xP1FlechaEsquerda += -self.v_Flecha
        self.xP1FlechaDireita += self.v_Flecha
        self.yP1FlechaCima += -self.v_Flecha
        self.yP1FlechaBaixo += self.v_Flecha
        
        self.xP2FlechaEsquerda += -self.v_Flecha
        self.xP2FlechaDireita += self.v_Flecha
        self.yP2FlechaCima += -self.v_Flecha
        self.yP2FlechaBaixo += self.v_Flecha
        
        self.xP1 += self.v_xP1
        self.yP1 += self.v_yP1
            
        self.xP2 += self.v_xP2
        self.yP2 += self.v_yP2
    
    def carregarPersonagem(self):
        if self.p1 == 1:
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'TRILHAREDE.png'))
            
        elif self.p1 == 2:
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'TRON.png'))
            
        elif self.p1 == 3:
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'CYBORG.png'))
            
        elif self.p1 == 4:
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'ATIRADORA.png'))
            
            
            
        if self.p2 == 1:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'TRILHAREDE.png'))
            
        elif self.p2 == 2:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'TRON.png'))
            
        elif self.p2 == 3:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'CYBORG.png'))
            
        elif self.p2 == 4:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'ATIRADORA.png'))
            
        self.personagem() 
            
    
    def personagem (self):
        
        self.missel = pg.image.load(os.path.join('sprites', '5.png'))
        font_vida = pg.font.SysFont(None, ConfigJogo.FONTE_VIDA)
        self.textoVida1 = font_vida.render(
            f'{int(self.p1Vida)}/{self.p1VidaTotal}', True, ConfigJogo.COR_VIDA)
        
        self.textoVida2 = font_vida.render(
            f'{int(self.p2Vida)}/{self.p2VidaTotal}', True, ConfigJogo.COR_VIDA)
        
        self.tela.blit(self.textoVida1, (self.xP1, self.yP1-20))
        self.tela.blit(self.textoVida2, (self.xP2, self.yP2-20))
        
        self.tela.blit(self.sprite1_tamanho, (self.xP1, self.yP1))
        self.tela.blit(self.sprite2_tamanho, (self.xP2, self.yP2)) 
        
    def ataques(self):
        self.xP1CirculoCentralizado = self.xP1+30
        self.yP1CirculoCentralizado = self.yP1+25
        
        self.xP2CirculoCentralizado = self.xP2+30
        self.yP2CirculoCentralizado = self.yP2+25
        
        #Ataque Melee E
        if self.p1 == 1 and self.p1AtaqueE:
            if time() - self.duracaoCastE < 0.1:
                pg.draw.circle(self.tela, (0,0,0), (self.xP1CirculoCentralizado, self.yP1CirculoCentralizado), self.raioATQGiratorio, 5)
                #Se o p2 está localizado na área de p1:
                if ((int(self.xP2) in range (int(self.xP1CirculoCentralizado-self.raioATQGiratorio), int(self.xP1CirculoCentralizado+self.raioATQGiratorio)) or \
                    int (self.xP2+40) in range (int(self.xP1CirculoCentralizado-self.raioATQGiratorio), int(self.xP1CirculoCentralizado+self.raioATQGiratorio))) and \
                        (int(self.yP2) in range (int(self.yP1CirculoCentralizado-self.raioATQGiratorio), int(self.yP1CirculoCentralizado+self.raioATQGiratorio)) or \
                            int(self.yP2+55) in range (int(self.yP1CirculoCentralizado-self.raioATQGiratorio), int(self.yP1CirculoCentralizado+self.raioATQGiratorio)))) and \
                                self.p2Vida - self.p2VidaAntes == 0:
                                    self.p2Vida = self.p2Vida-self.p1Dano
            else:
                self.p2VidaAntes = self.p2Vida
                
        #SUPER LAZER E + Mouse
        if self.p1 == 2 and self.p1AtaqueE:
            if time() - self.duracaoCastE < 2:
                if self.clique:
                    self.posicaoAdquirida = True
                
                if self.posicaoAdquirida: 
                    pg.draw.circle(self.tela, (255,0,0), (self.mouse_pos[0], self.mouse_pos[1]), self.raioATQGiratorio, 5)  
                 
                    #Se o p2 está localizado na area do lazer:
                    if ((int(self.xP2) in range (int(self.mouse_pos[0]-self.raioATQGiratorio), int(self.mouse_pos[0]+self.raioATQGiratorio)) or \
                        int (self.xP2+40) in range (int(self.mouse_pos[0]-self.raioATQGiratorio), int(self.mouse_pos[0]+self.raioATQGiratorio))) and \
                            (int(self.yP2) in range (int(self.mouse_pos[1]-self.raioATQGiratorio), int(self.mouse_pos[1]+self.raioATQGiratorio)) or \
                                int(self.yP2+55) in range (int(self.mouse_pos[1]-self.raioATQGiratorio), int(self.mouse_pos[1]+self.raioATQGiratorio)))) and \
                                    self.p2Vida - self.p2VidaAntes == 0:
                                        self.p2Vida = self.p2Vida-self.p1Dano
            else:
                self.p2VidaAntes = self.p2Vida
                
        #Lancar Missel E
        if self.p1 == 3 and self.p1AtaqueE:
            if time() - self.duracaoCastE < 3:
                self.tela.blit(self.missel, (self.xP1missel, self.yP1missel))
                
                distP2 = math.sqrt(
                    (self.xP2 - self.xP1missel) ** 2 +
                    (self.yP2 - self.yP1missel) ** 2
                )

                if distP2 > 1:
                    
                    #1 primeiro calcula a direcao
                    self.P1v_x = self.xP2 - self.xP1missel
                    self.P1v_y = self.yP2 - self.yP1missel
                    #2 faz o tamanho do vetor igual a 1 (normalizacao)
                    normaP1 = math.sqrt(self.P1v_x ** 2 + self.P1v_y ** 2)
                    self.P1v_x /= normaP1
                    self.P1v_y /= normaP1
                    #3 ajusta o tamanho para ser igual à constante self.v_missel
                    self.P1v_x *= self.v_missel
                    self.P1v_y *= self.v_missel
                else:
                    if self.p2VidaAntes == self.p2Vida:
                        self.p2Vida = self.p2Vida-self.p1Dano
                    self.P1v_x = 0
                    self.P1v_y = 0

                # Atualiza a posicao do missel de acordo com a velocidade
                self.xP1missel += self.P1v_x
                self.yP1missel += self.P1v_y
                
            else:
                self.p2VidaAntes = self.p2Vida
                
        #Projetil E - lanca o projetil nas 4 direções
        if self.p1 == 4 and self.p1AtaqueE:
            if time() - self.duracaoCastE < 1:
                
                pg.draw.circle(self.tela, (0,0,0), (self.xP1FlechaEsquerda, self.yP1Flecha), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP1FlechaDireita, self.yP1Flecha), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP1Flecha, self.yP1FlechaCima), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP1Flecha, self.yP1FlechaBaixo), self.raioATQProjetil, 5)
                
                
                #projetil da esquerda 
                if (((int(self.xP1FlechaEsquerda - self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) or \
                    int(self.xP1FlechaEsquerda + self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) and \
                        ((int(self.yP1Flecha - self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55))) or \
                            int(self.yP1Flecha + self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55)))) and \
                                self.p2Vida - self.p2VidaAntes == 0:
                                    self.p2Vida = self.p2Vida-self.p1Dano
                   
                #projetil da direita                 
                if (((int(self.xP1FlechaDireita - self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) or \
                    int(self.xP1FlechaDireita + self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) and \
                        ((int(self.yP1Flecha - self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55))) or \
                            int(self.yP1Flecha + self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55)))) and \
                                self.p2Vida - self.p2VidaAntes == 0:
                                    self.p2Vida = self.p2Vida-self.p1Dano
                                    
                #projetil de cima                
                if (((int(self.xP1Flecha - self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) or \
                    int(self.xP1Flecha + self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) and \
                        ((int(self.yP1FlechaCima - self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55))) or \
                            int(self.yP1FlechaCima + self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55)))) and \
                                self.p2Vida - self.p2VidaAntes == 0:
                                    self.p2Vida = self.p2Vida-self.p1Dano
                                    
                #projetil de baixo               
                if (((int(self.xP1Flecha - self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) or \
                    int(self.xP1Flecha + self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) and \
                        ((int(self.yP1FlechaBaixo - self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55))) or \
                            int(self.yP1FlechaBaixo + self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55)))) and \
                                self.p2Vida - self.p2VidaAntes == 0:
                                    self.p2Vida = self.p2Vida-self.p1Dano

            else:
                self.p2VidaAntes = self.p2Vida  
                
          
        #Ataque Melee (M)        
        if self.p2 == 1 and self.p2AtaqueM:
            if time() - self.duracaoCastM < 0.1:
                pg.draw.circle(self.tela, (0,0,0), (self.xP2CirculoCentralizado, self.yP2CirculoCentralizado), self.raioATQGiratorio, 5)
                #Se o p1 está localizado na área de p2:
                if ((int(self.xP1) in range (int(self.xP2CirculoCentralizado-self.raioATQGiratorio), int(self.xP2CirculoCentralizado+self.raioATQGiratorio)) or \
                    int (self.xP1+40) in range (int(self.xP2CirculoCentralizado-self.raioATQGiratorio), int(self.xP2CirculoCentralizado+self.raioATQGiratorio))) and \
                        (int(self.yP1) in range (int(self.yP2CirculoCentralizado-self.raioATQGiratorio), int(self.yP2CirculoCentralizado+self.raioATQGiratorio)) or \
                            int(self.yP1+55) in range (int(self.yP2CirculoCentralizado-self.raioATQGiratorio), int(self.yP2CirculoCentralizado+self.raioATQGiratorio)))) and \
                                self.p1Vida - self.p1VidaAntes == 0:
                                    self.p1Vida = self.p1Vida-self.p2Dano
        
            else:
                self.p1VidaAntes = self.p1Vida
        
        #SUPER LAZER M + Mouse        
        if self.p2 == 2 and self.p2AtaqueM:
            
            if time() - self.duracaoCastM < 2:
                if self.clique:
                    self.posicaoAdquirida = True
                
                if self.posicaoAdquirida: 
                    pg.draw.circle(self.tela, (255,0,0), (self.mouse_pos[0], self.mouse_pos[1]), self.raioATQGiratorio, 5)  
                    
                    #Se o p1 está localizado na área do lazer:
                    if ((int(self.xP1) in range (int(self.mouse_pos[0]-self.raioATQGiratorio), int(self.mouse_pos[0]+self.raioATQGiratorio)) or \
                        int (self.xP1+40) in range (int(self.mouse_pos[0]-self.raioATQGiratorio), int(self.mouse_pos[0]+self.raioATQGiratorio))) and \
                            (int(self.yP1) in range (int(self.mouse_pos[1]-self.raioATQGiratorio), int(self.mouse_pos[1]+self.raioATQGiratorio)) or \
                                int(self.yP1+55) in range (int(self.mouse_pos[1]-self.raioATQGiratorio), int(self.mouse_pos[1]+self.raioATQGiratorio)))) and \
                                    self.p1Vida - self.p1VidaAntes == 0:
                                        self.p1Vida = self.p1Vida-self.p2Dano
            else:
                self.p1VidaAntes = self.p1Vida
                 
        #Invocar Missel M
        if self.p1 == 3 and self.p2AtaqueM:
            if time() - self.duracaoCastM < 3:
                self.tela.blit(self.missel, (self.xP2missel, self.yP2missel))
                
                distP1 = math.sqrt(
                    (self.xP1 - self.xP2missel) ** 2 +
                    (self.yP1 - self.yP2missel) ** 2
                )

                if distP1 > 1:
                    
                    #1 primeiro calcula a direcao
                    self.P2v_x = self.xP1 - self.xP2missel
                    self.P2v_y = self.yP1 - self.yP2missel
                    #2 faz o tamanho do vetor igual a 1 (normalizacao)
                    normaP2 = math.sqrt(self.P2v_x ** 2 + self.P2v_y ** 2)
                    self.P2v_x /= normaP2
                    self.P2v_y /= normaP2
                    #3 ajusta o tamanho para ser igual à constante self.v_missel
                    self.P2v_x *= self.v_missel
                    self.P2v_y *= self.v_missel
                else:
                    if self.p1VidaAntes == self.p1Vida:
                        self.p1Vida = self.p1Vida-self.p2Dano
                    self.P2v_x = 0
                    self.P2v_y = 0

                # Atualiza a posicao do missel de acordo com a velocidade
                self.xP2missel += self.P2v_x
                self.yP2missel += self.P2v_y
                
            else:
                self.p1VidaAntes = self.p1Vida
                
        #Projetil M - Projetil nas 4 direções
        if self.p2 == 4 and self.p2AtaqueM:
            if time() - self.duracaoCastM < 1:
                
                pg.draw.circle(self.tela, (0,0,0), (self.xP2FlechaEsquerda, self.yP2Flecha), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP2FlechaDireita, self.yP2Flecha), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP2Flecha, self.yP2FlechaCima), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP2Flecha, self.yP2FlechaBaixo), self.raioATQProjetil, 5)
                
                #projetil da esquerda
                if (((int(self.xP2FlechaEsquerda - self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) or \
                    int(self.xP2FlechaEsquerda + self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) and \
                        ((int(self.yP2Flecha - self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55))) or \
                            int(self.yP2Flecha + self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55)))) and \
                                self.p1Vida - self.p1VidaAntes == 0:
                                    self.p1Vida = self.p1Vida-self.p2Dano
                   
                #projetil da direita                 
                if (((int(self.xP2FlechaDireita - self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) or \
                    int(self.xP2FlechaDireita + self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) and \
                        ((int(self.yP2Flecha - self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55))) or \
                            int(self.yP2Flecha + self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55)))) and \
                                self.p1Vida - self.p1VidaAntes == 0:
                                    self.p1Vida = self.p1Vida-self.p2Dano
                                    
                #projetil de cima                
                if (((int(self.xP2Flecha - self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) or \
                    int(self.xP2Flecha + self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) and \
                        ((int(self.yP2FlechaCima - self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55))) or \
                            int(self.yP2FlechaCima + self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55)))) and \
                                self.p1Vida - self.p1VidaAntes == 0:
                                    self.p1Vida = self.p1Vida-self.p2Dano
                                    
                #projetil de baixo               
                if (((int(self.xP2Flecha - self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) or \
                    int(self.xP2Flecha + self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) and \
                        ((int(self.yP2FlechaBaixo - self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55))) or \
                            int(self.yP2FlechaBaixo + self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55)))) and \
                                self.p1Vida - self.p1VidaAntes == 0:
                                    self.p1Vida = self.p1Vida-self.p2Dano

            else:
                self.p1VidaAntes = self.p1Vida
            