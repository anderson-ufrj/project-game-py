import pygame
from settings import WIDTH, HEIGTH
from audio_manager import audio_manager

class SettingsManager:
    """Gerenciador de configurações reutilizável para todas as fases"""
    
    def __init__(self, initial_volume=0.5):
        # Garantir que pygame está inicializado
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
            
        # Usar o AudioManager centralizado
        self.settings_open = False
        
        # UI positioning
        self.gear_rect = pygame.Rect(WIDTH - 60, 20, 40, 40)
        self.settings_rect = pygame.Rect(WIDTH - 280, 70, 260, 180)
        
        # Fonts
        try:
            self.info_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 12)
            self.symbol_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 16)
        except:
            self.info_font = pygame.font.Font(None, 16)
            self.symbol_font = pygame.font.Font(None, 20)
    
    def handle_keydown(self, event):
        """Handle keyboard events for settings"""
        if event.key == pygame.K_m:
            audio_manager.toggle_mute()
        elif event.key == pygame.K_UP:
            new_volume = min(1.0, audio_manager.volume + 0.1)
            audio_manager.set_volume(new_volume)
        elif event.key == pygame.K_DOWN:
            new_volume = max(0.0, audio_manager.volume - 0.1)
            audio_manager.set_volume(new_volume)
        elif event.key == pygame.K_ESCAPE:
            self.settings_open = False
    
    def handle_mouse_click(self, mouse_pos):
        """Handle mouse clicks for settings"""
        # Check if clicked on gear icon
        if self.gear_rect.collidepoint(mouse_pos):
            self.settings_open = not self.settings_open
            return True  # Consumed the click
        
        # Check if clicked on volume slider (when menu is open)
        elif self.settings_open:
            slider_rect = pygame.Rect(self.settings_rect.x + 15, self.settings_rect.y + 80, 200, 18)
            if slider_rect.collidepoint(mouse_pos):
                # Calculate new volume based on mouse position
                relative_x = mouse_pos[0] - slider_rect.x
                new_volume = max(0.0, min(1.0, relative_x / 200.0))
                audio_manager.set_volume(new_volume)
                return True  # Consumed the click
            
            # Check if clicked outside settings menu to close it
            elif not self.settings_rect.collidepoint(mouse_pos):
                self.settings_open = False
                return False  # Didn't consume the click
        
        return False  # Didn't consume the click
    
    def toggle_mute(self):
        """Toggle music mute on/off"""
        audio_manager.toggle_mute()
    
    def change_volume(self, delta):
        """Change music volume by delta (-0.1 to +0.1)"""
        new_volume = max(0.0, min(1.0, audio_manager.volume + delta))
        audio_manager.set_volume(new_volume)
    
    def set_volume(self, volume):
        """Set absolute volume level"""
        audio_manager.set_volume(volume)
    
    def draw_settings_button(self, surface, color=(200, 200, 200)):
        """Draw an enhanced settings button"""
        is_hovered = self.gear_rect.collidepoint(pygame.mouse.get_pos())
        
        # Shadow effect
        shadow_rect = pygame.Rect(self.gear_rect.x + 2, self.gear_rect.y + 2, 
                                 self.gear_rect.width, self.gear_rect.height)
        pygame.draw.circle(surface, (20, 20, 20), shadow_rect.center, self.gear_rect.width//2)
        
        # Background with gradient effect
        bg_color = (80, 80, 80) if is_hovered else (50, 50, 50)
        pygame.draw.circle(surface, bg_color, self.gear_rect.center, self.gear_rect.width//2)
        
        # Border with glow effect when hovered
        border_color = (255, 215, 0) if is_hovered else color
        border_width = 3 if is_hovered else 2
        pygame.draw.circle(surface, border_color, self.gear_rect.center, self.gear_rect.width//2, border_width)
        
        # Settings symbol
        try:
            settings_text = self.symbol_font.render("⚙", True, border_color)
        except:
            settings_text = self.info_font.render("CONF", True, border_color)
        
        text_rect = settings_text.get_rect(center=self.gear_rect.center)
        surface.blit(settings_text, text_rect)
    
    def draw_settings_menu(self, surface):
        """Draw the settings dropdown menu"""
        if not self.settings_open:
            return
        
        # Menu shadow
        shadow_rect = pygame.Rect(self.settings_rect.x + 3, self.settings_rect.y + 3, 
                                self.settings_rect.width, self.settings_rect.height)
        pygame.draw.rect(surface, (10, 10, 10), shadow_rect, border_radius=10)
        
        # Menu background with rounded corners
        pygame.draw.rect(surface, (45, 45, 45), self.settings_rect, border_radius=10)
        pygame.draw.rect(surface, (120, 120, 120), self.settings_rect, 3, border_radius=10)
        
        # Header background
        header_rect = pygame.Rect(self.settings_rect.x, self.settings_rect.y, 
                                self.settings_rect.width, 35)
        pygame.draw.rect(surface, (60, 60, 60), header_rect, border_top_left_radius=10, border_top_right_radius=10)
        
        # Menu title
        title_text = self.info_font.render("⚙ CONFIGURAÇÕES", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=self.settings_rect.centerx, y=self.settings_rect.y + 10)
        surface.blit(title_text, title_rect)
        
        # Volume control section
        vol_y = self.settings_rect.y + 55
        vol_text = self.info_font.render(f"🔊 Volume: {audio_manager.get_volume_percentage()}%", True, (220, 220, 220))
        vol_rect = vol_text.get_rect(x=self.settings_rect.x + 15, y=vol_y)
        surface.blit(vol_text, vol_rect)
        
        # Enhanced volume slider
        slider_y = vol_y + 25
        slider_rect = pygame.Rect(self.settings_rect.x + 15, slider_y, 200, 18)
        
        # Slider background with gradient
        pygame.draw.rect(surface, (30, 30, 30), slider_rect, border_radius=9)
        pygame.draw.rect(surface, (100, 100, 100), slider_rect, 2, border_radius=9)
        
        # Volume slider fill with gradient colors
        fill_width = int(200 * audio_manager.volume)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.settings_rect.x + 15, slider_y, fill_width, 18)
            # Color based on volume level
            if audio_manager.volume > 0.7:
                fill_color = (100, 255, 100)  # Green for high volume
            elif audio_manager.volume > 0.3:
                fill_color = (255, 255, 100)  # Yellow for medium volume  
            else:
                fill_color = (255, 150, 100)  # Orange for low volume
            pygame.draw.rect(surface, fill_color, fill_rect, border_radius=9)
        
        # Volume slider handle
        handle_x = self.settings_rect.x + 15 + int(200 * audio_manager.volume) - 6
        handle_y = slider_y + 3
        handle_rect = pygame.Rect(handle_x, handle_y, 12, 12)
        pygame.draw.circle(surface, (200, 200, 200), handle_rect.center, 6)
        pygame.draw.circle(surface, (255, 255, 255), handle_rect.center, 4)
        
        # Mute button with enhanced styling
        mute_y = slider_y + 35
        mute_bg_rect = pygame.Rect(self.settings_rect.x + 15, mute_y - 5, 220, 25)
        mute_bg_color = (70, 30, 30) if audio_manager.is_muted() else (30, 70, 30)
        pygame.draw.rect(surface, mute_bg_color, mute_bg_rect, border_radius=5)
        
        mute_status = "🔇 MUDO" if audio_manager.is_muted() else "🔊 SOM LIGADO"
        mute_color = (255, 150, 150) if audio_manager.is_muted() else (150, 255, 150)
        mute_text = self.info_font.render(f"[M] {mute_status}", True, mute_color)
        mute_rect = mute_text.get_rect(x=self.settings_rect.x + 20, y=mute_y)
        surface.blit(mute_text, mute_rect)
        
        # Controls help with icons
        help_y = mute_y + 35
        help_text = self.info_font.render("↑↓ Teclas | 🖱️ Mouse | ESC Fechar", True, (160, 160, 160))
        help_rect = help_text.get_rect(x=self.settings_rect.x + 15, y=help_y)
        surface.blit(help_text, help_rect)
        
        # Pause notice for in-game
        pause_y = help_y + 25
        pause_text = self.info_font.render("⏸️ Jogo pausado", True, (255, 255, 100))
        pause_rect = pause_text.get_rect(centerx=self.settings_rect.centerx, y=pause_y)
        surface.blit(pause_text, pause_rect)
    
    def draw(self, surface):
        """Draw both button and menu"""
        self.draw_settings_button(surface)
        self.draw_settings_menu(surface)
    
    def is_menu_open(self):
        """Check if settings menu is open"""
        return self.settings_open