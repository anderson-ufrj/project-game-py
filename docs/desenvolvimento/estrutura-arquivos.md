# 📁 Estrutura de Arquivos

## 📋 Visão Geral

Este documento detalha a organização completa dos arquivos e diretórios do projeto "Corrida pela Relíquia".

## 🏗️ Estrutura Principal

```
project-game-py/
├── 📁 audio/                    # Sons e músicas
├── 📁 code/                     # Código fonte principal
├── 📁 docs/                     # Documentação do projeto
├── 📁 font/                     # Arquivos de fontes
├── 📁 graphics/                 # Recursos visuais
├── 📁 map new/                  # Mapas e layouts
├── 📁 saves/                    # Arquivos de save
├── 📄 .gitignore               # Configuração Git
├── 📄 CLAUDE.md                # Histórico de desenvolvimento
├── 📄 README.md                # Documentação principal
├── 📄 requirements.txt         # Dependências Python
└── 📄 rungame.sh              # Script de execução
```

## 📂 Detalhamento por Diretório

### 📁 `/audio`
Contém todos os arquivos de áudio do jogo.

```
audio/
├── 🎵 home.mp3                 # Música do menu principal
├── 🎵 Ambient 2.mp3            # Música dos níveis 1-2
├── 🎵 darkambience(from fable).mp3  # Música do nível 3
├── 🔊 coin_collect.wav         # Som de coleta de moeda
├── 🔊 enemy_death.wav          # Som de morte de inimigo
├── 🔊 sword_swing.ogg          # Som de ataque
└── ... (outros efeitos sonoros)
```

### 📁 `/code`
Código fonte principal do jogo.

#### 🎮 Arquivos Principais
```
code/
├── 🐍 main.py                  # Ponto de entrada principal
├── 🐍 settings.py              # Configurações globais
├── 🐍 support.py               # Funções auxiliares
└── 🐍 debug.py                 # Ferramentas de debug
```

#### 🎭 Entidades
```
code/
├── 🐍 entity.py                # Classe base para entidades
├── 🐍 player.py                # Lógica do jogador
├── 🐍 enemy.py                 # Sistema de inimigos
├── 🐍 weapon.py                # Sistema de armas
└── 🐍 magic.py                 # Sistema de magia
```

#### 🏞️ Níveis
```
code/
├── 🐍 level.py                 # Level 1 - Floresta
├── 🐍 level2.py                # Level 2 - Labirinto
├── 🐍 level3.py                # Level 3 - Fortaleza
└── 🐍 level4.py                # Level 4 - Boss Final
```

#### 🎨 Interface e Menus
```
code/
├── 🐍 ui.py                    # HUD do jogo
├── 🐍 ui_system.py             # Sistema UI moderno
├── 🐍 main_menu.py             # Menu principal
├── 🐍 story_screen.py          # Telas de história
├── 🐍 stats_screen.py          # Tela de estatísticas
├── 🐍 achievements_screen.py   # Tela de conquistas
├── 🐍 save_screen.py           # Interface de save/load
└── 🐍 name_input_screen.py     # Entrada de nome
```

#### ⚙️ Sistemas (Managers)
```
code/
├── 🐍 audio_manager.py         # Gerenciador de áudio
├── 🐍 graphics_manager.py      # Gerenciador gráfico
├── 🐍 save_manager.py          # Sistema de save/load
├── 🐍 difficulty_manager.py    # Sistema de dificuldade
├── 🐍 font_manager.py          # Gerenciador de fontes
└── 🐍 player_stats.py          # Estatísticas do jogador
```

#### 🗑️ Arquivos Descontinuados
```
code/trash/
├── 🐍 modern_settings_ui.py    # UI antiga removida
├── 🐍 settings_manager.py      # Manager legado
└── ... (outros arquivos obsoletos)
```

### 📁 `/graphics`
Todos os recursos visuais organizados por categoria.

```
graphics/
├── 📁 font/                    # Arquivos de fonte
│   └── joystix.ttf            # Fonte pixelada principal
│
├── 📁 monsters/                # Sprites de inimigos
│   ├── 📁 bamboo/             # Inimigo Bamboo
│   ├── 📁 spirit/             # Inimigo Spirit
│   ├── 📁 raccoon/            # Inimigo Raccoon
│   └── 📁 squid/              # Inimigo Squid
│
├── 📁 particles/               # Efeitos de partículas
│   ├── 📁 flame/              # Partículas de fogo
│   ├── 📁 heal/               # Partículas de cura
│   └── 📁 sparkle/            # Partículas de brilho
│
├── 📁 player/                  # Sprites do jogador
│   ├── 📁 down/               # Animação para baixo
│   ├── 📁 up/                 # Animação para cima
│   ├── 📁 left/               # Animação esquerda
│   └── 📁 right/              # Animação direita
│
├── 📁 test/                    # Sprites de teste
│   └── player.png             # Sprite teste do jogador
│
├── 📁 tilemap/                 # Tiles do mapa
│   ├── Floor.png              # Tiles de chão
│   ├── details.png            # Detalhes decorativos
│   └── ... (outros tilesets)
│
├── 📁 ui/                      # Interface do usuário
│   ├── button.png             # Sprite de botão
│   ├── health_bar.png         # Barra de vida
│   ├── home page.jpg          # Background do menu
│   └── gameover.jpg           # Tela de game over
│
└── 📁 weapons/                 # Sprites de armas
    ├── sword/                  # Espada
    ├── lance/                  # Lança
    ├── axe/                    # Machado
    ├── rapier/                 # Rapieira
    └── sai/                    # Sai
```

