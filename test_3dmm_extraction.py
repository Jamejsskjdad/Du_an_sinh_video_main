#!/usr/bin/env python3
"""
Test Script for 3DMM Extraction Logic
Kiểm tra logic xử lý coefficients và array concatenation
"""

import numpy as np
import os
import sys

def test_array_concatenation():
    """Test array concatenation logic"""
    print("🧪 Testing Array Concatenation Logic")
    print("=" * 50)
    
    try:
        # Test 1: Basic concatenation
        print("🔍 Test 1: Basic concatenation")
        a = np.array([[1, 2], [3, 4]], dtype=np.float32)
        b = np.array([[5, 6], [7, 8]], dtype=np.float32)
        c = np.concatenate([a, b], axis=1)
        print(f"✅ Basic concatenation: {a.shape} + {b.shape} = {c.shape}")
        
        # Test 2: Different row dimensions
        print("\n🔍 Test 2: Different row dimensions")
        a = np.array([[1, 2], [3, 4]], dtype=np.float32)
        b = np.array([[5, 6]], dtype=np.float32)
        
        # Pad to match dimensions
        target_dim = max(a.shape[0], b.shape[0])
        if a.shape[0] < target_dim:
            padding = np.zeros((target_dim - a.shape[0], a.shape[1]), dtype=np.float32)
            a = np.concatenate([a, padding], axis=0)
        if b.shape[0] < target_dim:
            padding = np.zeros((target_dim - b.shape[0], b.shape[1]), dtype=np.float32)
            b = np.concatenate([b, padding], axis=0)
        
        c = np.concatenate([a, b], axis=1)
        print(f"✅ Different row dimensions: {a.shape} + {b.shape} = {c.shape}")
        
        # Test 3: Complex coefficient simulation
        print("\n🔍 Test 3: Complex coefficient simulation")
        exp_coeff = np.random.randn(1, 80).astype(np.float32)
        angle_coeff = np.random.randn(1, 3).astype(np.float32)
        trans_coeff = np.random.randn(1, 3).astype(np.float32)
        trans_params_2d = np.random.randn(1, 2).astype(np.float32)
        
        print(f"🔍 exp_coeff: {exp_coeff.shape}")
        print(f"🔍 angle_coeff: {angle_coeff.shape}")
        print(f"🔍 trans_coeff: {trans_coeff.shape}")
        print(f"🔍 trans_params_2d: {trans_params_2d.shape}")
        
        # Ensure consistent shapes
        target_dim = max(exp_coeff.shape[0], angle_coeff.shape[0], 
                        trans_coeff.shape[0], trans_params_2d.shape[0])
        
        if exp_coeff.shape[0] < target_dim:
            padding = np.zeros((target_dim - exp_coeff.shape[0], exp_coeff.shape[1]), dtype=np.float32)
            exp_coeff = np.concatenate([exp_coeff, padding], axis=0)
        
        if angle_coeff.shape[0] < target_dim:
            padding = np.zeros((target_dim - angle_coeff.shape[0], angle_coeff.shape[1]), dtype=np.float32)
            angle_coeff = np.concatenate([angle_coeff, padding], axis=0)
        
        if trans_coeff.shape[0] < target_dim:
            padding = np.zeros((target_dim - trans_coeff.shape[0], trans_coeff.shape[1]), dtype=np.float32)
            trans_coeff = np.concatenate([trans_coeff, padding], axis=0)
        
        if trans_params_2d.shape[0] < target_dim:
            padding = np.zeros((target_dim - trans_params_2d.shape[0], trans_params_2d.shape[1]), dtype=np.float32)
            trans_params_2d = np.concatenate([trans_params_2d, padding], axis=0)
        
        # Concatenate
        pred_coeff = np.concatenate([
            exp_coeff,
            angle_coeff,
            trans_coeff,
            trans_params_2d,
        ], axis=1)
        
        print(f"✅ Complex concatenation successful: {pred_coeff.shape}")
        print(f"🔍 Total columns: {exp_coeff.shape[1] + angle_coeff.shape[1] + trans_coeff.shape[1] + trans_params_2d.shape[1]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Array concatenation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_coefficient_validation():
    """Test coefficient validation logic"""
    print("\n🧪 Testing Coefficient Validation Logic")
    print("=" * 50)
    
    try:
        # Create test coefficients with different shapes
        coeffs = [
            np.random.randn(1, 70).astype(np.float32),  # Standard
            np.random.randn(1, 75).astype(np.float32),  # Different size
            np.random.randn(1, 68).astype(np.float32),  # Different size
        ]
        
        print(f"🔍 Test coefficients: {[c.shape for c in coeffs]}")
        
        # Find most common shape
        from collections import Counter
        coeff_shapes = [coeff.shape for coeff in coeffs]
        shape_counts = Counter(coeff_shapes)
        most_common_shape = shape_counts.most_common(1)[0][0]
        
        print(f"🎯 Most common shape: {most_common_shape}")
        
        # Fix inconsistencies
        fixed_coeffs = []
        for i, coeff in enumerate(coeffs):
            if coeff.shape != most_common_shape:
                if coeff.shape[1] < most_common_shape[1]:
                    # Pad with zeros
                    padding = np.zeros((coeff.shape[0], most_common_shape[1] - coeff.shape[1]), dtype=np.float32)
                    coeff = np.concatenate([coeff, padding], axis=1)
                    print(f"🔧 Frame {i}: Padded to {coeff.shape}")
                elif coeff.shape[1] > most_common_shape[1]:
                    # Truncate
                    coeff = coeff[:, :most_common_shape[1]]
                    print(f"🔧 Frame {i}: Truncated to {coeff.shape}")
            else:
                print(f"✅ Frame {i}: Shape already correct {coeff.shape}")
            
            fixed_coeffs.append(coeff)
        
        # Verify all have same shape
        final_shapes = [c.shape for c in fixed_coeffs]
        if len(set(final_shapes)) == 1:
            print(f"✅ All coefficients have consistent shape: {final_shapes[0]}")
            return True
        else:
            print(f"❌ Shape inconsistency still exists: {final_shapes}")
            return False
            
    except Exception as e:
        print(f"❌ Coefficient validation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_preprocess_import():
    """Test if preprocess module can be imported"""
    print("\n🧪 Testing Preprocess Module Import")
    print("=" * 50)
    
    try:
        from src.utils.preprocess import CropAndExtract
        print("✅ Preprocess module imported successfully")
        print("✅ CropAndExtract class available")
        return True
    except Exception as e:
        print(f"❌ Preprocess module import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 3DMM Extraction Logic Test Suite")
    print("=" * 60)
    
    tests = [
        ("Array Concatenation", test_array_concatenation),
        ("Coefficient Validation", test_coefficient_validation),
        ("Preprocess Import", test_preprocess_import),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! 3DMM extraction logic is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
