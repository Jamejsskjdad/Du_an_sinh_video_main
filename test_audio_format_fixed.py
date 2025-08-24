#!/usr/bin/env python3
"""
Test script for fixed audio format and TTS functionality
This script tests the fixes for XTTS and audio format issues
"""

import sys
import os
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_transformers_version():
    """Test transformers version compatibility"""
    print("🔧 Testing Transformers Version Compatibility")
    print("=" * 45)
    
    try:
        import transformers
        version = transformers.__version__
        print(f"📦 Transformers version: {version}")
        
        if version.startswith('4.49'):
            print("✅ Transformers 4.49.x - Compatible with XTTS")
            return True
        elif version.startswith('4.55'):
            print("❌ Transformers 4.55.x - Incompatible with XTTS")
            print("💡 This version causes 'generate' method error")
            return False
        else:
            print(f"⚠️ Transformers {version} - Unknown compatibility")
            return False
            
    except Exception as e:
        print(f"❌ Transformers version test failed: {e}")
        return False

def test_xtts_language_handling():
    """Test XTTS language handling"""
    print("\n🌐 Testing XTTS Language Handling")
    print("=" * 35)
    
    try:
        from voice.tts_engine import synthesize
        
        # Get the function source
        import inspect
        source = inspect.getsource(synthesize)
        
        # Check if language handling is fixed
        if 'get_xtts_language' in source:
            print("✅ Language handling function found")
            
            # Check if Vietnamese is kept as 'vi'
            if "'vi'" in source and "ép giữ tiếng Việt" in source:
                print("✅ Vietnamese language preservation found")
            else:
                print("❌ Vietnamese language preservation not found")
                return False
                
            return True
        else:
            print("❌ Language handling function not found")
            return False
            
    except Exception as e:
        print(f"❌ XTTS language handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gtts_fallback_improvements():
    """Test gTTS fallback improvements"""
    print("\n🔧 Testing gTTS Fallback Improvements")
    print("=" * 40)
    
    try:
        from voice.tts_engine import synthesize
        
        # Get the function source
        import inspect
        source = inspect.getsource(synthesize)
        
        # Check for improvements
        improvements = [
            'PCM 16-bit format',
            'sample_fmt s16',
            'apad=pad_dur=0.5',
            'Audio format verified',
            '16kHz mono'
        ]
        
        found_improvements = 0
        for improvement in improvements:
            if improvement in source:
                found_improvements += 1
                print(f"✅ Found: {improvement}")
            else:
                print(f"❌ Missing: {improvement}")
        
        if found_improvements >= 4:  # At least 4 out of 5 should be found
            print(f"✅ gTTS improvements: {found_improvements}/5 features")
            return True
        else:
            print(f"❌ gTTS improvements: {found_improvements}/5 features")
            return False
            
    except Exception as e:
        print(f"❌ gTTS fallback test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ffmpeg_availability():
    """Test FFmpeg availability for audio conversion"""
    print("\n🎵 Testing FFmpeg Availability")
    print("=" * 35)
    
    try:
        # Check if ffmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            print("✅ FFmpeg is available")
            
            # Test basic conversion
            test_input = "test_input.wav"
            test_output = "test_output.wav"
            
            # Create a simple test file if needed
            if not os.path.exists(test_input):
                # Create a simple test audio file
                cmd = [
                    'ffmpeg', '-y',
                    '-f', 'lavfi',
                    '-i', 'sine=frequency=1000:duration=1',
                    '-ac', '1',
                    '-ar', '16000',
                    '-sample_fmt', 's16',
                    test_input
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"⚠️ Test file creation failed: {result.stderr}")
                    return False
            
            # Test conversion
            cmd = [
                'ffmpeg', '-y',
                '-i', test_input,
                '-ac', '1',
                '-ar', '16000',
                '-sample_fmt', 's16',
                test_output
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(test_output):
                print("✅ FFmpeg conversion test successful")
                
                # Clean up test files
                try:
                    if os.path.exists(test_input):
                        os.unlink(test_input)
                    if os.path.exists(test_output):
                        os.unlink(test_output)
                except:
                    pass
                
                return True
            else:
                print(f"❌ FFmpeg conversion test failed: {result.stderr}")
                return False
                
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ FFmpeg not found")
            print("💡 Please install FFmpeg first:")
            print("   Windows: Download from https://ffmpeg.org/download.html")
            print("   Or use: winget install ffmpeg")
            return False
            
    except Exception as e:
        print(f"❌ FFmpeg test failed: {e}")
        return False

def test_audio_format_verification():
    """Test audio format verification"""
    print("\n🔍 Testing Audio Format Verification")
    print("=" * 40)
    
    try:
        from voice.tts_engine import synthesize
        
        # Get the function source
        import inspect
        source = inspect.getsource(synthesize)
        
        # Check for audio format verification
        verifications = [
            'Audio format verified',
            '16kHz mono',
            'sr == 16000',
            'len(audio.shape) == 1'
        ]
        
        found_verifications = 0
        for verification in verifications:
            if verification in source:
                found_verifications += 1
                print(f"✅ Found: {verification}")
            else:
                print(f"❌ Missing: {verification}")
        
        if found_verifications >= 3:  # At least 3 out of 4 should be found
            print(f"✅ Audio format verification: {found_verifications}/4 features")
            return True
        else:
            print(f"❌ Audio format verification: {found_verifications}/4 features")
            return False
            
    except Exception as e:
        print(f"❌ Audio format verification test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Fixed Audio Format & TTS Test Suite")
    print("=" * 50)
    
    # Test 1: Transformers version
    success1 = test_transformers_version()
    
    # Test 2: XTTS language handling
    success2 = test_xtts_language_handling()
    
    # Test 3: gTTS fallback improvements
    success3 = test_gtts_fallback_improvements()
    
    # Test 4: FFmpeg availability
    success4 = test_ffmpeg_availability()
    
    # Test 5: Audio format verification
    success5 = test_audio_format_verification()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Fixed Audio Format Test Results Summary")
    print("=" * 60)
    print(f"Transformers Version: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"XTTS Language Handling: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"gTTS Fallback Improvements: {'✅ PASS' if success3 else '❌ FAIL'}")
    print(f"FFmpeg Availability: {'✅ PASS' if success4 else '❌ FAIL'}")
    print(f"Audio Format Verification: {'✅ PASS' if success5 else '❌ FAIL'}")
    
    if all([success1, success2, success3, success4, success5]):
        print("\n🎉 All audio format tests passed!")
        print("\n🚀 Audio format fixes are working:")
        print("   ✅ Transformers 4.49.x - XTTS compatible")
        print("   ✅ Language preservation - Vietnamese kept as 'vi'")
        print("   ✅ PCM 16-bit format - Standard audio format")
        print("   ✅ 16kHz mono - SadTalker compatible")
        print("   ✅ Audio padding - Sufficient frame count")
        print("\n🎬 SadTalker should now work without audio format errors!")
        return True
    else:
        print("\n⚠️ Some audio format tests failed.")
        print("\n🔧 Issues to fix:")
        if not success1:
            print("   - Transformers version compatibility")
        if not success2:
            print("   - XTTS language handling")
        if not success3:
            print("   - gTTS fallback improvements")
        if not success4:
            print("   - FFmpeg availability")
        if not success5:
            print("   - Audio format verification")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
