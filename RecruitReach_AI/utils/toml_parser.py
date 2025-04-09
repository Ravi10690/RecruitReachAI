import tomli
from pathlib import Path
from typing import Dict, Any, Optional
from RecruitReach_AI.config.file_paths import TOML_PATH

class TomlParser:
    """A utility class for parsing TOML configuration files."""
    
    def __init__(self, config_path: Optional[str] = TOML_PATH):
        """
        Initialize the TOML parser.
        
        Args:
            config_path (str, optional): Path to the TOML config file.
                If not provided, defaults to '../config/config.toml'
        """
        if config_path is None:
            # Get the directory of the current file
            current_dir = Path(__file__).parent
            # Construct path to config.toml relative to current file
            config_path = str(current_dir.parent / 'config' / 'config.toml')
            
        self.config_path = config_path
        self._config_data: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load and parse the TOML configuration file."""
        try:
            with open(self.config_path, 'rb') as f:
                self._config_data = tomli.load(f)
                
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at: {self.config_path}")
        except tomli.TOMLDecodeError as e:
            raise ValueError(f"Error parsing TOML file: {str(e)}")

    def get_value(self, section: str, key: str) -> Any:
        """
        Get a value from the configuration.
        
        Args:
            section (str): The section name in the TOML file (e.g., 'openai', 'email')
            key (str): The key name within the section
            
        Returns:
            Any: The value associated with the key in the specified section
            
        Raises:
            KeyError: If the section or key doesn't exist
        """
        try:
            return self._config_data.get(section, {}).get(key)
        except KeyError:
            raise KeyError(f"Config value not found for section '{section}' and key '{key}'")

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get all key-value pairs from a section.
        
        Args:
            section (str): The section name in the TOML file
            
        Returns:
            Dict[str, Any]: Dictionary containing all key-value pairs in the section
            
        Raises:
            KeyError: If the section doesn't exist
        """
        try:
            return dict(self._config_data.get(section, {}))
        except KeyError:
            raise KeyError(f"Section '{section}' not found in config")

    def get_all(self) -> Dict[str, Any]:
        """
        Get the entire configuration as a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary containing all configuration data
        """
        return dict(self._config_data)


if __name__ == "__main__":
    # Example usage
    parser = TomlParser()