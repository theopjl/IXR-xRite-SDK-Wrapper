"""
Test script for i1Pro Python wrapper
Run without device to test SDK loading
"""

import sys
import os

# Add src directory to path for importing xRite package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from xRite import I1Pro, MeasurementMode, Observer, Illumination, I1ProException


def test_sdk_loading():
    """Test if SDK DLL can be loaded"""
    print("Test 1: SDK Loading")
    print("-" * 50)
    try:
        device = I1Pro()
        print("✓ SDK loaded successfully")
        print(f"✓ SDK Version: {device.get_sdk_version()}")
        return True
    except FileNotFoundError as e:
        print(f"✗ DLL not found: {e}")
        return False
    except Exception as e:
        print(f"✗ Error loading SDK: {e}")
        return False


def test_device_detection():
    """Test device detection"""
    print("\nTest 2: Device Detection")
    print("-" * 50)
    try:
        device = I1Pro()
        num_devices = device.get_devices()
        print(f"✓ Devices found: {num_devices}")
        if num_devices == 0:
            print("  Note: No i1Pro devices connected (this is OK for testing)")
        return True
    except I1ProException as e:
        print(f"✗ Error detecting devices: {e}")
        return False


def test_enums():
    """Test enum definitions"""
    print("\nTest 3: Enum Definitions")
    print("-" * 50)
    try:
        # Test MeasurementMode
        modes = [
            MeasurementMode.EMISSION_SPOT,
            MeasurementMode.REFLECTANCE_SPOT,
            MeasurementMode.REFLECTANCE_SCAN,
        ]
        print(f"✓ MeasurementMode enum: {len(modes)} modes tested")
        
        # Test Illumination
        illums = [
            Illumination.D50,
            Illumination.D65,
            Illumination.A,
        ]
        print(f"✓ Illumination enum: {len(illums)} illuminants tested")
        
        # Test Observer
        observers = [Observer.TWO_DEGREE, Observer.TEN_DEGREE]
        print(f"✓ Observer enum: {len(observers)} observers tested")
        
        return True
    except Exception as e:
        print(f"✗ Error with enums: {e}")
        return False


def test_device_operations():
    """Test device operations if device is connected"""
    print("\nTest 4: Device Operations")
    print("-" * 50)
    
    try:
        device = I1Pro()
        num_devices = device.get_devices()
        
        if num_devices == 0:
            print("⊘ Skipping - no device connected")
            return True
        
        # Open device
        print("Opening device...")
        device.open()
        print(f"✓ Device opened")
        print(f"  Serial: {device.get_serial_number()}")
        
        # Set measurement mode
        print("Setting measurement mode...")
        device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
        device.set_observer(Observer.TWO_DEGREE)
        print("✓ Measurement mode set")
        
        # Get wavelengths
        wavelengths = device.get_wavelengths()
        print(f"✓ Wavelengths: {wavelengths[0]:.0f}nm to {wavelengths[-1]:.0f}nm ({len(wavelengths)} points)")
        
        # Close device
        device.close()
        print("✓ Device closed")
        
        return True
        
    except I1ProException as e:
        print(f"✗ Device operation failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_numpy_integration():
    """Test numpy integration"""
    print("\nTest 5: NumPy Integration")
    print("-" * 50)
    try:
        import numpy as np
        device = I1Pro()
        wavelengths = device.get_wavelengths()
        
        # Check type
        assert isinstance(wavelengths, np.ndarray), "Wavelengths should be numpy array"
        assert wavelengths.dtype == np.float32, "Should be float32"
        assert len(wavelengths) == 36, "Should have 36 values"
        
        print("✓ NumPy arrays working correctly")
        print(f"  Shape: {wavelengths.shape}")
        print(f"  Dtype: {wavelengths.dtype}")
        print(f"  Range: {wavelengths[0]:.0f} to {wavelengths[-1]:.0f} nm")
        
        return True
    except AssertionError as e:
        print(f"✗ Assertion failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("i1Pro Python Wrapper Test Suite")
    print("=" * 50 + "\n")
    
    results = []
    
    # Run tests
    results.append(("SDK Loading", test_sdk_loading()))
    results.append(("Device Detection", test_device_detection()))
    results.append(("Enum Definitions", test_enums()))
    results.append(("Device Operations", test_device_operations()))
    results.append(("NumPy Integration", test_numpy_integration()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
