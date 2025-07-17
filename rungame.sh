#!/bin/bash

# Script para executar o jogo Corrida pela Relíquia
# Criado para facilitar a execução do projeto

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
echo "   ➤ Espaço: Ataque (dano 360°!) - MELHORADO!"
echo "   ➤ Q: Trocar arma (5 armas disponíveis!) - NOVO!"
echo "   ➤ E: Trocar magia (Chama/Cura) - NOVO!"
echo "   ➤ Ctrl: Usar magia - NOVO!"
echo "   ➤ Enter: Iniciar jogo"
echo "   ➤ ⚙️ Engrenagem (mouse): Menu de configurações"
echo "   ➤ M: Liga/Desliga som | ↑↓: Volume"
echo "   ➤ TAB: Minimapa (Fase 3)"
echo ""
echo "🎯 Objetivo: Encontre a Pedra Mística de Zappaguri através de 4 níveis!"
echo "🌟 Novidades: Ataque 360°, Sistema de Armas, Magias, Histórias épicas!"
echo "🏗️ NOVA ARQUITETURA: Código modular e profissional!"
echo ""
echo "⚡ Iniciando jogo em 3 segundos..."
sleep 3

# Detectar qual versão usar
if [ -f "main_with_modern_audio.py" ]; then
    echo "🎵 Executando com controles de áudio modernos..."
    python3 main_with_modern_audio.py
else
    echo "🎮 Executando jogo original (versão estável)..."
    python3 main.py
fi

# Versões alternativas (descomentadas para testar)
# if [ -f "main_direct.py" ]; then
#     echo "🎮 Executando jogo original com logging aprimorado..."
#     python3 main_direct.py
# elif [ -f "main_hybrid.py" ]; then
#     echo "🔗 Usando versão híbrida (Nova Arquitetura + Jogo Original)..."
#     python3 main_hybrid.py
# elif [ -f "main_new.py" ]; then
#     echo "🆕 Usando nova arquitetura (apenas teste)..."
#     python3 main_new.py
# fi

# Voltar ao diretório original
cd ..

echo ""
echo "🎮 Obrigado por jogar Corrida pela Relíquia!"
echo "📚 Projeto desenvolvido para IFSULDEMINAS Campus Muzambinho"