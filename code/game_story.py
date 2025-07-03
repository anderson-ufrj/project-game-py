"""
NARRATIVA DO JOGO: CORRIDA PELA RELÍQUIA - A BUSCA PELA PEDRA MÍSTICA DO ZAPPAGURI
Game Story: The Zappaguri Mystic Stone Quest

=== CONTEXTO PRINCIPAL ===
Há milênios, a lendária PEDRA MÍSTICA DO ZAPPAGURI mantinha o equilíbrio entre os mundos.
Para protegê-la, os antigos sábios a dividiram em três essências menores e a ocultaram:
- Essência da Vida (Orbes Verdes - cura e regeneração)
- Essência da Força (Orbes Vermelhos - poder de combate)
- Essência da Velocidade (Orbes Azuis - agilidade e movimento)
- A PEDRA MÍSTICA DO ZAPPAGURI (núcleo principal - poder absoluto)

O protagonista KAEL é um jovem aventureiro que descobriu os antigos pergaminhos
falando sobre a Pedra do Zappaguri. Quando forças sombrias começaram a despertar,
ele percebeu que apenas coletando as essências e encontrando a Pedra sagrada
poderia restaurar o equilíbrio e salvar seu mundo.

Sua jornada o levará através de quatro domínios perigosos, cada um guardado
por criaturas antigas que protegem os segredos da Pedra Mística...
"""

# Histórias entre fases (estilo Star Wars)
PHASE_STORIES = {
    "intro": {
        "title": "CORRIDA PELA RELÍQUIA",
        "subtitle": "Capítulo I: O Despertar da Busca",
        "text": [
            "Nas profundezas da biblioteca abandonada,",
            "KAEL descobriu os pergaminhos antigos que",
            "falavam de uma lenda esquecida:",
            "",
            "A PEDRA MÍSTICA DO ZAPPAGURI - uma relíquia",
            "de poder incomensurável que mantinha a paz",
            "entre os mundos por milênios.",
            "",
            "Quando sinais sombrios começaram a surgir,",
            "Kael compreendeu que apenas encontrando",
            "a Pedra sagrada e coletando suas essências",
            "poderia impedir o caos iminente.",
            "",
            "Sua jornada começa na FLORESTA ANCESTRAL,",
            "onde as primeiras Essências da Vida",
            "aguardam entre as criaturas guardiãs",
            "da natureza..."
        ]
    },
    
    "phase_1": {
        "title": "ESSÊNCIAS DA VIDA",
        "subtitle": "Capítulo II: A Floresta dos Guardiões",
        "text": [
            "Kael coletou as primeiras ESSÊNCIAS DA VIDA",
            "na Floresta Ancestral, sentindo sua força",
            "vital se renovar a cada orbe coletado.",
            "",
            "Os pergaminhos falam de um antigo",
            "LABIRINTO SUBTERRÂNEO onde as Essências",
            "da Força foram escondidas pelos sábios.",
            "",
            "Criaturas mais perigosas aguardam nas",
            "profundezas. O caminho até a Pedra do",
            "Zappaguri torna-se mais treacherous...",
            "",
            "Kael respira fundo e adentra as",
            "sombras do labirinto perdido..."
        ]
    },
    
    "phase_2": {
        "title": "ESSÊNCIAS DA FORÇA",
        "subtitle": "Capítulo III: O Labirinto das Profundezas",
        "text": [
            "No labirinto subterrâneo, Kael coletou",
            "as ESSÊNCIAS DA FORÇA, sentindo seu",
            "poder de combate se multiplicar.",
            "",
            "Os pergaminhos revelam a localização",
            "da FORTALEZA DOS QUATRO SELOS, onde",
            "as Essências da Velocidade foram",
            "protegidas por guardiões antigos.",
            "",
            "Quatro chaves místicas são necessárias",
            "para romper os selos da fortaleza.",
            "A jornada se intensifica..."
        ]
    },
    
    "phase_3": {
        "title": "ESSÊNCIAS DA VELOCIDADE",
        "subtitle": "Capítulo IV: A Fortaleza dos Quatro Selos",
        "text": [
            "Com as quatro chaves, Kael desbloqueou",
            "os selos da fortaleza e coletou as",
            "ESSÊNCIAS DA VELOCIDADE, ganhando",
            "agilidade sobre-humana.",
            "",
            "Agora, com todas as três essências,",
            "o caminho para a lendária PEDRA MÍSTICA",
            "DO ZAPPAGURI finalmente se revela.",
            "",
            "O SANTUÁRIO FINAL aguarda, guardado",
            "pelo mais temível dos guardiões antigos.",
            "O destino do mundo será decidido..."
        ]
    },
    
    "phase_4": {
        "title": "A PEDRA MÍSTICA DO ZAPPAGURI",
        "subtitle": "Capítulo V: O Santuário do Poder Absoluto",
        "text": [
            "No coração do Santuário Final,",
            "Kael finalmente encontrou a lendária",
            "PEDRA MÍSTICA DO ZAPPAGURI.",
            "",
            "Mas um guardião supremo se interpõe",
            "entre ele e a relíquia sagrada.",
            "A batalha derradeira começou!",
            "",
            "Com todas as essências coletadas,",
            "Kael sente o poder ancestral fluindo",
            "através de seu ser. O momento final",
            "da verdade chegou..."
        ]
    },
    
    "victory": {
        "title": "O EQUILÍBRIO RESTAURADO",
        "subtitle": "O Poder da Pedra Zappaguri Desperta",
        "text": [
            "Com a PEDRA MÍSTICA DO ZAPPAGURI",
            "em suas mãos e todas as essências",
            "reunidas, Kael canaliza o poder",
            "ancestral dos antigos sábios.",
            "",
            "A Pedra brilha intensamente, banindo",
            "as forças sombrias para as dimensões",
            "distantes de onde vieram.",
            "",
            "O equilíbrio entre os mundos está",
            "restaurado. Kael, agora guardião da",
            "Pedra Zappaguri, torna-se uma lenda.",
            "",
            "Mas ele sabe que sempre estará",
            "vigilante, protegendo o poder sagrado",
            "que une todos os mundos..."
        ]
    }
}

# Tradução dos elementos do jogo
GAME_ELEMENTS = {
    "health_orbs": "Fragmentos da Esmeralda de Cura",
    "attack_orbs": "Fragmentos do Cristal do Poder", 
    "speed_orbs": "Fragmentos do Orbe dos Ventos",
    "keys": "Chaves Místicas",
    "zappaguri_stone": "Pedra Mística do Zappaguri",
    
    "enemies": {
        "golu": "Guardião Sombrio",
        "bigboi": "Titã das Trevas", 
        "black": "Sombra Menor"
    },
    
    "levels": {
        "level1": "Ruínas Antigas",
        "level2": "Labirinto das Ilusões",
        "level3": "Fortaleza Sombria", 
        "level4": "Santuário Final"
    }
}