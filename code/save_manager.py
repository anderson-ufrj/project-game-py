import json
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional, List

class SaveManager:
    """Gerencia sistema de save/load do jogo"""
    
    def __init__(self):
        self.saves_directory = "saves"
        self.max_save_slots = 5
        self.current_save_slot = None
        
        # Criar diretório de saves se não existir
        if not os.path.exists(self.saves_directory):
            os.makedirs(self.saves_directory)
            print(f"📁 Diretório de saves criado: {self.saves_directory}")
    
    def get_save_file_path(self, slot: int) -> str:
        """Retorna o caminho do arquivo de save para um slot"""
        return os.path.join(self.saves_directory, f"save_slot_{slot}.json")
    
    def create_save_data(self, game_instance) -> Dict[str, Any]:
        """Cria dados de save a partir do estado atual do jogo"""
        save_data = {
            "metadata": {
                "save_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "game_version": "1.0.0",
                "player_name": getattr(game_instance, 'player_name', 'Jogador'),
                "save_slot": self.current_save_slot
            },
            "game_state": {
                "current_level": game_instance.game_state,
                "current_difficulty": self._get_difficulty()
            },
            "player_progress": {
                "levels_completed": self._get_completed_levels(),
                "current_level_progress": self._get_current_level_progress(game_instance)
            },
            "player_stats": self._get_player_stats_data(),
            "inventory": self._get_player_inventory(game_instance),
            "settings": {
                "audio_volume": self._get_audio_volume(),
                "difficulty": self._get_difficulty()
            }
        }
        return save_data
    
    def save_game(self, game_instance, slot: int, save_name: str = None) -> bool:
        """Salva o jogo em um slot específico"""
        try:
            self.current_save_slot = slot
            save_data = self.create_save_data(game_instance)
            
            # Adicionar nome personalizado do save
            if save_name:
                save_data["metadata"]["save_name"] = save_name
            else:
                level_names = {
                    0: "Menu Principal", 3: "Floresta", 4: "Labirinto", 
                    5: "Fortaleza", 6: "Fase Final"
                }
                current_level_name = level_names.get(game_instance.game_state, "Desconhecido")
                save_data["metadata"]["save_name"] = f"Save {slot} - {current_level_name}"
            
            # Salvar arquivo
            save_file = self.get_save_file_path(slot)
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Jogo salvo no slot {slot}: {save_data['metadata']['save_name']}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar jogo: {e}")
            return False
    
    def load_game(self, slot: int) -> Optional[Dict[str, Any]]:
        """Carrega o jogo de um slot específico"""
        try:
            save_file = self.get_save_file_path(slot)
            if not os.path.exists(save_file):
                print(f"❌ Save slot {slot} não existe")
                return None
            
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            print(f"📂 Jogo carregado do slot {slot}: {save_data['metadata']['save_name']}")
            self.current_save_slot = slot
            return save_data
            
        except Exception as e:
            print(f"❌ Erro ao carregar jogo: {e}")
            return None
    
    def apply_save_data(self, game_instance, save_data: Dict[str, Any]) -> bool:
        """Aplica dados carregados ao jogo"""
        try:
            # Aplicar estado do jogo
            game_state = save_data["game_state"]["current_level"]
            game_instance.game_state = game_state
            
            # Aplicar dificuldade
            if "difficulty" in save_data["settings"]:
                from difficulty_manager import difficulty_manager
                difficulty_manager.set_difficulty(save_data["settings"]["difficulty"])
            
            # Aplicar estatísticas do jogador
            if "player_stats" in save_data:
                from player_stats import player_stats
                player_stats.stats.update(save_data["player_stats"])
            
            # Aplicar configurações de áudio
            if "audio_volume" in save_data["settings"]:
                from audio_manager import audio_manager
                audio_manager.set_volume(save_data["settings"]["audio_volume"])
            
            print(f"✅ Dados do save aplicados com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao aplicar dados do save: {e}")
            return False
    
    def delete_save(self, slot: int) -> bool:
        """Deleta um save específico"""
        try:
            save_file = self.get_save_file_path(slot)
            if os.path.exists(save_file):
                os.remove(save_file)
                print(f"🗑️ Save slot {slot} deletado")
                return True
            else:
                print(f"❌ Save slot {slot} não existe")
                return False
        except Exception as e:
            print(f"❌ Erro ao deletar save: {e}")
            return False
    
    def get_save_info(self, slot: int) -> Optional[Dict[str, Any]]:
        """Retorna informações sobre um save sem carregá-lo completamente"""
        try:
            save_file = self.get_save_file_path(slot)
            if not os.path.exists(save_file):
                return None
            
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Extrair apenas metadados e informações básicas
            info = {
                "slot": slot,
                "save_name": save_data["metadata"].get("save_name", f"Save {slot}"),
                "save_time": save_data["metadata"]["save_time"],
                "player_name": save_data["metadata"].get("player_name", "Jogador"),
                "current_level": save_data["game_state"]["current_level"],
                "difficulty": save_data["settings"].get("difficulty", "normal"),
                "levels_completed": len(save_data["player_progress"]["levels_completed"]),
                "play_time": save_data["player_stats"].get("total_playtime", 0)
            }
            
            return info
            
        except Exception as e:
            print(f"❌ Erro ao obter info do save {slot}: {e}")
            return None
    
    def get_all_saves_info(self) -> List[Dict[str, Any]]:
        """Retorna informações de todos os saves disponíveis"""
        saves_info = []
        
        for slot in range(1, self.max_save_slots + 1):
            save_info = self.get_save_info(slot)
            if save_info:
                saves_info.append(save_info)
            else:
                # Slot vazio
                saves_info.append({
                    "slot": slot,
                    "save_name": f"Slot {slot} - Vazio",
                    "save_time": None,
                    "player_name": None,
                    "current_level": None,
                    "difficulty": None,
                    "levels_completed": 0,
                    "play_time": 0,
                    "is_empty": True
                })
        
        return saves_info
    
    def quick_save(self, game_instance) -> bool:
        """Save rápido no último slot usado ou slot 1"""
        slot = self.current_save_slot if self.current_save_slot else 1
        return self.save_game(game_instance, slot, f"Quick Save - {datetime.now().strftime('%H:%M')}")
    
    def auto_save(self, game_instance) -> bool:
        """Auto save em slot dedicado (slot 0)"""
        return self.save_game(game_instance, 0, f"Auto Save - {datetime.now().strftime('%H:%M:%S')}")
    
    # Métodos auxiliares para extrair dados do jogo
    def _get_difficulty(self) -> str:
        """Obtém dificuldade atual"""
        try:
            from difficulty_manager import difficulty_manager
            return difficulty_manager.get_current_difficulty()
        except:
            return "normal"
    
    def _get_completed_levels(self) -> List[int]:
        """Obtém níveis completados"""
        try:
            from player_stats import player_stats
            return player_stats.stats.get("levels_completed", [])
        except:
            return []
    
    def _get_current_level_progress(self, game_instance) -> Dict[str, Any]:
        """Obtém progresso do nível atual"""
        try:
            progress = {
                "game_state": game_instance.game_state,
                "timestamp": time.time()
            }
            
            # Adicionar dados específicos do nível se disponível
            if hasattr(game_instance, 'level1') and game_instance.game_state == 3:
                if hasattr(game_instance.level1, 'player'):
                    player = game_instance.level1.player
                    progress["player_data"] = {
                        "health": player.health,
                        "energy": player.energy,
                        "inventory": player.inventory,
                        "weapon": player.weapon,
                        "magic": player.magic
                    }
            
            return progress
        except:
            return {"game_state": game_instance.game_state, "timestamp": time.time()}
    
    def _get_player_stats_data(self) -> Dict[str, Any]:
        """Obtém dados de estatísticas do jogador"""
        try:
            from player_stats import player_stats
            return player_stats.stats.copy()
        except:
            return {}
    
    def _get_player_inventory(self, game_instance) -> Dict[str, Any]:
        """Obtém inventário do jogador"""
        try:
            # Tentar obter inventário do nível atual
            if hasattr(game_instance, 'level1') and game_instance.game_state == 3:
                if hasattr(game_instance.level1, 'player'):
                    return game_instance.level1.player.inventory.copy()
            elif hasattr(game_instance, 'level2') and game_instance.game_state == 4:
                if hasattr(game_instance.level2, 'player'):
                    return game_instance.level2.player.inventory.copy()
            elif hasattr(game_instance, 'level3') and game_instance.game_state == 5:
                if hasattr(game_instance.level3, 'player'):
                    return game_instance.level3.player.inventory.copy()
            elif hasattr(game_instance, 'level4') and game_instance.game_state == 6:
                if hasattr(game_instance.level4, 'player'):
                    return game_instance.level4.player.inventory.copy()
            
            # Inventário padrão se não conseguir obter
            return {'healthOrbs': 0, 'attackOrbs': 0, 'speedOrbs': 0, 'keys': 0, 'zappaguriStone': 0}
        except:
            return {'healthOrbs': 0, 'attackOrbs': 0, 'speedOrbs': 0, 'keys': 0, 'zappaguriStone': 0}
    
    def _get_audio_volume(self) -> float:
        """Obtém volume do áudio"""
        try:
            from audio_manager import audio_manager
            return audio_manager.volume
        except:
            return 0.5

# Instância singleton
save_manager = SaveManager()