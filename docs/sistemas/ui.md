# 🎨 Sistema de Interface (UI)

## 📋 Visão Geral

O sistema de UI do jogo utiliza uma arquitetura baseada em componentes com um sistema de temas centralizado, oferecendo uma interface moderna e responsiva.

## 🏗️ Arquitetura Component-Based

### Hierarquia de Componentes

```
UIComponent (base)
├── ModernButton
├── ModernSlider
├── ModernPanel
├── AnimatedText
└── Custom Components

UIManager (gerenciador central)
└── Gerencia todos os componentes
```

### UITheme (Sistema de Temas)

```python
class UITheme:
    # Cores principais
    PRIMARY = (64, 224, 208)      # Turquesa
    SECONDARY = (255, 107, 107)   # Coral
    BACKGROUND = (25, 25, 35)     # Cinza escuro
    SURFACE = (35, 35, 45)        # Cinza médio
    TEXT = (255, 255, 255)        # Branco
    TEXT_SECONDARY = (180, 180, 180) # Cinza claro
    
    # Estados
    HOVER = (80, 240, 220)
    ACTIVE = (48, 208, 192)
    DISABLED = (100, 100, 100)
    
    # Feedback
    SUCCESS = (46, 213, 115)
    WARNING = (255, 193, 7)
    ERROR = (255, 71, 87)
```

## 🧩 Componentes Principais

### 1. **UIComponent (Base)**

#### Propriedades Base
```python
- rect: pygame.Rect        # Posição e tamanho
- visible: bool           # Visibilidade
- enabled: bool           # Interatividade
- animations: dict        # Animações ativas
- hover: bool            # Estado de hover
- pressed: bool          # Estado pressionado
```

#### Métodos Principais
- `handle_event()`: Processa eventos
- `update()`: Atualiza animações
- `draw()`: Renderiza componente
- `animate()`: Inicia animação

### 2. **ModernButton**

#### Características
- Gradiente de fundo animado
- Efeito glow no hover
- Animação de scale no click
- Sombra multinível
- Texto com anti-aliasing

#### Exemplo de Uso
```python
button = ModernButton(
    x=100, y=100,
    width=200, height=50,
    text="JOGAR",
    callback=self.start_game,
    style='primary'  # ou 'secondary', 'danger'
)
```

### 3. **ModernSlider**

#### Características
- Track com gradiente
- Handle circular animado
- Drag & drop suave
- Valor numérico no handle
- Efeito de brilho pulsante

#### Exemplo de Uso
```python
slider = ModernSlider(
    x=100, y=200,
    width=300, height=40,
    min_value=0, max_value=100,
    initial_value=50,
    callback=self.on_volume_change
)
```

### 4. **ModernPanel**

#### Características
- Background com transparência
- Bordas arredondadas
- Sombra difusa
- Suporte a gradientes
- Auto-layout de conteúdo

#### Exemplo de Uso
```python
panel = ModernPanel(
    x=50, y=50,
    width=400, height=300,
    title="Configurações",
    background_alpha=0.9
)
```

## 🎭 Sistema de Animações

### Tipos de Easing

```python
def ease_in(t): return t * t
def ease_out(t): return t * (2 - t)
def ease_in_out(t): return 3*t*t - 2*t*t*t if t < 0.5 else 1 - pow(-2*t + 2, 3) / 2
def bounce(t): # Implementação complexa
```

### Propriedades Animáveis
- **scale**: Tamanho do componente
- **glow**: Intensidade do brilho
- **alpha**: Transparência
- **position**: Posição X/Y
- **rotation**: Rotação
- **color**: Transição de cor

### Exemplo de Animação
```python
button.animate('scale', 
    start_value=1.0,
    end_value=1.1,
    duration=0.3,
    easing='ease_out'
)
```

## 🎯 UIManager

### Responsabilidades
1. **Gerenciamento de Componentes**
   - Adicionar/remover componentes
   - Ordenação por z-index
   - Grupos de componentes

2. **Event Handling**
   - Distribuir eventos
   - Prioridade por z-order
   - Event bubbling

3. **Renderização**
   - Draw order
   - Clipping regions
   - Batch rendering

### Exemplo de Uso
```python
# Criar manager
ui_manager = UIManager()

# Adicionar componentes
ui_manager.add(button, z_order=1)
ui_manager.add(slider, z_order=2)

# Game loop
ui_manager.handle_event(event)
ui_manager.update(dt)
ui_manager.draw(screen)
```

## 📱 Componentes Especializados

### 1. **Menu Principal**

