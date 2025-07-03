"""
Projeto Ícaro - Jogo de Plataforma Mitológico
Versão 2.0 Refatorada

Desenvolvido por: Anderson Henrique
Instituição: IFSULDEMINAS – Campus Muzambinho
Disciplina: Tópicos Especiais I
"""

import sys
import os

# Adiciona o diretório src ao path para importações
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.game_manager import main

if __name__ == "__main__":
    main()