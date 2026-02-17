"""
MAXY Chat Backend - Main FastAPI Application
Advanced multi-model AI chatbot with file processing and data analysis
"""

from fastapi import FastAPI, HTTPException, Request, status, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import logging
import sys
import time
import os
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# Import custom modules
from config import config
from schemas import (
    ChatRequest, ChatResponse, ChatMessage, FileData, AnalysisResult,
    ConversationCreate, ConversationResponse, DataAnalysisRequest,
    DataAnalysisResponse, ErrorResponse, FeedbackRequest, HealthStatus,
    ModelInfo, ChartRequest, ChartResponse, FileType
)
from models import ModelRouter, MAXYThinkingEngine
from engine import ConversationManager, ResponseValidator
from file_processor import FileProcessor
from data_analyzer import AdvancedAnalyzer, CorrelationAnalyzer
from chart_generator import ChartGenerator
from credit_manager import credit_manager, get_user_id_from_request

# Setup logging
log_dir = os.path.dirname(config.LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend) - ALWAYS serve frontend
static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    @app.get("/", include_in_schema=False)
    async def serve_index():
        """Serve the main frontend page"""
        return FileResponse(os.path.join(static_dir, "chat.html"))
    


# Server status page
@app.get("/server-status", include_in_schema=False)
async def serve_server_status():
    """Serve server startup status page"""
    status_file = os.path.join(os.path.dirname(__file__), "server_status.html")
    if os.path.exists(status_file):
        return FileResponse(status_file)
    return {"status": "running", "message": "Server is online!"}

# Initialize managers
conversation_manager = ConversationManager()

# Request tracking
request_stats = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "start_time": datetime.now(),
    "average_response_time": 0,
    "request_times": []
}


# Middleware for request tracking and logging
@app.middleware("http")
async def track_requests(request: Request, call_next):
    """Track and log all requests"""
    start_time = time.time()
    request_stats["total_requests"] += 1
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Track response time
        request_stats["request_times"].append(process_time)
        if len(request_stats["request_times"]) > 100:
            request_stats["request_times"].pop(0)
        request_stats["average_response_time"] = (
            sum(request_stats["request_times"]) / len(request_stats["request_times"])
        )
        
        if response.status_code < 400:
            request_stats["successful_requests"] += 1
        else:
            request_stats["failed_requests"] += 1
        
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
        )
        return response
    
    except Exception as e:
        request_stats["failed_requests"] += 1
        logger.error(f"Request failed: {request.method} {request.url.path} - {str(e)}")
        raise


# ===== HEALTH & MONITORING ENDPOINTS =====

@app.get("/api", tags=["Health"])
async def root():
    """API information endpoint"""
    return {
        "name": config.API_TITLE,
        "version": config.API_VERSION,
        "description": config.API_DESCRIPTION,
        "status": "operational",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "conversations": "/conversations",
            "models": "/models",
            "docs": "/api/docs"
        }
    }


@app.get("/health", response_model=HealthStatus, tags=["Health"])
async def health_check():
    """Comprehensive health check endpoint"""
    uptime = datetime.now() - request_stats["start_time"]
    
    features = {
        "file_processing": config.ENABLE_FILE_PROCESSING,
        "charts": config.ENABLE_CHARTS,
        "wikipedia": config.ENABLE_WIKIPEDIA,
        "thinking_enabled": config.THINKING_ENABLED,
        "analytics": config.ENABLE_ANALYTICS,
    }
    
    dependencies = {
        "conversation_engine": True,
        "model_router": True,
        "file_processor": True,
        "data_analyzer": True,
        "chart_generator": True
    }
    
    return HealthStatus(
        status="healthy",
        uptime_seconds=uptime.total_seconds(),
        features=features,
        dependencies=dependencies,
        metrics={
            "total_requests": request_stats["total_requests"],
            "successful_requests": request_stats["successful_requests"],
            "average_response_time": round(request_stats["average_response_time"], 3),
            "active_conversations": len(conversation_manager.conversations)
        }
    )


@app.get("/stats", tags=["Health"])
async def get_stats():
    """Get API usage statistics"""
    uptime = datetime.now() - request_stats["start_time"]
    conv_stats = conversation_manager.get_statistics_summary()
    
    return {
        "timestamp": datetime.now().isoformat(),
        "request_stats": {
            "total_requests": request_stats["total_requests"],
            "successful_requests": request_stats["successful_requests"],
            "failed_requests": request_stats["failed_requests"],
            "success_rate": round(
                request_stats["successful_requests"] / max(request_stats["total_requests"], 1) * 100, 2
            ),
            "average_response_time_ms": round(request_stats["average_response_time"] * 1000, 2)
        },
        "uptime": {
            "seconds": uptime.total_seconds(),
            "formatted": str(uptime).split('.')[0]
        },
        "conversations": conv_stats
    }


