#!/usr/bin/env python3
"""
Fix audio format for SadTalker pipeline
This script converts audio to the correct format (16kHz mono PCM) to prevent 3DMM extraction errors
"""

import os
import subprocess
import sys

def fix_audio_format(input_path, output_path=None):
    """
    Fix audio format to 16kHz mono PCM s16 for SadTalker compatibility
    
    Args:
        input_path: Path to input audio file
        output_path: Path to output audio file (optional)
    
    Returns:
        Path to fixed audio file
    """
    if output_path is None:
        # Create output path in same directory
        dir_path = os.path.dirname(input_path)
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(dir_path, f"{name}_16k_mono.wav")
    
    print(f"🔧 Fixing audio format...")
    print(f"📥 Input: {input_path}")
    print(f"📤 Output: {output_path}")
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        return None
    
    try:
        # Convert to 16kHz mono PCM s16
        cmd = [
            'ffmpeg', '-y',  # Overwrite output
            '-i', input_path,  # Input file
            '-ac', '1',  # Mono (1 channel)
            '-ar', '16000',  # 16kHz sample rate
            '-sample_fmt', 's16',  # 16-bit signed PCM
            '-af', 'apad=pad_dur=0.5',  # Pad with 0.5s silence
            output_path  # Output file
        ]
        
        print(f"🔄 Running command: {' '.join(cmd)}")
        
        # Run ffmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Audio format fixed successfully!")
            
            # Verify output file
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"✅ Output file verified: {os.path.getsize(output_path)} bytes")
                return output_path
            else:
                print(f"❌ Output file verification failed")
                return None
        else:
            print(f"❌ FFmpeg failed with return code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print(f"❌ FFmpeg not found. Please install FFmpeg first.")
        print(f"   Windows: Download from https://ffmpeg.org/download.html")
        print(f"   Or use: winget install ffmpeg")
        return None
    except Exception as e:
        print(f"❌ Error fixing audio format: {e}")
        return None

def check_audio_info(audio_path):
    """
    Check audio file information using ffprobe
    """
    try:
        cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', 
               '-show_format', '-show_streams', audio_path]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"🔍 Audio file info for: {audio_path}")
            print(f"📊 {result.stdout}")
        else:
            print(f"⚠️ Could not get audio info: {result.stderr}")
            
    except Exception as e:
        print(f"⚠️ Error checking audio info: {e}")

def main():
    """Main function"""
    print("🚀 Audio Format Fixer for SadTalker")
    print("=" * 40)
    
    # Check if ffmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg not found. Please install FFmpeg first.")
        print("   Windows: Download from https://ffmpeg.org/download.html")
        print("   Or use: winget install ffmpeg")
        return False
    
    # Default input path (from your log)
    default_input = "data/tmp/voice_out.wav"
    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = default_input
        print(f"📝 Using default input path: {input_path}")
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        print(f"💡 Please provide a valid audio file path as argument")
        print(f"   Example: python fix_audio_format.py path/to/your/audio.wav")
        return False
    
    # Check original audio info
    print(f"\n🔍 Checking original audio...")
    check_audio_info(input_path)
    
    # Fix audio format
    print(f"\n🔧 Fixing audio format...")
    fixed_path = fix_audio_format(input_path)
    
    if fixed_path:
        print(f"\n✅ Audio format fixed successfully!")
        print(f"📁 Fixed file: {fixed_path}")
        
        # Check fixed audio info
        print(f"\n🔍 Checking fixed audio...")
        check_audio_info(fixed_path)
        
        print(f"\n🎯 Next steps:")
        print(f"   1. Use this fixed audio file in SadTalker: {fixed_path}")
        print(f"   2. The audio is now 16kHz mono PCM, compatible with SadTalker")
        print(f"   3. This should fix the 3DMM extraction error")
        
        return True
    else:
        print(f"\n❌ Failed to fix audio format")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

