"""
Logging utility for the game
"""

import logging
import os
import datetime

class GameLogger:
    """
    Game logging utility to write debug and error messages to console and file
    """
    def __init__(self, log_level=logging.DEBUG, log_to_file=True):
        self.logger = logging.getLogger('game_logger')
        self.logger.setLevel(log_level)
        self.logger.propagate = False  # Don't propagate to parent loggers
        
        # Create formatter for log messages
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Create file handler if requested
        if log_to_file:
            # Create logs directory if it doesn't exist
            log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            # Create log file with timestamp
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            log_file = os.path.join(log_dir, f'game_{timestamp}.log')
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message):
        """Log a debug message"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log an info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log a warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log an error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log a critical message"""
        self.logger.critical(message)

# Create a global logger instance
logger = GameLogger()

def get_logger():
    """Get the global logger instance"""
    return logger

# Example usage
if __name__ == "__main__":
    logger.info("Logger test")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
