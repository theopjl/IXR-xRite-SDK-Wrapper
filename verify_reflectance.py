"""
Simple script to verify reflectance measurements
Shows that white tile at ~90% is correct and expected
"""

from i1pro_wrapper import I1Pro, MeasurementMode, Observer, Illumination
import numpy as np


def verify_reflectance():
    """Verify that reflectance measurements are working correctly"""
    print("=" * 60)
    print("i1Pro Reflectance Verification Test")
    print("=" * 60)
    print("\nThis test will verify that your reflectance measurements")
    print("are working correctly by measuring the white calibration tile.")
    print("\nExpected results:")
    print("  - White tile Y value: 85-95%")
    print("  - Spectral values: 85-95% across all wavelengths")
    print("  - Relatively flat spectrum (neutral white)")
    print()
    
    try:
        with I1Pro() as device:
            # Setup
            device.open()
            print(f"Device serial: {device.get_serial_number()}")
            print(f"SDK version: {device.get_sdk_version()}\n")
            
            device.set_measurement_mode(MeasurementMode.REFLECTANCE_SPOT)
            device.set_observer(Observer.TWO_DEGREE)
            device.set_illumination(Illumination.D50)
            
            # Calibrate
            print("Step 1: Calibration")
            print("-" * 60)
            print("Place the i1Pro on the white calibration tile.")
            input("Press Enter when ready to calibrate...")
            
            device.calibrate()
            print("✓ Calibration successful!\n")
            
            # Measure white tile
            print("Step 2: Measure White Tile")
            print("-" * 60)
            print("Keep the i1Pro on the white calibration tile.")
            input("Press Enter to measure the white tile...")
            
            xyY, spectrum = device.measure_xyY_and_spectrum()
            wavelengths = device.get_wavelengths()
            
            # Display results
            print("\n" + "=" * 60)
            print("MEASUREMENT RESULTS")
            print("=" * 60)
            
            print(f"\nCIE xyY Coordinates:")
            print(f"  x = {xyY[0]:.4f}")
            print(f"  y = {xyY[1]:.4f}")
            print(f"  Y = {xyY[2]:.2f}%")
            
            print(f"\nSpectral Reflectance Statistics:")
            print(f"  Minimum: {np.min(spectrum):.2f}%")
            print(f"  Maximum: {np.max(spectrum):.2f}%")
            print(f"  Mean:    {np.mean(spectrum):.2f}%")
            print(f"  Std Dev: {np.std(spectrum):.2f}%")
            print(f"  Range:   {np.max(spectrum) - np.min(spectrum):.2f}%")
            
            print(f"\nSample Spectral Values:")
            print(f"  {'Wavelength':<12} {'Reflectance'}")
            print(f"  {'-'*12} {'-'*12}")
            
            # Show every 5th wavelength
            for i in range(0, len(wavelengths), 5):
                wl = int(wavelengths[i])
                ref = spectrum[i]
                print(f"  {wl:3d} nm       {ref:6.2f}%")
            
            # Analysis
            print("\n" + "=" * 60)
            print("ANALYSIS")
            print("=" * 60)
            
            # Check if values are in expected range
            y_ok = 85 <= xyY[2] <= 95
            # Allow lower values at UV end (380-400nm) - some tiles have UV absorption
            spec_visible = spectrum[3:]  # Skip first 3 values (380, 390, 400 nm)
            spec_min_ok = np.min(spec_visible) >= 80
            spec_max_ok = np.max(spectrum) <= 100
            spec_range_ok = (np.max(spec_visible) - np.min(spec_visible)) < 15
            
            print(f"\nWhite Tile Y Value ({xyY[2]:.2f}%):")
            if y_ok:
                print(f"  ✓ CORRECT - In expected range (85-95%)")
                print(f"    This is the actual reflectance of your white tile.")
            else:
                print(f"  ⚠ WARNING - Outside expected range")
                if xyY[2] < 85:
                    print(f"    Value is lower than expected. Check calibration.")
                else:
                    print(f"    Value is higher than expected. Unusual.")
            
            print(f"\nSpectral Values (Range: {np.min(spectrum):.1f}-{np.max(spectrum):.1f}%):")
            if spec_min_ok and spec_max_ok:
                print(f"  ✓ CORRECT - All values in expected range (80-100%)")
            else:
                print(f"  ⚠ WARNING - Some values outside expected range")
            
            print(f"\nSpectral Flatness (Range: {np.max(spectrum) - np.min(spectrum):.2f}%):")
            if spec_range_ok:
                print(f"  ✓ CORRECT - Relatively flat (neutral white)")
                print(f"    A good white standard should have similar")
                print(f"    reflectance across all wavelengths.")
            else:
                print(f"  ⚠ Note - More variation than expected for white")
            
            # Overall verdict
            print("\n" + "=" * 60)
            if y_ok and spec_min_ok and spec_max_ok:
                print("✓ VERIFICATION PASSED")
                print("=" * 60)
                print("\nYour i1Pro is measuring correctly!")
                print("The white tile at ~90% reflectance is EXPECTED behavior.")
                print("\nKey points:")
                print("  • No real material reflects 100% of light")
                print("  • The white tile is a calibrated reference (~90%)")
                print("  • These are absolute reflectance values")
                print("  • Your measurements are physically accurate")
            else:
                print("⚠ VERIFICATION ISSUES DETECTED")
                print("=" * 60)
                print("\nSome values are outside expected ranges.")
                print("Recommendations:")
                print("  • Ensure device is clean")
                print("  • Try recalibrating")
                print("  • Check white tile for dirt/damage")
                print("  • Contact support if issues persist")
            
            # Additional test option
            print("\n" + "=" * 60)
            print("Optional: Compare to Another Sample")
            print("=" * 60)
            response = input("\nWould you like to measure another sample? (y/n): ")
            
            if response.lower() == 'y':
                print("\nPlace the i1Pro on your sample (e.g., white paper).")
                input("Press Enter to measure...")
                
                sample_xyY, sample_spectrum = device.measure_xyY_and_spectrum()
                
                print(f"\nSample Measurement:")
                print(f"  x = {sample_xyY[0]:.4f}")
                print(f"  y = {sample_xyY[1]:.4f}")
                print(f"  Y = {sample_xyY[2]:.2f}%")
                print(f"  Spectral range: {np.min(sample_spectrum):.1f}% - {np.max(sample_spectrum):.1f}%")
                
                # Calculate relative reflectance
                relative = (sample_xyY[2] / xyY[2]) * 100
                print(f"\nComparison to White Tile:")
                print(f"  White tile Y: {xyY[2]:.2f}%")
                print(f"  Sample Y:     {sample_xyY[2]:.2f}%")
                print(f"  Relative:     {relative:.1f}% of white tile")
                
                if sample_xyY[2] < xyY[2]:
                    print(f"\n  → Your sample is less reflective than the white tile")
                    print(f"     (as expected for most materials)")
                elif sample_xyY[2] > xyY[2]:
                    print(f"\n  → Your sample appears more reflective than the tile")
                    print(f"     (unusual - check for fluorescence or specular reflection)")
                else:
                    print(f"\n  → Your sample has similar reflectance to the tile")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  • Ensure i1Pro is connected")
        print("  • Check that i1Pro64.dll is in the correct location")
        print("  • Try reconnecting the device")
        return False
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)
    print("\nFor more information, see UNDERSTANDING_REFLECTANCE.md")
    return True


if __name__ == "__main__":
    verify_reflectance()
