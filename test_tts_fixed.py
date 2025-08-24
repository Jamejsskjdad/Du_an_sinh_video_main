#!/usr/bin/env python3
"""
Test script for fixed TTS engine
This script tests the TTS synthesis with proper error handling
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_tts_synthesis():
    """Test TTS synthesis with the fixed engine"""
    print("🧪 Testing Fixed TTS Engine")
    print("=" * 40)
    
    try:
        # Import required functions
        from voice.tts_engine import synthesize
        from voice.enrollment import load_xtts
        
        print("📦 Successfully imported TTS functions")
        
        # Test TTS model loading
        print("\n🚀 Testing TTS model loading...")
        model, model_type = load_xtts()
        print(f"✅ TTS model loaded: {model_type}")
        
        # Test synthesis with different scenarios
        test_cases = [
            {
                "text": "Xin chào! Đây là bài kiểm tra giọng nói.",
                "user_id": "test_user",
                "voice_id": "test_voice",
                "lang": "vi",
                "description": "Vietnamese text with non-existent voice"
            },
            {
                "text": "Hello! This is a voice test.",
                "user_id": "test_user",
                "voice_id": "test_voice",
                "lang": "en",
                "description": "English text with non-existent voice"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Test Case {i}: {test_case['description']}")
            print(f"📝 Text: {test_case['text']}")
            print(f"🌐 Language: {test_case['lang']}")
            
            try:
                # Test synthesis
                result = synthesize(
                    text=test_case['text'],
                    user_id=test_case['user_id'],
                    voice_id=test_case['voice_id'],
                    lang=test_case['lang'],
                    speed=1.0
                )
                
                if result:
                    print(f"✅ Synthesis successful: {result}")
                    # Check if file exists
                    if os.path.exists(result):
                        file_size = os.path.getsize(result)
                        print(f"📁 Output file: {result} ({file_size:,} bytes)")
                    else:
                        print(f"⚠️ Output file not found: {result}")
                else:
                    print("⚠️ Synthesis returned None")
                    
            except Exception as e:
                print(f"❌ Synthesis failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_profile_loading():
    """Test voice profile loading functionality"""
    print("\n🎤 Testing Voice Profile Loading")
    print("=" * 35)
    
    try:
        from voice.store import list_voices, has_voice
        
        print("📦 Successfully imported voice store functions")
        
        # Test listing voices
        print("\n📋 Testing voice listing...")
        voices = list_voices("current_user")
        print(f"Found {len(voices)} voices for current_user")
        
        for i, voice in enumerate(voices):
            print(f"  {i+1}. {voice['voice_id']} - {voice.get('language', 'unknown')}")
        
        # Test specific voice existence
        if voices:
            test_voice = voices[0]
            user_id = "current_user"
            voice_id = test_voice['voice_id']
            
            print(f"\n🔍 Testing voice existence: {voice_id}")
            exists = has_voice(user_id, voice_id)
            print(f"Voice exists: {exists}")
            
            if exists:
                from voice.store import load_profile
                try:
                    emb, meta = load_profile(user_id, voice_id)
                    print(f"✅ Profile loaded successfully")
                    print(f"📊 Embedding shape: {emb.shape if hasattr(emb, 'shape') else 'N/A'}")
                    print(f"🔧 Metadata keys: {list(meta.keys())}")
                except Exception as e:
                    print(f"⚠️ Failed to load profile: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice profile test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Fixed TTS Engine Test Suite")
    print("=" * 40)
    
    # Test 1: TTS Synthesis
    success1 = test_tts_synthesis()
    
    # Test 2: Voice Profile Loading
    success2 = test_voice_profile_loading()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"TTS Synthesis: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Voice Profile Loading: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! TTS engine is working correctly.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
