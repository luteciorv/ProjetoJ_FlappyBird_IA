import os
import random

import pygame
from pygame import Mask, Surface

from Models.passaro import Passaro


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x: int):
        self.x: int = x
        self.altura: int = 0
        self.posicao_topo: int = 0
        self.posicao_base: int = 0
        self.SPRITE_CANO_BASE: Surface = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'pipe.png')))
        self.SPRITE_CANO_TOPO: Surface = pygame.transform.flip(self.SPRITE_CANO_BASE, False, True)
        self.passaroPassou: bool = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.posicao_topo = self.altura - self.SPRITE_CANO_TOPO.get_height()
        self.posicao_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela: Surface):
        tela.blit(self.SPRITE_CANO_TOPO, (self.x, self.posicao_topo))
        tela.blit(self.SPRITE_CANO_BASE, (self.x, self.posicao_base))

    def colidir(self, passaro: Passaro):
        passaro_mask: Mask = passaro.get_mask()
        topo_mask: Mask = pygame.mask.from_surface(self.SPRITE_CANO_TOPO)
        base_mask: Mask = pygame.mask.from_surface(self.SPRITE_CANO_BASE)

        distancia_topo: tuple[int, int] = (round(self.x - passaro.x), round(self.posicao_topo - passaro.y))
        distancia_base: tuple[int, int] = (round(self.x - passaro.x), round(self.posicao_base - passaro.y))

        topo_ponto_colisao = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto_colisao = passaro_mask.overlap(base_mask, distancia_base)

        return topo_ponto_colisao or base_ponto_colisao
