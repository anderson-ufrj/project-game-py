#!/bin/bash
# Script para instalar dependências da UI moderna

echo "🎨 Instalando dependências para modernização da UI..."

# Pygame GUI - Interface moderna
pip install pygame-gui==0.6.9

# Efeitos visuais avançados
pip install pillow>=10.0.0
pip install numpy>=1.24.0

# Cache de gradientes e efeitos
pip install cachetools>=5.3.0

echo "✅ Dependências instaladas com sucesso!"
echo "📝 Pygame GUI: Interface moderna com temas"
echo "📝 Pillow: Processamento avançado de imagens"
echo "📝 NumPy: Cálculos para efeitos visuais"
echo "📝 CacheTools: Otimização de performance"