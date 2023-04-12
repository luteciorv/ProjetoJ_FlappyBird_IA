import os.path

import neat.config
from Models.jogo import Jogo


class NeatIA:
    CAMINHO_ARQUIVO_CONFIG: str = os.path.join(os.path.dirname(__file__), 'config.txt')

    def aprender(self):
        config = neat.config.Config(neat.DefaultGenome,
                                    neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation,
                                    self.CAMINHO_ARQUIVO_CONFIG)

        populacao = neat.Population(config)
        populacao.add_reporter(neat.StdOutReporter(True))
        populacao.add_reporter(neat.StatisticsReporter())

        jogo: Jogo = Jogo()

        if jogo.ia_jogando:
            populacao.run(jogo.iniciar_jogo, 50)
        else:
            jogo.iniciar_jogo(None, None)
