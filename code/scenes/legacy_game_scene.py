"""
Cena que executa o jogo original usando a nova arquitetura como wrapper
"""
import pygame
import sys
import os
from typing import List, Optional

from scenes.base_scene import BaseScene
from utils.logger import game_logger


class LegacyGameScene(BaseScene):
    """
    Cena que executa o jogo original dentro da nova arquitetura.
    """
    
    def __init__(self, name: str, screen: pygame.Surface):
        super().__init__(name, screen)
        self.legacy_game = None
        self.initialized = False
        
    def setup_scene(self) -> None:
        """
        Configura a cena legacy.
        """
        try:
            # Import do jogo original
            from main import Game as LegacyGame
            
            # Substitui a tela do jogo original pela nossa
            self.legacy_game = LegacyGame()
            self.legacy_game.screen = self.screen
            
            game_logger.info("Jogo original carregado na nova arquitetura")
            self.initialized = True
            
        except Exception as e:
            game_logger.error(f"Erro ao carregar jogo original: {e}")
            self.initialized = False
    
    def handle_scene_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        """
        Repassa eventos para o jogo original.
        """
        if not self.initialized or not self.legacy_game:
            return None
        
        # O jogo original gerencia seus próprios eventos
        # Apenas interceptamos QUIT
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
        
        return None
    
    def update_scene(self, dt: float) -> None:
        """
        Atualiza o jogo original.
        """
        if not self.initialized or not self.legacy_game:
            return
        
        # O jogo original tem seu próprio loop
        # Por enquanto, deixamos ele gerenciar
        pass
    
    def draw_scene(self, screen: pygame.Surface) -> None:
        """
        Desenha o jogo original.
        """
        if not self.initialized:
            # Desenha tela de erro
            font = pygame.font.Font(None, 48)
            error_text = font.render("Erro ao carregar jogo original", True, (255, 0, 0))
            text_rect = error_text.get_rect(center=screen.get_rect().center)
            screen.blit(error_text, text_rect)
            return
        
        if not self.legacy_game:
            return
        
        # Executa um frame do jogo original
        try:
            # O jogo original desenha diretamente na tela
            # Vamos tentar executar seu método run de forma não-bloqueante
            self._run_legacy_frame()
        except Exception as e:
            game_logger.error(f"Erro ao executar frame do jogo original: {e}")
    
    def _run_legacy_frame(self) -> None:
        """
        Executa um frame do jogo original.
        """
        # Por simplicidade, vamos usar a abordagem de executar o jogo original
        # e capturar quando ele terminar
        
        if hasattr(self.legacy_game, 'homescreen') and self.legacy_game.game_state == 0:
            self.legacy_game.homescreen()
        elif hasattr(self.legacy_game, 'run'):
            # Seria ideal refatorar o run() para ser frame-based
            # Por agora, vamos usar uma abordagem mais direta
            pass


class LegacyGameBridge(BaseScene):
    """
    Bridge simplificado que executa o jogo original diretamente.
    """
    
    def __init__(self, name: str, screen: pygame.Surface):
        super().__init__(name, screen)
        self.game_running = False
        
    def setup_scene(self) -> None:
        """
        Setup do bridge.
        """
        game_logger.info("Bridge para jogo original configurado")
    
    def handle_scene_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        """
        Detecta quando iniciar o jogo original.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return "start_legacy_game"
                elif event.key == pygame.K_ESCAPE:
                    return "quit"
        return None
    
    def update_scene(self, dt: float) -> None:
        """
        Update do bridge.
        """
        pass
    
    def draw_scene(self, screen: pygame.Surface) -> None:
        """
        Desenha tela de transição.
        """
        # Fundo
        screen.fill((25, 25, 35))
        
        # Textos
        font_title = pygame.font.Font(None, 64)
        font_text = pygame.font.Font(None, 36)
        
        title = font_title.render("CORRIDA PELA RELÍQUIA", True, (255, 255, 255))
        subtitle = font_text.render("Nova Arquitetura + Jogo Original", True, (180, 180, 180))
        instruction = font_text.render("SPACE/ENTER: Iniciar Jogo Original", True, (100, 255, 100))
        instruction2 = font_text.render("ESC: Sair", True, (255, 100, 100))
        
        # Centralizar textos
        title_rect = title.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 100))
        subtitle_rect = subtitle.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))
        instruction_rect = instruction.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 50))
        instruction2_rect = instruction2.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 100))
        
        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)
        screen.blit(instruction, instruction_rect)
        screen.blit(instruction2, instruction2_rect)


def start_legacy_game():
    """
    Inicia o jogo original diretamente.
    """
    try:
        game_logger.info("Iniciando jogo original...")
        
        # Import e execução do jogo original
        from main import Game
        
        # Cria e executa o jogo original
        legacy_game = Game()
        legacy_game.run()
        
    except Exception as e:
        game_logger.error(f"Erro ao executar jogo original: {e}")
        pygame.quit()
        sys.exit(1)