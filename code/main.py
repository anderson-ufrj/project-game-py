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
from settings_manager import SettingsManager
from audio_manager import audio_manager
from main_menu import AdvancedMainMenu
from story_screen import StoryScreen
# CHEAT: Import cheat system for testing (remove for final version)
from cheat_system import cheat_system
# pygame.mixer.pre_init(44100, 16, 2, 4096)
from pygame.locals import*

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH),pygame.SCALED)
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
        self.game_state = 0
        
        # Font for homescreen text
        self.title_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 36)
        self.subtitle_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 18)
        self.info_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 12)

        # Settings manager
        self.settings = SettingsManager(initial_volume=0.5)
        
        # Advanced main menu
        fonts = {
            'title': self.title_font,
            'subtitle': self.subtitle_font,
            'info': self.info_font,
            'button': self.info_font
        }
        self.advanced_menu = AdvancedMainMenu(self.screen, fonts)
        
        # Use AudioManager for music control
        audio_manager.play_music('../audio/home.mp3')


    def homescreen(self):
        # Get mouse position and click status
        mouse_pos = pygame.mouse.get_pos()
        
        # Check for mouse clicks in the events
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
                # Also handle settings mouse clicks
                self.settings.handle_mouse_click(mouse_pos)
            elif event.type == pygame.KEYDOWN:
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
                else:
                    # Handle settings controls
                    self.settings.handle_keydown(event)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Put back non-consumed events
            if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT]:
                pygame.event.post(event)
        
        # Use the advanced menu system
        menu_action = self.advanced_menu.update_and_draw(mouse_pos, mouse_click)
        
        # Handle menu actions
        if menu_action == "start_game":
            # Show intro story first
            if not hasattr(self, 'intro_story_shown'):
                story = StoryScreen("intro")
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
        
        # Still draw settings overlay for compatibility
        self.settings.draw(self.screen)
        
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
            if self.game_state == 0:  # Homescreen - events handled in homescreen() method
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
                    
                    # Put non-consumed events back for the level to handle
                    events_for_level.append(event)
                
                # Repost events for levels
                for event in events_for_level:
                    pygame.event.post(event)

            self.screen.fill((0, 0, 0))  # Fill with black

            if self.game_state == 0:
                self.homescreen()

            elif self.game_state == 3:  # Level 1 (skipped intro animations)
                # Mostrar história antes da fase 1
                if not hasattr(self, 'level1_story_shown'):
                    story = StoryScreen("phase_1")
                    story_finished = False
                    while not story_finished:
                        story_finished = story.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.level1_story_shown = True
                
                self.level1.run()
                if self.level1.gameover:
                    audio_manager.stop_music()
                    self.game_state = 20  # Game over, return to homescreen
                elif self.level1.completed:
                    self.transition_start_time = pygame.time.get_ticks()
                    self.game_state = 4  # Set game state to transition


            elif self.game_state == 4:  # Level 2 (simplified)
                # Mostrar história antes da fase 2
                if not hasattr(self, 'level2_story_shown'):
                    story = StoryScreen("phase_2")
                    story_finished = False
                    while not story_finished:
                        story_finished = story.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.level2_story_shown = True
                
                self.level2.run()
                if self.level2.gameover:
                    self.game_state = 20
                    audio_manager.stop_music()
                elif self.level2.completed:
                    self.game_state = 5  # Go to Level 3
                    audio_manager.play_music('../audio/darkambience(from fable).mp3')

            elif self.game_state == 5:  # Level 3 (simplified)
                # Mostrar história antes da fase 3
                if not hasattr(self, 'level3_story_shown'):
                    story = StoryScreen("phase_3")
                    story_finished = False
                    while not story_finished:
                        story_finished = story.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.level3_story_shown = True
                
                self.level3.run()
                if self.level3.completed:
                    self.game_state = 6  # Go to Level 4
                    audio_manager.play_music('../audio/home.mp3')

            elif self.game_state == 6:  # Level 4 (simplified)
                # Mostrar história antes da fase 4
                if not hasattr(self, 'level4_story_shown'):
                    story = StoryScreen("phase_4")
                    story_finished = False
                    while not story_finished:
                        story_finished = story.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.level4_story_shown = True
                
                self.level4.run()
                if self.level4.completed:
                    # Mostrar história de vitória
                    story = StoryScreen("victory")
                    story_finished = False
                    while not story_finished:
                        story_finished = story.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.game_state = 0  # Voltar ao menu principal
                    audio_manager.stop_music()
                if self.level4.gameover:
                    self.game_state = 20
                    
            elif self.game_state == 20:  # Game Over
                self.gameover()
                # Don't reset automatically - let gameover() handle it
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