# ===== MODELS ENDPOINTS =====

@app.get("/models", tags=["Models"])
async def list_models():
    """Get available AI models and their capabilities"""
    models = []
    for model_name in ['maxy1.1', 'maxy1.2', 'maxy1.3']:
        model_info = ModelRouter.get_model_info(model_name)
        if model_info and len(model_info) > 0:
            models.append(model_info)
    
    return {
        "available_models": len(models),
        "models": models,
        "default_model": "maxy1.1"
    }


@app.get("/models/{model_name}", tags=["Models"])
async def get_model_info(model_name: str):
    """Get detailed information about a specific model"""
    model_info = ModelRouter.get_model_info(model_name.lower())
    
    if not model_info or len(model_info) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{model_name}' not found"
        )
    
    return model_info


# ===== CHAT ENDPOINTS =====

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest, http_request: Request):
    """
    Main chat endpoint with enhanced AI thinking and multi-model support
    
    Features:
    - AI thinking display (reasoning process)
    - File processing and analysis
    - Conversation context management
    - Multiple AI models with different specialties
    - Credit system integration
    """
    start_time = time.time()
    
    try:
        # Check credits if enabled
        if config.ENABLE_CREDITS:
            # Use user_id from request body if provided, otherwise extract from request
            user_id = request.user_id if request.user_id else get_user_id_from_request(http_request)
            has_credits, user_data = credit_manager.use_credit(user_id)
            
            if not has_credits:
                next_refresh = user_data.get('next_refresh', '3 hours')
                raise HTTPException(
                    status_code=429,
                    detail=f"You've used all {config.MAX_CREDITS_PER_USER} messages. Credits refresh at {next_refresh}."
                )
        
        # Validate request
        if not request.message or len(request.message.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )
        
        logger.info(
            f"Chat request - Model: {request.model}, "
            f"Message length: {len(request.message)}, "
            f"Has file: {request.file is not None}"
        )
        
        # Get or create conversation
        conv_id = conversation_manager.get_or_create_conversation(request.conversation_id)
        engine = conversation_manager.get_conversation(conv_id)
        
        if not engine:
            raise HTTPException(
                status_code=500,
                detail="Failed to create or retrieve conversation"
            )
        
        # Process user message
        engine.process_user_message(request.message)
        
        # Process file if uploaded
        file_analysis = None
        if request.file:
            try:
                file_type = FileProcessor.detect_file_type(request.file.name, request.file.type)
                
                if file_type == 'image':
                    result = FileProcessor.process_image(request.file.content)
                elif file_type == 'pdf':
                    result = FileProcessor.process_pdf(request.file.content)
                elif file_type == 'document':
                    result = FileProcessor.process_word_document(request.file.content)
                else:
                    result = FileProcessor.process_text_file(request.file.content, request.file.name)
                
                if result.get('success'):
                    file_analysis = AnalysisResult(
                        file_name=request.file.name,
                        file_type=file_type, # type: ignore
                        analysis=result['analysis'],
                        metadata=result.get('metadata'),
                        extraction_successful=True
                    )
                else:
                    file_analysis = AnalysisResult(
                        file_name=request.file.name,
                        file_type=file_type, # type: ignore
                        analysis="",
                        extraction_successful=False,
                        error_message=result.get('error', 'Unknown error')
                    )
                
                logger.info(f"File processed: {request.file.name} ({file_type})")
            
            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                file_analysis = AnalysisResult(
                    file_name=request.file.name,
                    file_type=FileType.UNKNOWN,
                    analysis="",
                    extraction_successful=False,
                    error_message=str(e)
                )
        
        # Generate AI response
        thinking = None
        if request.include_thinking:
            thinking = MAXYThinkingEngine.generate_thinking(
                request.model,
                request.message,
                "general"
            )
        
        # Route to appropriate model
        model_response = ModelRouter.process(
            request.model,
            request.message,
            include_thinking=False,
            conversation_history=engine.get_conversation_context()
        )
        
        response_text = model_response['response']
        confidence = model_response.get('confidence', 0.8)
        
        # Add file analysis to response if available
        if file_analysis and file_analysis.extraction_successful:
            response_text = f"{file_analysis.analysis}\n\n{'='*60}\n\n{response_text}"
        
        # Process response
        if engine:
            engine.process_assistant_response(
                response_text,
                request.model,
                thinking={'reasoning': thinking, 'model_used': request.model} if thinking else None,
                metadata={'confidence': confidence}
            )
        
        # Generate follow-up suggestions
        suggestions = ResponseValidator.generate_follow_up_suggestions(
            request.message,
            response_text,
            request.model
        )
        
        process_time = time.time() - start_time
        logger.info(f"Chat request completed in {process_time:.3f}s")
        
        return ChatResponse(
            conversation_id=conv_id,
            response=response_text,
            model_used=request.model,
            thinking=None,  # Simplified - not using AIThinking object for now
            file_processed=file_analysis is not None,
            analysis=file_analysis,
            confidence=confidence,
            suggestions=suggestions,
            sources=model_response.get('sources', []),
            charts=model_response.get('charts'),  # Pass charts from model response
            metadata={
                'response_time_ms': round(process_time * 1000, 2),
                'conversation_message_count': engine.message_count if engine else 0
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)[:100]}"
        )


