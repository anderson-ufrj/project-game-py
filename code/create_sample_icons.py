#!/usr/bin/env python3
"""
Script para criar samples dos ícones avançados
Demonstra as capacidades do sistema de ícones
"""
import pygame
import os
from icon_manager import icon_manager

def create_icon_samples():
    """Cria samples de todos os ícones disponíveis"""
    pygame.init()
    
    # Tamanhos de teste
    sizes = [24, 32, 48, 64]
    
    # Cores de teste
    colors = [
        (255, 255, 255),   # Branco
        (64, 224, 208),    # Turquesa
        (255, 107, 107),   # Coral
        (46, 213, 115),    # Verde
        (255, 193, 7),     # Amarelo
        (255, 71, 87),     # Vermelho
    ]
    
    # Ícones disponíveis
    icons = [
        'volume_high', 'volume_medium', 'volume_low', 'volume_mute',
        'fullscreen', 'windowed', 'settings', 'music', 'sound'
    ]
    
    # Criar pasta para samples
    sample_dir = "../graphics/icon_samples"
    os.makedirs(sample_dir, exist_ok=True)
    
    for size in sizes:
        for color in colors:
            color_name = f"rgb_{color[0]}_{color[1]}_{color[2]}"
            
            # Criar surface grande para mostrar todos os ícones
            sample_surface = pygame.Surface((len(icons) * (size + 10), size + 20), pygame.SRCALPHA)
            
            # Fundo semitransparente
            pygame.draw.rect(sample_surface, (0, 0, 0, 50), sample_surface.get_rect())
            
            # Gerar cada ícone
            for i, icon_name in enumerate(icons):
                try:
                    icon_surface = icon_manager.get_icon(icon_name, size, color)
                    
                    # Posição no sample
                    x = i * (size + 10) + 5
                    y = 10
                    
                    # Desenhar ícone
                    sample_surface.blit(icon_surface, (x, y))
                    
                    # Label do ícone
                    font = pygame.font.Font(None, 12)
                    label = font.render(icon_name[:6], True, (255, 255, 255))
                    label_rect = label.get_rect(centerx=x + size//2, y=y + size + 2)
                    sample_surface.blit(label, label_rect)
                    
                except Exception as e:
                    print(f"❌ Erro ao criar ícone {icon_name}: {e}")
            
            # Salvar sample
            filename = f"icons_size_{size}_{color_name}.png"
            filepath = os.path.join(sample_dir, filename)
            pygame.image.save(sample_surface, filepath)
            print(f"✅ Sample criado: {filename}")
    
    print(f"\n🎨 Samples criados em: {sample_dir}")
    print("📖 Abra os arquivos PNG para ver os ícones renderizados")

if __name__ == "__main__":
    create_icon_samples()