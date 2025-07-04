"""
Configuration management for gdl package.
Handles loading configuration from files, environment variables, and defaults.
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Configuration manager for gdl."""
    
    # Default configuration values
    DEFAULT_CONFIG = {
        "output_dir": "./downloads",
        "chunk_size": 8192,
        "max_retries": 3,
        "retry_delay": 1.0,
        "timeout": 30,
        "verify_ssl": True,
        "auto_create_dirs": True,
        "log_level": "INFO"
    }
    
    # Environment variable prefixes
    ENV_PREFIX = "GDL_"
    
    def __init__(self, config_file: Optional[str] = None, **kwargs):
        """
        Initialize configuration with defaults, file, environment, and overrides.
        
        Args:
            config_file: Optional path to configuration file
            **kwargs: Configuration overrides
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        # Load from config file if provided or found
        config_path = config_file or self._find_config_file()
        if config_path and os.path.exists(config_path):
            self._load_config_file(config_path)
        
        # Override with environment variables
        self._load_env_vars()
        
        # Override with provided kwargs
        self.config.update(kwargs)
    
    def _find_config_file(self) -> Optional[str]:
        """Find configuration file in standard locations."""
        possible_paths = [
            "gdl_config.json",
            os.path.expanduser("~/.gdl/config.json"),
            os.path.expanduser("~/.config/gdl/config.json")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    def _load_config_file(self, config_path: str):
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                self.config.update(file_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config file {config_path}: {e}")
    
    def _load_env_vars(self):
        """Load configuration from environment variables."""
        for key in self.DEFAULT_CONFIG:
            env_key = f"{self.ENV_PREFIX}{key.upper()}"
            env_value = os.getenv(env_key)
            
            if env_value is not None:
                # Convert string values to appropriate types
                if key in ["chunk_size", "max_retries", "timeout"]:
                    try:
                        self.config[key] = int(env_value)
                    except ValueError:
                        print(f"Warning: Invalid integer value for {env_key}: {env_value}")
                elif key in ["retry_delay"]:
                    try:
                        self.config[key] = float(env_value)
                    except ValueError:
                        print(f"Warning: Invalid float value for {env_key}: {env_value}")
                elif key in ["verify_ssl", "auto_create_dirs"]:
                    self.config[key] = env_value.lower() in ('true', '1', 'yes', 'on')
                else:
                    self.config[key] = env_value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.config[key] = value
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values."""
        self.config.update(updates)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self.config.copy()
    
    def save(self, config_path: str):
        """Save current configuration to file."""
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
