#!/usr/bin/env python3
# Teste completo do sistema de áudio

import pygame
import sys
import os

def test_audio_system():
    print("🔍 Testando Sistema de Áudio...")
    
    # Inicializar pygame
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    
    print("✅ Pygame inicializado")
    
    # Verificar se os arquivos de áudio existem
    audio_files = [
        '../audio/home.mp3',
        '../audio/Ambient 2.mp3',
        '../audio/darkambience(from fable).mp3'
    ]
    
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            print(f"✅ Encontrado: {audio_file}")
        else:
            print(f"❌ Não encontrado: {audio_file}")
    
    # Testar carregamento de música
    try:
        print("\n🎵 Testando carregamento de música...")
        pygame.mixer.music.load('../audio/home.mp3')
        print("✅ Música carregada com sucesso")
        
        # Testar volume
        print(f"🔊 Volume atual: {pygame.mixer.music.get_volume()}")
        
        # Testar diferentes volumes
        volumes = [0.0, 0.3, 0.5, 0.8, 1.0]
        for vol in volumes:
            pygame.mixer.music.set_volume(vol)
            current_vol = pygame.mixer.music.get_volume()
            print(f"   Definido: {vol} | Atual: {current_vol}")
        
        # Testar reprodução (sem som real para não incomodar)
        print("🎮 Testando reprodução...")
        pygame.mixer.music.play(-1)  # Loop infinito
        
        if pygame.mixer.music.get_busy():
            print("✅ Música está tocando")
        else:
            print("❌ Música NÃO está tocando")
        
        # Testar pause/unpause
        pygame.mixer.music.pause()
        print("⏸️ Música pausada")
        
        pygame.mixer.music.unpause()
        print("▶️ Música despausada")
        
        # Testar stop
        pygame.mixer.music.stop()
        print("⏹️ Música parada")
        
    except Exception as e:
        print(f"❌ Erro no teste de música: {e}")
    
    # Testar mixer info
    print(f"\n📊 Info do Mixer:")
    print(f"   Frequência: {pygame.mixer.get_init()[0] if pygame.mixer.get_init() else 'N/A'}")
    print(f"   Formato: {pygame.mixer.get_init()[1] if pygame.mixer.get_init() else 'N/A'}")
    print(f"   Canais: {pygame.mixer.get_init()[2] if pygame.mixer.get_init() else 'N/A'}")
    print(f"   Número de canais de som: {pygame.mixer.get_num_channels()}")
    
    pygame.quit()
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    test_audio_system()