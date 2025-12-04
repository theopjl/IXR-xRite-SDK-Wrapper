# i1Pro Python Wrapper - Setup Guide

## Prerequisites

### 1. Hardware
- X-Rite i1Pro, i1Pro2, or i1Display colorimeter
- USB connection to Windows PC
- White calibration tile

### 2. Software
- Windows 10 or later (64-bit recommended)
- Python 3.11 or later
- i1Pro SDK DLL files (provided by X-Rite)

### 3. Python Packages
- numpy (required)
- matplotlib (optional, for examples with plotting)

## Installation Steps

### Step 1: Verify SDK Files

Ensure you have the following files in your working directory:

```
xRite/
├── i1Pro64.dll         # Main SDK library (64-bit)
├── i1Pro.lib           # Import library (for development)
├── i1Pro.h             # SDK header (for reference)
├── MeasurementConditions.h  # Constants header
├── i1pro_wrapper.py    # Python wrapper (this package)
├── example_simple.py   # Simple example
├── example_advanced.py # Advanced examples
├── test_wrapper.py     # Test suite
└── README.md           # Documentation
```

**Note:** For 32-bit Python, use `i1Pro.dll` instead of `i1Pro64.dll`

### Step 2: Install Python Dependencies

Open PowerShell or Command Prompt in the project directory:

```powershell
cd "C:\Users\colantoni\Nextcloud\Pedagogie\Plateforme IXR\Wraper\xRite"
```

Install required packages:

```powershell
pip install -r requirements.txt
```

Or manually:

```powershell
pip install numpy matplotlib
```

### Step 3: Verify Installation

Run the test script to verify everything is working:

```powershell
python test_wrapper.py
```

Expected output:
```
==================================================
i1Pro Python Wrapper Test Suite
==================================================

Test 1: SDK Loading
--------------------------------------------------
✓ SDK loaded successfully
✓ SDK Version: 4.2.0.0

Test 2: Device Detection
--------------------------------------------------
✓ Devices found: 1

...

✓ All tests passed!
```

If tests fail, check the troubleshooting section below.

### Step 4: Run Example

Try the simple example:

```powershell
python example_simple.py
```

## Usage Patterns

### Pattern 1: Quick Measurement

```python
from i1pro_wrapper import I1Pro, MeasurementMode

device = I1Pro()
device.open()
device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
device.calibrate()

xyY, spectrum = device.measure_xyY_and_spectrum()
print(f"Measured: x={xyY[0]:.4f}, y={xyY[1]:.4f}, Y={xyY[2]:.2f}")

device.close()
```

### Pattern 2: Context Manager (Recommended)

```python
from i1pro_wrapper import I1Pro, MeasurementMode

with I1Pro() as device:
    device.open()
    device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
    device.calibrate()
    
    xyY, spectrum = device.measure_xyY_and_spectrum()
    print(f"Measured: {xyY}")
    # Device automatically closed when exiting 'with' block
```

### Pattern 3: Multiple Measurements

```python
from i1pro_wrapper import I1Pro, MeasurementMode
import numpy as np

with I1Pro() as device:
    device.open()
    device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
    device.calibrate()
    
    # Collect 10 measurements
    Y_values = []
    for i in range(10):
        xyY, _ = device.measure_xyY_and_spectrum()
        Y_values.append(xyY[2])
    
    # Statistics
    Y_array = np.array(Y_values)
    print(f"Mean: {Y_array.mean():.2f} cd/m²")
    print(f"Std Dev: {Y_array.std():.2f} cd/m²")
```

## Common Workflows

### Workflow 1: Display Calibration

```python
from i1pro_wrapper import I1Pro, MeasurementMode, Observer

with I1Pro() as device:
    device.open()
    device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
    device.set_observer(Observer.TWO_DEGREE)
    
    # Calibrate
    print("Place device on white tile...")
    input("Press Enter to calibrate...")
    device.calibrate()
    
    # Measure white point
    print("Place device on display white...")
    input("Press Enter...")
    white_xyY, white_spectrum = device.measure_xyY_and_spectrum()
    
    # Measure primaries
    print("Place device on display red...")
    input("Press Enter...")
    red_xyY, _ = device.measure_xyY_and_spectrum()
    
    print("Place device on display green...")
    input("Press Enter...")
    green_xyY, _ = device.measure_xyY_and_spectrum()
    
    print("Place device on display blue...")
    input("Press Enter...")
    blue_xyY, _ = device.measure_xyY_and_spectrum()
    
    print(f"\nWhite: {white_xyY}")
    print(f"Red:   {red_xyY}")
    print(f"Green: {green_xyY}")
    print(f"Blue:  {blue_xyY}")
```

