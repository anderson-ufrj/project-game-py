"""
Gerenciador Principal do Jogo Modernizado
Substitui o main.py antigo com UI moderna e efeitos
"""
import pygame
import sys
from typing import Optional, Dict, Any
from enum import Enum

# Imports do sistema antigo
from settings import WIDTH, HEIGTH
from level import Level1
from level2 import Level2
from level3 import Level3
from level4 import Level4
from audio_manager import audio_manager
from player_stats import player_stats
from save_manager import save_manager
from difficulty_manager import difficulty_manager

# Imports do sistema moderno
from modern_ui_system import modern_ui, UITheme
from modern_main_menu import ModernMainMenu
from modern_settings_screen import ModernSettingsScreen
from modern_hud import modern_hud
from transition_manager import transition_manager, TransitionType
from story_screen import StoryScreen

class GameState(Enum):
    MAIN_MENU = "main_menu"
    LOADING = "loading"
    STORY = "story"
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"
    LEVEL_4 = "level_4"
    GAME_OVER = "game_over"
    SETTINGS = "settings"
    PAUSE = "pause"

class ModernGameManager:
    """Gerenciador principal do jogo com UI moderna"""
    
    def __init__(self):
        # Inicialização do Pygame
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        
        # Tela
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.SCALED)
        pygame.display.set_caption('CORRIDA PELA RELÍQUIA - EDIÇÃO MODERNA')
        
        # Clock
        self.clock = pygame.time.Clock()
        self.fps_target = 60
        self.fps_current = 60.0
        
        # Estado do jogo
        self.current_state = GameState.MAIN_MENU
        self.previous_state = None
        self.running = True
        
        # Sistemas modernos
        self.main_menu = ModernMainMenu()
        self.settings_screen = ModernSettingsScreen()
        
        # Fases do jogo (mantendo compatibilidade)
        self.levels = {
            GameState.LEVEL_1: Level1(),
            GameState.LEVEL_2: Level2(),
            GameState.LEVEL_3: Level3(),
            GameState.LEVEL_4: Level4()
        }
        
        # Estado das histórias
        self.story_flags = {
            "intro_shown": False,
            "level1_story_shown": False,
            "level2_story_shown": False,
            "level3_story_shown": False,
            "level4_story_shown": False
        }
        
        # Cache de superfícies para transições
        self.surface_cache = {}
        
        # Configurações de qualidade
        self.visual_quality = "alta"  # baixa, média, alta, ultra
        self.particles_enabled = True
        self.shadows_enabled = True
        
        # Inicialização dos sistemas
        self.initialize_systems()
        
        print("🎮 Game Manager Moderno inicializado!")
    
    def initialize_systems(self):
        """Inicializa todos os sistemas do jogo"""
        # Áudio
        audio_manager.play_music('../audio/home.mp3')
        
        # Estatísticas
        player_stats.start_session()
        
        # Tema inicial
        modern_ui.set_theme(UITheme.DARK)
        
        # Configurar qualidade visual inicial
        self.update_visual_quality()
        
        # Notificação de boas-vindas
        modern_ui.create_notification("Bem-vindo ao jogo modernizado!", "success", 4.0)
    
    def update_visual_quality(self):
        """Atualiza configurações de qualidade visual"""
        quality_settings = {
            "baixa": {
                "particles": False,
                "shadows": False,
                "fps_target": 30,
                "ui_effects": False
            },
            "média": {
                "particles": True,
                "shadows": False,
                "fps_target": 45,
                "ui_effects": True
            },
            "alta": {
                "particles": True,
                "shadows": True,
                "fps_target": 60,
                "ui_effects": True
            },
            "ultra": {
                "particles": True,
                "shadows": True,
                "fps_target": 120,
                "ui_effects": True
            }
        }
        
        settings = quality_settings.get(self.visual_quality, quality_settings["alta"])
        
        self.particles_enabled = settings["particles"]
        self.shadows_enabled = settings["shadows"]
        self.fps_target = settings["fps_target"]
        modern_ui.animations_enabled = settings["ui_effects"]
    
    def handle_events(self):
        """Processa eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
                return
            
            # Eventos globais
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_F1:
                    self.cycle_ui_theme()
                elif event.key == pygame.K_F2:
                    self.cycle_visual_quality()
                elif event.key == pygame.K_ESCAPE:
                    self.handle_escape()
            
            # Eventos do sistema de UI moderno
            modern_ui.process_event(event)
            
            # Eventos específicos do estado
            self.handle_state_events(event)
    
    def handle_state_events(self, event: pygame.event.Event):
        """Processa eventos específicos do estado atual"""
        if self.current_state == GameState.MAIN_MENU:
            result = self.main_menu.handle_event(event)
            if result:
                self.handle_menu_action(result)
        
        elif self.current_state == GameState.SETTINGS:
            # Settings screen já processa eventos internamente
            pass
        
        elif self.current_state in self.levels:
            # Repassar eventos para as fases
            if not transition_manager.is_active():
                # Só processar se não estiver em transição
                pygame.event.post(event)
    
    def handle_menu_action(self, action: str):
        """Processa ações do menu principal"""
        if action == "new_game":
            self.start_new_game()
        elif action == "continue":
            self.continue_game()
        elif action == "settings":
            self.open_settings()
        elif action == "quit":
            self.quit_game()
    
    def handle_escape(self):
        """Processa tecla ESC baseada no estado"""
        if self.current_state == GameState.SETTINGS:
            self.close_settings()
        elif self.current_state in self.levels:
            self.pause_game()
        elif self.current_state == GameState.PAUSE:
            self.resume_game()
    
    def toggle_fullscreen(self):
        """Alterna entre fullscreen e janela"""
        flags = self.screen.get_flags()
        if flags & pygame.FULLSCREEN:
            self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.SCALED)
            modern_ui.create_notification("Modo janela ativado", "info")
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.FULLSCREEN | pygame.SCALED)
            modern_ui.create_notification("Tela cheia ativada", "info")
    
    def cycle_ui_theme(self):
        """Alterna entre temas da UI"""
        themes = [UITheme.DARK, UITheme.LIGHT, UITheme.CYBERPUNK, UITheme.FANTASY]
        current_index = themes.index(modern_ui.current_theme)
        next_theme = themes[(current_index + 1) % len(themes)]
        
        modern_ui.set_theme(next_theme)
        modern_ui.create_notification(f"Tema: {next_theme.value}", "info")
    
    def cycle_visual_quality(self):
        """Alterna qualidade visual"""
        qualities = ["baixa", "média", "alta", "ultra"]
        current_index = qualities.index(self.visual_quality)
        self.visual_quality = qualities[(current_index + 1) % len(qualities)]
        
        self.update_visual_quality()
        modern_ui.create_notification(f"Qualidade: {self.visual_quality}", "info")
    
    def start_new_game(self):
        """Inicia um novo jogo"""
        # Reset de todos os sistemas
        self.reset_game_state()
        
        # Transição para história introdutória
        transition_manager.start_transition(
            TransitionType.FADE,
            duration=1.0,
            on_complete=lambda: self.show_story("intro")
        )
    
    def continue_game(self):
        """Continua um jogo salvo"""
        # TODO: Implementar carregamento de save
        modern_ui.create_notification("Funcionalidade em desenvolvimento", "warning")
    
    def open_settings(self):
        """Abre a tela de configurações"""
        self.previous_state = self.current_state
        self.current_state = GameState.SETTINGS
        self.settings_screen.open()
        
        transition_manager.start_transition(TransitionType.SLIDE_UP, duration=0.5)
    
    def close_settings(self):
        """Fecha a tela de configurações"""
        self.settings_screen.close()
        self.current_state = self.previous_state or GameState.MAIN_MENU
        
        transition_manager.start_transition(TransitionType.SLIDE_DOWN, duration=0.5)
    
    def pause_game(self):
        """Pausa o jogo"""
        if self.current_state in self.levels:
            self.previous_state = self.current_state
            self.current_state = GameState.PAUSE
            modern_ui.create_notification("Jogo pausado", "info")
    
    def resume_game(self):
        """Resume o jogo"""
        if self.current_state == GameState.PAUSE:
            self.current_state = self.previous_state or GameState.LEVEL_1
            modern_ui.create_notification("Jogo resumido", "success")
    
    def reset_game_state(self):
        """Reset completo do estado do jogo"""
        # Reset das fases
        for level in self.levels.values():
            level.reset()
        
        # Reset das flags de história
        for key in self.story_flags:
            self.story_flags[key] = False
        
        # Reset das estatísticas
        player_stats.start_session()
        
        print("🔄 Estado do jogo resetado")
    
    def show_story(self, story_key: str):
        """Mostra uma história específica"""
        self.current_state = GameState.STORY
        
        # Determinar background baseado na história
        backgrounds = {
            "intro": "../graphics/ui/home page.jpg",
            "phase_1": "../map new/map.png",
            "phase_2": "../map new/maze1.png",
            "phase_3": "../map new/dungeon.png",
            "phase_4": "../map new/final.png",
            "victory": "../graphics/ui/home page.jpg"
        }
        
        background = backgrounds.get(story_key, "../graphics/ui/home page.jpg")
        
        # Criar e executar história
        story = StoryScreen(story_key, custom_background=background)
        
        # Loop da história
        story_running = True
        while story_running and self.running:
            dt = self.clock.tick(60) / 1000.0
            
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE]:
                        story_running = False
            
            # Atualizar e desenhar história
            story_finished = story.update()
            if story_finished:
                story_running = False
        
        # Determinar próximo estado após história
        self.handle_story_completion(story_key)
    
    def handle_story_completion(self, story_key: str):
        """Processa o que acontece após uma história"""
        if story_key == "intro":
            self.story_flags["intro_shown"] = True
            self.transition_to_level(GameState.LEVEL_1)
        elif story_key == "phase_1":
            self.story_flags["level1_story_shown"] = True
            self.current_state = GameState.LEVEL_1
        elif story_key == "phase_2":
            self.story_flags["level2_story_shown"] = True
            self.current_state = GameState.LEVEL_2
        elif story_key == "phase_3":
            self.story_flags["level3_story_shown"] = True
            self.current_state = GameState.LEVEL_3
        elif story_key == "phase_4":
            self.story_flags["level4_story_shown"] = True
            self.current_state = GameState.LEVEL_4
        elif story_key == "victory":
            self.transition_to_main_menu()
    
    def transition_to_level(self, level_state: GameState):
        """Transição para uma fase específica"""
        transition_manager.start_transition(
            TransitionType.CIRCLE_EXPAND,
            duration=1.5,
            on_complete=lambda: self.enter_level(level_state)
        )
    
    def enter_level(self, level_state: GameState):
        """Entra em uma fase específica"""
        self.current_state = level_state
        
        # Mostrar história se necessário
        story_map = {
            GameState.LEVEL_1: ("phase_1", "level1_story_shown"),
            GameState.LEVEL_2: ("phase_2", "level2_story_shown"),
            GameState.LEVEL_3: ("phase_3", "level3_story_shown"),
            GameState.LEVEL_4: ("phase_4", "level4_story_shown")
        }
        
        if level_state in story_map:
            story_key, flag_key = story_map[level_state]
            if not self.story_flags[flag_key]:
                self.show_story(story_key)
        
        # Configurar áudio da fase
        audio_map = {
            GameState.LEVEL_1: '../audio/Ambient 2.mp3',
            GameState.LEVEL_2: '../audio/Ambient 2.mp3',
            GameState.LEVEL_3: '../audio/darkambience(from fable).mp3',
            GameState.LEVEL_4: '../audio/home.mp3'
        }
        
        if level_state in audio_map:
            audio_manager.play_music(audio_map[level_state])\n    \n    def transition_to_main_menu(self):\n        \"\"\"Transição de volta ao menu principal\"\"\"\n        transition_manager.start_transition(\n            TransitionType.FADE,\n            duration=2.0,\n            on_complete=lambda: setattr(self, 'current_state', GameState.MAIN_MENU)\n        )\n        audio_manager.play_music('../audio/home.mp3')\n    \n    def quit_game(self):\n        \"\"\"Encerra o jogo\"\"\"\n        modern_ui.create_notification(\"Encerrando jogo...\", \"info\", 1.0)\n        player_stats.end_session()\n        \n        # Pequeno delay para mostrar notificação\n        pygame.time.wait(500)\n        \n        self.running = False\n        pygame.quit()\n        sys.exit()\n    \n    def update(self):\n        \"\"\"Atualiza o jogo baseado no estado atual\"\"\"\n        dt = self.clock.get_time() / 1000.0\n        \n        # Atualizar FPS\n        self.fps_current = self.clock.get_fps()\n        \n        # Atualizar sistemas universais\n        modern_ui.update(dt)\n        transition_manager.update(dt)\n        \n        # Atualizar baseado no estado\n        if self.current_state == GameState.MAIN_MENU:\n            self.main_menu.update(dt)\n        \n        elif self.current_state == GameState.SETTINGS:\n            self.settings_screen.update(dt)\n        \n        elif self.current_state in self.levels:\n            level = self.levels[self.current_state]\n            \n            # Só atualizar se não estiver em transição\n            if not transition_manager.is_active():\n                level.run()\n                modern_hud.update(dt)\n                \n                # Verificar condições de vitória/derrota\n                self.check_level_conditions(level)\n        \n        elif self.current_state == GameState.PAUSE:\n            # Jogo pausado - não atualizar gameplay\n            pass\n    \n    def check_level_conditions(self, level):\n        \"\"\"Verifica condições de vitória/derrota da fase\"\"\"\n        if hasattr(level, 'completed') and level.completed:\n            self.handle_level_completion()\n        \n        elif hasattr(level, 'gameover') and level.gameover:\n            self.handle_game_over()\n    \n    def handle_level_completion(self):\n        \"\"\"Processa conclusão de uma fase\"\"\"\n        current_level_num = {\n            GameState.LEVEL_1: 1,\n            GameState.LEVEL_2: 2,\n            GameState.LEVEL_3: 3,\n            GameState.LEVEL_4: 4\n        }.get(self.current_state, 1)\n        \n        # Registrar estatísticas\n        player_stats.complete_level(current_level_num)\n        \n        # Auto-save\n        save_manager.auto_save(self)\n        \n        # Determinar próxima fase\n        next_states = {\n            GameState.LEVEL_1: GameState.LEVEL_2,\n            GameState.LEVEL_2: GameState.LEVEL_3,\n            GameState.LEVEL_3: GameState.LEVEL_4,\n            GameState.LEVEL_4: None  # Fim do jogo\n        }\n        \n        next_state = next_states.get(self.current_state)\n        \n        if next_state:\n            modern_ui.create_notification(f\"Fase {current_level_num} completa!\", \"success\", 3.0)\n            self.transition_to_level(next_state)\n        else:\n            # Fim do jogo - mostrar história de vitória\n            modern_ui.create_notification(\"Jogo completo!\", \"success\", 4.0)\n            player_stats.complete_game()\n            self.show_story(\"victory\")\n    \n    def handle_game_over(self):\n        \"\"\"Processa game over\"\"\"\n        player_stats.record_death()\n        modern_ui.create_notification(\"Game Over\", \"error\", 3.0)\n        \n        # Transição para menu principal\n        transition_manager.start_transition(\n            TransitionType.FADE,\n            duration=2.0,\n            on_complete=lambda: self.transition_to_main_menu()\n        )\n    \n    def draw(self):\n        \"\"\"Desenha o jogo baseado no estado atual\"\"\"\n        # Limpar tela\n        self.screen.fill((0, 0, 0))\n        \n        # Desenhar baseado no estado\n        if self.current_state == GameState.MAIN_MENU:\n            self.main_menu.draw(self.screen)\n        \n        elif self.current_state == GameState.SETTINGS:\n            # Desenhar menu principal atrás\n            self.main_menu.draw(self.screen)\n            # Desenhar configurações por cima\n            self.settings_screen.draw(self.screen)\n        \n        elif self.current_state in self.levels:\n            level = self.levels[self.current_state]\n            \n            # Desenhar fase\n            level_surface = pygame.Surface((WIDTH, HEIGTH))\n            level.visible_sprites.custom_draw(level.player)\n            \n            # Desenhar HUD moderno\n            if hasattr(level, 'player'):\n                modern_hud.draw_complete_hud(\n                    self.screen,\n                    level.player.health,\n                    level.player.stats['health'],\n                    level.player.energy,\n                    level.player.stats['energy'],\n                    level.player.inventory,\n                    self.get_current_level_number(),\n                    (level.player.rect.centerx, level.player.rect.centery),\n                    getattr(level.ui, 'current_message', \"\"),\n                    self.fps_current\n                )\n        \n        elif self.current_state == GameState.PAUSE:\n            # Desenhar jogo pausado\n            if self.previous_state in self.levels:\n                level = self.levels[self.previous_state]\n                level.visible_sprites.custom_draw(level.player)\n            \n            # Overlay de pausa\n            overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)\n            overlay.fill((0, 0, 0, 180))\n            self.screen.blit(overlay, (0, 0))\n            \n            # Texto de pausa\n            colors = modern_ui.get_current_colors()\n            font = pygame.font.Font(None, 72)\n            pause_text = font.render(\"PAUSADO\", True, colors.text_primary)\n            pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGTH//2))\n            self.screen.blit(pause_text, pause_rect)\n            \n            # Instruções\n            font_small = pygame.font.Font(None, 36)\n            instruction_text = font_small.render(\"Pressione ESC para continuar\", True, colors.text_secondary)\n            instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGTH//2 + 100))\n            self.screen.blit(instruction_text, instruction_rect)\n        \n        # Desenhar transições\n        transition_manager.draw(self.screen)\n        \n        # Desenhar UI moderna (notificações, etc.)\n        modern_ui.draw(self.screen)\n        \n        # Atualizar display\n        pygame.display.flip()\n    \n    def get_current_level_number(self) -> int:\n        \"\"\"Retorna o número da fase atual\"\"\"\n        level_map = {\n            GameState.LEVEL_1: 1,\n            GameState.LEVEL_2: 2,\n            GameState.LEVEL_3: 3,\n            GameState.LEVEL_4: 4\n        }\n        return level_map.get(self.current_state, 1)\n    \n    def run(self):\n        \"\"\"Loop principal do jogo\"\"\"\n        print(\"🚀 Iniciando jogo modernizado...\")\n        \n        while self.running:\n            # Processar eventos\n            self.handle_events()\n            \n            # Atualizar jogo\n            self.update()\n            \n            # Desenhar\n            self.draw()\n            \n            # Controlar FPS\n            self.clock.tick(self.fps_target)\n        \n        print(\"👋 Jogo encerrado!\")\n\nif __name__ == '__main__':\n    game = ModernGameManager()\n    game.run()