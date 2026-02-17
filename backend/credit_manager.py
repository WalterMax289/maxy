"""
Simple credit management without database
Uses in-memory storage with JSON file backup
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import hashlib

# In-memory storage
credits_data = {}
DATA_FILE = os.path.join(os.path.dirname(__file__), "credits_data.json")

def load_credits_data():
    """Load credits from JSON file"""
    global credits_data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                # Convert string dates back to datetime
                for user_id, user_data in data.items():
                    if 'last_reset' in user_data and user_data['last_reset']:
                        user_data['last_reset'] = datetime.fromisoformat(user_data['last_reset'])
                credits_data = data
        except:
            credits_data = {}

def save_credits_data():
    """Save credits to JSON file"""
    try:
        # Convert datetime to string for JSON serialization
        data_to_save = {}
        for user_id, user_data in credits_data.items():
            data_copy = user_data.copy()
            if 'last_reset' in data_copy and data_copy['last_reset']:
                if isinstance(data_copy['last_reset'], datetime):
                    data_copy['last_reset'] = data_copy['last_reset'].isoformat()
            data_to_save[user_id] = data_copy
        
        with open(DATA_FILE, 'w') as f:
            json.dump(data_to_save, f)
    except Exception as e:
        print(f"Warning: Could not save credits data: {e}")

def get_user_id_from_request(request) -> str:
    """Extract or create user ID from request"""
    # Try to get from header first (for authenticated users)
    user_id = request.headers.get("X-User-ID")
    
    if not user_id:
        # Try to get from query params
        user_id = request.query_params.get("user_id")
    
    if not user_id:
        # Generate a new ID based on IP + User-Agent (for anonymous tracking)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        # Create a hash of IP + User-Agent
        user_hash = hashlib.md5(f"{client_ip}:{user_agent}".encode()).hexdigest()[:16]
        user_id = f"anon_{user_hash}"
    
    return user_id

class CreditManager:
    """Manages user credits using in-memory storage"""
    
    def __init__(self):
        from config import config
        self.config = config
        load_credits_data()
    
    def get_or_create_user(self, user_id: str) -> Dict[str, Any]:
        """Get existing user or create new one"""
        from config import config
        
        if user_id not in credits_data:
            credits_data[user_id] = {
                "user_id": user_id,
                "credits_remaining": config.MAX_CREDITS_PER_USER,
                "last_reset": datetime.utcnow(),
                "total_messages_sent": 0,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            save_credits_data()
        
        user = credits_data[user_id]
        
        # Check if credits should be refreshed
        if self.should_refresh(user):
            self.refresh_credits(user)
            save_credits_data()
        
        return user
    
    def should_refresh(self, user: Dict) -> bool:
        """Check if credits should be refreshed"""
        from config import config
        
        if user["credits_remaining"] < config.MAX_CREDITS_PER_USER:
            last_reset = user["last_reset"]
            if isinstance(last_reset, str):
                last_reset = datetime.fromisoformat(last_reset)
            next_refresh = last_reset + timedelta(hours=config.CREDIT_REFRESH_HOURS)
            return datetime.utcnow() >= next_refresh
        return False
    
    def refresh_credits(self, user: Dict):
        """Reset credits to max"""
        from config import config
        user["credits_remaining"] = config.MAX_CREDITS_PER_USER
        user["last_reset"] = datetime.utcnow()
        user["updated_at"] = datetime.utcnow()
    
    def use_credit(self, user_id: str) -> tuple[bool, Dict[str, Any]]:
        """Use one credit. Returns (success, user_data)"""
        from config import config
        
        user = self.get_or_create_user(user_id)
        
        # Check if we should refresh first
        if self.should_refresh(user):
            self.refresh_credits(user)
        
        if user["credits_remaining"] > 0:
            user["credits_remaining"] -= 1
            user["total_messages_sent"] += 1
            user["updated_at"] = datetime.utcnow()
            save_credits_data()
            
            return True, self._format_user_data(user)
        else:
            return False, self._format_user_data(user)
    
    def get_user_credits(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user credit information"""
        if user_id not in credits_data:
            user = self.get_or_create_user(user_id)
        else:
            user = credits_data[user_id]
            # Check for refresh
            if self.should_refresh(user):
                self.refresh_credits(user)
                save_credits_data()
        
        return self._format_user_data(user)
    
    def _format_user_data(self, user: Dict) -> Dict[str, Any]:
        """Format user data for response"""
        from config import config
        
        last_reset = user["last_reset"]
        if isinstance(last_reset, str):
            last_reset = datetime.fromisoformat(last_reset)
        
        next_refresh = None
        if user["credits_remaining"] == 0:
            next_refresh = (last_reset + timedelta(hours=config.CREDIT_REFRESH_HOURS)).isoformat()
        
        return {
            "user_id": user["user_id"],
            "credits_remaining": user["credits_remaining"],
            "max_credits": config.MAX_CREDITS_PER_USER,
            "refresh_hours": config.CREDIT_REFRESH_HOURS,
            "last_reset": last_reset.isoformat() if isinstance(last_reset, datetime) else last_reset,
            "next_refresh": next_refresh,
            "total_messages_sent": user["total_messages_sent"]
        }
    
    def get_all_users(self) -> list:
        """Get all users (for admin)"""
        return [self._format_user_data(user) for user in credits_data.values()]


# Global credit manager instance
credit_manager = CreditManager()
