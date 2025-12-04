"""
Simple example for ambient light measurement with i1Pro 3
Useful for measuring room lighting, photography lighting, etc.
"""

from i1pro_wrapper import I1Pro, MeasurementMode, Observer, Illumination, I1ProException
import numpy as np


def classify_light_level(lux):
    """Classify illuminance level"""
    if lux < 1:
        return "Darkness", "Moonless night"
    elif lux < 10:
        return "Very dark", "Moonlight, dimmed lights"
    elif lux < 50:
        return "Dark", "Typical home lighting (evening)"
    elif lux < 100:
        return "Low light", "Hallways, corridors"
    elif lux < 300:
        return "Medium-low", "Living room, bedroom"
    elif lux < 500:
        return "Medium", "Office lighting (recommended minimum)"
    elif lux < 1000:
        return "Bright", "Office, retail (good lighting)"
    elif lux < 2500:
        return "Very bright", "Supermarket, well-lit workspace"
    elif lux < 10000:
        return "Extremely bright", "Operating room, studio lighting"
    elif lux < 50000:
        return "Outdoor shade", "Cloudy day outdoors"
    else:
        return "Direct sunlight", "Full daylight"


def estimate_cct(x, y):
    """Estimate Correlated Color Temperature"""
    n = (x - 0.3320) / (0.1858 - y)
    cct = 449 * n**3 + 3525 * n**2 + 6823.3 * n + 5520.33
    return cct


def classify_color_temperature(cct):
    """Classify color temperature"""
    if cct < 2000:
        return "Candle flame"
    elif cct < 2700:
        return "Warm white (incandescent)"
    elif cct < 3500:
        return "Warm white (halogen)"
    elif cct < 4500:
        return "Neutral white"
    elif cct < 6000:
        return "Cool white"
    elif cct < 7000:
        return "Daylight"
    else:
        return "Cool daylight / Overcast sky"


def main():
    """Main ambient light measurement loop"""
    print("=" * 70)
    print("i1Pro 3 - Ambient Light Measurement")
    print("=" * 70)
    print("\nThis tool measures ambient lighting conditions including:")
    print("  • Illuminance (lux)")
    print("  • Color temperature (Kelvin)")
    print("  • Chromaticity coordinates")
    print("  • Spectral power distribution")
    print()
    
    try:
        with I1Pro() as device:
            # Setup
            device.open()
            print(f"Device: {device.get_serial_number()}")
            
            device.set_measurement_mode(MeasurementMode.AMBIENT_LIGHT_SPOT)
            device.set_observer(Observer.TWO_DEGREE)
            device.set_illumination(Illumination.D50)
            
            # Calibrate
            print("\n" + "=" * 70)
            print("CALIBRATION")
            print("=" * 70)
            print("Place the i1Pro with the white diffuser facing upward.")
            print("Position it on the white calibration tile.")
            input("\nPress Enter to calibrate...")
            
            device.calibrate()
            print("✓ Calibrated successfully!")
            
            # Measurement loop
            print("\n" + "=" * 70)
            print("MEASUREMENT")
            print("=" * 70)
            print("Position the i1Pro where you want to measure light.")
            print("Point the white diffuser toward the main light source.")
            print()
            
            measurement_count = 0
            
            while True:
                input("Press Enter to measure (or Ctrl+C to exit)...")
                
                measurement_count += 1
                xyY, spectrum = device.measure_xyY_and_spectrum()
                wavelengths = device.get_wavelengths()
                
                # Display results
                print("\n" + "-" * 70)
                print(f"MEASUREMENT #{measurement_count}")
                print("-" * 70)
                
                # Basic measurements
                print(f"\n📊 Illuminance:")
                print(f"   {xyY[2]:,.1f} lux")
                level, description = classify_light_level(xyY[2])
                print(f"   Level: {level}")
                print(f"   ({description})")
                
                # Color temperature
                cct = estimate_cct(xyY[0], xyY[1])
                print(f"\n🌡️  Color Temperature:")
                print(f"   {cct:.0f} K")
                print(f"   Type: {classify_color_temperature(cct)}")
                
                # Chromaticity
                print(f"\n🎨 Chromaticity:")
                print(f"   x = {xyY[0]:.4f}")
                print(f"   y = {xyY[1]:.4f}")
                
                # Spectral analysis
                blue_power = np.mean(spectrum[0:10])   # 380-480nm
                green_power = np.mean(spectrum[10:20]) # 480-580nm  
                red_power = np.mean(spectrum[20:36])   # 580-730nm
                total_power = blue_power + green_power + red_power
                
                print(f"\n🌈 Spectral Composition:")
                print(f"   Blue:  {(blue_power/total_power)*100:5.1f}% (380-480nm)")
                print(f"   Green: {(green_power/total_power)*100:5.1f}% (480-580nm)")
                print(f"   Red:   {(red_power/total_power)*100:5.1f}% (580-730nm)")
                
                peak_wl = int(wavelengths[np.argmax(spectrum)])
                print(f"   Peak wavelength: {peak_wl} nm")
                
                # Light quality assessment
                print(f"\n💡 Light Quality Notes:")
                
                # Check for balanced spectrum (good for color rendering)
                if 30 < (blue_power/total_power)*100 < 40 and \
                   30 < (green_power/total_power)*100 < 40 and \
                   25 < (red_power/total_power)*100 < 35:
                    print(f"   ✓ Well-balanced spectrum (good color rendering)")
                else:
                    print(f"   ⚠ Unbalanced spectrum")
                
                # Warm vs cool
                if cct < 3000:
                    print(f"   🔥 Warm light (relaxing, cozy)")
                elif cct > 5000:
                    print(f"   ❄️  Cool light (alerting, energizing)")
                else:
                    print(f"   ⚪ Neutral light (versatile)")
                
                # Brightness assessment for different activities
                print(f"\n📖 Lighting Recommendations:")
                if xyY[2] < 200:
                    print(f"   Too dark for most tasks")
                    print(f"   Good for: Ambient/mood lighting, watching TV")
                elif xyY[2] < 500:
                    print(f"   Adequate for: Reading, casual work")
                    print(f"   Too dim for: Detailed work, precise tasks")
                elif xyY[2] < 1000:
                    print(f"   Good for: Office work, general tasks")
                    print(f"   Adequate for: Reading, computer work")
                elif xyY[2] < 2000:
                    print(f"   Excellent for: Detailed work, art, precision tasks")
                else:
                    print(f"   Very bright - excellent for: All tasks")
                
                # Comparison to standards
                print(f"\n📏 Standards Comparison:")
                if xyY[2] < 300:
                    print(f"   ⚠ Below ISO 8995 office minimum (500 lux)")
                elif xyY[2] < 500:
                    print(f"   ⚠ At lower limit for office work")
                elif xyY[2] < 750:
                    print(f"   ✓ Good for general office work")
                else:
                    print(f"   ✓ Exceeds office requirements")
                
                print("\n" + "-" * 70)
    
    except KeyboardInterrupt:
        print("\n\nMeasurement stopped by user.")
    
    except I1ProException as e:
        print(f"\n❌ i1Pro Error: {e}")
        print("\nTroubleshooting:")
        print("  • Ensure the device is properly connected")
        print("  • Check that calibration was successful")
        print("  • Make sure the white diffuser is attached")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        print("\n" + "=" * 70)
        print("Measurement session ended")
        print("=" * 70)


if __name__ == "__main__":
    main()
