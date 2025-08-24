#!/usr/bin/env python3
"""
Test script để kiểm tra việc load XTTS v2
"""

import os
import sys
sys.path.append('.')

def test_xtts_loading():
    print("🔍 Testing XTTS v2 loading...")
    
    try:
        from src.voice.enrollment import load_xtts
        
        print("📦 Loading XTTS model...")
        model, model_type = load_xtts()
        
        print(f"✅ Model loaded successfully!")
        print(f"🤖 Model type: {model_type}")
        print(f"📦 Model object: {type(model)}")
        
        if model_type == "xtts_v2":
            print("🎉 XTTS v2 loaded successfully!")
            return True
        else:
            print("⚠️ Fallback model loaded (Tacotron2)")
            return False
            
    except Exception as e:
        print(f"❌ Error loading XTTS: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_synthesis():
    print("\n🔍 Testing voice synthesis...")
    
    try:
        from src.voice.store import has_voice, list_voices
        from lecture_input import convert_text_to_audio_with_voice
        
        user_id = "current_user"
        voice_id = "myVoice"
        
        if not has_voice(user_id, voice_id):
            print(f"❌ Voice not found: {voice_id}")
            return False
        
        print(f"✅ Voice found: {voice_id}")
        
        test_text = "Xin chào các em, hôm nay chúng ta sẽ học bài mới."
        
        result = convert_text_to_audio_with_voice(test_text, user_id, voice_id)
        
        if result and os.path.exists(result):
            print(f"✅ Voice synthesis successful: {result}")
            return True
        else:
            print(f"❌ Voice synthesis failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error in voice synthesis: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing XTTS v2 and voice synthesis...")
    
    xtts_loaded = test_xtts_loading()
    synthesis_worked = test_voice_synthesis()
    
    print(f"\n📊 Test Results:")
    print(f"XTTS v2 loaded: {'✅' if xtts_loaded else '❌'}")
    print(f"Voice synthesis: {'✅' if synthesis_worked else '❌'}")
    
    if xtts_loaded and synthesis_worked:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check the logs above.")

