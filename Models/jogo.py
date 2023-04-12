import os

import pygame
from pygame import Surface
from pygame.font import Font
from pygame.time import Clock

from Models.passaro import Passaro
from Models.chao import Chao
from Models.cano import Cano


class Jogo:
    SPRITE_FUNDO: Surface = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))
    TELA_LARGURA: int = 500
    TELA_ALTURA: int = 800

    def __init__(self):
        pygame.font.init()
        self.FONTE_PONTOS: Font = pygame.font.SysFont('comic sans', 50)
        self.jogo_rodando: bool = False

        self.tela: Surface = pygame.display.set_mode((self.TELA_LARGURA, self.TELA_ALTURA))
        self.pontuacao: int = 0
        self.atualizacao_por_segundo: Clock = pygame.time.Clock()

        self.passaros: list[Passaro] = [Passaro(200, 350)]
        self.chao: Chao = Chao(730)
        self.canos: list[Cano] = [Cano(700)]

        self.canos_a_serem_removidos: [Cano] = []

    def iniciar_jogo(self):
        self.jogo_rodando = True
        while self.jogo_rodando:
            self.atualizacao_por_segundo.tick(30)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.encerrar_jogo()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.encerrar_jogo()

                    if evento.key == pygame.K_SPACE:
                        self.pular()

            self.chao.mover()

            self.mover_passaros()

            adicionar_cano: bool = False
            self.canos_a_serem_removidos = []

            for cano_atual in self.canos:
                for i, passaro_atual in enumerate(self.passaros):
                    if cano_atual.colidir(passaro_atual):
                        self.passaros.pop(i)

                    if not cano_atual.passaroPassou and passaro_atual.x > cano_atual.x:
                        cano_atual.passaroPassou = True
                        adicionar_cano = True

                cano_atual.mover()

                if cano_atual.x + cano_atual.SPRITE_CANO_TOPO.get_width() < 0:
                    self.canos_a_serem_removidos.append(cano_atual)

            if adicionar_cano:
                self.adicionar_cano()

            self.remover_canos()

            self.remover_passaros()

            self.desenhar_tela()

    def desenhar_tela(self):
        self.tela.blit(self.SPRITE_FUNDO, (0, 0))

        self.chao.desenhar(self.tela)

        for passaro in self.passaros:
            passaro.desenhar(self.tela)

        for cano in self.canos:
            cano.desenhar(self.tela)

        texto = self.FONTE_PONTOS.render(f"Pontuação: {self.pontuacao}", True, (255, 255, 255))
        self.tela.blit(texto, (self.TELA_LARGURA - 10 - texto.get_width(), 10))

        pygame.display.update()

    def encerrar_jogo(self):
        self.jogo_rodando = False
        pygame.quit()
        quit()

    def pular(self):
        for passaro_atual in self.passaros:
            passaro_atual.pular()

    def mover_passaros(self):
        for passaro in self.passaros:
            passaro.mover()

    def adicionar_cano(self):
        self.pontuacao += 1
        self.canos.append(Cano(600))

    def remover_canos(self):
        for cano in self.canos_a_serem_removidos:
            self.canos.remove(cano)

    def remover_passaros(self):
        for i, passaro in enumerate(self.passaros):
            if passaro.y + passaro.sprite.get_height() > self.chao.y or passaro.y < 0:
                self.passaros.pop(i)
