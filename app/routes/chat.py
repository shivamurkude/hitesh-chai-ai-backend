from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import StreamingResponse
from typing import Optional
import json
import time
from ..models.chat import (
    ChatRequest, 
    ChatResponse, 
    ChatHistoryResponse, 
    StreamStep,
    HealthResponse
)
from ..services.chat_service import OptimizedChatService
import asyncio
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Initialize optimized chat service
chat_service = OptimizedChatService()

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest, response: Response):
    """
    Send a message to Hitesh AI and get a response with processing steps
    """
    start_time = time.time()
    
    try:
        result = await chat_service.process_message(
            content=request.content,
            session_id=request.session_id
        )
        
        # Add performance header to response
        processing_time = time.time() - start_time
        response.headers["X-Processing-Time"] = f"{processing_time:.3f}s"
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.post("/stream")
async def stream_message(request: ChatRequest):
    """
    Stream processing steps in real-time using Server-Sent Events
    """
    async def generate():
        start_time = time.time()
        
        try:
            async for step in chat_service.stream_processing_steps(
                content=request.content,
                session_id=request.session_id
            ):
                # Format as Server-Sent Event
                data = json.dumps({
                    "step": step.step,
                    "content": step.content,
                    "timestamp": step.timestamp.isoformat(),
                    "is_complete": step.is_complete
                })
                yield f"data: {data}\n\n"
                
                # Add a small delay for better UX
                await asyncio.sleep(0.1)
                
        except Exception as e:
            error_data = json.dumps({
                "step": "error",
                "content": f"Error: {str(e)}",
                "timestamp": "2024-01-01T00:00:00Z",
                "is_complete": True
            })
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )

@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(session_id: Optional[str] = None):
    """
    Get chat history for a session
    """
    try:
        messages = chat_service.get_chat_history(session_id=session_id)
        return ChatHistoryResponse(
            success=True,
            messages=messages
        )
    except Exception as e:
        return ChatHistoryResponse(
            success=False,
            error=str(e)
        )

@router.delete("/history")
async def clear_chat_history(session_id: Optional[str] = None):
    """
    Clear chat history for a session
    """
    try:
        chat_service.clear_chat_history(session_id=session_id)
        return {"success": True, "message": "Chat history cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )

@router.get("/performance")
async def get_performance_stats():
    """
    Get performance statistics
    """
    try:
        stats = chat_service.get_performance_stats()
        return {
            "success": True,
            "performance_stats": stats
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/cache/clear")
async def clear_cache():
    """
    Clear all caches
    """
    try:
        chat_service.clear_cache()
        return {"success": True, "message": "All caches cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")

@router.get("/cache/stats")
async def get_cache_stats():
    """
    Get cache statistics
    """
    try:
        ai_stats = chat_service.hitesh_ai.get_performance_stats()
        return {
            "success": True,
            "cache_stats": {
                "cache_size": ai_stats.get("cache_size", 0),
                "cache_hit_rate": ai_stats.get("cache_hit_rate", 0),
                "avg_response_time": ai_stats.get("avg_response_time", 0),
                "total_requests": ai_stats.get("total_requests", 0)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/stream/test")
async def test_stream():
    """
    Test streaming endpoint to verify SSE is working
    """
    async def generate():
        steps = [
            {"step": "test", "content": "Testing streaming...", "is_complete": False},
            {"step": "test", "content": "Streaming is working!", "is_complete": True}
        ]
        
        for i, step in enumerate(steps):
            data = json.dumps({
                "step": step["step"],
                "content": step["content"],
                "timestamp": datetime.utcnow().isoformat(),
                "is_complete": step["is_complete"]
            })
            yield f"data: {data}\n\n"
            
            if i < len(steps) - 1:
                await asyncio.sleep(1)
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "X-Accel-Buffering": "no",
        }
    ) 