### 📁 `/map new`
Arquivos de mapa exportados do Tiled.

```
map new/
├── 📄 map_Floor.csv            # Camada de chão
├── 📄 map_Objects.csv          # Objetos do mapa
├── 📄 map_Entities.csv         # Posições de entidades
├── 🖼️ map.png                 # Preview do mapa
└── ... (outros arquivos de mapa)
```

### 📁 `/font`
Fontes customizadas do jogo.

```
font/
├── 📝 HennyPenny-Regular.ttf   # Fonte decorativa
├── 📝 KOMIKAX_.ttf             # Fonte estilo comic
├── 📝 OCRAEXT.ttf              # Fonte OCR
└── 📝 PressStart2P-Regular.ttf # Fonte retro principal
```

### 📁 `/saves`
Arquivos de salvamento do jogo.

```
saves/
├── 💾 save_slot_0.json         # Auto-save
├── 💾 save_slot_1.json         # Save manual 1
├── 💾 save_slot_2.json         # Save manual 2
├── 💾 save_slot_3.json         # Save manual 3
├── 💾 save_slot_4.json         # Save manual 4
└── 💾 save_slot_5.json         # Save manual 5
```

### 📁 `/docs`
Documentação completa do projeto.

```
docs/
├── 📄 README.md                # Índice da documentação
├── 📄 arquitetura.md           # Arquitetura do sistema
├── 📄 padroes-design.md        # Padrões de design
├── 📄 fluxo-jogo.md           # Fluxo e estados
├── 📁 sistemas/                # Documentação de sistemas
├── 📁 gameplay/                # Documentação de gameplay
└── 📁 desenvolvimento/         # Guias de desenvolvimento
```

## 📄 Arquivos de Configuração

### `.gitignore`
```
__pycache__/
*.pyc
*.pyo
.DS_Store
saves/
*.log
```

### `requirements.txt`
```
pygame>=2.6.0
pillow>=9.0.0
```

### `rungame.sh`
```bash
#!/bin/bash
# Script para executar o jogo
cd code
python main.py
```

## 🗂️ Convenções de Nomenclatura

### Arquivos Python
- **snake_case** para nomes de arquivo
- **Prefixo descritivo** (ex: `audio_manager.py`)
- **Sufixo _screen** para telas (ex: `stats_screen.py`)
- **Sufixo _manager** para sistemas (ex: `save_manager.py`)

### Assets Gráficos
- **Lowercase** com underscores
- **Diretórios por categoria**
- **Sprites animados em subpastas**
- **Formato**: PNG para sprites, JPG para backgrounds

### Arquivos de Áudio
- **Lowercase** com underscores
- **Extensão apropriada** (.mp3 para música, .wav/.ogg para SFX)
- **Nome descritivo** da ação/contexto

## 🔄 Arquivos Gerados

### Em Runtime
```
code/__pycache__/               # Cache Python
graphics_settings.json          # Configurações gráficas
difficulty_settings.json        # Configuração de dificuldade
player_stats.json              # Estatísticas do jogador
achievements.json              # Conquistas desbloqueadas
```

### Temporários
- Logs de debug (se ativado)
- Screenshots (se implementado)
- Crash reports (não implementado)

## 📊 Estatísticas do Projeto

### Contagem de Arquivos (Aproximada)
- **Python (.py)**: ~70 arquivos
- **Imagens (.png/.jpg)**: ~200 arquivos
- **Áudio (.mp3/.wav/.ogg)**: ~20 arquivos
- **Dados (.csv/.json)**: ~30 arquivos
- **Documentação (.md)**: ~20 arquivos

### Tamanho Total
- **Código**: ~5 MB
- **Gráficos**: ~50 MB
- **Áudio**: ~20 MB
- **Total**: ~75 MB

## 🚀 Setup Inicial

### Estrutura Mínima Necessária
```
project-game-py/
├── code/
│   └── *.py (todos os arquivos Python)
├── graphics/
│   └── (todas as subpastas)
├── audio/
│   └── (todos os arquivos de áudio)
└── font/
    └── PressStart2P-Regular.ttf (mínimo)
```

### Arquivos Auto-Criados
- `saves/` - Criado ao primeiro save
- `*.json` - Criados ao primeiro uso
- `__pycache__/` - Criado pelo Python

---

[← Voltar: Instalação](./instalacao.md) | [Índice](../README.md) | [Próximo: Contribuição →](./contribuicao.md)