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
            "macha", "machaa", "maga", "magane", "guru", "boss", "bossu", "thika", "sisya", 
            "da", "kane", "kano", "le", "lo", "aliyas", "dove",
            "mama", "machan", "mass", "scene", "sakath", "tumba", 
            "swalpa", "adjust", "beda", "beku", "super", "ayyo", 
            "chindi", "bindaas", "figure", "loose", "item", "jugaad", 
            "ghanta", "pakao", "mast", "kaand", "faltu", "timepass", 
            "jhol", "funda", "bakwaas", "senti", "patli", "jhakas",
            "bro", "broski", "dude", "buddy", "maadi", "kelsa", "hogona", "banni",
            "yen", "helu", "samachara", "yelli", "hogu", "dei", "barre", "chal", "oye",
            "ri", "ba", "seri", "howdu", "howdu howdu", "yesu", "sceneu",
            
            # Common/Command Slangs (Isolated)
            "next", "previous", "start", "stop", "go", "come", "wait", "hold", "leave",
            "take", "give", "show", "check", "look", "talk", "tell", "ask", "reply",
            "text", "call", "ping", "msg", "status", "update", "fix", "error", "bug",
            "issue", "problem", "solution", "idea", "plan", "project", "task", "work",
            "job", "money", "food", "tea", "coffee", "lunch", "dinner", "party", "trip",
            "movie", "game", "bored", "sleep", "wake", "study", "exam", "result", "rank",
            "fail", "pass", "win", "lose", "fight", "love", "crush", "breakup", "marriage",
            "family", "friend", "group", "gang", "area", "local", "global",
            
            # Hindi
            "kya", "haal", "bhai", "yaar", "dost", "kaise", "bol", "mast", "jhakaas",
            "bindaas", "paisa", "waat", "kalti", "khopdi", "bheja", "dhassu","acha"
            
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
            # --- CONVERSATIONAL PHRASES ---
            "yen guru": "Helu guru, yen samachara? What can I help you with today? 😉",
            "yen samachara": "Yellu super guru! Tell me what's on your mind today.",
            "maga helu": "Helu maga! Ready and set, what do you need?",
            "yen maga": "Yenu illa maga! Fast responses ready for you. Tell me!",
            "kya haal hai": "Ekdum mast bhai! Aap batao, how can I help you today? 🔥",
            "kaise ho": "Badiya dost! Ready to assist you. What's the plan?",
            "bol bhai": "Ji bhai, tell me what you need! I'm here for you.",
            "eppadi irukkenga": "Nalla irukkenga nanba! How about you? What can MAXY do for you?",
            "yenna saappaadu": "Innum saapala nanba! AI logic doesn't need food, only your queries! 😂",
            "ela unnavu": "Chala bagunnanu anna! How can I help you today?",
            "enti sangathi": "Antha manchide! Ready to chat, tell me what you need.",
            
            # --- ISOLATED SLANGS (To prevent Wiki triggers) ---
            "macha": "En macha, what's the scene?",
            "machaa": "Macha machaa! Tell me properly.",
            "machan": "Machan, sollu da!",
            "maga": "Helu maga, yen samachara?",
            "magane": "Magane! What happened?",
            "guru": "Guru, what's cooking?",
            "boss": "Yes boss, tell me.",
            "bossu": "Bossu! What service?",
            "bro": "Brooo, what plan?",
            "broski": "Broski! What’s up?",
            "da": "En da, heli!",
            "dei": "Dei, calm and tell.",
            "yaar": "Bol yaar, kya hua?",
            "dost": "Haan dost, scene kya?",
            "bhai": "Bhai, batao.",
            "anna": "Heli anna.",
            "akka": "Heli akka.",
            "thambi": "Sollu thambi.",
            "thala": "Thala! What help?",
            "chetta": "Parayoo chetta.",
            "saar": "Yes saar, tell me.",
            "madam": "Yes madam, what do you need?",
            "mapla": "Mapla, enna da?",
            "figure": "Which figure macha?",
            "mass": "Mass ah? Explain.",
            "scene": "En scene guru?",
            "tight": "Why tight face?",
            "ayyo": "Ayyo! What happened?",
            "arre": "Arre baba, bolo.",
            "chal": "Chal, start telling.",
            "oye": "Oye hero!",
            "lo": "Lo guru, talk.",
            "ri": "Ri, yen aitu?",
            "ba": "Ba, sit and tell.",
            "swalpa": "Swalpa detail kodi.",
            "adjust": "Adjust maadi, heli.",
            "chill": "Chill guru.",
            "seri": "Seri, now tell.",
            "okay da": "Okay da, next?",
            "correct": "Correct aa?",
            "super": "Super! Now what?",
            "top": "Top macha!",
            "full": "Full confusion ah?",
            "item": "Which item guru?",
            "matter": "En matter?",
            "ganchali": "Ganchali beda, straight heli.",
            "summane": "Summane ya?",
            "nakko": "Nakko tension.",
            "beda": "Beda worry.",
            "illa": "Illa problem.",
            "howdu": "Howdu howdu!",
            "yesu": "Yesu maga?",
            "nope": "Nope ah?",
            "sceneu": "Sceneu yen guru?",
            "mad": "Why mad bro?",
            "cool": "Cool macha.",
            "hot": "Hot topic ah?",
            "fresh": "Fresh news ah?",
            "oldu": "Oldu story?",
            "waste": "Waste topic beda.",
            "solid": "Solid idea!",
            "kick": "Kick ide!",
            "josh": "Full josh!",
            "speed": "Speed kammi maadi.",
            "slow": "Slow ah heli.",
            "fast": "Fast fast solra.",
            "late": "Late aita?",
            "early": "Early bird ah?",
            "peak": "Peak level guru!",
            "level": "Level beda.",
            "next": "Next enu?",
            "previous": "Previous story?",
            "random": "Random ah?",
            "direct": "Direct point heli.",
            "indirect": "Round round beda.",
            "clear": "Clear aa?",
            "doubt": "Doubt ide?",
            "confirm": "Confirm maadi.",
            "cancel": "Cancel aita?",
            "start": "Start maadona?",
            "stop": "Stop guru.",
            "go": "Go ahead.",
            "come": "Come on macha.",
            "sit": "Sit and tell.",
            "stand": "Stand by guru.",
            "wait": "Wait swalpa.",
            "hold": "Hold on.",
            "leave": "Leave it guru.",
            "take": "Take easy.",
            "give": "Give details.",
            "bring": "Bring topic.",
            "send": "Send info.",
            "show": "Show me scene.",
            "check": "Check maadi.",
            "look": "Look guru.",
            "watch": "Watch out.",
            "listen": "Listen maga.",
            "hear": "Hearing you.",
            "speak": "Speak up.",
            "talk": "Talk da.",
            "tell": "Tell fully.",
            "ask": "Ask freely.",
            "answer": "Answer kodtini.",
            "reply": "Reply fast.",
            "text": "Text maadu.",
            "call": "Call maadi.",
            "ping": "Ping guru.",
            "msg": "Message maadu.",
            "status": "Status yen?",
            "update": "Update kodi.",
            "upgrade": "Upgrade aita?",
            "downgrade": "Downgrade ya?",
            "fix": "Fix maadona.",
            "repair": "Repair ide?",
            "break": "Break aita?",
            "build": "Build maadi.",
            "create": "Create maadona.",
            "delete": "Delete maadi.",
            "remove": "Remove aita?",
            "add": "Add maadu.",
            "insert": "Insert maadi.",
            "edit": "Edit maadona.",
            "copy": "Copy maadu.",
            "paste": "Paste maadi.",
            "cut": "Cut maadu.",
            "save": "Save maadi.",
            "open": "Open maadi.",
            "close": "Close maadu.",
            "lock": "Lock aita?",
            "unlock": "Unlock maadi.",
            "run": "Run maadona.",
            "execute": "Execute maadi.",
            "error": "Error bandide?",
            "bug": "Bug ide?",
            "issue": "Issue yen?",
            "problem": "Problem heli.",
            "solution": "Solution kodtini.",
            "idea": "Idea super!",
            "plan": "Plan yen?",
            "project": "Project scene?",
            "task": "Task enu?",
            "work": "Work item?",
            "job": "Job update?",
            "salary": "Salary yen?",
            "money": "Money scene?",
            "loan": "Loan beka?",
            "rent": "Rent katra?",
            "food": "Food aita?",
            "tea": "Tea break?",
            "coffee": "Coffee beka?",
            "lunch": "Lunch aita?",
            "dinner": "Dinner plan?",
            "party": "Party scene?",
            "trip": "Trip hogona?",
            "movie": "Movie plan?",
            "match": "Match nodtira?",
            "game": "Game aata?",
            "timepass": "Timepass ah?",
            "bored": "Bored ah?",
            "sleep": "Sleep aita?",
            "wake": "Wake up guru!",
            "study": "Study maadtira?",
            "exam": "Exam tension?",
            "result": "Result bandide?",
            "rank": "Rank yen?",
            "fail": "Fail aita?",
            "pass": "Pass ayta?",
            "win": "Win maadona!",
            "lose": "Lose aita?",
            "fight": "Fight beda.",
            "love": "Love story ah?",
            "crush": "Crush ide?",
            "breakup": "Breakup aita?",
            "marriage": "Marriage plan?",
            "family": "Family members chennagidara?",
            "friend": "Friend scene?",
            "group": "Group plan?",
            "gang": "Gang entry!",
            "area": "Area yen?",
            "local": "Local hero!",
            "global": "Global level!"
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