### Workflow 2: Print Quality Control

```python
from i1pro_wrapper import I1Pro, MeasurementMode, Illumination, Observer

with I1Pro() as device:
    device.open()
    device.set_measurement_mode(MeasurementMode.REFLECTANCE_SPOT)
    device.set_illumination(Illumination.D50)
    device.set_observer(Observer.TWO_DEGREE)
    
    device.calibrate()
    
    # Measure paper white
    print("Measure paper white...")
    input("Press Enter...")
    paper_xyY, _ = device.measure_xyY_and_spectrum()
    
    # Measure color patches
    patches = []
    for i in range(5):
        print(f"Measure patch {i+1}...")
        input("Press Enter...")
        xyY, spectrum = device.measure_xyY_and_spectrum()
        patches.append((xyY, spectrum))
    
    # Analyze
    print(f"\nPaper white Y: {paper_xyY[2]:.2f}%")
    for i, (xyY, _) in enumerate(patches):
        print(f"Patch {i+1} Y: {xyY[2]:.2f}%")
```

### Workflow 3: Scanning Color Charts

```python
from i1pro_wrapper import I1Pro, MeasurementMode

with I1Pro() as device:
    device.open()
    device.set_measurement_mode(MeasurementMode.REFLECTANCE_SCAN)
    device.calibrate()
    
    print("Press button on device and scan chart...")
    device.wait_for_button()
    device.trigger_measurement()
    
    num_patches = device.get_number_of_samples()
    print(f"Scanned {num_patches} patches")
    
    # Export data
    wavelengths = device.get_wavelengths()
    
    with open("scan_data.csv", "w") as f:
        # Header
        f.write("Patch,x,y,Y," + ",".join(f"{int(w)}nm" for w in wavelengths) + "\n")
        
        # Data
        for i in range(num_patches):
            xyY = device.get_xyY(i)
            spectrum = device.get_spectrum(i)
            
            f.write(f"{i+1},{xyY[0]:.6f},{xyY[1]:.6f},{xyY[2]:.4f},")
            f.write(",".join(f"{s:.6f}" for s in spectrum) + "\n")
    
    print("Data exported to scan_data.csv")
```

## Troubleshooting

### Error: "DLL not found"

**Problem:** The wrapper cannot locate `i1Pro64.dll`

**Solutions:**
1. Copy `i1Pro64.dll` to the same directory as your Python script
2. Copy `i1Pro64.dll` to the same directory as `i1pro_wrapper.py`
3. Add the DLL directory to your PATH
4. Specify DLL path explicitly:
   ```python
   device = I1Pro(dll_path=r"C:\full\path\to\i1Pro64.dll")
   ```

### Error: "No i1Pro devices connected"

**Problem:** Device not detected

**Solutions:**
1. Check USB cable connection
2. Verify device drivers are installed (should be automatic on Windows)
3. Try a different USB port
4. Restart the device by unplugging and reconnecting
5. Check Device Manager for "i1Pro" device

### Error: "Device not calibrated"

**Problem:** Attempting measurement without calibration

**Solutions:**
1. Call `device.calibrate()` after setting measurement mode
2. Place device on white tile during calibration
3. Ensure white tile cover is open
4. Recalibrate if you change measurement modes

### Error: "Calibration failed - not on white tile"

**Problem:** Device not properly positioned during calibration

**Solutions:**
1. Place device firmly on white calibration tile
2. Open the white tile protective cover
3. Ensure clean contact (no dust or debris)
4. Try cleaning the measurement aperture

### Error: "Access violation" or crash

**Problem:** DLL architecture mismatch

**Solutions:**
1. Match Python architecture (64-bit Python → `i1Pro64.dll`, 32-bit Python → `i1Pro.dll`)
2. Check Python version: `python --version`
3. Check architecture: `python -c "import struct; print(struct.calcsize('P') * 8)"`

### Slow measurements

**Problem:** Each measurement takes too long

**Solutions:**
1. For emission mode, this is normal (adaptive measurement)
2. Disable adaptive mode if acceptable:
   ```python
   # Not recommended - reduces accuracy
   device.sdk.dll.I1_SetOption(
       device.device_handle,
       b"AdaptiveMeasurement",
       b"0"
   )
   ```

### Import errors

**Problem:** Cannot import numpy or wrapper

**Solutions:**
1. Install numpy: `pip install numpy`
2. Check Python PATH
3. Verify you're using the correct Python interpreter

## Performance Tips

1. **Reuse device connection**: Open once, measure multiple times
2. **Use context managers**: Ensures proper cleanup
3. **Batch measurements**: Calibrate once, measure many times
4. **NumPy operations**: Use vectorized operations on spectral data

## Best Practices

