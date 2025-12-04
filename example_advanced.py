"""
Advanced example showing various i1Pro features
"""

from i1pro_wrapper import I1Pro, MeasurementMode, Observer, Illumination, I1ProException
import numpy as np
import matplotlib.pyplot as plt


def plot_spectrum(wavelengths, spectrum, title="Spectral Power Distribution", ylabel="Relative Power", 
                  ylim=None, show_100_percent_line=False):
    """Plot spectrum data"""
    plt.figure(figsize=(10, 6))
    plt.plot(wavelengths, spectrum, 'b-', linewidth=2)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.xlim(380, 730)
    if ylim is not None:
        plt.ylim(ylim)
    if show_100_percent_line:
        plt.axhline(y=100, color='r', linestyle='--', alpha=0.3, label='100% Reference')
        plt.legend()
    plt.show()


def display_measurement_example():
    """Measure display (emission mode)"""
    print("=== Display Measurement Example ===\n")
    
    with I1Pro() as device:
        device.open()
        device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
        device.set_observer(Observer.TWO_DEGREE)
        
        print("Place device on white tile and press Enter to calibrate...")
        input()
        device.calibrate()
        print("Calibrated!\n")
        
        print("Place device on display and press Enter to measure...")
        input()
        
        xyY, spectrum = device.measure_xyY_and_spectrum()
        wavelengths = device.get_wavelengths()
        
        print(f"\nMeasurement Results:")
        print(f"  x = {xyY[0]:.4f}")
        print(f"  y = {xyY[1]:.4f}")
        print(f"  Y = {xyY[2]:.2f} cd/m²")
        
        # Calculate CCT (simplified)
        n = (xyY[0] - 0.3320) / (0.1858 - xyY[1])
        cct = 449 * n**3 + 3525 * n**2 + 6823.3 * n + 5520.33
        print(f"  CCT ≈ {cct:.0f} K")
        
        # Plot spectrum
        plot_spectrum(wavelengths, spectrum, f"Display Spectrum (CCT ≈ {cct:.0f}K)")


def reflectance_measurement_example():
    """Measure reflectance"""
    print("=== Reflectance Measurement Example ===\n")
    
    with I1Pro() as device:
        device.open()
        device.set_measurement_mode(MeasurementMode.REFLECTANCE_SPOT)
        device.set_observer(Observer.TWO_DEGREE)
        device.set_illumination(Illumination.D50)
        
        print("Place device on white tile and press Enter to calibrate...")
        input()
        device.calibrate()
        print("Calibrated!\n")
        
        print("Place device on sample and press Enter to measure...")
        input()
        
        xyY, spectrum = device.measure_xyY_and_spectrum()
        wavelengths = device.get_wavelengths()
        
        print(wavelengths)

        print(f"\nReflectance Results:")
        print(f"  x = {xyY[0]:.4f}")
        print(f"  y = {xyY[1]:.4f}")
        print(f"  Y = {xyY[2]:.2f}% (reflectance)")
        
        # In reflectance mode, the SDK returns values as percentages (0-100)
        # Display spectral reflectance statistics
        print(f"\nSpectral Reflectance Statistics:")
        print(f"  Min: {np.min(spectrum):.2f}%")
        print(f"  Max: {np.max(spectrum):.2f}%")
        print(f"  Mean: {np.mean(spectrum):.2f}%")
        print(f"  Std: {np.std(spectrum):.2f}%")
        
        # Show some spectral values
        print(f"\nSample Spectral Values:")
        for i in [0, 9, 18, 27, 35]:  # Show values at 380, 470, 560, 650, 730 nm
            print(f"  {int(wavelengths[i])}nm: {spectrum[i]:.2f}%")
        
        # Note about white tile
        if xyY[2] > 85 and xyY[2] < 100:
            print(f"\nNote: White tile reflectance of {xyY[2]:.1f}% is expected.")
            print(f"      White tiles are typically 90-95% reflective.")
        
        # Plot spectrum with proper y-axis label
        plt.figure(figsize=(10, 6))
        plt.plot(wavelengths, spectrum, 'b-', linewidth=2)
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Reflectance (%)')
        plt.title(f"Reflectance Spectrum (Y = {xyY[2]:.1f}%)")
        plt.grid(True, alpha=0.3)
        plt.xlim(380, 730)
        plt.ylim(0, 105)  # Set y-axis from 0 to 105%
        plt.axhline(y=100, color='r', linestyle='--', alpha=0.3, label='100% Reference')
        plt.legend()
        plt.show()


