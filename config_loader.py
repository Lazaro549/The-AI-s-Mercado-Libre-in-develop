"""Configuration loader for the AI Mercado Libre Optimizer.

This module handles loading and managing configuration from config.yaml file.
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file.
    
    Args:
        config_path (str): Path to the configuration file. Defaults to "config.yaml".
        
    Returns:
        Dict[str, Any]: Configuration dictionary.
        
    Raises:
        FileNotFoundError: If config file doesn't exist.
        yaml.YAMLError: If YAML parsing fails.
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        logger.warning(f"Config file not found at {config_path}, using defaults")
        return get_default_config()
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise


def get_default_config() -> Dict[str, Any]:
    """Get default configuration when config file is not available.
    
    Returns:
        Dict[str, Any]: Default configuration dictionary.
    """
    return {
        "metrics": {
            "ctr": {"low": 0.02, "good": 0.03, "excellent": 0.05},
            "conversion_rate": {"low": 0.02, "good": 0.03, "excellent": 0.05},
            "acos": {"critical": 0.40, "high": 0.30, "good": 0.20}
        },
        "scoring": {
            "ctr_max_points": 30,
            "conversion_max_points": 40,
            "acos_max_points": 30,
            "scale_threshold": 70,
            "optimize_threshold": 40
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }


# Global config instance
_config = None


def get_config() -> Dict[str, Any]:
    """Get the global configuration instance.
    
    Returns:
        Dict[str, Any]: Configuration dictionary.
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config


def reset_config():
    """Reset the global configuration instance."""
    global _config
    _config = None
