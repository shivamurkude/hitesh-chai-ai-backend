# 🚀 Hitesh AI Chat API

> **Namaste! Welcome to Hitesh AI Chat API** - Your tech mentor and chai companion 🫖

A high-performance FastAPI backend that simulates conversations with **Hitesh Choudhary** - India's beloved tech educator, YouTuber, and automation evangelist. This API provides an interactive chat experience with step-by-step processing, streaming responses, and optimized performance.

## 🌟 Features

### ✨ Core Features
- **🤖 AI-Powered Chat**: Simulates Hitesh Choudhary's personality and teaching style
- **🔄 Step-by-Step Processing**: Analyze → Think → Output workflow
- **📡 Real-time Streaming**: Server-Sent Events for live response streaming
- **💾 Intelligent Caching**: Redis-based caching for improved performance
- **📊 Performance Monitoring**: Built-in metrics and analytics
- **🔒 Session Management**: Multi-user session support
- **🏥 Health Checks**: Comprehensive health monitoring

### 🎯 Technical Features
- **⚡ High Performance**: Optimized with async/await and connection pooling
- **🛡️ Security**: CORS, trusted host middleware, and input validation
- **📈 Scalable**: Docker containerized with Gunicorn workers
- **🔧 Developer Friendly**: Auto-generated API documentation
- **🌐 Production Ready**: Deployed on Render with environment configuration

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   OpenAI API    │
│   (React/Vue)   │◄──►│   Backend       │◄──►│   GPT-4o-mini   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Redis Cache   │
                       │   (Optional)    │
                       └─────────────────┘
```

### 📁 Project Structure
```
render-deploy/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat.py            # Pydantic models for data validation
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chat.py            # API endpoints and routing
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py    # Main chat business logic
│   │   └── hitesh_ai.py       # OpenAI integration and AI processing
│   └── utils/
│       ├── __init__.py
│       └── system_prompt.py   # Hitesh's personality and prompts
├── Dockerfile                 # Container configuration
├── requirements.txt           # Python dependencies
├── render.yaml               # Render deployment config
├── build.sh                  # Build script
├── start.sh                  # Startup script
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API Key
- Docker (optional)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd render-deploy
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
DEBUG=false
LOG_LEVEL=info
```

### 4. Run the Application

#### Development Mode
```bash
python -m app.main
```

#### Production Mode (Docker)
```bash
docker build -t hitesh-ai-api .
docker run -p 8000:8000 --env-file .env hitesh-ai-api
```

#### Using Scripts
```bash
chmod +x build.sh start.sh
./build.sh
./start.sh
```

### 5. Access the API
- **API Base URL**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/chat/health`

## 📚 API Endpoints

### 🔗 Core Endpoints

#### `GET /`
Welcome endpoint with API information
```json
{
  "message": "⚡ Namaste! Welcome to Hitesh AI Chat API",
  "description": "Your tech mentor and chai companion",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/api/chat/health"
}
```

#### `POST /api/chat/send`
Send a message and get a complete response with processing steps
```json
{
  "content": "Sir mujhe backend development kaise start karna hai?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "success": true,
  "message": {
    "id": "uuid",
    "type": "ai",
    "content": "Start with Python + FastAPI ya Node.js + Express...",
    "timestamp": "2024-01-01T00:00:00Z"
  },
  "processing_steps": [
    {
      "step": "analyze",
      "content": "User backend start karna chahta hai...",
      "timestamp": "2024-01-01T00:00:00Z"
    },
    {
      "step": "think",
      "content": "Main bhi jab start kiya tha...",
      "timestamp": "2024-01-01T00:00:00Z"
    },
    {
      "step": "output",
      "content": "Start with Python + FastAPI...",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### `POST /api/chat/stream`
Stream processing steps in real-time using Server-Sent Events
```bash
curl -X POST "http://localhost:8000/api/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{"content": "LangGraph kya hota hai?"}'
```

**Stream Response:**
```
data: {"step": "analyze", "content": "User LangGraph ke baare mein puch raha hai...", "timestamp": "2024-01-01T00:00:00Z", "is_complete": false}

data: {"step": "think", "content": "LangGraph ek powerful tool hai...", "timestamp": "2024-01-01T00:00:00Z", "is_complete": false}

