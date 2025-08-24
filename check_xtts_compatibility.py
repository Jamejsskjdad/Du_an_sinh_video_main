#!/usr/bin/env python3
"""
Script kiểm tra compatibility của XTTS v2
"""

import os
import json
import torch
import sys

def check_xtts_compatibility():
    print("🔍 Checking XTTS v2 compatibility...")
    
    # Kiểm tra TTS version
    try:
        import TTS
        print(f"📦 TTS version: {TTS.__version__}")
    except Exception as e:
        print(f"❌ Error checking TTS version: {e}")
    
    # Kiểm tra PyTorch
    print(f"🔥 PyTorch version: {torch.__version__}")
    print(f"🔥 CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"🔥 CUDA version: {torch.version.cuda}")
        print(f"🔥 GPU count: {torch.cuda.device_count()}")
    
    # Kiểm tra files
    model_root = "data/models/xtts_v2"
    files_to_check = ["config.json", "model.pth", "speakers_xtts.pth"]
    
    print(f"\n📁 Checking files in {model_root}:")
    for file in files_to_check:
        file_path = os.path.join(model_root, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file}: {size:,} bytes")
        else:
            print(f"❌ {file}: Not found")
    
    # Kiểm tra config.json
    config_path = os.path.join(model_root, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"\n📋 Config keys: {list(config.keys())}")
            
            # Kiểm tra required fields
            required_fields = ["model", "audio", "model_args"]
            for field in required_fields:
                if field in config:
                    print(f"✅ Required field '{field}' found")
                else:
                    print(f"❌ Required field '{field}' missing")
                    
        except Exception as e:
            print(f"❌ Error reading config.json: {e}")
    
    # Kiểm tra memory
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory
        print(f"\n💾 GPU memory: {gpu_memory / 1024**3:.1f} GB")
    else:
        print(f"\n💾 Using CPU mode")
    
    # Kiểm tra disk space
    import shutil
    total, used, free = shutil.disk_usage(".")
    print(f"💾 Disk space: {free / 1024**3:.1f} GB free")

def test_xtts_load():
    print("\n🧪 Testing XTTS load...")
    
    try:
        from src.voice.enrollment import load_xtts
        
        model, model_type = load_xtts()
        
        print(f"🤖 Model type: {model_type}")
        
        if model_type == "xtts_v2":
            print("✅ XTTS v2 loaded successfully!")
            return True
        else:
            print("⚠️ Using fallback model")
            return False
            
    except Exception as e:
        print(f"❌ Error loading XTTS: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 XTTS v2 Compatibility Checker")
    print("=" * 50)
    
    check_xtts_compatibility()
    test_xtts_load()