### 1. Always use context managers

```python
# Good
with I1Pro() as device:
    # ... operations ...
    pass

# Bad - manual cleanup required
device = I1Pro()
device.open()
# ... operations ...
device.close()  # Easy to forget!
```

### 2. Check calibration status

```python
if not device.is_calibrated:
    device.calibrate()
```

### 3. Handle exceptions

```python
from i1pro_wrapper import I1ProException

try:
    xyY, spectrum = device.measure_xyY_and_spectrum()
except I1ProException as e:
    print(f"Measurement failed: {e}")
    # Handle error appropriately
```

### 4. Validate measurements

```python
xyY, spectrum = device.measure_xyY_and_spectrum()

# Check for reasonable values
if xyY[2] < 0 or xyY[2] > 10000:  # Luminance out of reasonable range
    print("Warning: Unusual luminance value")

if np.any(spectrum < 0):
    print("Warning: Negative spectral values detected")
```

## Advanced Topics

### Custom DLL Loading

```python
import os
from i1pro_wrapper import I1Pro

# Method 1: Relative path
dll_path = os.path.join(os.path.dirname(__file__), "sdk", "i1Pro64.dll")
device = I1Pro(dll_path=dll_path)

# Method 2: Absolute path
device = I1Pro(dll_path=r"C:\SDK\i1Pro\bin\i1Pro64.dll")

# Method 3: Environment variable
dll_path = os.environ.get("I1PRO_SDK_PATH", "i1Pro64.dll")
device = I1Pro(dll_path=dll_path)
```

### Working with Spectral Data

```python
import numpy as np
from i1pro_wrapper import I1Pro, MeasurementMode

with I1Pro() as device:
    device.open()
    device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
    device.calibrate()
    
    xyY, spectrum = device.measure_xyY_and_spectrum()
    wavelengths = device.get_wavelengths()
    
    # Normalize spectrum
    spectrum_norm = spectrum / np.max(spectrum)
    
    # Integrate over visible range
    total_power = np.trapz(spectrum, wavelengths)
    
    # Find peak wavelength
    peak_wl = wavelengths[np.argmax(spectrum)]
    print(f"Peak wavelength: {peak_wl:.0f} nm")
```

### Logging Measurements

```python
import csv
from datetime import datetime
from i1pro_wrapper import I1Pro, MeasurementMode

def log_measurement(filename, xyY, spectrum, wavelengths):
    """Append measurement to CSV file"""
    timestamp = datetime.now().isoformat()
    
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        
        # Write row: timestamp, x, y, Y, then all spectral values
        row = [timestamp, xyY[0], xyY[1], xyY[2]] + list(spectrum)
        writer.writerow(row)

# Usage
with I1Pro() as device:
    device.open()
    device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
    device.calibrate()
    
    wavelengths = device.get_wavelengths()
    
    # Create CSV with header
    with open("measurements.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        header = ["Timestamp", "x", "y", "Y"] + [f"{int(w)}nm" for w in wavelengths]
        writer.writerow(header)
    
    # Continuous logging
    while True:
        input("Press Enter to measure (Ctrl+C to exit)...")
        xyY, spectrum = device.measure_xyY_and_spectrum()
        log_measurement("measurements.csv", xyY, spectrum, wavelengths)
        print(f"Logged: Y = {xyY[2]:.2f}")
```

## Migration from C++ Wrapper

If you're migrating from the C++ `IVeyeOne` wrapper:

| C++ Code | Python Equivalent |
|----------|------------------|
| `IVeyeOne eyeOne;` | `device = I1Pro()` |
| `eyeOne.IVinit(eyeOneMeasureEmissionSpot);` | `device.open()`<br>`device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)` |
| `eyeOne.IVcalibrate();` | `device.calibrate()` |
| `IVcxyYColor xyY;`<br>`IVarray<float> spectrum;`<br>`eyeOne.IVmeasurexyYAndSpectrum(xyY, spectrum);` | `xyY, spectrum = device.measure_xyY_and_spectrum()` |
| `xyY[0], xyY[1], xyY[2]` | `xyY[0], xyY[1], xyY[2]` (same!) |
| `spectrum[i]` | `spectrum[i]` (same!) |
| `spectrum.IVnbElt()` | `len(spectrum)` or `spectrum.shape[0]` |

## Additional Resources

- X-Rite i1Pro SDK Documentation (included with SDK)
- X-Rite Developer Support: devsupport@xrite.com
- NumPy Documentation: https://numpy.org/doc/

## Support

For issues with:
- **The Python wrapper**: Check this documentation and test_wrapper.py
- **The i1Pro SDK**: Contact X-Rite developer support
- **Hardware issues**: Contact X-Rite customer support
