# 🧹 Plano de Limpeza do Projeto

## 📋 Arquivos e Pastas para Remover

### 🗂️ **Arquivos de Documentação Desnecessários**
- ❌ `CLAUDE.local.md` - Arquivo local, não deve ir para GitHub
- ❌ `CHEAT_REMOVAL_INSTRUCTIONS.md` - Instruções antigas, não relevantes
- ❌ `ICONS_DOCUMENTATION.md` - Documentação já incluída em docs/

### 🗂️ **Código Obsoleto e Backup**
- ❌ `code/backup_ui_original/` - Backups antigos da UI
- ❌ `code/trash/` - Pasta completa de arquivos descartados
- ❌ `code/apply_ui_improvements.py` - Script temporário
- ❌ `code/homescreen.py` - Arquivo obsoleto
- ❌ `code/intermediate.py` - Arquivo não usado
- ❌ `code/intro.py` - Arquivo não usado
- ❌ `code/main_direct.py` - Versão alternativa não usada
- ❌ `code/main_hybrid.py` - Versão alternativa não usada
- ❌ `code/main_new.py` - Versão alternativa não usada
- ❌ `code/name_input_screen_old.py` - Versão antiga
- ❌ `code/simple_audio_controls.py` - Substituído por modern_audio_controls
- ❌ `code/test_audio.py` - Arquivo de teste
- ❌ `code/test_new_architecture.py` - Arquivo de teste
- ❌ `code/ui.py.bak` - Backup antigo
- ❌ `code/ui_enhanced.py` - Arquivo não usado
- ❌ `code/ui_original_backup.py` - Backup antigo
- ✅ `code/entity.py` - MANTER! Usado por player.py e enemy.py

### 🗂️ **Logs e Arquivos Temporários**
- ❌ `code/logs/` - Pasta completa de logs antigos
- ❌ `code/create_sample_icons.py` - Script temporário, samples já criados
- ❌ `fix_png_profiles.py` - Script temporário, já executado

### 🗂️ **Arquivos de Configuração Desnecessários**
- ❌ `code/game_config.json` - Configuração não usada
- ❌ `install_ui_libs.sh` - Script temporário

### 🗂️ **Estrutura de Pastas Vazias/Não Utilizadas**
- ❌ `code/core/` - Nova arquitetura não utilizada
- ❌ `code/entities/` - Nova arquitetura não utilizada
- ❌ `code/levels/` - Pasta vazia
- ❌ `code/scenes/` - Nova arquitetura não utilizada
- ❌ `code/systems/` - Nova arquitetura não utilizada
- ❌ `code/ui_new/` - Nova arquitetura não utilizada
- ❌ `code/utils/` - Nova arquitetura não utilizada

### 🗂️ **Samples e Arquivos de Exemplo**
- ❌ `graphics/icon_samples/` - Samples criados, não necessários no projeto final
- ❌ `graphics/author.jpeg` - Arquivo pessoal não relacionado

### 🗂️ **Scripts Temporários**
- ❌ `run_options.sh` - Script temporário de teste

## ✅ **Arquivos Essenciais a Manter**

### 🎮 **Código Principal**
- ✅ `code/main.py` - Arquivo principal
- ✅ `code/main_with_modern_audio.py` - Versão com áudio moderno
- ✅ `code/level.py`, `code/level2.py`, `code/level3.py`, `code/level4.py` - Fases do jogo
- ✅ `code/player.py` - Lógica do jogador
- ✅ `code/enemy.py` - Lógica dos inimigos
- ✅ `code/weapon.py` - Sistema de armas
- ✅ `code/ui.py` - Interface do usuário
- ✅ `code/particles.py` - Sistema de partículas
- ✅ `code/collectables.py` - Itens coletáveis

### 🎵 **Sistemas Modernos**
- ✅ `code/audio_manager.py` - Sistema de áudio
- ✅ `code/modern_audio_controls.py` - Controles modernos
- ✅ `code/icon_manager.py` - Sistema de ícones
- ✅ `code/advanced_icons.py` - Ícones avançados
- ✅ `code/enhanced_font_system.py` - Sistema de fontes
- ✅ `code/font_manager.py` - Gerenciador de fontes

### 🎨 **Interface e Experiência**
- ✅ `code/main_menu.py` - Menu principal
- ✅ `code/ui_system.py` - Sistema de UI
- ✅ `code/tutorial_system.py` - Tutorial
- ✅ `code/graphics_manager.py` - Gerenciador gráfico
- ✅ `code/stats_screen.py` - Tela de estatísticas
- ✅ `code/achievements_screen.py` - Conquistas
- ✅ `code/save_manager.py` - Sistema de save

### 🎯 **Funcionalidades Específicas**
- ✅ `code/cheat_system.py` - Sistema de cheats
- ✅ `code/difficulty_manager.py` - Gerenciador de dificuldade
- ✅ `code/story_screen.py` - Telas de história
- ✅ `code/loading.py` - Tela de carregamento
- ✅ `code/professional_renderer.py` - Renderizador profissional

### 📁 **Assets Essenciais**
- ✅ `audio/` - Todos os arquivos de áudio
- ✅ `graphics/` - Gráficos necessários (exceto samples)
- ✅ `map new/` - Mapas das fases
- ✅ `docs/` - Documentação do projeto

### 📄 **Documentação**
- ✅ `README.md` - Documentação principal
- ✅ `CLAUDE.md` - Histórico de desenvolvimento
- ✅ `docs/` - Documentação técnica
- ✅ `rungame.sh` - Script principal de execução

## 🎯 **Resumo da Limpeza**

**Arquivos/Pastas para Remover:** ~50 items
**Espaço Estimado Liberado:** ~200MB (logs, samples, backups)
**Estrutura Final:** Código limpo, organizado e funcional

## 📋 **Próximos Passos**

1. ✅ Remover arquivos desnecessários
2. ✅ Limpar pastas vazias
3. ✅ Atualizar .gitignore
4. ✅ Commit das alterações
5. ✅ Sincronizar com GitHub