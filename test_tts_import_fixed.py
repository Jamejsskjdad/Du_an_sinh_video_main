#!/usr/bin/env python3
"""
Test script for TTS engine import fixes
This script tests that all imports are working correctly
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all required imports work correctly"""
    print("🧪 Testing TTS Engine Imports")
    print("=" * 40)
    
    try:
        # Test basic imports
        print("📦 Testing basic imports...")
        import soundfile as sf
        print("✅ soundfile imported successfully")
        
        import torch
        print("✅ torch imported successfully")
        
        import tempfile
        print("✅ tempfile imported successfully")
        
        from gtts import gTTS
        print("✅ gTTS imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_tts_engine_import():
    """Test TTS engine module import"""
    print("\n🚀 Testing TTS Engine Module Import")
    print("=" * 45)
    
    try:
        from voice.tts_engine import synthesize
        print("✅ TTS engine module imported successfully")
        print(f"🔧 synthesize function: {synthesize}")
        return True
        
    except Exception as e:
        print(f"❌ TTS engine import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_enrollment_import():
    """Test voice enrollment module import"""
    print("\n🎤 Testing Voice Enrollment Module Import")
    print("=" * 50)
    
    try:
        from voice.enrollment import load_xtts, enroll_voice
        print("✅ Voice enrollment module imported successfully")
        print(f"🔧 load_xtts function: {load_xtts}")
        print(f"🔧 enroll_voice function: {enroll_voice}")
        return True
        
    except Exception as e:
        print(f"❌ Voice enrollment import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_store_import():
    """Test voice store module import"""
    print("\n💾 Testing Voice Store Module Import")
    print("=" * 45)
    
    try:
        from voice.store import load_profile, list_voices
        print("✅ Voice store module imported successfully")
        print(f"🔧 load_profile function: {load_profile}")
        print(f"🔧 list_voices function: {list_voices}")
        return True
        
    except Exception as e:
        print(f"❌ Voice store import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_synthesis():
    """Test simple TTS synthesis without voice profile"""
    print("\n🎵 Testing Simple TTS Synthesis")
    print("=" * 40)
    
    try:
        from voice.tts_engine import synthesize
        
        # Test with non-existent voice (should trigger gTTS fallback)
        print("🧪 Testing synthesis with non-existent voice...")
        result = synthesize(
            text="Xin chào! Đây là bài kiểm tra.",
            user_id="test_user",
            voice_id="non_existent_voice",
            lang="vi"
        )
        
        if result:
            print(f"✅ Synthesis successful: {result}")
            if os.path.exists(result):
                file_size = os.path.getsize(result)
                print(f"📁 Output file: {result} ({file_size:,} bytes)")
            else:
                print(f"⚠️ Output file not found: {result}")
        else:
            print("⚠️ Synthesis returned None")
        
        return True
        
    except Exception as e:
        print(f"❌ Synthesis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 TTS Engine Import Test Suite")
    print("=" * 40)
    
    # Test 1: Basic imports
    success1 = test_imports()
    
    # Test 2: TTS engine module import
    success2 = test_tts_engine_import()
    
    # Test 3: Voice enrollment module import
    success3 = test_voice_enrollment_import()
    
    # Test 4: Voice store module import
    success4 = test_voice_store_import()
    
    # Test 5: Simple synthesis
    success5 = test_simple_synthesis()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"Basic Imports: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"TTS Engine Import: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"Voice Enrollment Import: {'✅ PASS' if success3 else '❌ FAIL'}")
    print(f"Voice Store Import: {'✅ PASS' if success4 else '❌ FAIL'}")
    print(f"Simple Synthesis: {'✅ PASS' if success5 else '❌ FAIL'}")
    
    if all([success1, success2, success3, success4, success5]):
        print("\n🎉 All tests passed! TTS engine imports are working correctly.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
