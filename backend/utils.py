"""
Utility functions and helpers
"""

import hashlib
import json
import logging
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from functools import wraps
import time

logger = logging.getLogger(__name__)


class CacheManager:
    """Simple caching mechanism"""
    
    def __init__(self, ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        if key not in self.cache:
            return None
        
        cache_entry = self.cache[key]
        if datetime.now().timestamp() - cache_entry['timestamp'] > self.ttl:
            del self.cache[key]
            return None
        
        return cache_entry['value']
    
    def set(self, key: str, value: Any):
        """Set cache value"""
        self.cache[key] = {
            'value': value,
            'timestamp': datetime.now().timestamp()
        }
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
    
    def delete(self, key: str):
        """Delete specific cache entry"""
        if key in self.cache:
            del self.cache[key]


def cache_result(ttl: int = 3600):
    """Decorator for caching function results"""
    cache = CacheManager(ttl)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}_{hashlib.md5(str((args, kwargs)).encode()).hexdigest()}"
            
            # Check cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            logger.debug(f"Cached result for {func.__name__}")
            
            return result
        
        return wrapper
    return decorator


def measure_time(func: Callable) -> Callable:
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        logger.debug(f"{func.__name__} executed in {execution_time:.3f}s")
        return result
    return wrapper


class DataValidator:
    """Validate various data types"""
    
    @staticmethod
    def validate_numerical_data(data: List[Any]) -> tuple[bool, str]:
        """Validate numerical data"""
        if not isinstance(data, list):
            return False, "Data must be a list"
        
        if len(data) == 0:
            return False, "Data list cannot be empty"
        
        if len(data) > 100000:
            return False, "Data list is too large (max 100000 items)"
        
        for item in data:
            try:
                float(item)
            except (ValueError, TypeError):
                return False, f"Invalid numerical value: {item}"
        
        return True, "Data is valid"
    
    @staticmethod
    def validate_string_data(data: str, max_length: int = 10000) -> tuple[bool, str]:
        """Validate string data"""
        if not isinstance(data, str):
            return False, "Data must be a string"
        
        if len(data) == 0:
            return False, "String cannot be empty"
        
        if len(data) > max_length:
            return False, f"String exceeds maximum length of {max_length}"
        
        return True, "String is valid"
    
    @staticmethod
    def validate_json(data: str) -> tuple[bool, Any]:
        """Validate and parse JSON"""
        try:
            parsed = json.loads(data)
            return True, parsed
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"


class TextProcessor:
    """Text processing utilities"""
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text to maximum length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def extract_keywords(text: str, top_n: int = 5) -> List[str]:
        """Extract keywords from text"""
        import re
        
        # Remove special characters and convert to lowercase
        text = re.sub(r'[^a-z0-9\s]', '', text.lower())
        
        # Split into words
        words = text.split()
        
        # Filter common words
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can'
        }
        
        filtered_words = [w for w in words if w not in common_words and len(w) > 2]
        
        # Count occurrences
        from collections import Counter
        word_counts = Counter(filtered_words)
        
        # Return top N
        return [word for word, _ in word_counts.most_common(top_n)]
    
    @staticmethod
    def sentiment_score(text: str) -> float:
        """Simple sentiment scoring (-1 to 1)"""
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'best'}
        negative_words = {'bad', 'terrible', 'awful', 'hate', 'worst', 'horrible'}
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        
        return (positive_count - negative_count) / total


class FormatUtil:
    """Formatting utilities"""
    
    @staticmethod
    def format_number(num: float, decimals: int = 2) -> str:
        """Format number with specified decimals"""
        return f"{num:.{decimals}f}"
    
    @staticmethod
    def format_percentage(num: float, decimals: int = 1) -> str:
        """Format as percentage"""
        return f"{num * 100:.{decimals}f}%"
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format bytes as human-readable size"""
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = float(size_bytes)
        
        for unit in units[:-1]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        
        return f"{size:.1f} {units[-1]}"
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format seconds as human-readable duration"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    @staticmethod
    def format_timestamp(dt: datetime = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format datetime"""
        if dt is None:
            dt = datetime.now()
        return dt.strftime(fmt)


class ListUtil:
    """List utilities"""
    
    @staticmethod
    def batch(items: List[Any], batch_size: int) -> List[List[Any]]:
        """Split list into batches"""
        return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
    
    @staticmethod
    def flatten(nested_list: List[List[Any]]) -> List[Any]:
        """Flatten nested list"""
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(ListUtil.flatten(item))
            else:
                result.append(item)
        return result
    
    @staticmethod
    def deduplicate(items: List[Any], preserve_order: bool = True) -> List[Any]:
        """Remove duplicates from list"""
        if preserve_order:
            seen = set()
            result = []
            for item in items:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            return result
        else:
            return list(set(items))


class ResponseBuilder:
    """Build structured responses"""
    
    @staticmethod
    def success(data: Any, message: str = "Success") -> Dict[str, Any]:
        """Build success response"""
        return {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def error(error_code: str, message: str, details: Dict = None) -> Dict[str, Any]:
        """Build error response"""
        return {
            "success": False,
            "error": error_code,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def paginated(items: List[Any], page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Build paginated response"""
        total = len(items)
        total_pages = (total + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = start + page_size
        
        return {
            "items": items[start:end],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": total_pages
            }
        }


class Logger:
    """Enhanced logging utilities"""
    
    @staticmethod
    def info(message: str, **kwargs):
        """Log info message"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs)}"
        logger.info(message)
    
    @staticmethod
    def error(message: str, exc: Exception = None, **kwargs):
        """Log error message"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs)}"
        logger.error(message, exc_info=exc)
    
    @staticmethod
    def debug(message: str, **kwargs):
        """Log debug message"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs)}"
        logger.debug(message)
    
    @staticmethod
    def warning(message: str, **kwargs):
        """Log warning message"""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs)}"
        logger.warning(message)
