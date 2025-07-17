import json
import os
from typing import Dict, Any

class DifficultyManager:
    """Gerencia os níveis de dificuldade do jogo"""
    
    def __init__(self):
        self.settings_file = "difficulty_settings.json"
        self.current_difficulty = "normal"
        
        # Definir configurações de dificuldade
        self.difficulty_settings = {
            "facil": {
                "name": "Fácil",
                "description": "Para iniciantes",
                "player_health_multiplier": 1.5,  # +50% vida
                "player_damage_multiplier": 1.2,   # +20% dano
                "enemy_health_multiplier": 0.7,    # -30% vida dos inimigos
                "enemy_damage_multiplier": 0.6,    # -40% dano dos inimigos
                "enemy_speed_multiplier": 0.8,     # -20% velocidade dos inimigos
                "orb_spawn_multiplier": 1.5,       # +50% orbs
                "experience_multiplier": 0.8,      # -20% experiência (menor desafio)
                "color": (100, 255, 100)           # Verde
            },
            "normal": {
                "name": "Normal",
                "description": "Experiência equilibrada",
                "player_health_multiplier": 1.0,
                "player_damage_multiplier": 1.0,
                "enemy_health_multiplier": 1.0,
                "enemy_damage_multiplier": 1.0,
                "enemy_speed_multiplier": 1.0,
                "orb_spawn_multiplier": 1.0,
                "experience_multiplier": 1.0,
                "color": (255, 255, 100)           # Amarelo
            },
            "dificil": {
                "name": "Difícil",
                "description": "Para veteranos",
                "player_health_multiplier": 0.7,   # -30% vida
                "player_damage_multiplier": 0.9,   # -10% dano
                "enemy_health_multiplier": 1.3,    # +30% vida dos inimigos
                "enemy_damage_multiplier": 1.5,    # +50% dano dos inimigos
                "enemy_speed_multiplier": 1.2,     # +20% velocidade dos inimigos
                "orb_spawn_multiplier": 0.7,       # -30% orbs
                "experience_multiplier": 1.5,      # +50% experiência (maior desafio)
                "color": (255, 100, 100)           # Vermelho
            }
        }
        
        self.load_settings()
    
    def load_settings(self):
        """Carrega configurações de dificuldade do arquivo"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.current_difficulty = data.get("current_difficulty", "normal")
                    print(f"🎯 Dificuldade carregada: {self.get_current_name()}")
            except Exception as e:
                print(f"❌ Erro ao carregar dificuldade: {e}")
                self.current_difficulty = "normal"
    
    def save_settings(self):
        """Salva configurações de dificuldade no arquivo"""
        try:
            data = {
                "current_difficulty": self.current_difficulty
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Dificuldade salva: {self.get_current_name()}")
        except Exception as e:
            print(f"❌ Erro ao salvar dificuldade: {e}")
    
    def set_difficulty(self, difficulty: str):
        """Define a dificuldade atual"""
        if difficulty in self.difficulty_settings:
            self.current_difficulty = difficulty
            self.save_settings()
            print(f"🎯 Dificuldade alterada para: {self.get_current_name()}")
            return True
        return False
    
    def get_current_difficulty(self) -> str:
        """Retorna a dificuldade atual"""
        return self.current_difficulty
    
    def get_current_name(self) -> str:
        """Retorna o nome da dificuldade atual"""
        return self.difficulty_settings[self.current_difficulty]["name"]
    
    def get_current_description(self) -> str:
        """Retorna a descrição da dificuldade atual"""
        return self.difficulty_settings[self.current_difficulty]["description"]
    
    def get_current_color(self) -> tuple:
        """Retorna a cor da dificuldade atual"""
        return self.difficulty_settings[self.current_difficulty]["color"]
    
    def get_setting(self, setting_name: str) -> float:
        """Retorna um valor específico da dificuldade atual"""
        return self.difficulty_settings[self.current_difficulty].get(setting_name, 1.0)
    
    def get_all_difficulties(self) -> Dict[str, Dict[str, Any]]:
        """Retorna todas as dificuldades disponíveis"""
        return self.difficulty_settings
    
    def cycle_difficulty(self) -> str:
        """Alterna para a próxima dificuldade"""
        difficulties = list(self.difficulty_settings.keys())
        current_index = difficulties.index(self.current_difficulty)
        next_index = (current_index + 1) % len(difficulties)
        self.set_difficulty(difficulties[next_index])
        return self.current_difficulty
    
    def apply_to_player_stats(self, base_health: int, base_damage: int) -> tuple:
        """Aplica modificadores de dificuldade às estatísticas do jogador"""
        health = int(base_health * self.get_setting("player_health_multiplier"))
        damage = int(base_damage * self.get_setting("player_damage_multiplier"))
        return health, damage
    
    def apply_to_enemy_stats(self, base_health: int, base_damage: int, base_speed: float) -> tuple:
        """Aplica modificadores de dificuldade às estatísticas dos inimigos"""
        health = int(base_health * self.get_setting("enemy_health_multiplier"))
        damage = int(base_damage * self.get_setting("enemy_damage_multiplier"))
        speed = base_speed * self.get_setting("enemy_speed_multiplier")
        return health, damage, speed
    
    def should_spawn_orb(self, base_chance: float = 1.0) -> bool:
        """Determina se deve spawnar um orb baseado na dificuldade"""
        import random
        spawn_chance = base_chance * self.get_setting("orb_spawn_multiplier")
        return random.random() < spawn_chance
    
    def get_experience_reward(self, base_exp: int) -> int:
        """Calcula a experiência baseada na dificuldade"""
        return int(base_exp * self.get_setting("experience_multiplier"))
    
    def get_stats_summary(self) -> Dict[str, str]:
        """Retorna um resumo das modificações da dificuldade atual"""
        settings = self.difficulty_settings[self.current_difficulty]
        
        def format_multiplier(value: float, is_positive_good: bool = True) -> str:
            if value == 1.0:
                return "Normal"
            elif value > 1.0:
                percent = int((value - 1.0) * 100)
                symbol = "+" if is_positive_good else "-"
                return f"{symbol}{percent}%"
            else:
                percent = int((1.0 - value) * 100)
                symbol = "-" if is_positive_good else "+"
                return f"{symbol}{percent}%"
        
        return {
            "Vida do Jogador": format_multiplier(settings["player_health_multiplier"], True),
            "Dano do Jogador": format_multiplier(settings["player_damage_multiplier"], True),
            "Vida dos Inimigos": format_multiplier(settings["enemy_health_multiplier"], False),
            "Dano dos Inimigos": format_multiplier(settings["enemy_damage_multiplier"], False),
            "Velocidade Inimigos": format_multiplier(settings["enemy_speed_multiplier"], False),
            "Quantidade de Orbs": format_multiplier(settings["orb_spawn_multiplier"], True),
            "Experiência": format_multiplier(settings["experience_multiplier"], True)
        }

# Instância singleton
difficulty_manager = DifficultyManager()