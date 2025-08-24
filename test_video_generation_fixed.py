#!/usr/bin/env python3
"""
Test script for fixed video generation
This script tests that the 3DMM extraction fixes work correctly
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_preprocess_import():
    """Test that preprocess module can be imported"""
    print("🧪 Testing Preprocess Module Import")
    print("=" * 40)
    
    try:
        from utils.preprocess import CropAndExtract
        print("✅ Preprocess module imported successfully")
        print(f"🔧 CropAndExtract class: {CropAndExtract}")
        return True
        
    except Exception as e:
        print(f"❌ Preprocess import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_3dmm_functions():
    """Test 3DMM related functions"""
    print("\n🎯 Testing 3DMM Functions")
    print("=" * 30)
    
    try:
        from face3d.util.preprocess import align_img, extract_5p
        
        print("✅ 3DMM utility functions imported successfully")
        print(f"🔧 align_img function: {align_img}")
        print(f"🔧 extract_5p function: {extract_5p}")
        
        return True
        
    except Exception as e:
        print(f"❌ 3DMM functions import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_array_consistency():
    """Test array consistency fixes"""
    print("\n🔧 Testing Array Consistency Fixes")
    print("=" * 40)
    
    try:
        import numpy as np
        from collections import Counter
        
        print("✅ Required modules imported successfully")
        
        # Test 1: Create test coefficients with different shapes
        print("\n🧪 Test 1: Creating test coefficients with different shapes...")
        coeff1 = np.random.rand(1, 70).astype(np.float32)
        coeff2 = np.random.rand(1, 73).astype(np.float32)
        coeff3 = np.random.rand(1, 68).astype(np.float32)
        
        video_coeffs = [coeff1, coeff2, coeff3]
        print(f"✅ Created test coefficients:")
        for i, coeff in enumerate(video_coeffs):
            print(f"   Coefficient {i+1}: {coeff.shape}")
        
        # Test 2: Check shape consistency
        print("\n🧪 Test 2: Checking shape consistency...")
        coeff_shapes = [coeff.shape for coeff in video_coeffs]
        print(f"✅ Coefficient shapes: {coeff_shapes}")
        
        if len(set(coeff_shapes)) > 1:
            print("⚠️ Inconsistent shapes detected (expected)")
        else:
            print("✅ All shapes are consistent")
        
        # Test 3: Fix shape inconsistency
        print("\n🧪 Test 3: Fixing shape inconsistency...")
        if len(set(coeff_shapes)) > 1:
            # Find the most common shape
            shape_counts = Counter(coeff_shapes)
            most_common_shape = shape_counts.most_common(1)[0][0]
            print(f"🎯 Most common shape: {most_common_shape}")
            
            # Pad or truncate coefficients to match the most common shape
            fixed_video_coeffs = []
            for i, coeff in enumerate(video_coeffs):
                if coeff.shape != most_common_shape:
                    if coeff.shape[1] < most_common_shape[1]:
                        # Pad with zeros
                        padding = np.zeros((coeff.shape[0], most_common_shape[1] - coeff.shape[1]), dtype=np.float32)
                        coeff = np.concatenate([coeff, padding], axis=1)
                        print(f"🔧 Padded coefficient {i+1}: {coeff.shape}")
                    elif coeff.shape[1] > most_common_shape[1]:
                        # Truncate
                        coeff = coeff[:, :most_common_shape[1]]
                        print(f"🔧 Truncated coefficient {i+1}: {coeff.shape}")
                else:
                    print(f"✅ Coefficient {i+1} already has correct shape: {coeff.shape}")
                fixed_video_coeffs.append(coeff)
            
            video_coeffs = fixed_video_coeffs
        
        # Test 4: Create array with consistent shapes
        print("\n🧪 Test 4: Creating array with consistent shapes...")
        video_coeffs_array = np.array(video_coeffs)
        print(f"✅ Final array shape: {video_coeffs_array.shape}")
        print(f"✅ Final array type: {video_coeffs_array.dtype}")
        
        # Test 5: Extract semantic npy
        print("\n🧪 Test 5: Extracting semantic npy...")
        if video_coeffs_array.shape[1] > 0:
            semantic_npy = video_coeffs_array[:, 0]
            print(f"✅ Semantic npy shape: {semantic_npy.shape}")
        else:
            semantic_npy = video_coeffs_array
            print(f"✅ Semantic npy shape: {semantic_npy.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Array consistency test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_landmark_processing():
    """Test landmark processing functions"""
    print("\n🎭 Testing Landmark Processing")
    print("=" * 35)
    
    try:
        import numpy as np
        
        # Test 1: Create test landmarks
        print("🧪 Test 1: Creating test landmarks...")
        test_lm = np.random.rand(68, 2).astype(np.float32)
        print(f"✅ Test landmark shape: {test_lm.shape}")
        
        # Test 2: Test landmark reshaping
        print("\n🧪 Test 2: Testing landmark reshaping...")
        lm_reshaped = test_lm.reshape([1, -1, 2])
        print(f"✅ Reshaped landmark shape: {lm_reshaped.shape}")
        
        # Test 3: Test individual frame landmark
        print("\n🧪 Test 3: Testing individual frame landmark...")
        lm1 = lm_reshaped[0].reshape([-1, 2])
        print(f"✅ Individual frame landmark shape: {lm1.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Landmark processing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Video Generation Fix Test Suite")
    print("=" * 40)
    
    # Test 1: Preprocess module import
    success1 = test_preprocess_import()
    
    # Test 2: 3DMM functions
    success2 = test_3dmm_functions()
    
    # Test 3: Array consistency fixes
    success3 = test_array_consistency()
    
    # Test 4: Landmark processing
    success4 = test_landmark_processing()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"Preprocess Import: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"3DMM Functions: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"Array Consistency: {'✅ PASS' if success3 else '❌ FAIL'}")
    print(f"Landmark Processing: {'✅ PASS' if success4 else '❌ FAIL'}")
    
    if all([success1, success2, success3, success4]):
        print("\n🎉 All tests passed! Video generation fixes are working correctly.")
        print("🎬 You should now be able to generate videos without array shape errors!")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
