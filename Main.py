import pygame
import os
import random

TELA_LARGURA = 600
TELA_ALTURA = 800

IMG_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))
IMG_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'base.png')))
IMG_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))
IMGS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png')))
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('comic sans', 50)