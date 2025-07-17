import pygame
import math
import time
from typing import List, Dict, Tuple, Optional
from settings import WIDTH, HEIGTH
from ui_system import UIManager, ModernPanel, ModernButton, UITheme
from font_manager import font_manager

# Importar sistema de fontes melhorado se disponível
try:
    from enhanced_font_system import EnhancedFontRenderer
    enhanced_font_renderer = EnhancedFontRenderer()
    ENHANCED_FONTS_AVAILABLE = True
except ImportError:
    ENHANCED_FONTS_AVAILABLE = False
    enhanced_font_renderer = None  # Definir como None para evitar erro de referência
    print("⚠️ Sistema de fontes melhorado não disponível - usando fallback")

class TutorialStep:
    """Representa um passo do tutorial"""
    
    def __init__(self, title: str, content: List[str], image_path: Optional[str] = None,
                 controls: Optional[List[str]] = None):
        self.title = title
        self.content = content
        self.image_path = image_path
        self.controls = controls or []
        self.completed = False

class InteractiveTutorial:
    """Sistema de tutorial interativo com UI moderna"""
    
    def __init__(self):
        self.active = False
        self.current_step = 0
        self.ui_manager = UIManager()
        self.components_created = False
        
        # Layout
        self.panel_width = 800
        self.panel_height = 600
        self.panel_x = (WIDTH - self.panel_width) // 2
        self.panel_y = (HEIGTH - self.panel_height) // 2
        
        # Animações
        self.step_transition = 0.0
        self.content_alpha = 255
        
        # Criar passos do tutorial
        self.tutorial_steps = self.create_tutorial_steps()
        
        # Efeitos visuais
        self.particles = []
        self.create_particles()
    
    def create_tutorial_steps(self) -> List[TutorialStep]:
        """Cria todos os passos do tutorial"""
        steps = [
            TutorialStep(
                "🎮 BEM-VINDO À CORRIDA PELA RELÍQUIA!",
                [
                    "Embarque numa aventura épica em busca da misteriosa Gema Eldritch!",
                    "Explore 4 níveis únicos, derrote inimigos poderosos e colete itens mágicos.",
                    "Este tutorial te guiará pelos controles e mecânicas básicas do jogo.",
                    "",
                    "Pressione PRÓXIMO para começar sua jornada!"
                ]
            ),
            
            TutorialStep(
                "🚶 MOVIMENTO E NAVEGAÇÃO",
                [
                    "Use as SETAS DO TECLADO ou WASD para mover seu personagem.",
                    "Segure SHIFT para correr mais rápido (consome energia).",
                    "Explore cada área completamente para encontrar itens secretos!",
                    "",
                    "💡 Dica: Correr é útil para escapar de inimigos, mas use com moderação."
                ],
                controls=["⬆️ W / ↑", "⬇️ S / ↓", "⬅️ A / ←", "➡️ D / →", "🏃 SHIFT + movimento"]
            ),
            
            TutorialStep(
                "⚔️ SISTEMA DE COMBATE",
                [
                    "Pressione ESPAÇO para atacar inimigos próximos.",
                    "O ataque tem alcance de 360°, atingindo todos os inimigos ao redor!",
                    "Use Q para trocar entre 5 armas diferentes (cada uma tem dano único).",
                    "Cada arma tem um tempo de recarga - use estrategicamente!",
                    "",
                    "💡 Dica: Experimente diferentes armas para encontrar sua favorita."
                ],
                controls=["⚔️ ESPAÇO", "🗡️ Q (trocar arma)", "🎯 Ataque 360°"]
            ),
            
            TutorialStep(
                "✨ SISTEMA DE MAGIAS",
                [
                    "Pressione E para alternar entre magias: Chama e Cura.",
                    "Use CTRL para lançar a magia selecionada (consome energia).",
                    "🔥 CHAMA: Causa dano em área aos inimigos.",
                    "💚 CURA: Restaura sua vida (muito útil em situações difíceis).",
                    "",
                    "💡 Dica: Gerencie sua energia! Magias são poderosas mas custosas."
                ],
                controls=["✨ E (trocar magia)", "🎭 CTRL (usar magia)", "⚡ Consome energia"]
            ),
            
            TutorialStep(
                "💎 COLETA DE ITENS",
                [
                    "Colete gemas azuis para aumentar sua energia máxima.",
                    "Orbs vermelhos restauram sua vida instantaneamente.",
                    "Orbs dourados aumentam seu dano de ataque.",
                    "🗝️ CHAVES são essenciais para progredir no Nível 3!",
                    "",
                    "💡 Dica: Alguns itens estão escondidos - explore tudo!"
                ],
                controls=["💎 Gemas (energia)", "❤️ Orbs vermelhos (vida)", "⚡ Orbs dourados (ataque)"]
            ),
            
            TutorialStep(
                "🗺️ NAVEGAÇÃO AVANÇADA",
                [
                    "No Nível 3, pressione TAB para abrir o minimapa interativo.",
                    "O minimapa mostra sua posição, chaves coletadas e a saída.",
                    "Você precisa de 3 chaves para desbloquear a saída do Nível 3.",
                    "Use o minimapa para se orientar no labirinto complexo!",
                    "",
                    "💡 Dica: O minimapa é sua ferramenta mais valiosa no Nível 3."
                ],
                controls=["🗺️ TAB (minimapa)", "🗝️ 3 chaves necessárias", "🚪 Saída desbloqueável"]
            ),
            
            TutorialStep(
                "⚙️ CONFIGURAÇÕES E CONTROLES",
                [
                    "Clique no ícone ⚙️ ou pressione M para controles de áudio.",
                    "Use ↑↓ para ajustar volume, M para mutar/desmutar.",
                    "Pressione G para configurações gráficas avançadas.",
                    "F5 = Quick Save | F9 = Quick Load | F6 = Menu de Saves",
                    "",
                    "💡 Dica: Salve frequentemente para não perder progresso!"
                ],
                controls=["⚙️ Configurações", "🔊 M (mute)", "🖥️ G (gráficos)", "💾 F5/F6/F9"]
            ),
            
            TutorialStep(
                "🏆 SISTEMA DE DIFICULDADE",
                [
                    "Escolha entre 3 níveis de dificuldade:",
                    "🟢 FÁCIL: Vida e energia maiores, inimigos mais fracos",
                    "🟡 NORMAL: Experiência balanceada e desafiadora",
                    "🔴 DIFÍCIL: Para jogadores experientes que buscam desafio!",
                    "",
                    "💡 Dica: Comece no Fácil se for sua primeira vez jogando."
                ],
                controls=["🎮 D (menu dificuldade)", "⚡ Afeta vida/energia", "👹 Modifica inimigos"]
            ),
            
            TutorialStep(
                "📊 ESTATÍSTICAS E CONQUISTAS",
                [
                    "Pressione S para ver suas estatísticas detalhadas.",
                    "Acompanhe tempo de jogo, mortes, itens coletados e mais!",
                    "Desbloqueie 32 conquistas únicas jogando de diferentes formas.",
                    "Suas estatísticas são salvas automaticamente.",
                    "",
                    "💡 Dica: Tente desbloquear todas as conquistas para 100%!"
                ],
                controls=["📊 S (estatísticas)", "🏆 32 conquistas", "📈 Progresso automático"]
            ),
            
            TutorialStep(
                "🎯 OBJETIVO PRINCIPAL",
                [
                    "Seu objetivo é encontrar a GEMA ELDRITCH no final do Nível 4.",
                    "Cada nível tem desafios únicos e inimigos diferentes:",
                    "🌲 Nível 1: Floresta Mística",
                    "🌀 Nível 2: Labirinto das Sombras", 
                    "🏰 Nível 3: Fortaleza Sombria (com minimapa)",
                    "⚡ Nível 4: Confronto Final",
                    "",
                    "Boa sorte em sua aventura, herói! 🗡️✨"
                ]
            )
        ]
        
        return steps
    
    def create_particles(self):
        """Cria partículas decorativas para o tutorial"""
        for i in range(20):
            particle = {
                'x': WIDTH // 2 + (i - 10) * 30,
                'y': HEIGTH // 2 + math.sin(i * 0.5) * 100,
                'vx': (i - 10) * 0.1,
                'vy': math.sin(i * 0.3) * 0.5,
                'color': (100 + i * 8, 150 + i * 5, 255),
                'size': 3 + i % 3,
                'life': 255,
                'phase': i * 0.2
            }
            self.particles.append(particle)
    
    def update_particles(self):
        """Atualiza partículas decorativas"""
        current_time = time.time()
        
        for particle in self.particles:
            # Movimento
            particle['x'] += particle['vx']
            particle['y'] += particle['vy'] + math.sin(current_time * 2 + particle['phase']) * 0.3
            
            # Resetar posição se sair da tela
            if particle['x'] < -50:
                particle['x'] = WIDTH + 50
            elif particle['x'] > WIDTH + 50:
                particle['x'] = -50
            
            if particle['y'] < -50:
                particle['y'] = HEIGTH + 50
            elif particle['y'] > HEIGTH + 50:
                particle['y'] = -50
    
    def draw_particles(self, surface: pygame.Surface):
        """Desenha partículas decorativas"""
        for particle in self.particles:
            # Criar surface para partícula com alpha
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            color_with_alpha = (*particle['color'], 100)
            pygame.draw.circle(particle_surface, color_with_alpha, 
                             (particle['size'], particle['size']), particle['size'])
            
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
    
    def open_tutorial(self):
        """Abre o tutorial"""
        self.active = True
        self.current_step = 0
        self.create_ui_components()
    
    def close_tutorial(self):
        """Fecha o tutorial"""
        self.active = False
        self.ui_manager.clear_components()
        self.components_created = False
    
    def create_ui_components(self):
        """Cria componentes da interface do tutorial"""
        if self.components_created:
            self.ui_manager.clear_components()
        
        # Painel principal
        main_panel = ModernPanel(
            self.panel_x, self.panel_y, self.panel_width, self.panel_height,
            "",  # Título será desenhado separadamente
            UITheme.BG_DARK,
            UITheme.PRIMARY
        )
        self.ui_manager.add_component(main_panel)
        
        # Botões de navegação
        button_y = self.panel_y + self.panel_height - 70
        button_width = 120
        button_height = 40
        
        # Botão anterior
        if self.current_step > 0:
            prev_button = ModernButton(
                self.panel_x + 50, button_y, button_width, button_height,
                "⬅️ ANTERIOR", 'button', UITheme.SECONDARY,
                UITheme.TEXT_PRIMARY, self.previous_step
            )
            self.ui_manager.add_component(prev_button)
        
        # Botão próximo/finalizar
        if self.current_step < len(self.tutorial_steps) - 1:
            next_text = "PRÓXIMO ➡️"
            next_action = self.next_step
        else:
            next_text = "✅ FINALIZAR"
            next_action = self.close_tutorial
        
        next_button = ModernButton(
            self.panel_x + self.panel_width - button_width - 50, button_y, 
            button_width, button_height,
            next_text, 'button', UITheme.SUCCESS,
            UITheme.TEXT_PRIMARY, next_action
        )
        self.ui_manager.add_component(next_button)
        
        # Botão fechar
        close_button = ModernButton(
            self.panel_x + self.panel_width - 90, self.panel_y + 10,
            80, 30,
            "✕ SAIR", 'small', UITheme.DANGER,
            UITheme.TEXT_PRIMARY, self.close_tutorial
        )
        self.ui_manager.add_component(close_button)
        
        self.components_created = True
    
    def next_step(self):
        """Vai para o próximo passo"""
        if self.current_step < len(self.tutorial_steps) - 1:
            self.current_step += 1
            self.create_ui_components()
    
    def previous_step(self):
        """Vai para o passo anterior"""
        if self.current_step > 0:
            self.current_step -= 1
            self.create_ui_components()
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Manipula eventos do tutorial"""
        if not self.active:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close_tutorial()
                return True
            elif event.key == pygame.K_LEFT:
                self.previous_step()
                return True
            elif event.key == pygame.K_RIGHT:
                self.next_step()
                return True
        
        # Repassar eventos para UI manager
        if self.components_created:
            return self.ui_manager.handle_event(event)
        
        return True  # Consumir todos os eventos quando ativo
    
    def update(self):
        """Atualiza o tutorial"""
        if not self.active:
            return
        
        self.update_particles()
        
        if self.components_created:
            self.ui_manager.update()
    
    def draw(self, surface: pygame.Surface):
        """Desenha o tutorial"""
        if not self.active:
            return
        
        # Overlay escuro de fundo
        overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Partículas de fundo
        self.draw_particles(surface)
        
        # Componentes UI
        if self.components_created:
            self.ui_manager.draw(surface)
        
        # Conteúdo do passo atual
        self.draw_current_step(surface)
        
        # Indicador de progresso
        self.draw_progress_indicator(surface)
    
    def draw_current_step(self, surface: pygame.Surface):
        """Desenha o conteúdo do passo atual"""
        if self.current_step >= len(self.tutorial_steps):
            return
        
        step = self.tutorial_steps[self.current_step]
        
        # Título
        title_y = self.panel_y + 40
        if ENHANCED_FONTS_AVAILABLE:
            enhanced_font_renderer.render_title(
                step.title, self.panel_x + self.panel_width // 2, title_y,
                surface, UITheme.TEXT_PRIMARY, "gradient"
            )
        else:
            # Fallback usando font_manager
            title_font = font_manager.get('title')
            title_surface = title_font.render(step.title, True, UITheme.TEXT_PRIMARY)
            title_rect = title_surface.get_rect(centerx=self.panel_x + self.panel_width // 2, y=title_y)
            surface.blit(title_surface, title_rect)
        
        # Conteúdo
        content_y = title_y + 80
        line_height = 25
        
        for i, line in enumerate(step.content):
            if line.strip():  # Pular linhas vazias
                if ENHANCED_FONTS_AVAILABLE:
                    enhanced_font_renderer.render_body_text(
                        line,
                        self.panel_x + 50,
                        content_y + i * line_height,
                        surface,
                        UITheme.TEXT_SECONDARY,
                        self.panel_width - 100
                    )
                else:
                    # Fallback usando font_manager
                    content_font = font_manager.get('text')
                    content_surface = content_font.render(line, True, UITheme.TEXT_SECONDARY)
                    surface.blit(content_surface, (self.panel_x + 50, content_y + i * line_height))
        
        # Controles (se existirem)
        if step.controls:
            controls_y = content_y + len(step.content) * line_height + 30
            
            # Título dos controles
            if ENHANCED_FONTS_AVAILABLE:
                enhanced_font_renderer.render_subtitle(
                    "🎮 CONTROLES:",
                    self.panel_x + 70,
                    controls_y,
                    surface,
                    UITheme.WARNING
                )
            else:
                # Fallback usando font_manager
                subtitle_font = font_manager.get('subtitle')
                subtitle_surface = subtitle_font.render("🎮 CONTROLES:", True, UITheme.WARNING)
                surface.blit(subtitle_surface, (self.panel_x + 70, controls_y))
            
            # Lista de controles
            for i, control in enumerate(step.controls):
                if ENHANCED_FONTS_AVAILABLE:
                    enhanced_font_renderer.render_body_text(
                        f"  • {control}",
                        self.panel_x + 80,
                        controls_y + 30 + i * 20,
                        surface,
                        UITheme.SUCCESS
                    )
                else:
                    # Fallback usando font_manager
                    control_font = font_manager.get('text')
                    control_surface = control_font.render(f"  • {control}", True, UITheme.SUCCESS)
                    surface.blit(control_surface, (self.panel_x + 80, controls_y + 30 + i * 20))
    
    def draw_progress_indicator(self, surface: pygame.Surface):
        """Desenha indicador de progresso"""
        # Posição
        indicator_y = self.panel_y + self.panel_height - 25
        indicator_width = self.panel_width - 100
        indicator_x = self.panel_x + 50
        
        # Fundo da barra
        bg_rect = pygame.Rect(indicator_x, indicator_y, indicator_width, 6)
        pygame.draw.rect(surface, UITheme.BG_LIGHT, bg_rect, border_radius=3)
        
        # Progresso
        progress = (self.current_step + 1) / len(self.tutorial_steps)
        progress_width = int(indicator_width * progress)
        progress_rect = pygame.Rect(indicator_x, indicator_y, progress_width, 6)
        pygame.draw.rect(surface, UITheme.PRIMARY, progress_rect, border_radius=3)
        
        # Texto do progresso
        progress_text = f"Passo {self.current_step + 1} de {len(self.tutorial_steps)}"
        if ENHANCED_FONTS_AVAILABLE:
            enhanced_font_renderer.render_instruction(
                progress_text,
                self.panel_x + self.panel_width // 2,
                indicator_y - 15,
                surface,
                UITheme.TEXT_MUTED
            )
        else:
            # Fallback usando font_manager
            progress_font = font_manager.get('small')
            progress_surface = progress_font.render(progress_text, True, UITheme.TEXT_MUTED)
            progress_rect = progress_surface.get_rect(centerx=self.panel_x + self.panel_width // 2, y=indicator_y - 15)
            surface.blit(progress_surface, progress_rect)

# Instância global do tutorial
tutorial_system = TutorialSystem = InteractiveTutorial()