def multiple_measurements_example():
    """Take multiple measurements and compute statistics"""
    print("=== Multiple Measurements Example ===\n")
    
    with I1Pro() as device:
        device.open()
        device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
        device.set_observer(Observer.TWO_DEGREE)
        
        print("Calibrating...")
        input("Press Enter...")
        device.calibrate()
        print("Calibrated!\n")
        
        num_measurements = 5
        measurements_Y = []
        measurements_x = []
        measurements_y = []
        
        print(f"Taking {num_measurements} measurements...")
        for i in range(num_measurements):
            print(f"Measurement {i+1}/{num_measurements} - Press Enter...")
            input()
            
            xyY, spectrum = device.measure_xyY_and_spectrum()
            measurements_x.append(xyY[0])
            measurements_y.append(xyY[1])
            measurements_Y.append(xyY[2])
            print(f"  Y = {xyY[2]:.2f} cd/m²")
        
        # Statistics
        x_array = np.array(measurements_x)
        y_array = np.array(measurements_y)
        Y_array = np.array(measurements_Y)
        
        print(f"\n=== Statistics ===")
        print(f"x: mean={x_array.mean():.4f}, std={x_array.std():.4f}")
        print(f"y: mean={y_array.mean():.4f}, std={y_array.std():.4f}")
        print(f"Y: mean={Y_array.mean():.2f}, std={Y_array.std():.2f} cd/m²")
        print(f"Y coefficient of variation: {(Y_array.std()/Y_array.mean())*100:.2f}%")


def reflectance_comparison_example():
    """Compare white tile to sample reflectance"""
    print("=== Reflectance Comparison Example ===\n")
    print("This example shows how to compare different samples")
    print("and understand reflectance values.\n")
    
    with I1Pro() as device:
        device.open()
        device.set_measurement_mode(MeasurementMode.REFLECTANCE_SPOT)
        device.set_observer(Observer.TWO_DEGREE)
        device.set_illumination(Illumination.D50)
        
        print("Place device on white tile and press Enter to calibrate...")
        input()
        device.calibrate()
        print("Calibrated!\n")
        
        # Measure white tile
        print("Keep device on white tile and press Enter to measure reference...")
        input()
        white_xyY, white_spectrum = device.measure_xyY_and_spectrum()
        wavelengths = device.get_wavelengths()
        
        print(f"\nWhite Tile (Reference):")
        print(f"  x = {white_xyY[0]:.4f}, y = {white_xyY[1]:.4f}")
        print(f"  Y = {white_xyY[2]:.2f}%")
        print(f"  Spectral range: {np.min(white_spectrum):.1f}% - {np.max(white_spectrum):.1f}%")
        
        # Measure sample
        print("\nPlace device on your sample and press Enter to measure...")
        input()
        sample_xyY, sample_spectrum = device.measure_xyY_and_spectrum()
        
        print(f"\nSample:")
        print(f"  x = {sample_xyY[0]:.4f}, y = {sample_xyY[1]:.4f}")
        print(f"  Y = {sample_xyY[2]:.2f}%")
        print(f"  Spectral range: {np.min(sample_spectrum):.1f}% - {np.max(sample_spectrum):.1f}%")
        
        # Calculate relative reflectance (sample vs white tile)
        # Note: In reflectance mode, values are already percentages
        relative_reflectance = (sample_xyY[2] / white_xyY[2]) * 100
        print(f"\nSample reflectance relative to white tile: {relative_reflectance:.1f}%")
        
        # Plot comparison
        plt.figure(figsize=(12, 6))
        plt.plot(wavelengths, white_spectrum, 'b-', linewidth=2, label=f'White Tile (Y={white_xyY[2]:.1f}%)')
        plt.plot(wavelengths, sample_spectrum, 'r-', linewidth=2, label=f'Sample (Y={sample_xyY[2]:.1f}%)')
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Reflectance (%)')
        plt.title('Spectral Reflectance Comparison')
        plt.grid(True, alpha=0.3)
        plt.xlim(380, 730)
        plt.ylim(0, max(105, np.max(white_spectrum) * 1.1))
        plt.axhline(y=100, color='gray', linestyle='--', alpha=0.3, label='100% Reference')
        plt.legend()
        plt.show()


