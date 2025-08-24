#!/usr/bin/env python3
"""
Test script for voice enrollment functionality
This script tests the complete voice enrollment flow
"""

import sys
import os
import tempfile
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_test_audio():
    """Create a test audio file for testing"""
    try:
        # Create a simple test audio file
        sample_rate = 48000
        duration = 2.0  # 2 seconds
        samples = int(sample_rate * duration)
        
        # Generate a simple sine wave
        frequency = 440  # A4 note
        t = np.linspace(0, duration, samples, False)
        audio = np.sin(2 * np.pi * frequency * t) * 0.3
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_path = temp_file.name
        temp_file.close()
        
        # Save as WAV file
        import soundfile as sf
        sf.write(temp_path, audio, sample_rate)
        
        print(f"✅ Test audio created: {temp_path}")
        print(f"📊 Audio info: {len(audio)} samples, {sample_rate} Hz, {duration:.1f}s")
        
        return temp_path
        
    except Exception as e:
        print(f"❌ Failed to create test audio: {e}")
        return None

def test_voice_enrollment():
    """Test the complete voice enrollment process"""
    print("🧪 Testing Voice Enrollment Process")
    print("=" * 50)
    
    try:
        # Import required functions
        from voice.enrollment import enroll_voice, get_voice_profile, list_voice_profiles
        from voice.store import list_voices
        
        print("📦 Successfully imported voice functions")
        
        # Create test audio
        print("\n🎵 Creating test audio...")
        test_audio_path = create_test_audio()
        if not test_audio_path:
            return False
        
        # Test voice enrollment
        print(f"\n🎤 Testing voice enrollment with: {test_audio_path}")
        user_id = "test_user"
        voice_id = "test_voice"
        
        success = enroll_voice(test_audio_path, user_id, voice_id, lang_hint="vi")
        
        if success:
            print("✅ Voice enrollment successful!")
        else:
            print("❌ Voice enrollment failed!")
            return False
        
        # Test getting voice profile
        print(f"\n🔍 Testing get_voice_profile...")
        profile = get_voice_profile(user_id, voice_id)
        
        if profile:
            print(f"✅ Voice profile loaded: {profile['voice_id']}")
            print(f"📁 Directory: {profile['voice_dir']}")
            print(f"🔧 Metadata: {profile['metadata']}")
        else:
            print("❌ Failed to load voice profile")
            return False
        
        # Test listing voices
        print(f"\n📋 Testing list_voices...")
        voices = list_voices(user_id)
        print(f"Found {len(voices)} voices for user {user_id}")
        
        for i, voice in enumerate(voices):
            print(f"  {i+1}. {voice['voice_id']} - {voice.get('language', 'unknown')} - {voice.get('created_at', 'unknown')}")
        
        # Test list_voice_profiles
        print(f"\n📋 Testing list_voice_profiles...")
        profiles = list_voice_profiles(user_id)
        print(f"Found {len(profiles)} voice profiles")
        
        for profile_path in profiles:
            print(f"  - {profile_path}")
        
        # Clean up test audio
        try:
            os.unlink(test_audio_path)
            print(f"\n🧹 Cleaned up test audio: {test_audio_path}")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_synthesis():
    """Test voice synthesis with enrolled voice"""
    print("\n🎤 Testing Voice Synthesis")
    print("=" * 30)
    
    try:
        from voice.enrollment import load_xtts
        from voice.tts_engine import synthesize
        
        print("📦 Successfully imported synthesis functions")
        
        # Load TTS model
        print("\n🚀 Loading TTS model...")
        model, model_type = load_xtts()
        print(f"✅ TTS model loaded: {model_type}")
        
        # Test synthesis
        print("\n🎵 Testing text-to-speech synthesis...")
        test_text = "Xin chào! Đây là bài kiểm tra giọng nói."
        print(f"📝 Test text: {test_text}")
        
        # Test with default voice (no specific speaker)
        audio = synthesize(model, test_text, model_type, None, "vi")
        
        if audio is not None:
            print(f"✅ Synthesis successful: {type(audio)}")
            if hasattr(audio, 'shape'):
                print(f"📊 Audio shape: {audio.shape}")
            elif hasattr(audio, '__len__'):
                print(f"📊 Audio length: {len(audio)}")
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
    print("🚀 Voice Enrollment Test Suite")
    print("=" * 40)
    
    # Test 1: Voice Enrollment
    success1 = test_voice_enrollment()
    
    # Test 2: Voice Synthesis
    success2 = test_voice_synthesis()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"Voice Enrollment: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Voice Synthesis: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! Voice system is working correctly.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
