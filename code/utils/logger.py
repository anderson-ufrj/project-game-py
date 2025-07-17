"""
Sistema de logging para o jogo
"""
import logging
import os
import sys
from datetime import datetime
from typing import Optional


class GameLogger:
    """
    Logger customizado para o jogo.
    """
    
    def __init__(self, name: str = "game", log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Evita duplicação de handlers
        if not self.logger.handlers:
            self._setup_handlers(log_file)
    
    def _setup_handlers(self, log_file: Optional[str] = None) -> None:
        """
        Configura handlers de logging.
        
        Args:
            log_file (Optional[str]): Arquivo de log
        """
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            try:
                # Cria diretório se não existir
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                print(f"Erro ao criar arquivo de log: {e}")
    
    def debug(self, message: str) -> None:
        """Log de debug."""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log de informação."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log de aviso."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log de erro."""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log crítico."""
        self.logger.critical(message)
    
    def exception(self, message: str) -> None:
        """Log de exceção com traceback."""
        self.logger.exception(message)


# Instância global do logger
game_logger = GameLogger(
    name="corrida_reliquia",
    log_file=f"logs/game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)

# Aliases para facilitar uso
debug = game_logger.debug
info = game_logger.info
warning = game_logger.warning
error = game_logger.error
critical = game_logger.critical
exception = game_logger.exception