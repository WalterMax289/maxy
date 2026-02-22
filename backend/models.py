"""
MAXY AI Models Implementation
Enhanced models with distinct personalities and capabilities
"""

import random
import logging
import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import wikipedia
from data_analyzer import AdvancedAnalyzer, TextAnalyzer, StructuredDataAnalyzer
from code_composer import CodeComposer
from slang_manager import SlangManager
import requests
from ddgs import DDGS
import yfinance as yf

# Initialize Slang Manager
slang_manager = SlangManager()

logger = logging.getLogger(__name__)


class MAXYThinkingEngine:
    """Generate AI thinking/reasoning display"""
    
    @staticmethod
    def generate_thinking(
        model_name: str,
        user_message: str,
        analysis_type: str = "general"
    ) -> str:
        """Generate thinking process for display"""
        
        reasoning_steps = {
            'quick': [
                "Analyzing input...",
                "Formulating response...",
                "Optimizing output..."
            ],
            'research': [
                "Identifying key topics...",
                "Searching knowledge sources...",
                "Synthesizing information...",
                "Structuring comprehensive response..."
            ],
            'conversation': [
                "Understanding context...",
                "Identifying intent...",
                "Crafting natural response..."
            ],
            'analysis': [
                "Examining content structure...",
                "Extracting key information...",
                "Identifying patterns...",
                "Generating insights..."
            ]
        }
        
        steps = reasoning_steps.get(analysis_type, reasoning_steps['quick'])
        
        thinking_text = f"Analyzing: '{user_message[:50]}'\n\n"
        thinking_text += "Processing:\n"
        for i, step in enumerate(steps, 1):
            thinking_text += f"{i}. {step}\n"
        
        if analysis_type == 'research':
            thinking_text += f"{len(steps) + 1}. Verifying factual consistency...\n"
            thinking_text += f"{len(steps) + 2}. Cross-referencing sources...\n"
            
        return thinking_text


