"""
Sistema de cenas base para o jogo
"""
import pygame
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from utils.constants import GAME_STATES
from systems.input.input_manager import input_manager
from systems.audio.audio_manager import audio_manager
from systems.graphics.graphics_manager import GraphicsManager


class BaseScene(ABC):
    """
    Classe base para todas as cenas do jogo.
    """
    
    def __init__(self, name: str, screen: pygame.Surface):
        self.name = name
        self.screen = screen
        self.active = False
        self.initialized = False
        
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group()
        
        # Configurações da cena
        self.background_color = (0, 0, 0)
        self.background_image = None
        
        # Managers
        self.graphics_manager = GraphicsManager()
        
        # Estados
        self.transition_alpha = 0
        self.transitioning = False
        self.next_scene = None
        
        # Inicialização
        self._initialize_scene()
    
    def _initialize_scene(self) -> None:
        """
        Inicialização interna da cena.
        """
        if not self.initialized:
            self.setup_scene()
            self.initialized = True
    
    @abstractmethod
    def setup_scene(self) -> None:
        """
        Configuração inicial da cena.
        Deve ser implementada pelas subclasses.
        """
        pass
    
    def enter(self) -> None:
        """
        Chamada quando a cena se torna ativa.
        """
        self.active = True
        self.on_enter()
    
    def exit(self) -> None:
        """
        Chamada quando a cena deixa de ser ativa.
        """
        self.active = False
        self.on_exit()
    
    def on_enter(self) -> None:
        """
        Callback para quando a cena é ativada.
        Pode ser sobrescrita pelas subclasses.
        """
        pass
    
    def on_exit(self) -> None:
        """
        Callback para quando a cena é desativada.
        Pode ser sobrescrita pelas subclasses.
        """
        pass
    
    def handle_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        """
        Trata eventos da cena.
        
        Args:
            events (List[pygame.event.Event]): Lista de eventos
            
        Returns:
            Optional[str]: Comando de mudança de cena ou None
        """
        if not self.active:
            return None
        
        # Eventos globais
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            
            # Fullscreen toggle
            if (event.type == pygame.KEYDOWN and 
                event.key == pygame.K_RETURN and 
                (pygame.key.get_pressed()[pygame.K_LALT] or pygame.key.get_pressed()[pygame.K_RALT])):
                self.graphics_manager.toggle_fullscreen()
                self.graphics_manager.apply_settings()
                continue
        
        # Eventos específicos da cena
        return self.handle_scene_events(events)
    
    @abstractmethod
    def handle_scene_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        """
        Trata eventos específicos da cena.
        
        Args:
            events (List[pygame.event.Event]): Lista de eventos
            
        Returns:
            Optional[str]: Comando de mudança de cena ou None
        """
        pass
    
    def update(self, dt: float) -> None:
        """
        Atualiza a cena.
        
        Args:
            dt (float): Delta time
        """
        if not self.active:
            return
        
        # Atualiza sprites
        self.all_sprites.update(dt)
        self.ui_sprites.update(dt)
        
        # Atualiza lógica específica da cena
        self.update_scene(dt)
        
        # Atualiza transições
        if self.transitioning:
            self._update_transition(dt)
    
    @abstractmethod
    def update_scene(self, dt: float) -> None:
        """
        Atualiza lógica específica da cena.
        
        Args:
            dt (float): Delta time
        """
        pass
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha a cena.
        
        Args:
            screen (pygame.Surface): Surface da tela
        """
        if not self.active:
            return
        
        # Limpa a tela
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(self.background_color)
        
        # Desenha sprites
        self.all_sprites.draw(screen)
        
        # Desenha conteúdo específico da cena
        self.draw_scene(screen)
        
        # Desenha UI por último
        self.ui_sprites.draw(screen)
        
        # Desenha transições
        if self.transitioning:
            self._draw_transition(screen)
    
    @abstractmethod
    def draw_scene(self, screen: pygame.Surface) -> None:
        """
        Desenha conteúdo específico da cena.
        
        Args:
            screen (pygame.Surface): Surface da tela
        """
        pass
    
    def start_transition(self, next_scene: str) -> None:
        """
        Inicia uma transição para outra cena.
        
        Args:
            next_scene (str): Nome da próxima cena
        """
        self.transitioning = True
        self.next_scene = next_scene
        self.transition_alpha = 0
    
    def _update_transition(self, dt: float) -> None:
        """
        Atualiza a transição.
        
        Args:
            dt (float): Delta time
        """
        self.transition_alpha += dt * 1000  # 1 segundo de transição
        if self.transition_alpha >= 255:
            self.transition_alpha = 255
            self.transitioning = False
    
    def _draw_transition(self, screen: pygame.Surface) -> None:
        """
        Desenha efeito de transição.
        
        Args:
            screen (pygame.Surface): Surface da tela
        """
        if self.transition_alpha > 0:
            overlay = pygame.Surface(screen.get_size())
            overlay.set_alpha(self.transition_alpha)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
    
    def set_background_color(self, color: tuple) -> None:
        """
        Define a cor de fundo da cena.
        
        Args:
            color (tuple): Cor RGB
        """
        self.background_color = color
    
    def set_background_image(self, image_path: str) -> None:
        """
        Define uma imagem de fundo para a cena.
        
        Args:
            image_path (str): Caminho para a imagem
        """
        try:
            self.background_image = pygame.image.load(image_path).convert()
            self.background_image = pygame.transform.scale(
                self.background_image, 
                self.screen.get_size()
            )
        except pygame.error as e:
            print(f"Erro ao carregar imagem de fundo: {e}")
            self.background_image = None


class MenuScene(BaseScene):
    """
    Cena base para menus.
    """
    
    def __init__(self, name: str, screen: pygame.Surface):
        super().__init__(name, screen)
        self.menu_items = []
        self.selected_index = 0
        self.font = None
        
    def setup_scene(self) -> None:
        """
        Configuração do menu.
        """
        # Carrega fonte padrão
        try:
            self.font = pygame.font.Font(None, 36)
        except pygame.error:
            self.font = pygame.font.Font(None, 36)
    
    def add_menu_item(self, text: str, action: str) -> None:
        """
        Adiciona item ao menu.
        
        Args:
            text (str): Texto do item
            action (str): Ação do item
        """
        self.menu_items.append({
            'text': text,
            'action': action,
            'surface': self.font.render(text, True, (255, 255, 255))
        })
    
    def handle_scene_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        """
        Trata eventos do menu.
        
        Args:
            events (List[pygame.event.Event]): Lista de eventos
            
        Returns:
            Optional[str]: Comando de mudança de cena ou None
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    return self.menu_items[self.selected_index]['action']
        
        return None
    
    def update_scene(self, dt: float) -> None:
        """
        Atualiza o menu.
        
        Args:
            dt (float): Delta time
        """
        pass
    
    def draw_scene(self, screen: pygame.Surface) -> None:
        """
        Desenha o menu.
        
        Args:
            screen (pygame.Surface): Surface da tela
        """
        if not self.menu_items:
            return
        
        # Calcula posição central
        total_height = len(self.menu_items) * 60
        start_y = (screen.get_height() - total_height) // 2
        
        for i, item in enumerate(self.menu_items):
            y = start_y + i * 60
            x = (screen.get_width() - item['surface'].get_width()) // 2
            
            # Destaca item selecionado
            if i == self.selected_index:
                pygame.draw.rect(screen, (50, 50, 50), 
                               (x - 10, y - 5, item['surface'].get_width() + 20, 40))
            
            screen.blit(item['surface'], (x, y))


