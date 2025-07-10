import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class PlayerStats:
    def __init__(self):
        self.stats_file = "player_stats.json"
        self.session_start_time = time.time()
        self.level_start_time = None
        self.current_level = 1
        
        # Inicializar estatísticas padrão
        self.stats = {
            "player_name": "",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_played": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_playtime": 0,  # em segundos
            "game_sessions": 0,
            "current_level": 1,
            "levels_completed": [],
            
            # Estatísticas de combate
            "combat_stats": {
                "enemies_killed": 0,
                "enemies_by_type": {
                    "golu": 0,
                    "black": 0,
                    "bigboi": 0
                },
                "damage_dealt": 0,
                "damage_taken": 0,
                "deaths": 0,
                "attacks_made": 0,
                "magic_cast": 0,
                "magic_by_type": {
                    "flame": 0,
                    "heal": 0
                }
            },
            
            # Estatísticas de performance
            "performance": {
                "best_times": {
                    "level1": None,
                    "level2": None,
                    "level3": None,
                    "level4": None
                },
                "attempts_per_level": {
                    "level1": 0,
                    "level2": 0,
                    "level3": 0,
                    "level4": 0
                },
                "steps_taken": 0,
                "distance_traveled": 0
            },
            
            # Estatísticas de coleta
            "collection_stats": {
                "health_orbs": 0,
                "attack_orbs": 0,
                "speed_orbs": 0,
                "keys_found": 0,
                "eldritch_gems": 0
            },
            
            # Estatísticas de equipamentos
            "equipment_stats": {
                "weapon_usage": {
                    "sword": 0,
                    "axe": 0,
                    "lance": 0,
                    "rapier": 0,
                    "sai": 0
                },
                "weapon_time": {
                    "sword": 0,
                    "axe": 0,
                    "lance": 0,
                    "rapier": 0,
                    "sai": 0
                },
                "favorite_weapon": "sword",
                "favorite_magic": "flame"
            }
        }
        
        # Carregar estatísticas existentes
        self.load_stats()
    
    def load_stats(self):
        """Carrega estatísticas do arquivo JSON"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    loaded_stats = json.load(f)
                    # Mesclar com estatísticas padrão para garantir todas as chaves
                    self._merge_stats(loaded_stats)
                    print(f"✅ Estatísticas carregadas para {self.stats['player_name']}")
            except Exception as e:
                print(f"❌ Erro ao carregar estatísticas: {e}")
                self.save_stats()  # Salvar com dados padrão
    
    def _merge_stats(self, loaded_stats):
        """Mescla estatísticas carregadas com padrão"""
        def merge_dict(default, loaded):
            for key, value in loaded.items():
                if key in default:
                    if isinstance(value, dict) and isinstance(default[key], dict):
                        merge_dict(default[key], value)
                    else:
                        default[key] = value
        
        merge_dict(self.stats, loaded_stats)
    
    def save_stats(self):
        """Salva estatísticas no arquivo JSON"""
        try:
            # Atualizar tempo de sessão
            self.stats["last_played"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
            print("💾 Estatísticas salvas com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao salvar estatísticas: {e}")
    
    def set_player_name(self, name: str):
        """Define o nome do jogador"""
        if not self.stats["player_name"]:  # Só define se ainda não tiver nome
            self.stats["player_name"] = name
            self.stats["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_stats()
    
    def start_session(self):
        """Inicia uma nova sessão de jogo"""
        self.session_start_time = time.time()
        self.stats["game_sessions"] += 1
        print(f"🎮 Sessão iniciada para {self.stats['player_name']}")
    
    def end_session(self):
        """Finaliza a sessão atual"""
        session_time = time.time() - self.session_start_time
        self.stats["total_playtime"] += int(session_time)
        self.save_stats()
        print(f"⏰ Sessão finalizada: {int(session_time)}s")
    
    def start_level(self, level_num: int):
        """Inicia o cronômetro para uma fase"""
        self.level_start_time = time.time()
        self.current_level = level_num
        self.stats["current_level"] = level_num
        self.stats["performance"]["attempts_per_level"][f"level{level_num}"] += 1
        print(f"🏁 Fase {level_num} iniciada")
    
    def complete_level(self, level_num: int):
        """Completa uma fase e registra o tempo"""
        if self.level_start_time:
            level_time = time.time() - self.level_start_time
            level_key = f"level{level_num}"
            
            # Registrar melhor tempo
            if (self.stats["performance"]["best_times"][level_key] is None or 
                level_time < self.stats["performance"]["best_times"][level_key]):
                self.stats["performance"]["best_times"][level_key] = level_time
                print(f"🏆 Novo recorde na Fase {level_num}: {int(level_time)}s")
            
            # Adicionar à lista de fases completadas
            if level_num not in self.stats["levels_completed"]:
                self.stats["levels_completed"].append(level_num)
                print(f"✅ Fase {level_num} completada pela primeira vez!")
            
            self.level_start_time = None
            self.save_stats()
    
    # Métodos para registrar eventos de combate
    def record_enemy_kill(self, enemy_type: str):
        """Registra morte de inimigo"""
        self.stats["combat_stats"]["enemies_killed"] += 1
        if enemy_type in self.stats["combat_stats"]["enemies_by_type"]:
            self.stats["combat_stats"]["enemies_by_type"][enemy_type] += 1
    
    def record_damage_dealt(self, damage: int):
        """Registra dano causado"""
        self.stats["combat_stats"]["damage_dealt"] += damage
    
    def record_damage_taken(self, damage: int):
        """Registra dano recebido"""
        self.stats["combat_stats"]["damage_taken"] += damage
    
    def record_death(self):
        """Registra morte do jogador"""
        self.stats["combat_stats"]["deaths"] += 1
        print(f"💀 Mortes: {self.stats['combat_stats']['deaths']}")
    
    def record_attack(self, weapon: str):
        """Registra ataque realizado"""
        self.stats["combat_stats"]["attacks_made"] += 1
        if weapon in self.stats["equipment_stats"]["weapon_usage"]:
            self.stats["equipment_stats"]["weapon_usage"][weapon] += 1
    
    def record_magic_cast(self, magic_type: str):
        """Registra magia lançada"""
        self.stats["combat_stats"]["magic_cast"] += 1
        if magic_type in self.stats["combat_stats"]["magic_by_type"]:
            self.stats["combat_stats"]["magic_by_type"][magic_type] += 1
    
    # Métodos para registrar coleta de itens
    def record_orb_collection(self, orb_type: str):
        """Registra coleta de orb"""
        if orb_type in self.stats["collection_stats"]:
            self.stats["collection_stats"][orb_type] += 1
    
    def record_key_found(self):
        """Registra chave encontrada"""
        self.stats["collection_stats"]["keys_found"] += 1
    
    def record_gem_collected(self):
        """Registra gema coletada"""
        self.stats["collection_stats"]["eldritch_gems"] += 1
    
    # Métodos para registrar movimento
    def record_movement(self, distance: float):
        """Registra movimentação"""
        self.stats["performance"]["steps_taken"] += 1
        self.stats["performance"]["distance_traveled"] += distance
    
    def get_formatted_stats(self) -> Dict:
        """Retorna estatísticas formatadas para exibição"""
        playtime_str = str(timedelta(seconds=self.stats["total_playtime"]))
        
        return {
            "Jogador": self.stats["player_name"],
            "Tempo Total": playtime_str,
            "Sessões": self.stats["game_sessions"],
            "Fase Atual": self.stats["current_level"],
            "Fases Completadas": len(self.stats["levels_completed"]),
            "Inimigos Derrotados": self.stats["combat_stats"]["enemies_killed"],
            "Mortes": self.stats["combat_stats"]["deaths"],
            "Orbs Coletados": sum(self.stats["collection_stats"].values()),
            "Arma Favorita": self._get_favorite_weapon(),
            "Melhor Tempo": self._get_best_overall_time()
        }
    
    def _get_favorite_weapon(self) -> str:
        """Retorna a arma mais usada"""
        weapon_usage = self.stats["equipment_stats"]["weapon_usage"]
        return max(weapon_usage.items(), key=lambda x: x[1])[0] if any(weapon_usage.values()) else "sword"
    
    def _get_best_overall_time(self) -> str:
        """Retorna o melhor tempo geral"""
        best_times = self.stats["performance"]["best_times"]
        valid_times = [t for t in best_times.values() if t is not None]
        if valid_times:
            return f"{int(min(valid_times))}s"
        return "N/A"
    
    def check_achievements(self) -> List[str]:
        """Verifica e retorna conquistas desbloqueadas"""
        achievements = []
        stats = self.stats
        
        # Conquistas básicas de progressão
        if len(stats["levels_completed"]) >= 1:
            achievements.append("🏁 Primeiro Passo")
        if len(stats["levels_completed"]) >= 2:
            achievements.append("🚀 Em Movimento")
        if len(stats["levels_completed"]) >= 3:
            achievements.append("💪 Quase Lá")
        if len(stats["levels_completed"]) >= 4:
            achievements.append("🏆 Campeão")
        
        # Conquistas de sobrevivência
        if stats["combat_stats"]["deaths"] == 0 and len(stats["levels_completed"]) >= 1:
            achievements.append("🛡️ Invencível")
        if stats["combat_stats"]["deaths"] == 0 and len(stats["levels_completed"]) >= 4:
            achievements.append("💀 Imortal")
        
        # Conquistas de combate
        if stats["combat_stats"]["enemies_killed"] >= 10:
            achievements.append("⚔️ Caçador")
        if stats["combat_stats"]["enemies_killed"] >= 50:
            achievements.append("🗡️ Guerreiro")
        if stats["combat_stats"]["enemies_killed"] >= 100:
            achievements.append("⚡ Devastador")
        if stats["combat_stats"]["enemies_killed"] >= 200:
            achievements.append("🔥 Lenda")
        
        # Conquistas de coleta
        total_orbs = sum(stats["collection_stats"].values())
        if total_orbs >= 10:
            achievements.append("💎 Coletor")
        if total_orbs >= 25:
            achievements.append("🔮 Colecionador")
        if total_orbs >= 50:
            achievements.append("💰 Tesouro")
        if total_orbs >= 100:
            achievements.append("👑 Rei dos Orbs")
        
        # Conquistas de tempo
        if stats["total_playtime"] >= 1800:  # 30 minutos
            achievements.append("⏰ Dedicado")
        if stats["total_playtime"] >= 3600:  # 1 hora
            achievements.append("🕐 Persistente")
        if stats["total_playtime"] >= 7200:  # 2 horas
            achievements.append("⌚ Veterano")
        
        # Conquistas especiais de performance
        best_times = stats["performance"]["best_times"]
        if any(t for t in best_times.values() if t is not None and t < 120):  # Menos de 2 minutos
            achievements.append("🚄 Velocista")
        if any(t for t in best_times.values() if t is not None and t < 60):   # Menos de 1 minuto
            achievements.append("💨 Relâmpago")
        
        # Conquistas de dano
        if stats["combat_stats"]["damage_dealt"] >= 1000:
            achievements.append("💥 Destruidor")
        if stats["combat_stats"]["damage_dealt"] >= 5000:
            achievements.append("🌪️ Tempestade")
        
        # Conquistas de magia
        total_magic = sum(stats["combat_stats"]["magic_by_type"].values())
        if total_magic >= 20:
            achievements.append("🔮 Mago Novato")
        if total_magic >= 50:
            achievements.append("✨ Feiticeiro")
        if total_magic >= 100:
            achievements.append("🌟 Arcano")
        
        # Conquistas de sessões
        if stats["game_sessions"] >= 5:
            achievements.append("🔄 Habitual")
        if stats["game_sessions"] >= 10:
            achievements.append("📅 Frequente")
        
        # Conquistas específicas por tipo de inimigo
        enemies_by_type = stats["combat_stats"]["enemies_by_type"]
        if enemies_by_type["golu"] >= 20:
            achievements.append("🐉 Caçador de Golus")
        if enemies_by_type["black"] >= 15:
            achievements.append("🖤 Sombras Vencidas")
        if enemies_by_type["bigboi"] >= 5:
            achievements.append("👹 Gigante Slayer")
        
        # Conquista especial de coleta por tipo
        if stats["collection_stats"]["health_orbs"] >= 20:
            achievements.append("❤️ Curandeiro")
        if stats["collection_stats"]["attack_orbs"] >= 20:
            achievements.append("💪 Berserker")
        if stats["collection_stats"]["speed_orbs"] >= 20:
            achievements.append("💨 Corredor")
        
        return achievements
    
    def get_achievement_description(self, achievement_name: str) -> str:
        """Retorna descrição de uma conquista"""
        descriptions = {
            "🏁 Primeiro Passo": "Complete a primeira fase",
            "🚀 Em Movimento": "Complete duas fases",
            "💪 Quase Lá": "Complete três fases",
            "🏆 Campeão": "Complete todas as fases",
            "🛡️ Invencível": "Complete uma fase sem morrer",
            "💀 Imortal": "Complete o jogo sem morrer",
            "⚔️ Caçador": "Derrote 10 inimigos",
            "🗡️ Guerreiro": "Derrote 50 inimigos",
            "⚡ Devastador": "Derrote 100 inimigos",
            "🔥 Lenda": "Derrote 200 inimigos",
            "💎 Coletor": "Colete 10 orbs",
            "🔮 Colecionador": "Colete 25 orbs",
            "💰 Tesouro": "Colete 50 orbs",
            "👑 Rei dos Orbs": "Colete 100 orbs",
            "⏰ Dedicado": "Jogue por 30 minutos",
            "🕐 Persistente": "Jogue por 1 hora",
            "⌚ Veterano": "Jogue por 2 horas",
            "🚄 Velocista": "Complete uma fase em menos de 2 minutos",
            "💨 Relâmpago": "Complete uma fase em menos de 1 minuto",
            "💥 Destruidor": "Cause 1000 de dano",
            "🌪️ Tempestade": "Cause 5000 de dano",
            "🔮 Mago Novato": "Lance 20 magias",
            "✨ Feiticeiro": "Lance 50 magias",
            "🌟 Arcano": "Lance 100 magias",
            "🔄 Habitual": "Jogue 5 sessões",
            "📅 Frequente": "Jogue 10 sessões",
            "🐉 Caçador de Golus": "Derrote 20 Golus",
            "🖤 Sombras Vencidas": "Derrote 15 Blacks",
            "👹 Gigante Slayer": "Derrote 5 Bigbois",
            "❤️ Curandeiro": "Colete 20 Health Orbs",
            "💪 Berserker": "Colete 20 Attack Orbs",
            "💨 Corredor": "Colete 20 Speed Orbs"
        }
        return descriptions.get(achievement_name, "Conquista especial")
    
    def print_stats(self):
        """Imprime estatísticas no console"""
        print("\n" + "="*50)
        print(f"📊 ESTATÍSTICAS DE {self.stats['player_name'].upper()}")
        print("="*50)
        
        formatted = self.get_formatted_stats()
        for key, value in formatted.items():
            print(f"{key:20}: {value}")
        
        print("="*50)

# Instância singleton
player_stats = PlayerStats()