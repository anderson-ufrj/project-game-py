# 🎨 Padrões de Design

## 📋 Visão Geral

Este documento descreve os principais padrões de design utilizados no projeto "Corrida pela Relíquia", explicando suas implementações e benefícios.

## 🔧 Padrões Implementados

### 1. **Singleton Pattern**

#### Definição
Garante que uma classe tenha apenas uma instância e fornece um ponto global de acesso a ela.

#### Implementações no Projeto

##### AudioManager (Thread-Safe)
```python
class AudioManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
```

**Benefícios**:
- Evita múltiplas instâncias conflitantes de áudio
- Thread-safe para operações concorrentes
- Estado global consistente de volume/mute

##### GraphicsManager
```python
class GraphicsManager:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Benefícios**:
- Configurações gráficas centralizadas
- Evita conflitos de resolução/modo de tela
- Facilita aplicação global de mudanças

### 2. **Component-Based Architecture**

#### Definição
Constrói sistemas complexos a partir de componentes menores e reutilizáveis.

#### Implementação: UI System

```python
# Hierarquia de Componentes
UIComponent (base)
├── ModernButton
├── ModernSlider  
├── ModernPanel
└── AnimatedText

# Manager Central
UIManager
├── components[]
├── handle_event()
├── update()
└── draw()
```

**Benefícios**:
- Alta reutilização de código
- Fácil criação de novas interfaces
- Manutenção simplificada
- Comportamentos consistentes

### 3. **Entity-Component Pattern**

#### Definição
Separa dados (componentes) de comportamento (sistemas).

#### Implementação: Entity System

```python
class Entity(pygame.sprite.Sprite):
    # Componentes base
    - position (rect)
    - direction (vector)
    - speed
    - animation_speed
    
    # Sistemas
    - move()
    - collision()
    - animate()
```

**Benefícios**:
- Herança limpa para Player/Enemy
- Comportamentos compartilhados
- Fácil adição de novos tipos de entidades

### 4. **State Pattern**

#### Definição
Permite que um objeto altere seu comportamento quando seu estado interno muda.

#### Implementação: Game States

```python
# Estados do Jogo
STATES = {
    -1: "name_input",
     0: "main_menu",
     3: "level_1",
     4: "level_2",
     5: "level_3",
     6: "level_4",
    20: "game_over",
    30: "stats_screen",
    # ...
}

# Máquina de Estados
if self.game_state == 0:
    self.homescreen()
elif self.game_state == 3:
    self.level1.run()
# ...
```

**Benefícios**:
- Fluxo de jogo claro e organizado
- Fácil adição de novos estados
- Transições bem definidas

### 5. **Observer Pattern (Implícito)**

#### Definição
Define uma dependência um-para-muitos entre objetos.

#### Implementação: Event System

```python
# Pygame Events como Observer
for event in pygame.event.get():
    # Múltiplos "observers" respondem
    audio_manager.handle_event(event)
    ui_manager.handle_event(event)
    level.handle_event(event)
```

**Benefícios**:
- Desacoplamento entre sistemas
- Múltiplos handlers por evento
- Extensibilidade

### 6. **Factory Pattern**

#### Definição
Define uma interface para criar objetos, mas deixa as subclasses decidirem qual classe instanciar.

#### Implementação: Weapon Creation

```python
def create_weapon(self):
    weapon_type = list(weapon_data.keys())[self.weapon_index]
    # Factory decide qual arma criar
    Weapon(
        self.player,
        [self.visible_sprites, self.attack_sprites],
        weapon_type
    )
```

**Benefícios**:
- Criação flexível de armas
- Fácil adição de novos tipos
- Encapsulamento da lógica de criação

### 7. **Strategy Pattern**

#### Definição
Define uma família de algoritmos, encapsula cada um e os torna intercambiáveis.

#### Implementação: Difficulty System

```python
# Estratégias de Dificuldade
DIFFICULTY_SETTINGS = {
    "easy": {
        "player_health": 1.5,
        "enemy_health": 0.7,
        # ...
    },
    "normal": {
        "player_health": 1.0,
        "enemy_health": 1.0,
        # ...
    }
}

