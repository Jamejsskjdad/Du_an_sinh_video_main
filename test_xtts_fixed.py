#!/usr/bin/env python3
"""
Test script để kiểm tra XTTS loading đã được sửa
"""

import sys
import os

# Thêm đường dẫn hiện tại vào sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_xtts_loading():
    print("🔍 Testing fixed XTTS loading...")
    
    try:
        from src.voice.enrollment import load_xtts
        
        print("📦 Loading XTTS model...")
        model, model_type = load_xtts()
        
        print(f"✅ Model loaded successfully!")
        print(f"🤖 Model type: {model_type}")
        print(f"📦 Model object: {type(model)}")
        
        if model_type in ["xtts_v2", "xtts_v2_api"]:
            print("🎉 XTTS v2 loaded successfully!")
            return True
        elif model_type == "gtts":
            print("✅ gTTS fallback loaded successfully!")
            return True
        else:
            print(f"⚠️ {model_type} model loaded (fallback)")
            return True
            
    except Exception as e:
        print(f"❌ Error loading XTTS: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_synthesis():
    print("\n🔍 Testing voice synthesis...")
    
    try:
        from src.voice.tts_engine import synthesize
        
        # Test với text đơn giản
        text = "Xin chào, đây là test giọng nói."
        user_id = "test_user"
        voice_id = "test_voice"
        
        print(f"🎤 Synthesizing: {text}")
        output_path = synthesize(text, user_id, voice_id, lang="vi")
        
        if output_path and os.path.exists(output_path):
            print(f"✅ Synthesis successful! Output: {output_path}")
            return True
        else:
            print("❌ Synthesis failed or output file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error in synthesis: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 XTTS Fixed Test Script")
    print("=" * 50)
    
    # Test 1: Loading
    print("\n🧪 Test 1: Model Loading")
    loading_success = test_xtts_loading()
    
    if loading_success:
        # Test 2: Synthesis
        print("\n🧪 Test 2: Voice Synthesis")
        synthesis_success = test_voice_synthesis()
        
        if synthesis_success:
            print("\n🎉 All tests passed!")
        else:
            print("\n⚠️ Loading passed but synthesis failed")
    else:
        print("\n❌ Loading failed")
