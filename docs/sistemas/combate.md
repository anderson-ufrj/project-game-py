# ⚔️ Sistema de Combate

## 📋 Visão Geral

O sistema de combate de "Corrida pela Relíquia" oferece uma experiência dinâmica com ataques físicos, mágicos e mecânicas especiais como o ataque 360°.

## 🗡️ Armas

### Tipos Disponíveis

| Arma | Dano | Cooldown | Alcance | Sprite |
|------|------|----------|---------|---------|
| **Sword** | 15 | 100ms | Médio | sword_full.png |
| **Lance** | 20 | 300ms | Longo | lance_full.png |
| **Axe** | 20 | 200ms | Médio | axe_full.png |
| **Rapier** | 8 | 50ms | Curto | rapier_full.png |
| **Sai** | 10 | 80ms | Curto | sai_full.png |

### Mecânica de Troca
- **Tecla Q**: Cicla entre as armas
- Mensagem visual ao trocar
- Sem custo ou penalidade
- Mudança instantânea

### Sistema de Ataque 360°

#### Implementação
```python
# Classe Weapon360Damage
- Área invisível ao redor do jogador
- Raio de 60 pixels
- Duração de 1 frame
- Detecta colisão com todos os inimigos próximos
```

#### Características
- **Visual**: Mantém animação direcional original
- **Dano**: Atinge todos os inimigos no raio
- **Cooldown**: Baseado na arma equipada
- **Sem custo**: Não consome recursos

## 🔮 Sistema de Magia

### Tipos de Magia

#### 1. **Flame (Fogo)**
- **Tipo**: Ofensiva
- **Dano**: Base 5 + Magic Stat
- **Custo**: 20 de energia
- **Efeito**: Dano contínuo (3s)
- **Visual**: Partículas de fogo

#### 2. **Heal (Cura)**
- **Tipo**: Suporte
- **Cura**: Base 20 + Magic Stat
- **Custo**: 20 de energia
- **Efeito**: Recupera vida instantânea
- **Visual**: Partículas verdes

### Mecânica de Uso
- **Tecla E**: Alterna entre magias
- **Tecla Ctrl**: Lança magia selecionada
- Consome energia do jogador
- Cooldown de 300ms

## 💥 Cálculo de Dano

### Dano do Jogador

```python
dano_total = dano_base_arma + attack_stat

# Com modificador de dificuldade
dano_final = dano_total * difficulty_modifier
```

### Dano dos Inimigos

```python
dano_base = enemy.attack_damage

# Com modificador de dificuldade
dano_final = dano_base * difficulty_modifier
```

## 🛡️ Sistema de Defesa

### Invulnerabilidade
- **Duração**: 500ms (jogador) / 300ms (inimigo)
- **Visual**: Efeito de piscar (flicker)
- **Ativação**: Após receber dano
- **Propósito**: Evitar dano contínuo

### Knockback
- **Força**: Baseada na resistência do alvo
- **Direção**: Oposta ao atacante
- **Fórmula**: `knockback = 3 * (1 - resistance)`

## 🎯 Detecção de Colisão

### Sistema de Sprites
```python
# Grupos de colisão
- attack_sprites: Armas ativas
- attackable_sprites: Alvos válidos
- obstacle_sprites: Bloqueios de movimento
```

### Hitboxes
- **Player**: Retângulo ajustado ao sprite
- **Enemy**: Retângulo com offset vertical
- **Weapon**: Área circular (360°) ou retangular

## 🔥 Efeitos de Status

### Fogo (Fire Effect)
- **Duração**: 3 segundos
- **Dano**: 1/3 do dano inicial a cada 0.5s
- **Visual**: Overlay vermelho + partículas
- **Stackable**: Não (reseta timer)

### Gelo (Ice Effect)
- **Duração**: 2 segundos
- **Efeito**: Reduz velocidade em 50%
- **Visual**: Overlay azul + partículas
- **Stackable**: Não (reseta timer)

## 📊 Estatísticas de Combate

### Player Stats
```python
# Base
health = 500
energy = 120
attack = 10
magic = 4
speed = 3

# Modificados por dificuldade
health *= difficulty_health_modifier
attack *= difficulty_attack_modifier
```

### Enemy Stats (Exemplo: Bamboo)
```python
health = 70
exp = 40
speed = 3
attack_damage = 10
resistance = 3
attack_radius = 20
notice_radius = 300
```

## 🎮 Combos e Técnicas

### Técnicas Básicas
1. **Hit and Run**: Atacar e recuar
2. **Kiting**: Manter distância usando velocidade
3. **Area Control**: Usar ataque 360° contra grupos

### Combos Efetivos
1. **Fire + Melee**: Aplicar fogo e atacar
2. **Ice + Heavy Weapon**: Congelar e usar axe/lance
3. **Heal + Tank**: Curar-se e enfrentar diretamente

## 🏃 Sistema de Energia

### Consumo
- **Correr**: 0.2/frame (com Shift)
- **Magia**: 20 por uso
- **Ataque**: Sem custo

### Regeneração
- **Taxa**: 0.15/frame quando parado
- **Máximo**: 120 pontos
- **Visual**: Barra azul na UI

## 🎯 IA dos Inimigos

### Estados de Comportamento

#### 1. **Idle**
- Sem detecção do jogador
- Movimento aleatório mínimo
- Animação idle

#### 2. **Alert**
- Jogador dentro do notice_radius
- Perseguição ativa
- Pathfinding básico

#### 3. **Attack**
- Jogador dentro do attack_radius
- Executa ataque
- Cooldown antes do próximo

### Estratégias por Tipo
- **Bamboo**: Perseguição direta
- **Spirit**: Ataques à distância
- **Raccoon**: Movimento errático
- **Squid**: Ataques em área

## 💀 Sistema de Morte

### Morte do Jogador
1. Vida chega a 0
2. Transição para Game Over
3. Opção de retry no menu

### Morte de Inimigos
1. Vida chega a 0
2. Animação de explosão (20 partículas)
3. Drop de experiência
4. Possível drop de orbes
5. Som de morte
6. Registro nas estatísticas

## 🎨 Feedback Visual

### Indicadores de Dano
- **Números de dano**: Não implementado
- **Screen shake**: Não implementado
- **Flash de hit**: Via invulnerabilidade
- **Partículas**: Na morte e efeitos

### Health Bars
- **Jogador**: UI fixa no canto
- **Inimigos**: Flutuante acima do sprite
- **Cores**: Verde → Amarelo → Vermelho

## ⚙️ Configurações de Balanceamento

### Modificadores por Dificuldade

#### Fácil
- Player Health: +50%
- Player Attack: +20%
- Enemy Health: -30%
- Enemy Attack: -20%

#### Normal
- Todos os valores: 100%

#### Difícil
- Player Health: -30%
- Player Attack: -10%
- Enemy Health: +50%
- Enemy Attack: +30%

## 🔧 Otimizações

### Performance
1. **Collision Groups**: Apenas sprites relevantes
2. **Spatial Hashing**: Não implementado
3. **Object Pooling**: Parcial (partículas)

### Melhorias Futuras
1. Sistema de combo counter
2. Parry/block mechanics
3. Elemental weaknesses
4. Critical hits
5. Status effect stacking

---

[← Voltar: Fluxo do Jogo](../fluxo-jogo.md) | [Índice](../README.md) | [Próximo: Sistema de Áudio →](./audio.md)