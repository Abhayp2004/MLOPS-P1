import logging
import os
from datetime import datetime

# Create logs directory
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Create log file path
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Get root logger
root_logger = logging.getLogger()

# Check if file handler already exists
has_file_handler = any(
    isinstance(handler, logging.FileHandler) 
    for handler in root_logger.handlers
)

# Always ensure we have a file handler
if not has_file_handler:
    # Create file handler
    file_handler = logging.FileHandler(LOG_FILE, mode='a')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)
    
    # If no other handlers exist, also add console handler for visibility
    if len(root_logger.handlers) == 1:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

def get_logger(name: str):
    """Get a logger instance with the specified name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # Ensure logger propagates to root logger so it writes to file
    logger.propagate = True
    return logger