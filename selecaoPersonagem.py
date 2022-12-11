import sys
import pygame as pg
import os
from configJogo import ConfigJogo

class telaSelecao:
    def __init__(self, tela):
        self.tela = tela
        self.encerrada = False
        

        self.largura_retangulo = 0.5*ConfigJogo.LARGURA_TELA
        self.altura_retangulo = 0.6*ConfigJogo.ALTURA_TELA
        
        self.posicaoX_retangulo = (ConfigJogo.LARGURA_TELA * 0.25) 
        self.posicaoY_retangulo = (ConfigJogo.ALTURA_TELA * 0.25)
        self.cor_retangulo = (121, 126, 133)

        self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'TRILHAREDE.png'))
        self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'TRON.png'))
        self.sprite3_tamanho = pg.image.load(os.path.join('sprites', 'CYBORG.png'))
        self.sprite4_tamanho = pg.image.load(os.path.join('sprites', 'ATIRADORA.png'))
        
        self.imagerect = self.sprite1_tamanho.get_rect()
        
        self.sprite1_posicao = (self.posicaoX_retangulo+10, self.posicaoY_retangulo+10)
        self.sprite2_posicao = (self.posicaoX_retangulo+10, self.posicaoY_retangulo+100)
        self.sprite3_posicao = (self.posicaoX_retangulo+10, self.posicaoY_retangulo+190)
        self.sprite4_posicao = (self.posicaoX_retangulo+10, self.posicaoY_retangulo+280)

        self.persoSelecionado = 1
        self.persoConfirmado = False
        self.personagem1 = 0
        self.personagem2 = 0
 
        
    def rodar(self):
        while not self.encerrada:
            self.tratamento_eventos()
            self.desenha()
        if self.encerrada:
            return (self.personagem1, self.personagem2)
            
    
    def tratamento_eventos(self):
        events = pg.event.get()

        # evento de saida
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            sys.exit(0)
        
        
# Selecionar Personagens com a SETINHA e ESPACO para confirmar

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    if self.persoSelecionado == 4:
                        self.persoSelecionado = 1
                        
                    else:
                        self.persoSelecionado += 1

                if event.key == pg.K_UP:
                    if self.persoSelecionado == 1:
                        self.persoSelecionado = 4

                    else:
                        self.persoSelecionado -= 1
                
                if event.key == pg.K_SPACE:
                    
                    if self.personagem1 == 0:
                        self.personagem1 = self.persoSelecionado
                    
                    elif self.personagem2 == 0:
                        self.personagem2 = self.persoSelecionado
                        self.persoConfirmado = True


    
    def desenha(self):
        self.tela.fill((255, 255, 255))
        self.desenha_titulo(self.tela)
        self.desenha_opcao()
        self.selecionar_personagem(self.tela)
        
        pg.display.flip()
        
        if self.persoConfirmado:
            self.encerrada = True

    def desenha_titulo(self, tela):
        font_titulo = pg.font.SysFont(None, ConfigJogo.FONTE_TITULO)

        if self.personagem1 == 0:
            self.titulo = font_titulo.render(
                f'Selecione o PRIMEIRO personagem', True, ConfigJogo.COR_TITULO)
        elif self.personagem2 == 0:
            self.titulo = font_titulo.render(
                f'Selecione o SEGUNDO personagem', True, ConfigJogo.COR_TITULO)

            
        px = ConfigJogo.LARGURA_TELA // 2 - self.titulo.get_size()[0] // 2
        py = (0.1 * ConfigJogo.ALTURA_TELA // 2)
        tela.blit(self.titulo, (px, py))


    def selecionar_personagem(self,tela):
        
        tela.blit(self.sprite1_tamanho, self.sprite1_posicao)
        tela.blit(self.sprite2_tamanho, self.sprite2_posicao)
        tela.blit(self.sprite3_tamanho, self.sprite3_posicao)
        tela.blit(self.sprite4_tamanho, self.sprite4_posicao)

        if self.persoSelecionado == 1:

            pg.draw.rect(
                self.tela, 
                (0,0,0),
                pg.Rect(self.posicaoX_retangulo, self.posicaoY_retangulo, self.largura_retangulo, 90),
                5
            )

        elif self.persoSelecionado == 2:

            pg.draw.rect(
                self.tela, 
                (0,0,0),
                pg.Rect(self.posicaoX_retangulo, self.posicaoY_retangulo+90, self.largura_retangulo, 90),
                5
            )     

        elif self.persoSelecionado == 3:
            
            pg.draw.rect(
                self.tela, 
                (0,0,0),
                pg.Rect(self.posicaoX_retangulo, self.posicaoY_retangulo+180, self.largura_retangulo, 90),
                5
            )

        elif self.persoSelecionado == 4:

            pg.draw.rect(
                self.tela, 
                (0,0,0),
                pg.Rect(self.posicaoX_retangulo, self.posicaoY_retangulo+270, self.largura_retangulo, 90),
                5
            )


    def desenha_opcao(self):
        pg.draw.rect(
            self.tela, 
            self.cor_retangulo,
            pg.Rect(self.posicaoX_retangulo, self.posicaoY_retangulo, self.largura_retangulo, self.altura_retangulo)
        )

   