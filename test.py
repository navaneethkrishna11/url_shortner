#!/usr/bin/env python3
"""
Test script to check imports
"""

def test_imports():
    try:
        print("🔍 Testing imports...")
        
        print("  ✓ Testing FastAPI...")
        from fastapi import FastAPI
        
        print("  ✓ Testing app config...")
        from app.config import settings
        print(f"    - Host: {settings.HOST}")
        print(f"    - Port: {settings.PORT}")
        print(f"    - Debug: {settings.DEBUG}")
        
        print("  ✓ Testing app models...")
        from app.models import URLCreate, URLResponse
        
        print("  ✓ Testing app utils...")
        from app.utils import generate_short_code, is_valid_url
        
        print("  ✓ Testing main app...")
        from app.main import app
        
        print("✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n🚀 Ready to run the server!")
        print("Run: python run.py")
    else:
        print("\n❌ Fix the errors above first")
    
    input("\nPress Enter to exit...")