import pygame
from settings import WIDTH, HEIGTH
from graphics_manager import GraphicsManager
from font_manager import font_manager

class GraphicsScreen:
    """Interface para configurações gráficas do jogo"""
    
    def __init__(self):
        # Garantir que pygame está inicializado
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
            
        self.graphics_manager = GraphicsManager()
        self.screen_open = False
        self.current_section = 0  # Para navegação por seções
        
        # UI positioning
        self.center_x = WIDTH // 2
        self.center_y = HEIGTH // 2
        self.menu_width = 500
        self.menu_height = 450
        self.menu_rect = pygame.Rect(
            self.center_x - self.menu_width // 2,
            self.center_y - self.menu_height // 2,
            self.menu_width,
            self.menu_height
        )
        
        # Fonts
        self.title_font = font_manager.get('large')
        self.text_font = font_manager.get('text')
        self.small_font = font_manager.get('small')
        
        # Seções do menu
        self.sections = [
            'Resolução',
            'Tela',
            'Qualidade',
            'Performance',
            'Aplicar'
        ]
        
        self.pending_changes = False
    
    def handle_keydown(self, event):
        """Handle keyboard events"""
        if not self.screen_open:
            return False
            
        if event.key == pygame.K_ESCAPE:
            self.screen_open = False
            return True
        elif event.key == pygame.K_UP:
            self.current_section = (self.current_section - 1) % len(self.sections)
            return True
        elif event.key == pygame.K_DOWN:
            self.current_section = (self.current_section + 1) % len(self.sections)
            return True
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            return self.handle_section_action()
        elif event.key == pygame.K_LEFT:
            return self.handle_left_action()
        elif event.key == pygame.K_RIGHT:
            return self.handle_right_action()
        
        return False
    
    def handle_section_action(self):
        """Ação da seção atual"""
        section = self.sections[self.current_section]
        
        if section == 'Tela':
            self.graphics_manager.toggle_fullscreen()
            self.pending_changes = True
            return True
        elif section == 'Aplicar':
            self.apply_changes()
            return True
        
        return False
    
    def handle_left_action(self):
        """Ação para tecla esquerda"""
        section = self.sections[self.current_section]
        
        if section == 'Resolução':
            self.cycle_resolution(-1)
            self.pending_changes = True
            return True
        elif section == 'Qualidade':
            self.cycle_quality(-1)
            self.pending_changes = True
            return True
        elif section == 'Performance':
            self.cycle_fps(-1)
            self.pending_changes = True
            return True
        
        return False
    
    def handle_right_action(self):
        """Ação para tecla direita"""
        section = self.sections[self.current_section]
        
        if section == 'Resolução':
            self.cycle_resolution(1)
            self.pending_changes = True
            return True
        elif section == 'Qualidade':
            self.cycle_quality(1)
            self.pending_changes = True
            return True
        elif section == 'Performance':
            self.cycle_fps(1)
            self.pending_changes = True
            return True
        
        return False
    
    def cycle_resolution(self, direction):
        """Navega entre resoluções"""
        resolutions = self.graphics_manager.supported_resolutions
        current = self.graphics_manager.get_resolution()
        current_str = f"{current[0]}x{current[1]}"
        
        try:
            current_index = resolutions.index(current_str)
        except ValueError:
            current_index = 0
        
        new_index = (current_index + direction) % len(resolutions)
        self.graphics_manager.set_resolution(resolutions[new_index])
    
    def cycle_quality(self, direction):
        """Navega entre qualidades"""
        qualities = ['low', 'medium', 'high']
        current = self.graphics_manager.get_quality()
        
        try:
            current_index = qualities.index(current)
        except ValueError:
            current_index = 2  # high
        
        new_index = (current_index + direction) % len(qualities)
        self.graphics_manager.set_quality(qualities[new_index])
    
    def cycle_fps(self, direction):
        """Navega entre limites de FPS"""
        fps_options = [30, 60, 120, 144, 0]  # 0 = sem limite
        current = self.graphics_manager.get_fps_limit()
        
        try:
            current_index = fps_options.index(current)
        except ValueError:
            current_index = 1  # 60 FPS
        
        new_index = (current_index + direction) % len(fps_options)
        self.graphics_manager.set_fps_limit(fps_options[new_index])
    
    def handle_mouse_click(self, mouse_pos):
        """Handle mouse clicks"""
        if not self.screen_open:
            return False
        
        # Check if clicked outside menu to close
        if not self.menu_rect.collidepoint(mouse_pos):
            self.screen_open = False
            return True
        
        # Check section clicks
        for i, section in enumerate(self.sections):
            section_y = self.menu_rect.y + 80 + i * 60
            section_rect = pygame.Rect(self.menu_rect.x + 20, section_y, self.menu_width - 40, 50)
            
            if section_rect.collidepoint(mouse_pos):
                self.current_section = i
                self.handle_section_action()
                return True
        
        return True  # Consumed the click
    
    def apply_changes(self):
        """Aplica as mudanças pendentes"""
        if self.pending_changes:
            success = self.graphics_manager.apply_settings()
            if success:
                self.pending_changes = False
                # Fechar menu após aplicar
                self.screen_open = False
            return success
        return True
    
    def open_screen(self):
        """Abre a tela de configurações"""
        self.screen_open = True
        self.current_section = 0
    
    def close_screen(self):
        """Fecha a tela de configurações"""
        self.screen_open = False
    
    def is_open(self):
        """Verifica se a tela está aberta"""
        return self.screen_open
    
    def draw(self, surface):
        """Desenha a interface de configurações gráficas"""
        if not self.screen_open:
            return
        
        # Overlay escuro
        overlay = pygame.Surface((WIDTH, HEIGTH))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Menu shadow
        shadow_rect = pygame.Rect(
            self.menu_rect.x + 5, self.menu_rect.y + 5,
            self.menu_rect.width, self.menu_rect.height
        )
        pygame.draw.rect(surface, (10, 10, 10), shadow_rect, border_radius=15)
        
        # Menu background
        pygame.draw.rect(surface, (40, 40, 40), self.menu_rect, border_radius=15)
        pygame.draw.rect(surface, (120, 120, 120), self.menu_rect, 3, border_radius=15)
        
        # Header
        header_rect = pygame.Rect(
            self.menu_rect.x, self.menu_rect.y,
            self.menu_rect.width, 60
        )
        pygame.draw.rect(surface, (60, 60, 60), header_rect, 
                        border_top_left_radius=15, border_top_right_radius=15)
        
        # Title
        title_text = self.title_font.render("🖥️ CONFIGURAÇÕES GRÁFICAS", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=self.menu_rect.centerx, y=self.menu_rect.y + 20)
        surface.blit(title_text, title_rect)
        
        # Current display info
        display_info = self.graphics_manager.get_display_info()
        current_res = display_info['current_resolution']
        info_text = self.small_font.render(f"Atual: {current_res}", True, (200, 200, 200))
        info_rect = info_text.get_rect(centerx=self.menu_rect.centerx, y=self.menu_rect.y + 45)
        surface.blit(info_text, info_rect)
        
        # Sections
        for i, section in enumerate(self.sections):
            y_pos = self.menu_rect.y + 80 + i * 60
            
            # Section background
            section_rect = pygame.Rect(self.menu_rect.x + 20, y_pos, self.menu_width - 40, 50)
            
            if i == self.current_section:
                # Highlighted section
                pygame.draw.rect(surface, (80, 80, 120), section_rect, border_radius=8)
                pygame.draw.rect(surface, (150, 150, 200), section_rect, 2, border_radius=8)
                text_color = (255, 255, 255)
            else:
                # Normal section
                pygame.draw.rect(surface, (60, 60, 60), section_rect, border_radius=8)
                text_color = (200, 200, 200)
            
            # Section text
            section_text = self.text_font.render(section, True, text_color)
            text_rect = section_text.get_rect(x=section_rect.x + 15, centery=section_rect.centery)
            surface.blit(section_text, text_rect)
            
            # Section value
            value_text = self.get_section_value(section)
            if value_text:
                value_surface = self.small_font.render(value_text, True, text_color)
                value_rect = value_surface.get_rect(right=section_rect.right - 15, centery=section_rect.centery)
                surface.blit(value_surface, value_rect)
        
        # Instructions
        instructions_y = self.menu_rect.bottom - 60
        instructions = [
            "↑↓ Navegar | ←→ Alterar | ENTER Ação | ESC Sair",
            "🖱️ Mouse: Clique nas opções"
        ]
        
        for i, instruction in enumerate(instructions):
            instr_text = self.small_font.render(instruction, True, (160, 160, 160))
            instr_rect = instr_text.get_rect(centerx=self.menu_rect.centerx, y=instructions_y + i * 20)
            surface.blit(instr_text, instr_rect)
        
        # Pending changes indicator
        if self.pending_changes:
            changes_text = self.small_font.render("⚠️ Alterações pendentes - Clique em Aplicar", True, (255, 255, 100))
            changes_rect = changes_text.get_rect(centerx=self.menu_rect.centerx, y=self.menu_rect.bottom - 25)
            surface.blit(changes_text, changes_rect)
    
    def get_section_value(self, section):
        """Retorna o valor atual da seção"""
        if section == 'Resolução':
            res = self.graphics_manager.get_resolution()
            return f"{res[0]}x{res[1]}"
        elif section == 'Tela':
            return "Tela Cheia" if self.graphics_manager.is_fullscreen() else "Janela"
        elif section == 'Qualidade':
            quality = self.graphics_manager.get_quality()
            quality_names = {'low': 'Baixa', 'medium': 'Média', 'high': 'Alta'}
            return quality_names.get(quality, quality)
        elif section == 'Performance':
            fps = self.graphics_manager.get_fps_limit()
            return f"{fps} FPS" if fps > 0 else "Sem Limite"
        elif section == 'Aplicar':
            return "💾 Salvar" if self.pending_changes else "✅ Salvo"
        
        return None