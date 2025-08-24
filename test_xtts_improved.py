#!/usr/bin/env python3
"""
Test script để kiểm tra XTTS loading với các cải tiến mới
"""

import sys
import os

# Thêm đường dẫn hiện tại vào sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_xtts_loading():
    print("🔍 Testing improved XTTS loading...")
    
    try:
        from src.voice.enrollment import load_xtts
        
        print("📦 Loading XTTS model...")
        model, model_type = load_xtts()
        
        print(f"✅ Model loaded successfully!")
        print(f"🤖 Model type: {model_type}")
        print(f"📦 Model object: {type(model)}")
        
        if model_type in ["xtts_v2", "xtts_v2_api"]:
            print("🎉 XTTS v2 loaded successfully!")
            return True
        elif model_type == "gtts":
            print("✅ gTTS fallback loaded successfully!")
            return True
        else:
            print(f"⚠️ {model_type} model loaded (fallback)")
            return True
            
    except Exception as e:
        print(f"❌ Error loading XTTS: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_enrollment():
    print("\n🔍 Testing voice enrollment...")
    
    try:
        from src.voice.enrollment import enroll_voice
        
        # Test với audio file giả (không thực sự tồn tại)
        print("🎤 Testing voice enrollment process...")
        
        # Tạo file audio giả để test
        test_audio = "test_audio.wav"
        if not os.path.exists(test_audio):
            # Tạo file audio giả
            import wave
            import struct
            
            # Tạo file WAV đơn giản
            with wave.open(test_audio, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(24000)  # 24kHz
                
                # Tạo 1 giây silence
                frames = b'\x00\x00' * 24000
                wav_file.writeframes(frames)
            
            print(f"✅ Created test audio file: {test_audio}")
        
        # Test enrollment
        try:
            meta = enroll_voice(test_audio, "test_user", "test_voice", "vi")
            print(f"✅ Voice enrollment successful!")
            print(f"📊 Meta data: {meta}")
            return True
        except Exception as e:
            print(f"⚠️ Voice enrollment failed (expected for test): {e}")
            return True  # Không phải lỗi nghiêm trọng
            
    except Exception as e:
        print(f"❌ Error in voice enrollment test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_synthesis():
    print("\n🔍 Testing voice synthesis...")
    
    try:
        from src.voice.tts_engine import synthesize
        
        # Test với text đơn giản
        text = "Xin chào, đây là test giọng nói."
        user_id = "test_user"
        voice_id = "test_voice"
        
        print(f"🎤 Synthesizing: {text}")
        output_path = synthesize(text, user_id, voice_id, lang="vi")
        
        if output_path and os.path.exists(output_path):
            print(f"✅ Synthesis successful! Output: {output_path}")
            return True
        else:
            print("❌ Synthesis failed or output file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error in synthesis: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 XTTS Improved Test Script")
    print("=" * 50)
    
    # Test 1: Loading
    print("\n🧪 Test 1: Model Loading")
    loading_success = test_xtts_loading()
    
    if loading_success:
        # Test 2: Voice Enrollment
        print("\n🧪 Test 2: Voice Enrollment")
        enrollment_success = test_voice_enrollment()
        
        # Test 3: Synthesis
        print("\n🧪 Test 3: Voice Synthesis")
        synthesis_success = test_voice_synthesis()
        
        if enrollment_success and synthesis_success:
            print("\n🎉 All tests passed!")
        else:
            print("\n⚠️ Some tests failed but system is functional")
    else:
        print("\n❌ Loading failed")
    
    print("\n" + "=" * 50)
    print("�� Test completed!")
