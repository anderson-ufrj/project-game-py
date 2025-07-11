#!/bin/bash

echo "🚀 Instalando bibliotecas modernas para UI profissional..."
echo "📍 Projeto: Corrida pela Relíquia - Modernização Gráfica"

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    echo "🔧 Ativando ambiente virtual..."
    source venv/bin/activate
fi

echo "📦 Instalando bibliotecas essenciais..."

# Bibliotecas para UI moderna e efeitos visuais
pip install pygame-gui
pip install numpy
pip install scipy

# Bibliotecas para processamento de imagem avançado
pip install opencv-python-headless

# Bibliotecas para efeitos visuais e matemática
pip install pillow --upgrade

# Bibliotecas opcionais para efeitos avançados
echo "📦 Instalando bibliotecas opcionais..."
pip install pygame-menu
pip install moderngl-window

# Verificar instalações
echo "✅ Verificando instalações..."
python3 -c "
try:
    import pygame_gui
    print('✅ pygame-gui instalado com sucesso')
except ImportError:
    print('❌ Erro na instalação do pygame-gui')

try:
    import numpy
    print('✅ numpy instalado com sucesso')
except ImportError:
    print('❌ Erro na instalação do numpy')

try:
    import cv2
    print('✅ opencv-python instalado com sucesso')
except ImportError:
    print('❌ Erro na instalação do opencv-python')

try:
    import pygame_menu
    print('✅ pygame-menu instalado com sucesso')
except ImportError:
    print('❌ Erro na instalação do pygame-menu')
"

echo "🎉 Instalação concluída!"
echo "🎮 Agora você pode usar componentes UI profissionais no jogo!"