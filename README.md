# Corrida pela Relíquia: A Busca pela Pedra Mística do Zappaguri / Race for the Relic: The Quest for Zappaguri's Mystic Stone

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green?style=for-the-badge&logo=pygame&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completo-success?style=for-the-badge)
![Licença](https://img.shields.io/badge/Licença-MIT-orange?style=for-the-badge)

**Projeto Acadêmico - Tópicos Especiais I / Academic Project - Special Topics I**  
**IFSULDEMINAS Campus Muzambinho**  
**Aluno/Student: Anderson Henrique da Silva**  
**Orientador/Advisor: Prof. Ricardo Martins**

---

## 🌍 Language / Idioma

- [Português](#português)
- [English](#english)

---

# Português

## 🎮 Sobre o Jogo

Corrida pela Relíquia é um jogo de ação e aventura onde você embarca em uma jornada épica para recuperar a lendária Pedra Mística do Zappaguri. Com mecânicas de combate aprimoradas, sistema de progressão dinâmico e uma narrativa envolvente, o jogo oferece uma experiência completa de RPG de ação.

### 🌟 Novidades da Versão Atual

- **Sistema de História Épico**: Narrativas estilo Star Wars entre as fases
- **Ataque 360°**: Sistema de combate melhorado com dano em área
- **Textos Flutuantes Dinâmicos**: Feedback visual ao coletar itens
- **Minimapa Interativo**: Disponível na fase 3 (pressione TAB)
- **Barras de Vida dos Inimigos**: Visualize o HP dos adversários
- **Sistema de Partículas**: Efeitos visuais para coleta e morte
- **Áudio Centralizado**: Controle total do som com menu de configurações

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Pygame 2.6+**: Engine do jogo
- **PIL/Pillow**: Processamento de imagens
- **Threading**: Gerenciamento de áudio
- **CSV**: Sistema de mapas (Tiled)
- **OpenGameArt**: Assets visuais e sonoros

## 📋 Requisitos do Sistema

- Python 3.8 ou superior
- Pygame 2.6 ou superior
- 2GB de RAM mínimo
- 500MB de espaço em disco
- Placa de som compatível

## 🚀 Como Jogar

### Instalação Rápida
```bash
# Clone o repositório
git clone https://github.com/anderson-ufrj/project-game-py.git
cd project-game-py

# Execute o script automatizado
./rungame.sh
```

### Instalação Manual
```bash
# 1. Crie o ambiente virtual
python3 -m venv venv

# 2. Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install pygame pillow

# 4. Execute o jogo
cd code
python main.py
```

## 🎮 Controles

| Tecla | Ação |
|-------|------|
| ↑↓←→ | Movimentação |
| Shift | Correr |
| Espaço | Ataque (360°) |
| Enter | Iniciar/Confirmar |
| TAB | Minimapa (Fase 3) |
| M | Mutar/Desmutar som |
| ↑↓ | Ajustar volume |
| ESC | Menu de pausa |

## 📖 História

Há muito tempo, o reino de Zappaguri prosperava sob a proteção da lendária Pedra Mística. Mas forças sombrias fragmentaram este artefato sagrado, espalhando seus pedaços pelos quatro cantos do reino. Como o guerreiro escolhido, você deve:

1. **Planícies Verdejantes**: Enfrente criaturas corrompidas
2. **Labirinto das Sombras**: Navegue pelo labirinto mortal
3. **Fortaleza Sombria**: Colete as três chaves místicas
4. **Santuário Corrompido**: Derrote o Guardião das Sombras

## 🏆 Características do Jogo

### Sistema de Combate
- Ataque com dano em área 360°
- Diferentes tipos de inimigos com padrões únicos
- Sistema de esquiva com invulnerabilidade temporária

### Progressão
- Colete orbes para melhorar:
  - ❤️ **Vida**: Aumenta HP máximo
  - ⚡ **Velocidade**: Movimento mais rápido
  - ⚔️ **Ataque**: Maior dano

### Recursos Visuais
- Animações de partículas para coletas
- Efeitos de morte elaborados
- Sistema de câmera Y-sort
- Vinheta dinâmica nas fases escuras

### Áudio
- Trilhas sonoras atmosféricas por fase
- Efeitos sonoros imersivos
- Sistema de volume ajustável
- Música dinâmica baseada no contexto

## 🐛 Problemas Conhecidos

- Performance pode cair com muitos inimigos na tela
- Alguns sprites podem sobrepor incorretamente
- O jogo requer reinicialização após game over

## 👥 Créditos

- **Desenvolvimento**: Anderson Henrique da Silva
- **Orientação**: Prof. Ricardo Martins
- **Assets**: OpenGameArt Community
- **Engine**: Pygame Development Team
- **Fonte**: Press Start 2P

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

# English

## 🎮 About the Game

Race for the Relic is an action-adventure game where you embark on an epic journey to recover the legendary Mystic Stone of Zappaguri. With enhanced combat mechanics, dynamic progression system, and an engaging narrative, the game offers a complete action-RPG experience.

### 🌟 Current Version Features

- **Epic Story System**: Star Wars-style narratives between levels
- **360° Attack**: Enhanced combat system with area damage
- **Dynamic Floating Text**: Visual feedback when collecting items
- **Interactive Minimap**: Available in level 3 (press TAB)
- **Enemy Health Bars**: Visualize opponent HP
- **Particle System**: Visual effects for collection and death
- **Centralized Audio**: Full sound control with settings menu

## 🛠️ Technologies Used

- **Python 3.8+**: Main language
- **Pygame 2.6+**: Game engine
- **PIL/Pillow**: Image processing
- **Threading**: Audio management
- **CSV**: Map system (Tiled)
- **OpenGameArt**: Visual and audio assets

## 📋 System Requirements

- Python 3.8 or higher
- Pygame 2.6 or higher
- 2GB RAM minimum
- 500MB disk space
- Compatible sound card

## 🚀 How to Play

### Quick Installation
```bash
# Clone the repository
git clone https://github.com/anderson-ufrj/project-game-py.git
cd project-game-py

# Run the automated script
./rungame.sh
```

### Manual Installation
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install pygame pillow

# 4. Run the game
cd code
python main.py
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| ↑↓←→ | Movement |
| Shift | Run |
| Space | Attack (360°) |
| Enter | Start/Confirm |
| TAB | Minimap (Level 3) |
| M | Mute/Unmute sound |
| ↑↓ | Adjust volume |
| ESC | Pause menu |

## 📖 Story

Long ago, the kingdom of Zappaguri prospered under the protection of the legendary Mystic Stone. But dark forces fragmented this sacred artifact, scattering its pieces across the four corners of the realm. As the chosen warrior, you must:

1. **Green Plains**: Face corrupted creatures
2. **Shadow Maze**: Navigate the deadly labyrinth
3. **Dark Fortress**: Collect the three mystic keys
4. **Corrupted Sanctuary**: Defeat the Shadow Guardian

## 🏆 Game Features

### Combat System
- 360° area damage attack
- Different enemy types with unique patterns
- Dodge system with temporary invulnerability

### Progression
- Collect orbs to improve:
  - ❤️ **Health**: Increases max HP
  - ⚡ **Speed**: Faster movement
  - ⚔️ **Attack**: Higher damage

### Visual Features
- Particle animations for collections
- Elaborate death effects
- Y-sort camera system
- Dynamic vignette in dark levels

### Audio
- Atmospheric soundtracks per level
- Immersive sound effects
- Adjustable volume system
- Context-based dynamic music

## 🐛 Known Issues

- Performance may drop with many enemies on screen
- Some sprites may overlap incorrectly
- Game requires restart after game over

## 👥 Credits

- **Development**: Anderson Henrique da Silva
- **Advisor**: Prof. Ricardo Martins
- **Assets**: OpenGameArt Community
- **Engine**: Pygame Development Team
- **Font**: Press Start 2P

## 📄 License

This project is under the MIT license. See the [LICENSE](LICENSE) file for more details.

---

**📧 Contact / Contato**: andersonhs27@gmail.com
**🎮 Enjoy the game! / Divirta-se jogando!**
