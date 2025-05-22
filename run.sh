#!/bin/bash

# Script para executar o jogo Wizarding Duel
# Ativa o ambiente virtual e executa o jogo

echo "Iniciando Wizarding Duel: Varinha vs Diabretes..."

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
fi

# Ativa o ambiente virtual
source venv/bin/activate

# Instala dependências se necessário
if ! python -c "import pygame" 2>/dev/null; then
    echo "Instalando dependências..."
    pip install -r requirements.txt
fi

# Executa o jogo
echo "Executando o jogo..."
python jogo.py