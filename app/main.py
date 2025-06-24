from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import os
from dotenv import load_dotenv

# Import routes
from .routes import chat

# Load environment variables
load_dotenv()

# Create FastAPI app with optimized settings
app = FastAPI(
    title="Hitesh AI Chat API",
    description="Backend API for Hitesh AI Chat Flow",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add GZip compression for better performance
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Configure CORS with optimized settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Add trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Performance monitoring middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include routers
app.include_router(chat.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "⚡ Namaste! Welcome to Hitesh AI Chat API",
        "description": "Your tech mentor and chai companion",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/chat/health"
    }

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Hitesh AI Chat API",
        "version": "1.0.0",
        "description": "Backend API for Hitesh AI Chat Flow",
        "endpoints": {
            "chat": {
                "send": "POST /api/chat/send",
                "stream": "POST /api/chat/stream", 
                "history": "GET /api/chat/history",
                "clear_history": "DELETE /api/chat/history",
                "health": "GET /api/chat/health"
            }
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": "Something went wrong on our end. Please try again.",
            "details": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else None
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload for better performance
        log_level="info",
        workers=1,  # Single worker for development
        loop="asyncio",
        http="httptools"  # Faster HTTP parser
    ) 