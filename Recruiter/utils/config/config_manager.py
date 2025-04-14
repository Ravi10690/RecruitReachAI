"""
Configuration manager for RecruitReach2.

This module provides utilities for loading and accessing configuration
settings from TOML files.
"""

import os
import tomllib
from pathlib import Path
from typing import Dict, Any, Optional, Union
from Recruiter.models.schemas import AppConfig, EmailConfig, APIConfig
from Recruiter.utils.file_utils.path_manager import PathManager

class ConfigManager:
    """
    Manages application configuration from TOML files.
    
    This class provides methods for loading configuration from TOML files,
    accessing configuration values, and validating configuration settings.
    """
    
    def __init__(self):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the TOML configuration file.
                If not provided, defaults to 'config/config.toml' relative to the project root.
        """
        # Get the project root directory (parent of utils)
        paths = PathManager()
        self.config_path = str(paths.get_config_path())
        self._config_data: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """
        Load and parse the TOML configuration file.
        
        Raises:
            FileNotFoundError: If the configuration file is not found.
            ValueError: If there is an error parsing the TOML file.
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'rb') as f:
                    self._config_data = tomllib.load(f)
            else:
                self._config_data = {}
                
        except FileNotFoundError:
            # Don't raise an error, just use empty config
            self._config_data = {}
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"Error parsing TOML file: {str(e)}")
    
    def get_value(self, section: str, key: str) -> Any:
        """
        Get a value from the configuration.
        
        Args:
            section: The section name in the TOML file (e.g., 'openai', 'email')
            key: The key name within the section
            
        Returns:
            The value associated with the key in the specified section,
            or None if the section or key doesn't exist.
        """
        return self._config_data.get(section, {}).get(key)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get all key-value pairs from a section.
        
        Args:
            section: The section name in the TOML file
            
        Returns:
            Dictionary containing all key-value pairs in the section,
            or an empty dictionary if the section doesn't exist.
        """
        return dict(self._config_data.get(section, {}))
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get the entire configuration as a dictionary.
        
        Returns:
            Dictionary containing all configuration data.
        """
        return dict(self._config_data)
    
    def get_app_config(self) -> AppConfig:
        """
        Get the application configuration as a validated AppConfig object.
        
        Returns:
            AppConfig object containing the application configuration.
        """
        email_config = None
        api_config = None
        
        # Get email configuration if available
        email_section = self.get_section('email')
        if email_section:
            try:
                email_config = EmailConfig(**email_section)
            except Exception:
                # If validation fails, leave as None
                pass
        
        # Get API configuration if available
        api_section = self.get_section('openai')
        if api_section:
            try:
                api_config = APIConfig(openai_api_key=api_section.get('OPENAI_API_KEY', ''))
            except Exception:
                # If validation fails, leave as None
                pass
        
        return AppConfig(email=email_config, api=api_config)