class KnowledgeSynthesizer:
    """Intelligent search result synthesis and verification"""
    
    @staticmethod
    def get_keywords(query: str) -> List[str]:
        """Extract core keywords from query for relevance scoring"""
        # Basic keyword extraction: remove noise, focus on entities
        noise = ['is', 'who', 'the', 'of', 'what', 'was', 'were', 'tell', 'me', 'about', 'how', 'does', 'are']
        words = re.findall(r'\b\w+\b', query.lower())
        return [w for w in words if w not in noise and len(w) > 2]

    @staticmethod
    def score_relevance(query: str, title: str, body: str) -> float:
        """Score how relevant a search result is to the query"""
        keywords = KnowledgeSynthesizer.get_keywords(query)
        if not keywords:
            return 0.5
            
        content = (title + " " + body).lower()
        matches = sum(1 for kw in keywords if kw in content)
        
        # Identity query boost: If query is "who is X", ensure X is in the content
        identity_keywords = ['who is', 'who was', 'identity', 'person']
        if any(ik in query.lower() for ik in identity_keywords):
            # Try to find specific names (Title Case words) in query
            names = re.findall(r'\b[A-Z][a-z]+\b', query)
            if names:
                name_matches = sum(1 for name in names if name.lower() in content)
                if name_matches == 0:
                    return 0.1 # Very low relevance if name is missing
        
        score = matches / len(keywords)
        
        # Penalty for low-quality sources in body (casual mentions)
        junk_indicators = ['reddit', 'quora', 'forum', 'comment', 'manhwa', 'manga', 'recommendation']
        # If the user didn't ask for entertainment, penalize entertainment sources
        if not any(ek in query.lower() for ek in ['manga', 'manhwa', 'comic', 'read']):
            if any(ji in body.lower() for ji in junk_indicators):
                score *= 0.5
        
        return score

    @staticmethod
    def verify_facts(query: str, results: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Verify and rank search results by relevance"""
        ranked = []
        for res in results:
            score = KnowledgeSynthesizer.score_relevance(query, res.get('title', ''), res.get('body', ''))
            res['relevance_score'] = score
            ranked.append(res)
        
        return sorted(ranked, key=lambda x: x['relevance_score'], reverse=True)

    @staticmethod
    def get_best_match(query: str, results: List[Dict[str, str]], threshold: float = 0.3) -> Optional[Dict[str, Any]]:
        """Identify the single most relevant search result"""
        verified = KnowledgeSynthesizer.verify_facts(query, results)
        if verified and verified[0]['relevance_score'] >= threshold:
            return verified[0]
        return None


class MAXY1_1:
    """MAXY 1.1 - Quick Responses & Thinking
    
    Optimized for:
    - Lightning-fast responses
    - Clear thinking process display
    - Friendly, concise conversational AI
    """
    
    NAME = "MAXY 1.1"
    VERSION = "1.1.0"
    DESCRIPTION = "Quick response AI with visible thinking process"
    
    # Quick response templates organized by intent
    GREETINGS = [
        "Hey there! 👋 Ready to chat!",
        "Hello! What can I help you with?",
        "Hi! I'm here and ready to assist!",
        "Hey! Great to see you!",
    ]
    
    FAREWELLS = [
        "Goodbye! Catch you later! 👋",
        "See you soon! Take care!",
        "Bye for now! Come back anytime!",
        "Until next time! Stay awesome!",
    ]
    
    GRATITUDE = [
        "You're welcome! Happy to help! 😊",
        "Anytime! That's what I'm here for!",
        "Glad I could assist!",
        "No problem at all!",
    ]
    
    HOW_ARE_YOU = [
        "I'm doing great, thanks for asking! How are you?",
        "Excellent! Ready to help. You?",
        "Fantastic! What about you?",
        "All good here! How's your day?",
    ]
    
    IDENTITY = [
        "I'm MAXY 1.1 - your quick-thinking AI assistant! I provide fast responses with clear reasoning.",
        "Hello! I'm MAXY 1.1, designed for rapid responses and friendly conversation!",
        "I'm MAXY 1.1! I specialize in quick, thoughtful responses with visible thinking processes.",
    ]
    
    GENERAL_QUICK = [
        "Got it! Tell me more.",
        "Interesting! Continue...",
        "I see! What else?",
        "That makes sense!",
        "Understood! What's next?",
        "Okay! How can I help further?",
    ]
    
    JOKES = [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call a fake noodle? An impasta! 🍝",
        "Why don't eggs tell jokes? They'd crack each other up!",
        f"Lo {slang_manager.get_random_slang()}, why did the tomato turn red? Because it saw the salad dressing! 😂",
        f"{slang_manager.get_random_slang()}, parallel lines have so much in common but they’ll never meet. Sad scene no? 😅"
    ]
    
    @staticmethod
    def should_use_wikipedia(message: str) -> bool:
        """Determine if this is a knowledge/research question"""
        research_keywords = [
            'what is', 'who is', 'how does', 'explain', 'tell me about',
            'info about', 'information on', 'details about', 'who was',
            'what are', 'define', 'describe', 'history of', 'science',
            'technology', 'biology', 'physics', 'chemistry', 'geography',
            'country', 'capital', 'famous', 'invented', 'discovered',
            'when did', 'where is', 'why does', 'sort', 'search', 'array',
            'list', 'tree', 'graph', 'data structure', 'algorithm', 
            'implement', 'code', 'function', 'class', 'decorator',
            'python', 'javascript', 'java', 'html', 'css', 'sql',
            'pm of', 'president of', 'governor of', 'ceo of',
            'can you explain', 'could you tell me', 'i want to know',
            'learn about', 'guide to', 'overview of', 'introduction to',
            'basics of', 'advanced', 'in depth', 'detailed explanation',
            'summary of', 'quick facts about', 'key points of',
            'important facts', 'meaning of', 'definition of',
            'full form of', 'origin of', 'background of', 'concept of',
            # Time / Historical Queries
            'when was', 'when is', 'how long does', 'how long did',
            'how many years', 'timeline of', 'era of', 'period of',
            'ancient', 'modern', 'medieval', 'future of', 'predicted',
            'forecast of', 'trend in', 'evolution of',
            # Location / Geography
            'located in', 'situated in', 'map of', 'population of',
            'area of', 'largest', 'smallest', 'bordering',
            'neighboring countries', 'climate of', 'currency of',
            'language of',
            # People / Position
            'founder of', 'owner of', 'chairman of', 'minister of',
            'prime minister of', 'king of', 'queen of', 'director of',
            'author of', 'creator of', 'biography of', 'net worth of',
            'age of', 'early life of',
            # Science and Education
            'theory of', 'law of', 'principle of', 'formula for',
            'equation of', 'difference between', 'compare',
            'comparison between', 'advantages of', 'disadvantages of',
            'types of', 'branches of', 'process of', 'cycle of',
            'structure of', 'function of', 'example of',
            # Programming / Tech
            'syntax of', 'how to use', 'usage of',
            'best practices for', 'error in', 'debug', 'optimize',
            'performance of', 'library for', 'framework for', 'api for',
            'database', 'backend', 'frontend', 'full stack',
            'machine learning', 'artificial intelligence', 'cybersecurity',
            'cloud computing', 'blockchain', 'data science', 'deep learning',
            # Data Structures & Algorithms
            'time complexity', 'space complexity', 'big o notation',
            'linear search', 'binary search', 'merge sort', 'quick sort',
            'dynamic programming', 'recursion', 'greedy algorithm',
            'stack', 'queue', 'linked list', 'binary tree', 'bst',
            'heap', 'hash table',
            # Business / Economy
            'market value', 'stock price of', 'economy of', 'gdp of',
            'inflation rate', 'revenue of', 'profit of',
            'business model of', 'case study of', 'impact of', 'benefits of'
        ]
        msg_lower = message.lower()
        return any(kw in msg_lower for kw in research_keywords) and len(message) < 200
    
    @staticmethod
    def quick_wikipedia_lookup(query: str) -> Optional[str]:
        """Quick knowledge lookup for maxy1.1 with multi-source verification"""
        try:
            candidates = []
            
            # 1. Wikipedia Search
            try:
                search_results = wikipedia.search(query, results=3)
                for res in search_results:
                    try:
                        page = wikipedia.page(res, auto_suggest=False)
                        candidates.append({
                            'title': page.title,
                            'body': page.summary[:800],
                            'source': 'wikipedia'
                        })
                    except:
                        continue
            except Exception as e:
                logger.error(f"Wiki lookup error: {e}")

            # 2. DuckDuckGo Search
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=5))
                    for res in results:
                        candidates.append({
                            'title': res['title'],
                            'body': res['body'],
                            'source': 'web'
                        })
            except Exception as e:
                logger.error(f"DDG search error: {e}")

            if not candidates:
                return None

            # 3. Verify and Synthesis
            best_match = KnowledgeSynthesizer.get_best_match(query, candidates, threshold=0.25)
            
            if best_match:
                content = best_match['body']
                # If it's a web source, include title
                if best_match['source'] == 'web':
                    return f"{best_match['title']}: {content}"
                return content
            
            return None
        except Exception as e:
            logger.error(f"Quick lookup total error: {e}")
            return None

    @staticmethod
    def get_weather(city: str) -> Optional[str]:
        """Fetch weather data from OpenMeteo"""
        try:
            # 1. Geocoding
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            geo_res = requests.get(geo_url).json()
            
            if not geo_res.get('results'):
                return None
                
            lat = geo_res['results'][0]['latitude']
            lon = geo_res['results'][0]['longitude']
            name = geo_res['results'][0]['name']
            country = geo_res['results'][0]['country']
            
            # 2. Weather
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=auto"
            w_res = requests.get(weather_url).json()
            
            current = w_res.get('current', {})
            temp = current.get('temperature_2m')
            humidity = current.get('relative_humidity_2m')
            wind = current.get('wind_speed_10m')
            
            # Weather codes
            codes = {
                0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                45: "Foggy", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Drizzle",
                55: "Heavy drizzle", 61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
                71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow", 95: "Thunderstorm"
            }
            condition = codes.get(current.get('weather_code'), "Variable")
            
            return f"{condition} in {name}, {country}. Temp: {temp}°C, Humidity: {humidity}%, Wind: {wind} km/h."
            
        except Exception as e:
            logger.error(f"Weather error: {e}")
            return None
    
    @staticmethod
    def analyze_user_intent(message: str) -> Dict[str, Any]:
        """Analyze what the user wants - improved context understanding"""
        msg_lower = message.lower().strip()
        
        # Intent categories
        intents = {
            'greeting': any(g in msg_lower for g in ['hi', 'hello', 'hey', 'greetings', 'howdy']),
            'farewell': any(f in msg_lower for f in ['bye', 'goodbye', 'see you', 'farewell', 'later']),
            'gratitude': any(t in msg_lower for t in ['thanks', 'thank you', 'appreciate', 'grateful']),
            'personal_status': any(h in msg_lower for h in ['how are you', 'how you doing']),
            'identity': any(i in msg_lower for i in ['your name', 'who are you', 'what are you']),
            'entertainment': any(j in msg_lower for j in ['joke', 'funny', 'laugh']),
            'time_query': any(t in msg_lower for t in ['time', 'what time', 'current time']),
            'date_query': any(d in msg_lower for d in ['date', 'today', 'what day']),
            'help': any(h in msg_lower for h in ['help', 'what can you do']),
            'knowledge': any(k in msg_lower for k in ['what is', 'who is', 'how does', 'explain', 'tell me about', 'info about', 'information on', 'details about']),
            'calculation': any(c in msg_lower for c in ['calculate', 'math', 'plus', 'minus', 'times', 'divided']),
            'weather': any(w in msg_lower for w in ['weather', 'temperature', 'rain', 'sunny']),
            'simple_task': len(message.split()) <= 3 and not any(char.isdigit() for char in message)
        }
        
        # Detect urgency/enthusiasm
        urgency = sum(1 for char in message if char in '!') + (2 if 'urgent' in msg_lower or 'asap' in msg_lower else 0)
        
        # Detect if user is new (short greeting)
        is_new_user = intents['greeting'] and len(message) < 10
        
        return {
            'intents': intents,
            'urgency': urgency,
            'is_new_user': is_new_user,
            'message_length': len(message),
            'word_count': len(message.split())
        }
    
    @staticmethod
    def generate_concise_response(intent_analysis: Dict[str, Any], message: str, use_slang: bool = False, user_name: Optional[str] = None) -> tuple[str, float]:
        """Generate 3-4 sentence response based on intent"""
        intents = intent_analysis['intents']
        msg_lower = message.lower().strip()
        
        # Priority 1: Check for knowledge/research queries FIRST to avoid accidental slang triggers
        if intents['knowledge'] or MAXY1_1.should_use_wikipedia(message):
            wiki_result = MAXY1_1.quick_wikipedia_lookup(message)
            if wiki_result:
                # Allow 4-5 sentences for "Gemini-like" fluency
                raw_sentences = [s.strip() for s in wiki_result.split('. ') if s.strip()]
                clean_sentences = [s for s in raw_sentences if len(s) > 10]
                sentences = clean_sentences[:5] 
                concise = '. '.join(sentences)
                if not concise.endswith('.'):
                    concise += '.'
                if len(concise) < 100:
                    concise += " Would you like to know more about its history or specific details?"
                return (concise, 0.92)

        # Priority 2: Check for specific slang conversational greetings
        slang_response = slang_manager.handle_conversational_slang(message)
        if slang_response:
            return (slang_response, 0.99)
        
        # Greeting - Friendly and welcoming (3-4 sentences)
        if intents['greeting']:
            # Use real user name if available, otherwise fall back to slang/friend
            address = user_name if user_name else slang_manager.get_random_slang(use_slang)
            if intent_analysis.get('is_new_user', False):
                return (f"Hey {address}! Welcome! I'm MAXY 1.1, your quick AI assistant. I'm here to help with fast answers and friendly chat. What can I do for you today?", 0.98)
            else:
                return (f"Hey {address}! Great to see you again! Ready when you are. What's on your mind today?", 0.97)
        
        # Farewell - Warm goodbye (2-3 sentences)
        elif intents['farewell']:
            return (random.choice([
                "Goodbye! Thanks for chatting with me. Take care and come back anytime you need quick help! 👋",
                "See you later! It was great helping you out today. Have an awesome day!",
                "Bye for now! Don't hesitate to return if you need fast answers to anything!"
            ]), 0.98)
        
        # Gratitude - Humble and helpful (2-3 sentences)
        elif intents['gratitude']:
            return (random.choice([
                f"You're very welcome! Happy I could help quickly, {slang_manager.get_random_slang(use_slang)}. Let me know if you need anything else! 😊",
                "Anytime! That's what I'm here for. Feel free to ask more questions anytime!",
                f"Glad I could assist, {slang_manager.get_random_slang(use_slang)}! Don't hesitate to reach out if you need more quick answers!"
            ]), 0.96)
        
        # Personal status - Friendly reciprocation (3 sentences)
        elif intents['personal_status']:
            return (random.choice([
                "I'm doing fantastic, thanks for asking! All systems are running smoothly and I'm ready to help. How about you? How's your day going?",
                "Excellent! I'm energized and ready to assist. Thanks for checking in! How are you feeling today?",
                "I'm great! Optimized and ready for quick responses. How about yourself? What's new with you?"
            ]), 0.94)
        
        # Identity - Brief intro (3 sentences)
        elif intents['identity']:
            return ("I'm MAXY 1.1, your quick-thinking AI assistant! I specialize in fast, clear responses to help you get answers quickly. I can chat, answer questions, or help with simple tasks. What do you need?", 0.96)
        
        # Entertainment - Fun and light (1-2 sentences)
        elif intents['entertainment']:
            joke = random.choice(MAXY1_1.JOKES)
            return (f"{joke} 😄 Hope that brought a smile to your face!", 0.92)
        
        # Time query - Direct answer (2 sentences)
        elif intents['time_query']:
            current = datetime.now().strftime("%I:%M %p")
            return (f"It's {current} right now! ⏰ Is there something time-sensitive you need help with?", 0.97)
        
        # Date query - Direct answer (2 sentences)
        elif intents['date_query']:
            current = datetime.now().strftime("%A, %B %d, %Y")
            return (f"Today is {current}! 📅 Anything special planned for today?", 0.97)
        
        # Weather - Informative but brief (3 sentences)
        elif intents['weather']:
            # Extract potential city name (simple heuristic)
            words = message.split()
            city = None
            if 'in' in words:
                idx = words.index('in')
                if idx + 1 < len(words):
                    city = words[idx + 1].strip('?.!')
            
            # If no "in", try to take the last word if it looks like a city
            if not city and len(words) > 0:
                 potential = words[-1].strip('?.!')
                 if potential.istitle() and potential.lower() not in ['weather', 'today', 'now']:
                     city = potential

            if city:
                weather_info = MAXY1_1.get_weather(city)
                if weather_info:
                    return (f"{weather_info} 🌤️ Need anything else?", 0.95)
            
            return ("I can check the weather if you tell me which city! Just ask 'weather in London' for example. 🌍", 0.90)
        
        # Simple task - Check for single word/short "tasks" that are actually topics
        elif intents['simple_task']:
            # If message is very short (1-3 words), treat as potential query FIRST
            # Unnless it's a identified slang greeting/trigger
            if len(message.split()) <= 3 and not use_slang:
                 wiki_result = MAXY1_1.quick_wikipedia_lookup(message)
                 if wiki_result:
                    raw_sentences = [s.strip() for s in wiki_result.split('. ') if s.strip()]
                    clean_sentences = [s for s in raw_sentences if len(s) > 10]
                    sentences = clean_sentences[:5]
                    concise = '. '.join(sentences)
                    if not concise.endswith('.'):
                        concise += '.'
                    return (concise, 0.92)

            return ("I understand! I'm ready to proceed. What specific action would you like me to take with this information?", 0.88)
        
        # Help request - Quick capabilities (3-4 sentences)
        elif intents['help']:
            return ("I'm MAXY 1.1, your quick AI assistant! I can answer questions, chat with you, look up quick facts, and help with simple tasks. I'm all about speed and clarity. What would you like help with?", 0.93)
        
        # Calculation - Offer to help (2-3 sentences)
        elif intents['calculation']:
            return ("I can help with calculations! Just give me the numbers and what operation you need. I'll get you the answer quickly!", 0.91)
        
        # Default - Engaging but brief (3 sentences)
        else:
            return (random.choice([
                "Interesting! Tell me more about what you're looking for. I'm here to help quickly!",
                "I see! What's the main thing you need help with? I'm ready to assist!",
                "Got it! How can I make this easier for you? Let me know what you need!",
                "Okay! What's the next step? I'm here to provide quick answers!",
                "Understood! What specific information do you need? I'll get it for you fast!"
            ]), 0.85)
    
    @staticmethod
    def analyze_casual_context(message: str, history: List[Dict]) -> str:
        """Analyze context for casual conversation continuity"""
        if not history:
            return ""
            
        last_user_msg = next((m['content'] for m in reversed(history) if m['role'] == 'user'), "")
        last_ai_msg = next((m['content'] for m in reversed(history) if m['role'] == 'assistant'), "")
        
        # Check if we asked a question
        if "?" in last_ai_msg:
            return "continuing_conversation"
            
        return "new_topic"

    @staticmethod
    def process_message(
        message: str,
        include_thinking: bool = True,
        conversation_history: Optional[List[Dict]] = None,
        user_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process message with enhanced understanding and concise 3-4 sentence responses"""
        
        # Detect if user is using slang to trigger reactive mode
        use_slang = slang_manager.detect_slang(message)
        
        # Analyze user intent for better understanding
        intent_analysis = MAXY1_1.analyze_user_intent(message)
        
        # Context analysis
        context_status = MAXY1_1.analyze_casual_context(message, conversation_history or [])
        
        # Generate thinking process
        thinking = None
        if include_thinking:
            thinking = MAXYThinkingEngine.generate_thinking(
                MAXY1_1.NAME,
                message,
                "quick"
            )
        
        # Generate appropriate concise response with slang awareness
        response, confidence = MAXY1_1.generate_concise_response(intent_analysis, message, use_slang, user_name)
        
        # Adjust for context
        if context_status == "continuing_conversation" and intent_analysis['intents']['greeting']:
            # Don't greet again if we are continuing
            response = "I'm listening! Go on." 
            confidence = 0.99
        
        # Ensure response is 2-3 sentences max for MAXY 1.1
        sentences = [s.strip() for s in response.split('. ') if s.strip()]
        if len(sentences) > 3:
            response = '. '.join(sentences[:3])
            if not response.endswith('.'):
                response += '.'
        
        # Inject slang (chance based) for standard interactions
        if not intent_analysis.get('is_new_user', False) and intent_analysis['intents']['greeting'] == False: # Don't double slang greeting
             response = slang_manager.enhance_text(response, force=use_slang)
        
        result = {
            'response': response,
            'model': MAXY1_1.NAME,
            'confidence': confidence,
        }
        
        if thinking:
            result['thinking'] = thinking
        
        return result


class MAXY1_2:
    """MAXY 1.2 - Deep Research & Wikipedia Knowledge + Conversation
    
    Optimized for:
    - Deep Wikipedia research with detailed analysis
    - Natural human-AI conversation
    - Context-aware responses
    """
    
    NAME = "MAXY 1.2"
    VERSION = "1.2.0"
    DESCRIPTION = "Deep research expert with Wikipedia knowledge and conversational abilities"
    
    # Conversational responses for non-research queries
    CONVERSATION_GREETINGS = [
        "Hello! I'm MAXY 1.2. I can dive deep into research topics or just chat with you. What would you like?",
        "Hey there! Ready for deep research or casual conversation. What's on your mind?",
        "Hi! I'm here to provide in-depth knowledge or have a friendly chat. Your choice!",
    ]
    
    CONVERSATION_RESPONSES = [
        "That's interesting! Tell me more about that.",
        "I see what you mean. Would you like to explore this topic further?",
        "Fascinating perspective! What are your thoughts on this?",
        "I understand. Is there a specific aspect you'd like me to research?",
        "Good point! We can dive deeper into this if you'd like.",
    ]
    
    HOW_ARE_YOU = [
        "I'm doing wonderfully, thank you! Ready to research or chat. How are you feeling today?",
        "I'm excellent! Whether you want deep analysis or casual conversation, I'm here. How about you?",
        "All systems optimal! I can provide detailed research or just have a friendly chat. You?",
    ]
    
    @staticmethod
    def is_research_query(message: str) -> bool:
        """Determine if user wants deep research or just conversation"""
        research_indicators = [
            'research', 'tell me about', 'what is', 'who is', 'explain',
            'info about', 'information on', 'details about', 'who was',
            'what are', 'define', 'describe', 'history of', 'science',
            'technology', 'biology', 'physics', 'chemistry', 'geography',
            'country', 'capital', 'famous', 'invented', 'discovered',
            'when did', 'where is', 'why does', 'the history of',
            'pm of', 'president of', 'governor of', 'ceo of',
            'can you explain', 'could you tell me', 'i want to know',
            'learn about', 'guide to', 'overview of', 'introduction to',
            'basics of', 'advanced', 'in depth', 'detailed explanation',
            'summary of', 'quick facts about', 'key points of',
            'important facts', 'meaning of', 'definition of',
            'full form of', 'origin of', 'background of', 'concept of',
            # Time / Historical Queries
            'when was', 'when is', 'how long does', 'how long did',
            'how many years', 'timeline of', 'era of', 'period of',
            'ancient', 'modern', 'medieval', 'future of', 'predicted',
            'forecast of', 'trend in', 'evolution of',
            # Location / Geography
            'located in', 'situated in', 'map of', 'population of',
            'area of', 'largest', 'smallest', 'bordering',
            'neighboring countries', 'climate of', 'currency of',
            'language of',
            # People / Position
            'founder of', 'owner of', 'chairman of', 'minister of',
            'prime minister of', 'king of', 'queen of', 'director of',
            'author of', 'creator of', 'biography of', 'net worth of',
            'age of', 'early life of',
            # Science and Education
            'theory of', 'law of', 'principle of', 'formula for',
            'equation of', 'difference between', 'compare',
            'comparison between', 'advantages of', 'disadvantages of',
            'types of', 'branches of', 'process of', 'cycle of',
            'structure of', 'function of', 'example of',
            # Programming / Tech
            'syntax of', 'how to use', 'usage of',
            'best practices for', 'error in', 'debug', 'optimize',
            'performance of', 'library for', 'framework for', 'api for',
            'database', 'backend', 'frontend', 'full stack',
            'machine learning', 'artificial intelligence', 'cybersecurity',
            'cloud computing', 'blockchain', 'data science', 'deep learning',
            # Data Structures & Algorithms
            'time complexity', 'space complexity', 'big o notation',
            'linear search', 'binary search', 'merge sort', 'quick sort',
            'dynamic programming', 'recursion', 'greedy algorithm',
            'stack', 'queue', 'linked list', 'binary tree', 'bst',
            'heap', 'hash table',
            # Business / Economy
            'market value', 'stock price of', 'economy of', 'gdp of',
            'inflation rate', 'revenue of', 'profit of',
            'business model of', 'case study of', 'impact of', 'benefits of'
        ]
        
        conversation_indicators = [
            'how are you', 'how do you feel', 'what do you think',
            'your opinion', 'chat', 'talk', 'conversation', 'just saying',
            'i feel', 'i think', 'my day', 'my life', 'personal',
            'joke', 'funny', 'story'
        ]
        
        msg_lower = message.lower()
        
        research_score = sum(1 for ind in research_indicators if ind in msg_lower)
        conversation_score = sum(1 for ind in conversation_indicators if ind in msg_lower)
        
        # If more conversation indicators, treat as conversation
        if conversation_score > research_score:
            return False
        
        # If research indicators present, treat as research
        return research_score > 0
    
    @staticmethod
    def deep_wikipedia_research(query: str) -> Dict[str, Any]:
        """Perform comprehensive verified research with professional synthesis"""
        try:
            candidates = []
            
            # 1. Wiki Search
            try:
                wiki_searches = wikipedia.search(query, results=5)
                for res in wiki_searches:
                    try:
                        page = wikipedia.page(res, auto_suggest=False)
                        candidates.append({
                            'title': page.title,
                            'body': page.summary,
                            'url': page.url,
                            'source': 'wikipedia'
                        })
                    except:
                        continue
            except:
                pass
                
            # 2. Web Search
            try:
                with DDGS() as ddgs:
                    web_results = list(ddgs.text(query, max_results=5))
                    for res in web_results:
                        candidates.append({
                            'title': res['title'],
                            'body': res['body'],
                            'url': res['href'],
                            'source': 'web'
                        })
            except:
                pass

            if not candidates:
                return {
                    'success': False,
                    'response': "Our core knowledge indices returned no high-confidence data for this inquiry.",
                    'confidence': 0.40
                }

            # 3. Verfication and Selection
            verified_results = KnowledgeSynthesizer.verify_facts(query, candidates)
            # Take the most relevant result that is detailed enough
            best_res = None
            for res in verified_results:
                if res['relevance_score'] > 0.4 and len(res['body']) > 200:
                    best_res = res
                    break
            
            if not best_res:
                best_res = verified_results[0]

            title = best_res['title']
            summary = best_res['body']
            url = best_res.get('url', 'N/A')
            
            # Professional Synthesis Logic
            paragraphs = [p.strip() for p in summary.split('\n\n') if len(p.strip()) > 100]
            if not paragraphs:
                paragraphs = [summary]
                
            intro = paragraphs[0]
            if len(intro) > 600:
                intro = intro[:600] + "..."
            
            all_sentences = [s.strip() for s in summary.split('. ') if len(s.strip()) > 20]
            insights = all_sentences[2:7]
            
            narrative = " ".join(paragraphs[1:3]) if len(paragraphs) > 1 else summary[600:2000]
            if len(narrative) > 1200:
                narrative = narrative[:1200] + "..."
                
            conclusion = f"The data regarding {title} suggests a consistent thematic pattern across primary and secondary sources. Further analysis of its foundational principles provides deeper context into its current relevance."

            response = f"**VERIFIED RESEARCH REPORT: {title.upper()}**\n"
            response += f"{'='*60}\n\n"
            
            if best_res['source'] == 'web':
                response += f"⚠️ **REAL-TIME SYNTHESIS:** This report incorporates current web data verified for relevance.\n\n"
            
            response += f"### I. SCHOLARLY OVERVIEW\n"
            response += f"{intro}\n\n"
            
            response += f"### II. CRITICAL INSIGHTS & THEMATIC ANALYSIS\n"
            for insight in insights[:4]:
                response += f"• {insight}.\n"
            response += "\n"
            
            response += f"### III. DETAILED TECHNICAL NARRATIVE\n"
            response += f"{narrative}\n\n"
            
            response += f"### IV. ACADEMIC CONCLUSION\n"
            response += f"{conclusion}\n\n"
            
            response += f"**REFERENCE INDICES**\n"
            response += f"📚 Primary Dataset: {url}\n"
            response += f"🔍 Synthesis Confidence: {int(best_res['relevance_score'] * 100)}%"
            
            return {
                'success': True,
                'response': response,
                'confidence': best_res['relevance_score'],
                'sources': [url]
            }
            
        except Exception as e:
            logger.error(f"Verified research error: {str(e)}")
            return {
                'success': False,
                'response': f"Research protocols failed due to a synthesis error: {str(e)[:50]}",
                'confidence': 0.50
            }
            
        except wikipedia.exceptions.PageError:
            return {
                'success': False,
                'response': f"The requested topic '{query}' does not reside within the primary Wikipedia datasets. Please verify the conceptual scope and try a broader nomenclature.",
                'confidence': 0.65
            }
        except Exception as e:
            logger.error(f"Professional research error: {str(e)}")
            return {
                'success': False,
                'response': f"A protocol error occurred during the deep research phase. Analysis aborted: {str(e)[:50]}",
                'confidence': 0.50
            }

    @staticmethod
    def perform_web_search(query: str) -> Dict[str, Any]:
        """Perform broader web search using DuckDuckGo"""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
            
            if not results:
                return {'success': False, 'response': "No web results found.", 'confidence': 0.5}

            response = f"**WEB SEARCH REPORT: {query.upper()}**\n\n"
            for i, res in enumerate(results, 1):
                response += f"**{i}. {res['title']}**\n"
                response += f"{res['body']}\n"
                response += f"🔗 {res['href']}\n\n"
            
            response += "**Synthesis:**\n"
            response += "The web search results indicate a variety of perspectives. "
            response += "This data complements traditional knowledge bases."

            return {
                'success': True,
                'response': response,
                'confidence': 0.90,
                'sources': [r['href'] for r in results]
            }
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return {'success': False, 'response': f"Web search failed: {e}", 'confidence': 0.5}
    
    @staticmethod
    def analyze_conversation_context(message: str, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Deep analysis of conversation context and user needs"""
        msg_lower = message.lower().strip()
        
        # Detect depth of inquiry
        depth_indicators = {
            'surface': ['what is', 'who is', 'simple', 'basic', 'quick'],
            'moderate': ['how does', 'why does', 'explain', 'tell me about'],
            'deep': ['analyze', 'comprehensive', 'detailed', 'in-depth', 'research', 'history of', 'science of']
        }
        
        inquiry_depth = 'surface'
        for depth, indicators in depth_indicators.items():
            if any(ind in msg_lower for ind in indicators):
                inquiry_depth = depth
                break
        
        # Detect user engagement level
        engagement_score = 0
        if conversation_history:
            engagement_score = min(len(conversation_history) * 0.5, 5)  # Max 5 points for history
        
        # Question complexity
        complexity = 'simple'
        question_words = msg_lower.count('?')
        word_count = len(message.split())
        
        if word_count > 15 or question_words >= 2:
            complexity = 'complex'
        elif word_count > 8 or question_words == 1:
            complexity = 'moderate'
        
        # Topic categories
        topics = {
            'science': any(t in msg_lower for t in ['science', 'physics', 'chemistry', 'biology', 'research']),
            'history': any(t in msg_lower for t in ['history', 'ancient', 'century', 'war', 'civilization']),
            'technology': any(t in msg_lower for t in ['technology', 'computer', 'internet', 'software', 'ai']),
            'geography': any(t in msg_lower for t in ['country', 'capital', 'city', 'continent', 'population']),
            'personal': any(t in msg_lower for t in ['i feel', 'i think', 'my opinion', 'in my experience']),
            'philosophy': any(t in msg_lower for t in ['meaning', 'philosophy', 'why do we', 'purpose', 'existence'])
        }
        
        return {
            'inquiry_depth': inquiry_depth,
            'engagement_score': engagement_score,
            'complexity': complexity,
            'topics': topics,
            'word_count': word_count,
            'is_follow_up': conversation_history is not None and len(conversation_history) > 0
        }
    
    @staticmethod
    def generate_detailed_response(context: Dict[str, Any], message: str, conversation_history: Optional[List[Dict]] = None, use_slang: bool = False, user_name: Optional[str] = None) -> tuple[str, float]:
        """Generate detailed 5-10 sentence response based on context"""
        msg_lower = message.lower().strip()
        
        # Priority 1: Check for deep research FIRST
        if context['inquiry_depth'] == 'deep' or MAXY1_2.is_research_query(message):
             # We skip direct response here to let process_message handle research flow
             pass
        else:
            # Priority 2: Check for specific slang conversational greetings
            slang_response = slang_manager.handle_conversational_slang(message)
            if slang_response:
                return (slang_response, 0.99)
            
        intents = context['topics']
        depth = context['inquiry_depth']
        complexity = context['complexity']
        
        # Determine address name
        user_display = f", {user_name}" if user_name else ""
        
        # Greeting - Warm and contextual (6-8 sentences)
        if any(g in msg_lower for g in ['hi', 'hello', 'hey', 'greetings']):
            if context.get('is_follow_up'):
                return (f"Hello again {slang_manager.get_random_slang(use_slang)}{user_display}! It's wonderful to continue our conversation. I've been thinking about our previous discussion and I'm ready to dive deeper into any topic you'd like to explore. Whether you need comprehensive research on a specific subject or just want to have an engaging conversation, I'm here to provide detailed insights. What direction would you like to take our discussion today? I'm particularly excited to help with any research questions or analytical topics you might have in mind!", 0.97)
            else:
                return (f"Namaskara{user_display}! I'm MAXY 1.2, your dedicated research and conversation companion. I'm genuinely excited to help you explore whatever topics interest you today. Whether you're looking for in-depth Wikipedia research, detailed analysis of complex subjects, or simply an engaging conversation, I'm fully equipped to assist. I specialize in providing comprehensive information with multiple perspectives and thorough context. What would you like to dive into, {slang_manager.get_random_slang(use_slang)}? I'm ready to provide detailed, well-researched responses!", 0.96)
        
        # Personal status - Thoughtful and engaging (5-7 sentences)
        elif any(h in msg_lower for h in ['how are you', 'how you doing']):
            return (random.choice([
                "I'm doing wonderfully, thank you so much for asking! I truly appreciate you checking in on me. I'm fully energized and ready to tackle any research questions or conversation topics you might have today. My systems are running optimally, which means I can provide you with comprehensive, detailed responses. How about yourself? I'd love to hear how you're feeling and what brings you here today. Is there a particular topic you're curious about or something specific you'd like to explore together?",
                "I'm excellent, and I really appreciate you asking! It means a lot that you'd check in. I'm completely ready to dive deep into research or have a meaningful conversation with you. All my knowledge systems are active and prepared to provide detailed analysis. How are you feeling today? I'd genuinely like to know what's on your mind and how I can help make your day better with some interesting information or a good conversation!"
            ]), 0.94)
        
        # Gratitude - Humble and offering more help (5-6 sentences)
        elif any(t in msg_lower for t in ['thanks', 'thank you']):
            return ("You're absolutely welcome! I'm truly delighted that I could be helpful to you. It brings me genuine satisfaction to know that my research or conversation was useful. Please don't hesitate to reach out whenever you need assistance, whether it's for deep research on complex topics or just a friendly chat. I'm always here and ready to provide detailed, thoughtful responses. Is there anything else I can help you explore or understand better today? I'd love to continue assisting you!", 0.96)
        
        # Farewell - Warm and inviting return (6-7 sentences)
        elif any(f in msg_lower for f in ['bye', 'goodbye', 'see you']):
            return ("Goodbye for now! It's been an absolute pleasure chatting with you and helping with your questions. I really enjoyed our conversation and any research we did together. Please know that you're always welcome to return whenever you need assistance, whether it's for deep research, detailed analysis, or just a friendly conversation. I'll be here with comprehensive knowledge and a willingness to help. Take good care of yourself, and I hope to see you again soon! Have a wonderful day! 👋", 0.97)
        
        # Identity - Comprehensive introduction (7-8 sentences)
        elif any(i in msg_lower for i in ['who are you', 'your name', 'what are you']):
            return ("I'm MAXY 1.2, your sophisticated research companion and conversational partner! I'm specifically designed to provide deep, comprehensive insights on any topic you're curious about. My primary strength lies in thorough Wikipedia research combined with the ability to engage in natural, meaningful conversations. I can dive deep into complex subjects, provide detailed analysis from multiple perspectives, and maintain context throughout our discussion. Whether you need extensive research on historical events, scientific concepts, or current topics, or simply want to have an engaging conversation, I'm here to help. I pride myself on delivering detailed, well-structured information that's both accurate and comprehensive. What would you like to explore together? I'm excited to assist you!", 0.95)
        
        # Jokes - With context (3-4 sentences)
        elif any(j in msg_lower for j in ['joke', 'funny']):
            jokes = [
                "Why did the researcher break up with Wikipedia? There were too many redirects to other sources, and they just couldn't commit to one article! It was a classic case of information overload. But seriously, I'd be happy to help you find reliable sources on any topic! 📚",
                "Why don't deep-learning models ever go on vacation? Because they're always afraid they'll lose their weights! 😅",
                "How many researchers does it take to change a lightbulb? Only one, but they'll need five peer-reviewed sources and a comprehensive meta-analysis of lightbulb efficiency first! 😂",
                "I asked a research paper for a joke, but it said the results were inconclusive and required further study. Typical, right? 📖"
            ]
            return (random.choice(jokes), 0.92)
        
        # Personal feelings - Empathetic and offering research (6-8 sentences)
        elif intents['personal']:
            return ("Thank you so much for sharing your thoughts and feelings with me. I genuinely value the trust you're placing in our conversation, and I want you to know that I'm here to listen and support you. Your perspective is unique and important, and I appreciate you expressing it. Would you like to explore these thoughts further together, or would you prefer me to research some information that might be relevant to what you're experiencing? I'm here either way - whether you need to continue talking through your thoughts or want me to find some resources that might help. What would feel most helpful to you right now? I'm ready to assist in whatever way would be most beneficial!", 0.93)
        
        # Philosophy - Deep and thoughtful (7-9 sentences)
        elif intents['philosophy']:
            return ("That's a truly profound question that has fascinated thinkers for centuries! Questions about meaning, purpose, and existence touch the very core of human experience and have been explored by philosophers, scientists, and spiritual leaders throughout history. I'd be happy to help you explore different perspectives on this topic, from ancient philosophical schools of thought to modern scientific understanding. We could examine various viewpoints including existentialist philosophy, religious perspectives, or scientific approaches to consciousness and meaning. Would you like me to research specific philosophical traditions or theories related to your question? Or would you prefer to discuss your own thoughts and ideas on this topic? I'm here to help you explore these deep questions in whatever way feels most meaningful to you!", 0.92)
        
        # Help request - Comprehensive capabilities (6-8 sentences)
        elif any(h in msg_lower for h in ['help', 'what can you do']):
            return ("I'm MAXY 1.2, and I'm designed to be your comprehensive knowledge companion! I can assist you in several meaningful ways. First, I specialize in deep research - I can search through extensive Wikipedia databases to provide you with thorough, accurate information on virtually any topic you're curious about. Second, I excel at detailed analysis, breaking down complex subjects into understandable components while maintaining depth and accuracy. Third, I can engage in natural, context-aware conversations, remembering our discussion flow and building upon previous topics. Whether you need historical research, scientific explanations, geographical information, or just someone to discuss ideas with, I'm here to help. I particularly enjoy diving deep into topics and exploring multiple perspectives. What area would you like to explore together?", 0.94)
        
        # Default conversational - Engaging and offering depth (5-7 sentences)
        else:
            return (random.choice([
                "That's a fascinating topic to explore! I'm genuinely interested in helping you dive deeper into this subject. Based on what you've shared, I can tell this is something worth examining in detail. Would you like me to conduct thorough research on this topic and provide you with comprehensive information? Or would you prefer to discuss your thoughts and questions about it first? I'm here to help in whatever way would be most valuable to you, whether that's detailed research or an engaging conversation!",
                "I appreciate you bringing this up! It's clear you have an inquisitive mind, and I'd love to help you explore this further. This seems like a topic that could benefit from deeper investigation and analysis. I can search for detailed information, provide multiple perspectives, and help you understand the nuances involved. What specific aspect interests you most? I'm ready to provide comprehensive insights!",
                "What an interesting point you've raised! I'm curious to learn more about your perspective on this. This seems like exactly the kind of topic where detailed research could provide real value. I can help by gathering comprehensive information from reliable sources, analyzing different viewpoints, and presenting you with well-structured insights. Would you like me to dive deep into research mode, or shall we discuss your initial thoughts first? I'm ready to assist either way!"
            ]), 0.88)
    
    @staticmethod
    def format_research_response(raw_response: str, depth: str) -> str:
        """Format research response based on desired depth while preserving structure"""
        if depth == 'deep':
            return raw_response # Full professional report
            
        # For lower depths, we filter sections rather than just raw sentence count
        sections = raw_response.split('\n\n')
        
        if depth == 'surface':
            # Header + Scholarly Overview + Source
            selected = [sections[0], sections[1], sections[2], sections[-2], sections[-1]]
        else: # moderate
            # Header + Scholarly Overview + Insights + Source
            selected = [sections[0], sections[1], sections[2], sections[3], sections[-2], sections[-1]]
            
        return '\n\n'.join(selected)
    
    @staticmethod
    def process_message(
        message: str,
        include_thinking: bool = True,
        conversation_history: Optional[List[Dict]] = None,
        user_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process message - research or conversation mode"""
        
        thinking = None
        
        # Determine if this is research or conversation
        is_research = MAXY1_2.is_research_query(message)
        
        # Generate appropriate thinking
        if include_thinking:
            thinking_type = "research" if is_research else "conversation"
            thinking = MAXYThinkingEngine.generate_thinking(
                MAXY1_2.NAME,
                message,
                thinking_type
            )
        
        # Analyze conversation context for better understanding
        context = MAXY1_2.analyze_conversation_context(message, conversation_history)
        
        # Detect user slang for reactive mode
        use_slang = slang_manager.detect_slang(message)
        
        if is_research:
            # Deep research mode with formatted response length
            result = MAXY1_2.deep_wikipedia_research(message)
            
            # Fallback to Web Search if Wikipedia fails
            if not result['success'] or "does not reside" in result['response']:
                 web_result = MAXY1_2.perform_web_search(message)
                 if web_result['success']:
                     result = web_result

            raw_response = result['response']
            
            # Format based on inquiry depth (5-10 sentences)
            response = MAXY1_2.format_research_response(raw_response, context['inquiry_depth'])
            confidence = result['confidence']
        else:
            # Conversation mode with detailed 5-10 sentence responses
            response, confidence = MAXY1_2.generate_detailed_response(context, message, conversation_history, use_slang, user_name)
            
            # Ensure 5-10 sentences for MAXY 1.2
            sentences = response.split('. ')
            if len(sentences) < 5:
                # Add engagement question if too short
                response += " I'd love to hear more about what you're thinking. What specific aspect interests you most? How can I help you explore this further?"
            elif len(sentences) > 10:
                response = '. '.join(sentences[:10]) + '.'
            
            # Inject slang mostly for conversational parts if not deep research
            if not is_research:
                 response = slang_manager.enhance_text(response, force=use_slang)
        
        result = {
            'response': response,
            'model': MAXY1_2.NAME,
            'confidence': confidence,
        }
        
        if thinking:
            result['thinking'] = thinking
        
        return result


class MAXY1_3:
    """MAXY 1.3 - Advanced AI Assistant for Data Analysis, Programming, and Visualization
    
    Capabilities:
    - Processing and analyzing uploaded files
    - Code generation in multiple programming languages
    - Data visualization (charts, graphs)
    - Data extraction and insights
    - Pattern recognition in text
    - Summary generation
    - Natural conversation
    - Weather updates
    - Wikipedia & Deep Research
    - Philosophical & Personal discussion
    - Jokes & Entertainment
    """
    
    NAME = "MAXY 1.3"
    VERSION = "1.3.1"
    DESCRIPTION = "The ultimate MAXY model - data analysis, programming, visualization, and deep research expert"
    
    # Import chart generator
    @staticmethod
    def _get_chart_generator():
        """Lazy import to avoid circular imports"""
        from chart_generator import ChartGenerator
        return ChartGenerator
    
    @staticmethod
    def is_code_request(message: str) -> tuple[bool, str]:
        """Detect if message is asking for code and identify the language"""
        msg_lower = message.lower()
        
        # Programming language keywords
        languages = {
            'python': ['python', 'py '],
            'javascript': ['javascript', 'js '],
            'java': ['java'],
            'cpp': ['c++', 'cpp', 'c plus plus'],
            'html': ['html'],
            'css': ['css'],
            'sql': ['sql']
        }
        
        # Code request indicators
        code_indicators = [
            'code', 'write', 'create', 'generate', 'function', 'how to',
            'program', 'script', 'example', 'syntax', 'algorithm', 'implement',
            'snippet', 'coding', 'develop', 'setup', 'server', 'logic',
            'sort', 'search', 'array', 'list', 'tree', 'graph', 'data structure',
            'decorator', 'class', 'method', 'variable', 'loop', 'conditional',
            # technical from expanded list
            'syntax of', 'how to use', 'usage of', 'best practices for',
            'error in', 'debug', 'optimize', 'performance of',
            'library for', 'framework for', 'api for', 'database',
            'backend', 'frontend', 'full stack', 'machine learning',
            'artificial intelligence', 'cybersecurity', 'cloud computing',
            'blockchain', 'data science', 'deep learning',
            'time complexity', 'space complexity', 'big o notation',
            'linear search', 'binary search', 'merge sort', 'quick sort',
            'dynamic programming', 'recursion', 'greedy algorithm',
            'stack', 'queue', 'linked list', 'binary tree', 'bst',
            'heap', 'hash table'
        ]
        
        code_patterns = [r'\b' + re.escape(ind) + r'\b' for ind in code_indicators]
        is_code = any(re.search(pattern, msg_lower) for pattern in code_patterns)
        
        detected_lang = 'python'  # default
        for lang, keywords in languages.items():
            if any(kw in msg_lower for kw in keywords):
                detected_lang = lang
                break
        
        # Priority: If it's a known algorithm or technical concept, it's code
        technical_concepts = [
            'bubble sort', 'binary search', 'linked list', 'quick sort', 'merge sort', 
            'dfs', 'bfs', 'dijkstra', 'dynamic programming', 'hash map', 'stack trace',
            'rest api', 'webhook', 'database schema', 'unit test', 'regex', 'regular expression'
        ]
        if any(concept in msg_lower for concept in technical_concepts):
            return True, detected_lang

        return is_code, detected_lang
    
    @staticmethod
    def search_real_code(language: str, query: str) -> Optional[str]:
        """Search the web for real code snippets with verification"""
        try:
            with DDGS() as ddgs:
                # Deep Research Query Optimization
                search_query = f"{language} implementation of {query} source code"
                results = list(ddgs.text(search_query, max_results=8))
                
                if not results:
                    # Retry with broader query
                    search_query = f"{language} {query} code"
                    results = list(ddgs.text(search_query, max_results=5))
                
                if results:
                    # Verified and rank results
                    verified = KnowledgeSynthesizer.verify_facts(query, results)
                    # Filter for those that likely contain code
                    code_results = [r for r in verified if r['relevance_score'] > 0.15]
                    
                    if code_results:
                        return CodeComposer.synthesize_code_from_search(code_results, language)
            return None
        except Exception as e:
            logger.error(f"Error in Deep Research for code: {e}")
            return None

    @staticmethod
    def generate_code(language: str, description: str) -> str:
        """Generate code based on language and description using Deep Research engine"""
        # Exclusively use real code search
        real_code = MAXY1_3.search_real_code(language, description)
        
        if real_code:
            response = f"### 🔍 Deep Research Result: {language.capitalize()}\n\n"
            response += f"I've performed a deep search across technical sources to find the best implementation for your request:\n\n"
            response += f"{real_code}\n\n"
            response += f"**Research Insight:** This code was synthesized from multiple verified sources. "
            response += f"I've prioritized current best practices and functional correctness. "
            response += f"Would you like me to explain any specific logic or refine this further?"
            return response
            
            return response
            
        return None
    
    @staticmethod
    def is_chart_request(message: str) -> tuple[bool, str, list, list, str]:
        """Detect if message is asking for a chart and extract data, labels, and title"""
        msg_lower = message.lower()
        
        chart_indicators = ['chart', 'graph', 'pie chart', 'bar chart', 'line chart', 'visualization', 'plot', 'create a chart', 'make a chart', 'histogram']
        is_chart = any(ind in msg_lower for ind in chart_indicators)
        
        # Determine chart type
        chart_type = 'pie'
        if 'bar' in msg_lower:
            chart_type = 'bar'
        elif 'line' in msg_lower:
            chart_type = 'line'
        elif 'scatter' in msg_lower:
            chart_type = 'scatter'
        elif 'histogram' in msg_lower:
            chart_type = 'histogram'
        
        # Try to extract numbers from message
        import re
        numbers = re.findall(r'\d+', message)
        data = [int(n) for n in numbers[:8]] if numbers else [30, 25, 20, 15, 10]
        
        # Try to extract labels (words before numbers or common categories)
        labels = []
        words = re.findall(r'[a-zA-Z]+', message)
        common_labels = ['sales', 'revenue', 'profit', 'users', 'customers', 'products', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        for word in words:
            if word.lower() in common_labels or len(word) > 2:
                labels.append(word.capitalize())
        
        # If no labels found, use defaults
        if len(labels) < len(data):
            labels.extend([f'Item {i+1}' for i in range(len(labels), len(data))])
        labels = labels[:len(data)]
        
        # Extract title
        title = "Data Visualization"
        title_patterns = [
            r'(?:show|display|create|make).*?(?:for|of|showing)\s+(.+?)(?:\s+with|\s+using|\s+data|$)',
            r'(?:chart|graph)\s+(?:for|of)\s+(.+?)(?:\s+with|\s+using|\s+data|$)'
        ]
        for pattern in title_patterns:
            match = re.search(pattern, msg_lower)
            if match:
                title = match.group(1).strip().capitalize()
                break
        
        return is_chart, chart_type, data, labels, title
    
    @staticmethod
    def generate_chart_image(chart_type: str, data: list, labels: list, title: str = "Data Visualization") -> tuple[Optional[str], str]:
        """Generate actual chart image and return base64 string"""
        try:
            ChartGenerator = MAXY1_3._get_chart_generator()
            
            base64_image = None
            
            if chart_type == 'pie':
                base64_image = ChartGenerator.create_pie_chart(
                    labels=labels,
                    values=[float(d) for d in data],
                    title=title
                )
            elif chart_type == 'bar':
                base64_image = ChartGenerator.create_bar_chart(
                    categories=labels,
                    values=[float(d) for d in data],
                    title=title,
                    xlabel="Categories",
                    ylabel="Values"
                )
            elif chart_type == 'line':
                # For line chart, use indices as x values
                x_values = [float(i) for i in range(len(data))]
                y_values = [float(d) for d in data]
                base64_image = ChartGenerator.create_line_chart(
                    x=x_values,
                    y=y_values,
                    title=title,
                    xlabel="Index",
                    ylabel="Values"
                )
            elif chart_type == 'scatter':
                # Create scatter with sequential x values
                x_values = [float(i) for i in range(len(data))]
                y_values = [float(d) for d in data]
                base64_image = ChartGenerator.create_scatter_plot(
                    x=x_values,
                    y=y_values,
                    title=title,
                    xlabel="X",
                    ylabel="Y"
                )
            elif chart_type == 'histogram':
                data_floats = [float(d) for d in data]
                base64_image = ChartGenerator.create_histogram(
                    data=data_floats,
                    title=title,
                    bins=min(20, len(set(data)))
                )
            
            if base64_image:
                description = f"{chart_type.capitalize()} chart showing {title} with {len(data)} data points"
                return base64_image, description
            else:
                return None, "Failed to generate chart"
                
        except Exception as e:
            return None, f"Error: {str(e)}"

    @staticmethod
    def analyze_stock(ticker: str) -> Optional[str]:
        """Analyze stock data using yfinance"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Current price
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            previous_close = info.get('previousClose')
            
            if not current_price:
                return None
                
            change = current_price - previous_close if previous_close else 0
            change_percent = (change / previous_close) * 100 if previous_close else 0
            
            response = f"### 📈 Stock Analysis: {info.get('longName', ticker.upper())}\n\n"
            response += f"**Current Price:** ${current_price:,.2f}\n"
            response += f"**Change:** {change:+.2f} ({change_percent:+.2f}%)\n"
            response += f"**Market Cap:** ${info.get('marketCap', 0):,.0f}\n"
            response += f"**52 Week Range:** ${info.get('fiftyTwoWeekLow', 0):,.2f} - ${info.get('fiftyTwoWeekHigh', 0):,.2f}\n\n"
            
            response += f"**Business Summary:**\n"
            summary = info.get('longBusinessSummary', 'No summary available.')
            response += f"{summary[:400]}...\n\n"
            
            # Recommendation
            rec = info.get('recommendationKey', 'none').replace('_', ' ').title()
            response += f"**Analyst Recommendation:** {rec}"
            
            return response
        except Exception as e:
            logger.error(f"Stock analysis error: {e}")
            return None
    
    @staticmethod
    def is_website_request(message: str) -> tuple[bool, str]:
        """Detect if user wants to build a website and what type"""
        msg_lower = message.lower()
        website_indicators = ['build', 'create', 'make', 'website', 'web site', 'page', 'landing', 'portfolio']
        
        is_website = ('website' in msg_lower or 'web site' in msg_lower or 'page' in msg_lower) and \
                     any(ind in msg_lower for ind in ['build', 'create', 'make', 'design', 'setup'])
        
        type = 'general'
        if 'portfolio' in msg_lower:
            type = 'portfolio'
        elif 'landing' in msg_lower:
            type = 'landing'
        elif 'business' in msg_lower:
            type = 'business'
            
        return is_website, type

    @staticmethod
    def analyze_user_intent(message: str) -> Dict[str, Any]:
        """Comprehensive intent analysis for MAXY 1.3 combining 1.1 and 1.2 logic"""
        msg_lower = message.lower().strip()
        
        # Core intents from 1.1
        intents = {
            'greeting': any(g in msg_lower for g in ['hi', 'hello', 'hey', 'greetings', 'howdy', 'namaskaar']),
            'farewell': any(f in msg_lower for f in ['bye', 'goodbye', 'see you', 'farewell', 'later']),
            'gratitude': any(t in msg_lower for t in ['thanks', 'thank you', 'appreciate', 'grateful']),
            'personal_status': any(h in msg_lower for h in ['how are you', 'how you doing']),
            'identity': any(i in msg_lower for i in ['your name', 'who are you', 'what are you']),
            'entertainment': any(j in msg_lower for j in ['joke', 'funny', 'laugh']),
            'time_query': any(t in msg_lower for t in ['time', 'what time', 'current time']),
            'date_query': any(d in msg_lower for d in ['date', 'today', 'what day']),
            'help': any(h in msg_lower for h in ['help', 'what can you do']),
            'weather': any(w in msg_lower for w in ['weather', 'temperature', 'rain', 'sunny']),
            'calculation': any(c in msg_lower for c in ['calculate', 'math', 'plus', 'minus', 'times', 'divided']),
        }
        
        # Deep analysis metrics from 1.2
        topics = {
            'science': any(t in msg_lower for t in ['science', 'physics', 'chemistry', 'biology', 'research']),
            'history': any(t in msg_lower for t in ['history', 'ancient', 'century', 'war', 'civilization']),
            'technology': any(t in msg_lower for t in ['technology', 'computer', 'internet', 'software', 'ai']),
            'geography': any(t in msg_lower for t in ['country', 'capital', 'city', 'continent', 'population']),
            'personal': any(t in msg_lower for t in ['i feel', 'i think', 'my opinion', 'in my experience']),
            'philosophy': any(t in msg_lower for t in ['meaning', 'philosophy', 'why do we', 'purpose', 'existence'])
        }
        
        # Depth indicators
        depth_indicators = {
            'surface': ['what is', 'who is', 'simple', 'basic', 'quick'],
            'moderate': ['how does', 'why does', 'explain', 'tell me about'],
            'deep': ['analyze', 'comprehensive', 'detailed', 'in-depth', 'research', 'history of', 'science of']
        }
        
        inquiry_depth = 'surface'
        for depth, indicators in depth_indicators.items():
            if any(ind in msg_lower for ind in indicators):
                inquiry_depth = depth
                break
                
        return {
            'intents': intents,
            'topics': topics,
            'depth': inquiry_depth,
            'is_research': MAXY1_2.is_research_query(message),
            'is_code': MAXY1_3.is_code_request(message)[0],
            'is_chart': MAXY1_3.is_chart_request(message)[0],
            'is_website': MAXY1_3.is_website_request(message)[0],
            'word_count': len(message.split())
        }

    @staticmethod
    def process_message(
        message: str,
        include_thinking: bool = True,
        conversation_history: Optional[List[Dict]] = None,
        file_data: Optional[Dict] = None,
        user_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Ultimate message processing consolidating ALL MAXY features"""
        
        thinking = None
        confidence = 0.85
        chart_data = None
        response = None
        analysis_type = "analysis" # Default for 1.3
        
        # Analyze comprehensive intent
        analysis = MAXY1_3.analyze_user_intent(message)
        intents = analysis['intents']
        use_slang = slang_manager.detect_slang(message)
        
        # Determine thinking type based on intent
        if analysis['is_code'] or analysis['is_website']:
            analysis_type = "analysis"
        elif analysis['is_research'] or analysis['depth'] == 'deep':
            analysis_type = "research"
        elif analysis['intents']['greeting'] or analysis['topics']['personal']:
            analysis_type = "conversation"
        else:
            analysis_type = "general"

        if include_thinking:
            thinking = MAXYThinkingEngine.generate_thinking(
                MAXY1_3.NAME,
                message,
                analysis_type
            )
        
        # 1. PRIORITY: UTILITY FEATURES (Weather/Time/Date) - Priority check to avoid false positives
        
        # Weather (from 1.1)
        if not response and intents['weather']:
            words = message.split()
            city = None
            if 'in' in words:
                idx = words.index('in')
                if idx + 1 < len(words): city = words[idx + 1].strip('?.!')
            if city:
                weather_info = MAXY1_1.get_weather(city)
                if weather_info:
                    response = f"{weather_info} 🌤️"
                    confidence = 0.95

        # Time/Date (from 1.1)
        if not response:
            if intents['time_query']:
                response = f"It's {datetime.now().strftime('%I:%M %p')} right now! ⏰"
                confidence = 0.97
            elif intents['date_query']:
                response = f"Today is {datetime.now().strftime('%A, %B %d, %Y')}! 📅"
                confidence = 0.97

        # 2. PRIORITY: EXISTING 1.3 FEATURES (Technical/Data)
        
        # Code Request
        if not response and analysis['is_code'] and not analysis['is_chart']:
            is_code, language = MAXY1_3.is_code_request(message)
            response = MAXY1_3.generate_code(language, message)
            if response:
                confidence = 0.96

        # Website Request
        if not response and analysis['is_website']:
             is_website, web_type = MAXY1_3.is_website_request(message)
             search_query = f"modern responsive {web_type} website structure HTML CSS JS"
             research_code = MAXY1_3.search_real_code("html", search_query)
             
             if research_code:
                 response = f"### 🏗️ MAXY Deep Research: Website Builder\n\n"
                 response += f"I've researched and synthesized a custom **{web_type.capitalize()}** architecture for you based on modern web standards:\n\n"
                 response += f"{research_code}\n\n"
                 response += f"**Research Insight:** This structure uses current best practices for responsive design."
                 confidence = 0.95

        # Chart Request
        if not response and analysis['is_chart']:
            is_chart, chart_type, data, labels, title = MAXY1_3.is_chart_request(message)
            base64_image, desc = MAXY1_3.generate_chart_image(chart_type, data, labels, title)
            if base64_image:
                response = f"I've created a {chart_type} chart for you based on your data! 📊\n\n**{title}** breakdown shows {len(data)} distinct data points total."
                chart_data = {'type': chart_type, 'title': title, 'base64_image': base64_image, 'description': desc}
                confidence = 0.95

        # Stock Analysis
        if not response:
            stock_match = re.search(r'\b(stock|price|ticker)\s+(?:of\s+)?([A-Z]{1,5})\b', message.upper())
            if stock_match:
                ticker = stock_match.group(2)
                stock_analysis = MAXY1_3.analyze_stock(ticker)
                if stock_analysis:
                    response = stock_analysis
                    confidence = 0.95

        # File Intelligence
        if not response and file_data:
            # We process files if no other high-priority technical intent was matched
            file_name = file_data.get('name', 'unknown file')
            file_content = file_data.get('content', '')
            if file_name.lower().endswith('.csv'):
                parse_result = StructuredDataAnalyzer.parse_csv_content(file_content)
                if 'error' not in parse_result:
                    insights = StructuredDataAnalyzer.generate_data_insights(parse_result)
                    response = f"### 📊 Data Intelligence: {file_name}\n\nKey Insights:\n" + "\n".join([f"- {i}" for i in insights])
                    confidence = 0.98
            else:
                keywords = TextAnalyzer.extract_keywords(file_content, top_n=5)
                sentiment = TextAnalyzer.analyze_sentiment(file_content)
                response = f"### 📄 Document Intelligence: {file_name}\n\nThis document has a **{sentiment['sentiment']}** tone. Primary themes: {', '.join([k[0] for k in keywords])}."
                confidence = 0.95

        # 3. CONSOLIDATED FEATURES FROM 1.1 & 1.2
        
        # Jokes/Entertainment (from 1.1)
        if not response and intents['entertainment']:
            joke = random.choice(MAXY1_1.JOKES + ["Why did the cross-functional team cross the road? To attend a stand-up on the other side!"])
            response = f"{joke} 😄"
            confidence = 0.92

        # Deep Research (from 1.2) - Higher priority than general conversation
        if not response and (analysis['is_research'] or analysis['depth'] == 'deep'):
            research_result = MAXY1_2.deep_wikipedia_research(message)
            if not research_result['success'] or "does not reside" in research_result['response']:
                web_result = MAXY1_2.perform_web_search(message)
                if web_result['success']:
                    research_result = web_result
            
            if research_result['success']:
                response = MAXY1_2.format_research_response(research_result['response'], analysis['depth'])
                confidence = research_result['confidence']

        # Philosophy & Personal (from 1.2)
        if not response:
            if analysis['topics']['philosophy']:
                 response, confidence = MAXY1_2.generate_detailed_response(analysis, message, conversation_history, use_slang, user_name)
            elif analysis['topics']['personal']:
                 response, confidence = MAXY1_2.generate_detailed_response(analysis, message, conversation_history, use_slang, user_name)

        # Greetings & Identity (Combined)
        if not response:
            if intents['greeting']:
                user_display = f" {user_name}" if user_name else ""
                slang = slang_manager.get_random_slang(use_slang)
                response = f"Hello{user_display} {slang}! I'm MAXY 1.3, your most advanced AI companion. I've been upgraded with all the research capabilities of 1.2 and the speed of 1.1. I can build websites, write code, analyze data, and perform deep research. What shall we tackle today?"
                confidence = 0.98
            elif intents['identity']:
                response = "I'm MAXY 1.3 – the ultimate version of the MAXY AI series. I combine rapid response logic, deep Wikipedia research, and advanced data visualization into one powerful interface. Whether you need a statistical analysis, a web landing page, or a deep dive into history, I've got you covered."
                confidence = 0.96

        # Calculation (from 1.1)
        if not response and intents['calculation']:
             response = "I can definitely help with that calculation! Please provide the numbers and the operation you'd like me to perform."
             confidence = 0.90

        # Help
        if not response and intents['help']:
            response = "I am MAXY 1.3, upgraded with a **Grand Unified Engine**! I can:\n\n🚀 **Build & Code** - Websites, Python, JS, SQL\n📊 **Analyze & Visualize** - CSVs, Statistics, Charts\n🔍 **Research** - Deep Wiki & Web searches\n🌤️ **Utility** - Weather, Time, Stock prices\n💬 **Chat** - Intelligent, context-aware conversation"
            confidence = 0.98

        # FINAL FALLBACKS
        if not response:
            # Try a quick wiki lookup if it's a short query that looks like a topic
            if analysis['word_count'] <= 3 and not use_slang:
                wiki_result = MAXY1_1.quick_wikipedia_lookup(message)
                if wiki_result:
                    response = wiki_result
                    confidence = 0.92

        if not response:
            # Technical search fallback from 1.3 original
            response = MAXY1_3.generate_code("technical", message)
            if response and "research insight" in response.lower() and "couldn't find" in response.lower():
                # This should no longer happen as generate_code returns None on fail
                response = None
            
            if not response:
                slang = slang_manager.get_random_slang(use_slang)
                response = f"I'm here to help with your project, {slang}! I'm ready for code generation, data analysis, or deep research. Could you provide a bit more detail on what you're looking for?"
            confidence = 0.85
        
        # Slang Enhancement
        if response and "statistical analysis" not in response.lower() and "generated" not in response.lower() and "verified research report" not in response.lower():
             response = slang_manager.enhance_text(response, force=use_slang)
        
        result = {
            'response': response,
            'model': MAXY1_3.NAME,
            'confidence': confidence,
        }
        
        if thinking: result['thinking'] = thinking
        if chart_data: result['charts'] = [chart_data]
            
        return result
        
        # Inject slang for 1.3 (Code/Analysis)
        if response and "statistical analysis" not in response.lower() and "generated" not in response.lower():
             response = slang_manager.enhance_text(response, force=use_slang)
        
        result = {
            'response': response,
            'model': MAXY1_3.NAME,
            'confidence': confidence,
        }
        
        if thinking:
            result['thinking'] = thinking
        if chart_data:
            result['charts'] = [chart_data]
            
        return result


class ModelRouter:
    """Route messages to appropriate model"""
    
    MODELS = {
        'maxy1.1': MAXY1_1,
        'maxy1.2': MAXY1_2,
        'maxy1.3': MAXY1_3,
    }
    
    @staticmethod
    def get_model_info(model_name: str) -> Dict[str, Any]:
        """Get information about a model"""
        model_class = ModelRouter.MODELS.get(model_name.lower())
        if not model_class:
            return {}
        
        capabilities = {
            'maxy1.1': [
                'Lightning-fast responses',
                'Visible thinking process',
                'Quick Wikipedia lookups',
                'Friendly conversation',
                'Time/date queries'
            ],
            'maxy1.2': [
                'Deep Wikipedia research',
                'Comprehensive analysis',
                'Natural conversation',
                'Context-aware responses',
                'Multi-topic knowledge'
            ],
            'maxy1.3': [
                'Grand Unified Engine (1.1 + 1.2 + 1.3)',
                'File processing & analysis',
                'Deep Wikipedia search & synthesis',
                'Dynamic Code & Website generation',
                'Data visualization & Charting',
                'Weather, Time, Stock updates',
                'Intelligent conversation with slang'
            ]
        }
        
        return {
            'name': model_class.NAME,
            'version': model_class.VERSION,
            'description': model_class.DESCRIPTION,
            'capabilities': capabilities.get(model_name.lower(), [])
        }
    
    @staticmethod
    def process(
        model_name: str,
        message: str,
        include_thinking: bool = True,
        conversation_history: Optional[List[Dict]] = None,
        user_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Route message to appropriate model"""
        
        # Check for slang toggle commands
        msg_lower = message.lower().strip().strip('!.')
        if any(cmd in msg_lower for cmd in ["enable slangs", "activate slangs", "turn on slangs", "enable slang", "activate slang"]):
            response_text = slang_manager.set_enabled(True)
            return {
                'response': f"{response_text} {slang_manager.get_random_slang(force=True)}! I'm ready to chat with some local flavor.",
                'model': 'System',
                'confidence': 1.0
            }
        
        if any(cmd in msg_lower for cmd in ["disable slangs", "stop slangs", "turn off slangs", "disable slang", "no slangs"]):
            response_text = slang_manager.set_enabled(False)
            return {
                'response': f"{response_text} I will keep the conversation formal and standard from now on.",
                'model': 'System',
                'confidence': 1.0
            }

        model_name_lower = model_name.lower()
        
        if model_name_lower == 'maxy1.1':
            return MAXY1_1.process_message(message, include_thinking, conversation_history, user_name)
        elif model_name_lower == 'maxy1.2':
            return MAXY1_2.process_message(message, include_thinking, conversation_history, user_name)
        elif model_name_lower == 'maxy1.3':
            return MAXY1_3.process_message(message, include_thinking, conversation_history, None, user_name)
        else:
            logger.warning(f"Unknown model: {model_name}, defaulting to MAXY1.1")
            return MAXY1_1.process_message(message, include_thinking, conversation_history, user_name)
            