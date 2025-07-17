"""
Versão do main.py com a nova interface moderna de áudio unificada
Remove conflitos entre simple_audio_controls e settings_manager
"""
import pygame
import sys
from settings import *
from level import Level1
from level2 import Level2
from level3 import Level3
from level4 import Level4
from pygame.locals import *

from loading import LoadingScreen
from audio_manager import audio_manager
from main_menu import AdvancedMainMenu
from story_screen import StoryScreen
from cheat_system import cheat_system
from player_stats import player_stats
from name_input_screen import NameInputScreenV2
from stats_screen import StatsScreen
from achievements_screen import AchievementsScreen
from difficulty_manager import difficulty_manager
from difficulty_screen import DifficultyScreen
from save_manager import save_manager
from save_screen import SaveScreen
from font_manager import font_manager
from graphics_manager import GraphicsManager

# NOVA INTERFACE MODERNA
from modern_audio_controls import modern_audio_controls

pygame.mixer.pre_init(44100, 16, 2, 4096)


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        
        # Inicializar sistema de gráficos
        self.graphics_manager = GraphicsManager()
        self.graphics_manager.apply_settings()
        self.screen = self.graphics_manager.get_screen()
        
        # Fallback se GraphicsManager falhar
        if self.screen is None:
            self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.SCALED)
        
        pygame.display.set_caption('CORRIDA PELA RELÍQUIA')
        self.clock = pygame.time.Clock()

        self.level1 = Level1()
        self.level2 = Level2()
        self.level3 = Level3()
        self.level4 = Level4()

        # Transition variables
        self.transition_duration = 5000
        self.transition_start_time = 0
        self.transition_alpha = 0

        # Homescreen variables
        self.homescreen_image = pygame.image.load('../graphics/ui/home page.jpg').convert()
        self.homescreen_image = pygame.transform.scale(self.homescreen_image,(1280,720))
        self.gameover_image = pygame.image.load('../graphics/ui/gameover.jpg').convert()
        self.loading = LoadingScreen()
        self.gameover_image_rect = self.gameover_image.get_rect()
        self.homescreen_rect = self.homescreen_image.get_rect()
        
        # STATS: Start with name input if no name is set, otherwise homescreen
        self.game_state = -1 if not player_stats.stats.get("player_name") else 0
        
        # Font for homescreen text
        self.title_font = font_manager.get('title')
        self.subtitle_font = font_manager.get('subtitle')
        self.info_font = font_manager.get('text')

        # Advanced main menu
        fonts = {
            'title': self.title_font,
            'subtitle': self.subtitle_font,
            'info': self.info_font,
            'button': self.info_font
        }
        self.advanced_menu = AdvancedMainMenu(self.screen, fonts)
        
        # STATS: Name input screen and stats screen
        self.name_input_screen = NameInputScreenV2()
        self.stats_screen = StatsScreen()
        self.achievements_screen = AchievementsScreen()
        self.difficulty_screen = DifficultyScreen()
        self.save_screen = None  # Will be initialized when needed
        
        # Use AudioManager for music control
        audio_manager.play_music('../audio/home.mp3')
        
        # STATS: Initialize player stats session
        player_stats.start_session()

    def homescreen(self):
        # Get mouse position and click status
        mouse_pos = pygame.mouse.get_pos()
        
        # Check for mouse clicks in the events
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            elif event.type == pygame.KEYDOWN:
                # CHEAT: Handle cheat codes in menu
                cheat_action = cheat_system.handle_cheat_input(event)
                if cheat_action:
                    self.handle_cheat_action(cheat_action)
                    return
                
                if event.key == pygame.K_RETURN:
                    audio_manager.play_music('../audio/Ambient 2.mp3')
                    self.game_state = 3  # Go to Level 1
                    return
                elif event.key == pygame.K_1:
                    audio_manager.play_music('../audio/Ambient 2.mp3')
                    self.game_state = 3
                    return
                elif event.key == pygame.K_2:
                    audio_manager.play_music('../audio/Ambient 2.mp3')
                    self.game_state = 4
                    return
                elif event.key == pygame.K_3:
                    audio_manager.play_music('../audio/darkambience(from fable).mp3')
                    self.game_state = 5
                    return
                elif event.key == pygame.K_4:
                    audio_manager.play_music('../audio/home.mp3')
                    self.game_state = 6
                    return
                elif event.key == pygame.K_s:
                    self.game_state = 30
                    return
                elif event.key == pygame.K_d:
                    self.game_state = 40
                    return
                elif event.key == pygame.K_l:
                    self.game_state = 50
                    return
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # NOVA INTERFACE: Processa eventos nos controles modernos
            if modern_audio_controls.handle_event(event):
                continue  # Evento foi consumido pelos controles
            
            # Let the advanced menu handle events
            self.advanced_menu.handle_event(event)
            
            # Put back non-consumed events
            if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT]:
                pygame.event.post(event)
        
        # Use the advanced menu system
        menu_action = self.advanced_menu.update_and_draw(mouse_pos, mouse_click)
        
        # Handle menu actions
        if menu_action == "start_game":
            if not hasattr(self, 'intro_story_shown'):
                story = StoryScreen("intro", custom_background="../graphics/ui/home page.jpg")
                story_finished = False
                while not story_finished:
                    story_finished = story.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                self.intro_story_shown = True
            
            audio_manager.play_music('../audio/Ambient 2.mp3')
            self.game_state = 3  # Go to Level 1
        elif menu_action == "quit_game":
            pygame.quit()
            sys.exit()
        
        # NOVA INTERFACE: Desenha controles modernos
        modern_audio_controls.draw(self.screen)
        
        # CHEAT: Display cheat information in menu
        cheat_system.display_cheat_info(self.screen)
    
    def gameover(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                cheat_action = cheat_system.handle_cheat_input(event)
                if cheat_action:
                    self.handle_cheat_action(cheat_action)
                    return
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.game_state = 0  # Return to main menu
                    audio_manager.play_music('../audio/home.mp3')
                    self.reset_game()
                    return
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # NOVA INTERFACE: Processa eventos
            modern_audio_controls.handle_event(event)
        
        self.gameover_image = pygame.transform.scale(self.gameover_image,(1280,720))
        self.screen.blit(self.gameover_image,(0,0))
        
        # NOVA INTERFACE: Desenha controles
        modern_audio_controls.draw(self.screen)
        
        cheat_system.display_cheat_info(self.screen)
        pygame.display.update()

    def reset_game(self):
        self.level1.reset()
        self.level2.reset()
        self.level3.reset()
        self.level4.reset()
        
        # Reset story flags
        if hasattr(self, 'intro_story_shown'):
            del self.intro_story_shown
        if hasattr(self, 'level1_story_shown'):
            del self.level1_story_shown
        if hasattr(self, 'level2_story_shown'):
            del self.level2_story_shown
        if hasattr(self, 'level3_story_shown'):
            del self.level3_story_shown
        if hasattr(self, 'level4_story_shown'):
            del self.level4_story_shown
    
    def handle_cheat_action(self, cheat_action):
        """Handle cheat actions from levels"""
        if cheat_action == "level1":
            audio_manager.play_music('../audio/Ambient 2.mp3')
            self.game_state = 3
        elif cheat_action == "level2":
            audio_manager.play_music('../audio/Ambient 2.mp3')
            self.game_state = 4
        elif cheat_action == "level3":
            audio_manager.play_music('../audio/darkambience(from fable).mp3')
            self.game_state = 5
        elif cheat_action == "level4":
            audio_manager.play_music('../audio/home.mp3')
            self.game_state = 6
        elif cheat_action == "home":
            audio_manager.play_music('../audio/home.mp3')
            self.game_state = 0
            self.reset_game()

    def run(self):
        while True:
            # Calcula delta time para animações
            dt = self.clock.tick(self.graphics_manager.get_fps_limit()) / 1000.0
            
            # Atualiza animações dos controles modernos
            modern_audio_controls.update(dt)
            
            # Handle events based on game state
            if self.game_state == -1:  # Name input screen
                events = pygame.event.get()
                result = self.name_input_screen.handle_events(events)
                if result == 'main_menu':
                    self.game_state = 0  # Go to homescreen
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
            elif self.game_state == 0:  # Homescreen
                pass  # Events are handled inside homescreen()
            else:  # In levels - handle global events
                events_for_level = []
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        cheat_action = cheat_system.handle_cheat_input(event)
                        if cheat_action:
                            self.handle_cheat_action(cheat_action)
                            continue
                        
                        # Save/Load controls during game
                        if event.key == pygame.K_F5:
                            if save_manager.quick_save(self):
                                print("💾 Quick save realizado!")
                            continue
                        elif event.key == pygame.K_F9:
                            self.game_state = 50
                            continue
                        elif event.key == pygame.K_F6:
                            self.game_state = 51
                            continue
                    
                    # NOVA INTERFACE: Handle audio controls
                    if modern_audio_controls.handle_event(event):
                        continue  # Event consumed by audio controls
                    
                    # Put non-consumed events back for the level to handle
                    events_for_level.append(event)
                
                # Repost events for levels
                for event in events_for_level:
                    pygame.event.post(event)

            self.screen.fill((0, 0, 0))  # Fill with black

            if self.game_state == -1:
                self.name_input_screen.update(self.clock.get_time())
                self.name_input_screen.draw()
            elif self.game_state == 0:
                self.homescreen()

            elif self.game_state == 3:  # Level 1
                if not hasattr(self, 'level1_story_shown'):
                    story = StoryScreen("phase_1", custom_background="../map new/map.png")
                    story_finished = False
                    while not story_finished:
                        story_finished = story.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.level1_story_shown = True
                
                self.level1.run()
                # NOVA INTERFACE: Desenha controles nos levels
                modern_audio_controls.draw(self.screen)
                
                if self.level1.gameover:
                    audio_manager.stop_music()
                    self.game_state = 20
                elif self.level1.completed:
                    player_stats.complete_level(1)
                    save_manager.auto_save(self)
                    self.transition_start_time = pygame.time.get_ticks()
                    self.game_state = 4

            elif self.game_state == 4:  # Level 2
                if not hasattr(self, 'level2_story_shown'):
                    story = StoryScreen("phase_2", custom_background="../map new/maze1.png")
                    story_finished = False
                    while not story_finished:
                        story_finished = story.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.level2_story_shown = True
                
                self.level2.run()
                modern_audio_controls.draw(self.screen)
                
                if self.level2.gameover:
                    self.game_state = 20
                    audio_manager.stop_music()
                elif self.level2.completed:
                    player_stats.complete_level(2)
                    save_manager.auto_save(self)
                    self.game_state = 5
                    audio_manager.play_music('../audio/darkambience(from fable).mp3')

            elif self.game_state == 5:  # Level 3
                if not hasattr(self, 'level3_story_shown'):
                    story = StoryScreen("phase_3", custom_background="../map new/dungeon.png")
                    story_finished = False
                    while not story_finished:
                        story_finished = story.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.level3_story_shown = True
                
                self.level3.run()
                modern_audio_controls.draw(self.screen)
                
                if self.level3.completed:
                    player_stats.complete_level(3)
                    save_manager.auto_save(self)
                    self.game_state = 6
                    audio_manager.play_music('../audio/home.mp3')

            elif self.game_state == 6:  # Level 4
                if not hasattr(self, 'level4_story_shown'):
                    story = StoryScreen("phase_4", custom_background="../map new/final.png")
                    story_finished = False
                    while not story_finished:
                        story_finished = story.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.level4_story_shown = True
                
                self.level4.run()
                modern_audio_controls.draw(self.screen)
                
                if self.level4.completed:
                    player_stats.complete_level(4)
                    save_manager.auto_save(self)
                    
                    story = StoryScreen("victory", custom_background="../graphics/ui/home page.jpg")
                    story_finished = False
                    while not story_finished:
                        story_finished = story.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.game_state = 0
                    audio_manager.stop_music()
                    player_stats.end_session()
                if self.level4.gameover:
                    self.game_state = 20
                    
            elif self.game_state == 20:  # Game Over
                self.gameover()
            
            elif self.game_state == 30:  # Statistics Screen
                events = pygame.event.get()
                result = self.stats_screen.handle_events(events)
                if result == 'main_menu':
                    self.game_state = 0
                    self.stats_screen = StatsScreen()
                elif result == 'achievements':
                    self.game_state = 31
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
                else:
                    self.stats_screen.draw()
            
            elif self.game_state == 31:  # Achievements Screen
                events = pygame.event.get()
                result = self.achievements_screen.handle_events(events)
                if result == 'stats':
                    self.game_state = 30
                    self.achievements_screen = AchievementsScreen()
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
                else:
                    self.achievements_screen.draw()
            
            elif self.game_state == 40:  # Difficulty Screen
                events = pygame.event.get()
                result = self.difficulty_screen.handle_events(events)
                if result == 'main_menu' or result == 'confirm':
                    self.game_state = 0
                    self.difficulty_screen = DifficultyScreen()
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
                else:
                    self.difficulty_screen.draw()
            
            elif self.game_state == 50:  # Load Screen
                if self.save_screen is None:
                    self.save_screen = SaveScreen("load")
                
                events = pygame.event.get()
                result = self.save_screen.handle_events(events)
                
                if result == 'cancel':
                    self.game_state = 0
                    self.save_screen = None
                elif isinstance(result, tuple) and result[0] == 'load_confirm':
                    slot = result[1]
                    save_data = save_manager.load_game(slot)
                    if save_data:
                        if save_manager.apply_save_data(self, save_data):
                            print(f"✅ Jogo carregado do slot {slot}")
                            self.game_state = save_data["game_state"]["current_level"]
                        else:
                            print("❌ Erro ao aplicar dados do save")
                            self.game_state = 0
                    else:
                        print("❌ Erro ao carregar save")
                        self.game_state = 0
                    self.save_screen = None
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
                else:
                    self.save_screen.update(self.clock.get_time())
                    self.save_screen.draw()
            
            elif self.game_state == 51:  # Save Screen
                if self.save_screen is None:
                    self.save_screen = SaveScreen("save")
                
                events = pygame.event.get()
                result = self.save_screen.handle_events(events)
                
                if result == 'cancel':
                    self.game_state = 0
                    self.save_screen = None
                elif isinstance(result, tuple) and result[0] == 'save_confirm':
                    slot = result[1]
                    save_name = result[2] if len(result) > 2 else None
                    if save_manager.save_game(self, slot, save_name):
                        print(f"✅ Jogo salvo no slot {slot}")
                        self.game_state = 0
                    else:
                        print("❌ Erro ao salvar jogo")
                        self.game_state = 0
                    self.save_screen = None
                elif isinstance(result, tuple) and result[0] == 'delete_confirm':
                    slot = result[1]
                    if save_manager.delete_save(slot):
                        print(f"🗑️ Save slot {slot} deletado")
                        self.save_screen = SaveScreen("save")
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
                else:
                    self.save_screen.update(self.clock.get_time())
                    self.save_screen.draw()
            
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()