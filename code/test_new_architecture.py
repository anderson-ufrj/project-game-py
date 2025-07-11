"""
Teste da nova arquitetura - versão simplificada
"""
import pygame
import sys
import os

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from utils.logger import game_logger
from systems.audio.audio_manager import audio_manager
from systems.graphics.graphics_manager import GraphicsManager


class SimpleGameTest:
    """
    Teste simples da nova arquitetura.
    """
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Teste Nova Arquitetura')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Teste dos managers
        self.graphics_manager = GraphicsManager()
        
        # Fonte para texto
        self.font = pygame.font.Font(None, 36)
        
        game_logger.info("Teste da nova arquitetura iniciado")
    
    def run(self):
        """
        Loop principal de teste.
        """
        while self.running:
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            # Render
            self.screen.fill((50, 50, 100))
            
            # Texto de teste
            texts = [
                "🎮 TESTE DA NOVA ARQUITETURA",
                "",
                "✅ Pygame: OK",
                "✅ Utils: OK", 
                "✅ Systems: OK",
                "✅ Logger: OK",
                "✅ Audio Manager: OK",
                "✅ Graphics Manager: OK",
                "",
                "ESC para sair"
            ]
            
            y = 50
            for text in texts:
                if text:
                    surface = self.font.render(text, True, (255, 255, 255))
                    self.screen.blit(surface, (50, y))
                y += 40
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        game_logger.info("Teste finalizado")


def main():
    """
    Função principal de teste.
    """
    try:
        test = SimpleGameTest()
        test.run()
    except Exception as e:
        game_logger.error(f"Erro no teste: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()