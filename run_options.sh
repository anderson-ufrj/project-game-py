#!/bin/bash

# Script com opções para executar diferentes versões do jogo

echo "🎮 CORRIDA PELA RELÍQUIA - Seletor de Versões"
echo "📍 Projeto: Tópicos Especiais I - IFSULDEMINAS Muzambinho"
echo "👨‍🎓 Aluno: Anderson Henrique da Silva"
echo ""

# Verificar se está no diretório correto
if [ ! -d "code" ]; then
    echo "❌ Erro: Execute este script a partir do diretório raiz do projeto!"
    echo "💡 Certifique-se de estar em: project-game-py/"
    exit 1
fi

# Menu de opções
echo "Escolha qual versão executar:"
echo ""
echo "1) 🎮 Jogo Original (Recomendado)"
echo "2) 🔗 Versão Híbrida (Nova Arquitetura + Jogo)"
echo "3) 🆕 Nova Arquitetura (Apenas Teste)"
echo "4) 📝 Jogo Original com Logging Aprimorado"
echo "5) ❌ Cancelar"
echo ""

read -p "Digite sua escolha (1-5): " choice

# Verificar ambiente virtual
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar pygame
if ! python -c "import pygame" 2>/dev/null; then
    echo "📥 Instalando pygame..."
    pip install pygame
fi

# Entrar no diretório do código
cd code

case $choice in
    1)
        echo ""
        echo "🎮 Executando Jogo Original (Versão Estável)..."
        echo "⚡ Iniciando em 2 segundos..."
        sleep 2
        python3 main.py
        ;;
    2)
        echo ""
        echo "🔗 Executando Versão Híbrida..."
        echo "💡 Use SPACE/ENTER para iniciar o jogo original"
        echo "⚡ Iniciando em 2 segundos..."
        sleep 2
        python3 main_hybrid.py
        ;;
    3)
        echo ""
        echo "🆕 Executando Nova Arquitetura (Teste)..."
        echo "💡 Use ESC para sair"
        echo "⚡ Iniciando em 2 segundos..."
        sleep 2
        python3 main_new.py
        ;;
    4)
        echo ""
        echo "📝 Executando Jogo Original com Logging..."
        echo "⚡ Iniciando em 2 segundos..."
        sleep 2
        python3 main_direct.py
        ;;
    5)
        echo "❌ Cancelado pelo usuário"
        cd ..
        exit 0
        ;;
    *)
        echo "❌ Opção inválida! Executando versão original..."
        sleep 1
        python3 main.py
        ;;
esac

# Voltar ao diretório original
cd ..

echo ""
echo "🎮 Obrigado por jogar Corrida pela Relíquia!"
echo "📚 Projeto desenvolvido para IFSULDEMINAS Campus Muzambinho"