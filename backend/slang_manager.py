import random
import os
import re

class SlangManager:
    """Manages Bangalore slangs from a text file"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SlangManager, cls).__new__(cls)
            cls._instance.slangs = []
            cls._instance.enabled = False  # Default to False as requested
            cls._instance.load_slangs()
        return cls._instance
    
    def load_slangs(self):
        """Load slangs from the text file"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), 'Bangalore_Authentic_400_Slangs.txt')
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line in lines:
                line = line.strip()
                if not line or line.startswith('='):
                    continue
                    
                # Format: "1. Maga – Bro / Dude"
                # Handle different dash types
                if '–' in line:
                    parts = line.split('–')
                else:
                    parts = line.split('-')
                    
                if len(parts) >= 1:
                    # Extract the slang part (remove number and dot)
                    raw_slang = parts[0].strip()
                    # Remove "1. " prefix
                    slang = re.sub(r'^\d+\.\s*', '', raw_slang)
                    if slang and len(slang) < 30: # Avoid capturing long sentences mistakenly
                        self.slangs.append(slang)
            
            print(f"Loaded {len(self.slangs)} slangs.")
        except Exception as e:
            print(f"Error loading slangs: {e}")
            # Fallback slangs if file read fails
            self.slangs = ["Maga", "Machaa", "Guru", "Boss", "Sakkath"]

    def set_enabled(self, enabled: bool):
        """Enable or disable slang injection"""
        self.enabled = enabled
        status = "enabled" if enabled else "disabled"
        print(f"SlangManager {status}")
        return f"Slangs have been {status}."

    def get_random_slang(self):
        """Get a random slang word"""
        if not self.enabled:
            return "friend"
            
        if not self.slangs:
            return "Maga"
        return random.choice(self.slangs)

    def enhance_text(self, text, model_name="MAXY"):
        """Randomly inject slang into text"""
        if not self.enabled:
            return text
            
        # 30% chance to start with a slang
        if random.random() < 0.3:
            slang = self.get_random_slang()
            text = f"{slang}, {text}"
            
        # 30% chance to end with a slang
        elif random.random() < 0.3:
            slang = self.get_random_slang()
            if text.endswith('.'):
                text = text[:-1]
            text = f"{text}, {slang}."
            
        return text

    def get_greeting(self):
        """Get a slang-infused greeting"""
        if not self.enabled:
            return random.choice([
                "Hello, what's up?",
                "Namaste!",
                "Hey there, how are you?",
                "Hello, welcome!",
                "Hi, let's chat."
            ])
            
        slang = self.get_random_slang()
        greetings = [
            f"Yen {slang}, what's up?",
            f"Namaskara {slang}!",
            f"Hey {slang}, hegidira?",
            f"Lo {slang}, welcome!",
            f"Banni {slang}, let's chat."
        ]
        return random.choice(greetings)
