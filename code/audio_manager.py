import pygame
import threading

class AudioManager:
    """Gerenciador centralizado de áudio para todo o jogo"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton - garante uma única instância"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AudioManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.volume = 0.5
            self.muted = False
            self.current_music = None
            self._initialized = True
            print("🎵 AudioManager inicializado")
    
    def set_volume(self, volume):
        """Define o volume global (0.0 a 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        self._apply_volume()
        print(f"🔊 Volume definido para: {int(self.volume * 100)}%")
    
    def toggle_mute(self):
        """Liga/desliga o som"""
        self.muted = not self.muted
        self._apply_volume()
        status = "MUDO" if self.muted else f"SOM ({int(self.volume * 100)}%)"
        print(f"🔇 Estado do som: {status}")
    
    def _apply_volume(self):
        """Aplica o volume atual ao pygame"""
        effective_volume = 0.0 if self.muted else self.volume
        pygame.mixer.music.set_volume(effective_volume)
    
    def load_music(self, music_file):
        """Carrega uma nova música"""
        try:
            if self.current_music != music_file:
                pygame.mixer.music.load(music_file)
                self.current_music = music_file
                print(f"🎵 Música carregada: {music_file}")
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar música {music_file}: {e}")
            return False
    
    def play_music(self, music_file=None, loops=-1):
        """Reproduz música (loops=-1 para loop infinito)"""
        try:
            if music_file and self.load_music(music_file):
                pass  # Música já carregada
            
            pygame.mixer.music.play(loops)
            self._apply_volume()  # Garante que o volume está correto
            print(f"▶️ Reproduzindo música (volume: {int(self.volume * 100)}%)")
            return True
        except Exception as e:
            print(f"❌ Erro ao reproduzir música: {e}")
            return False
    
    def stop_music(self):
        """Para a música"""
        pygame.mixer.music.stop()
        print("⏹️ Música parada")
    
    def is_playing(self):
        """Verifica se a música está tocando"""
        return pygame.mixer.music.get_busy()
    
    def get_volume_percentage(self):
        """Retorna o volume em porcentagem"""
        return int(self.volume * 100)
    
    def is_muted(self):
        """Verifica se está mudo"""
        return self.muted

# Instância global
audio_manager = AudioManager()