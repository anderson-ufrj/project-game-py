"""
Componentes base do sistema core
"""
import pygame
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable
from math import sin

from utils.constants import GAME_STATES
from utils.helpers import normalize_vector


class BaseEntity(pygame.sprite.Sprite, ABC):
    """
    Classe base para todas as entidades do jogo.
    Refatoração melhorada da classe Entity original.
    """
    
    def __init__(self, groups: pygame.sprite.Group, position: tuple = (0, 0)):
        super().__init__(groups)
        
        # Propriedades básicas
        self.position = pygame.math.Vector2(position)
        self.direction = pygame.math.Vector2()
        self.speed = 0
        
        # Animação
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animations = {}
        self.current_animation = 'idle'
        
        # Colisão
        self.hitbox = pygame.Rect(0, 0, 32, 32)
        self.obstacle_sprites = None
        
        # Estados
        self.alive = True
        self.active = True
        
        # Inicialização
        self._setup_entity()
    
    @abstractmethod
    def _setup_entity(self) -> None:
        """
        Configuração específica da entidade.
        Deve ser implementada pelas subclasses.
        """
        pass
    
    def update(self, dt: float) -> None:
        """
        Atualiza a entidade.
        
        Args:
            dt (float): Delta time
        """
        if not self.active:
            return
        
        self._update_animation(dt)
        self._update_logic(dt)
    
    def _update_animation(self, dt: float) -> None:
        """
        Atualiza animação da entidade.
        
        Args:
            dt (float): Delta time
        """
        if self.current_animation in self.animations:
            animation = self.animations[self.current_animation]
            self.frame_index += self.animation_speed * dt
            
            if self.frame_index >= len(animation):
                self.frame_index = 0
            
            self.image = animation[int(self.frame_index)]
    
    @abstractmethod
    def _update_logic(self, dt: float) -> None:
        """
        Lógica específica de atualização.
        Deve ser implementada pelas subclasses.
        
        Args:
            dt (float): Delta time
        """
        pass
    
    def move(self, speed: float) -> None:
        """
        Move a entidade com colisão.
        
        Args:
            speed (float): Velocidade de movimento
        """
        if self.direction.magnitude() != 0:
            self.direction = normalize_vector(self.direction)
        
        # Movimento horizontal
        self.hitbox.x += self.direction.x * speed
        self._check_collision('horizontal')
        
        # Movimento vertical
        self.hitbox.y += self.direction.y * speed
        self._check_collision('vertical')
        
        # Atualiza posição do sprite
        self.rect.center = self.hitbox.center
        self.position = pygame.math.Vector2(self.hitbox.center)
    
    def _check_collision(self, direction: str) -> None:
        """
        Verifica colisão com obstáculos.
        
        Args:
            direction (str): Direção da colisão ('horizontal' ou 'vertical')
        """
        if not self.obstacle_sprites:
            return
        
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # Movendo para direita
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # Movendo para esquerda
                        self.hitbox.left = sprite.hitbox.right
                elif direction == 'vertical':
                    if self.direction.y > 0:  # Movendo para baixo
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # Movendo para cima
                        self.hitbox.top = sprite.hitbox.bottom
    
    def get_wave_value(self) -> int:
        """
        Retorna valor sinusoidal para efeitos visuais.
        
        Returns:
            int: Valor 0 ou 255 baseado em sine wave
        """
        value = sin(pygame.time.get_ticks() * 0.01)
        return 255 if value >= 0 else 0
    
    def destroy(self) -> None:
        """
        Destrói a entidade.
        """
        self.alive = False
        self.active = False
        self.kill()


