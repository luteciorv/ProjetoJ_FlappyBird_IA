import os

import pygame
from pygame import Surface


class Chao:
    VELOCIDADE: int = 5
    SPRITE_CHAO: Surface = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'base.png')))
    LARGURA: int = SPRITE_CHAO.get_width()

    def __init__(self, y):
        self.y: int = y
        self.x_primeiro_chao: int = 0
        self.x_segundo_chao: int = self.LARGURA

    def mover(self):
        self.x_primeiro_chao -= self.VELOCIDADE
        self.x_segundo_chao -= self.VELOCIDADE

        if self.x_primeiro_chao + self.LARGURA < 0:
            self.x_primeiro_chao = self.x_segundo_chao + self.LARGURA

        if self.x_segundo_chao + self.LARGURA < 0:
            self.x_segundo_chao = self.x_primeiro_chao + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.SPRITE_CHAO, (self.x_primeiro_chao, self.y))
        tela.blit(self.SPRITE_CHAO, (self.x_segundo_chao, self.y))