def ambient_light_measurement_example():
    """Measure ambient light (illuminance)"""
    print("=== Ambient Light Measurement Example ===\n")
    print("This mode measures ambient lighting conditions.")
    print("Useful for photography, videography, and lighting design.\n")
    
    with I1Pro() as device:
        device.open()
        device.set_measurement_mode(MeasurementMode.AMBIENT_LIGHT_SPOT)
        device.set_observer(Observer.TWO_DEGREE)
        device.set_illumination(Illumination.D50)  # Reference for color calculations
        
        print("Place device with diffuser facing the light source.")
        print("Press Enter to calibrate...")
        input()
        device.calibrate()
        print("Calibrated!\n")
        
        print("Point device at light source and press Enter to measure...")
        input()
        
        xyY, spectrum = device.measure_xyY_and_spectrum()
        wavelengths = device.get_wavelengths()
        
        print(f"\nAmbient Light Results:")
        print(f"  Illuminance (Y): {xyY[2]:.2f} lux")
        print(f"  Chromaticity x:  {xyY[0]:.4f}")
        print(f"  Chromaticity y:  {xyY[1]:.4f}")
        
        # Calculate CCT for ambient light
        n = (xyY[0] - 0.3320) / (0.1858 - xyY[1])
        cct = 449 * n**3 + 3525 * n**2 + 6823.3 * n + 5520.33
        print(f"  CCT: ≈{cct:.0f} K")
        
        # Classify light level
        print(f"\nLight Level Classification:")
        if xyY[2] < 50:
            classification = "Very dark (moonlight level)"
        elif xyY[2] < 200:
            classification = "Dark (dim interior)"
        elif xyY[2] < 500:
            classification = "Low light (residential)"
        elif xyY[2] < 1000:
            classification = "Medium light (office/commercial)"
        elif xyY[2] < 2000:
            classification = "Bright (well-lit workspace)"
        else:
            classification = "Very bright (outdoor daylight)"
        print(f"  {classification}")
        
        # Spectral analysis
        print(f"\nSpectral Distribution:")
        print(f"  Peak wavelength: {int(wavelengths[np.argmax(spectrum)])} nm")
        print(f"  Spectrum range: {np.min(spectrum):.2f} - {np.max(spectrum):.2f}")
        
        # Dominant wavelength region
        blue_power = np.mean(spectrum[0:10])   # 380-480nm
        green_power = np.mean(spectrum[10:20]) # 480-580nm
        red_power = np.mean(spectrum[20:36])   # 580-730nm
        total_power = blue_power + green_power + red_power
        
        print(f"\nSpectral Power Distribution:")
        print(f"  Blue (380-480nm):  {(blue_power/total_power)*100:.1f}%")
        print(f"  Green (480-580nm): {(green_power/total_power)*100:.1f}%")
        print(f"  Red (580-730nm):   {(red_power/total_power)*100:.1f}%")
        
        # Plot spectrum
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(wavelengths, spectrum, 'b-', linewidth=2)
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Relative Power')
        plt.title(f'Ambient Light Spectrum\n({xyY[2]:.0f} lux, {cct:.0f}K)')
        plt.grid(True, alpha=0.3)
        plt.xlim(380, 730)
        
        # Plot chromaticity on CIE diagram (simplified)
        plt.subplot(1, 2, 2)
        plt.plot(xyY[0], xyY[1], 'ro', markersize=10, label=f'Measured ({cct:.0f}K)')
        
        # Plot blackbody locus using correct Planckian formulas
        # Based on Krystek (1985) approximation for CIE 1931 2° observer
        cct_range = np.linspace(1000, 15000, 100)
        x_bb = []
        y_bb = []
        for T in cct_range:
            # Planckian locus approximation by Krystek
            x_t = (-0.2661239e9/T**3 - 0.2343589e6/T**2 + 0.8776956e3/T + 0.179910)
            
            # Calculate y from x based on temperature range
            if T <= 4000:
                y_t = -1.1063814*x_t**3 - 1.34811020*x_t**2 + 2.18555832*x_t - 0.20219683
            else:
                y_t = -0.9549476*x_t**3 - 1.37418593*x_t**2 + 2.09137015*x_t - 0.16748867
            
            x_bb.append(x_t)
            y_bb.append(y_t)
        
        plt.plot(x_bb, y_bb, 'k--', linewidth=1.5, alpha=0.7, label='Blackbody locus')
        
        # Add temperature markers
        cct_markers = [2000, 3000, 4000, 5000, 6500, 10000]
        for T in cct_markers:
            x_t = (-0.2661239e9/T**3 - 0.2343589e6/T**2 + 0.8776956e3/T + 0.179910)
            if T <= 4000:
                y_t = -1.1063814*x_t**3 - 1.34811020*x_t**2 + 2.18555832*x_t - 0.20219683
            else:
                y_t = -0.9549476*x_t**3 - 1.37418593*x_t**2 + 2.09137015*x_t - 0.16748867
            plt.plot(x_t, y_t, 'k.', markersize=4)
            plt.text(x_t+0.01, y_t, f'{T}K', fontsize=8, alpha=0.7)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('CIE 1931 Chromaticity')
        plt.grid(True, alpha=0.3)
        plt.xlim(0.2, 0.5)
        plt.ylim(0.2, 0.5)
        plt.legend()
        plt.axis('equal')
        
        plt.tight_layout()
        plt.show()
        
        # Option for multiple measurements
        print("\n" + "=" * 60)
        response = input("Take another measurement? (y/n): ")
        if response.lower() == 'y':
            ambient_light_measurement_example()


