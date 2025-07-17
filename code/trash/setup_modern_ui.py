#!/usr/bin/env python3
"""
Script de Configuração Automática da UI Moderna
Instala dependências e configura o sistema modernizado
"""
import subprocess
import sys
import os
import shutil
from pathlib import Path

def print_banner():
    """Imprime banner de boas-vindas"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                🎮 MODERNIZAÇÃO COMPLETA DA UI 🎮             ║
║                                                              ║
║  Instalando sistema moderno de interface com:               ║
║  • Pygame GUI para elementos modernos                       ║
║  • Animações suaves e transições                           ║
║  • Temas personalizáveis (Dark/Light/Cyberpunk/Fantasy)    ║
║  • HUD moderno com gradientes                              ║
║  • Sistema de notificações toast                           ║
║  • Configurações avançadas com tabs                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")

def install_dependencies():
    """Instala dependências necessárias"""
    dependencies = [
        "pygame-gui==0.6.9",
        "pillow>=10.0.0",
        "numpy>=1.24.0",
        "cachetools>=5.3.0"
    ]
    
    print("\\n🔧 Instalando dependências...")
    
    for dep in dependencies:
        print(f"   📦 Instalando {dep}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", dep
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   ✅ {dep} instalado")
        except subprocess.CalledProcessError:
            print(f"   ❌ Erro ao instalar {dep}")
            print(f"   💡 Tente: pip install {dep}")

def create_backup():
    """Cria backup do sistema antigo"""
    print("\\n💾 Criando backup do sistema antigo...")
    
    backup_dir = Path("backup_ui_antiga")
    backup_dir.mkdir(exist_ok=True)
    
    old_files = [
        "main.py",
        "main_menu.py", 
        "settings_manager.py",
        "simple_audio_controls.py"
    ]
    
    for file in old_files:
        if Path(file).exists():
            shutil.copy2(file, backup_dir / file)
            print(f"   📁 Backup: {file}")
    
    print("   ✅ Backup criado em backup_ui_antiga/")

def create_launcher():
    """Cria launcher para o jogo modernizado"""
    launcher_content = '''#!/usr/bin/env python3
"""
Launcher do Jogo Modernizado
"""
from modern_game_manager import ModernGameManager

if __name__ == "__main__":
    try:
        game = ModernGameManager()
        game.run()
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Execute: python setup_modern_ui.py")
    except Exception as e:
        print(f"❌ Erro: {e}")
'''
    
    with open("run_modern_game.py", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    # Tornar executável no Linux/Mac
    if os.name != 'nt':
        os.chmod("run_modern_game.py", 0o755)
    
    print("🚀 Launcher criado: run_modern_game.py")

def create_config_files():
    """Cria arquivos de configuração"""
    print("\\n⚙️ Criando arquivos de configuração...")
    
    # Configuração de temas
    themes_config = {
        "default_theme": "dark",
        "themes": {
            "dark": {
                "primary": [52, 152, 219],
                "secondary": [46, 204, 113],
                "accent": [155, 89, 182],
                "background": [30, 30, 40],
                "surface": [45, 45, 60]
            },
            "light": {
                "primary": [41, 128, 185],
                "secondary": [39, 174, 96],
                "accent": [142, 68, 173],
                "background": [245, 245, 250],
                "surface": [255, 255, 255]
            }
        }
    }
    
    import json
    with open("ui_themes.json", "w", encoding="utf-8") as f:
        json.dump(themes_config, f, indent=2)
    
    # Configuração de qualidade
    quality_config = {
        "default_quality": "alta",
        "qualities": {
            "baixa": {
                "particles": False,
                "shadows": False,
                "fps_target": 30
            },
            "alta": {
                "particles": True,
                "shadows": True,
                "fps_target": 60
            }
        }
    }
    
    with open("quality_settings.json", "w", encoding="utf-8") as f:
        json.dump(quality_config, f, indent=2)
    
    print("   📄 ui_themes.json criado")
    print("   📄 quality_settings.json criado")

def test_installation():
    """Testa a instalação"""
    print("\\n🧪 Testando instalação...")
    
    try:
        import pygame_gui
        print("   ✅ pygame_gui importado")
        
        import numpy
        print("   ✅ numpy importado")
        
        import PIL
        print("   ✅ pillow importado")
        
        # Testar imports do jogo
        from modern_ui_system import modern_ui
        print("   ✅ Sistema de UI moderno")
        
        from modern_main_menu import ModernMainMenu
        print("   ✅ Menu principal moderno")
        
        from modern_hud import modern_hud
        print("   ✅ HUD moderno")
        
        from transition_manager import transition_manager
        print("   ✅ Gerenciador de transições")
        
        print("   🎉 Todos os sistemas funcionando!")
        
    except ImportError as e:
        print(f"   ❌ Erro de importação: {e}")
        return False
    
    return True

def show_usage_instructions():
    """Mostra instruções de uso"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                     🎮 INSTALAÇÃO COMPLETA! 🎮               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  COMO USAR O JOGO MODERNIZADO:                              ║
║                                                              ║
║  🚀 Executar jogo:                                          ║
║     python run_modern_game.py                               ║
║                                                              ║
║  ⌨️  Controles especiais:                                   ║
║     F1  - Alternar tema da UI                              ║
║     F2  - Alternar qualidade visual                        ║
║     F11 - Fullscreen                                       ║
║     ESC - Pausar/Menu                                       ║
║                                                              ║
║  🎨 Temas disponíveis:                                      ║
║     • Dark (escuro moderno)                                ║
║     • Light (claro elegante)                               ║
║     • Cyberpunk (neon futurista)                           ║
║     • Fantasy (medieval mágico)                            ║
║                                                              ║
║  ⚙️  Configurações:                                         ║
║     • Áudio separado (música/efeitos)                      ║
║     • Gráficos (resolução, qualidade)                      ║
║     • Controles personalizáveis                            ║
║     • Configurações de jogo                                ║
║                                                              ║
║  📁 Arquivos importantes:                                   ║
║     backup_ui_antiga/ - Backup do sistema antigo           ║
║     ui_themes.json    - Configuração de temas              ║
║     quality_settings.json - Configurações de qualidade     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def main():
    """Função principal"""
    print_banner()
    
    try:
        check_python_version()
        install_dependencies()
        create_backup()
        create_config_files()
        create_launcher()
        
        if test_installation():
            show_usage_instructions()
            print("\\n🎉 Modernização completa! Execute: python run_modern_game.py")
        else:
            print("\\n❌ Instalação falhou. Verifique as dependências.")
            
    except KeyboardInterrupt:
        print("\\n❌ Instalação cancelada pelo usuário")
    except Exception as e:
        print(f"\\n❌ Erro durante instalação: {e}")

if __name__ == "__main__":
    main()