#!/usr/bin/env python3
"""
Debug script for 3DMM extraction issues
This script helps identify the exact problem with array shape inhomogeneity
"""

import sys
import os
import numpy as np
import torch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def debug_3dmm_extraction():
    """Debug 3DMM extraction step by step"""
    print("🧪 Debugging 3DMM Extraction Issues")
    print("=" * 50)
    
    try:
        from utils.preprocess import CropAndExtract
        from face3d.util.preprocess import align_img, extract_5p
        
        print("📦 Successfully imported 3DMM functions")
        
        # Test data creation
        print("\n🔧 Creating test data...")
        
        # Test 1: Landmark data
        print("🧪 Test 1: Landmark data shape consistency")
        test_lm = np.random.rand(68, 2).astype(np.float32)
        print(f"✅ Landmark shape: {test_lm.shape}")
        
        # Test 2: Extract 5 points
        print("\n🧪 Test 2: Extract 5 points")
        try:
            lm5p = extract_5p(test_lm)
            print(f"✅ 5-point landmark shape: {lm5p.shape}")
            print(f"✅ 5-point landmark data type: {lm5p.dtype}")
        except Exception as e:
            print(f"❌ Extract 5 points failed: {e}")
            return False
        
        # Test 3: Standard 3D landmarks
        print("\n🧪 Test 3: Standard 3D landmarks")
        try:
            # Create standard 3D landmarks (5, 3)
            lm3d_std = np.random.rand(5, 3).astype(np.float32)
            print(f"✅ Standard 3D landmarks shape: {lm3d_std.shape}")
            print(f"✅ Standard 3D landmarks data type: {lm3d_std.dtype}")
        except Exception as e:
            print(f"❌ Standard 3D landmarks failed: {e}")
            return False
        
        # Test 4: Image alignment
        print("\n🧪 Test 4: Image alignment")
        try:
            from PIL import Image
            
            # Create test image
            test_img = Image.new('RGB', (256, 256), color='red')
            print(f"✅ Test image created: {test_img.size}")
            
            # Test alignment
            trans_params, img_new, lm_new, mask_new = align_img(
                test_img, test_lm, lm3d_std, target_size=224.
            )
            print(f"✅ Alignment successful")
            print(f"✅ Trans params shape: {trans_params.shape}")
            print(f"✅ Trans params type: {trans_params.dtype}")
            print(f"✅ New image size: {img_new.size}")
            print(f"✅ New landmarks shape: {lm_new.shape}")
            
        except Exception as e:
            print(f"❌ Image alignment failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Test 5: Coefficient concatenation
        print("\n🧪 Test 5: Coefficient concatenation")
        try:
            # Create test coefficients
            exp_coeff = np.random.rand(1, 64).astype(np.float32)
            angle_coeff = np.random.rand(1, 3).astype(np.float32)
            trans_coeff = np.random.rand(1, 3).astype(np.float32)
            trans_params_2d = np.random.rand(1, 3).astype(np.float32)
            
            print(f"✅ Exp coeff shape: {exp_coeff.shape}")
            print(f"✅ Angle coeff shape: {angle_coeff.shape}")
            print(f"✅ Trans coeff shape: {trans_coeff.shape}")
            print(f"✅ Trans params 2D shape: {trans_params_2d.shape}")
            
            # Test concatenation
            pred_coeff = np.concatenate([
                exp_coeff, 
                angle_coeff,
                trans_coeff,
                trans_params_2d,
            ], axis=1)
            
            print(f"✅ Concatenated coeff shape: {pred_coeff.shape}")
            print(f"✅ Concatenated coeff type: {pred_coeff.dtype}")
            
        except Exception as e:
            print(f"❌ Coefficient concatenation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Test 6: Array consistency check
        print("\n🧪 Test 6: Array consistency check")
        try:
            # Create test video coefficients
            video_coeffs = []
            for i in range(3):  # Simulate 3 frames
                frame_coeff = np.random.rand(1, 73).astype(np.float32)  # 64+3+3+3
                video_coeffs.append(frame_coeff)
            
            print(f"✅ Video coeffs length: {len(video_coeffs)}")
            print(f"✅ Each frame coeff shape: {video_coeffs[0].shape}")
            
            # Check if all have same shape
            shapes = [coeff.shape for coeff in video_coeffs]
            print(f"✅ All shapes: {shapes}")
            
            if len(set(shapes)) == 1:
                print("✅ All coefficients have consistent shapes")
            else:
                print("⚠️ Inconsistent shapes detected!")
                return False
            
            # Convert to numpy array
            video_coeffs_array = np.array(video_coeffs)
            print(f"✅ Final array shape: {video_coeffs_array.shape}")
            print(f"✅ Final array type: {video_coeffs_array.dtype}")
            
        except Exception as e:
            print(f"❌ Array consistency check failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print("\n🎉 All 3DMM extraction tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_landmark_loading():
    """Debug landmark loading issues"""
    print("\n🔍 Debugging Landmark Loading")
    print("=" * 35)
    
    try:
        # Check if there are any existing landmark files
        results_dir = "results"
        if os.path.exists(results_dir):
            print(f"📁 Results directory exists: {results_dir}")
            
            # Look for landmark files
            for root, dirs, files in os.walk(results_dir):
                for file in files:
                    if 'landmarks' in file:
                        file_path = os.path.join(root, file)
                        try:
                            lm = np.loadtxt(file_path).astype(np.float32)
                            print(f"✅ Landmark file: {file_path}")
                            print(f"   Shape: {lm.shape}")
                            print(f"   Type: {lm.dtype}")
                            print(f"   Min: {lm.min()}, Max: {lm.max()}")
                            
                            # Check for NaN or inf values
                            if np.any(np.isnan(lm)) or np.any(np.isinf(lm)):
                                print(f"   ⚠️ Contains NaN or inf values!")
                            
                        except Exception as e:
                            print(f"❌ Failed to load landmark file {file_path}: {e}")
        else:
            print("⚠️ Results directory not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Landmark loading debug failed: {e}")
        return False

def main():
    """Main debug function"""
    print("🚀 3DMM Extraction Debug Suite")
    print("=" * 40)
    
    # Test 1: 3DMM extraction
    success1 = debug_3dmm_extraction()
    
    # Test 2: Landmark loading
    success2 = debug_landmark_loading()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Debug Results Summary")
    print("=" * 50)
    print(f"3DMM Extraction: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Landmark Loading: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All debug tests passed! 3DMM extraction should work.")
        return True
    else:
        print("\n⚠️ Some debug tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

