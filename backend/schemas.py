"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum


class ModelType(str, Enum):
    """Available AI models"""
    MAXY_1_1 = "maxy1.1"
    MAXY_1_2 = "maxy1.2"
    MAXY_1_3 = "maxy1.3"


class FileType(str, Enum):
    """Supported file types"""
    IMAGE = "image"
    PDF = "pdf"
    DOCUMENT = "document"
    TEXT = "text"
    DATA = "data"
    UNKNOWN = "unknown"


class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = None
    model: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "Hello, how are you?",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class AIThinking(BaseModel):
    """AI thinking process displayed to user"""
    reasoning: str = Field(..., description="The thinking/reasoning process")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0, description="Confidence score 0-1")
    reasoning_steps: Optional[List[str]] = Field(default=None, description="Step-by-step reasoning")
    model_used: str = Field(..., description="Which model generated this thinking")
    
    class Config:
        json_schema_extra = {
            "example": {
                "reasoning": "The user is asking about statistics, so I should provide detailed calculations...",
                "confidence": 0.92,
                "reasoning_steps": ["Identify question topic", "Gather relevant context", "Structure response"],
                "model_used": "maxy1.2"
            }
        }


class FileData(BaseModel):
    """File upload data"""
    name: str = Field(..., description="Original filename")
    type: str = Field(..., description="MIME type")
    size: int = Field(..., gt=0, description="File size in bytes")
    content: str = Field(..., description="Base64 encoded file content")
    
    @validator('content')
    def validate_content(cls, v):
        if not v or len(v) == 0:
            raise ValueError("File content cannot be empty")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "data.pdf",
                "type": "application/pdf",
                "size": 1024000,
                "content": "base64encodedcontent..."
            }
        }


class AnalysisResult(BaseModel):
    """Result of file or data analysis"""
    file_name: Optional[str] = None
    file_type: FileType
    analysis: str = Field(..., description="Analysis content")
    metadata: Optional[Dict[str, Any]] = None
    extraction_successful: bool = True
    error_message: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_name": "report.pdf",
                "file_type": "pdf",
                "analysis": "Document contains...",
                "metadata": {"pages": 5, "word_count": 2500},
                "extraction_successful": True
            }
        }


class ChartRequest(BaseModel):
    """Request for chart generation"""
    type: str = Field(..., description="Chart type: pie, bar, line, histogram, scatter, box")
    title: str = Field(..., description="Chart title")
    data: Union[List[float], Dict[str, Any]] = Field(..., description="Chart data")
    labels: Optional[List[str]] = None
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "bar",
                "title": "Monthly Sales",
                "data": [100, 200, 150, 300],
                "labels": ["Jan", "Feb", "Mar", "Apr"],
                "x_label": "Month",
                "y_label": "Sales"
            }
        }


class ChartResponse(BaseModel):
    """Generated chart response"""
    type: str
    title: str
    base64_image: str = Field(..., description="Base64 encoded PNG image")
    description: str
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "bar",
                "title": "Monthly Sales",
                "base64_image": "iVBORw0KGgoAAAANSUhEUgAAA...",
                "description": "Bar chart showing monthly sales data"
            }
        }


class ChatRequest(BaseModel):
    """Chat request with enhanced features"""
    message: str = Field(..., description="User message")
    model: ModelType = Field(default=ModelType.MAXY_1_1, description="AI model to use")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID")
    history: Optional[List[ChatMessage]] = Field(default=None, description="Conversation history")
    file: Optional[FileData] = None
    include_thinking: bool = Field(default=True, description="Include AI thinking process")
    include_sources: bool = Field(default=True, description="Include source citations")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Response creativity 0-1")
    max_tokens: Optional[int] = Field(default=None, description="Max response length")
    user_id: Optional[str] = Field(None, description="User ID for credit tracking")
    
    @validator('message')
    def validate_message(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Message cannot be empty")
        if len(v) > 10000:
            raise ValueError("Message too long (max 10000 characters)")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Analyze this data for trends",
                "model": "maxy1.2",
                "conversation_id": "conv_123",
                "include_thinking": True,
                "temperature": 0.7
            }
        }


