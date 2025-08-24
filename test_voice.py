#!/usr/bin/env python3
"""
Test script để kiểm tra voice synthesis
"""

import os
import sys
sys.path.append('.')

from src.voice.store import has_voice, list_voices
from src.voice.tts_engine import synthesize
from lecture_input import convert_text_to_audio_with_voice

def test_voice_synthesis():
    print("🔍 Testing voice synthesis...")
    
    # Kiểm tra voice có tồn tại không
    user_id = "current_user"
    voice_id = "myVoice"
    
    print(f"📁 Checking voice: {user_id}/{voice_id}")
    print(f"✅ Voice exists: {has_voice(user_id, voice_id)}")
    
    # Liệt kê tất cả voices
    voices = list_voices(user_id)
    print(f"📋 Available voices: {[v['voice_id'] for v in voices]}")
    
    # Test synthesize trực tiếp
    print("\n🎤 Testing direct synthesize...")
    test_text = "Xin chào các em, hôm nay chúng ta sẽ học bài mới."
    
    try:
        result = synthesize(test_text, user_id, voice_id, "vi")
        print(f"🔍 synthesize() result: {result}")
        if result and os.path.exists(result):
            print(f"✅ Direct synthesize successful: {result}")
        else:
            print(f"❌ Direct synthesize failed")
    except Exception as e:
        print(f"❌ Direct synthesize error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test convert_text_to_audio_with_voice
    print("\n🎤 Testing convert_text_to_audio_with_voice...")
    try:
        result = convert_text_to_audio_with_voice(test_text, user_id, voice_id, "vi")
        print(f"🔍 convert_text_to_audio_with_voice() result: {result}")
        if result and os.path.exists(result):
            print(f"✅ convert_text_to_audio_with_voice successful: {result}")
        else:
            print(f"❌ convert_text_to_audio_with_voice failed")
    except Exception as e:
        print(f"❌ convert_text_to_audio_with_voice error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_voice_synthesis()

