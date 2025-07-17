"""
Gerenciador de entrada centralizado
"""
import pygame
from typing import Dict, List, Optional, Callable, Any
from utils.constants import GAME_STATES
from utils.config import game_config


class InputManager:
    """
    Gerenciador centralizado de input para o jogo.
    """
    
    def __init__(self):
        self.key_bindings = self._load_key_bindings()
        self.mouse_bindings = {}
        self.event_handlers = {}
        self.key_states = {}
        self.mouse_states = {}
        
        # Estados de input
        self.keys_pressed = set()
        self.keys_held = set()
        self.keys_released = set()
        
        # Mouse
        self.mouse_pos = (0, 0)
        self.mouse_buttons = [False, False, False]  # Left, Middle, Right
        self.mouse_wheel = 0
        
        # Controles especiais
        self.alt_pressed = False
        self.ctrl_pressed = False
        self.shift_pressed = False
    
    def _load_key_bindings(self) -> Dict[str, List[int]]:
        """
        Carrega mapeamento de teclas.
        
        Returns:
            Dict[str, List[int]]: Mapeamento de ações para teclas
        """
        return {
            'move_up': [pygame.K_w, pygame.K_UP],
            'move_down': [pygame.K_s, pygame.K_DOWN],
            'move_left': [pygame.K_a, pygame.K_LEFT],
            'move_right': [pygame.K_d, pygame.K_RIGHT],
            'attack': [pygame.K_SPACE],
            'run': [pygame.K_LSHIFT, pygame.K_RSHIFT],
            'change_weapon': [pygame.K_q],
            'change_magic': [pygame.K_e],
            'cast_magic': [pygame.K_LCTRL, pygame.K_RCTRL],
            'pause': [pygame.K_ESCAPE],
            'minimap': [pygame.K_TAB],
            'mute': [pygame.K_m],
            'volume_up': [pygame.K_UP],
            'volume_down': [pygame.K_DOWN],
            'quick_save': [pygame.K_F5],
            'quick_load': [pygame.K_F9],
            'save_menu': [pygame.K_F6],
            'graphics_menu': [pygame.K_g],
            'stats_menu': [pygame.K_s],
            'difficulty_menu': [pygame.K_d],
            'load_menu': [pygame.K_l],
            'fullscreen': [pygame.K_RETURN],  # With Alt
            'cheat_level1': [pygame.K_F1, pygame.K_1],
            'cheat_level2': [pygame.K_F2, pygame.K_2],
            'cheat_level3': [pygame.K_F3, pygame.K_3],
            'cheat_level4': [pygame.K_F4, pygame.K_4],
        }
    
    def update(self, events: List[pygame.event.Event]) -> None:
        """
        Atualiza o estado do input manager.
        
        Args:
            events (List[pygame.event.Event]): Lista de eventos do pygame
        """
        # Reset estados por frame
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.mouse_wheel = 0
        
        # Atualiza posição do mouse
        self.mouse_pos = pygame.mouse.get_pos()
        
        # Atualiza estados de modificadores
        keys = pygame.key.get_pressed()
        self.alt_pressed = keys[pygame.K_LALT] or keys[pygame.K_RALT]
        self.ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        self.shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        
        # Processa eventos
        for event in events:
            self._process_event(event)
    
    def _process_event(self, event: pygame.event.Event) -> None:
        """
        Processa um evento específico.
        
        Args:
            event (pygame.event.Event): Evento a ser processado
        """
        if event.type == pygame.KEYDOWN:
            self.keys_pressed.add(event.key)
            self.keys_held.add(event.key)
            self.key_states[event.key] = True
            
        elif event.type == pygame.KEYUP:
            self.keys_released.add(event.key)
            self.keys_held.discard(event.key)
            self.key_states[event.key] = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button <= 3:
                self.mouse_buttons[event.button - 1] = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button <= 3:
                self.mouse_buttons[event.button - 1] = False
                
        elif event.type == pygame.MOUSEWHEEL:
            self.mouse_wheel = event.y
    
    def is_action_pressed(self, action: str) -> bool:
        """
        Verifica se uma ação foi pressionada neste frame.
        
        Args:
            action (str): Nome da ação
            
        Returns:
            bool: True se a ação foi pressionada
        """
        if action not in self.key_bindings:
            return False
        
        for key in self.key_bindings[action]:
            if key in self.keys_pressed:
                return True
        return False
    
    def is_action_held(self, action: str) -> bool:
        """
        Verifica se uma ação está sendo mantida pressionada.
        
        Args:
            action (str): Nome da ação
            
        Returns:
            bool: True se a ação está sendo mantida
        """
        if action not in self.key_bindings:
            return False
        
        for key in self.key_bindings[action]:
            if key in self.keys_held:
                return True
        return False
    
    def is_action_released(self, action: str) -> bool:
        """
        Verifica se uma ação foi liberada neste frame.
        
        Args:
            action (str): Nome da ação
            
        Returns:
            bool: True se a ação foi liberada
        """
        if action not in self.key_bindings:
            return False
        
        for key in self.key_bindings[action]:
            if key in self.keys_released:
                return True
        return False
    
    def is_key_pressed(self, key: int) -> bool:
        """
        Verifica se uma tecla específica foi pressionada.
        
        Args:
            key (int): Código da tecla
            
        Returns:
            bool: True se a tecla foi pressionada
        """
        return key in self.keys_pressed
    
    def is_key_held(self, key: int) -> bool:
        """
        Verifica se uma tecla específica está sendo mantida.
        
        Args:
            key (int): Código da tecla
            
        Returns:
            bool: True se a tecla está sendo mantida
        """
        return key in self.keys_held
    
    def get_movement_vector(self) -> pygame.math.Vector2:
        """
        Retorna o vetor de movimento baseado nas teclas pressionadas.
        
        Returns:
            pygame.math.Vector2: Vetor de movimento normalizado
        """
        direction = pygame.math.Vector2()
        
        if self.is_action_held('move_up'):
            direction.y -= 1
        if self.is_action_held('move_down'):
            direction.y += 1
        if self.is_action_held('move_left'):
            direction.x -= 1
        if self.is_action_held('move_right'):
            direction.x += 1
        
        if direction.magnitude() > 0:
            direction = direction.normalize()
        
        return direction
    
    def get_mouse_position(self) -> tuple:
        """
        Retorna a posição atual do mouse.
        
        Returns:
            tuple: Posição (x, y) do mouse
        """
        return self.mouse_pos
    
    def is_mouse_button_pressed(self, button: int) -> bool:
        """
        Verifica se um botão do mouse está pressionado.
        
        Args:
            button (int): Número do botão (1=esquerdo, 2=meio, 3=direito)
            
        Returns:
            bool: True se o botão está pressionado
        """
        if 1 <= button <= 3:
            return self.mouse_buttons[button - 1]
        return False
    
    def get_mouse_wheel(self) -> int:
        """
        Retorna o movimento da roda do mouse.
        
        Returns:
            int: Movimento da roda (-1, 0, 1)
        """
        return self.mouse_wheel
    
    def bind_key(self, action: str, key: int) -> None:
        """
        Vincula uma tecla a uma ação.
        
        Args:
            action (str): Nome da ação
            key (int): Código da tecla
        """
        if action not in self.key_bindings:
            self.key_bindings[action] = []
        
        if key not in self.key_bindings[action]:
            self.key_bindings[action].append(key)
    
    def unbind_key(self, action: str, key: int) -> None:
        """
        Remove a vinculação de uma tecla.
        
        Args:
            action (str): Nome da ação
            key (int): Código da tecla
        """
        if action in self.key_bindings:
            if key in self.key_bindings[action]:
                self.key_bindings[action].remove(key)
    
    def save_bindings(self) -> None:
        """
        Salva as vinculações de teclas na configuração.
        """
        game_config.set_section('controls', {
            'key_bindings': self.key_bindings
        })
        game_config.save_config()
    
    def load_bindings(self) -> None:
        """
        Carrega as vinculações de teclas da configuração.
        """
        controls = game_config.get_section('controls')
        if 'key_bindings' in controls:
            self.key_bindings.update(controls['key_bindings'])


# Instância global do input manager
input_manager = InputManager()