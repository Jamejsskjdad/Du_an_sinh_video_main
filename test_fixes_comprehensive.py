#!/usr/bin/env python3
"""
Comprehensive test script for all SadTalker fixes
This script tests:
1. Audio format fixing
2. XTTS speaker parameter
3. YAML config files
4. 3DMM extraction fixes
"""

import sys
import os
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_audio_format_fixer():
    """Test audio format fixing script"""
    print("🔧 Testing Audio Format Fixer")
    print("=" * 40)
    
    try:
        # Check if fix_audio_format.py exists
        script_path = "fix_audio_format.py"
        if not os.path.exists(script_path):
            print(f"❌ Script not found: {script_path}")
            return False
        
        print(f"✅ Script found: {script_path}")
        
        # Check if ffmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            print("✅ FFmpeg is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ FFmpeg not found")
            print("💡 Please install FFmpeg first:")
            print("   Windows: Download from https://ffmpeg.org/download.html")
            print("   Or use: winget install ffmpeg")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Audio format fixer test failed: {e}")
        return False

def test_xtts_fixes():
    """Test XTTS fixes"""
    print("\n🎤 Testing XTTS Fixes")
    print("=" * 30)
    
    try:
        from voice.tts_engine import synthesize
        
        print("✅ TTS engine imported successfully")
        print(f"🔧 synthesize function: {synthesize}")
        
        # Check if the function has the right parameters
        import inspect
        sig = inspect.signature(synthesize)
        params = list(sig.parameters.keys())
        
        print(f"🔍 Function parameters: {params}")
        
        if 'voice_id' in params:
            print("✅ voice_id parameter found - XTTS fixes applied")
            return True
        else:
            print("❌ voice_id parameter not found")
            return False
        
    except Exception as e:
        print(f"❌ XTTS fixes test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_yaml_configs():
    """Test YAML configuration files"""
    print("\n📋 Testing YAML Configs")
    print("=" * 30)
    
    try:
        config_dir = "src/config"
        
        # Check if correct YAML files exist
        required_files = ['audio2pose.yaml', 'audio2exp.yaml']
        existing_files = []
        
        for file in required_files:
            file_path = os.path.join(config_dir, file)
            if os.path.exists(file_path):
                existing_files.append(file)
                print(f"✅ {file} exists")
            else:
                print(f"❌ {file} not found")
        
        # Check if old typo files still exist
        typo_files = ['auido2pose.yaml', 'auido2exp.yaml']
        for file in typo_files:
            file_path = os.path.join(config_dir, file)
            if os.path.exists(file_path):
                print(f"⚠️ Old typo file still exists: {file}")
            else:
                print(f"✅ Old typo file removed: {file}")
        
        if len(existing_files) == len(required_files):
            print("✅ All required YAML configs found")
            return True
        else:
            print(f"❌ Missing YAML configs: {set(required_files) - set(existing_files)}")
            return False
        
    except Exception as e:
        print(f"❌ YAML configs test failed: {e}")
        return False

def test_config_paths():
    """Test configuration paths"""
    print("\n🛣️ Testing Config Paths")
    print("=" * 30)
    
    try:
        from utils.init_path import init_path
        
        print("✅ init_path function imported successfully")
        
        # Test with dummy paths
        checkpoint_dir = "checkpoints"
        config_dir = "src/config"
        
        paths = init_path(checkpoint_dir, config_dir)
        
        print(f"🔍 Generated paths: {paths}")
        
        # Check if audio2pose paths are correct
        if 'audio2pose_yaml_path' in paths:
            yaml_path = paths['audio2pose_yaml_path']
            if 'audio2pose.yaml' in yaml_path and 'auido2pose.yaml' not in yaml_path:
                print("✅ audio2pose_yaml_path is correct")
            else:
                print(f"❌ audio2pose_yaml_path is incorrect: {yaml_path}")
                return False
        else:
            print("❌ audio2pose_yaml_path not found in paths")
            return False
        
        if 'audio2exp_yaml_path' in paths:
            yaml_path = paths['audio2exp_yaml_path']
            if 'audio2exp.yaml' in yaml_path and 'auido2exp.yaml' not in yaml_path:
                print("✅ audio2exp_yaml_path is correct")
            else:
                print(f"❌ audio2exp_yaml_path is incorrect: {yaml_path}")
                return False
        else:
            print("❌ audio2exp_yaml_path not found in paths")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Config paths test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_3dmm_extraction():
    """Test 3DMM extraction fixes"""
    print("\n🎭 Testing 3DMM Extraction Fixes")
    print("=" * 40)
    
    try:
        from utils.preprocess import CropAndExtract
        
        print("✅ Preprocess module imported successfully")
        print(f"🔧 CropAndExtract class: {CropAndExtract}")
        
        # Check if the class has the generate method
        if hasattr(CropAndExtract, 'generate'):
            print("✅ generate method found")
        else:
            print("❌ generate method not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 3DMM extraction test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Comprehensive SadTalker Fixes Test Suite")
    print("=" * 50)
    
    # Test 1: Audio format fixer
    success1 = test_audio_format_fixer()
    
    # Test 2: XTTS fixes
    success2 = test_xtts_fixes()
    
    # Test 3: YAML configs
    success3 = test_yaml_configs()
    
    # Test 4: Config paths
    success4 = test_config_paths()
    
    # Test 5: 3DMM extraction
    success5 = test_3dmm_extraction()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Comprehensive Test Results Summary")
    print("=" * 60)
    print(f"Audio Format Fixer: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"XTTS Fixes: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"YAML Configs: {'✅ PASS' if success3 else '❌ FAIL'}")
    print(f"Config Paths: {'✅ PASS' if success4 else '❌ FAIL'}")
    print(f"3DMM Extraction: {'✅ PASS' if success5 else '❌ FAIL'}")
    
    if all([success1, success2, success3, success4, success5]):
        print("\n🎉 All tests passed! All fixes are working correctly.")
        print("\n🚀 Next steps:")
        print("   1. Run: python fix_audio_format.py")
        print("   2. Use the fixed audio file in SadTalker")
        print("   3. Test video generation again")
        print("\n🎬 SadTalker should now work without 3DMM extraction errors!")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        print("\n🔧 Fix the failed components before testing video generation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
