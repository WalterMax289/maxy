# MAXY Chat Backend 

## Overview

MAXY Chat Backend is a comprehensive FastAPI-based multi-model AI chatbot system with advanced features including:

- **AI Thinking Display**: See the reasoning process behind responses (Claude-style thinking)
- **Multi-Model Architecture**: Three specialized AI models with distinct personalities
- **Conversation Management**: Full conversation history, context awareness, and persistence
- **Advanced Data Analysis**: Comprehensive statistical analysis, outlier detection, trends
- **Advanced File Intelligence**: Enhanced text analysis (sentiment, keywords, entities) and CSV intelligence
- **Knowledge Synthesis**: Multi-source factual verification (Wikipedia + DuckDuckGo)
- **Supabase Authentication**: Secure user management with "Forgot Password" flow
- **Multi-lingual Slang**: Support for Kannada, Hindi, Tamil, and Telugu conversational styles
- **Professional Visualizations**: Generate charts and graphs with multiple visualization types
- **Error Handling**: Comprehensive error handling with recovery suggestions

## Architecture

### Core Components

```
/scripts/
├── server.py           # Main FastAPI application (675 lines)
├── models.py           # MAXY AI models implementation (587 lines)
├── engine.py           # Conversation engine & management (363 lines)
├── data_analyzer.py    # Advanced statistical analysis (470 lines)
├── chart_generator.py  # Professional visualizations (433 lines)
├── file_processor.py   # Document processing (438 lines)
├── schemas.py          # Pydantic models (374 lines)
├── config.py           # Configuration management (99 lines)
├── utils.py            # Helper utilities (347 lines)
└── requirements.txt    # Python dependencies
```

**Total: ~3,800+ lines of production-ready code**

## AI Models

### MAXY 1.1 - Conversational Assistant
- Natural, friendly conversation with **Multi-lingual Slang Support**
- Context-aware responses and personality-driven interactions
- **Slang Conversational Logic**: Recognizes local greetings (e.g., "yen guru")
- Real-time information handling and quick Wikipedia lookups

### MAXY 1.2 - Research Expert
- **KnowledgeSynthesizer Engine**: Multi-source factual verification
- Cross-references Wikipedia with DuckDuckGo for high accuracy
- Detailed analysis, insights, and relevance-scored results
- Automated context tracking and professional synthesis

### MAXY 1.3 - Data & Programming Expert
- **Advanced File Intelligence**: Sentiment, keywords, and entity extraction
- **Structured Data Analysis**: Automated CSV/JSON parsing and correlation
- Multi-language code generation and best practices
- Best-in-class programming, visualization, and debugging assistance

## Key Features

### 1. AI Thinking Display
Responses include an AI thinking process that shows:
- Reasoning steps taken
- Confidence scores
- Thought process transparency

### 2. Conversation Management
- Automatic conversation creation
- Full message history
- Context awareness
- Conversation statistics

### 3. Data Analysis
Comprehensive statistical analysis including:
- Central tendency (mean, median, mode)
- Dispersion (std dev, variance, coefficient of variation)
- Distribution shape (skewness, kurtosis)
- Outlier detection (IQR and Z-score methods)
- Trend analysis
- Correlation analysis
- Regression analysis

### 4. File Intelligence
Supported file types:
- **Images**: Analyze dimensions, colors, aspect ratio, format
- **PDFs**: Extract text, metadata, document structure
- **Word Documents**: Parse content, count paragraphs, extract tables
- **CSV/JSON**: Automated parsing, outlier detection, and correlation analysis
- **Text Analysis**: Sentiment detection, keyword extraction, and entity discovery

### 5. Chart Generation
Multiple chart types:
- Pie charts
- Bar charts
- Line charts
- Histograms
- Scatter plots
- Box plots
- Heatmaps

## API Endpoints

### Health & Monitoring
```
GET  /                 # API information
GET  /health           # Health check
GET  /stats            # Usage statistics
```

### Chat
```
POST /chat             # Main chat endpoint with AI thinking
GET  /conversations    # List all conversations
POST /conversations    # Create new conversation
GET  /conversations/{id}  # Get specific conversation
DELETE /conversations/{id} # Delete conversation
```

### Analysis
```
POST /analyze          # Advanced data analysis
POST /charts           # Generate visualizations
GET  /models           # List available models
GET  /models/{name}    # Model information
```

## Installation

### 1. Clone/Setup
```bash
cd scripts
pip install -r requirements.txt
```

### 2. Environment Variables (.env)
```
HOST=0.0.0.0
PORT=8000
DEBUG=False
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
MAX_FILE_SIZE=10485760

ENABLE_FILE_PROCESSING=True
ENABLE_CHARTS=True
ENABLE_WIKIPEDIA=True
ENABLE_ANALYTICS=True

THINKING_ENABLED=True
MAX_CONVERSATION_HISTORY=50
```

### 3. Run Server
```bash
python server.py
```

Server starts at `http://localhost:8000`
API docs available at `http://localhost:8000/api/docs`

## Usage Examples

### Basic Chat with Thinking
```json
POST /chat
{
  "message": "Tell me about AI",
  "model": "maxy1.2",
  "include_thinking": true
}
```

**Response:**
```json
{
  "conversation_id": "conv_123",
  "response": "Deep research analysis...",
  "model_used": "maxy1.2",
  "thinking": {
    "reasoning": "I'm analyzing your request about AI...",
    "confidence": 0.92,
    "reasoning_steps": [...]
  },
  "confidence": 0.88
}
```

### File Upload & Analysis
```json
POST /chat
{
  "message": "Analyze this PDF",
  "file": {
    "name": "report.pdf",
    "type": "application/pdf",
    "size": 1024000,
    "content": "base64encodedcontent..."
  }
}
```