#### Estrutura
```
AdvancedMainMenu
├── Logo animado
├── Botões principais
│   ├── JOGAR
│   ├── ESTATÍSTICAS
│   ├── DIFICULDADE
│   ├── CARREGAR
│   └── SAIR
├── Indicadores
│   ├── Volume
│   ├── Dificuldade
│   └── Versão
└── Partículas decorativas
```

### 2. **HUD In-Game**

#### Elementos
- **Health Bar**: Gradiente vermelho/verde
- **Energy Bar**: Gradiente azul
- **Weapon Display**: Ícone + nome
- **Key Counter**: Visual de chaves
- **Score/XP**: Números animados

### 3. **Settings UI**

#### Modern Settings UI
```
Painel Principal
├── Header (título + close)
├── Volume Section
│   ├── Equalizer bars
│   ├── Volume slider
│   └── Mute button
├── Graphics Section
│   ├── Resolution
│   ├── Quality
│   └── FPS limit
└── Apply/Cancel buttons
```

## 🎨 Sistema de Fontes

### FontManager
```python
FONTS = {
    'title': {'size': 48, 'bold': True},
    'subtitle': {'size': 32},
    'text': {'size': 20},
    'small': {'size': 16}
}
```

### Enhanced Font System
- **Efeitos**: Sombra, glow, outline, gradiente
- **Animações**: Fade, pulse, wave, rotate
- **Word wrap**: Quebra automática
- **Alinhamento**: Left, center, right, justify

## 📊 Telas Especiais

### 1. **Stats Screen**
- Grid de estatísticas
- Gráficos de progresso
- Animações de entrada
- Navegação por categorias

### 2. **Achievements Screen**
- Grid scrollável
- Ícones animados
- Progress bars
- Filtros e ordenação

### 3. **Save/Load Screen**
- Slots visuais
- Preview de saves
- Confirmação modal
- Animações de transição

## 🎮 Sistema de Tutorial

### TutorialSystem
```python
TUTORIAL_STEPS = [
    "Movimento básico",
    "Sistema de combate",
    "Uso de magia",
    "Coleta de itens",
    # ... 10 passos total
]
```

### Características
- Overlay semi-transparente
- Destaque de elementos
- Animações guiadas
- Skip disponível

## 🔧 Otimizações de Performance

### 1. **Batch Rendering**
- Agrupa draws similares
- Reduz state changes
- Surface caching

### 2. **Dirty Rectangles**
- Atualiza apenas áreas modificadas
- Track de regiões sujas
- Redraw inteligente

### 3. **Event Optimization**
- Event pooling
- Priority queues
- Early termination

## 🎯 Padrões de Uso

### Criação de Tela Completa
```python
class MyScreen:
    def __init__(self):
        self.ui_manager = UIManager()
        self._create_ui()
    
    def _create_ui(self):
        # Header
        self.title = AnimatedText("Minha Tela", ...)
        
        # Content
        self.panel = ModernPanel(...)
        
        # Actions
        self.confirm_btn = ModernButton(...)
        
        # Add to manager
        self.ui_manager.add_all([
            self.title,
            self.panel,
            self.confirm_btn
        ])
```

## 🌈 Customização Visual

### Temas Alternativos
```python
# Dark theme
DARK_THEME = {
    'background': (10, 10, 10),
    'surface': (20, 20, 20),
    'primary': (100, 200, 255)
}

# Light theme
LIGHT_THEME = {
    'background': (240, 240, 240),
    'surface': (255, 255, 255),
    'primary': (0, 100, 200)
}
```

### Efeitos Visuais
1. **Gradientes**: Linear, radial, conical
2. **Sombras**: Drop shadow, inner shadow
3. **Blur**: Gaussian blur (limitado)
4. **Glow**: Outer glow, inner glow
5. **Particles**: Sistema integrado

## 🔮 Roadmap de Melhorias

### Planejado
1. **Drag & Drop**: Sistema completo
2. **Tooltips**: Hover information
3. **Context Menus**: Right-click menus
4. **Notifications**: Toast messages
5. **Transitions**: Scene transitions

### Considerado
1. Layout managers (grid, flex)
2. Data binding
3. Responsive design
4. Accessibility features
5. Theme editor

## 💡 Boas Práticas

### Do's
- Use UIManager para todos os componentes
- Mantenha hierarquia clara
- Reutilize componentes base
- Siga o tema visual

### Don'ts
- Não renderize UI fora do manager
- Não hardcode cores/estilos
- Não ignore estados (disabled, hover)
- Não crie loops de animação infinitos

---

[← Voltar: Sistema Gráfico](./graficos.md) | [Índice](../README.md) | [Próximo: Controles →](../gameplay/controles.md)