#!/usr/bin/env python3
"""
Test script để kiểm tra tính năng bắt buộc giọng nhân bản
"""

import os
import sys
sys.path.append('.')

from src.voice.store import has_voice, list_voices
from lecture_input import convert_text_to_audio_with_voice

def test_voice_required():
    print("🔍 Testing voice required functionality...")
    
    # Test 1: Kiểm tra voice có tồn tại
    user_id = "current_user"
    voice_id = "myVoice"
    
    print(f"📁 Checking voice: {user_id}/{voice_id}")
    print(f"✅ Voice exists: {has_voice(user_id, voice_id)}")
    
    # Test 2: Test với voice hợp lệ
    print("\n🎤 Testing with valid voice...")
    test_text = "Xin chào các em, hôm nay chúng ta sẽ học bài mới."
    
    try:
        result = convert_text_to_audio_with_voice(test_text, user_id, voice_id)
        print(f"✅ Success with valid voice: {result}")
    except Exception as e:
        print(f"❌ Error with valid voice: {e}")
    
    # Test 3: Test với voice không tồn tại
    print("\n🎤 Testing with invalid voice...")
    invalid_voice_id = "non_existent_voice"
    
    try:
        result = convert_text_to_audio_with_voice(test_text, user_id, invalid_voice_id)
        print(f"❌ Should have failed but didn't: {result}")
    except Exception as e:
        print(f"✅ Correctly failed with invalid voice: {e}")
    
    # Test 4: Test với voice_id = None
    print("\n🎤 Testing with None voice_id...")
    
    try:
        result = convert_text_to_audio_with_voice(test_text, user_id, None)
        print(f"❌ Should have failed but didn't: {result}")
    except Exception as e:
        print(f"✅ Correctly failed with None voice_id: {e}")

if __name__ == "__main__":
    test_voice_required()

