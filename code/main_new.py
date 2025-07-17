"""
Ponto de entrada principal do jogo - Nova arquitetura
"""
import sys
import os

# Adiciona o diretório atual ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.game_engine import GameEngine
from utils.logger import game_logger


def main():
    """
    Função principal do jogo.
    """
    try:
        # Cria e executa o game engine
        game = GameEngine()
        game.run()
        
    except KeyboardInterrupt:
        game_logger.info("Jogo interrompido pelo usuário")
        
    except Exception as e:
        game_logger.critical(f"Erro fatal no jogo: {e}")
        game_logger.exception("Traceback completo:")
        
    finally:
        # Garante que o pygame seja finalizado
        import pygame
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()