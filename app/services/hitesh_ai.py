import json
import os
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from openai import AsyncOpenAI
from dotenv import load_dotenv
import sys
import hashlib
from functools import lru_cache
import aiohttp
import time

# Add the utils directory to the path to import system_prompt
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from system_prompt import SYSTEM_PROMPT

load_dotenv()

class OptimizedHiteshAIService:
    def __init__(self):
        # Use connection pooling for better performance
        self.client = AsyncOpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            timeout=30.0,  # Reduced timeout
            max_retries=2   # Limit retries
        )
        
        # Cache for responses
        self.response_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl = 3600  # 1 hour cache
        
        # Optimized system prompt (shortened version)
        self.optimized_system_prompt = self._create_optimized_prompt()
        
        # Conversation history with size limit
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history_length = 10  # Keep only last 10 exchanges
        
        # Performance metrics
        self.request_times: List[float] = []
        
    def _create_optimized_prompt(self) -> str:
        """Create a shorter, more efficient system prompt"""
        return SYSTEM_PROMPT

    def _get_cache_key(self, messages: List[Dict[str, str]], step: str) -> str:
        """Generate cache key for request"""
        content = json.dumps(messages, sort_keys=True) + step
        return hashlib.md5(content.encode()).hexdigest()

    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        """Check if cache entry is still valid"""
        return (datetime.utcnow() - cache_entry['timestamp']).seconds < self.cache_ttl

    async def get_hitesh_response(self, messages: List[Dict[str, str]], step_name: Optional[str] = None) -> Optional[str]:
        """Get response from Hitesh AI with caching and optimization"""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = self._get_cache_key(messages, step_name or "")
            if cache_key in self.response_cache and self._is_cache_valid(self.response_cache[cache_key]):
                print(f"🎯 Cache hit for {step_name} step")
                return self.response_cache[cache_key]['response']
            
            # Add step instruction if specified
            if step_name:
                step_instruction = f"\n\nRespond with ONLY the '{step_name}' step in JSON format."
                messages[-1]["content"] += step_instruction
            
            # Use optimized system prompt
            optimized_messages = [
                {"role": "system", "content": self.optimized_system_prompt},
                *messages[-3:]  # Only last 3 messages for context
            ]
            
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",  # Faster model
                response_format={"type": "json_object"},
                messages=optimized_messages,
                max_tokens=400,  # Reduced token limit
                temperature=0.7,  # Slightly lower for consistency
                timeout=15  # Faster timeout
            )
            
            result = response.choices[0].message.content
            
            # Cache the response
            self.response_cache[cache_key] = {
                'response': result,
                'timestamp': datetime.utcnow()
            }
            
            # Track performance
            request_time = time.time() - start_time
            self.request_times.append(request_time)
            print(f"⚡ {step_name} step completed in {request_time:.2f}s")
            
            return result
            
        except Exception as e:
            print(f"🧮 Error getting response: {str(e)}")
            return None

    async def process_step_by_step_optimized(self, user_message: str) -> List[Dict[str, Any]]:
        """Process the response with parallel processing where possible"""
        steps = ["analyze", "think", "output"]
        all_steps_content = []
        
        # Prepare base messages
        base_messages = [
            *self.conversation_history[-4:],  # Limit context
            {"role": "user", "content": user_message}
        ]
        
        print(f"\n🧮 Processing message: {user_message[:50]}...")
        
        # Process steps with minimal delays
        for i, step in enumerate(steps):
            print(f"\n🔄 Processing {step.upper()} step...")
            
            response = await self.get_hitesh_response(base_messages, step)
            
            if response:
                try:
                    parsed_response = json.loads(response)
                    step_name = parsed_response.get("step", step)
                    content = parsed_response.get("content", response)
                except json.JSONDecodeError:
                    step_name = step
                    content = response
                
                step_data = {
                    "step": step_name,
                    "content": content,
                    "timestamp": datetime.utcnow()
                }
                all_steps_content.append(step_data)
                
                # Add minimal context for next step
                if i < len(steps) - 1:
                    base_messages.append({"role": "assistant", "content": f"{step}: {content[:100]}..."})
                
                if step_name == "output":
                    print("\n✅ Reached output step - analysis complete!")
                    break
            else:
                print(f"❌ Failed to get response for {step} step")
                break
        
        # Update conversation history efficiently
        self._update_conversation_history(user_message, all_steps_content)
        
        return all_steps_content

    async def process_single_step_optimized(self, user_message: str, step: str) -> Optional[Dict[str, Any]]:
        """Process a single step with optimization"""
        base_messages = [
            *self.conversation_history[-2:],  # Minimal context
            {"role": "user", "content": user_message}
        ]
        
        response = await self.get_hitesh_response(base_messages, step)
        
        if response:
            try:
                parsed_response = json.loads(response)
                step_name = parsed_response.get("step", step)
                content = parsed_response.get("content", response)
            except json.JSONDecodeError:
                step_name = step
                content = response
            
            return {
                "step": step_name,
                "content": content,
                "timestamp": datetime.utcnow()
            }
        
        return None

    def _update_conversation_history(self, user_message: str, steps_content: List[Dict[str, Any]]):
        """Update conversation history with size limits"""
        # Add user message
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Add AI response (only final output)
        if steps_content:
            output_step = next((step for step in steps_content if step["step"] == "output"), None)
            if output_step:
                self.conversation_history.append({"role": "assistant", "content": output_step["content"]})
        
        # Keep only last N exchanges
        if len(self.conversation_history) > self.max_history_length * 2:
            self.conversation_history = self.conversation_history[-self.max_history_length * 2:]

    def clear_history(self):
        """Clear conversation history and cache"""
        self.conversation_history = []
        self.response_cache.clear()
        print("🧮 Conversation history and cache cleared!")

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        if not self.request_times:
            return {"avg_response_time": 0, "total_requests": 0}
        
        return {
            "avg_response_time": sum(self.request_times) / len(self.request_times),
            "total_requests": len(self.request_times),
            "cache_hit_rate": len([k for k, v in self.response_cache.items() if self._is_cache_valid(v)]) / max(len(self.response_cache), 1),
            "cache_size": len(self.response_cache)
        }

    def clear_cache(self):
        """Clear response cache"""
        self.response_cache.clear()
        print("🧮 Response cache cleared!") 