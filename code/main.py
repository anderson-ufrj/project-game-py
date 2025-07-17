from support import import_folder
import pygame
import sys
from settings import *
from level import Level1
from level2 import Level2
from level3 import Level3
from level4 import Level4
from pygame.locals import *
# from intro import * # Removed - no longer using intro animations

from loading import LoadingScreen
from modern_audio_controls import modern_audio_controls
from audio_manager import audio_manager
from main_menu import AdvancedMainMenu
from professional_main_menu import get_professional_menu
from story_screen import StoryScreen
# CHEAT: Import cheat system for testing (remove for final version)
from cheat_system import cheat_system
# STATS: Import player statistics system
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
from tutorial_system import tutorial_system
# pygame.mixer.pre_init(44100, 16, 2, 4096)
from pygame.locals import*

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
            self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        
        pygame.display.set_caption('CORRIDA PELA RELÍQUIA')
        self.clock = pygame.time.Clock()

        self.level1 = Level1()
        self.level2 = Level2()
        self.level3 = Level3()
        self.level4 = Level4()
        # Intro animations removed - going directly to levels

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
        
        # Font for homescreen text - usando novo sistema de fontes
        self.title_font = font_manager.get('title')
        self.subtitle_font = font_manager.get('subtitle')
        self.info_font = font_manager.get('text')

        # Audio controls - agora usando sistema moderno e simples
        
        # Professional main menu
        self.professional_menu = get_professional_menu(self.screen)
        
        # Keep advanced menu as backup
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
                # Handle new audio controls
                modern_audio_controls.handle_event(event)
            elif event.type == pygame.KEYDOWN:
                # Handle Alt+Enter for fullscreen toggle
                if (event.key == pygame.K_RETURN and 
                    (pygame.key.get_pressed()[pygame.K_LALT] or pygame.key.get_pressed()[pygame.K_RALT])):
                    self.graphics_manager.toggle_fullscreen()
                    self.graphics_manager.apply_settings()
                    self.screen = self.graphics_manager.get_screen()
                    return
                
                # CHEAT: Handle cheat codes in menu (remove for final version)
                cheat_action = cheat_system.handle_cheat_input(event)
                if cheat_action:
                    self.handle_cheat_action(cheat_action)
                    return
                
                if event.key == pygame.K_RETURN:
                    # Allow ENTER key to start game
                    audio_manager.play_music('../audio/Ambient 2.mp3')
                    self.game_state = 3  # Go to Level 1
                    return
                elif event.key == pygame.K_1:
                    # Ir direto para Level 1
                    audio_manager.play_music('../audio/Ambient 2.mp3')
                    self.game_state = 3
                    return
                elif event.key == pygame.K_2:
                    # Ir direto para Level 2
                    audio_manager.play_music('../audio/Ambient 2.mp3')
                    self.game_state = 4
                    return
                elif event.key == pygame.K_3:
                    # Ir direto para Level 3
                    audio_manager.play_music('../audio/darkambience(from fable).mp3')
                    self.game_state = 5
                    return
                elif event.key == pygame.K_4:
                    # Ir direto para Level 4
                    audio_manager.play_music('../audio/home.mp3')
                    self.game_state = 6
                    return
                elif event.key == pygame.K_s:
                    # STATS: Go to statistics screen
                    self.game_state = 30
                    return
                elif event.key == pygame.K_d:
                    # Go to difficulty screen
                    self.game_state = 40
                    return
                elif event.key == pygame.K_l:
                    # Load game screen
                    self.game_state = 50
                    return
                elif event.key == pygame.K_t:
                    # Tutorial screen
                    tutorial_system.open_tutorial()
                    return
                else:
                    # Handle keyboard controls for audio
                    modern_audio_controls.handle_event(event)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Let the professional menu handle events
            menu_event_action = self.professional_menu.handle_event(event)
            if menu_event_action:
                if menu_event_action == "start_game":
                    # Show intro story first
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
                    
                    # Start the game
                    audio_manager.play_music('../audio/Ambient 2.mp3')
                    self.game_state = 3  # Go to Level 1
                    return
                elif menu_event_action == "quit_game":
                    pygame.quit()
                    sys.exit()
                elif menu_event_action == "show_tutorial":
                    tutorial_system.open_tutorial()
                    return
            
            # Let the advanced menu handle events (backup)
            self.advanced_menu.handle_event(event)
            
            # Handle tutorial events
            tutorial_system.handle_event(event)
            
            # Put back non-consumed events
            if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT]:
                pygame.event.post(event)
        
        # Use the professional menu system
        menu_action = self.professional_menu.update_and_draw(mouse_pos, mouse_click)
        
        # Handle menu actions
        if menu_action == "start_game":
            # Show intro story first
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
            
            # Start the game
            audio_manager.play_music('../audio/Ambient 2.mp3')
            self.game_state = 3  # Go to Level 1
        elif menu_action == "quit_game":
            pygame.quit()
            sys.exit()
        elif menu_action == "show_tutorial":
            tutorial_system.open_tutorial()
        elif menu_action == "show_settings":
            # Open audio settings
            pass  # Audio controls are already drawn
        elif menu_action == "show_stats":
            self.game_state = 30  # Go to stats screen
        
        # Draw new audio controls
        modern_audio_controls.draw(self.screen)
        
        # Update and draw tutorial
        tutorial_system.update()
        tutorial_system.draw(self.screen)
        
        # CHEAT: Display cheat information in menu (remove for final version)
        cheat_system.display_cheat_info(self.screen)
    
    
    def gameover(self):
        # CHEAT: Handle cheat codes in gameover screen (remove for final version)
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
        
        self.gameover_image = pygame.transform.scale(self.gameover_image,(1280,720))
        self.screen.blit(self.gameover_image,(0,0))
        
        # CHEAT: Display cheat information in gameover (remove for final version)
        cheat_system.display_cheat_info(self.screen)
        
        pygame.display.update()

    def reset_game(self):
        # Reset all game-related variables and clear sprites
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
    
    # CHEAT: Handle cheat actions from levels (remove for final version)
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
            # Handle events based on game state
            if self.game_state == -1:  # Name input screen
                events = pygame.event.get()
                result = self.name_input_screen.handle_events(events)
                if result == 'main_menu':
                    self.game_state = 0  # Go to homescreen
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
            elif self.game_state == 0:  # Homescreen - events handled in homescreen() method
                pass  # Events are handled inside homescreen()
            else:  # In levels - handle QUIT and CHEAT events, let levels handle the rest
                events_for_level = []
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        # CHEAT: Handle cheat codes in main loop (remove for final version)
                        cheat_action = cheat_system.handle_cheat_input(event)
                        if cheat_action:
                            self.handle_cheat_action(cheat_action)
                            continue  # Don't pass this event to level
                        
                        # Save/Load controls during game
                        if event.key == pygame.K_F5:
                            # Quick save
                            if save_manager.quick_save(self):
                                print("💾 Quick save realizado!")
                            continue
                        elif event.key == pygame.K_F9:
                            # Quick load (go to load screen)
                            self.game_state = 50
                            continue
                        elif event.key == pygame.K_F6:
                            # Save screen
                            self.game_state = 51
                            continue
                    
                    # Handle audio controls in levels
                    if modern_audio_controls.handle_event(event):
                        continue  # Event consumed by audio controls
                    
                    # Put non-consumed events back for the level to handle
                    events_for_level.append(event)
                
                # Repost events for levels
                for event in events_for_level:
                    pygame.event.post(event)

            self.screen.fill((0, 0, 0))  # Fill with black

            if self.game_state == -1:
                # STATS: Draw name input screen
                self.name_input_screen.update(self.clock.get_time())
                self.name_input_screen.draw()
            elif self.game_state == 0:
                self.homescreen()

            elif self.game_state == 3:  # Level 1 (skipped intro animations)
                # Mostrar história antes da fase 1
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
                # Draw audio controls in level
                modern_audio_controls.draw(self.screen)
                if self.level1.gameover:
                    audio_manager.stop_music()
                    self.game_state = 20  # Game over, return to homescreen
                elif self.level1.completed:
                    # STATS: Record level completion
                    player_stats.complete_level(1)
                    # Auto-save progress
                    save_manager.auto_save(self)
                    self.transition_start_time = pygame.time.get_ticks()
                    self.game_state = 4  # Set game state to transition


            elif self.game_state == 4:  # Level 2 (simplified)
                # Mostrar história antes da fase 2
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
                # Draw audio controls in level
                modern_audio_controls.draw(self.screen)
                if self.level2.gameover:
                    self.game_state = 20
                    audio_manager.stop_music()
                elif self.level2.completed:
                    # STATS: Record level completion
                    player_stats.complete_level(2)
                    # Auto-save progress
                    save_manager.auto_save(self)
                    self.game_state = 5  # Go to Level 3
                    audio_manager.play_music('../audio/darkambience(from fable).mp3')

            elif self.game_state == 5:  # Level 3 (simplified)
                # Mostrar história antes da fase 3
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
                # Draw audio controls in level
                modern_audio_controls.draw(self.screen)
                if self.level3.completed:
                    # STATS: Record level completion
                    player_stats.complete_level(3)
                    # Auto-save progress
                    save_manager.auto_save(self)
                    self.game_state = 6  # Go to Level 4
                    audio_manager.play_music('../audio/home.mp3')

            elif self.game_state == 6:  # Level 4 (simplified)
                # Mostrar história antes da fase 4
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
                # Draw audio controls in level
                modern_audio_controls.draw(self.screen)
                if self.level4.completed:
                    # STATS: Record level completion and game completion
                    player_stats.complete_level(4)
                    # Auto-save final progress
                    save_manager.auto_save(self)
                    # Mostrar história de vitória
                    story = StoryScreen("victory", custom_background="../graphics/ui/home page.jpg")
                    story_finished = False
                    while not story_finished:
                        story_finished = story.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.game_state = 0  # Voltar ao menu principal
                    audio_manager.stop_music()
                    # STATS: End session and save stats
                    player_stats.end_session()
                if self.level4.gameover:
                    self.game_state = 20
                    
            elif self.game_state == 20:  # Game Over
                self.gameover()
                # Don't reset automatically - let gameover() handle it
            
            elif self.game_state == 30:  # Statistics Screen
                events = pygame.event.get()
                result = self.stats_screen.handle_events(events)
                if result == 'main_menu':
                    self.game_state = 0  # Return to homescreen
                    # Refresh stats screen for next time
                    self.stats_screen = StatsScreen()
                elif result == 'achievements':
                    self.game_state = 31  # Go to achievements screen
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
                else:
                    self.stats_screen.draw()
            
            elif self.game_state == 31:  # Achievements Screen
                events = pygame.event.get()
                result = self.achievements_screen.handle_events(events)
                if result == 'stats':
                    self.game_state = 30  # Return to stats screen
                    # Refresh achievements screen for next time
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
                    self.game_state = 0  # Return to homescreen
                    # Refresh difficulty screen for next time
                    self.difficulty_screen = DifficultyScreen()
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
                else:
                    self.difficulty_screen.draw()
            
            elif self.game_state == 50:  # Save/Load Screen
                # Initialize save screen if needed
                if self.save_screen is None:
                    self.save_screen = SaveScreen("load")
                
                events = pygame.event.get()
                result = self.save_screen.handle_events(events)
                
                if result == 'cancel':
                    self.game_state = 0  # Return to homescreen
                    self.save_screen = None
                elif isinstance(result, tuple) and result[0] == 'load_confirm':
                    slot = result[1]
                    save_data = save_manager.load_game(slot)
                    if save_data:
                        # Apply save data to game
                        if save_manager.apply_save_data(self, save_data):
                            print(f"✅ Jogo carregado do slot {slot}")
                            # Go to loaded game state
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
                # Initialize save screen if needed
                if self.save_screen is None:
                    self.save_screen = SaveScreen("save")
                
                events = pygame.event.get()
                result = self.save_screen.handle_events(events)
                
                if result == 'cancel':
                    # Return to previous game state (pause menu logic would be here)
                    self.game_state = 0
                    self.save_screen = None
                elif isinstance(result, tuple) and result[0] == 'save_confirm':
                    slot = result[1]
                    save_name = result[2] if len(result) > 2 else None
                    if save_manager.save_game(self, slot, save_name):
                        print(f"✅ Jogo salvo no slot {slot}")
                        # Return to previous game state
                        self.game_state = 0
                    else:
                        print("❌ Erro ao salvar jogo")
                        self.game_state = 0
                    self.save_screen = None
                elif isinstance(result, tuple) and result[0] == 'delete_confirm':
                    slot = result[1]
                    if save_manager.delete_save(slot):
                        print(f"🗑️ Save slot {slot} deletado")
                        # Refresh save screen
                        self.save_screen = SaveScreen("save")
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
                else:
                    self.save_screen.update(self.clock.get_time())
                    self.save_screen.draw()
            pygame.display.update()
            
            # Usar FPS dinâmico baseado nas configurações gráficas
            fps_limit = self.graphics_manager.get_fps_limit()
            if fps_limit > 0:
                self.clock.tick(fps_limit)
            else:
                self.clock.tick()  # Sem limite de FPS

if __name__ == '__main__':
    game = Game()
    game.run()
