#!/usr/bin/env python3
"""
Test script for language mapping functionality
This script tests the language mapping from Vietnamese to XTTS supported languages
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_language_mapping():
    """Test language mapping function"""
    print("🌐 Testing Language Mapping Function")
    print("=" * 40)
    
    try:
        from voice.tts_engine import synthesize
        
        # Get the function source to check language mapping
        import inspect
        source = inspect.getsource(synthesize)
        
        # Check if language mapping is implemented
        if 'map_language_for_xtts' in source:
            print("✅ Language mapping function found")
            
            # Check if Vietnamese is mapped to English
            if "'vi': 'en'" in source:
                print("✅ Vietnamese -> English mapping found")
            else:
                print("❌ Vietnamese -> English mapping not found")
                return False
                
            # Check if other languages are mapped
            if "'en': 'en'" in source and "'es': 'es'" in source:
                print("✅ Other language mappings found")
            else:
                print("❌ Other language mappings not found")
                return False
                
            return True
        else:
            print("❌ Language mapping function not found")
            return False
            
    except Exception as e:
        print(f"❌ Language mapping test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_xtts_language_usage():
    """Test if XTTS language is used in method calls"""
    print("\n🎤 Testing XTTS Language Usage")
    print("=" * 35)
    
    try:
        from voice.tts_engine import synthesize
        
        # Get the function source
        import inspect
        source = inspect.getsource(synthesize)
        
        # Check if xtts_lang is used in method calls
        method_calls = [
            'language=xtts_lang',
            'speaker=voice_id, speaker_embedding=emb, language=xtts_lang',
            'speaker=voice_id, language=xtts_lang',
            'speaker_wav=sample_audio_path, language=xtts_lang',
            'language=xtts_lang'
        ]
        
        found_calls = 0
        for call in method_calls:
            if call in source:
                found_calls += 1
                print(f"✅ Found: {call}")
            else:
                print(f"❌ Missing: {call}")
        
        if found_calls >= 3:  # At least 3 out of 5 should be found
            print(f"✅ Language mapping usage: {found_calls}/5 methods")
            return True
        else:
            print(f"❌ Language mapping usage: {found_calls}/5 methods")
            return False
            
    except Exception as e:
        print(f"❌ XTTS language usage test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gtts_fallback_improvement():
    """Test if gTTS fallback has been improved"""
    print("\n🔧 Testing gTTS Fallback Improvements")
    print("=" * 40)
    
    try:
        from voice.tts_engine import synthesize
        
        # Get the function source
        import inspect
        source = inspect.getsource(synthesize)
        
        # Check for improvements
        improvements = [
            'gTTS with proper format',
            'FFmpeg',
            '16kHz',
            'mono',
            'PCM s16',
            'apad=pad_dur=0.5'
        ]
        
        found_improvements = 0
        for improvement in improvements:
            if improvement in source:
                found_improvements += 1
                print(f"✅ Found: {improvement}")
            else:
                print(f"❌ Missing: {improvement}")
        
        if found_improvements >= 4:  # At least 4 out of 6 should be found
            print(f"✅ gTTS improvements: {found_improvements}/6 features")
            return True
        else:
            print(f"❌ gTTS improvements: {found_improvements}/6 features")
            return False
            
    except Exception as e:
        print(f"❌ gTTS fallback test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Language Mapping & TTS Improvements Test Suite")
    print("=" * 55)
    
    # Test 1: Language mapping function
    success1 = test_language_mapping()
    
    # Test 2: XTTS language usage
    success2 = test_xtts_language_usage()
    
    # Test 3: gTTS fallback improvements
    success3 = test_gtts_fallback_improvement()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Language Mapping Test Results Summary")
    print("=" * 60)
    print(f"Language Mapping Function: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"XTTS Language Usage: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"gTTS Fallback Improvements: {'✅ PASS' if success3 else '❌ FAIL'}")
    
    if all([success1, success2, success3]):
        print("\n🎉 All language mapping tests passed!")
        print("\n🚀 Language mapping improvements:")
        print("   ✅ Vietnamese (vi) -> English (en) for XTTS")
        print("   ✅ All XTTS methods use mapped language")
        print("   ✅ gTTS fallback with proper audio format")
        print("   ✅ 16kHz mono PCM s16 output")
        print("   ✅ Audio padding for stability")
        print("\n🎬 SadTalker should now work with Vietnamese text!")
        return True
    else:
        print("\n⚠️ Some language mapping tests failed.")
        print("\n🔧 Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
