import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from .hitesh_ai import OptimizedHiteshAIService
from ..models.chat import Message, ProcessingStep, ChatResponse, StreamStep

class OptimizedChatService:
    def __init__(self):
        self.hitesh_ai = OptimizedHiteshAIService()
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        # Performance tracking
        self.request_count = 0
        self.total_processing_time = 0.0
        
    def create_session(self, session_id: Optional[str] = None) -> str:
        """Create a new chat session"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "message_count": 0
        }
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information"""
        return self.sessions.get(session_id)
    
    def update_session_activity(self, session_id: str):
        """Update session last activity"""
        if session_id in self.sessions:
            self.sessions[session_id]["last_activity"] = datetime.utcnow()
            self.sessions[session_id]["message_count"] += 1
    
    async def process_message(self, content: str, session_id: Optional[str] = None) -> ChatResponse:
        """Process a user message with optimized performance"""
        start_time = asyncio.get_event_loop().time()
        self.request_count += 1
        
        try:
            # Create session if not provided
            if not session_id:
                session_id = self.create_session()
            
            # Update session activity
            self.update_session_activity(session_id)
            
            # Process the message with optimized Hitesh AI
            processing_steps = await self.hitesh_ai.process_step_by_step_optimized(content)
            
            # Get the final output from processing steps
            final_content = ""
            if processing_steps:
                # Find the output step
                output_step = next((step for step in processing_steps if step["step"] == "output"), None)
                if output_step:
                    final_content = output_step["content"]
                else:
                    # If no output step, use the last step's content
                    final_content = processing_steps[-1]["content"]
            
            # Create AI message
            ai_message = Message(
                type="ai",
                content=final_content,
                timestamp=datetime.utcnow()
            )
            
            # Convert processing steps to Pydantic models
            pydantic_steps = []
            for step in processing_steps:
                pydantic_step = ProcessingStep(
                    step=step["step"],
                    content=step["content"],
                    timestamp=step["timestamp"]
                )
                pydantic_steps.append(pydantic_step)
            
            # Track performance
            processing_time = asyncio.get_event_loop().time() - start_time
            self.total_processing_time += processing_time
            
            print(f"⚡ Request {self.request_count} completed in {processing_time:.2f}s")
            
            return ChatResponse(
                success=True,
                message=ai_message,
                processing_steps=pydantic_steps
            )
            
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return ChatResponse(
                success=False,
                message=Message(
                    type="ai",
                    content="Sorry, I'm having trouble processing your request right now. Please try again.",
                    timestamp=datetime.utcnow()
                ),
                error=str(e)
            )
    
    async def stream_processing_steps(self, content: str, session_id: Optional[str] = None):
        """Stream processing steps with optimized performance"""
        start_time = asyncio.get_event_loop().time()
        self.request_count += 1
        
        try:
            # Create session if not provided
            if not session_id:
                session_id = self.create_session()
            
            # Update session activity
            self.update_session_activity(session_id)
            
            steps = ["analyze", "think", "output"]
            
            for i, step in enumerate(steps):
                try:
                    # Process single step with optimization
                    step_result = await self.hitesh_ai.process_single_step_optimized(content, step)
                    
                    if step_result:
                        # Create stream step
                        stream_step = StreamStep(
                            step=step_result["step"],
                            content=step_result["content"],
                            timestamp=step_result["timestamp"],
                            is_complete=(i == len(steps) - 1)  # Last step
                        )
                        
                        yield stream_step
                        
                        # Reduced delay between steps for better UX
                        if i < len(steps) - 1:
                            await asyncio.sleep(0.1)  # Reduced delay for faster streaming
                    else:
                        # If step failed, yield error step
                        error_step = StreamStep(
                            step=step,
                            content=f"Failed to process {step} step",
                            timestamp=datetime.utcnow(),
                            is_complete=True
                        )
                        yield error_step
                        break
                        
                except Exception as step_error:
                    print(f"Error processing {step} step: {str(step_error)}")
                    error_step = StreamStep(
                        step=step,
                        content=f"Error processing {step} step: {str(step_error)}",
                        timestamp=datetime.utcnow(),
                        is_complete=True
                    )
                    yield error_step
                    break
            
            # Track performance
            processing_time = asyncio.get_event_loop().time() - start_time
            self.total_processing_time += processing_time
            print(f"⚡ Streaming request {self.request_count} completed in {processing_time:.2f}s")
            
        except Exception as e:
            print(f"Error streaming steps: {str(e)}")
            error_step = StreamStep(
                step="output",
                content="Sorry, I encountered an error while processing your request.",
                timestamp=datetime.utcnow(),
                is_complete=True
            )
            yield error_step
    
    def get_chat_history(self, session_id: Optional[str] = None) -> List[Message]:
        """Get chat history for a session"""
        # For now, return the conversation history from Hitesh AI service
        # In a real application, you'd store this in a database
        history = self.hitesh_ai.get_history()
        
        messages = []
        for i, msg in enumerate(history):
            if msg["role"] == "user":
                message = Message(
                    type="user",
                    content=msg["content"],
                    timestamp=datetime.utcnow()  # In real app, store actual timestamps
                )
                messages.append(message)
            elif msg["role"] == "assistant":
                # Try to parse the assistant response to extract the final output
                try:
                    import json
                    parsed = json.loads(msg["content"])
                    if isinstance(parsed, list) and len(parsed) > 0:
                        # Get the output step content
                        output_step = next((step for step in parsed if step.get("step") == "output"), None)
                        if output_step:
                            content = output_step.get("content", msg["content"])
                        else:
                            content = msg["content"]
                    else:
                        content = msg["content"]
                except:
                    content = msg["content"]
                
                message = Message(
                    type="ai",
                    content=content,
                    timestamp=datetime.utcnow()  # In real app, store actual timestamps
                )
                messages.append(message)
        
        return messages
    
    def clear_chat_history(self, session_id: Optional[str] = None):
        """Clear chat history"""
        self.hitesh_ai.clear_history()
        if session_id and session_id in self.sessions:
            self.sessions[session_id]["message_count"] = 0
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        ai_stats = self.hitesh_ai.get_performance_stats()
        
        return {
            "total_requests": self.request_count,
            "avg_processing_time": self.total_processing_time / max(self.request_count, 1),
            "total_processing_time": self.total_processing_time,
            "ai_service_stats": ai_stats,
            "active_sessions": len(self.sessions)
        }
    
    def clear_cache(self):
        """Clear all caches"""
        self.hitesh_ai.clear_cache()
        print("🧮 All caches cleared!") 