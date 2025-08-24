#!/usr/bin/env python3
"""
Test script để kiểm tra XTTS v2 trong môi trường ảo
"""

import os
import sys
import torch

def test_xtts_loading():
    """Test loading XTTS v2 model"""
    print("🔍 Testing XTTS v2 loading...")
    
    try:
        # Test TTS import
        print("📦 Importing TTS...")
        from TTS.api import TTS
        print("✅ TTS imported successfully")
        
        # Check available models
        print("🔍 Checking available models...")
        models = TTS.list_models()
        xtts_models = [m for m in models if "xtts" in m.lower()]
        print(f"✅ Found {len(xtts_models)} XTTS models:")
        for model in xtts_models:
            print(f"   - {model}")
        
        # Try to load XTTS v2
        print("🚀 Attempting to load XTTS v2...")
        try:
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            print("✅ XTTS v2 loaded successfully!")
            
            # Test synthesis
            print("🎤 Testing synthesis...")
            text = "Xin chào, đây là test giọng nói."
            output_path = "test_output.wav"
            
            tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav="data/voices/current_user/myVoice/sample.wav",
                language="vi"
            )
            print(f"✅ Synthesis successful! Output saved to {output_path}")
            
        except Exception as e:
            print(f"❌ Failed to load XTTS v2: {str(e)}")
            print("🔄 Trying alternative approach...")
            
            # Try alternative loading method
            try:
                from TTS.tts.configs.xtts_config import XttsConfig
                from TTS.tts.models.xtts import Xtts
                
                config = XttsConfig()
                config.load_json("data/models/xtts_v2/config.json")
                
                model = Xtts.init_from_config(config)
                model.load_checkpoint(config, "data/models/xtts_v2/model.pth")
                model.load_speaker_encoder("data/models/xtts_v2/speakers_xtts.pth")
                
                print("✅ XTTS v2 loaded with alternative method!")
                
            except Exception as e2:
                print(f"❌ Alternative method also failed: {str(e2)}")
                
    except Exception as e:
        print(f"❌ Error importing TTS: {str(e)}")

def test_environment():
    """Test environment setup"""
    print("🔍 Testing environment...")
    
    print(f"Python version: {sys.version}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"GPU count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")

if __name__ == "__main__":
    print("🚀 Starting XTTS v2 test...")
    test_environment()
    print("\n" + "="*50 + "\n")
    test_xtts_loading()
    print("\n✅ Test completed!")
