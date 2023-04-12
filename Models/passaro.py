import os
import pygame
from pygame import Surface, Mask


class Passaro:
    SPRITES = [
        pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),
        pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))),
        pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png')))
    ]

    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5
    ACELERACAO = 1.5

    def __init__(self, x: int, y: float):
        self.x: int = x
        self.y: float = y
        self.angulo: int = 0
        self.velocidade: float = 0
        self.altura: float = y
        self.tempo: int = 0
        self.tempoAnimacaoAtual: int = 0
        self.sprite: Surface = self.SPRITES[0]

    def pular(self):
        self.velocidade = -9.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento: float = self.ACELERACAO * (self.tempo ** 2) + (self.velocidade * self.tempo)

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        elif self.angulo > -80:
            self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.tempoAnimacaoAtual += 1

        if self.tempoAnimacaoAtual < self.TEMPO_ANIMACAO:
            self.sprite = self.SPRITES[0]
        elif self.tempoAnimacaoAtual < self.TEMPO_ANIMACAO * 2:
            self.sprite = self.SPRITES[1]
        elif self.tempoAnimacaoAtual < self.TEMPO_ANIMACAO * 3:
            self.sprite = self.SPRITES[2]
        elif self.tempoAnimacaoAtual < self.TEMPO_ANIMACAO * 4:
            self.sprite = self.SPRITES[1]
        elif self.tempoAnimacaoAtual < self.TEMPO_ANIMACAO * 4 + 1:
            self.tempoAnimacaoAtual = 0

        if self.angulo <= -80:
            self.sprite = self.SPRITES[1]
            self.tempoAnimacaoAtual = self.TEMPO_ANIMACAO * 2

        spriteRotacionado = pygame.transform.rotate(self.sprite, self.angulo)
        centroObjeto = self.sprite.get_rect(topleft=(self.x, self.y)).center
        objetoPassaro = spriteRotacionado.get_rect(center=centroObjeto)

        tela.blit(spriteRotacionado, objetoPassaro.topleft)

    def get_mask(self) -> Mask:
        return pygame.mask.from_surface(self.sprite)
