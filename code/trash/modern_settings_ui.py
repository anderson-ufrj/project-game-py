import pygame
import math
import time
from typing import Tuple, Optional
from settings import WIDTH, HEIGTH
from audio_manager import audio_manager
from ui_system import UIManager, ModernPanel, ModernSlider, ModernButton, UITheme
# from enhanced_font_system import enhanced_font_renderer  # Comentado - módulo não existe

class ModernSettingsManager:
    """Gerenciador de configurações com UI moderna"""
    
    def __init__(self):
        # Garantir que pygame está inicializado
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
        
        self.settings_open = False
        self.ui_manager = UIManager()
        self.components_created = False
        
        # Posicionamento
        self.gear_rect = pygame.Rect(WIDTH - 70, 20, 50, 50)
        self.panel_width = 400
        self.panel_height = 300
        self.panel_x = WIDTH - self.panel_width - 20
        self.panel_y = 80
        
        # Animações
        self.gear_rotation = 0
        self.panel_scale = 0.0
        self.gear_glow = 0
        
        # Volume visualizer
        self.volume_bars = []
        self.equalizer_active = False
        
    def toggle_settings(self):
        """Alterna abertura/fechamento do menu"""
        self.settings_open = not self.settings_open
        
        if self.settings_open:
            self.create_ui_components()
            self.panel_scale = 0.0
            self.animate_panel_open()
        else:
            self.ui_manager.clear_components()
            self.components_created = False
    
    def animate_panel_open(self):
        """Anima abertura do painel"""
        # Aqui você pode adicionar animação mais sofisticada se quiser
        self.panel_scale = 1.0
    
    def create_ui_components(self):
        """Cria os componentes da UI moderna"""
        if self.components_created:
            return
        
        # Painel principal
        main_panel = ModernPanel(
            self.panel_x, self.panel_y, self.panel_width, self.panel_height,
            "🎵 CONTROLE DE ÁUDIO",
            UITheme.BG_MEDIUM,
            UITheme.PRIMARY
        )
        self.ui_manager.add_component(main_panel)
        
        # Slider de volume
        volume_slider = ModernSlider(
            self.panel_x + 30, self.panel_y + 80, 
            self.panel_width - 60, 30,
            0.0, 1.0, audio_manager.volume,
            UITheme.PRIMARY,
            self.on_volume_change
        )
        self.ui_manager.add_component(volume_slider)
        
        # Botão mute/unmute
        mute_text = "🔇 DESMUTAR" if audio_manager.is_muted() else "🔇 MUTAR"
        mute_color = UITheme.DANGER if not audio_manager.is_muted() else UITheme.SUCCESS
        
        mute_button = ModernButton(
            self.panel_x + 30, self.panel_y + 130,
            self.panel_width - 60, 40,
            mute_text, 'button', mute_color,
            UITheme.TEXT_PRIMARY, self.on_mute_toggle
        )
        self.ui_manager.add_component(mute_button)
        
        # Botão de fechar
        close_button = ModernButton(
            self.panel_x + self.panel_width - 90, self.panel_y + 10,
            80, 30,
            "✕ FECHAR", 'small', UITheme.SECONDARY,
            UITheme.TEXT_PRIMARY, self.close_settings
        )
        self.ui_manager.add_component(close_button)
        
        self.components_created = True
    
    def on_volume_change(self, value: float):
        """Callback para mudança de volume"""
        audio_manager.set_volume(value)
        self.equalizer_active = True
        self.update_volume_bars()
    
    def on_mute_toggle(self):
        """Callback para toggle do mute"""
        audio_manager.toggle_mute()
        self.update_mute_button()
    
    def close_settings(self):
        """Fecha o menu de configurações"""
        self.settings_open = False
        self.ui_manager.clear_components()
        self.components_created = False
    
    def update_mute_button(self):
        """Atualiza o texto do botão mute"""
        if self.components_created:
            for component in self.ui_manager.components:
                if isinstance(component, ModernButton) and "MUTAR" in component.text:
                    component.text = "🔇 DESMUTAR" if audio_manager.is_muted() else "🔇 MUTAR"
                    component.color = UITheme.SUCCESS if audio_manager.is_muted() else UITheme.DANGER
                    break
    
    def update_volume_bars(self):
        """Atualiza as barras do equalizador"""
        self.volume_bars = []
        current_time = time.time()
        
        # Gerar barras baseadas no volume atual
        for i in range(15):
            if i / 15.0 <= audio_manager.volume:
                height_variation = math.sin(current_time * 8 + i * 0.7) * 5
                base_height = 20 + (i * 2)
                self.volume_bars.append({
                    'height': base_height + height_variation,
                    'intensity': audio_manager.volume + math.sin(current_time * 6 + i) * 0.1
                })
            else:
                self.volume_bars.append({'height': 5, 'intensity': 0})
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Manipula eventos"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar clique no ícone de engrenagem
            if self.gear_rect.collidepoint(event.pos):
                self.toggle_settings()
                return True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.settings_open:
                self.close_settings()
                return True
            elif event.key == pygame.K_m:
                self.on_mute_toggle()
                return True
            elif event.key == pygame.K_UP:
                new_volume = min(1.0, audio_manager.volume + 0.1)
                audio_manager.set_volume(new_volume)
                self.update_volume_slider()
                return True
            elif event.key == pygame.K_DOWN:
                new_volume = max(0.0, audio_manager.volume - 0.1)
                audio_manager.set_volume(new_volume)
                self.update_volume_slider()
                return True
        
        # Repassar eventos para UI manager
        if self.settings_open and self.components_created:
            return self.ui_manager.handle_event(event)
        
        return False
    
    def update_volume_slider(self):
        """Atualiza o valor do slider de volume"""
        if self.components_created:
            for component in self.ui_manager.components:
                if isinstance(component, ModernSlider):
                    component.value = audio_manager.volume
                    break
    
    def update(self):
        """Atualiza animações e componentes"""
        current_time = time.time()
        
        # Animação da engrenagem
        if self.settings_open:
            self.gear_rotation += 2  # Rotação quando aberto
            self.gear_glow = 70 + 30 * math.sin(current_time * 4)
        else:
            self.gear_rotation += 0.5  # Rotação lenta quando fechado
            self.gear_glow = 20 + 10 * math.sin(current_time * 2)
        
        # Manter rotação dentro de 360 graus
        self.gear_rotation = self.gear_rotation % 360
        
        # Atualizar barras de volume
        if self.equalizer_active:
            self.update_volume_bars()
        
        # Atualizar componentes UI
        if self.settings_open and self.components_created:
            self.ui_manager.update()
    
    def draw_modern_gear(self, surface: pygame.Surface):
        """Desenha o ícone de engrenagem moderno"""
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.gear_rect.collidepoint(mouse_pos)
        
        # Efeito de hover
        hover_scale = 1.1 if is_hovered else 1.0
        current_size = int(40 * hover_scale)
        
        # Centro da engrenagem
        center_x = self.gear_rect.centerx
        center_y = self.gear_rect.centery
        
        # Brilho de fundo
        if self.gear_glow > 0:
            glow_radius = int(30 + self.gear_glow * 0.3)
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            glow_color = (*UITheme.PRIMARY, int(self.gear_glow))
            pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
            surface.blit(glow_surface, (center_x - glow_radius, center_y - glow_radius))
        
        # Sombra da engrenagem
        shadow_offset = 3
        shadow_surface = pygame.Surface((current_size + 10, current_size + 10), pygame.SRCALPHA)
        self.draw_gear_shape(shadow_surface, (current_size + 10) // 2, (current_size + 10) // 2, 
                           current_size // 2, UITheme.SHADOW_COLOR[:3], self.gear_rotation)
        surface.blit(shadow_surface, (center_x - (current_size + 10) // 2 + shadow_offset, 
                                    center_y - (current_size + 10) // 2 + shadow_offset))
        
        # Engrenagem principal
        gear_color = tuple(min(255, c + 40) for c in UITheme.PRIMARY) if is_hovered else UITheme.PRIMARY
        self.draw_gear_shape(surface, center_x, center_y, current_size // 2, gear_color, self.gear_rotation)
        
        # Centro da engrenagem
        center_radius = current_size // 6
        pygame.draw.circle(surface, UITheme.BG_DARK, (center_x, center_y), center_radius)
        pygame.draw.circle(surface, gear_color, (center_x, center_y), center_radius - 2)
    
    def draw_gear_shape(self, surface: pygame.Surface, x: int, y: int, radius: int, 
                       color: Tuple[int, int, int], rotation: float):
        """Desenha formato de engrenagem"""
        # Número de dentes da engrenagem
        teeth = 8
        inner_radius = radius * 0.7
        tooth_height = radius * 0.3
        
        points = []
        
        for i in range(teeth * 2):
            angle = (i * 180 / teeth + rotation) * math.pi / 180
            
            if i % 2 == 0:  # Ponta do dente
                r = radius + tooth_height
            else:  # Base do dente
                r = inner_radius
            
            point_x = x + r * math.cos(angle)
            point_y = y + r * math.sin(angle)
            points.append((point_x, point_y))
        
        if len(points) > 2:
            pygame.draw.polygon(surface, color, points)
    
    def draw_volume_equalizer(self, surface: pygame.Surface):
        """Desenha equalizador de volume na interface"""
        if not self.settings_open or not self.equalizer_active:
            return
        
        eq_x = self.panel_x + 30
        eq_y = self.panel_y + 200
        bar_width = 15
        max_height = 40
        spacing = 3
        
        for i, bar_data in enumerate(self.volume_bars):
            bar_x = eq_x + i * (bar_width + spacing)
            bar_height = min(max_height, bar_data['height'])
            intensity = bar_data['intensity']
            
            # Cor baseada na intensidade
            if intensity > 0.8:
                bar_color = UITheme.DANGER
            elif intensity > 0.5:
                bar_color = UITheme.WARNING
            else:
                bar_color = UITheme.SUCCESS
            
            # Desenhar barra
            bar_rect = pygame.Rect(bar_x, eq_y + max_height - bar_height, bar_width, bar_height)
            
            # Gradiente na barra
            for j in range(int(bar_height)):
                alpha = 255 - int(j * 100 / bar_height)
                color = (*bar_color, alpha)
                line_surface = pygame.Surface((bar_width, 1), pygame.SRCALPHA)
                line_surface.fill(color)
                surface.blit(line_surface, (bar_x, eq_y + max_height - bar_height + j))
            
            # Borda da barra
            pygame.draw.rect(surface, tuple(min(255, c + 50) for c in bar_color), bar_rect, 1)
    
    def draw_volume_info(self, surface: pygame.Surface):
        """Desenha informações de volume"""
        if not self.settings_open:
            return
        
        # Volume percentage
        volume_text = f"Volume: {audio_manager.get_volume_percentage()}%"
        # enhanced_font_renderer.render_body_text(  # Comentado - módulo não existe
        #     volume_text, 
        #     self.panel_x + 30, 
        #     self.panel_y + 50, 
        #     surface,
        #     UITheme.TEXT_PRIMARY
        # )
        
        # Status do áudio
        status_text = "🔇 MUDO" if audio_manager.is_muted() else "🔊 ÁUDIO ATIVO"
        status_color = UITheme.DANGER if audio_manager.is_muted() else UITheme.SUCCESS
        # enhanced_font_renderer.render_body_text(  # Comentado - módulo não existe
        #     status_text,
        #     self.panel_x + 200,
        #     self.panel_y + 50,
        #     surface,
        #     status_color
        # )
    
    def draw(self, surface: pygame.Surface):
        """Desenha todo o sistema de configurações"""
        # Desenhar engrenagem
        self.draw_modern_gear(surface)
        
        if self.settings_open:
            # Desenhar componentes UI
            if self.components_created:
                self.ui_manager.draw(surface)
            
            # Desenhar informações adicionais
            self.draw_volume_info(surface)
            self.draw_volume_equalizer(surface)
            
            # Instruções
            instructions = [
                "⌨️ ↑↓ Ajustar Volume | M Mutar",
                "🖱️ Clique e Arraste no Slider",
                "⚙️ ESC Fechar Menu"
            ]
            
            for i, instruction in enumerate(instructions):
                # enhanced_font_renderer.render_instruction(  # Comentado - módulo não existe
                #     instruction,
                #     self.panel_x + self.panel_width // 2,
                #     self.panel_y + self.panel_height - 40 + i * 15,
                #     surface,
                #     UITheme.TEXT_MUTED
                # )
                pass  # Placeholder para manter estrutura

# Instância global do gerenciador moderno
modern_settings_manager = ModernSettingsManager()