# Aplicação da Estratégia
def apply_difficulty_to_player(self, base_stats):
    modifiers = self.get_current_modifiers()
    # Aplica estratégia escolhida
```

**Benefícios**:
- Troca fácil de dificuldade
- Comportamentos encapsulados
- Extensível para novos modos

### 8. **Command Pattern (Parcial)**

#### Definição
Encapsula uma solicitação como um objeto.

#### Implementação: Cheat System

```python
CHEAT_CODES = {
    "level1": [K_F1],
    "level2": [K_F2],
    # ...
}

def handle_cheat_input(self, event):
    # Cada cheat é um "comando"
    if sequence_matches:
        return cheat_name  # Comando a executar
```

**Benefícios**:
- Comandos desacoplados da execução
- Fácil adição de novos cheats
- Possibilidade de undo (não implementado)

### 9. **Facade Pattern**

#### Definição
Fornece uma interface simplificada para um subsistema complexo.

#### Implementação: Save System

```python
class SaveManager:
    def quick_save(self, game):
        # Facade esconde complexidade
        save_data = self._extract_game_data(game)
        return self.save_game_data(save_data, 0)
    
    def _extract_game_data(self, game):
        # Complexidade interna
        # ... coleta dados de múltiplos sistemas
```

**Benefícios**:
- Interface simples para operações complexas
- Esconde detalhes de implementação
- Facilita uso do sistema

### 10. **Template Method Pattern**

#### Definição
Define o esqueleto de um algoritmo, deixando alguns passos para subclasses.

#### Implementação: Level Base Class

```python
class Level:
    def run(self):
        # Template method
        self.handle_input()
        self.update()
        self.draw()
    
    # Métodos para override
    def handle_input(self): pass
    def update(self): pass
    def draw(self): pass
```

**Benefícios**:
- Estrutura consistente entre níveis
- Reutilização de código comum
- Flexibilidade para customização

## 🎯 Boas Práticas Aplicadas

### 1. **SOLID Principles**

#### Single Responsibility
- Cada classe tem uma única responsabilidade
- Ex: AudioManager só gerencia áudio

#### Open/Closed
- Classes abertas para extensão, fechadas para modificação
- Ex: Novos componentes UI sem alterar UIManager

#### Dependency Inversion
- Dependência de abstrações, não implementações
- Ex: Levels dependem de Entity, não Player/Enemy

### 2. **DRY (Don't Repeat Yourself)**
- Código comum em classes base (Entity)
- Funções utilitárias em support.py
- Componentes UI reutilizáveis

### 3. **KISS (Keep It Simple, Stupid)**
- Soluções simples para problemas complexos
- Ex: Estado do jogo como simples inteiro

### 4. **YAGNI (You Aren't Gonna Need It)**
- Implementar apenas o necessário
- Evitar over-engineering

## 📊 Análise de Impacto

### Benefícios dos Padrões

1. **Manutenibilidade**: Código organizado e previsível
2. **Extensibilidade**: Fácil adicionar features
3. **Testabilidade**: Componentes isolados
4. **Reutilização**: Menos duplicação
5. **Performance**: Singletons evitam instâncias desnecessárias

### Trade-offs

1. **Complexidade Inicial**: Mais código para setup
2. **Curva de Aprendizado**: Requer conhecimento dos padrões
3. **Over-engineering**: Risco de usar padrões desnecessários

## 🔄 Evolução dos Padrões

### Fase Inicial
- Código procedural simples
- Classes básicas sem padrões

### Refatoração 1
- Introdução de Singleton para Audio
- Separação Player/Enemy de Entity

### Refatoração 2
- Component-Based UI System
- State Pattern para game flow

### Estado Atual
- Múltiplos padrões integrados
- Arquitetura madura e extensível

---

[← Voltar: Arquitetura](./arquitetura.md) | [Índice](./README.md) | [Próximo: Fluxo do Jogo →](./fluxo-jogo.md)