"""
Conversation Engine
Manages conversation flow, history, and context
"""

import uuid
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)


class ConversationMemory:
    """Manage conversation history and context"""
    
    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self.messages: deque = deque(maxlen=max_history)
        self.context: Dict[str, Any] = {}
    
    def add_message(self, role: str, content: str, model: str = None, metadata: Dict = None):
        """Add message to history"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'model': model,
            'metadata': metadata or {}
        }
        self.messages.append(message)
        logger.debug(f"Added message: {role} - {content[:50]}...")
        return message
    
    def get_messages(self, limit: Optional[int] = None) -> List[Dict]:
        """Get conversation messages"""
        messages = list(self.messages)
        if limit:
            messages = messages[-limit:]
        return messages
    
    def get_context(self) -> Dict[str, Any]:
        """Get conversation context"""
        return self.context.copy()
    
    def update_context(self, key: str, value: Any):
        """Update context"""
        self.context[key] = value
        logger.debug(f"Updated context: {key}")
    
    def clear(self):
        """Clear conversation history"""
        self.messages.clear()
        self.context.clear()
        logger.info("Conversation history cleared")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get conversation summary"""
        return {
            'message_count': len(self.messages),
            'first_message': self.messages[0] if self.messages else None,
            'last_message': self.messages[-1] if self.messages else None,
            'context': self.context
        }


