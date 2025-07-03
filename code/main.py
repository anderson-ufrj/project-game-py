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
        # Use AudioManager for music control
        audio_manager.play_music('../audio/home.mp3')


    def homescreen(self):
        self.screen.blit(self.homescreen_image, (0,0))
        
        # Add title
        title_text = self.title_font.render("CORRIDA PELA RELÍQUIA", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH//2, 100))
        # Add shadow for better readability
        title_shadow = self.title_font.render("CORRIDA PELA RELÍQUIA", True, (0, 0, 0))
        shadow_rect = title_shadow.get_rect(center=(WIDTH//2 + 3, 103))
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Add subtitle
        subtitle_text = self.subtitle_font.render("A Busca pela Gema Eldritch", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, 160))
        subtitle_shadow = self.subtitle_font.render("A Busca pela Gema Eldritch", True, (0, 0, 0))
        subtitle_shadow_rect = subtitle_shadow.get_rect(center=(WIDTH//2 + 2, 162))
        self.screen.blit(subtitle_shadow, subtitle_shadow_rect)
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Add instructions
        instruction_text = self.info_font.render("Pressione ENTER para começar", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGTH - 150))
        instruction_shadow = self.info_font.render("Pressione ENTER para começar", True, (0, 0, 0))
        instruction_shadow_rect = instruction_shadow.get_rect(center=(WIDTH//2 + 1, HEIGTH - 149))
        self.screen.blit(instruction_shadow, instruction_shadow_rect)
        self.screen.blit(instruction_text, instruction_rect)
        
        # Add academic project info
        project_info_y = HEIGTH - 80
        project_text1 = self.info_font.render("Projeto Acadêmico - Tópicos Especiais I", True, (180, 180, 180))
        project_rect1 = project_text1.get_rect(center=(WIDTH//2, project_info_y))
        self.screen.blit(project_text1, project_rect1)
        
        project_text2 = self.info_font.render("IFSULDEMINAS Campus Muzambinho", True, (180, 180, 180))
        project_rect2 = project_text2.get_rect(center=(WIDTH//2, project_info_y + 20))
        self.screen.blit(project_text2, project_rect2)
        
        project_text3 = self.info_font.render("Aluno: Anderson Henrique da Silva", True, (180, 180, 180))
        project_rect3 = project_text3.get_rect(center=(WIDTH//2, project_info_y + 40))
        self.screen.blit(project_text3, project_rect3)
        
        project_text4 = self.info_font.render("Orientador: Prof. Ricardo Martins", True, (180, 180, 180))
        project_rect4 = project_text4.get_rect(center=(WIDTH//2, project_info_y + 60))
        self.screen.blit(project_text4, project_rect4)
        
        # Draw settings button and menu
        self.settings.draw(self.screen)
        
        pygame.display.update()
    
    
    def gameover(self):
        self.gameover_image = pygame.transform.scale(self.gameover_image,(1280,720))
        self.screen.blit(self.gameover_image,(0,0))
        self.reset_game()
        pygame.display.update()

    def reset_game(self):
        # Reset all game-related variables and clear sprites
        self.level1.reset()
        self.level2.reset()
        self.level3.reset()
        self.level4.reset()
        # Intro classes removed

    def run(self):

        while True:
            # Only handle events on homescreen, let levels handle their own events
            if self.game_state == 0:  # Homescreen - handle events here
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            # Skip intro animations, go directly to Level 1
                            audio_manager.play_music('../audio/Ambient 2.mp3')
                            self.game_state = 3  # Go directly to Level 1
                        else:
                            # Handle settings controls
                            self.settings.handle_keydown(event)
                    
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        # Handle settings mouse clicks
                        self.settings.handle_mouse_click(mouse_pos)
            else:  # In levels - only handle QUIT events, let levels handle the rest
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    # Put the event back for the level to handle
                    pygame.event.post(event)

            self.screen.fill((0, 0, 0))  # Fill with black

            if self.game_state == 0:
                self.homescreen()

            elif self.game_state == 3:  # Level 1 (skipped intro animations)
                self.level1.run()
                if self.level1.gameover:
                    audio_manager.stop_music()
                    self.game_state = 20  # Game over, return to homescreen
                elif self.level1.completed:
                    self.transition_start_time = pygame.time.get_ticks()
                    self.game_state = 4  # Set game state to transition


            elif self.game_state == 4:  # Level 2 (simplified)
                self.level2.run()
                if self.level2.gameover:
                    self.game_state = 20
                    audio_manager.stop_music()
                if self.level2.completed:
                    self.game_state = 5  # Go to Level 3
                    audio_manager.play_music('../audio/darkambience(from fable).mp3')

            elif self.game_state == 5:  # Level 3 (simplified)
                self.level3.run()
                if self.level3.completed:
                    self.game_state = 6  # Go to Level 4
                    audio_manager.play_music('../audio/home.mp3')

            elif self.game_state == 6:  # Level 4 (simplified)
                self.level4.run()
                if self.level4.completed:
                    # Game completed! Could add victory screen here
                    pass
                if self.level4.gameover:
                    self.game_state = 20
                    
            elif self.game_state == 20:  # Game Over
                self.gameover()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
