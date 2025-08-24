#!/usr/bin/env python3
"""
Test script để kiểm tra checkpoint loading với các cải tiến mới
"""

import os
import sys
import json

# Thêm đường dẫn hiện tại vào sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_checkpoint_structure():
    print("🔍 Testing checkpoint structure...")
    
    model_root = "data/models/xtts_v2"
    tts_ckpt = os.path.join(model_root, "model.pth")
    spk_ckpt = os.path.join(model_root, "speakers_xtts.pth")
    
    # Kiểm tra files tồn tại
    if not os.path.exists(tts_ckpt):
        print(f"❌ Model checkpoint not found: {tts_ckpt}")
        return False
    
    if not os.path.exists(spk_ckpt):
        print(f"❌ Speakers checkpoint not found: {spk_ckpt}")
        return False
    
    print(f"✅ Model checkpoint: {tts_ckpt}")
    print(f"✅ Speakers checkpoint: {spk_ckpt}")
    
    # Kiểm tra kích thước files
    tts_size = os.path.getsize(tts_ckpt)
    spk_size = os.path.getsize(spk_ckpt)
    print(f"📏 Model checkpoint size: {tts_size:,} bytes")
    print(f"📏 Speakers checkpoint size: {spk_size:,} bytes")
    
    return True

def test_checkpoint_content():
    print("\n🔍 Testing checkpoint content...")
    
    try:
        import torch
        
        model_root = "data/models/xtts_v2"
        tts_ckpt = os.path.join(model_root, "model.pth")
        spk_ckpt = os.path.join(model_root, "speakers_xtts.pth")
        
        # Load model checkpoint
        print("🔄 Loading model checkpoint...")
        checkpoint_data = torch.load(tts_ckpt, map_location='cpu')
        print(f"✅ Model checkpoint loaded successfully")
        print(f"📊 Checkpoint type: {type(checkpoint_data)}")
        
        if isinstance(checkpoint_data, dict):
            print(f"🔑 Checkpoint keys: {list(checkpoint_data.keys())}")
            
            # Kiểm tra từng key
            for key, value in checkpoint_data.items():
                if isinstance(value, dict):
                    print(f"   - {key}: dict with {len(value)} items")
                    # Hiển thị một số key con
                    if len(value) > 0:
                        sample_keys = list(value.keys())[:5]
                        print(f"     Sample keys: {sample_keys}")
                elif isinstance(value, str):
                    print(f"   - {key}: string '{value[:50]}...'")
                else:
                    print(f"   - {key}: {type(value)}")
        else:
            print(f"⚠️ Checkpoint is not a dict: {type(checkpoint_data)}")
        
        # Load speakers checkpoint
        print("\n🔄 Loading speakers checkpoint...")
        speakers_data = torch.load(spk_ckpt, map_location='cpu')
        print(f"✅ Speakers checkpoint loaded successfully")
        print(f"📊 Speakers type: {type(speakers_data)}")
        
        if isinstance(speakers_data, dict):
            print(f"🔑 Speakers keys: {list(speakers_data.keys())}")
            
            # Kiểm tra từng key
            for key, value in speakers_data.items():
                if isinstance(value, dict):
                    print(f"   - {key}: dict with {len(value)} items")
                elif isinstance(value, str):
                    print(f"   - {key}: string '{value[:50]}...'")
                else:
                    print(f"   - {key}: {type(value)}")
        else:
            print(f"⚠️ Speakers is not a dict: {type(speakers_data)}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing checkpoint content: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_xtts_loading():
    print("\n🔍 Testing XTTS loading with improved checkpoint handling...")
    
    try:
        from src.voice.enrollment import load_xtts
        
        print("📦 Loading XTTS model...")
        model, model_type = load_xtts()
        
        print(f"✅ Model loaded successfully!")
        print(f"🤖 Model type: {model_type}")
        print(f"📦 Model object: {type(model)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading XTTS: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Checkpoint Loading Test Script")
    print("=" * 50)
    
    # Test 1: Checkpoint structure
    print("\n🧪 Test 1: Checkpoint Structure")
    structure_success = test_checkpoint_structure()
    
    if structure_success:
        # Test 2: Checkpoint content
        print("\n🧪 Test 2: Checkpoint Content")
        content_success = test_checkpoint_content()
        
        # Test 3: XTTS loading
        print("\n🧪 Test 3: XTTS Loading")
        loading_success = test_xtts_loading()
        
        if content_success and loading_success:
            print("\n🎉 All tests passed!")
        else:
            print("\n⚠️ Some tests failed but system may be functional")
    else:
        print("\n❌ Checkpoint structure test failed")
    
    print("\n" + "=" * 50)
    print("�� Test completed!")