data: {"step": "output", "content": "LangGraph ek way hai nodes ke through flow banane ka...", "timestamp": "2024-01-01T00:00:00Z", "is_complete": true}
```

### 🔧 Utility Endpoints

#### `GET /api/chat/history`
Get chat history for a session
```bash
GET /api/chat/history?session_id=your-session-id
```

#### `DELETE /api/chat/history`
Clear chat history for a session
```bash
DELETE /api/chat/history?session_id=your-session-id
```

#### `GET /api/chat/health`
Health check endpoint
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

#### `GET /api/chat/performance`
Get performance statistics
```json
{
  "success": true,
  "performance_stats": {
    "total_requests": 150,
    "avg_response_time": 2.3,
    "cache_hit_rate": 0.75
  }
}
```

#### `POST /api/chat/cache/clear`
Clear all caches
```bash
POST /api/chat/cache/clear
```

#### `GET /api/chat/cache/stats`
Get cache statistics
```json
{
  "success": true,
  "cache_stats": {
    "cache_size": 50,
    "cache_hit_rate": 0.75,
    "avg_response_time": 2.3,
    "total_requests": 150
  }
}
```

## 🧠 How It Works

### 1. **Message Processing Flow**
```
User Message → Chat Service → Hitesh AI Service → OpenAI API → Response Processing → Caching → Response
```

### 2. **Step-by-Step Processing**
The AI processes each message through three distinct steps:

1. **🔍 Analyze**: Understand and break down the user's query
2. **💭 Think**: Reflect on the approach using personal experience and reasoning
3. **📤 Output**: Present the teaching or recommendation

### 3. **Caching Strategy**
- **Response Cache**: Caches AI responses for 1 hour
- **Session Cache**: Maintains conversation context
- **Performance Cache**: Stores frequently accessed data

### 4. **Performance Optimizations**
- **Async Processing**: Non-blocking I/O operations
- **Connection Pooling**: Reuses HTTP connections
- **Token Optimization**: Reduced context window for faster responses
- **Parallel Processing**: Where possible, processes steps concurrently

## 🎨 Hitesh's Personality

The AI simulates Hitesh Choudhary's authentic personality:

### 🗣️ **Speaking Style**
- **Hinglish**: Natural mix of Hindi and English
- **Casual & Relatable**: Like chatting with a friend over chai
- **Encouraging**: Always supportive and motivating
- **Storytelling**: Uses analogies and real-life examples

### 🎯 **Core Topics**
- Backend Development (FastAPI, Express, MongoDB)
- API Development and Authentication
- AI Tools (LangGraph, LangChain, n8n)
- Automation and Workflow Tools
- Career Advice and Tech Education
- YouTube Content Creation
- Productivity and Creator Life

### 💬 **Sample Conversations**
```
User: "Sir mujhe backend development kaise start karna hai?"
Hitesh: "Arey bhai, easy hai! Start with Python + FastAPI ya Node.js + Express. 
        Ek 'Hello World API' banao, fir connect karo MongoDB se. 
        Heroku ya Render pe deploy karke confidence le aao. 
        Main bhi pehle sochta tha yeh kya bakchodi hai… 
        lekin jab kiya na, toh maza aa gaya! 😄"
```

## 🚀 Deployment

### Render Deployment
The project is configured for easy deployment on Render:

1. **Connect Repository**: Link your GitHub repository to Render
2. **Environment Variables**: Set `OPENAI_API_KEY` in Render dashboard
3. **Auto Deploy**: Render automatically builds and deploys on push

### Docker Deployment
```bash
# Build image
docker build -t hitesh-ai-api .

# Run container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e DEBUG=false \
  --name hitesh-ai-container \
  hitesh-ai-api
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `info` |

## 🛠️ Development

### Running Tests
```bash
python -m pytest test_backend.py
```

### Code Structure
- **Models**: Pydantic models for data validation
- **Routes**: FastAPI route handlers
- **Services**: Business logic and external API integration
- **Utils**: Helper functions and system prompts

### Adding New Features
1. **New Endpoint**: Add to `app/routes/chat.py`
2. **New Model**: Create in `app/models/chat.py`
3. **New Service**: Add to `app/services/` directory
4. **Update Tests**: Modify `test_backend.py`

## 📊 Performance Metrics

The API includes built-in performance monitoring:

- **Response Time**: Average processing time per request
- **Cache Hit Rate**: Percentage of cached responses
- **Request Count**: Total number of processed requests
- **Error Rate**: Percentage of failed requests

## 🔧 Configuration

### Production Settings
- **Workers**: 1 worker for optimal performance
- **Timeout**: 30 seconds for OpenAI API calls
- **Cache TTL**: 1 hour for response caching
- **Max History**: 10 messages per session

### Development Settings
- **Auto-reload**: Disabled for better performance
- **Debug Mode**: Controlled via environment variable
- **Logging**: Configurable log levels

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Hitesh Choudhary**: For inspiring this project with his teaching style
- **OpenAI**: For providing the GPT-4o-mini API
- **FastAPI**: For the excellent web framework
- **Render**: For hosting and deployment services

## 📞 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Check `/docs` endpoint for interactive API docs
- **Health**: Monitor `/api/chat/health` for system status

---

**Made with ❤️ and lots of ☕ chai**

*"Build karo, break karo, repeat karo!" - Hitesh Choudhary*