def scan_mode_example():
    """Example of using scan mode"""
    print("=== Scan Mode Example ===\n")
    
    with I1Pro() as device:
        device.open()
        device.set_measurement_mode(MeasurementMode.REFLECTANCE_SCAN)
        device.set_observer(Observer.TWO_DEGREE)
        device.set_illumination(Illumination.D50)
        
        print("Calibrating...")
        input("Press Enter...")
        device.calibrate()
        print("Calibrated!\n")
        
        print("Press button on device and scan across patch strip...")
        device.wait_for_button()
        
        # Trigger scan
        device.trigger_measurement()
        
        # Get all samples
        num_samples = device.get_number_of_samples()
        print(f"\nScanned {num_samples} patches")
        
        # Collect all measurements
        spectra = []
        xyY_values = []
        
        for i in range(num_samples):
            xyY = device.get_xyY(i)
            spectrum = device.get_spectrum(i)
            xyY_values.append(xyY)
            spectra.append(spectrum)
            print(f"Patch {i+1}: Y={xyY[2]:.2f}%")
        
        # Plot all spectra
        wavelengths = device.get_wavelengths()
        plt.figure(figsize=(12, 6))
        for i, spectrum in enumerate(spectra):
            plt.plot(wavelengths, spectrum, label=f"Patch {i+1}")
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Reflectance (%)')
        plt.title(f'Scan Results: {num_samples} Patches')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()


def main():
    """Main menu"""
    print("i1Pro Python Wrapper - Advanced Examples")
    print("=" * 50)
    print("\nSelect example:")
    print("1. Display measurement (emission)")
    print("2. Reflectance measurement")
    print("3. Reflectance comparison (white tile vs sample)")
    print("4. Ambient light measurement")
    print("5. Multiple measurements with statistics")
    print("6. Scan mode")
    print("0. Exit")
    
    while True:
        choice = input("\nEnter choice: ")
        
        try:
            if choice == "1":
                display_measurement_example()
            elif choice == "2":
                reflectance_measurement_example()
            elif choice == "3":
                reflectance_comparison_example()
            elif choice == "4":
                ambient_light_measurement_example()
            elif choice == "5":
                multiple_measurements_example()
            elif choice == "6":
                scan_mode_example()
            elif choice == "0":
                break
            else:
                print("Invalid choice!")
        
        except I1ProException as e:
            print(f"\ni1Pro Error: {e}")
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
