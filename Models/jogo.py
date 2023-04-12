import os

import pygame
from neat.nn import FeedForwardNetwork
from pygame import Surface
from pygame.font import Font
from pygame.time import Clock

import neat

from Models.passaro import Passaro
from Models.chao import Chao
from Models.cano import Cano


class Jogo:
    SPRITE_FUNDO: Surface = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'bg.png')))
    TELA_LARGURA: int = 500
    TELA_ALTURA: int = 800
    FPS: int = 30

    def __init__(self):
        pygame.font.init()
        self.FONTE_PONTOS: Font = pygame.font.SysFont('comic sans', 30)
        self.jogo_rodando: bool = False

        self.ia_jogando: bool = True
        if self.ia_jogando:
            self.geracao: int = -1
            self.redes_neurais: [FeedForwardNetwork] = []
            self.genomas = []
            self.indice_cano: int = 0

        self.tela: Surface = pygame.display.set_mode((self.TELA_LARGURA, self.TELA_ALTURA))
        self.pontuacao: int = 0
        self.atualizacao_por_segundo: Clock = pygame.time.Clock()

        self.passaros: list[Passaro] = [Passaro(200, 350)]
        self.chao: Chao = Chao(730)
        self.canos: list[Cano] = [Cano(700)]

        self.canos_a_serem_removidos: [Cano] = []

        self.iniciar_variaveis()

    def iniciar_jogo(self, novos_genomas, config):
        self.jogo_rodando = True

        if self.ia_jogando:
            self.iniciar_variaveis()

            self.geracao += 1
            self.redes_neurais: [FeedForwardNetwork] = []
            self.genomas = []
            self.passaros: [Passaro] = []

            for _, genoma in novos_genomas:
                rede_neural: FeedForwardNetwork = neat.nn.FeedForwardNetwork.create(genoma, config)
                self.redes_neurais.append(rede_neural)
                genoma.fitness = 0
                self.genomas.append(genoma)
                self.passaros.append(Passaro(230, 350))

        while self.jogo_rodando:
            self.atualizacao_por_segundo.tick(self.FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.encerrar_jogo()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.encerrar_jogo()

                    if not self.ia_jogando:
                        if evento.key == pygame.K_SPACE:
                            self.pular()

            self.indice_cano: int = 0
            if len(self.passaros) > 0:
                if len(self.canos) > 1 and self.passaros[0].x > (
                        self.canos[0].x + self.canos[0].SPRITE_CANO_TOPO.get_width()):
                    self.indice_cano = 1
            else:
                self.jogo_rodando = False
                break

            self.mover_passaros()
            self.chao.mover()

            adicionar_cano: bool = False
            self.canos_a_serem_removidos = []

            for cano_atual in self.canos:
                for i, passaro_atual in enumerate(self.passaros):
                    if cano_atual.colidir(passaro_atual):
                        self.passaros.pop(i)

                        if self.ia_jogando:
                            self.genomas[i].fitness -= 1
                            self.genomas.pop(i)
                            self.redes_neurais.pop(i)

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

        if self.ia_jogando:
            texto = self.FONTE_PONTOS.render(f"Geração: {self.geracao}", True, (255, 255, 255))
            self.tela.blit(texto, (10, 10))

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
        for i, passaro in enumerate(self.passaros):
            passaro.mover()

            if self.ia_jogando:
                self.genomas[i].fitness += 0.1

                distancia_passaro_cano_topo: float = abs(passaro.y - self.canos[self.indice_cano].altura)
                distancia_passaro_cano_chao: float = abs(passaro.y - self.canos[self.indice_cano].posicao_base)
                inputs: tuple[float, float, float] = (
                    passaro.y, distancia_passaro_cano_topo, distancia_passaro_cano_chao)
                output: [float] = self.redes_neurais[i].activate(inputs)

                if output[0] > 0.5:
                    passaro.pular()

    def adicionar_cano(self):
        self.pontuacao += 1
        self.canos.append(Cano(600))

        if self.ia_jogando:
            for genoma in self.genomas:
                genoma.fitness += 5

    def remover_canos(self):
        for cano in self.canos_a_serem_removidos:
            self.canos.remove(cano)

    def remover_passaros(self):
        for i, passaro in enumerate(self.passaros):
            if passaro.y + passaro.sprite.get_height() > self.chao.y or passaro.y < 0:
                self.passaros.pop(i)

                if self.ia_jogando:
                    self.genomas[i].fitness -= 0.5
                    self.genomas.pop(i)
                    self.redes_neurais.pop(i)

    def iniciar_variaveis(self):
        pygame.font.init()
        self.FONTE_PONTOS: Font = pygame.font.SysFont('comic sans', 30)

        self.redes_neurais: [FeedForwardNetwork] = []
        self.genomas = []
        self.indice_cano: int = 0

        self.tela: Surface = pygame.display.set_mode((self.TELA_LARGURA, self.TELA_ALTURA))
        self.pontuacao: int = 0
        self.atualizacao_por_segundo: Clock = pygame.time.Clock()

        self.chao: Chao = Chao(730)
        self.canos: list[Cano] = [Cano(700)]

        self.canos_a_serem_removidos: [Cano] = []
