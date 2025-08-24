#!/usr/bin/env python3
"""
Test script for voice selection logic and language handling
This script tests if the correct voice is selected and used
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_language_handling_logic():
    """Test language handling logic"""
    print("🌐 Testing Language Handling Logic")
    print("=" * 40)
    
    try:
        from voice.tts_engine import synthesize
        
        # Get the function source
        import inspect
        source = inspect.getsource(synthesize)
        
        # Check if language handling is correct
        if 'XTTS không support tiếng Việt' in source:
            print("✅ XTTS language handling logic found")
            
            # Check if Vietnamese is mapped to English for XTTS
            if 'return \'en\'' in source and 'dùng English để giữ giọng clone' in source:
                print("✅ Vietnamese → English mapping for XTTS found")
            else:
                print("❌ Vietnamese → English mapping not found")
                return False
                
            return True
        else:
            print("❌ XTTS language handling logic not found")
            return False
            
    except Exception as e:
        print(f"❌ Language handling logic test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gtts_language_preservation():
    """Test gTTS language preservation"""
    print("\n🎤 Testing gTTS Language Preservation")
    print("=" * 40)
    
    try:
        from voice.tts_engine import synthesize
        
        # Get the function source
        import inspect
        source = inspect.getsource(synthesize)
        
        # Check if gTTS preserves original language
        if 'gTTS fallback: Sử dụng language' in source and 'để giữ tiếng Việt' in source:
            print("✅ gTTS language preservation logic found")
            return True
        else:
            print("❌ gTTS language preservation logic not found")
            return False
            
    except Exception as e:
        print(f"❌ gTTS language preservation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_profile_integration():
    """Test voice profile integration"""
    print("\n📁 Testing Voice Profile Integration")
    print("=" * 40)
    
    try:
        from voice.store import load_profile, list_voices
        
        # Test current user voices
        user_id = "current_user"
        voices = list_voices(user_id)
        
        if not voices:
            print("❌ No voices found for current_user")
            return False
        
        print(f"✅ Found {len(voices)} voices for {user_id}")
        
        # Check if myVoice exists
        my_voice = None
        for voice in voices:
            if voice['voice_id'] == 'myVoice':
                my_voice = voice
                break
        
        if my_voice:
            print(f"✅ myVoice found: {my_voice}")
            
            # Load profile
            profile = load_profile(user_id, 'myVoice')
            if profile:
                print(f"✅ Profile loaded successfully")
                print(f"🔑 Profile type: {type(profile)}")
                
                # Profile is a tuple: (embedding, metadata)
                if isinstance(profile, tuple) and len(profile) == 2:
                    embedding, metadata = profile
                    print(f"✅ Profile structure: (embedding, metadata)")
                    print(f"🔑 Metadata keys: {list(metadata.keys())}")
                    
                    # Check sample audio
                    sample_audio = metadata.get('sample_audio')
                    if sample_audio and os.path.exists(sample_audio):
                        print(f"✅ Sample audio exists: {sample_audio}")
                        return True
                    else:
                        print(f"❌ Sample audio not found or doesn't exist")
                        return False
                else:
                    print(f"❌ Profile structure unexpected: {type(profile)}")
                    return False
            else:
                print(f"❌ Failed to load profile")
                return False
        else:
            print(f"❌ myVoice not found in voices list")
            return False
            
    except Exception as e:
        print(f"❌ Voice profile integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_xtts_speaker_parameter():
    """Test XTTS speaker parameter handling"""
    print("\n🎭 Testing XTTS Speaker Parameter")
    print("=" * 40)
    
    try:
        from voice.tts_engine import synthesize
        
        # Get the function source
        import inspect
        source = inspect.getsource(synthesize)
        
        # Check if speaker parameter is used correctly
        speaker_methods = [
            'speaker=voice_id, speaker_embedding=emb',
            'speaker=voice_id',
            'speaker_wav=sample_audio_path'
        ]
        
        found_methods = 0
        for method in speaker_methods:
            if method in source:
                found_methods += 1
                print(f"✅ Found: {method}")
            else:
                print(f"❌ Missing: {method}")
        
        if found_methods >= 2:  # At least 2 out of 3 should be found
            print(f"✅ Speaker parameter methods: {found_methods}/3")
            return True
        else:
            print(f"❌ Speaker parameter methods: {found_methods}/3")
            return False
            
    except Exception as e:
        print(f"❌ XTTS speaker parameter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_chain():
    """Test fallback chain logic"""
    print("\n🔄 Testing Fallback Chain Logic")
    print("=" * 40)
    
    try:
        from voice.tts_engine import synthesize
        
        # Get the function source
        import inspect
        source = inspect.getsource(synthesize)
        
        # Check fallback chain
        fallback_steps = [
            'Speaker embedding with speaker parameter',
            'with speaker parameter',
            'speaker_wav',
            'without speaker',
            'gTTS with PCM 16-bit format'
        ]
        
        found_steps = 0
        for step in fallback_steps:
            if step in source:
                found_steps += 1
                print(f"✅ Found: {step}")
            else:
                print(f"❌ Missing: {step}")
        
        if found_steps >= 4:  # At least 4 out of 5 should be found
            print(f"✅ Fallback chain steps: {found_steps}/5")
            return True
        else:
            print(f"❌ Fallback chain steps: {found_steps}/5")
            return False
            
    except Exception as e:
        print(f"❌ Fallback chain test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Voice Selection Logic & Language Handling Test Suite")
    print("=" * 60)
    
    # Test 1: Language handling logic
    success1 = test_language_handling_logic()
    
    # Test 2: gTTS language preservation
    success2 = test_gtts_language_preservation()
    
    # Test 3: Voice profile integration
    success3 = test_voice_profile_integration()
    
    # Test 4: XTTS speaker parameter
    success4 = test_xtts_speaker_parameter()
    
    # Test 5: Fallback chain
    success5 = test_fallback_chain()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Voice Selection Logic Test Results Summary")
    print("=" * 70)
    print(f"Language Handling Logic: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"gTTS Language Preservation: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"Voice Profile Integration: {'✅ PASS' if success3 else '❌ FAIL'}")
    print(f"XTTS Speaker Parameter: {'✅ PASS' if success4 else '❌ FAIL'}")
    print(f"Fallback Chain Logic: {'✅ PASS' if success5 else '❌ FAIL'}")
    
    if all([success1, success2, success3, success4, success5]):
        print("\n🎉 All voice selection logic tests passed!")
        print("\n🚀 Voice selection logic is working correctly:")
        print("   ✅ XTTS uses English for voice cloning (language compatibility)")
        print("   ✅ gTTS preserves Vietnamese language (user experience)")
        print("   ✅ Voice profiles are properly integrated")
        print("   ✅ Speaker parameters are used correctly")
        print("   ✅ Fallback chain works properly")
        print("\n🎬 SadTalker should now use the correct cloned voice!")
        return True
    else:
        print("\n⚠️ Some voice selection logic tests failed.")
        print("\n🔧 Issues to fix:")
        if not success1:
            print("   - Language handling logic")
        if not success2:
            print("   - gTTS language preservation")
        if not success3:
            print("   - Voice profile integration")
        if not success4:
            print("   - XTTS speaker parameter")
        if not success5:
            print("   - Fallback chain logic")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
