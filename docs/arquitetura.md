# 🏗️ Arquitetura do Sistema

## 📋 Visão Geral

O projeto "Corrida pela Relíquia" utiliza uma arquitetura modular baseada em componentes, com clara separação de responsabilidades entre os diferentes sistemas do jogo.

## 🎯 Princípios Arquiteturais

### 1. **Modularidade**
- Cada sistema é independente e possui interface bem definida
- Facilita manutenção e expansão de funcionalidades
- Reduz acoplamento entre componentes

### 2. **Padrão Singleton**
- Usado para sistemas globais (Audio, Graphics)
- Garante única instância e estado consistente
- Facilita acesso global aos recursos

### 3. **Herança e Polimorfismo**
- Classe base `Entity` para Player e Enemy
- Reutilização de código comum
- Especialização através de sobrescrita de métodos

### 4. **Separação de Responsabilidades**
- Cada classe/módulo tem propósito único e claro
- Facilita testes e depuração
- Melhora legibilidade do código

## 🏛️ Estrutura de Alto Nível

```
┌─────────────────┐
│   main.py       │  ← Ponto de entrada e game loop
└────────┬────────┘
         │
    ┌────┴────────────────────────────────┐
    │         Game State Manager          │
    └────┬────────────────────────────────┘
         │
    ┌────┴────┬──────────┬──────────┬─────────┐
    │ Screens │  Levels  │ Managers │ Systems │
    └─────────┴──────────┴──────────┴─────────┘
```

## 📦 Componentes Principais

### 1. **Core (Núcleo)**

#### `main.py`
- **Responsabilidade**: Gerenciar o game loop principal e estados
- **Componentes**:
  - Classe `Game`: Controla fluxo do jogo
  - Sistema de estados (menu, levels, game over)
  - Integração com todos os managers

#### `settings.py`
- **Responsabilidade**: Constantes globais do jogo
- **Dados**: Dimensões da tela, paths, configurações base

### 2. **Entidades**

#### `entity.py`
- **Classe Base**: Fornece funcionalidades comuns
- **Recursos**:
  - Sistema de movimento com normalização
  - Detecção de colisão
  - Animação básica

#### `player.py`
- **Herda de**: Entity
- **Recursos Únicos**:
  - Input handling (teclado)
  - Sistema de armas (5 tipos)
  - Sistema de magia (2 tipos)
  - Energia para corrida
  - Inventário de itens

#### `enemy.py`
- **Herda de**: Entity
- **Recursos Únicos**:
  - IA de perseguição
  - Sistema de detecção (notice_radius)
  - Health bar flutuante
  - Efeitos mágicos (fogo/gelo)

### 3. **Níveis (Levels)**

#### Estrutura Base
```python
class Level:
    def __init__(self):
        self.visible_sprites    # Y-sort camera
        self.obstacle_sprites   # Colisões
        self.attack_sprites     # Ataques
        self.attackable_sprites # Podem ser atacados
```

#### Níveis Implementados
- **Level 1**: Floresta - Tutorial básico
- **Level 2**: Labirinto - Exploração
- **Level 3**: Fortaleza - Combate + Minimapa
- **Level 4**: Boss Final - Desafio culminante

### 4. **Sistemas Globais (Managers)**

#### `audio_manager.py`
- **Padrão**: Singleton Thread-Safe
- **Recursos**:
  - Música de fundo
  - Efeitos sonoros categorizados
  - Cache de sons
  - Controle de volume separado

#### `graphics_manager.py`
- **Padrão**: Singleton
- **Recursos**:
  - Múltiplas resoluções
  - Fullscreen toggle
  - V-Sync e FPS limit
  - Qualidade gráfica

#### `save_manager.py`
- **Padrão**: Utility Class
- **Recursos**:
  - 5 slots + auto-save
  - Quick save/load
  - Serialização JSON
  - Validação de dados

#### `difficulty_manager.py`
- **Padrão**: Utility Class com Estado
- **Níveis**: Fácil, Normal, Difícil
- **Afeta**: Vida, dano, spawn de itens

### 5. **Interface (UI)**

#### `ui_system.py`
- **Padrão**: Component-Based Architecture
- **Componentes**:
  - UIComponent (base)
  - ModernButton
  - ModernSlider
  - ModernPanel
  - UIManager

#### Características
- Sistema de temas (UITheme)
- Animações com easing
- Gradientes e efeitos visuais
- Event handling centralizado

### 6. **Telas (Screens)**

#### Tipos de Telas
- **Menu Principal**: `main_menu.py`
- **Entrada de Nome**: `name_input_screen.py`
- **História**: `story_screen.py`
- **Estatísticas**: `stats_screen.py`
- **Conquistas**: `achievements_screen.py`
- **Dificuldade**: `difficulty_screen.py`
- **Save/Load**: `save_screen.py`

## 🔄 Fluxo de Dados

### 1. **Input → Processing → Output**
```
Teclado/Mouse → pygame.event → Game/Level → Update → Render
```

### 2. **Game States**
```
-1: Name Input
 0: Main Menu
 3: Level 1
 4: Level 2
 5: Level 3
 6: Level 4
20: Game Over
30: Stats Screen
31: Achievements
40: Difficulty
50: Load Game
51: Save Game
```

### 3. **Comunicação entre Sistemas**
- **Direta**: Import de instâncias singleton
- **Callbacks**: Funções passadas como parâmetros
- **Events**: Sistema de eventos do pygame
- **Estado Global**: Através dos managers

## 🎮 Ciclo de Jogo (Game Loop)

```python
while True:
    # 1. Handle Events
    process_input()
    
    # 2. Update Game State
    update_entities()
    check_collisions()
    update_ui()
    
    # 3. Render
    draw_sprites()
    draw_ui()
    
    # 4. Control Frame Rate
    clock.tick(fps)
```

## 🔧 Decisões Técnicas

### 1. **Por que Singleton?**
- Evita múltiplas instâncias de sistemas críticos
- Facilita acesso global
- Mantém estado consistente

### 2. **Por que Component-Based UI?**
- Reutilização de componentes
- Facilita criação de novas interfaces
- Separação visual/lógica

### 3. **Por que Y-Sort Camera?**
- Ordenação automática por profundidade
- Efeito visual 2.5D
- Performance otimizada

### 4. **Por que JSON para Saves?**
- Formato legível por humanos
- Fácil serialização/deserialização
- Compatível entre versões

## 📊 Diagrama de Classes Principais

```
Entity
├── Player
│   ├── input()
│   ├── animate()
│   └── create_attack()
│
└── Enemy
    ├── get_status()
    ├── actions()
    └── get_damage()

Level (Base)
├── Level1
├── Level2
├── Level3 (+ Minimap)
└── Level4

Manager (Pattern)
├── AudioManager (Singleton)
├── GraphicsManager (Singleton)
├── SaveManager (Utility)
└── DifficultyManager (Utility)
```

## 🚀 Escalabilidade

### Pontos de Extensão
1. **Novos Níveis**: Herdar de Level base
2. **Novos Inimigos**: Adicionar em enemy types
3. **Novas Armas**: Expandir weapon_data
4. **Novos Sistemas**: Criar novo manager
5. **Novas UIs**: Usar UISystem components

### Limitações Conhecidas
1. **Performance**: Muitas partículas podem afetar FPS
2. **Memória**: Todos os assets carregados na inicialização
3. **Save System**: Tamanho fixo de slots
4. **Resolução**: Limitada às predefinidas

---

[← Voltar ao Índice](./README.md) | [Próximo: Padrões de Design →](./padroes-design.md)