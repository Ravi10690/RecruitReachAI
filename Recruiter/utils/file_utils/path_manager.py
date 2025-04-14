"""
Path manager for RecruitReach2.

This module provides utilities for managing file paths in the application.
"""

import os
from pathlib import Path
from typing import Optional


class PathManager:
    """
    Manages file paths for the application.
    
    This class provides methods for getting paths to various files and directories
    used by the application.
    """
    
    def __init__(self):
        """Initialize the path manager."""
        # Get the project root directory
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        
        # Define common paths
        self.config_dir =   os.path.join(self.root_dir , 'config')
        self.data_dir = os.path.join(self.root_dir , 'data')
        self.templates_dir = os.path.join(self.root_dir , 'app' , 'web' , 'templates')
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Ensure that required directories exist."""
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)
    
    def get_config_path(self, filename: str = 'config.toml') -> str:
        """
        Get the path to a configuration file.
        
        Args:
            filename: Name of the configuration file.
            
        Returns:
            Path to the configuration file.
        """
        return os.path.join(self.config_dir, filename)
    
    def get_data_path(self, filename: Optional[str] = None) -> Path:
        """
        Get the path to a data file or directory.
        
        Args:
            filename: Name of the data file, or None to get the data directory.
            
        Returns:
            Path to the data file or directory.
        """
        if filename:
            return os.path.join(self.data_dir, filename)
        return self.data_dir
    
    def get_resume_path(self, filename: str = 'resume.pdf') -> Path:
        """
        Get the path to a resume file.
        
        Args:
            filename: Name of the resume file.
            
        Returns:
            Path to the resume file.
        """
        return os.path.join(self.data_dir, filename)
    
    def get_template_path(self, filename: str) -> Path:
        """
        Get the path to a template file.
        
        Args:
            filename: Name of the template file.
            
        Returns:
            Path to the template file.
        """
        return os.path.join(self.templates_dir, filename)
