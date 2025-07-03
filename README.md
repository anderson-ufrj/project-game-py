# Corrida pela Relíquia: A Busca pela Pedra Mística do Zappaguri

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green?style=for-the-badge&logo=pygame&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completo-success?style=for-the-badge)
![Licença](https://img.shields.io/badge/Licença-MIT-orange?style=for-the-badge)

**Projeto Acadêmico - Tópicos Especiais I**  
**IFSULDEMINAS Campus Muzambinho**  
**Aluno: Anderson Henrique da Silva**  
**Orientador: Prof. Ricardo Martins**

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** - Linguagem de programação principal
- **Pygame 2.6+** - Engine para desenvolvimento do jogo
- **PIL/Pillow** - Manipulação de imagens
- **Threading** - Gerenciamento de áudio centralizado
- **CSV** - Importação de mapas do Tiled
- **OpenGameArt** - Assets visuais e sonoros

## 🎮 Características Técnicas

- ⚙️ **Sistema de áudio centralizado** com controles visuais
- 🎯 **Ataque 360°** - Dano em área mantendo animação original  
- 🗺️ **Minimapa interativo** na Fase 3 (tecla TAB)
- 🎨 **Animações de partículas** para coleta de gemas e morte de inimigos
- ❤️ **Barras de vida** flutuantes para inimigos
- 📱 **Interface responsiva** com menu de configurações
- 🌍 **Tradução completa** para português brasileiro

## Visão Geral do Jogo

Bem-vindo ao Corrida pela Relíquia, um jogo de aventura encantador que convida você a embarcar em uma missão para descobrir a mítica Pedra Mística do Zappaguri. Mergulhe em um mundo cativante cheio de níveis desafiadores, gemas místicas e uma rica experiência auditiva. Este jogo apresenta ambientes visualmente deslumbrantes e diversos com assets obtidos do [OpenGameArt](https://opengameart.org/).

## Instalação

Antes de executar o jogo, certifique-se de que o módulo `pygame` esteja instalado. Você pode instalá-lo usando o seguinte comando:

```bash
pip install pygame
```

## Jogabilidade

### Objetivo

Embarque em uma jornada para guiar o jogador através de níveis intrincados, coletando várias gemas e descobrindo os segredos da Pedra Mística do Zappaguri. Desfrute de uma experiência visualmente atraente com assets do OpenGameArt, acompanhada por música de fundo dinâmica e efeitos sonoros imersivos.

### Movimento

Use as setas do teclado para navegar o jogador pelo mundo do jogo, shift para correr.

### Design dos Níveis

- Música de fundo dinâmica, alimentada pelo módulo `pygame.mixer`, aprimora diferentes estados do jogo, proporcionando uma experiência perfeita e atmosférica.
- Efeitos sonoros, incluindo a coleta de gemas, são implementados usando o módulo `pygame.sound`, criando um ambiente de jogo satisfatório e imersivo.
- Utilizando assets do OpenGameArt, o jogo possui uma estética visualmente deslumbrante que complementa o tema místico.
- Câmera personalizada do jogador que move o mapa em vez do jogador (função YSortCameraGroup()).
- Processo completamente original de colisão e mapeamento de tiles! Nenhum uso do pytmx.
- Recurso opcional para resetar o jogo, limpar todos os sprites, etc. para melhorar a performance (ainda não totalmente implementado para todas as fases)
- Interface personalizada usando apenas pygame.

### Design Visual e Auditivo

- Duas camadas de imagens, fundo e primeiro plano, combinadas com assets do OpenGameArt, criam uma experiência de jogo visualmente atraente e imersiva.
- Desfrute de uma paisagem auditiva rica com música de fundo cuidadosamente escolhida e efeitos sonoros satisfatórios, melhorando a atmosfera geral do jogo.
- Cutscenes feitas quadro a quadro no PowerPoint/imagens GIF exibidas sucessivamente na tela.
- Transições feitas usando lógica similar de tempo e exibição.
- Mapa projetado no Tiled. O mapa em si não contém sprites, é uma imagem. Apenas as colisões foram importadas como `.csv` e exibidas invisivelmente sobre a imagem do mapa, otimizando a performance considerando o baixo desempenho do pygame quando há muitos sprites.

### Sistema de Inventário

- Colete várias gemas para afetar o inventário e estatísticas do jogador, adicionando uma camada extra de estratégia ao seu jogo.
- Lógica de coletáveis implementada, que afeta as estatísticas do jogador. Funciona através da criação de um grupo de classe Collectable e configurando seus sprites para serem eliminados e as estatísticas do jogador mudarem na colisão usando os métodos de colisão pygame.sprite.Sprite integrados.

### Inimigos

- Supere desafios impostos por inimigos, navegando estrategicamente através de cada nível para progredir em sua missão.
- Atualmente existem 3 tipos de inimigos no jogo, cada um com seu próprio conjunto de propriedades e habilidades.

## Como Executar o Jogo

### 🚀 Método Fácil (Recomendado):
```bash
# Execute o script automatizado
./rungame.sh
```

O script `rungame.sh` automaticamente:
- ✅ Cria o ambiente virtual (se necessário)
- ✅ Instala o pygame (se necessário) 
- ✅ Executa o jogo
- ✅ Mostra instruções e controles

### 📋 Método Manual:
```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Instalar pygame
pip install pygame

# 4. Executar o jogo
cd code
python main.py
```

Embarque nesta jornada mágica, onde a combinação de assets do OpenGameArt e design de áudio dinâmico aguarda para transportá-lo para o mundo da Corrida pela Relíquia!

---

*Projeto desenvolvido com assistência de IA para otimização de código e implementação de recursos avançados.*