# ===== CONVERSATION MANAGEMENT ENDPOINTS =====

@app.post("/conversations", response_model=ConversationResponse, tags=["Conversations"])
async def create_conversation(request: ConversationCreate):
    """Create a new conversation"""
    try:
        conv_id = conversation_manager.create_conversation()
        engine = conversation_manager.get_conversation(conv_id)
        
        if not engine:
            raise HTTPException(status_code=500, detail="Failed to create conversation")
        
        if request.title:
            engine.metadata['title'] = request.title
        if request.metadata:
            engine.metadata.update(request.metadata)
        
        return ConversationResponse(
            id=conv_id,
            title=request.title,
            model=request.model,
            created_at=engine.created_at,
            updated_at=engine.updated_at,
            message_count=engine.message_count,
            metadata=engine.metadata
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations", tags=["Conversations"])
async def list_conversations():
    """Get list of all conversations"""
    try:
        conversations = conversation_manager.list_conversations()
        return {
            "total_conversations": len(conversations),
            "conversations": conversations
        }
    
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations/{conversation_id}", response_model=ConversationResponse, tags=["Conversations"])
async def get_conversation(conversation_id: str):
    """Get specific conversation details"""
    try:
        engine = conversation_manager.get_conversation(conversation_id)
        
        if not engine:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        stats = engine.get_statistics()
        
        return ConversationResponse(
            id=conversation_id,
            title=engine.metadata.get('title'),
            model=list(engine.models_used)[0] if engine.models_used else "maxy1.1",
            created_at=engine.created_at,
            updated_at=engine.updated_at,
            message_count=stats['total_messages'],
            metadata=engine.metadata
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/conversations/{conversation_id}", tags=["Conversations"])
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    try:
        if conversation_manager.delete_conversation(conversation_id):
            return {"message": "Conversation deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Conversation not found")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== DATA ANALYSIS ENDPOINTS =====

@app.post("/analyze", response_model=DataAnalysisResponse, tags=["Analysis"])
async def analyze_data(request: DataAnalysisRequest):
    """
    Perform comprehensive data analysis
    
    Includes:
    - Basic statistics (mean, median, mode, std dev)
    - Distribution analysis (skewness, kurtosis)
    - Outlier detection
    - Trend analysis
    - Generated insights
    """
    try:
        logger.info(f"Starting data analysis - {len(request.data)} data points")
        
        # Generate comprehensive analysis
        analysis = AdvancedAnalyzer.generate_comprehensive_analysis(request.data)
        
        if 'error' in analysis:
            raise HTTPException(status_code=400, detail=analysis['error'])
        
        # Generate insights
        insights = AdvancedAnalyzer.generate_insights(analysis)
        
        # Generate visualization
        charts = []
        try:
            histogram = ChartGenerator.create_histogram(
                request.data,
                title=f"{request.title or 'Data'} Distribution",
                bins=min(20, len(set(request.data)))
            )
            if histogram:
                charts.append(ChartResponse(
                    type="histogram",
                    title=f"{request.title or 'Data'} Distribution",
                    base64_image=histogram,
                    description="Distribution of data values"
                ))
        except Exception as e:
            logger.warning(f"Could not generate histogram: {str(e)}")
        
        return DataAnalysisResponse(
            title=request.title or "Data Analysis",
            analysis_type=request.analysis_type,
            summary="Comprehensive statistical analysis completed",
            statistics=analysis,
            insights=insights,
            outliers=analysis.get('outliers', {}).get('values', []),
            recommendations=[
                "Review outliers for data quality",
                "Consider transforming skewed data",
                "Validate data sources"
            ] if analysis.get('outliers', {}).get('count', 0) > 0 else [],
            charts=charts if charts else None
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in data analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== CHART GENERATION ENDPOINTS =====

@app.post("/charts", response_model=ChartResponse, tags=["Visualization"])
async def generate_chart(request: ChartRequest):
    """
    Generate professional charts and visualizations
    
    Supported types:
    - bar, pie, line, histogram, scatter, box, heatmap
    """
    try:
        logger.info(f"Generating {request.type} chart: {request.title}")
        
        chart_type = request.type.lower()
        base64_image = None
        
        if chart_type == 'pie' and isinstance(request.data, list):
            base64_image = ChartGenerator.create_pie_chart(
                request.labels or [f"Item {i}" for i in range(len(request.data))],
                request.data,
                request.title
            )
        
        elif chart_type == 'bar' and isinstance(request.data, list):
            base64_image = ChartGenerator.create_bar_chart(
                request.labels or [f"Item {i}" for i in range(len(request.data))],
                request.data,
                request.title,
                request.x_label or "Categories",
                request.y_label or "Values"
            )
        
        elif chart_type == 'line' and isinstance(request.data, dict):
            base64_image = ChartGenerator.create_line_chart(
                request.data.get('x', []),
                request.data.get('y', []),
                request.title,
                request.x_label or "X",
                request.y_label or "Y"
            )
        
        elif chart_type == 'histogram' and isinstance(request.data, list):
            base64_image = ChartGenerator.create_histogram(
                request.data,
                title=request.title,
                ylabel=request.y_label or "Frequency"
            )
        
        elif chart_type == 'scatter' and isinstance(request.data, dict):
            base64_image = ChartGenerator.create_scatter_plot(
                request.data.get('x', []),
                request.data.get('y', []),
                request.title,
                request.x_label or "X",
                request.y_label or "Y"
            )
        
        elif chart_type == 'box' and isinstance(request.data, list):
            base64_image = ChartGenerator.create_box_plot(
                request.data,
                request.title,
                request.y_label or "Value"
            )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported chart type: {chart_type}"
            )
        
        if not base64_image:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate chart"
            )
        
        return ChartResponse(
            type=chart_type,
            title=request.title,
            base64_image=base64_image,
            description=f"{chart_type.capitalize()} chart visualization"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating chart: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== ERROR HANDLING =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch-all exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500,
            "timestamp": datetime.now().isoformat()
        }
    )


