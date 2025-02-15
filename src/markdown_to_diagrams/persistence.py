"""Utility module for JSON data persistence operations

This module provides a client interface for handling JSON data persistence operations,
including saving and loading JSON files, managing research metadata, and handling
search results. It implements proper error handling and directory management.

Typical usage example:
    client = PersistenceClient()
    client.save_json({"key": "value"}, "data.json")
    data = client.load_json("data.json")
"""

import json
import os
from typing import Any, Dict, Optional, List
from .log_util import LogUtil

class PersistenceClient:
    """Client for handling JSON data persistence operations
    
    This class provides methods to save and load JSON data, manage research metadata,
    and handle search results. It includes proper error handling, directory creation,
    and path sanitization.
    
    Attributes:
        base_dir: The base directory for all file operations
        logger: Logger instance for tracking operations
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """Initialize the persistence client
        
        Args:
            base_dir: Optional base directory for storing files. If not provided,
                     uses the current working directory
        """
        self.base_dir = base_dir or os.getcwd()
        self.logger = LogUtil.get_logger()  # Initialize logger
        self.logger.info(f"Initialized PersistenceClient with base directory: {self.base_dir}")
        
    def save_json(self, data: Any, file_path: str) -> Dict[str, Any]:
        """Save data to a JSON file
        
        This method ensures the target directory exists before writing and handles
        any potential errors during the save operation.
        
        Args:
            data: The data to save (must be JSON serializable)
            file_path: Path to the file where data will be saved
            
        Returns:
            A dictionary indicating success or error
        """
        full_path = os.path.join(self.base_dir, file_path)
        self.logger.debug(f"Attempting to save JSON data to: {full_path}")
        
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            self.logger.debug(f"Ensured directory exists: {os.path.dirname(full_path)}")
            
            # Write data to file
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Successfully saved JSON data to: {file_path}")
            return {"success": True, "message": f"Data successfully saved to {file_path}"}
        except Exception as e:
            self.logger.error(f"Failed to save JSON data to {file_path}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    
    def load_json(self, file_path: str) -> Dict[str, Any]:
        """Load data from a JSON file
        
        This method attempts to read and parse a JSON file, handling any potential
        file access or JSON parsing errors.
        
        Args:
            file_path: Path to the file to load data from
            
        Returns:
            A dictionary containing the loaded data
            
        Raises:
            ValueError: If the file cannot be read or parsed
        """
        full_path = os.path.join(self.base_dir, file_path)
        self.logger.debug(f"Attempting to load JSON data from: {full_path}")
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.logger.info(f"Successfully loaded JSON data from: {file_path}")
                return data
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            raise ValueError(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON format in {file_path}: {str(e)}")
            raise ValueError(f"Invalid JSON format in {file_path}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Failed to load JSON data from {file_path}: {str(e)}")
            raise ValueError(f"Failed to load JSON data from {file_path}: {str(e)}")



    def load_file(self, file_path: str) -> str:
        """Load content from a file
        
        This method attempts to read a file and return its content as text,
        handling any potential file access errors.
        
        Args:
            file_path: Path to the file to load content from
            
        Returns:
            The content of the file as a string
            
        Raises:
            ValueError: If the file cannot be read
        """
        full_path = os.path.join(self.base_dir, file_path)
        self.logger.debug(f"Attempting to load file content from: {full_path}")
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.logger.info(f"Successfully loaded file content from: {file_path}")
                return content
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            raise ValueError(f"File not found: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to load file content from {file_path}: {str(e)}")
            raise ValueError(f"Failed to load file content from {file_path}: {str(e)}")

    def save_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Save content to a file
        
        This method ensures the target directory exists before writing and handles
        any potential errors during the save operation. It's useful for saving
        non-JSON content like text files or configuration files.
        
        Args:
            file_path: Path to the file where content will be saved
            content: The content to save to the file
            
        Returns:
            A dictionary indicating success or error
        """
        full_path = os.path.join(self.base_dir, file_path)
        self.logger.debug(f"Attempting to save content to: {full_path}")
        
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            self.logger.debug(f"Ensured directory exists: {os.path.dirname(full_path)}")
            
            # Write content to file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Successfully saved content to: {file_path}")
            return {"success": True, "message": f"Content successfully saved to {file_path}"}
        except Exception as e:
            self.logger.error(f"Failed to save content to {file_path}: {str(e)}")
            return {"success": False, "error": str(e)}

if __name__ == '__main__':
    # Example usage of PersistenceClient
    client = PersistenceClient()
    
    # Example data
    test_data = {
        "name": "Test User",
        "age": 30,
        "interests": ["programming", "reading"]
    }
    
    # Save data
    save_result = client.save_json(test_data, "test_data.json")
    print("Save result:", save_result)
    
    # Load data
    load_result = client.load_json("test_data.json")
    print("\nLoad result:", load_result)