"""
Versão híbrida: Nova arquitetura como launcher do jogo original
"""
import sys
import os
import pygame

# Adiciona o diretório atual ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from utils.logger import game_logger
from systems.audio.audio_manager import audio_manager
from systems.graphics.graphics_manager import GraphicsManager
from scenes.legacy_game_scene import LegacyGameBridge, start_legacy_game
from core.base_components import StateManager


class HybridGameEngine:
    """
    Engine híbrido que combina nova arquitetura com jogo original.
    """
    
    def __init__(self):
        self.running = False
        self.screen = None
        self.clock = None
        
        # Managers
        self.graphics_manager = None
        self.state_manager = None
        
        # Inicialização
        self._initialize_pygame()
        self._initialize_managers()
        self._register_scenes()
        
        game_logger.info("HybridGameEngine inicializado")
    
    def _initialize_pygame(self) -> None:
        """
        Inicializa pygame.
        """
        try:
            pygame.mixer.pre_init(44100, 16, 2, 4096)
            pygame.init()
            
            # Configurar tela
            self.graphics_manager = GraphicsManager()
            self.graphics_manager.apply_settings()
            self.screen = self.graphics_manager.get_screen()
            
            # Fallback
            if self.screen is None:
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            
            pygame.display.set_caption('CORRIDA PELA RELÍQUIA')
            self.clock = pygame.time.Clock()
            
        except Exception as e:
            game_logger.error(f"Erro ao inicializar pygame: {e}")
            raise
    
    def _initialize_managers(self) -> None:
        """
        Inicializa managers.
        """
        try:
            self.state_manager = StateManager()
            audio_manager.play_music('../audio/home.mp3')
            
        except Exception as e:
            game_logger.error(f"Erro ao inicializar managers: {e}")
            raise
    
    def _register_scenes(self) -> None:
        """
        Registra cenas.
        """
        try:
            # Cena de bridge
            bridge_scene = LegacyGameBridge("bridge", self.screen)
            self.state_manager.register_state("bridge", bridge_scene)
            
            # Define cena inicial
            self.state_manager.change_state("bridge")
            
        except Exception as e:
            game_logger.error(f"Erro ao registrar cenas: {e}")
            raise
    
    def run(self) -> None:
        """
        Loop principal.
        """
        self.running = True
        
        try:
            while self.running:
                dt = self.clock.tick(60) / 1000.0
                
                # Eventos
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False
                        return
                
                # Processa eventos nas cenas
                self.state_manager.handle_events(events)
                
                # Verifica se deve iniciar jogo original
                current_state = self.state_manager.current_state
                if current_state:
                    result = current_state.handle_scene_events(events)
                    if result == "start_legacy_game":
                        self._start_legacy_game()
                        return
                    elif result == "quit":
                        self.running = False
                        return
                
                # Atualiza
                self.state_manager.update(dt)
                
                # Renderiza
                self.screen.fill((0, 0, 0))
                self.state_manager.draw(self.screen)
                pygame.display.flip()
                
        except Exception as e:
            game_logger.error(f"Erro no loop principal: {e}")
        finally:
            self._cleanup()
    
    def _start_legacy_game(self) -> None:
        """
        Inicia o jogo original.
        """
        game_logger.info("Transitioning para jogo original...")
        
        # Para a música da nova arquitetura
        audio_manager.stop_music()
        
        # Limpa a tela
        pygame.quit()
        
        # Inicia o jogo original
        start_legacy_game()
    
    def _cleanup(self) -> None:
        """
        Limpa recursos.
        """
        game_logger.info("Finalizando HybridGameEngine")
        pygame.quit()
        sys.exit()


def main():
    """
    Função principal híbrida.
    """
    try:
        # Primeiro verifica se deve usar o jogo original diretamente
        if len(sys.argv) > 1 and sys.argv[1] == "--original":
            game_logger.info("Iniciando jogo original diretamente")
            start_legacy_game()
            return
        
        # Senão, usa o engine híbrido
        engine = HybridGameEngine()
        engine.run()
        
    except KeyboardInterrupt:
        game_logger.info("Jogo interrompido pelo usuário")
        
    except Exception as e:
        game_logger.critical(f"Erro fatal: {e}")
        
    finally:
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()