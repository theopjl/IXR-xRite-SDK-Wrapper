"""
Simple example of using the i1Pro Python wrapper
Mirrors the functionality of eyeone.cpp example
"""

import sys
import os

# Add src directory to path for importing xRite package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from xRite import I1Pro, MeasurementMode, Observer, I1ProException
import numpy as np


def main():
    """Simple measurement loop"""
    try:
        # Create and initialize device
        device = I1Pro()
        
        print("Initializing i1Pro device...")
        device.open()
        print(f"Device serial number: {device.get_serial_number()}")
        
        # Set measurement mode for emission (display measurement)
        device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
        device.set_observer(Observer.TWO_DEGREE)
        
        # Calibrate
        print("\nPlace device on white tile and press Enter...")
        input()
        device.calibrate()
        print("Calibrated!")
        
        # Continuous measurement loop
        print("\nMeasurement loop - Press Ctrl+C to exit")
        print("Press Enter to measure...")
        
        while True:
            input()  # Wait for Enter key
            
            # Measure both xyY and spectrum
            xyY, spectrum = device.measure_xyY_and_spectrum()
            
            # Display results
            print(f"\nxyY: x={xyY[0]:.4f}, y={xyY[1]:.4f}, Y={xyY[2]:.2f} cd/m²")
            print(f"Spectrum: {spectrum}")
            print("\nPress Enter to measure again...")
    
    except KeyboardInterrupt:
        print("\nExiting...")
    
    except I1ProException as e:
        print(f"i1Pro Error: {e}")
    
    finally:
        # Clean up
        device.close()
        print("Device closed.")


if __name__ == "__main__":
    main()
