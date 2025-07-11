# 🎵 Sistema de Áudio

## 📋 Visão Geral

O sistema de áudio do jogo utiliza o padrão Singleton thread-safe para gerenciar toda a reprodução de sons e música, garantindo consistência e controle centralizado.

## 🏗️ Arquitetura

### AudioManager (Singleton)

```python
class AudioManager:
    _instance = None
    _lock = threading.Lock()
    _initialized = False
```

### Características
- **Thread-Safe**: Usa threading.Lock() para evitar condições de corrida
- **Singleton**: Garante única instância global
- **Cache**: Armazena sons carregados para otimização
- **Canais Dedicados**: Separa tipos de sons em canais

## 🎼 Componentes do Sistema

### 1. **Música de Fundo**

#### Arquivos Disponíveis
| Arquivo | Uso | Loop |
|---------|-----|------|
| home.mp3 | Menu principal | Sim |
| Ambient 2.mp3 | Levels 1 e 2 | Sim |
| darkambience(from fable).mp3 | Level 3 | Sim |
| home.mp3 | Level 4 (boss) | Sim |

#### Controle
```python
# Tocar música
audio_manager.play_music(path, loops=-1)

# Parar música
audio_manager.stop_music()

# Ajustar volume
audio_manager.set_music_volume(0.5)
```

### 2. **Efeitos Sonoros (SFX)**

#### Categorias de Sons

##### Interface (UI)
- button_hover.wav
- button_click.wav
- menu_open.wav
- menu_close.wav

##### Combate
- sword_swing.ogg
- axe_hit.wav
- magic_cast.wav
- hit_impact.ogg
- enemy_death.wav

##### Movimento
- footstep_grass.wav
- footstep_stone.wav
- jump.wav
- land.wav

##### Coleta
- coin_collect.wav
- health_orb.wav
- key_pickup.wav
- gem_collect.ogg

##### Ambiente
- ambient_forest.wav
- ambient_dungeon.wav
- water_flow.wav
- torch_burning.wav

### 3. **Sistema de Canais**

```python
CHANNELS = {
    'movement': 0,    # Sons de movimento
    'combat': 1,      # Sons de combate
    'collect': 2,     # Sons de coleta
    'ambient': 3,     # Sons ambientes
    'ui': 4          # Sons de interface
}
```

#### Benefícios
- Evita sobreposição indevida
- Permite controle por categoria
- Otimiza uso de recursos

## 🎛️ Interface de Controle

### 1. **Controles Visuais**

#### Modern Settings UI
- **Localização**: Ícone de engrenagem no canto
- **Componentes**:
  - Slider de volume (0-100%)
  - Botão mute/unmute
  - Barras de equalização animadas
  - Indicador numérico

#### Características Visuais
- Gradientes animados
- Efeito de brilho pulsante
- Cores dinâmicas por volume
- Feedback visual imediato

### 2. **Controles por Teclado**

| Tecla | Ação |
|-------|------|
| M | Toggle mute |
| ↑ | Aumentar volume |
| ↓ | Diminuir volume |
| Click no 🔊 | Abrir controles |

## 🔧 Implementação Técnica

### 1. **Inicialização**

```python
def __init__(self):
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(8)
    
    # Estado inicial
    self.music_volume = 0.5
    self.sfx_volume = 0.5
    self.is_muted = False
```

### 2. **Cache de Sons**

```python
self._sound_cache = {}

def _get_sound(self, sound_path):
    if sound_path not in self._sound_cache:
        self._sound_cache[sound_path] = pygame.mixer.Sound(sound_path)
    return self._sound_cache[sound_path]
```

### 3. **Thread Safety**

```python
def play_sound(self, sound_name, volume=None):
    with self._lock:
        # Operações thread-safe
        sound = self._get_sound(path)
        channel.play(sound)
```

## 📊 Sistema de Volume

### Hierarquia de Volume
1. **Master Volume**: Não implementado
2. **Music Volume**: 0.0 a 1.0
3. **SFX Volume**: 0.0 a 1.0
4. **Individual Sound**: Opcional por som

### Cálculo de Volume
```python
# Volume efetivo
if self.is_muted:
    effective_volume = 0
else:
    effective_volume = base_volume * category_volume
```

## 🎯 Integração com o Jogo

### 1. **Game States**
```python
# Menu Principal
audio_manager.play_music('../audio/home.mp3')

# Ao iniciar Level 1
audio_manager.play_music('../audio/Ambient 2.mp3')

# Game Over
audio_manager.stop_music()
```

### 2. **Eventos de Gameplay**
```python
# Ataque do jogador
audio_manager.play_sound('sword_swing')

# Coleta de item
audio_manager.play_sound('collect_orb')

# Morte de inimigo
audio_manager.play_sound('enemy_death')
```

### 3. **Feedback de UI**
```python
# Hover em botão
audio_manager.play_sound('button_hover', channel='ui')

# Click em botão
audio_manager.play_sound('button_click', channel='ui')
```

## 💾 Persistência

### Configurações Salvas
```json
{
    "music_volume": 0.7,
    "sfx_volume": 0.5,
    "is_muted": false
}
```

### Integração com Save System
- Volume é salvo junto com o progresso
- Restaurado ao carregar save
- Mantido entre sessões

## 🎨 Feedback Visual do Áudio

### 1. **Equalizer Bars**
- 15 barras verticais
- Animação baseada no volume
- Cores: Verde → Amarelo → Vermelho
- Movimento senoidal simulado

### 2. **Ícones de Estado**
- 🔊 Volume normal
- 🔇 Mudo
- 🎵 Tocando música
- 🔈 Volume baixo

### 3. **Animações**
- Ripple effect ao clicar
- Pulsação do slider
- Transições suaves

## 🐛 Compatibilidade e Fallbacks

### 1. **Formatos Suportados**
- MP3 (música)
- OGG (efeitos longos)
- WAV (efeitos curtos)

### 2. **Tratamento de Erros**
```python
try:
    sound = pygame.mixer.Sound(path)
except pygame.error:
    print(f"Erro ao carregar: {path}")
    return None
```

### 3. **Fallbacks**
- Som não encontrado: Log silencioso
- Mixer não inicializado: Tenta reinicializar
- Canal ocupado: Usa próximo disponível

## ⚡ Otimizações

### 1. **Performance**
- Cache de sons carregados
- Canais pré-alocados
- Lazy loading de sons

### 2. **Memória**
- Limite de cache (não implementado)
- Compressão de áudio adequada
- Limpeza de sons não usados (futuro)

### 3. **Qualidade**
- Sample rate: 44100 Hz
- Bit depth: 16 bits
- Channels: Stereo
- Buffer: 4096 bytes

## 🔮 Melhorias Futuras

### Planejadas
1. **3D Audio**: Posicionamento espacial
2. **Dynamic Music**: Música adaptativa
3. **Sound Variations**: Múltiplas versões
4. **Master Volume**: Controle global
5. **Audio Profiles**: Presets de áudio

### Consideradas
1. Fade in/out automático
2. Crossfade entre músicas
3. Ducking (reduzir música em diálogos)
4. Reverb por ambiente
5. Compressor/limiter

## 🎯 Boas Práticas

### Do's
- Sempre usar o AudioManager
- Cachear sons frequentes
- Usar canais apropriados
- Testar com volume 0 e 100%

### Don'ts
- Não criar Sound objects diretamente
- Não modificar volume do mixer global
- Não tocar sons em loops tight
- Não ignorar erros de carregamento

---

[← Voltar: Sistema de Combate](./combate.md) | [Índice](../README.md) | [Próximo: Sistema Gráfico →](./graficos.md)