class ConversationEngine:
    """Main conversation engine"""
    
    def __init__(self, conversation_id: Optional[str] = None, max_history: int = 50):
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.memory = ConversationMemory(max_history)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.message_count = 0
        self.models_used = set()
        self.metadata: Dict[str, Any] = {}
    
    def process_user_message(self, message: str) -> Dict[str, Any]:
        """Process user message and add to history"""
        try:
            self.memory.add_message('user', message)
            self.message_count += 1
            self.updated_at = datetime.now()
            
            return {
                'success': True,
                'message_id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error processing user message: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_assistant_response(
        self,
        response: str,
        model: str,
        thinking: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Process and store assistant response"""
        try:
            msg_metadata = metadata or {}
            msg_metadata['thinking'] = thinking
            
            self.memory.add_message('assistant', response, model=model, metadata=msg_metadata)
            self.models_used.add(model)
            self.updated_at = datetime.now()
            
            return {
                'success': True,
                'message_id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error processing assistant response: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_conversation_context(self, depth: int = 5) -> List[Dict]:
        """Get recent conversation context"""
        messages = self.memory.get_messages()
        if depth:
            messages = messages[-depth:]
        return messages
    
    def get_user_intent(self) -> Optional[str]:
        """Analyze user intent from recent messages"""
        try:
            messages = self.memory.get_messages()
            if not messages:
                return None
            
            # Get last user message
            user_messages = [m for m in messages if m['role'] == 'user']
            if not user_messages:
                return None
            
            last_message = user_messages[-1]['content'].lower()
            
            # Simple intent detection
            if any(word in last_message for word in ['analyze', 'data', 'statistics', 'calculate']):
                return 'analysis'
            elif any(word in last_message for word in ['code', 'write', 'program', 'function']):
                return 'coding'
            elif any(word in last_message for word in ['research', 'tell', 'explain', 'what is']):
                return 'research'
            elif any(word in last_message for word in ['chart', 'graph', 'visualize', 'plot']):
                return 'visualization'
            elif any(word in last_message for word in ['file', 'upload', 'document', 'pdf']):
                return 'file_processing'
            else:
                return 'general'
        
        except Exception as e:
            logger.error(f"Error detecting user intent: {str(e)}")
            return 'general'
    
    def should_switch_model(self) -> Optional[str]:
        """Determine if model switch is needed based on intent"""
        intent = self.get_user_intent()
        
        intent_to_model = {
            'analysis': 'maxy1.2',
            'research': 'maxy1.2',
            'coding': 'maxy1.3',
            'general': 'maxy1.1',
            'visualization': 'maxy1.2',
            'file_processing': 'maxy1.2'
        }
        
        return intent_to_model.get(intent)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get conversation statistics"""
        messages = self.memory.get_messages()
        
        user_messages = [m for m in messages if m['role'] == 'user']
        assistant_messages = [m for m in messages if m['role'] == 'assistant']
        
        total_characters = sum(len(m['content']) for m in messages)
        avg_message_length = total_characters / len(messages) if messages else 0
        
        return {
            'conversation_id': self.conversation_id,
            'total_messages': len(messages),
            'user_messages': len(user_messages),
            'assistant_messages': len(assistant_messages),
            'models_used': list(self.models_used),
            'total_characters': total_characters,
            'average_message_length': round(avg_message_length, 2),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'duration_seconds': (self.updated_at - self.created_at).total_seconds()
        }
    
    def export_conversation(self) -> Dict[str, Any]:
        """Export full conversation"""
        return {
            'conversation_id': self.conversation_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'messages': self.memory.get_messages(),
            'metadata': self.metadata,
            'statistics': self.get_statistics()
        }


class ConversationManager:
    """Manage multiple conversations"""
    
    def __init__(self):
        self.conversations: Dict[str, ConversationEngine] = {}
        self.logger = logging.getLogger(__name__)
    
    def create_conversation(self, conversation_id: Optional[str] = None) -> str:
        """Create new conversation"""
        conv_id = conversation_id or str(uuid.uuid4())
        self.conversations[conv_id] = ConversationEngine(conv_id)
        self.logger.info(f"Created conversation: {conv_id}")
        return conv_id
    
    def get_conversation(self, conversation_id: str) -> Optional[ConversationEngine]:
        """Get conversation by ID"""
        return self.conversations.get(conversation_id)
    
    def get_or_create_conversation(self, conversation_id: Optional[str] = None) -> str:
        """Get existing or create new conversation"""
        if conversation_id and conversation_id in self.conversations:
            return conversation_id
        return self.create_conversation(conversation_id)
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete conversation"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            self.logger.info(f"Deleted conversation: {conversation_id}")
            return True
        return False
    
    def list_conversations(self) -> List[Dict[str, Any]]:
        """List all conversations"""
        conversations_list = []
        for conv_id, engine in self.conversations.items():
            stats = engine.get_statistics()
            conversations_list.append({
                'id': conv_id,
                'created_at': engine.created_at.isoformat(),
                'updated_at': engine.updated_at.isoformat(),
                'message_count': stats['total_messages'],
                'models_used': stats['models_used']
            })
        return sorted(conversations_list, key=lambda x: x['updated_at'], reverse=True)
    
    def get_statistics_summary(self) -> Dict[str, Any]:
        """Get summary statistics across all conversations"""
        total_conversations = len(self.conversations)
        total_messages = sum(
            engine.get_statistics()['total_messages']
            for engine in self.conversations.values()
        )
        
        all_models = set()
        for engine in self.conversations.values():
            all_models.update(engine.models_used)
        
        return {
            'total_conversations': total_conversations,
            'total_messages': total_messages,
            'models_used': list(all_models),
            'average_messages_per_conversation': (
                total_messages / total_conversations if total_conversations > 0 else 0
            )
        }


class ResponseValidator:
    """Validate and enhance responses"""
    
    @staticmethod
    def validate_response(response: str) -> Tuple[bool, str]:
        """Validate response quality"""
        if not response:
            return False, "Response is empty"
        
        if len(response.strip()) < 10:
            return False, "Response is too short"
        
        if len(response) > 50000:
            return False, "Response is too long"
        
        return True, "Response is valid"
    
    @staticmethod
    def add_confidence_score(response: Dict[str, Any], base_confidence: float) -> Dict[str, Any]:
        """Add confidence score to response"""
        response['confidence'] = round(base_confidence, 2)
        return response
    
    @staticmethod
    def generate_follow_up_suggestions(
        message: str,
        response: str,
        model: str
    ) -> List[str]:
        """Generate follow-up question suggestions"""
        
        suggestions_template = {
            'maxy1.1': [
                "Want to explore this topic further?",
                "Should we discuss something else?",
                "Any other questions for me?",
                "Would you like more details?",
            ],
            'maxy1.2': [
                "Would you like citations for any claims?",
                "Should we dive deeper into any aspect?",
                "Want to explore related topics?",
                "Need clarification on anything?",
            ],
            'maxy1.3': [
                "Want to see an optimized version?",
                "Should I explain the code in more detail?",
                "Would you like examples of other approaches?",
                "Need help adapting this for your use case?",
            ]
        }
        
        suggestions = suggestions_template.get(model, suggestions_template['maxy1.1'])
        return suggestions[:2]  # Return 2 suggestions
    
    @staticmethod
    def enhance_response(
        response: str,
        model: str,
        thinking: Optional[Dict] = None,
        confidence: float = 0.8
    ) -> Dict[str, Any]:
        """Enhance response with metadata"""
        
        is_valid, validation_msg = ResponseValidator.validate_response(response)
        
        if not is_valid:
            logger.warning(f"Response validation failed: {validation_msg}")
        
        enhanced = {
            'response': response,
            'model': model,
            'confidence': round(confidence, 2),
            'thinking': thinking,
            'valid': is_valid,
            'generated_at': datetime.now().isoformat()
        }
        
        return enhanced
