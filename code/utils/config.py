"""
Sistema de configuração do jogo
"""
import json
import os
from typing import Dict, Any, Optional


class GameConfig:
    """
    Gerenciador de configurações do jogo.
    """
    
    def __init__(self, config_file: str = "game_config.json"):
        self.config_file = config_file
        self.config = self._load_default_config()
        self.load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """
        Carrega configurações padrão.
        
        Returns:
            Dict[str, Any]: Configurações padrão
        """
        return {
            'graphics': {
                'resolution': '1280x800',
                'fullscreen': False,
                'vsync': True,
                'quality': 'high',
                'fps_limit': 60
            },
            'audio': {
                'music_volume': 0.5,
                'sfx_volume': 0.5,
                'is_muted': False
            },
            'gameplay': {
                'difficulty': 'normal',
                'auto_save': True,
                'tutorial_completed': False
            },
            'controls': {
                'movement_keys': ['w', 'a', 's', 'd'],
                'attack_key': 'space',
                'run_key': 'shift',
                'menu_key': 'escape'
            },
            'debug': {
                'show_fps': False,
                'show_hitboxes': False,
                'enable_cheats': False
            }
        }
    
    def load_config(self) -> None:
        """
        Carrega configurações do arquivo.
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge com configurações padrão
                    self._merge_config(self.config, loaded_config)
            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")
                print("Usando configurações padrão.")
    
    def save_config(self) -> None:
        """
        Salva configurações no arquivo.
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
    
    def _merge_config(self, default: Dict[str, Any], loaded: Dict[str, Any]) -> None:
        """
        Faz merge das configurações carregadas com as padrão.
        
        Args:
            default (Dict[str, Any]): Configurações padrão
            loaded (Dict[str, Any]): Configurações carregadas
        """
        for key, value in loaded.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Obtém valor de configuração.
        
        Args:
            section (str): Seção da configuração
            key (str): Chave da configuração
            default (Any): Valor padrão se não encontrar
            
        Returns:
            Any: Valor da configuração
        """
        if section in self.config and key in self.config[section]:
            return self.config[section][key]
        return default
    
    def set(self, section: str, key: str, value: Any) -> None:
        """
        Define valor de configuração.
        
        Args:
            section (str): Seção da configuração
            key (str): Chave da configuração
            value (Any): Valor a ser definido
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Obtém uma seção completa de configurações.
        
        Args:
            section (str): Nome da seção
            
        Returns:
            Dict[str, Any]: Configurações da seção
        """
        return self.config.get(section, {})
    
    def set_section(self, section: str, values: Dict[str, Any]) -> None:
        """
        Define valores para uma seção completa.
        
        Args:
            section (str): Nome da seção
            values (Dict[str, Any]): Valores da seção
        """
        self.config[section] = values
    
    def reset_to_default(self) -> None:
        """
        Reseta configurações para o padrão.
        """
        self.config = self._load_default_config()
    
    def __getitem__(self, key: str) -> Any:
        """
        Permite acesso direto como config['section']['key'].
        
        Args:
            key (str): Chave da configuração
            
        Returns:
            Any: Valor da configuração
        """
        return self.config[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """
        Permite definição direta como config['section'] = value.
        
        Args:
            key (str): Chave da configuração
            value (Any): Valor a ser definido
        """
        self.config[key] = value


# Instância global de configuração
game_config = GameConfig()