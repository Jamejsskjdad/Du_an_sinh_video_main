#!/usr/bin/env python3
"""
Debug script để kiểm tra chi tiết lỗi XTTS loading
"""

import os
import json
import torch
import sys

def debug_xtts_loading():
    print("🔍 Debugging XTTS loading step by step...")
    
    model_root = "data/models/xtts_v2"
    
    # Bước 1: Kiểm tra files
    print("\n📁 Step 1: Checking files...")
    cfg_path = os.path.join(model_root, "config.json")
    tts_ckpt = os.path.join(model_root, "model.pth")
    spk_ckpt = os.path.join(model_root, "speakers_xtts.pth")
    
    for path, name in [(cfg_path, "config.json"), (tts_ckpt, "model.pth"), (spk_ckpt, "speakers_xtts.pth")]:
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ {name}: {size:,} bytes")
        else:
            print(f"❌ {name}: Not found")
    
    # Bước 2: Kiểm tra config.json
    print("\n📋 Step 2: Checking config.json...")
    try:
        with open(cfg_path, 'r', encoding='utf-8') as f:
            cfg_dict = json.load(f)
        print(f"✅ Config loaded successfully")
        print(f"📊 Config type: {type(cfg_dict)}")
        print(f"🔑 Config keys: {list(cfg_dict.keys())[:10]}")
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return
    
    # Bước 3: Kiểm tra checkpoint files
    print("\n💾 Step 3: Checking checkpoint files...")
    
    # Kiểm tra model.pth
    try:
        print(f"🔍 Loading {tts_ckpt}...")
        checkpoint = torch.load(tts_ckpt, map_location="cpu")
        print(f"✅ Model checkpoint loaded successfully")
        print(f"📊 Checkpoint type: {type(checkpoint)}")
        
        if isinstance(checkpoint, dict):
            print(f"🔑 Checkpoint keys: {list(checkpoint.keys())[:10]}")
            # Kiểm tra kích thước của state_dict
            if 'state_dict' in checkpoint:
                state_dict = checkpoint['state_dict']
                print(f"📏 State dict keys count: {len(state_dict)}")
                print(f"🔑 First few state dict keys: {list(state_dict.keys())[:5]}")
        else:
            print(f"⚠️ Checkpoint is not a dict, it's: {type(checkpoint)}")
            
    except Exception as e:
        print(f"❌ Error loading model checkpoint: {e}")
        import traceback
        traceback.print_exc()
    
    # Kiểm tra speakers_xtts.pth
    try:
        print(f"\n🔍 Loading {spk_ckpt}...")
        speakers = torch.load(spk_ckpt, map_location="cpu")
        print(f"✅ Speakers checkpoint loaded successfully")
        print(f"📊 Speakers type: {type(speakers)}")
        
        if isinstance(speakers, dict):
            print(f"🔑 Speakers keys: {list(speakers.keys())[:10]}")
        else:
            print(f"⚠️ Speakers is not a dict, it's: {type(speakers)}")
            
    except Exception as e:
        print(f"❌ Error loading speakers checkpoint: {e}")
        import traceback
        traceback.print_exc()
    
    # Bước 4: Kiểm tra TTS library
    print("\n📦 Step 4: Checking TTS library...")
    try:
        import TTS
        print(f"✅ TTS version: {TTS.__version__}")
        
        # Kiểm tra Xtts class
        try:
            from TTS.tts.models.xtts import Xtts
            print("✅ Xtts class imported successfully")
            
            # Kiểm tra XttsConfig
            try:
                from TTS.tts.configs.xtts_config import XttsConfig
                print("✅ XttsConfig class imported successfully")
                
                # Thử tạo config object
                try:
                    config = XttsConfig()
                    config.load_json(cfg_path)
                    print("✅ Config object created successfully")
                    
                    # Thử khởi tạo model
                    try:
                        model = Xtts.init_from_config(config)
                        print("✅ Model initialized from config successfully")
                        
                        # Thử load checkpoint
                        try:
                            model.load_checkpoint(tts_ckpt, spk_ckpt)
                            print("🎉 SUCCESS: All steps completed!")
                            return True
                            
                        except Exception as e:
                            print(f"❌ Failed at load_checkpoint: {e}")
                            import traceback
                            traceback.print_exc()
                            
                    except Exception as e:
                        print(f"❌ Failed at init_from_config: {e}")
                        import traceback
                        traceback.print_exc()
                        
                except Exception as e:
                    print(f"❌ Failed at config.load_json: {e}")
                    import traceback
                    traceback.print_exc()
                    
            except Exception as e:
                print(f"❌ Failed to import XttsConfig: {e}")
                
        except Exception as e:
            print(f"❌ Failed to import Xtts: {e}")
            
    except Exception as e:
        print(f"❌ Error importing TTS: {e}")
    
    return False

if __name__ == "__main__":
    print("🚀 XTTS Debug Script")
    print("=" * 50)
    
    success = debug_xtts_loading()
    
    if success:
        print("\n🎉 Debug completed successfully!")
    else:
        print("\n❌ Debug completed with errors!")
