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

    def detect_slang(self, text):
        """Detect if the input text contains slang triggers (Kannada, Hindi, Tamil, Telugu, etc.)"""
        if not text:
            return False
            
        triggers = [
            # Kannada / Bangalore
            "macha", "maga", "guru", "boss", "thika", "sisya", 
            "da", "kane", "kano", "le", "lo", "aliyas", "dove",
            "mama", "machan", "mass", "scene", "sakath", "tumba", 
            "swalpa", "adjust", "beda", "beku", "super", "ayyo", 
            "chindi", "bindaas", "figure", "loose", "item", "jugaad", 
            "ghanta", "pakao", "mast", "kaand", "faltu", "timepass", 
            "jhol", "funda", "bakwaas", "senti", "patli", "jhakas",
            "bro", "dude", "buddy", "maadi", "kelsa", "hogona", "banni",
            "yen", "helu", "samachara", "yelli", "hogu",
            
            # Hindi
            "kya", "haal", "bhai", "yaar", "dost", "kaise", "bol", "mast", "jhakaas",
            "bindaas", "paisa", "waat", "kalti", "khopdi", "bheja", "dhassu",
            
            # Tamil
            "eppadi", "irukkenga", "nanba", "vanakkam", "yenna", "saappaadu", "thalaiva",
            
            # Telugu
            "ela", "unnavu", "thammudu", "anna", "namaskaram", "enti", "sangathi"
        ]
        
        text_lower = text.lower()
        # Check for whole words to avoid false positives
        for trigger in triggers:
            if re.search(r'\b' + re.escape(trigger) + r'\b', text_lower):
                return True
        return False

    def handle_conversational_slang(self, text):
        """Handle specific slang greetings with localized responses"""
        text_lower = text.lower().strip().replace('?', '').replace('!', '')
        
        # Mapping common greetings to localized responses
        greetings_map = {
            # Kannada
            "yen guru": "Helu guru, yen samachara? What can I help you with today? 😉",
            "yen samachara": "Yellu super guru! Tell me what's on your mind today.",
            "maga helu": "Helu maga! Ready and set, what do you need?",
            "yen maga": "Yenu illa maga! Fast responses ready for you. Tell me!",
            
            # Hindi
            "kya haal hai": "Ekdum mast bhai! Aap batao, how can I help you today? 🔥",
            "kaise ho": "Badiya dost! Ready to assist you. What's the plan?",
            "bol bhai": "Ji bhai, tell me what you need! I'm here for you.",
            
            # Tamil
            "eppadi irukkenga": "Nalla irukkenga nanba! How about you? What can MAXY do for you?",
            "yenna saappaadu": "Innum saapala nanba! AI logic doesn't need food, only your queries! 😂",
            
            # Telugu
            "ela unnavu": "Chala bagunnanu anna! How can I help you today?",
            "enti sangathi": "Antha manchide! Ready to chat, tell me what you need."
        }
        
        # Check for exact matches first
        if text_lower in greetings_map:
            return greetings_map[text_lower]
            
        # Check if text contains the keywords
        for key, response in greetings_map.items():
            if key in text_lower:
                return response
                
        return None

    def get_random_slang(self, force=False):
        """Get a random slang word"""
        if not self.enabled and not force:
            return "friend"
            
        if not self.slangs:
            return "Maga"
        return random.choice(self.slangs)

    def enhance_text(self, text, model_name="MAXY", force=False):
        """Randomly inject slang into text"""
        if not self.enabled and not force:
            return text
            
        # Higher chance if forced
        threshold = 0.6 if force else 0.3
            
        # Chance to start with a slang
        if random.random() < threshold:
            slang = self.get_random_slang(force=True)
            text = f"{slang}, {text}"
            
        # Chance to end with a slang
        elif random.random() < threshold:
            slang = self.get_random_slang(force=True)
            if text.endswith('.'):
                text = text[:-1]
            text = f"{text}, {slang}."
            
        return text

    def get_greeting(self, force=False):
        """Get a slang-infused greeting"""
        if not self.enabled and not force:
            return random.choice([
                "Hello, what's up?",
                "Namaste!",
                "Hey there, how are you?",
                "Hello, welcome!",
                "Hi, let's chat."
            ])
            
            
        slang = self.get_random_slang(force=True)
        greetings = [
            f"Yen {slang}, what's up?",
            f"Namaskara {slang}!",
            f"Hey {slang}, hegidira?",
            f"Lo {slang}, welcome!",
            f"Banni {slang}, let's chat.",
            f"Kya haal hai {slang}?",
            f"Eppadi irukkiya {slang}?",
            f"Ela unnavu {slang}?"
        ]
        return random.choice(greetings)
