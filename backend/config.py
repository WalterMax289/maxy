"""
Configuration management for MAXY Chat Backend
Handles all environment variables and application settings
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
    
    # CORS Configuration - Allow all localhost origins for development
    ALLOWED_ORIGINS_STR = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000,http://127.0.0.1:3000,http://localhost:5500,http://127.0.0.1:5500,http://localhost:*,null")
    ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_STR.split(",") if origin.strip()]
    # Also add wildcard for file:// protocol (when opening HTML directly)
    if "*" not in ALLOWED_ORIGINS:
        ALLOWED_ORIGINS.append("*")
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
    
    # File Processing Configuration
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB default
    ENABLE_FILE_PROCESSING = os.getenv("ENABLE_FILE_PROCESSING", "True").lower() == "true"
    ENABLE_CHARTS = os.getenv("ENABLE_CHARTS", "True").lower() == "true"
    ENABLE_WIKIPEDIA = os.getenv("ENABLE_WIKIPEDIA", "True").lower() == "true"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 100))  # requests
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 60))  # seconds
    
    # Credit System Configuration
    ENABLE_CREDITS = os.getenv("ENABLE_CREDITS", "True").lower() == "true"
    MAX_CREDITS_PER_USER = int(os.getenv("MAX_CREDITS_PER_USER", 30))  # messages
    CREDIT_REFRESH_HOURS = int(os.getenv("CREDIT_REFRESH_HOURS", 3))  # hours
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./maxy_chat.db")
    DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", 10))
    DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", 20))
    
    # API Configuration
    API_TITLE = "MAXY Chat Backend"
    API_VERSION = "2.0.0"
    API_DESCRIPTION = "Advanced multi-model AI chatbot with conversation management, data analysis, and file processing"
    
    # AI Model Configuration
    THINKING_ENABLED = os.getenv("THINKING_ENABLED", "True").lower() == "true"
    SHOW_CONFIDENCE_SCORES = os.getenv("SHOW_CONFIDENCE_SCORES", "True").lower() == "true"
    MAX_CONVERSATION_HISTORY = int(os.getenv("MAX_CONVERSATION_HISTORY", 50))
    
    # Feature Flags
    ENABLE_ANALYTICS = os.getenv("ENABLE_ANALYTICS", "True").lower() == "true"
    ENABLE_FEEDBACK = os.getenv("ENABLE_FEEDBACK", "True").lower() == "true"
    ENABLE_EXPORT = os.getenv("ENABLE_EXPORT", "True").lower() == "true"
    
    # Cache Configuration
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # 1 hour
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "True").lower() == "true"
    
    @classmethod
    def validate_config(cls) -> tuple[bool, str]:
        """Validate configuration settings"""
        try:
            # Create logs directory if it doesn't exist
            log_dir = os.path.dirname(cls.LOG_FILE)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            # Validate file size
            if cls.MAX_FILE_SIZE < 1024 * 1024:  # Less than 1MB
                return False, "MAX_FILE_SIZE must be at least 1MB"
            
            # Validate rate limiting
            if cls.RATE_LIMIT_REQUESTS < 1:
                return False, "RATE_LIMIT_REQUESTS must be at least 1"
            
            if cls.RATE_LIMIT_WINDOW < 1:
                return False, "RATE_LIMIT_WINDOW must be at least 1 second"
            
            # Validate history size
            if cls.MAX_CONVERSATION_HISTORY < 1:
                return False, "MAX_CONVERSATION_HISTORY must be at least 1"
            
            # Validate credit settings
            if cls.MAX_CREDITS_PER_USER < 1:
                return False, "MAX_CREDITS_PER_USER must be at least 1"
            
            if cls.CREDIT_REFRESH_HOURS < 1:
                return False, "CREDIT_REFRESH_HOURS must be at least 1"
            
            # Validate CORS origins in production
            if not cls.DEBUG and ("*" in cls.ALLOWED_ORIGINS or not cls.ALLOWED_ORIGINS):
                return False, "CORS origins must be explicitly set in production (not *)"
            
            # Validate secret key in production
            if not cls.DEBUG and cls.SECRET_KEY == "your-super-secret-key-change-this-in-production":
                return False, "SECRET_KEY must be changed from default in production"
            
            return True, "Configuration valid"
            
        except Exception as e:
            return False, f"Configuration validation error: {str(e)}"


# Create config instance
config = Config()

# Validate on import
is_valid, validation_msg = config.validate_config()
if not is_valid:
    print(f"WARNING: {validation_msg}")