class GameScene(BaseScene):
    """
    Cena base para gameplay.
    """
    
    def __init__(self, name: str, screen: pygame.Surface):
        super().__init__(name, screen)
        self.camera_group = None
        self.paused = False
        self.pause_overlay = None
        
    def setup_scene(self) -> None:
        """
        Configuração da cena de gameplay.
        """
        # Cria overlay de pause
        self.pause_overlay = pygame.Surface(self.screen.get_size())
        self.pause_overlay.set_alpha(128)
        self.pause_overlay.fill((0, 0, 0))
    
    def handle_scene_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        """
        Trata eventos do gameplay.
        
        Args:
            events (List[pygame.event.Event]): Lista de eventos
            
        Returns:
            Optional[str]: Comando de mudança de cena ou None
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    return None
        
        # Se pausado, não processa outros eventos
        if self.paused:
            return None
        
        return self.handle_gameplay_events(events)
    
    @abstractmethod
    def handle_gameplay_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        """
        Trata eventos específicos do gameplay.
        
        Args:
            events (List[pygame.event.Event]): Lista de eventos
            
        Returns:
            Optional[str]: Comando de mudança de cena ou None
        """
        pass
    
    def update_scene(self, dt: float) -> None:
        """
        Atualiza o gameplay.
        
        Args:
            dt (float): Delta time
        """
        if not self.paused:
            self.update_gameplay(dt)
    
    @abstractmethod
    def update_gameplay(self, dt: float) -> None:
        """
        Atualiza lógica específica do gameplay.
        
        Args:
            dt (float): Delta time
        """
        pass
    
    def draw_scene(self, screen: pygame.Surface) -> None:
        """
        Desenha o gameplay.
        
        Args:
            screen (pygame.Surface): Surface da tela
        """
        # Desenha jogo
        self.draw_gameplay(screen)
        
        # Overlay de pause
        if self.paused:
            screen.blit(self.pause_overlay, (0, 0))
            
            # Texto de pause
            font = pygame.font.Font(None, 72)
            text = font.render("PAUSADO", True, (255, 255, 255))
            text_rect = text.get_rect(center=screen.get_rect().center)
            screen.blit(text, text_rect)
    
    @abstractmethod
    def draw_gameplay(self, screen: pygame.Surface) -> None:
        """
        Desenha conteúdo específico do gameplay.
        
        Args:
            screen (pygame.Surface): Surface da tela
        """
        pass