class BaseScene(ABC):
    """
    Classe base para todas as cenas do jogo.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.active = False
        self.screen = None
        self.clock = None
        
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.setup_scene()
    
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
    
    @abstractmethod
    def handle_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        """
        Trata eventos da cena.
        
        Args:
            events (List[pygame.event.Event]): Lista de eventos
            
        Returns:
            Optional[str]: Comando de mudança de cena ou None
        """
        pass
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Atualiza a cena.
        
        Args:
            dt (float): Delta time
        """
        pass
    
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha a cena.
        
        Args:
            screen (pygame.Surface): Surface da tela
        """
        pass


class StateManager:
    """
    Gerenciador de estados do jogo.
    """
    
    def __init__(self):
        self.states: Dict[str, BaseScene] = {}
        self.current_state: Optional[BaseScene] = None
        self.next_state: Optional[str] = None
        self.state_history: List[str] = []
    
    def register_state(self, name: str, state: BaseScene) -> None:
        """
        Registra um novo estado.
        
        Args:
            name (str): Nome do estado
            state (BaseScene): Instância do estado
        """
        self.states[name] = state
    
    def change_state(self, name: str) -> None:
        """
        Muda para um novo estado.
        
        Args:
            name (str): Nome do estado
        """
        if name in self.states:
            self.next_state = name
    
    def update(self, dt: float) -> None:
        """
        Atualiza o gerenciador de estados.
        
        Args:
            dt (float): Delta time
        """
        # Processa mudança de estado
        if self.next_state:
            self._perform_state_change()
        
        # Atualiza estado atual
        if self.current_state:
            self.current_state.update(dt)
    
    def _perform_state_change(self) -> None:
        """
        Executa a mudança de estado.
        """
        new_state_name = self.next_state
        self.next_state = None
        
        # Sai do estado atual
        if self.current_state:
            self.current_state.exit()
            self.state_history.append(self.current_state.name)
        
        # Entra no novo estado
        self.current_state = self.states[new_state_name]
        self.current_state.enter()
    
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Repassa eventos para o estado atual.
        
        Args:
            events (List[pygame.event.Event]): Lista de eventos
        """
        if self.current_state:
            result = self.current_state.handle_events(events)
            if result:
                self.change_state(result)
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o estado atual.
        
        Args:
            screen (pygame.Surface): Surface da tela
        """
        if self.current_state:
            self.current_state.draw(screen)
    
    def get_current_state_name(self) -> Optional[str]:
        """
        Retorna o nome do estado atual.
        
        Returns:
            Optional[str]: Nome do estado atual ou None
        """
        return self.current_state.name if self.current_state else None
    
    def go_back(self) -> None:
        """
        Volta para o estado anterior.
        """
        if self.state_history:
            previous_state = self.state_history.pop()
            self.change_state(previous_state)


class EventDispatcher:
    """
    Dispatcher de eventos para desacoplamento.
    """
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_name: str, callback: Callable) -> None:
        """
        Inscreve um callback para um evento.
        
        Args:
            event_name (str): Nome do evento
            callback (Callable): Função callback
        """
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)
    
    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """
        Remove um callback de um evento.
        
        Args:
            event_name (str): Nome do evento
            callback (Callable): Função callback
        """
        if event_name in self.listeners:
            if callback in self.listeners[event_name]:
                self.listeners[event_name].remove(callback)
    
    def emit(self, event_name: str, *args, **kwargs) -> None:
        """
        Emite um evento para todos os listeners.
        
        Args:
            event_name (str): Nome do evento
            *args: Argumentos do evento
            **kwargs: Argumentos nomeados do evento
        """
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"Erro no listener de {event_name}: {e}")


class BaseManager(ABC):
    """
    Classe base para todos os managers do jogo.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.initialized = False
        self.active = True
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Inicializa o manager.
        Deve ser implementado pelas subclasses.
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """
        Limpa recursos do manager.
        Deve ser implementado pelas subclasses.
        """
        pass
    
    def update(self, dt: float) -> None:
        """
        Atualiza o manager.
        
        Args:
            dt (float): Delta time
        """
        if not self.active:
            return
        
        self._update_manager(dt)
    
    def _update_manager(self, dt: float) -> None:
        """
        Lógica de atualização específica do manager.
        Pode ser sobrescrita pelas subclasses.
        
        Args:
            dt (float): Delta time
        """
        pass