### Data Analysis
```json
POST /analyze
{
  "data": [10, 20, 15, 25, 30, 22, 18, 28],
  "analysis_type": "comprehensive",
  "title": "Monthly Revenue"
}
```

**Response includes:**
- Central tendency measures
- Distribution analysis
- Outlier detection
- Trend analysis
- Generated insights
- Visualization (histogram)

### Chart Generation
```json
POST /charts
{
  "type": "bar",
  "title": "Sales by Region",
  "data": [100, 200, 150, 300],
  "labels": ["North", "South", "East", "West"],
  "x_label": "Region",
  "y_label": "Sales"
}
```

## Advanced Features

### Conversation Context Awareness
- Automatic context tracking
- User intent detection
- Model switching based on intent
- Conversation statistics

### Error Handling
- Comprehensive error messages
- Recovery suggestions
- Detailed logging
- Graceful degradation

### Performance Optimization
- Response caching
- Efficient data serialization
- Optimized file processing
- Batch operations support

### Security
- **Supabase Auth**: Secure user accounts and sessions
- **Password Recovery**: Complete "Forgot Password" email recovery flow
- **Input Validation**: Robust sanitization of user messages and data
- **SQL injection prevention**: Prepared for DB integration
- **File upload validation**: Size and type checks
- **CORS security**: Configurable origin controls

## Configuration

### Feature Flags
```python
ENABLE_FILE_PROCESSING = True     # File analysis
ENABLE_CHARTS = True              # Chart generation
ENABLE_WIKIPEDIA = True           # Research capability
ENABLE_ANALYTICS = True           # Usage tracking
THINKING_ENABLED = True           # AI thinking display
```

### Rate Limiting
```python
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS = 100  # requests
RATE_LIMIT_WINDOW = 60     # seconds
```

### Conversation Settings
```python
MAX_CONVERSATION_HISTORY = 50     # Max messages kept
DATABASE_POOL_SIZE = 10           # Ready for DB
CACHE_TTL = 3600                  # Cache lifetime (seconds)
```

## Response Format

All responses follow a consistent format:

### Success Response
```json
{
  "conversation_id": "string",
  "response": "string",
  "model_used": "string",
  "thinking": { ... },
  "confidence": 0.8,
  "file_processed": false,
  "analysis": null,
  "charts": [],
  "suggestions": ["question1", "question2"],
  "metadata": { ... }
}
```

### Error Response
```json
{
  "error": "ERROR_CODE",
  "message": "Error description",
  "details": { ... },
  "suggestion": "Suggested fix",
  "status_code": 400,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Statistical Analysis Details

The data analyzer provides:

#### Measures of Central Tendency
- Mean (average)
- Median (middle value)
- Mode (most frequent value)

#### Measures of Dispersion
- Standard Deviation
- Variance
- Coefficient of Variation (%)
- Range (min, max, span)

#### Distribution Shape
- Skewness (asymmetry measure)
- Kurtosis (tail heaviness measure)

#### Percentiles & Quartiles
- Q1, Q2 (median), Q3
- IQR (Interquartile Range)
- Percentiles: 10, 25, 50, 75, 90, 95, 99

#### Advanced Analysis
- Outlier detection (IQR and Z-score methods)
- Trend detection (up/down/stable)
- Correlation analysis
- Linear regression with R-squared

## Performance Metrics

### Typical Response Times
- Chat with thinking: 200-500ms
- Data analysis: 100-300ms
- Chart generation: 300-800ms
- File processing: 500ms-2s (depends on file size)

### Memory Efficiency
- Conversation storage: ~1KB per message
- Chart generation: Streams to base64
- File processing: Streams with base64

## Logging

Logs are written to:
- File: `logs/app.log`
- Console: stdout

Log levels:
- DEBUG: Detailed information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages

## Future Enhancements

- [x] Database integration (Supabase/PostgreSQL)
- [ ] Redis caching layer
- [x] User authentication & authorization (Supabase)
- [ ] Conversation export (PDF/JSON)
- [x] Advanced NLP features (Sentiment/Entities)
- [ ] Real-time WebSocket support
- [ ] Batch processing API
- [ ] Custom model fine-tuning
- [x] Multi-language support (Slang & Triggers)
- [ ] Advanced rate limiting per user

## Troubleshooting

### Common Issues

**1. PIL/Pillow not available**
```bash
pip install Pillow
```

**2. PyPDF2 import error**
```bash
pip install PyPDF2==4.0.1
```

**3. matplotlib backend issues**
- Already configured to use 'Agg' backend (non-interactive)
- Add to environment if needed: `export MPLBACKEND=Agg`

**4. Port already in use**
```bash
python server.py --port 8001
```

## Contributing

Code organization follows best practices:
- Modular design (each file has single responsibility)
- Type hints throughout
- Comprehensive error handling
- Detailed logging
- Docstrings for all public functions

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions:
1. Check logs in `logs/app.log`
2. Enable DEBUG logging: `LOG_LEVEL=DEBUG`
3. Review API documentation at `/api/docs`

## Statistics

- **Total Lines of Code**: 4,200+
- **Endpoints**: 18+
- **AI Models**: 3 (with specialized personalities)
- **Chart Types**: 7
- **File Types Supported**: 8+
- **Statistical Measures**: 25+
- **Slang Library**: 440+ Authentic Bangalore Slangs
- **Test Coverage Ready**: Yes

---

**MAXY Chat Backend v2.0** - Advanced AI-powered conversational system with thinking display, multi-model architecture, and comprehensive data analysis capabilities.
