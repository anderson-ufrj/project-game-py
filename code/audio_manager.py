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
            # Controles separados para música e efeitos
            self.music_volume = 0.5
            self.sfx_volume = 0.5
            self.music_muted = False
            self.sfx_muted = False
            
            # Cache de sons carregados para performance
            self.loaded_sounds = {}
            
            # Mapeamento de sons para facilitar o uso
            self.sound_paths = {
                'heal': '../audio/heal.wav',
                'walk': '../audio/walk.wav', 
                'stomp': '../audio/stomp.wav',
                'ambience': '../audio/Light Ambience 1.mp3',
                'sword': '../audio/sword.wav',
                'hit': '../audio/hit.wav',
                'monster_scream': '../audio/monsterScream.wav',
                'bigboi_death': '../audio/bigboi death.wav',
                'slash': '../audio/attack/slash.wav',
                'claw': '../audio/attack/claw.wav',
                'fireball': '../audio/attack/fireball.wav'
            }
            
            # Canais dedicados para diferentes tipos de som
            self.channels = {
                'movement': 1,    # Sons de movimento (walking, running)
                'combat': 2,      # Sons de combate (attack, hit)
                'collection': 3,  # Sons de coleta (pickup, heal)
                'environment': 4, # Sons de ambiente
                'ui': 5          # Sons de interface
            }
            
            self.current_music = None
            self._initialized = True
            print("🎵 AudioManager inicializado com controles separados")
    
    # Métodos de controle de música
    def set_music_volume(self, volume):
        """Define o volume da música de fundo (0.0 a 1.0)"""
        new_volume = max(0.0, min(1.0, volume))
        # Só imprime se o volume mudou significativamente (mais de 5%)
        if abs(new_volume - self.music_volume) > 0.05:
            print(f"🎵 Volume da música: {int(new_volume * 100)}%")
        self.music_volume = new_volume
        self._apply_music_volume()
    
    def set_sfx_volume(self, volume):
        """Define o volume dos efeitos sonoros (0.0 a 1.0)"""
        new_volume = max(0.0, min(1.0, volume))
        # Só imprime se o volume mudou significativamente (mais de 5%)
        if abs(new_volume - self.sfx_volume) > 0.05:
            print(f"🔊 Volume dos efeitos: {int(new_volume * 100)}%")
        self.sfx_volume = new_volume
    
    def toggle_music_mute(self):
        """Liga/desliga apenas a música de fundo"""
        self.music_muted = not self.music_muted
        self._apply_music_volume()
        status = "MUDO" if self.music_muted else f"{int(self.music_volume * 100)}%"
        print(f"🎵 Música: {status}")
    
    def toggle_sfx_mute(self):
        """Liga/desliga apenas os efeitos sonoros"""
        self.sfx_muted = not self.sfx_muted
        status = "MUDO" if self.sfx_muted else f"{int(self.sfx_volume * 100)}%"
        print(f"🔊 Efeitos: {status}")
    
    def _apply_music_volume(self):
        """Aplica o volume atual à música"""
        effective_volume = 0.0 if self.music_muted else self.music_volume
        pygame.mixer.music.set_volume(effective_volume)
    
    # Métodos de compatibilidade com código existente
    def set_volume(self, volume):
        """Define volume global - mantido para compatibilidade"""
        self.set_music_volume(volume)
        self.set_sfx_volume(volume)
    
    def toggle_mute(self):
        """Liga/desliga todo o som - mantido para compatibilidade"""
        self.toggle_music_mute()
        self.toggle_sfx_mute()
    
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
            self._apply_music_volume()  # Garante que o volume está correto
            print(f"▶️ Reproduzindo música (volume: {int(self.music_volume * 100)}%)")
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
    
    # Novos métodos para efeitos sonoros
    def load_sound(self, sound_file):
        """Carrega um efeito sonoro no cache"""
        if sound_file not in self.loaded_sounds:
            try:
                self.loaded_sounds[sound_file] = pygame.mixer.Sound(sound_file)
                print(f"🔊 Som carregado: {sound_file}")
            except Exception as e:
                print(f"❌ Erro ao carregar som {sound_file}: {e}")
                return None
        return self.loaded_sounds[sound_file]
    
    def play_sound(self, sound_file, category='environment', loops=0):
        """Reproduz um efeito sonoro com controle de volume"""
        if self.sfx_muted:
            return None
        
        # Permitir uso por nome ou caminho completo
        if sound_file in self.sound_paths:
            sound_file = self.sound_paths[sound_file]
            
        sound = self.load_sound(sound_file)
        if sound:
            try:
                # Definir volume do som baseado no volume de efeitos
                sound.set_volume(self.sfx_volume)
                
                # Usar canal dedicado se especificado
                if category in self.channels:
                    channel = pygame.mixer.Channel(self.channels[category])
                    return channel.play(sound, loops=loops)
                else:
                    return sound.play(loops=loops)
            except Exception as e:
                print(f"❌ Erro ao reproduzir som {sound_file}: {e}")
        return None
    
    def play_sound_by_name(self, sound_name, category='environment', loops=0):
        """Reproduz um som por nome (método conveniente)"""
        return self.play_sound(sound_name, category, loops)
    
    def stop_all_sounds(self):
        """Para todos os efeitos sonoros"""
        pygame.mixer.stop()
        print("⏹️ Todos os efeitos sonoros parados")
    
    def stop_sound_category(self, category):
        """Para sons de uma categoria específica"""
        if category in self.channels:
            channel = pygame.mixer.Channel(self.channels[category])
            channel.stop()
            print(f"⏹️ Sons de {category} parados")
    
    # Métodos de informação atualizados
    def get_music_volume_percentage(self):
        """Retorna o volume da música em porcentagem"""
        return int(self.music_volume * 100)
    
    def get_sfx_volume_percentage(self):
        """Retorna o volume dos efeitos em porcentagem"""
        return int(self.sfx_volume * 100)
    
    def get_volume_percentage(self):
        """Retorna o volume da música em porcentagem - compatibilidade"""
        return self.get_music_volume_percentage()
    
    def is_music_muted(self):
        """Verifica se a música está muda"""
        return self.music_muted
    
    def is_sfx_muted(self):
        """Verifica se os efeitos estão mudos"""
        return self.sfx_muted
    
    def is_muted(self):
        """Verifica se está mudo - compatibilidade"""
        return self.music_muted and self.sfx_muted
    
    # Propriedades de compatibilidade com código existente
    @property
    def volume(self):
        """Propriedade de compatibilidade - retorna volume da música"""
        return self.music_volume
    
    @volume.setter
    def volume(self, value):
        """Propriedade de compatibilidade - define volume da música"""
        self.set_music_volume(value)
    
    @property
    def muted(self):
        """Propriedade de compatibilidade - retorna se música está muda"""
        return self.music_muted
    
    @muted.setter 
    def muted(self, value):
        """Propriedade de compatibilidade - define mute da música"""
        if value != self.music_muted:
            self.toggle_music_mute()

# Instância global
audio_manager = AudioManager()