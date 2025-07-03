#!/bin/bash
# Script para executar o Projeto Ícaro

echo "🎮 Iniciando Projeto Ícaro..."
echo "📦 Ativando ambiente virtual..."

# Ativa o ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Ambiente virtual ativado"
else
    echo "⚠️  Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "✅ Ambiente virtual criado e dependências instaladas"
fi

echo "🚀 Executando jogo..."
python main_new.py