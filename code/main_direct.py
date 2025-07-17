"""
Execução direta do jogo original com logging da nova arquitetura
"""
import sys
import os

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import game_logger


def main():
    """
    Executa o jogo original diretamente com logging melhorado.
    """
    try:
        game_logger.info("🎮 Iniciando Corrida pela Relíquia (Versão Original)")
        
        # Import e execução do jogo original
        from main import Game
        
        # Cria e executa o jogo original
        game = Game()
        game_logger.info("🚀 Jogo original carregado com sucesso")
        game.run()
        
    except KeyboardInterrupt:
        game_logger.info("🛑 Jogo interrompido pelo usuário")
        
    except Exception as e:
        game_logger.error(f"❌ Erro fatal no jogo: {e}")
        game_logger.exception("Traceback completo:")
        
    finally:
        # Garante que o pygame seja finalizado
        try:
            import pygame
            pygame.quit()
        except:
            pass
        
        game_logger.info("🎮 Jogo finalizado")
        sys.exit(0)


if __name__ == "__main__":
    main()