import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

def setup_logging(log_level: str = "INFO", log_dir: str = "logs") -> None:
    """
    Setup comprehensive logging configuration with file and console handlers
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Console handler (INFO level and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)
    
    # File handlers with rotation
    today = datetime.now().strftime("%Y-%m-%d")
    
    # General application log
    app_log_file = log_path / f"app_{today}.log"
    app_handler = logging.handlers.RotatingFileHandler(
        app_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    app_handler.setLevel(logging.DEBUG)
    app_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(app_handler)
    
    # Error log (ERROR level and above)
    error_log_file = log_path / f"errors_{today}.log"
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_handler)
    
    # Database operations log
    db_log_file = log_path / f"database_{today}.log"
    db_handler = logging.handlers.RotatingFileHandler(
        db_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )
    db_handler.setLevel(logging.DEBUG)
    db_handler.setFormatter(detailed_formatter)
    
    # Create database logger
    db_logger = logging.getLogger("database")
    db_logger.addHandler(db_handler)
    db_logger.setLevel(logging.DEBUG)
    
    # API requests log
    api_log_file = log_path / f"api_{today}.log"
    api_handler = logging.handlers.RotatingFileHandler(
        api_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    api_handler.setLevel(logging.INFO)
    api_handler.setFormatter(detailed_formatter)
    
    # Create API logger
    api_logger = logging.getLogger("api")
    api_logger.addHandler(api_handler)
    api_logger.setLevel(logging.INFO)
    
    # Vector service log
    vector_log_file = log_path / f"vector_{today}.log"
    vector_handler = logging.handlers.RotatingFileHandler(
        vector_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )
    vector_handler.setLevel(logging.DEBUG)
    vector_handler.setFormatter(detailed_formatter)
    
    # Create vector service logger
    vector_logger = logging.getLogger("vector_service")
    vector_logger.addHandler(vector_handler)
    vector_logger.setLevel(logging.DEBUG)
    
    # Document processing log
    doc_log_file = log_path / f"document_processing_{today}.log"
    doc_handler = logging.handlers.RotatingFileHandler(
        doc_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )
    doc_handler.setLevel(logging.DEBUG)
    doc_handler.setFormatter(detailed_formatter)
    
    # Create document processing logger
    doc_logger = logging.getLogger("document_processor")
    doc_logger.addHandler(doc_handler)
    doc_logger.setLevel(logging.DEBUG)
    
    # RAG service log
    rag_log_file = log_path / f"rag_{today}.log"
    rag_handler = logging.handlers.RotatingFileHandler(
        rag_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )
    rag_handler.setLevel(logging.DEBUG)
    rag_handler.setFormatter(detailed_formatter)
    
    # Create RAG service logger
    rag_logger = logging.getLogger("rag_service")
    rag_logger.addHandler(rag_handler)
    rag_logger.setLevel(logging.DEBUG)
    
    # Log startup message
    logging.info(f"Logging system initialized. Log files will be stored in: {log_path.absolute()}")
    logging.info(f"Log level set to: {log_level.upper()}")

    # Always add file handler to ensure log file is created
    root_logger.addHandler(error_handler)
    # Only add console handler if not present
    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        root_logger.addHandler(console_handler)

    # Test log to verify file creation
    root_logger.debug("[LOGGING] errors.log file handler initialized and ready.")

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

def log_system_info() -> None:
    """Log system information for debugging"""
    import platform
    import sys
    
    logger = logging.getLogger("system")
    
    logger.info("=" * 60)
    logger.info("SYSTEM INFORMATION")
    logger.info("=" * 60)
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Architecture: {platform.architecture()}")
    logger.info(f"Machine: {platform.machine()}")
    logger.info(f"Processor: {platform.processor()}")
    logger.info(f"Node: {platform.node()}")
    logger.info("=" * 60)

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, 'backend_debug.log')

# Set up root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Console handler (INFO and above)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# File handler (DEBUG and above)
file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Always add file handler to ensure log file is created
logger.addHandler(file_handler)
# Only add console handler if not present
if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
    logger.addHandler(console_handler)

# Test log to verify file creation
logger.debug("[LOGGING] backend_debug.log file handler initialized and ready.") 