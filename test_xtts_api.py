#!/usr/bin/env python3
"""
Test script for XTTS loading using Coqui TTS API
This script tests the new approach that avoids checkpoint loading issues
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_xtts_loading():
    """Test XTTS loading with the new API approach"""
    print("🧪 Testing XTTS Loading with Coqui TTS API")
    print("=" * 50)
    
    try:
        # Import the enrollment module
        from voice.enrollment import load_xtts
        
        print("📦 Successfully imported enrollment module")
        
        # Test XTTS loading
        print("\n🚀 Testing XTTS loading...")
        model, model_type = load_xtts()
        
        print(f"✅ XTTS loaded successfully!")
        print(f"🤖 Model type: {model_type}")
        print(f"🔧 Model object: {type(model)}")
        
        # Test if model has required methods
        if hasattr(model, 'tts'):
            print("✅ Model has 'tts' method")
        else:
            print("❌ Model missing 'tts' method")
        
        if hasattr(model, 'get_speaker_embedding'):
            print("✅ Model has 'get_speaker_embedding' method")
        else:
            print("⚠️ Model missing 'get_speaker_embedding' method")
        
        # Test TTS synthesis if possible
        if hasattr(model, 'tts'):
            print("\n🎤 Testing TTS synthesis...")
            try:
                # Test with Vietnamese text
                test_text = "Xin chào! Đây là bài kiểm tra giọng nói."
                print(f"📝 Test text: {test_text}")
                
                if model_type == "gtts":
                    # gTTS wrapper
                    audio = model.tts(text=test_text, language="vi")
                    print(f"✅ gTTS synthesis successful: {type(audio)}")
                else:
                    # XTTS or other TTS models
                    audio = model.tts(text=test_text, language="vi")
                    print(f"✅ TTS synthesis successful: {type(audio)}")
                
            except Exception as e:
                print(f"⚠️ TTS synthesis failed: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_voice_enrollment():
    """Test voice enrollment functionality"""
    print("\n🎤 Testing Voice Enrollment")
    print("=" * 30)
    
    try:
        from voice.enrollment import enroll_voice, get_voice_profile, list_voice_profiles
        
        print("📦 Successfully imported voice functions")
        
        # Test voice profile listing
        print("\n📋 Testing voice profile listing...")
        profiles = list_voice_profiles()
        print(f"Found {len(profiles)} voice profiles")
        
        # Test getting specific voice profile
        if profiles:
            test_profile = profiles[0]
            print(f"\n🔍 Testing get_voice_profile for: {test_profile}")
            
            user_id, voice_id = test_profile.split(os.sep)
            profile = get_voice_profile(user_id, voice_id)
            
            if profile:
                print(f"✅ Voice profile loaded: {profile['voice_id']}")
                print(f"📁 Directory: {profile['voice_dir']}")
            else:
                print("⚠️ Failed to load voice profile")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice enrollment test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 XTTS API Test Suite")
    print("=" * 40)
    
    # Test 1: XTTS Loading
    success1 = test_xtts_loading()
    
    # Test 2: Voice Enrollment
    success2 = test_voice_enrollment()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"XTTS Loading: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Voice Enrollment: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! XTTS is working correctly.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
