"""
NARRATIVA DO JOGO: O GUARDIÃO DAS RELÍQUIAS PERDIDAS
Game Story: The Guardian of Lost Relics

=== CONTEXTO PRINCIPAL ===
Era uma vez um reino em harmonia, protegido por quatro Relíquias Sagradas:
- Relíquia da Vida (Esmeralda de Cura)
- Relíquia da Força (Cristal do Poder)  
- Relíquia da Velocidade (Orbe dos Ventos)
- Relíquia Suprema (Pedra Mística do Zappaguri)

O protagonista KAEL é o último Guardião da Ordem dos Protetores,
uma antiga ordem de guerreiros que protegia essas relíquias.

As Sombras Corrompidas invadiram o reino e espalharam as relíquias
pelos quatro domínios sombrios. Kael deve recuperá-las antes que
o reino seja consumido pela escuridão eterna.
"""

# Histórias entre fases (estilo Star Wars)
PHASE_STORIES = {
    "intro": {
        "title": "O GUARDIÃO DAS RELÍQUIAS",
        "subtitle": "Episódio I: O Despertar das Sombras",
        "text": [
            "Há muito tempo, em um reino distante...",
            "",
            "O último guardião KAEL desperta em",
            "um mundo devastado pelas SOMBRAS",
            "CORROMPIDAS que roubaram as quatro",
            "Relíquias Sagradas do reino.",
            "",
            "Com apenas sua espada e coragem,",
            "Kael deve atravessar os domínios",
            "sombrios para recuperar as relíquias",
            "e restaurar o equilíbrio perdido.",
            "",
            "A jornada começa nas RUÍNAS",
            "ANTIGAS, onde a primeira relíquia",
            "aguarda entre perigos mortais..."
        ]
    },
    
    "level_1_to_2": {
        "title": "A PRIMEIRA RELÍQUIA",
        "subtitle": "A Esmeralda de Cura foi recuperada",
        "text": [
            "Kael conquistou a ESMERALDA DE CURA",
            "nas Ruínas Antigas, sentindo suas",
            "feridas se regenerarem rapidamente.",
            "",
            "Mas as Sombras Corrompidas crescem",
            "mais fortes. Ele deve seguir para o",
            "LABIRINTO DAS ILUSÕES, onde a",
            "Relíquia da Força está escondida.",
            "",
            "Os ecos de risadas sinistras ecoam",
            "pelos corredores infinitos...",
            "Kael avança, determinado."
        ]
    },
    
    "level_2_to_3": {
        "title": "O PODER CRESCENTE",
        "subtitle": "O Cristal do Poder fortalece o guardião",
        "text": [
            "O CRISTAL DO PODER pulsa em suas",
            "mãos, multiplicando sua força de",
            "combate contra as criaturas sombrias.",
            "",
            "Duas relíquias recuperadas, duas ainda",
            "perdidas. Kael segue para a FORTALEZA",
            "SOMBRIA, onde a Relíquia da Velocidade",
            "está guardada pelo temível BIGBOI.",
            "",
            "As chaves mágicas serão necessárias",
            "para atravessar as defesas da fortaleza.",
            "A batalha se intensifica..."
        ]
    },
    
    "level_3_to_4": {
        "title": "A VELOCIDADE DOS VENTOS",
        "subtitle": "O Orbe dos Ventos acelera o destino",
        "text": [
            "Com o ORBE DOS VENTOS, Kael move-se",
            "como o próprio vento, esquivando dos",
            "ataques das Sombras Corrompidas.",
            "",
            "Apenas uma relíquia resta: a lendária",
            "PEDRA MÍSTICA DO ZAPPAGURI, guardada",
            "no SANTUÁRIO FINAL pelas forças",
            "mais sombrias do reino.",
            "",
            "Kael reúne todas as suas forças.",
            "O destino do reino será decidido",
            "na batalha final..."
        ]
    },
    
    "victory": {
        "title": "O EQUILÍBRIO RESTAURADO",
        "subtitle": "O Guardião cumpriu sua missão",
        "text": [
            "Com as quatro Relíquias Sagradas",
            "reunidas, Kael canaliza o poder",
            "ancestral dos Guardiões.",
            "",
            "A PEDRA MÍSTICA DO ZAPPAGURI brilha intensamente,",
            "banindo as Sombras Corrompidas para",
            "as dimensões distantes de onde vieram.",
            "",
            "O reino está salvo. A ordem é",
            "restaurada. Kael, o último Guardião,",
            "torna-se uma lenda.",
            "",
            "Mas ele sabe que sempre estará",
            "vigilante, protegendo o equilíbrio",
            "entre luz e escuridão..."
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