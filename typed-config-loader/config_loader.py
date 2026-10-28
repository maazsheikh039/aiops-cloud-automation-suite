from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator
import yaml
import json
import os


class DatabaseConfig(BaseModel):
    """Database connection configuration"""
    host: str = Field(default="localhost")
    port: int = Field(default=5432, ge=1, le=65535)
    username: str
    password: str
    database: str
    max_connections: int = Field(default=10, ge=1, le=100)
    
    @validator('host')
    def validate_host(cls, v):
        """Validate host is not empty and has a reasonable format."""
        if not v or not v.strip():
            raise ValueError("Database host cannot be empty.")
        return v.strip()


class CacheConfig(BaseModel):
    """Cache configuration"""
    enabled: bool = Field(default=True)
    ttl_seconds: int = Field(default=300, ge=0)
    max_size_mb: int = Field(default=100, ge=1)
    
    @validator('max_size_mb')
    def validate_max_size(cls, v):
        """Ensure cache max size does not exceed 1024 MB."""
        if v > 1024:
            raise ValueError("Cache max_size_mb cannot exceed 1024 MB.")
        return v


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = Field(default="INFO")
    format: str = Field(default="json")
    output_path: Optional[str] = Field(default="/var/log/app.log")
    
    @validator('level')
    def validate_log_level(cls, v):
        """Validate and normalize log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper_v = v.upper()
        if upper_v not in valid_levels:
            raise ValueError(f"Invalid log level '{v}'. Must be one of {valid_levels}")
        return upper_v


class AppConfig(BaseModel):
    """Main application configuration"""
    app_name: str
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    database: DatabaseConfig
    cache: CacheConfig = Field(default_factory=CacheConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    @validator('environment')
    def validate_environment(cls, v):
        """Validate environment string."""
        valid_envs = {"development", "staging", "production"}
        lower_v = v.lower()
        if lower_v not in valid_envs:
            raise ValueError(f"Invalid environment '{v}'. Must be one of {valid_envs}")
        return lower_v


class ConfigLoader:
    """Configuration loader with type validation"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config: Optional[AppConfig] = None
    
    def load(self) -> AppConfig:
        """Load and validate configuration from file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found at: {self.config_path}")
        
        ext = os.path.splitext(self.config_path)[1].lower()
        if ext in ['.json']:
            raw_data = self._load_json(self.config_path)
        elif ext in ['.yaml', '.yml']:
            raw_data = self._load_yaml(self.config_path)
        else:
            raise ValueError(f"Unsupported configuration file extension: {ext}")
            
        self.config = self.validate_config(raw_data)
        return self.config
    
    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """Load JSON configuration file."""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """Load YAML configuration file."""
        with open(file_path, 'r') as f:
            return yaml.safe_load(f) or {}
    
    def validate_config(self, config_dict: Dict[str, Any]) -> AppConfig:
        """Validate configuration dictionary against AppConfig schema."""
        try:
            return AppConfig(**config_dict)
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {e}")
    
    def get_config(self) -> AppConfig:
        """Return loaded configuration."""
        if self.config is None:
            raise RuntimeError("Configuration not loaded. Call load() first.")
        return self.config
    
    def reload(self) -> AppConfig:
        """Reload configuration from file."""
        return self.load()
