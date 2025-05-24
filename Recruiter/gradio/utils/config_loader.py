"""Configuration loading utilities."""

from typing import Dict
from Recruiter.utils.config.config_manager import ConfigManager

def get_config_values() -> Dict[str, str]:
    """
    Get configuration values from config.toml.
    
    Returns:
        Dictionary containing configuration values.
    """
    try:
        config_manager = ConfigManager()
        app_config = config_manager.get_app_config()
        
        return {
            'openai_api_key': app_config.api.openai_api_key if app_config.api else '',
            'sender_email': app_config.email.sender_email if app_config.email else '',
            'sender_name': app_config.email.sender_name if app_config.email else '',
            'app_password': app_config.email.app_password if app_config.email else ''
        }
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        return {
            'openai_api_key': '',
            'sender_email': '',
            'sender_name': '',
            'app_password': ''
        }