# ===== CREDIT SYSTEM ENDPOINTS =====

@app.get("/credits", tags=["Credits"])
async def get_user_credits_endpoint(request: Request, user_id: Optional[str] = None):
    """Get current user's credit information"""
    try:
        if not config.ENABLE_CREDITS:
            return {
                "credits_enabled": False,
                "message": "Credit system is disabled"
            }
        
        # Use provided user_id from query param, otherwise extract from request
        if not user_id:
            user_id = get_user_id_from_request(request)
        user_data = credit_manager.get_user_credits(user_id)
        
        if user_data:
            return {
                "credits_enabled": True,
                "user_id": user_id[:8] + "..." if len(user_id) > 8 else user_id,
                "credits_remaining": user_data["credits_remaining"],
                "max_credits": user_data["max_credits"],
                "refresh_hours": user_data["refresh_hours"],
                "next_refresh": user_data.get("next_refresh"),
                "total_messages_sent": user_data["total_messages_sent"]
            }
        else:
            return {
                "credits_enabled": True,
                "credits_remaining": config.MAX_CREDITS_PER_USER,
                "max_credits": config.MAX_CREDITS_PER_USER,
                "refresh_hours": config.CREDIT_REFRESH_HOURS
            }
    
    except Exception as e:
        logger.error(f"Error getting credits: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/credits/status", tags=["Credits"])
async def get_credits_status():
    """Get credit system configuration"""
    return {
        "enabled": config.ENABLE_CREDITS,
        "max_credits": config.MAX_CREDITS_PER_USER,
        "refresh_hours": config.CREDIT_REFRESH_HOURS
    }


# ===== STARTUP & SHUTDOWN =====

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info(f"Starting {config.API_TITLE} v{config.API_VERSION}")
    logger.info(f"Debug mode: {config.DEBUG}")
    logger.info(f"CORS origins: {config.ALLOWED_ORIGINS}")
    logger.info(f"Features - Wikipedia: {config.ENABLE_WIKIPEDIA}, Charts: {config.ENABLE_CHARTS}")
    logger.info(f"Credit System - Enabled: {config.ENABLE_CREDITS}, Max: {config.MAX_CREDITS_PER_USER}, Refresh: {config.CREDIT_REFRESH_HOURS}h")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("Shutting down MAXY Chat Backend")
    logger.info(f"Final statistics: {request_stats}")


# Catch-all route for frontend (must be last)
if os.path.exists(static_dir):
    @app.get("/{path:path}", include_in_schema=False)
    async def serve_frontend(path: str):
        """Serve frontend files"""
        file_path = os.path.join(static_dir, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        # If file doesn't exist, serve index (for SPA routing)
        return FileResponse(os.path.join(static_dir, "chat.html"))


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {config.HOST}:{config.PORT}")
    uvicorn.run(
        "server:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower()
    )
