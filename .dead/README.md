# Wizarding Duel: Varinha vs Diabretes

Um jogo mágico inspirado no mundo de Harry Potter onde você controla uma varinha mágica voadora para repelir diabretes da Cornualha.

## Características do Jogo

- **Controle de varinha mágica voadora**: Use as setas ou WASD para mover
- **Sistema de feitiços**: Pressione ESPAÇO para lançar feitiços mágicos
- **Múltiplas varinhas**: Escolha entre diferentes tipos de varinha (Clássica, Sabugueiro, Azevinho, Cristal)
- **Diversos inimigos**: Enfrente diferentes tipos de diabretes (Azul, Verde, Fada, Sombrio)
- **Fundo mágico animado**: Galáxia com estrelas e partículas mágicas em movimento
- **Sistema de pontuação e níveis**: A dificuldade aumenta com o tempo
- **Gráficos gerados proceduralmente**: Todas as imagens são criadas pelo próprio jogo

## Instalação e Execução

### Pré-requisitos
- Python 3.7 ou superior
- pygame

### Instalação das Dependências

**Opção 1: Usando o script automático (recomendado)**
```bash
./run.sh
```

**Opção 2: Instalação manual**
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Como Jogar

**Opção 1: Usando o script (mais fácil)**
```bash
./run.sh
```

**Opção 2: Execução manual**
```bash
source venv/bin/activate
python3 jogo.py
```

## Controles

- **Movimento**: Setas direcionais ou WASD
- **Lançar feitiços**: ESPAÇO
- **Pausar**: ESC
- **Menu**: ENTER para começar/confirmar
- **Seleção de personagem**: Setas para navegar, CIMA/BAIXO para alternar entre seletores

## Gameplay

1. **Menu Principal**: Pressione ENTER para começar
2. **Seleção de Personagem**: 
   - Escolha sua varinha mágica
   - Escolha o tipo de diabrete que enfrentará
   - Use as setas para navegar e ENTER para confirmar
3. **Jogo**: 
   - Mova sua varinha para evitar diabretes e seus feitiços
   - Lance feitiços para destruir os diabretes
   - Ganhe pontos e sobreviva o máximo de tempo possível
   - A dificuldade aumenta com o tempo

## Estrutura do Projeto

```
project-game-py/
├── jogo.py              # Arquivo principal do jogo
├── requirements.txt     # Dependências do projeto
├── README.md           # Este arquivo
├── assets/             # Diretório para recursos (criado automaticamente)
│   ├── images/         # Imagens (geradas proceduralmente)
│   └── sounds/         # Sons (gerados proceduralmente)
└── images/             # Diretório adicional de imagens (criado automaticamente)
```

## Características Técnicas

- **Engine**: pygame
- **Gráficos**: Gerados proceduralmente (sem arquivos externos)
- **Sons**: Gerados programaticamente
- **Resolução**: 800x600 pixels
- **FPS**: 60 quadros por segundo

## Tipos de Varinha

1. **Varinha Clássica**: Varinha tradicional marrom
2. **Varinha de Sabugueiro**: A varinha mais poderosa (inspirada em Harry Potter)
3. **Varinha de Azevinho**: Varinha do Harry Potter
4. **Varinha de Cristal**: Varinha mágica translúcida

## Tipos de Diabrete

1. **Diabrete Azul**: Diabrete padrão da Cornualha
2. **Duende Verde**: Variante verde dos diabretes
3. **Fada da Floresta**: Criatura mágica mais amigável
4. **Diabrete Sombrio**: Versão mais sinistra com olhos vermelhos

## Sistema de Dificuldade

- O nível aumenta a cada 30 segundos
- Diabretes aparecem mais frequentemente
- Diabretes ganham mais vida em níveis altos
- Pontuação aumenta com a dificuldade

Divirta-se jogando Wizarding Duel!