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
from data_analyzer import AdvancedAnalyzer
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
        
        return thinking_text


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
            'what are', 'define', 'describe', 'history of', 'science',
            'technology', 'biology', 'physics', 'chemistry', 'geography',
            'country', 'capital', 'famous', 'invented', 'discovered',
            'when did', 'where is', 'why does'
        ]
        msg_lower = message.lower()
        return any(kw in msg_lower for kw in research_keywords) and len(message) < 200
    
    @staticmethod
    def quick_wikipedia_lookup(query: str) -> Optional[str]:
        """Quick Wikipedia lookup for maxy1.1 with DDG fallback"""
        try:
            # 1. Try Wikipedia first
            search_results = wikipedia.search(query, results=1)
            if search_results:
                page = wikipedia.page(search_results[0], auto_suggest=False)
                summary = page.summary[:500]
                return summary
            
            # 2. Fallback to DuckDuckGo
            with DDGS() as ddgs:
                 # Use ddgs.text() and get the first result
                 results = list(ddgs.text(query, max_results=1))
                 if results:
                     return results[0]['body']
            
            return None
        except Exception as e:
            # If Wikipedia fails, also try DDG
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=1))
                    if results:
                        return results[0]['body']
            except:
                pass
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
            'knowledge': any(k in msg_lower for k in ['what is', 'who is', 'how does', 'explain', 'tell me about']),
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
    def generate_concise_response(intent_analysis: Dict[str, Any], message: str, use_slang: bool = False) -> tuple[str, float]:
        """Generate 3-4 sentence response based on intent"""
        intents = intent_analysis['intents']
        msg_lower = message.lower().strip()
        
        # Greeting - Friendly and welcoming (3-4 sentences)
        if intents['greeting']:
            if intent_analysis.get('is_new_user', False):
                return (f"Hey {slang_manager.get_random_slang(use_slang)}! Welcome! I'm MAXY 1.1, your quick AI assistant. I'm here to help with fast answers and friendly chat. What can I do for you today?", 0.98)
            else:
                return (f"Hey {slang_manager.get_random_slang(use_slang)}! Great to see you again! Ready when you are. What's on your mind today?", 0.97)
        
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
        
        # Knowledge query - Quick facts (prioritized over simple task)
        elif intents['knowledge'] or MAXY1_1.should_use_wikipedia(message):
            wiki_result = MAXY1_1.quick_wikipedia_lookup(message)
            if wiki_result:
                # Strictly 2-3 sentences as requested
                raw_sentences = [s.strip() for s in wiki_result.split('. ') if s.strip()]
                sentences = raw_sentences[:3] # Ensure at most 3 sentences
                concise = '. '.join(sentences)
                if not concise.endswith('.'):
                    concise += '.'
                return (concise, 0.90)
            else:
                # If lookup fails, fall back to a generic but helpful response
                return ("I tried to look that up but couldn't find a quick answer. I'd love to help though! Could you be more specific about what you'd like to know?", 0.82)

        # Simple task acknowledgment (2-3 sentences)
        elif intents['simple_task']:
            # First try to see if it's a topic we can look up (double check)
            wiki_result = MAXY1_1.quick_wikipedia_lookup(message)
            if wiki_result:
                raw_sentences = [s.strip() for s in wiki_result.split('. ') if s.strip()]
                sentences = raw_sentences[:3]
                concise = '. '.join(sentences)
                if not concise.endswith('.'):
                    concise += '.'
                return (concise, 0.90)
                
            return ("Got it! I'm on it. What would you like me to do with this? Just let me know the next step!", 0.88)
        
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
        conversation_history: Optional[List[Dict]] = None
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
        response, confidence = MAXY1_1.generate_concise_response(intent_analysis, message, use_slang)
        
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
            'history of', 'science of', 'how does', 'why does', 'information about',
            'learn about', 'tell me more about', 'details about', 'wikipedia',
            'discovered', 'invented', 'founded', 'created by', 'origin of',
            'biology', 'chemistry', 'physics', 'astronomy', 'geography',
            'country', 'capital', 'population', 'famous for'
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
        """Perform comprehensive Wikipedia research with professional synthesis"""
        try:
            # Search for relevant pages
            search_results = wikipedia.search(query, results=5)
            
            if not search_results:
                return {
                    'success': False,
                    'response': (
                        f"**RESEARCH INQUIRY: '{query}'**\n"
                        f"{'='*50}\n\n"
                        f"Our primary knowledge indices currently contain no direct correlation for this specific inquiry.\n\n"
                        f"**Recommendations for Refined Synthesis:**\n"
                        f"• Employ expanded conceptual terminologies\n"
                        f"• Increase categorical specificity\n"
                        f"• Verify orthographic accuracy\n"
                        f"• Establish a broader foundational query"
                    ),
                    'confidence': 0.60
                }
            
            # Try to get the main page
            try:
                page = wikipedia.page(search_results[0], auto_suggest=False)
            except wikipedia.exceptions.DisambiguationError as e:
                best_option = e.options[0] if e.options else search_results[0]
                page = wikipedia.page(best_option, auto_suggest=False)
            
            title = page.title
            summary = page.summary
            url = page.url
            
            # Professional Synthesis Logic
            paragraphs = [p.strip() for p in summary.split('\n\n') if len(p.strip()) > 100]
            if not paragraphs:
                paragraphs = [summary]
                
            # 1. Scholarly Overview (First para refined)
            intro = paragraphs[0]
            if len(intro) > 600:
                intro = intro[:600] + "..."
            
            # 2. Critical Insights & Thematic Analysis
            # Extract key sentences for bullet points
            all_sentences = [s.strip() for s in summary.split('. ') if len(s.strip()) > 20]
            insights = all_sentences[2:7] # Take some middle sentences for "insights"
            
            # 3. Technical Narrative (Main body)
            narrative = " ".join(paragraphs[1:3]) if len(paragraphs) > 1 else summary[600:2000]
            if len(narrative) > 1200:
                narrative = narrative[:1200] + "..."
                
            # 4. Academic Conclusion
            conclusion = f"In summary, the study of {title} reveals a multifaceted landscape across its historical and practical dimensions. Understanding its core principles remains essential for comprehensive mastery of the subject matter."

            # Build Professional Report
            response = f"**DEEP RESEARCH REPORT: {title.upper()}**\n"
            response += f"{'='*60}\n\n"
            
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
            response += f"🔍 Associated Domains: {', '.join(search_results[1:4])}"
            
            return {
                'success': True,
                'response': response,
                'confidence': 0.95,
                'sources': [url]
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
    def generate_detailed_response(context: Dict[str, Any], message: str, conversation_history: Optional[List[Dict]] = None, use_slang: bool = False) -> tuple[str, float]:
        """Generate detailed 5-10 sentence response based on context"""
        msg_lower = message.lower().strip()
        intents = context['topics']
        depth = context['inquiry_depth']
        complexity = context['complexity']
        
        # Greeting - Warm and contextual (6-8 sentences)
        if any(g in msg_lower for g in ['hi', 'hello', 'hey', 'greetings']):
            if context.get('is_follow_up'):
                return (f"Hello again {slang_manager.get_random_slang(use_slang)}! It's wonderful to continue our conversation. I've been thinking about our previous discussion and I'm ready to dive deeper into any topic you'd like to explore. Whether you need comprehensive research on a specific subject or just want to have an engaging conversation, I'm here to provide detailed insights. What direction would you like to take our discussion today? I'm particularly excited to help with any research questions or analytical topics you might have in mind!", 0.97)
            else:
                return (f"Namaskara! I'm MAXY 1.2, your dedicated research and conversation companion. I'm genuinely excited to help you explore whatever topics interest you today. Whether you're looking for in-depth Wikipedia research, detailed analysis of complex subjects, or simply an engaging conversation, I'm fully equipped to assist. I specialize in providing comprehensive information with multiple perspectives and thorough context. What would you like to dive into, {slang_manager.get_random_slang(use_slang)}? I'm ready to provide detailed, well-researched responses!", 0.96)
        
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
                "What do you call a scientist who loves to dance? A step-researcher! They really know how to move through the data. I'd love to help you find information that's equally engaging and informative! 🎵",
                "Why don't scientists trust atoms? Because they make up everything - literally! And I've thoroughly researched this claim. Speaking of research, is there a topic you'd like me to investigate for you? ⚛️"
            ]
            return (random.choice(jokes), 0.91)
        
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
        conversation_history: Optional[List[Dict]] = None
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
            response, confidence = MAXY1_2.generate_detailed_response(context, message, conversation_history, use_slang)
            
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
    """
    
    NAME = "MAXY 1.3"
    VERSION = "1.3.0"
    DESCRIPTION = "Advanced AI assistant for data analysis, programming, and visualization"
    
    # Import chart generator
    @staticmethod
    def _get_chart_generator():
        """Lazy import to avoid circular imports"""
        from chart_generator import ChartGenerator
        return ChartGenerator
    
    # Programming language templates
    CODE_TEMPLATES = {
        'python': {
            'greeting': 'print("Hello, World!")',
            'function': '''def greet(name):
    """Greet a person by name"""
    return f"Hello, {name}!"

# Example usage
result = greet("User")
print(result)''',
            'loop': '''# Loop through items
items = [1, 2, 3, 4, 5]
for item in items:
    print(f"Item: {item}")'''
        },
        'javascript': {
            'greeting': 'console.log("Hello, World!");',
            'function': '''function greet(name) {
    // Greet a person by name
    return `Hello, ${name}!`;
}

// Example usage
const result = greet("User");
console.log(result);''',
            'loop': '''// Loop through items
const items = [1, 2, 3, 4, 5];
items.forEach(item => {
    console.log(`Item: ${item}`);
});'''
        },
        'java': {
            'greeting': 'System.out.println("Hello, World!");',
            'function': '''public class Greeting {
    public static String greet(String name) {
        // Greet a person by name
        return "Hello, " + name + "!";
    }
    
    public static void main(String[] args) {
        // Example usage
        String result = greet("User");
        System.out.println(result);
    }
}''',
            'loop': '''// Loop through items
int[] items = {1, 2, 3, 4, 5};
for (int item : items) {
    System.out.println("Item: " + item);
}'''
        },
        'cpp': {
            'greeting': 'std::cout << "Hello, World!" << std::endl;',
            'function': '''#include <iostream>
#include <string>

std::string greet(const std::string& name) {
    // Greet a person by name
    return "Hello, " + name + "!";
}

int main() {
    // Example usage
    std::string result = greet("User");
    std::cout << result << std::endl;
    return 0;
}''',
            'loop': '''// Loop through items
int items[] = {1, 2, 3, 4, 5};
for (int item : items) {
    std::cout << "Item: " << item << std::endl;
}'''
        },
        'html': {
            'greeting': '''<!DOCTYPE html>
<html>
<head>
    <title>Greeting</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>''',
            'function': '''<!DOCTYPE html>
<html>
<head>
    <title>Greeting App</title>
</head>
<body>
    <input type="text" id="nameInput" placeholder="Enter your name">
    <button onclick="greet()">Greet</button>
    <p id="result"></p>
    
    <script>
        function greet() {
            const name = document.getElementById('nameInput').value;
            document.getElementById('result').innerText = `Hello, ${name}!`;
        }
    </script>
</body>
</html>'''
        },
        'css': {
            'greeting': '''body {
    font-family: Arial, sans-serif;
    text-align: center;
    padding: 50px;
}

h1 {
    color: #333;
}''',
            'function': '''.greeting-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.greeting-card h1 {
    margin: 0;
    font-size: 2em;
}'''
        },
        'sql': {
            'greeting': '-- SQL Greeting\nSELECT "Hello, World!" AS greeting;',
            'function': '''-- Create a function to greet users
CREATE FUNCTION greet_user(user_name VARCHAR(50))
RETURNS VARCHAR(100)
DETERMINISTIC
BEGIN
    RETURN CONCAT("Hello, ", user_name, "!");
END;

-- Example usage
SELECT greet_user("User") AS greeting;''',
            'loop': '''-- Loop through items using a cursor
DECLARE @item INT;
DECLARE item_cursor CURSOR FOR SELECT number FROM numbers;

OPEN item_cursor;
FETCH NEXT FROM item_cursor INTO @item;

WHILE @@FETCH_STATUS = 0
BEGIN
    PRINT "Item: " + CAST(@item AS VARCHAR);
    FETCH NEXT FROM item_cursor INTO @item;
END;

CLOSE item_cursor;
DEALLOCATE item_cursor;'''
        }
    }
    
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
            'code', 'write', 'create', 'generate', 'function',
            'program', 'script', 'example', 'syntax', 'algorithm'
        ]
        
        is_code = any(ind in msg_lower for ind in code_indicators)
        
        detected_lang = 'python'  # default
        for lang, keywords in languages.items():
            if any(kw in msg_lower for kw in keywords):
                detected_lang = lang
                break
        
        return is_code, detected_lang
    
    @staticmethod
    def generate_code(language: str, description: str) -> str:
        """Generate code based on language and description"""
        templates = MAXY1_3.CODE_TEMPLATES.get(language, MAXY1_3.CODE_TEMPLATES['python'])
        
        desc_lower = description.lower()
        
        # Select appropriate template
        if any(word in desc_lower for word in ['function', 'method', 'def']):
            template = templates['function']
        elif any(word in desc_lower for word in ['loop', 'iterate', 'for', 'while']):
            template = templates['loop']
        else:
            template = templates['greeting']
        
        code = f"```{language}\n{template}\n```"
        
        response = f"Here's a {language} example for you:\n\n{code}\n\n"
        response += f"**What this code does:**\n"
        response += f"This is a simple {language} example that demonstrates basic syntax. "
        response += f"You can modify it to suit your specific needs. "
        response += f"Would you like me to explain any part of this code or create something more specific?"
        
        return response
    
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
    def process_message(
        message: str,
        include_thinking: bool = True,
        conversation_history: Optional[List[Dict]] = None,
        file_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Process message with AI capabilities including dynamic code and website generation"""
        
        thinking = None
        confidence = 0.85
        chart_data = None
        
        if include_thinking:
            thinking = MAXYThinkingEngine.generate_thinking(
                MAXY1_3.NAME,
                message,
                "analysis"
            )
        
        # Detect slang usage
        use_slang = slang_manager.detect_slang(message)
        
        msg_lower = message.lower().strip()
        response = None
        
        # 1. Check for Website Building Request (NEW Logic)
        is_website, web_type = MAXY1_3.is_website_request(message)
        if is_website:
            if web_type == 'portfolio':
                site = CodeComposer.build_portfolio()
                type_name = "Portfolio Website"
            else:
                site = CodeComposer.build_website(title="Project MAXY Site")
                type_name = "Landing Page"
                
            response = f"### 🏗️ MAXY Website Builder\n\n"
            response += f"I've generated a clean, responsive **{type_name}** structure for you! "
            response += f"I've used modern HTML5, CSS Flexbox/Grid, and added some smooth interactivity with JavaScript.\n\n"
            
            response += f"#### 📄 HTML Structure\n```html\n{site['html'][:1000]}...\n```\n\n"
            response += f"#### 🎨 CSS Styles\n```css\n{site['css'][:500]}...\n```\n\n"
            response += f"#### ⚡ JavaScript Logic\n```javascript\n{site['js']}\n```\n\n"
            
            response += f"**How to use this:**\n"
            response += f"1. Save the HTML as `index.html`.\n"
            response += f"2. Save the CSS as `style.css`.\n"
            response += f"3. Save the JS as `script.js`.\n"
            response += f"4. Open `index.html` in your browser to see your new site!"
            
            confidence = 0.95
            
        # 2. Check for chart request (Prioritized over code/analysis)
        if not response and MAXY1_3.is_chart_request(message)[0]:
            is_chart, chart_type, data, labels, title = MAXY1_3.is_chart_request(message)
            base64_image, description = MAXY1_3.generate_chart_image(chart_type, data, labels, title)
            
            if base64_image:
                response = f"I've created a {chart_type} chart for you based on your data! 📊\n\n"
                response += f"**{title}** breakdown shows {len(data)} distinct data points total. "
                response += f"The visual representation above should make the distribution clear."
                chart_data = {'type': chart_type, 'title': title, 'base64_image': base64_image, 'description': description}
                confidence = 0.95
            
        # 3. Check for code generation request (Upgraded)
        if not response and MAXY1_3.is_code_request(message)[0]:
             # Double check it's not a misclassified chart request
             if "chart" not in message.lower() and "plot" not in message.lower():
                language = MAXY1_3.is_code_request(message)[1]
                response = MAXY1_3.generate_code(language, message)
                confidence = 0.93

        # 5. Check for Stock Analysis (NEW Logic)
        if not response:
            stock_match = re.search(r'\b(stock|price|ticker)\s+(?:of\s+)?([A-Z]{1,5})\b', message.upper())
            if stock_match:
                ticker = stock_match.group(2)
                stock_analysis = MAXY1_3.analyze_stock(ticker)
                if stock_analysis:
                    response = stock_analysis
                    confidence = 0.95

        # Fallback to original logic if no response generated yet
        if not response:
            # Detect numeric data for analysis
            numbers = re.findall(r'-?\d+\.?\d*', message)
            
            if len(numbers) >= 3 and any(x in msg_lower for x in ['analyze', 'stats', 'statistics', 'mean', 'average', 'data']):
                try:
                    data_points = [float(n) for n in numbers]
                    analysis = AdvancedAnalyzer.generate_comprehensive_analysis(data_points)
                    
                    if 'error' not in analysis:
                        response = f"### 📊 Statistical Analysis\n\n"
                        response += f"I analyzed your **{len(data_points)} data points**. "
                        
                        # Better integration of insights
                        insights = AdvancedAnalyzer.generate_insights(analysis)
                        response += f"{insights[0]} " if insights else ""
                        
                        response += f"\n\n**Findings:**\n"
                        response += f"- **Average (Mean):** {analysis['central_tendency']['mean']}\n"
                        response += f"- **Midpoint (Median):** {analysis['central_tendency']['median']}\n"
                        response += f"- **Variation:** Standard deviation of {analysis['dispersion']['std_dev']}\n"
                        
                        if analysis['trends']['trend'] != 'insufficient_data':
                            response += f"- **Trend:** Data shows a {analysis['trends']['strength']} {analysis['trends']['trend']} direction.\n"
                            
                        confidence = 0.95
                    else:
                        response = f"I tried to analyze the numbers, but encountered an error: {analysis['error']}"
                except Exception as e:
                    logger.error(f"Error in quick analysis: {e}")

            # Check if we have file data to analyze
            elif file_data:
                file_name = file_data.get('name', 'unknown file')
                file_type = file_data.get('type', 'unknown')
                file_content = file_data.get('content', '')
                
                response = f"I've analyzed your file **{file_name}**. Here's what I found:\n\n"
                
                content_preview = file_content[:500] if len(file_content) > 500 else file_content
                word_count = len(file_content.split()) if file_content else 0
                
                response += f"📄 **File Overview**\n"
                response += f"This {file_type} document contains approximately {word_count} words of content. "
                response += f"I've processed the file and can help you with summarizing points, pattern recognition, or extracting specifics."
                confidence = 0.90
            
            # Check for chart request (if not handled above)
            elif MAXY1_3.is_chart_request(message)[0]:
                is_chart, chart_type, data, labels, title = MAXY1_3.is_chart_request(message)
                base64_image, description = MAXY1_3.generate_chart_image(chart_type, data, labels, title)
                
                if base64_image:
                    response = f"I've created a {chart_type} chart for you based on your data! 📊\n\n"
                    response += f"**{title}** breakdown shows {len(data)} distinct data points total. "
                    response += f"The visual representation above should make the distribution clear."
                    chart_data = {'type': chart_type, 'title': title, 'base64_image': base64_image, 'description': description}
                else:
                    response = f"I tried to create your {chart_type} chart, but there was a rendering issue. "
                    response += f"The total for your data ({title}) is {sum(data)}."
                confidence = 0.92

            # Basic responses
            elif any(g in msg_lower for g in ['hello', 'hi', 'hey']):
                slang = slang_manager.get_random_slang(use_slang)
                response = f"Hello {slang}! I'm MAXY 1.3, your advanced AI assistant. I can help you build websites, write code, analyze data, and create visualizations. What are we building today?"
                confidence = 0.95
            
            elif any(q in msg_lower for q in ['who are you', 'what can you do']):
                response = "I'm MAXY 1.3, upgraded with a **Dynamic Code Engine**! I can:\n\n🚀 **Build Websites** - Ask me to 'build a landing page' or 'create a portfolio'\n💻 **Programming** - Write complex scripts in Python, JS, and more\n📊 **Data Insights** - Analyze numbers and generate visual charts\n📁 **File Intelligence** - Process and extract data from your uploads"
                confidence = 0.96
            
            else:
                slang = slang_manager.get_random_slang(use_slang)
                response = f"I'm ready to help with your project, {slang}! As MAXY 1.3, I can build web structures, write custom code, or perform deep data analysis. What's the next step for us?"
                confidence = 0.85
        
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
                'File processing & analysis',
                'Data extraction',
                'Content summarization',
                'Pattern recognition',
                'Document insights'
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
        conversation_history: Optional[List[Dict]] = None
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
            return MAXY1_1.process_message(message, include_thinking, conversation_history)
        elif model_name_lower == 'maxy1.2':
            return MAXY1_2.process_message(message, include_thinking, conversation_history)
        elif model_name_lower == 'maxy1.3':
            return MAXY1_3.process_message(message, include_thinking, conversation_history)
        else:
            logger.warning(f"Unknown model: {model_name}, defaulting to MAXY1.1")
            return MAXY1_1.process_message(message, include_thinking, conversation_history)
            