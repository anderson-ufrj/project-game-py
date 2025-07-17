#!/bin/bash

# Script oficial para executar Corrida pela Relíquia
# Projeto: Tópicos Especiais I - IFSULDEMINAS Muzambinho
# Aluno: Anderson Henrique da Silva

echo "🎮 Iniciando Corrida pela Relíquia..."
echo "📍 Projeto: Tópicos Especiais I - IFSULDEMINAS Muzambinho"
echo "👨‍🎓 Aluno: Anderson Henrique da Silva"
echo ""

# Verificar se está no diretório correto
if [ ! -d "code" ]; then
    echo "❌ Erro: Execute este script a partir do diretório raiz do projeto!"
    echo "💡 Certifique-se de estar em: project-game-py/"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar ambiente virtual!"
        echo "💡 Certifique-se de ter python3 instalado"
        exit 1
    fi
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se pygame está instalado
if ! python -c "import pygame" 2>/dev/null; then
    echo "📥 Instalando pygame..."
    pip install pygame
    
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar pygame!"
        exit 1
    fi
fi

# Entrar no diretório do código
cd code

# Executar o jogo
echo "🚀 Executando o jogo..."
echo ""
echo "🎮 Controles:"
echo "   ➤ Setas: Movimento"
echo "   ➤ Shift: Correr"
echo "   ➤ Espaço: Ataque (dano 360°!)"
echo "   ➤ Q: Trocar arma (5 armas disponíveis!)"
echo "   ➤ E: Trocar magia (Chama/Cura)"
echo "   ➤ Ctrl: Usar magia"
echo "   ➤ Enter: Iniciar jogo"
echo "   ➤ M: Liga/Desliga som | ↑↓: Volume"
echo "   ➤ TAB: Minimapa (Fase 3)"
echo ""
echo "🎯 Objetivo: Encontre a Pedra Mística de Zappaguri através de 4 níveis!"
echo ""
echo "⚡ Iniciando jogo em 3 segundos..."
sleep 3

# Executar versão oficial
echo "🎮 Executando Corrida pela Relíquia..."
python3 main.py

# Voltar ao diretório original
cd ..

echo ""
echo "🎮 Obrigado por jogar Corrida pela Relíquia!"
echo "📚 Projeto desenvolvido para IFSULDEMINAS Campus Muzambinho"