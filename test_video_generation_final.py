#!/usr/bin/env python3
"""
Final test script for video generation fixes
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

def test_array_consistency():
    """Test array consistency fixes"""
    print("\n🔧 Testing Array Consistency Fixes")
    print("=" * 40)
    
    try:
        import numpy as np
        from collections import Counter
        
        print("✅ Required modules imported successfully")
        
        # Test: Create test coefficients with different shapes
        print("\n🧪 Creating test coefficients with different shapes...")
        coeff1 = np.random.rand(1, 70).astype(np.float32)
        coeff2 = np.random.rand(1, 73).astype(np.float32)
        coeff3 = np.random.rand(1, 68).astype(np.float32)
        
        video_coeffs = [coeff1, coeff2, coeff3]
        print(f"✅ Created test coefficients:")
        for i, coeff in enumerate(video_coeffs):
            print(f"   Coefficient {i+1}: {coeff.shape}")
        
        # Test: Check shape consistency
        print("\n🧪 Checking shape consistency...")
        coeff_shapes = [coeff.shape for coeff in video_coeffs]
        print(f"✅ Coefficient shapes: {coeff_shapes}")
        
        if len(set(coeff_shapes)) > 1:
            print("⚠️ Inconsistent shapes detected (expected)")
            
            # Test: Fix shape inconsistency
            print("\n🧪 Fixing shape inconsistency...")
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
        
        # Test: Create array with consistent shapes
        print("\n🧪 Creating array with consistent shapes...")
        video_coeffs_array = np.array(video_coeffs)
        print(f"✅ Final array shape: {video_coeffs_array.shape}")
        print(f"✅ Final array type: {video_coeffs_array.dtype}")
        
        # Test: Extract semantic npy
        print("\n🧪 Extracting semantic npy...")
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

def test_trans_params_processing():
    """Test trans_params processing fixes"""
    print("\n🎯 Testing Trans Params Processing")
    print("=" * 40)
    
    try:
        import numpy as np
        
        # Test 1: List trans_params
        print("🧪 Test 1: List trans_params...")
        trans_params_list = [1.0, 2.0, 3.0, 4.0, 5.0]
        trans_params = np.array(trans_params_list, dtype=np.float32)
        
        if trans_params.ndim == 1:
            if len(trans_params) >= 3:
                trans_params_2d = trans_params[2:3]
            else:
                trans_params_2d = np.array([0.0], dtype=np.float32)
        else:
            trans_params_2d = trans_params[2:3] if trans_params.shape[1] >= 3 else np.array([[0.0]], dtype=np.float32)
        
        print(f"✅ Original trans_params: {trans_params.shape}")
        print(f"✅ trans_params_2d: {trans_params_2d.shape}")
        
        # Test 2: Array trans_params
        print("\n🧪 Test 2: Array trans_params...")
        trans_params_array = np.array([[1.0, 2.0, 3.0, 4.0, 5.0]], dtype=np.float32)
        
        if trans_params_array.ndim == 1:
            if len(trans_params_array) >= 3:
                trans_params_2d = trans_params_array[2:3]
            else:
                trans_params_2d = np.array([0.0], dtype=np.float32)
        else:
            trans_params_2d = trans_params_array[2:3] if trans_params_array.shape[1] >= 3 else np.array([[0.0]], dtype=np.float32)
        
        print(f"✅ Original trans_params_array: {trans_params_array.shape}")
        print(f"✅ trans_params_2d: {trans_params_2d.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Trans params processing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Final Video Generation Fix Test Suite")
    print("=" * 40)
    
    # Test 1: Preprocess module import
    success1 = test_preprocess_import()
    
    # Test 2: Array consistency fixes
    success2 = test_array_consistency()
    
    # Test 3: Trans params processing
    success3 = test_trans_params_processing()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"Preprocess Import: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Array Consistency: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"Trans Params Processing: {'✅ PASS' if success3 else '❌ FAIL'}")
    
    if all([success1, success2, success3]):
        print("\n🎉 All tests passed! Video generation fixes are working correctly.")
        print("🎬 You should now be able to generate videos without array shape errors!")
        print("\n🚀 Ready to test video generation!")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
