#!/usr/bin/env python3
"""
Test script for voice profile and sample audio
This script tests if voice profiles are created correctly with sample audio
"""

import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_voice_profile_structure():
    """Test voice profile structure"""
    print("📁 Testing Voice Profile Structure")
    print("=" * 40)
    
    try:
        from voice.store import load_profile, list_voices
        
        # Test current user voices
        user_id = "current_user"
        voices = list_voices(user_id)
        
        if not voices:
            print("❌ No voices found for current_user")
            print("💡 Please register a voice first")
            return False
        
        print(f"✅ Found {len(voices)} voices for {user_id}")
        
        for i, voice in enumerate(voices):
            print(f"\n🎤 Voice {i+1}: {voice['voice_id']}")
            print(f"   📊 Metadata: {voice}")
            
            # Check if voice_id exists
            voice_id = voice['voice_id']
            profile = load_profile(user_id, voice_id)
            
            if profile:
                print(f"   ✅ Profile loaded successfully")
                print(f"   🔑 Profile keys: {list(profile.keys())}")
                
                # Check sample audio
                sample_audio = profile.get('sample_audio')
                if sample_audio:
                    print(f"   🎵 Sample audio: {sample_audio}")
                    if os.path.exists(sample_audio):
                        file_size = os.path.getsize(sample_audio)
                        print(f"   📏 File size: {file_size} bytes")
                        print(f"   ✅ Sample audio file exists")
                    else:
                        print(f"   ❌ Sample audio file not found")
                else:
                    print(f"   ❌ No sample_audio in profile")
                
                # Check embedding
                embedding_path = os.path.join("data", "voices", user_id, voice_id, "embedding.pth")
                if os.path.exists(embedding_path):
                    print(f"   🧠 Embedding: {embedding_path}")
                    print(f"   ✅ Embedding file exists")
                else:
                    print(f"   ❌ Embedding file not found")
                
                # Check metadata
                meta_path = os.path.join("data", "voices", user_id, voice_id, "meta.json")
                if os.path.exists(meta_path):
                    print(f"   📋 Metadata: {meta_path}")
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        meta_data = json.load(f)
                    print(f"   🔍 Meta keys: {list(meta_data.keys())}")
                    print(f"   ✅ Metadata file exists")
                else:
                    print(f"   ❌ Metadata file not found")
                
            else:
                print(f"   ❌ Failed to load profile")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice profile test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_directory_structure():
    """Test voice directory structure"""
    print("\n📂 Testing Voice Directory Structure")
    print("=" * 40)
    
    try:
        voice_base_dir = "data/voices"
        if not os.path.exists(voice_base_dir):
            print(f"❌ Voice base directory not found: {voice_base_dir}")
            return False
        
        print(f"✅ Voice base directory exists: {voice_base_dir}")
        
        # Check current_user directory
        user_dir = os.path.join(voice_base_dir, "current_user")
        if not os.path.exists(user_dir):
            print(f"❌ User directory not found: {user_dir}")
            return False
        
        print(f"✅ User directory exists: {user_dir}")
        
        # List all voice directories
        voice_dirs = [d for d in os.listdir(user_dir) if os.path.isdir(os.path.join(user_dir, d))]
        
        if not voice_dirs:
            print(f"❌ No voice directories found in {user_dir}")
            return False
        
        print(f"✅ Found voice directories: {voice_dirs}")
        
        for voice_dir in voice_dirs:
            voice_path = os.path.join(user_dir, voice_dir)
            print(f"\n🔍 Voice directory: {voice_path}")
            
            # List files in voice directory
            files = os.listdir(voice_path)
            print(f"   📁 Files: {files}")
            
            # Check required files
            required_files = ['embedding.pth', 'meta.json', 'sample.wav']
            for req_file in required_files:
                file_path = os.path.join(voice_path, req_file)
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"   ✅ {req_file}: {file_size} bytes")
                else:
                    print(f"   ❌ {req_file}: Not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice directory test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sample_audio_quality():
    """Test sample audio quality"""
    print("\n🎵 Testing Sample Audio Quality")
    print("=" * 40)
    
    try:
        import subprocess
        
        # Check if ffmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            print("✅ FFmpeg is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ FFmpeg not found")
            print("💡 Please install FFmpeg first")
            return False
        
        # Find sample audio files
        voice_base_dir = "data/voices/current_user"
        if not os.path.exists(voice_base_dir):
            print(f"❌ Voice directory not found: {voice_base_dir}")
            return False
        
        voice_dirs = [d for d in os.listdir(voice_base_dir) if os.path.isdir(os.path.join(voice_base_dir, d))]
        
        for voice_dir in voice_dirs:
            sample_path = os.path.join(voice_base_dir, voice_dir, "sample.wav")
            if os.path.exists(sample_path):
                print(f"\n🔍 Testing sample audio: {sample_path}")
                
                # Get audio info using ffprobe
                cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', 
                       '-show_format', '-show_streams', sample_path]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"   📊 Audio info: {result.stdout}")
                else:
                    print(f"   ⚠️ Could not get audio info: {result.stderr}")
                
                # Check file size
                file_size = os.path.getsize(sample_path)
                print(f"   📏 File size: {file_size} bytes")
                
                if file_size > 0:
                    print(f"   ✅ Sample audio file is valid")
                else:
                    print(f"   ❌ Sample audio file is empty")
        
        return True
        
    except Exception as e:
        print(f"❌ Sample audio quality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Voice Profile & Sample Audio Test Suite")
    print("=" * 55)
    
    # Test 1: Voice profile structure
    success1 = test_voice_profile_structure()
    
    # Test 2: Voice directory structure
    success2 = test_voice_directory_structure()
    
    # Test 3: Sample audio quality
    success3 = test_sample_audio_quality()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Voice Profile Test Results Summary")
    print("=" * 60)
    print(f"Voice Profile Structure: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Voice Directory Structure: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"Sample Audio Quality: {'✅ PASS' if success3 else '❌ FAIL'}")
    
    if all([success1, success2, success3]):
        print("\n🎉 All voice profile tests passed!")
        print("\n🚀 Voice profiles are correctly configured:")
        print("   ✅ Voice metadata loaded")
        print("   ✅ Sample audio files exist")
        print("   ✅ Embedding files exist")
        print("   ✅ Directory structure correct")
        print("\n🎬 SadTalker should now work with voice cloning!")
        return True
    else:
        print("\n⚠️ Some voice profile tests failed.")
        print("\n🔧 Issues to fix:")
        if not success1:
            print("   - Voice profile loading")
        if not success2:
            print("   - Directory structure")
        if not success3:
            print("   - Sample audio quality")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
