import pygame
import math
import time
from settings import WIDTH, HEIGTH
from audio_manager import audio_manager
from font_manager import font_manager

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
        self.settings_rect = pygame.Rect(WIDTH - 320, 70, 300, 220)  # Maior para nova UI
        
        # Fonts - usando novo sistema
        self.info_font = font_manager.get('small')
        self.symbol_font = font_manager.get('text')
        
        # Volume control enhancements
        self.volume_animation_time = 0
        self.handle_hover = False
        self.handle_dragging = False
        self.volume_change_time = 0
        self.last_volume = audio_manager.volume
        
        # Visual effects
        self.ripple_effects = []  # Para efeitos de onda quando clica
        self.glow_intensity = 0
        self.volume_bars = []  # Para barras de volume animadas
    
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
    
    def add_ripple_effect(self, x, y):
        """Adiciona efeito de onda na posição especificada"""
        self.ripple_effects.append({
            'x': x,
            'y': y,
            'radius': 0,
            'max_radius': 30,
            'alpha': 255,
            'time': time.time()
        })
    
    def update_volume_effects(self):
        """Atualiza efeitos visuais do volume"""
        current_time = time.time()
        self.volume_animation_time = current_time
        
        # Detectar mudança de volume para animações
        if self.last_volume != audio_manager.volume:
            self.volume_change_time = current_time
            self.last_volume = audio_manager.volume
            
            # Gerar barras de volume animadas
            self.volume_bars = []
            for i in range(10):
                if i / 10.0 <= audio_manager.volume:
                    self.volume_bars.append({
                        'height': 20 + (i * 2),
                        'alpha': 255,
                        'delay': i * 0.02
                    })
        
        # Atualizar efeitos de onda
        self.ripple_effects = [effect for effect in self.ripple_effects 
                              if current_time - effect['time'] < 1.0]
        
        for effect in self.ripple_effects:
            elapsed = current_time - effect['time']
            effect['radius'] = min(effect['max_radius'], elapsed * 40)
            effect['alpha'] = max(0, 255 - int(elapsed * 255))
        
        # Atualizar brilho
        self.glow_intensity = 50 + 25 * math.sin(current_time * 3)
    
    def handle_mouse_click(self, mouse_pos):
        """Handle mouse clicks for settings"""
        # Check if clicked on gear icon
        if self.gear_rect.collidepoint(mouse_pos):
            self.settings_open = not self.settings_open
            self.add_ripple_effect(mouse_pos[0], mouse_pos[1])
            return True  # Consumed the click
        
        # Check if clicked on volume slider (when menu is open)
        elif self.settings_open:
            slider_rect = pygame.Rect(self.settings_rect.x + 25, self.settings_rect.y + 90, 250, 25)
            if slider_rect.collidepoint(mouse_pos):
                # Calculate new volume based on mouse position
                relative_x = mouse_pos[0] - slider_rect.x
                new_volume = max(0.0, min(1.0, relative_x / 250.0))
                audio_manager.set_volume(new_volume)
                self.add_ripple_effect(mouse_pos[0], mouse_pos[1])
                return True  # Consumed the click
            
            # Check mute button
            mute_rect = pygame.Rect(self.settings_rect.x + 25, self.settings_rect.y + 130, 250, 30)
            if mute_rect.collidepoint(mouse_pos):
                audio_manager.toggle_mute()
                self.add_ripple_effect(mouse_pos[0], mouse_pos[1])
                return True
            
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
    
    def draw_advanced_volume_bars(self, surface, x, y, width, height):
        """Desenha barras de volume animadas estilo equalizador"""
        bar_count = 15
        bar_width = width // bar_count - 2
        current_time = time.time()
        
        for i in range(bar_count):
            bar_x = x + i * (bar_width + 2)
            
            # Altura baseada no volume e animação
            volume_threshold = i / bar_count
            if volume_threshold <= audio_manager.volume:
                # Animação de altura
                animation_offset = math.sin(current_time * 8 + i * 0.5) * 3
                bar_height = height * (0.3 + 0.7 * (i / bar_count)) + animation_offset
                
                # Cor baseada na altura da barra
                if i < bar_count * 0.6:
                    color = (50 + i * 8, 255 - i * 5, 50)  # Verde para baixo volume
                elif i < bar_count * 0.8:
                    color = (255, 255 - i * 8, 50)  # Amarelo para médio
                else:
                    color = (255, 100 - i * 3, 50)  # Vermelho para alto
                
                # Efeito de brilho
                glow_alpha = int(100 + 50 * math.sin(current_time * 6 + i))
                glow_color = (*color, glow_alpha)
                
                # Desenhar barra principal
                bar_rect = pygame.Rect(bar_x, y + height - bar_height, bar_width, bar_height)
                pygame.draw.rect(surface, color, bar_rect, border_radius=2)
                
                # Efeito de reflexo
                reflect_height = bar_height * 0.3
                reflect_rect = pygame.Rect(bar_x, y + height + 2, bar_width, reflect_height)
                reflect_color = (color[0]//3, color[1]//3, color[2]//3)
                pygame.draw.rect(surface, reflect_color, reflect_rect, border_radius=2)
    
    def draw_modern_slider(self, surface, x, y, width, height, value):
        """Desenha slider moderno com efeitos visuais"""
        current_time = time.time()
        
        # Background track com gradiente
        track_rect = pygame.Rect(x, y + height//3, width, height//3)
        pygame.draw.rect(surface, (40, 40, 40), track_rect, border_radius=height//6)
        
        # Track interno escuro
        inner_track = pygame.Rect(x + 2, y + height//3 + 2, width - 4, height//3 - 4)
        pygame.draw.rect(surface, (20, 20, 20), inner_track, border_radius=height//8)
        
        # Preenchimento do track
        fill_width = int(width * value)
        if fill_width > 0:
            # Gradiente de cor baseado no volume
            if value > 0.8:
                colors = [(255, 100, 100), (255, 150, 100)]  # Vermelho alto
            elif value > 0.5:
                colors = [(255, 255, 100), (255, 200, 100)]  # Amarelo médio
            else:
                colors = [(100, 255, 100), (150, 255, 150)]  # Verde baixo
            
            fill_rect = pygame.Rect(x + 2, y + height//3 + 2, fill_width - 4, height//3 - 4)
            
            # Efeito de brilho animado
            glow_intensity = int(100 + 50 * math.sin(current_time * 4))
            for i in range(3):
                glow_rect = pygame.Rect(x + 2 - i, y + height//3 + 2 - i, 
                                      fill_width - 4 + 2*i, height//3 - 4 + 2*i)
                glow_color = (*colors[0], glow_intensity // (i + 1))
                glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, glow_color, 
                               (0, 0, glow_rect.width, glow_rect.height), border_radius=height//8)
                surface.blit(glow_surface, glow_rect.topleft)
            
            pygame.draw.rect(surface, colors[0], fill_rect, border_radius=height//8)
        
        # Handle do slider
        handle_x = x + int(width * value)
        handle_y = y
        handle_size = height
        
        # Sombra do handle
        shadow_offset = 3
        shadow_rect = pygame.Rect(handle_x - handle_size//2 + shadow_offset, 
                                handle_y + shadow_offset, handle_size, handle_size)
        pygame.draw.circle(surface, (0, 0, 0, 100), shadow_rect.center, handle_size//2)
        
        # Handle principal com gradiente
        handle_rect = pygame.Rect(handle_x - handle_size//2, handle_y, handle_size, handle_size)
        
        # Brilho animado no handle
        pulse = math.sin(current_time * 3) * 0.2 + 0.8
        outer_color = (int(200 * pulse), int(200 * pulse), int(255 * pulse))
        inner_color = (255, 255, 255)
        
        pygame.draw.circle(surface, outer_color, handle_rect.center, handle_size//2)
        pygame.draw.circle(surface, inner_color, handle_rect.center, handle_size//2 - 3)
        pygame.draw.circle(surface, outer_color, handle_rect.center, handle_size//2 - 6)
        
        # Indicador de valor no handle
        if value > 0:
            value_text = self.info_font.render(f"{int(value * 100)}", True, (50, 50, 50))
            value_rect = value_text.get_rect(center=handle_rect.center)
            surface.blit(value_text, value_rect)
    
    def draw_settings_menu(self, surface):
        """Draw the advanced settings dropdown menu"""
        if not self.settings_open:
            return
        
        # Atualizar efeitos visuais
        self.update_volume_effects()
        
        # Menu shadow com múltiplas camadas
        for i in range(5):
            shadow_rect = pygame.Rect(self.settings_rect.x + i, self.settings_rect.y + i, 
                                    self.settings_rect.width, self.settings_rect.height)
            shadow_alpha = 50 - i * 8
            shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surface, (0, 0, 0, shadow_alpha), 
                           (0, 0, shadow_rect.width, shadow_rect.height), border_radius=15)
            surface.blit(shadow_surface, shadow_rect.topleft)
        
        # Menu background com gradiente
        pygame.draw.rect(surface, (30, 30, 35), self.settings_rect, border_radius=15)
        
        # Borda brilhante animada
        border_glow = int(self.glow_intensity)
        border_color = (100 + border_glow, 100 + border_glow, 150 + border_glow)
        pygame.draw.rect(surface, border_color, self.settings_rect, 3, border_radius=15)
        
        # Header com gradiente
        header_rect = pygame.Rect(self.settings_rect.x, self.settings_rect.y, 
                                self.settings_rect.width, 40)
        pygame.draw.rect(surface, (50, 50, 60), header_rect, 
                        border_top_left_radius=15, border_top_right_radius=15)
        
        # Título com efeito
        title_text = self.info_font.render("🎵 CONTROLE DE ÁUDIO", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=self.settings_rect.centerx, y=self.settings_rect.y + 12)
        
        # Sombra do título
        title_shadow = self.info_font.render("🎵 CONTROLE DE ÁUDIO", True, (0, 0, 0))
        surface.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        surface.blit(title_text, title_rect)
        
        # Seção de volume com título
        vol_section_y = self.settings_rect.y + 55
        section_title = self.info_font.render(f"🔊 VOLUME: {audio_manager.get_volume_percentage()}%", 
                                            True, (220, 220, 255))
        section_rect = section_title.get_rect(x=self.settings_rect.x + 25, y=vol_section_y)
        surface.blit(section_title, section_rect)
        
        # Barras de volume estilo equalizador
        eq_y = vol_section_y + 25
        eq_rect = pygame.Rect(self.settings_rect.x + 25, eq_y, 100, 20)
        self.draw_advanced_volume_bars(surface, eq_rect.x, eq_rect.y, eq_rect.width, eq_rect.height)
        
        # Slider moderno
        slider_y = eq_y + 30
        slider_rect = pygame.Rect(self.settings_rect.x + 25, slider_y, 250, 25)
        self.draw_modern_slider(surface, slider_rect.x, slider_rect.y, 
                              slider_rect.width, slider_rect.height, audio_manager.volume)
        
        # Botão mute moderno
        mute_y = slider_y + 40
        mute_rect = pygame.Rect(self.settings_rect.x + 25, mute_y, 250, 30)
        
        # Background do botão mute
        if audio_manager.is_muted():
            mute_bg_color = (80, 30, 30)
            mute_border_color = (255, 100, 100)
            mute_text_color = (255, 200, 200)
            mute_icon = "🔇"
            mute_status = "ÁUDIO DESLIGADO"
        else:
            mute_bg_color = (30, 80, 30)
            mute_border_color = (100, 255, 100)
            mute_text_color = (200, 255, 200)
            mute_icon = "🔊"
            mute_status = "ÁUDIO LIGADO"
        
        # Efeito hover no botão mute
        mouse_pos = pygame.mouse.get_pos()
        if mute_rect.collidepoint(mouse_pos):
            mute_bg_color = tuple(min(255, c + 20) for c in mute_bg_color)
        
        pygame.draw.rect(surface, mute_bg_color, mute_rect, border_radius=8)
        pygame.draw.rect(surface, mute_border_color, mute_rect, 2, border_radius=8)
        
        mute_text = self.info_font.render(f"{mute_icon} [M] {mute_status}", True, mute_text_color)
        mute_text_rect = mute_text.get_rect(center=mute_rect.center)
        surface.blit(mute_text, mute_text_rect)
        
        # Instruções com ícones melhorados
        help_y = mute_y + 45
        help_texts = [
            "⌨️ ↑↓ Volume | 🖱️ Clique/Arraste | M Mudo",
            "⚙️ ESC Fechar | 🎵 Áudio em Tempo Real"
        ]
        
        for i, help_text in enumerate(help_texts):
            help_surface = self.info_font.render(help_text, True, (160, 180, 200))
            help_rect = help_surface.get_rect(centerx=self.settings_rect.centerx, y=help_y + i * 15)
            surface.blit(help_surface, help_rect)
        
        # Desenhar efeitos de onda
        for effect in self.ripple_effects:
            if effect['alpha'] > 0:
                ripple_surface = pygame.Surface((effect['radius'] * 2, effect['radius'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(ripple_surface, (255, 255, 255, effect['alpha']), 
                                 (effect['radius'], effect['radius']), effect['radius'], 2)
                surface.blit(ripple_surface, (effect['x'] - effect['radius'], effect['y'] - effect['radius']))
    
    def draw(self, surface):
        """Draw both button and menu"""
        self.draw_settings_button(surface)
        self.draw_settings_menu(surface)
    
    def is_menu_open(self):
        """Check if settings menu is open"""
        return self.settings_open