#!/usr/bin/env python3
"""
Test script to verify backend imports work correctly
"""

import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test all imports"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from app.main import app
        print("✅ app.main imported successfully")
        
        from app.routes import chat
        print("✅ app.routes.chat imported successfully")
        
        from app.services.chat_service import OptimizedChatService
        print("✅ app.services.chat_service imported successfully")
        
        from app.services.hitesh_ai import OptimizedHiteshAIService
        print("✅ app.services.hitesh_ai imported successfully")
        
        from app.models.chat import ChatRequest, ChatResponse, ProcessingStep
        print("✅ app.models.chat imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 