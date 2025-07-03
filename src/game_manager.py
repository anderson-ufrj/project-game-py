"""
Gerenciador principal do jogo Icarus - Versão Moderna
"""
import pygame
import sys
from src.config import WIDTH, HEIGHT, GAME_STATES, FPS
from src.scenes.modern_menu import ModernMainMenu
from src.scenes.modern_credits import ModernCreditsScreen

class GameManager:
    def __init__(self):
        # Inicialização do Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Configuração da tela
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Projeto Ícaro - Jogo de Plataforma Mitológico")
        
        # Controle de tempo
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Estado atual do jogo
        self.current_state = GAME_STATES['MENU']
        
        # Inicialização das cenas modernas
        self.main_menu = ModernMainMenu()
        self.credits_screen = ModernCreditsScreen()
        
        # Cursor personalizado
        pygame.mouse.set_visible(True)
        
        # Ícone da janela (se existir)
        try:
            icon = pygame.image.load('images/placeangel.png')
            pygame.display.set_icon(icon)
        except:
            pass  # Se não conseguir carregar o ícone, continua sem ele
    
    def handle_events(self):
        """Processa todos os eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Eventos específicos de cada estado
            if self.current_state == GAME_STATES['MENU']:
                result = self.main_menu.handle_event(event)
                if result == 'QUIT':
                    self.running = False
                elif result == GAME_STATES['PLAYING']:
                    # Aqui posteriormente vamos iniciar o jogo
                    print("🚀 Iniciando jogo... (Em desenvolvimento)")
                elif result == GAME_STATES['CREDITS']:
                    self.current_state = GAME_STATES['CREDITS']
                elif result == 'FULLSCREEN':
                    self.toggle_fullscreen()
            
            elif self.current_state == GAME_STATES['CREDITS']:
                result = self.credits_screen.handle_event(event)
                if result == GAME_STATES['MENU']:
                    self.current_state = GAME_STATES['MENU']
            
            # Teclas globais
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE and self.current_state == GAME_STATES['MENU']:
                    self.running = False
    
    def update(self):
        """Atualiza a lógica do jogo"""
        dt = self.clock.tick(FPS) / 1000.0  # Delta time em segundos
        
        if self.current_state == GAME_STATES['MENU']:
            self.main_menu.update(dt)
        elif self.current_state == GAME_STATES['CREDITS']:
            self.credits_screen.update(dt)
    
    def draw(self):
        """Renderiza tudo na tela"""
        if self.current_state == GAME_STATES['MENU']:
            self.main_menu.draw(self.screen)
        elif self.current_state == GAME_STATES['CREDITS']:
            self.credits_screen.draw(self.screen)
        
        # Atualiza a tela
        pygame.display.flip()
    
    def toggle_fullscreen(self):
        """Alterna entre tela cheia e janela"""
        flags = self.screen.get_flags()
        if flags & pygame.FULLSCREEN:
            pygame.display.set_mode((WIDTH, HEIGHT))
        else:
            pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    
    def run(self):
        """Loop principal do jogo"""
        print("🎮 Iniciando Projeto Ícaro - Modern Edition...")
        print(f"📐 Resolução: {WIDTH}x{HEIGHT} (HD Optimized)")
        print(f"⚡ FPS Target: {FPS}")
        print("🖱️  Controles: Mouse + Teclado + Gamepad")
        print("🔧 F11: Tela cheia | ESC: Sair")
        print("✨ Design System: Glassmorphism + Material Design 3")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()
        sys.exit()

def main():
    """Função principal"""
    game = GameManager()
    game.run()

if __name__ == "__main__":
    main()