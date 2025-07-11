# 🎮 Controles do Jogo

## 📋 Visão Geral

"Corrida pela Relíquia" oferece controles intuitivos para teclado, com comandos específicos para cada situação do jogo.

## ⌨️ Controles por Contexto

### 🏠 Menu Principal

| Tecla | Ação | Descrição |
|-------|------|-----------|
| **Mouse** | Navegar | Mover cursor sobre opções |
| **Click** | Selecionar | Confirmar opção |
| **Enter** | Iniciar Jogo | Começa nova partida |
| **S** | Estatísticas | Abre tela de stats |
| **D** | Dificuldade | Abre seleção de dificuldade |
| **L** | Carregar | Abre tela de load |
| **M** | Mute | Liga/desliga som |
| **↑/↓** | Volume | Ajusta volume do áudio |
| **G** | Gráficos | Configurações gráficas |
| **Alt+Enter** | Fullscreen | Alterna tela cheia |
| **ESC** | Sair | Fecha o jogo |

#### 🎯 Atalhos de Debug (Menu)
| Tecla | Ação |
|-------|------|
| **1** | Ir para Level 1 |
| **2** | Ir para Level 2 |
| **3** | Ir para Level 3 |
| **4** | Ir para Level 4 |

### 🎮 Controles In-Game

#### Movimento
| Tecla | Ação | Detalhes |
|-------|------|----------|
| **W** ou **↑** | Mover para cima | Velocidade base: 3 |
| **A** ou **←** | Mover para esquerda | Movimento 8 direções |
| **S** ou **↓** | Mover para baixo | Normalizado diagonal |
| **D** ou **→** | Mover para direita | Colisão com obstacles |
| **Shift** | Correr | +3 velocidade, gasta energia |

#### Combate
| Tecla | Ação | Detalhes |
|-------|------|----------|
| **Space** | Atacar | Ataque 360° com arma atual |
| **Q** | Trocar Arma | Cicla entre 5 armas |
| **E** | Trocar Magia | Alterna Flame/Heal |
| **Ctrl** | Usar Magia | Gasta 20 de energia |

#### Interface
| Tecla | Ação | Contexto |
|-------|------|----------|
| **TAB** | Minimapa | Apenas no Level 3 |
| **M** | Mute | Toggle áudio |
| **↑/↓** | Volume | Ajusta som |
| **ESC** | Pausar* | *Não implementado |

### 💾 Sistema de Save

| Tecla | Ação | Descrição |
|-------|------|-----------|
| **F5** | Quick Save | Salva no slot 0 (auto-save) |
| **F9** | Quick Load | Abre tela de load |
| **F6** | Save Menu | Abre interface de save |

### 🛠️ Comandos de Debug

| Tecla | Ação | Descrição |
|-------|------|-----------|
| **F1** | Level 1 | Pula direto para floresta |
| **F2** | Level 2 | Pula para labirinto |
| **F3** | Level 3 | Pula para fortaleza |
| **F4** | Level 4 | Pula para boss |

## 🎯 Detalhes de Controle

### 🏃 Sistema de Movimento

#### Movimento Normal
- **Velocidade Base**: 3 pixels/frame
- **Direções**: 8 (incluindo diagonais)
- **Normalização**: Velocidade consistente em diagonais
- **Colisão**: Sliding contra paredes

#### Corrida (Sprint)
- **Ativação**: Segurar Shift
- **Velocidade**: +3 (total: 6)
- **Custo**: 0.2 energia/frame
- **Limitação**: Para quando energia = 0
- **Regeneração**: 0.15/frame quando parado

### ⚔️ Sistema de Combate

#### Ataque Físico
- **Tecla**: Space
- **Tipo**: Área 360° ao redor
- **Alcance**: 60 pixels de raio
- **Cooldown**: Varia por arma (50-300ms)
- **Dano**: Base da arma + stat de ataque

#### Troca de Armas
```
Q → Sword → Lance → Axe → Rapier → Sai → (volta ao início)
```

#### Sistema de Magia
- **Seleção**: E alterna entre Flame/Heal
- **Uso**: Ctrl lança a magia selecionada
- **Custo**: 20 de energia
- **Cooldown**: 300ms
- **Indicador**: Nome da magia na UI

### 📊 Controles de Interface

#### Volume
- **Incremento**: 10% por tecla
- **Visual**: Slider animado
- **Feedback**: Barras de equalização
- **Persistência**: Salvo entre sessões

#### Tela Cheia
- **Toggle**: Alt+Enter
- **Preservação**: Mantém resolução
- **Aplicação**: Imediata

### 🗺️ Minimapa (Level 3)

#### Controles
- **TAB**: Mostrar/esconder
- **Informações**:
  - Posição do jogador
  - Chaves coletadas/necessárias
  - Status da saída
  - Dicas de localização

## 🎮 Fluxo de Input

### Prioridade de Processamento
1. **Eventos de Sistema** (QUIT, Alt+Enter)
2. **Cheats/Debug** (F1-F4)
3. **Controles de Áudio** (M, ↑↓)
4. **Save/Load** (F5, F6, F9)
5. **Gameplay** (movimento, combate)

### Event Handling
```python
# Ordem de processamento
1. main.py captura eventos
2. Filtra eventos de sistema
3. Passa para audio_manager
4. Reposta eventos para levels
5. Level processa gameplay
```

## 🎨 Feedback Visual

### Indicadores de Estado
| Estado | Visual |
|--------|--------|
| **Correndo** | Animação acelerada |
| **Atacando** | Animação de swing |
| **Invulnerável** | Piscando (flicker) |
| **Sem energia** | Barra vermelha |
| **Arma atual** | Ícone na UI |

### Confirmações Visuais
- **Troca de arma**: Nome aparece brevemente
- **Save realizado**: Mensagem de confirmação
- **Volume alterado**: Slider se move
- **Mute ativado**: Ícone muda

## 🔧 Configurações Avançadas

### Sensibilidade (Não Implementado)
- Movimento tem velocidade fixa
- Sem aceleração/desaceleração
- Sem configuração de sensibilidade

### Remapeamento (Não Implementado)
- Controles são fixos
- Não há suporte para customização
- Padrão otimizado para QWERTY

## 💡 Dicas de Uso

### Combate Eficiente
1. **Kiting**: Use Sprint para manter distância
2. **Gestão de Energia**: Alterne corrida/regeneração
3. **Combo Mágico**: Flame + ataque físico
4. **Posicionamento**: Use 360° contra grupos

### Navegação
1. **Quick Save frequente**: F5 antes de áreas perigosas
2. **Minimapa**: TAB no Level 3 para orientação
3. **Sprint estratégico**: Economize para fugas

### Interface
1. **Volume rápido**: ↑↓ sem abrir menu
2. **Fullscreen**: Alt+Enter para imersão
3. **Stats**: S para ver progresso

## 🚫 Limitações Conhecidas

### Não Suportado
- Controle/Joystick
- Mouse para movimento
- Customização de teclas
- Macros ou combos

### Problemas Conhecidos
- Diagonal pode parecer mais rápida visualmente
- Alguns eventos podem ser perdidos em transições
- Sem suporte para teclados não-QWERTY

---

[← Voltar: Sistema UI](../sistemas/ui.md) | [Índice](../README.md) | [Próximo: Personagem →](./personagem.md)