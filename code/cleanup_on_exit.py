import atexit
import os
import json
from player_stats import player_stats

def cleanup_name_on_exit():
    """Limpa o nome do jogador ao sair do jogo"""
    try:
        # Limpar nome do jogador para mostrar popup na próxima execução
        player_stats.stats["player_name"] = ""
        player_stats.save_stats()
        print("🧹 Nome do jogador limpo para próxima execução")
    except Exception as e:
        print(f"❌ Erro na limpeza: {e}")

# Registrar função para executar ao sair do programa
atexit.register(cleanup_name_on_exit)

print("🔄 Sistema de limpeza de nome registrado")