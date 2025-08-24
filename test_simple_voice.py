#!/usr/bin/env python3
"""
Test đơn giản để kiểm tra voice synthesis
"""

import os
import sys
sys.path.append('.')

def test_simple_voice():
    print("🔍 Testing simple voice synthesis...")
    
    try:
        from lecture_input import convert_text_to_audio_with_voice
        
        user_id = "current_user"
        voice_id = "myVoice"
        test_text = "Xin chào các em."
        
        print(f"Testing with voice: {voice_id}")
        result = convert_text_to_audio_with_voice(test_text, user_id, voice_id)
        
        if result and os.path.exists(result):
            print(f"✅ Success: {result}")
            return True
        else:
            print(f"❌ Failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_voice()
    print(f"\nResult: {'✅ Success' if success else '❌ Failed'}")

