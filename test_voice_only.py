#!/usr/bin/env python3
"""
Test chỉ kiểm tra voice synthesis không phụ thuộc gradio
"""

import os
import sys
sys.path.append('.')

def test_voice_only():
    print("🔍 Testing voice synthesis only...")
    
    try:
        # Import trực tiếp từ voice modules
        from src.voice.store import has_voice, load_profile
        from src.voice.tts_engine import synthesize
        
        user_id = "current_user"
        voice_id = "myVoice"
        test_text = "Xin chào các em."
        
        print(f"Checking voice: {voice_id}")
        
        if not has_voice(user_id, voice_id):
            print(f"❌ Voice not found: {voice_id}")
            return False
        
        print(f"✅ Voice found: {voice_id}")
        
        # Lấy thông tin voice
        emb, meta = load_profile(user_id, voice_id)
        voice_language = meta.get('lang_hint', 'vi')
        model_type = meta.get('model_type', 'unknown')
        
        print(f"🌐 Voice language: {voice_language}")
        print(f"🤖 Model type: {model_type}")
        
        # Test synthesize
        print("🎤 Testing synthesize...")
        result = synthesize(test_text, user_id, voice_id, voice_language)
        
        if result and os.path.exists(result):
            print(f"✅ Synthesize success: {result}")
            return True
        else:
            print(f"❌ Synthesize failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_voice_only()
    print(f"\nResult: {'✅ Success' if success else '❌ Failed'}")