class ChatResponse(BaseModel):
    """Enhanced chat response"""
    conversation_id: str = Field(..., description="Unique conversation identifier")
    response: str = Field(..., description="AI response text")
    model_used: str = Field(..., description="Which model generated the response")
    thinking: Optional[AIThinking] = Field(None, description="AI thinking process")
    file_processed: bool = Field(default=False, description="Whether file was processed")
    analysis: Optional[AnalysisResult] = None
    charts: Optional[List[ChartResponse]] = Field(default=None, description="Generated charts")
    sources: Optional[List[str]] = Field(None, description="Source citations")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0, description="Response confidence score")
    suggestions: Optional[List[str]] = Field(None, description="Follow-up suggestions")
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "response": "Based on your data...",
                "model_used": "maxy1.2",
                "thinking": {"reasoning": "...", "confidence": 0.92},
                "file_processed": True,
                "confidence": 0.88
            }
        }


class ConversationCreate(BaseModel):
    """Create new conversation"""
    title: Optional[str] = Field(None, description="Conversation title")
    model: ModelType = Field(default=ModelType.MAXY_1_1, description="Initial model")
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Data Analysis Session",
                "model": "maxy1.2"
            }
        }


class ConversationResponse(BaseModel):
    """Conversation metadata"""
    id: str
    title: Optional[str]
    model: str
    created_at: datetime
    updated_at: datetime
    message_count: int
    metadata: Optional[Dict[str, Any]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "conv_123",
                "title": "Data Analysis",
                "model": "maxy1.2",
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
                "message_count": 5
            }
        }


class DataAnalysisRequest(BaseModel):
    """Advanced data analysis request"""
    data: List[float] = Field(..., description="Numerical data to analyze")
    analysis_type: str = Field(default="comprehensive", description="Type: comprehensive, statistical, correlation, regression")
    labels: Optional[List[str]] = None
    title: Optional[str] = None
    
    @validator('data')
    def validate_data(cls, v):
        if len(v) < 2:
            raise ValueError("At least 2 data points required")
        if len(v) > 10000:
            raise ValueError("Maximum 10000 data points")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "data": [10, 20, 15, 25, 30, 22],
                "analysis_type": "comprehensive",
                "title": "Monthly Revenue"
            }
        }


class DataAnalysisResponse(BaseModel):
    """Data analysis results"""
    title: str
    analysis_type: str
    summary: str
    statistics: Dict[str, Any]
    insights: List[str]
    outliers: Optional[List[float]] = None
    recommendations: Optional[List[str]] = None
    charts: Optional[List[ChartResponse]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Revenue Analysis",
                "analysis_type": "comprehensive",
                "summary": "Data shows positive trend...",
                "statistics": {"mean": 20.3, "median": 22.0},
                "insights": ["Trend is increasing", "Low variance"],
                "recommendations": ["Monitor for anomalies"]
            }
        }


class ErrorResponse(BaseModel):
    """Standardized error response"""
    error: str = Field(..., description="Error type/code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = None
    suggestion: Optional[str] = Field(None, description="Suggested fix or action")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "FILE_TOO_LARGE",
                "message": "Uploaded file exceeds maximum size",
                "suggestion": "Please upload a file smaller than 10MB",
                "status_code": 413
            }
        }


class FeedbackRequest(BaseModel):
    """User feedback submission"""
    conversation_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5 stars")
    feedback: str = Field(..., description="Detailed feedback")
    tags: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "rating": 5,
                "feedback": "Very helpful response!",
                "tags": ["helpful", "accurate"]
            }
        }


class HealthStatus(BaseModel):
    """System health status"""
    status: str = Field(..., description="overall: healthy, degraded, unhealthy")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    uptime_seconds: float
    features: Dict[str, bool]
    dependencies: Dict[str, bool]
    metrics: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "uptime_seconds": 3600,
                "features": {"wikipedia": True, "charts": True},
                "dependencies": {"database": True, "cache": True}
            }
        }


class ModelInfo(BaseModel):
    """Information about available AI models"""
    name: str
    version: str
    description: str
    capabilities: List[str]
    parameters: Dict[str, Any]
    examples: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "MAXY 1.2",
                "version": "1.2.0",
                "description": "Research and analysis expert",
                "capabilities": ["deep research", "citations", "detailed explanations"],
                "parameters": {"temperature": 0.7, "max_tokens": 2000},
                "examples": ["Research climate change", "Analyze market trends"]
            }
        }
