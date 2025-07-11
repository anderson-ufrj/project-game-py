# 📚 Documentação - Corrida pela Relíquia

## 🎮 Sobre o Projeto

**Corrida pela Relíquia - A Busca pela Gema Eldritch** é um jogo 2D de aventura desenvolvido em Python usando a biblioteca Pygame. O projeto foi desenvolvido como trabalho acadêmico para a disciplina de Tópicos Especiais I do IFSULDEMINAS Campus Muzambinho.

### 📋 Informações Gerais

- **Aluno:** Anderson Henrique da Silva
- **Orientador:** Prof. Ricardo Martins  
- **Instituição:** IFSULDEMINAS Campus Muzambinho
- **Disciplina:** Tópicos Especiais I
- **Linguagem:** Python 3.8+
- **Framework:** Pygame 2.6+

## 📖 Índice da Documentação

### 🏗️ Arquitetura e Design
- [Arquitetura do Sistema](./arquitetura.md) - Visão geral da estrutura do projeto
- [Padrões de Design](./padroes-design.md) - Padrões utilizados no desenvolvimento
- [Fluxo do Jogo](./fluxo-jogo.md) - Estados e transições do jogo
- [🆕 Refatoração da Arquitetura](./refatoracao-arquitetura.md) - Nova estrutura modular

### 🎮 Sistemas do Jogo
- [Sistema de Combate](./sistemas/combate.md) - Mecânicas de ataque e dano
- [Sistema de Áudio](./sistemas/audio.md) - Gerenciamento de sons e música
- [Sistema Gráfico](./sistemas/graficos.md) - Configurações e renderização
- [Sistema de Save/Load](./sistemas/save-load.md) - Persistência de dados
- [Sistema de Dificuldade](./sistemas/dificuldade.md) - Níveis e modificadores
- [Sistema de UI](./sistemas/ui.md) - Interface moderna e componentes

### 🏃 Gameplay e Mecânicas
- [Controles](./gameplay/controles.md) - Comandos e teclas
- [Personagem](./gameplay/personagem.md) - Player e suas habilidades
- [Inimigos](./gameplay/inimigos.md) - Tipos e comportamentos
- [Itens e Coletáveis](./gameplay/itens.md) - Orbes, chaves e power-ups
- [Fases](./gameplay/fases.md) - Descrição dos 4 níveis

### 🛠️ Desenvolvimento
- [Instalação](./desenvolvimento/instalacao.md) - Como configurar o ambiente
- [Estrutura de Arquivos](./desenvolvimento/estrutura-arquivos.md) - Organização do projeto
- [Guia de Contribuição](./desenvolvimento/contribuicao.md) - Como contribuir
- [Cheats e Debug](./desenvolvimento/debug.md) - Ferramentas de desenvolvimento

### 📈 Histórico
- [Changelog](./changelog.md) - Histórico de mudanças
- [Roadmap](./roadmap.md) - Funcionalidades planejadas

## 🎯 Objetivos do Projeto

1. **Educacional**: Demonstrar conhecimentos em programação orientada a objetos
2. **Técnico**: Implementar sistemas complexos de forma modular e escalável
3. **Gameplay**: Criar uma experiência divertida e desafiadora
4. **Localização**: Jogo totalmente em português brasileiro

## 🚀 Quick Start

```bash
# Clone o repositório
git clone [url-do-repositorio]

# Entre na pasta
cd project-game-py

# Execute o jogo
./rungame.sh
```

## 🎮 Visão Geral do Gameplay

O jogador controla um herói em busca da lendária Gema Eldritch, atravessando 4 fases desafiadoras:

1. **Floresta Sombria** - Tutorial e introdução às mecânicas
2. **Labirinto Místico** - Puzzles e exploração
3. **Fortaleza Antiga** - Combate intenso e chaves
4. **Confronto Final** - Boss e conclusão épica

## 🏆 Características Principais

- **Sistema de Combate 360°**: Ataque em área ao redor do personagem
- **5 Armas Diferentes**: Cada uma com características únicas
- **2 Magias**: Fogo (dano) e Cura
- **Sistema de Dificuldade**: 3 níveis que afetam gameplay
- **32 Conquistas**: Sistema completo de achievements
- **Save/Load**: 5 slots + auto-save
- **Interface Moderna**: UI com animações e efeitos visuais
- **Áudio Dinâmico**: Música contextual e efeitos sonoros
- **Minimapa**: No nível 3 para navegação (TAB)

## 📱 Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Pygame 2.6+**: Engine de desenvolvimento
- **PIL/Pillow**: Manipulação de imagens
- **JSON**: Persistência de dados
- **CSV**: Importação de mapas (Tiled)

---

📝 **Nota**: Esta documentação está em constante evolução. Última atualização: Julho 2025