"""
Engine principal do jogo - substitui o main.py gigante
"""
import pygame
import sys
from typing import Dict, Optional

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from utils.logger import game_logger
from utils.config import game_config
from core.base_components import StateManager, EventDispatcher
from systems.audio.audio_manager import audio_manager
from systems.graphics.graphics_manager import GraphicsManager
from systems.input.input_manager import input_manager
from scenes.base_scene import BaseScene


class GameEngine:
    """
    Engine principal do jogo - coordena todos os sistemas.
    """
    
    def __init__(self):
        self.running = False
        self.screen = None
        self.clock = None
        self.dt = 0
        
        # Managers
        self.graphics_manager = None
        self.state_manager = None
        self.event_dispatcher = None
        
        # Inicialização
        self._initialize_pygame()
        self._initialize_managers()
        self._register_scenes()
        
        game_logger.info("GameEngine inicializado com sucesso")
    
    def _initialize_pygame(self) -> None:
        """
        Inicializa o pygame e configurações básicas.
        """
        try:
            pygame.mixer.pre_init(44100, 16, 2, 4096)
            pygame.init()
            
            # Configurar tela
            self.graphics_manager = GraphicsManager()
            self.graphics_manager.apply_settings()
            self.screen = self.graphics_manager.get_screen()
            
            # Fallback se GraphicsManager falhar
            if self.screen is None:
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                game_logger.warning("Fallback para resolução padrão")
            
            pygame.display.set_caption('CORRIDA PELA RELÍQUIA')
            self.clock = pygame.time.Clock()
            
            game_logger.info("Pygame inicializado com sucesso")
            
        except Exception as e:
            game_logger.error(f"Erro ao inicializar pygame: {e}")
            raise
    
    def _initialize_managers(self) -> None:
        """
        Inicializa todos os managers do jogo.
        """
        try:
            # State Manager
            self.state_manager = StateManager()
            
            # Event Dispatcher
            self.event_dispatcher = EventDispatcher()
            
            # Audio Manager já é singleton
            audio_manager.play_music('../audio/home.mp3')
            
            game_logger.info("Managers inicializados com sucesso")
            
        except Exception as e:
            game_logger.error(f"Erro ao inicializar managers: {e}")
            raise
    
    def _register_scenes(self) -> None:
        """
        Registra todas as cenas do jogo.
        """
        try:
            # Por enquanto, vamos usar uma cena placeholder
            from scenes.base_scene import MenuScene
            
            # Cena de menu principal
            main_menu = MenuScene("main_menu", self.screen)
            main_menu.add_menu_item("JOGAR", "start_game")
            main_menu.add_menu_item("CONFIGURAÇÕES", "settings")
            main_menu.add_menu_item("SAIR", "quit")
            
            self.state_manager.register_state("main_menu", main_menu)
            
            # Define cena inicial
            self.state_manager.change_state("main_menu")
            
            game_logger.info("Cenas registradas com sucesso")
            
        except Exception as e:
            game_logger.error(f"Erro ao registrar cenas: {e}")
            raise
    
    def run(self) -> None:
        """
        Loop principal do jogo.
        """
        self.running = True
        game_logger.info("Iniciando game loop principal")
        
        try:
            while self.running:
                # Calcula delta time
                self.dt = self.clock.tick(self.graphics_manager.get_fps_limit()) / 1000.0
                
                # Processa eventos
                events = pygame.event.get()
                self._handle_events(events)
                
                # Atualiza sistemas
                self._update()
                
                # Renderiza
                self._render()
                
                # Atualiza display
                pygame.display.flip()
                
        except Exception as e:
            game_logger.error(f"Erro no game loop: {e}")
            raise
        finally:
            self._cleanup()
    
    def _handle_events(self, events: list) -> None:
        """
        Processa eventos do jogo.
        
        Args:
            events (list): Lista de eventos do pygame
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
        
        # Atualiza input manager
        input_manager.update(events)
        
        # Repassa eventos para state manager
        self.state_manager.handle_events(events)
        
        # Processa comandos especiais
        self._handle_special_commands()
    
    def _handle_special_commands(self) -> None:
        """
        Processa comandos especiais globais.
        """
        # Quit command
        if input_manager.is_action_pressed('pause'):
            # Aqui poderia abrir menu de pause
            pass
        
        # Cheats (se habilitados)
        if game_config.get('debug', 'enable_cheats', False):
            if input_manager.is_action_pressed('cheat_level1'):
                # Implementar cheat
                pass
    
    def _update(self) -> None:
        """
        Atualiza todos os sistemas do jogo.
        """
        # Atualiza state manager
        self.state_manager.update(self.dt)
        
        # Atualiza sistemas que precisam de update
        # (AudioManager e GraphicsManager são passivos)
    
    def _render(self) -> None:
        """
        Renderiza o frame atual.
        """
        # Limpa tela
        self.screen.fill((0, 0, 0))
        
        # Renderiza cena atual
        self.state_manager.draw(self.screen)
        
        # Debug info (se habilitado)
        if game_config.get('debug', 'show_fps', False):
            self._draw_debug_info()
    
    def _draw_debug_info(self) -> None:
        """
        Desenha informações de debug.
        """
        font = pygame.font.Font(None, 24)
        fps_text = font.render(f"FPS: {self.clock.get_fps():.1f}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
        
        # Estado atual
        current_state = self.state_manager.get_current_state_name()
        if current_state:
            state_text = font.render(f"Estado: {current_state}", True, (255, 255, 255))
            self.screen.blit(state_text, (10, 35))
    
    def _cleanup(self) -> None:
        """
        Limpa recursos ao finalizar.
        """
        game_logger.info("Finalizando GameEngine")
        
        # Salva configurações
        game_config.save_config()
        
        # Finaliza pygame
        pygame.quit()
        sys.exit()
    
    def change_scene(self, scene_name: str) -> None:
        """
        Muda para uma nova cena.
        
        Args:
            scene_name (str): Nome da cena
        """
        self.state_manager.change_state(scene_name)
        game_logger.info(f"Mudando para cena: {scene_name}")
    
    def quit(self) -> None:
        """
        Encerra o jogo.
        """
        self.running = False
        game_logger.info("Comando de quit recebido")


# Ponto de entrada alternativo
def main():
    """
    Função principal alternativa.
    """
    try:
        engine = GameEngine()
        engine.run()
    except Exception as e:
        game_logger.critical(f"Erro fatal: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()