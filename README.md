# i1Pro Python Wrapper

Python wrapper for the X-Rite i1Pro SDK, compatible with Python 3.11+.

## Overview

This wrapper provides a Pythonic interface to the i1Pro SDK for colorimetric measurements. It uses `ctypes` to interface with the native i1Pro DLL and `numpy` for efficient data handling.

## Features

- **Simple API**: High-level Python interface similar to the C++ wrapper
- **Type Safety**: Uses Python enums and type hints
- **NumPy Integration**: Spectral data returned as numpy arrays
- **Context Manager Support**: Automatic resource cleanup with `with` statement
- **Comprehensive Error Handling**: Detailed exception messages
- **Multiple Measurement Modes**: 
  - Emission (display measurements)
  - Reflectance (paper, print measurements)
  - Ambient light
  - Scan mode for patch strips

## Requirements

- Python 3.11+
- NumPy
- i1Pro SDK DLL files:
  - `i1Pro64.dll` (for 64-bit Python)
  - `i1Pro.lib` (for compilation, not needed at runtime)
  - `i1Pro.h` and `MeasurementConditions.h` (for reference)

## Installation

1. Ensure the i1Pro DLL is in the same directory as the wrapper or in your system PATH
2. Install required Python packages:

```bash
pip install numpy
```

For the advanced examples with plotting:

```bash
pip install numpy matplotlib
```

## Quick Start

### Basic Usage

```python
from i1pro_wrapper import I1Pro, MeasurementMode, Observer

# Create device instance
with I1Pro() as device:
    # Open device
    device.open()
    
    # Set measurement mode
    device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
    device.set_observer(Observer.TWO_DEGREE)
    
    # Calibrate
    print("Place on white tile...")
    input("Press Enter to calibrate...")
    device.calibrate()
    
    # Measure
    print("Place on display...")
    input("Press Enter to measure...")
    xyY, spectrum = device.measure_xyY_and_spectrum()
    
    print(f"x={xyY[0]:.4f}, y={xyY[1]:.4f}, Y={xyY[2]:.2f}")
    print(f"Spectrum: {spectrum}")
```

### Measurement Modes

```python
# Display measurement (emission)
device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)

# Paper/print measurement (reflectance)
device.set_measurement_mode(MeasurementMode.REFLECTANCE_SPOT)

# Scan mode (for color patches)
device.set_measurement_mode(MeasurementMode.REFLECTANCE_SCAN)

# Ambient light
device.set_measurement_mode(MeasurementMode.AMBIENT_LIGHT_SPOT)
```

### Setting Illumination and Observer

```python
from i1pro_wrapper import Illumination, Observer

# Set illumination (for reflectance measurements)
device.set_illumination(Illumination.D50)  # D50, D65, A, etc.

# Set observer
device.set_observer(Observer.TWO_DEGREE)   # 2° or 10° observer
```

## API Reference

### Class: I1Pro

Main class for interacting with i1Pro devices.

#### Methods

##### `__init__(dll_path: Optional[str] = None)`
Initialize the i1Pro wrapper.
- `dll_path`: Optional path to the DLL. If None, searches in current directory.

##### `open(device_index: int = 0) -> bool`
Open connection to device.
- `device_index`: Device index (default 0 for first device)
- Returns: True if successful

##### `close()`
Close device connection and cleanup resources.

##### `set_measurement_mode(mode: MeasurementMode)`
Set the measurement mode.
- `mode`: One of MeasurementMode enum values

##### `set_illumination(illumination: Illumination)`
Set illumination type for reflectance measurements.
- `illumination`: One of Illumination enum values

##### `set_observer(observer: Observer)`
Set observer angle (2° or 10°).
- `observer`: One of Observer enum values

##### `calibrate() -> bool`
Calibrate the device. Must place on white tile first.
- Returns: True if successful
- Raises: I1ProException if calibration fails

##### `trigger_measurement() -> bool`
Trigger a measurement.
- Returns: True if successful
- Raises: I1ProException if measurement fails

##### `measure_xyY() -> Tuple[float, float, float]`
Perform complete measurement and return xyY coordinates.
- Returns: Tuple of (x, y, Y)

##### `measure_spectrum() -> np.ndarray`
Perform complete measurement and return spectrum.
- Returns: NumPy array of 36 spectral values (380-730nm, 10nm steps)

##### `measure_xyY_and_spectrum() -> Tuple[Tuple[float, float, float], np.ndarray]`
Perform measurement and return both xyY and spectrum.
- Returns: Tuple of (xyY tuple, spectrum array)

##### `get_spectrum(index: int = 0) -> np.ndarray`
Get spectrum from previous measurement.
- `index`: Sample index (for scan mode)
- Returns: NumPy array of spectral values

##### `get_tristimulus(index: int = 0) -> np.ndarray`
Get tristimulus values from previous measurement.
- `index`: Sample index
- Returns: NumPy array of 3 values

##### `get_xyY(index: int = 0) -> Tuple[float, float, float]`
Get xyY from previous measurement.
- `index`: Sample index
- Returns: Tuple of (x, y, Y)

##### `get_number_of_samples() -> int`
Get number of samples from last measurement.
- Returns: 1 for spot, multiple for scan mode

##### `get_wavelengths() -> np.ndarray`
Get wavelength array for spectrum.
- Returns: NumPy array [380, 390, 400, ..., 730]

##### `is_button_pressed() -> bool`
Check if device button is currently pressed.
- Returns: True if pressed

##### `wait_for_button()`
Block until user presses and releases device button.

##### `get_serial_number() -> str`
Get device serial number.
- Returns: Serial number string

##### `get_sdk_version() -> str`
Get SDK version.
- Returns: Version string

### Enums

#### MeasurementMode
- `EMISSION_SPOT`: Display/emission spot measurement
- `REFLECTANCE_SPOT`: Reflectance spot measurement
- `DUAL_REFLECTANCE_SPOT`: Dual illumination spot (i1Pro2)
- `REFLECTANCE_SCAN`: Reflectance scan mode
- `DUAL_REFLECTANCE_SCAN`: Dual scan mode (i1Pro2)
- `AMBIENT_LIGHT_SPOT`: Ambient light spot
- `AMBIENT_LIGHT_SCAN`: Ambient light scan

#### Illumination
- `A`, `B`, `C`: CIE illuminants
- `D50`, `D55`, `D65`, `D75`: CIE daylight illuminants
- `F2`, `F7`, `F11`: Fluorescent illuminants
- `EMISSION`: For emissive measurements

#### Observer
- `TWO_DEGREE`: CIE 1931 2° observer
- `TEN_DEGREE`: CIE 1964 10° observer

### Exceptions

#### I1ProException
Raised when SDK returns an error.

Properties:
- `result_code`: I1ResultType enum value
- `message`: Error description string

## Examples

### Example 1: Simple Measurement (like eyeone.cpp)

```python
from i1pro_wrapper import I1Pro, MeasurementMode, Observer

device = I1Pro()
device.open()
device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
device.set_observer(Observer.TWO_DEGREE)

device.calibrate()
print("Calibrated!")

while True:
    input("Press Enter to measure...")
    xyY, spectrum = device.measure_xyY_and_spectrum()
    print(f"xyY: {xyY}")
    print(f"Spectrum: {spectrum}")

device.close()
```

### Example 2: Reflectance Measurement

```python
from i1pro_wrapper import I1Pro, MeasurementMode, Observer, Illumination

with I1Pro() as device:
    device.open()
    device.set_measurement_mode(MeasurementMode.REFLECTANCE_SPOT)
    device.set_illumination(Illumination.D50)
    device.set_observer(Observer.TWO_DEGREE)
    
    device.calibrate()
    xyY, spectrum = device.measure_xyY_and_spectrum()
    
    print(f"Reflectance: Y = {xyY[2]:.2f}%")
```

### Example 3: Scan Mode

```python
from i1pro_wrapper import I1Pro, MeasurementMode

with I1Pro() as device:
    device.open()
    device.set_measurement_mode(MeasurementMode.REFLECTANCE_SCAN)
    device.calibrate()
    
    print("Scan across patch strip...")
    device.wait_for_button()
    device.trigger_measurement()
    
    num_patches = device.get_number_of_samples()
    print(f"Found {num_patches} patches")
    
    for i in range(num_patches):
        xyY = device.get_xyY(i)
        spectrum = device.get_spectrum(i)
        print(f"Patch {i+1}: Y={xyY[2]:.2f}%")
```

### Example 4: Statistics from Multiple Measurements

```python
import numpy as np
from i1pro_wrapper import I1Pro, MeasurementMode

with I1Pro() as device:
    device.open()
    device.set_measurement_mode(MeasurementMode.EMISSION_SPOT)
    device.calibrate()
    
    measurements = []
    for i in range(10):
        xyY, _ = device.measure_xyY_and_spectrum()
        measurements.append(xyY[2])  # Y value
    
    measurements = np.array(measurements)
    print(f"Mean: {measurements.mean():.2f} cd/m²")
    print(f"Std: {measurements.std():.2f} cd/m²")
    print(f"CV: {(measurements.std()/measurements.mean())*100:.2f}%")
```

## Comparison with C++ Wrapper

The Python wrapper provides similar functionality to the C++ `IVeyeOne` class:

| C++ Method | Python Method |
|------------|---------------|
| `IVinit()` | `open()` + `set_measurement_mode()` |
| `IVcalibrate()` | `calibrate()` |
| `IVmeasurexyY()` | `measure_xyY()` |
| `IVmeasureSpectrum()` | `measure_spectrum()` |
| `IVmeasurexyYAndSpectrum()` | `measure_xyY_and_spectrum()` |
| `IVkeyPressed()` | `is_button_pressed()` |
| `IVclose()` | `close()` |
| `IVsetIllumination()` | `set_illumination()` |
| `IVsetObserver()` | `set_observer()` |

Key differences:
- Python uses NumPy arrays instead of `IVarray<float>`
- Python uses tuples for xyY instead of `IVcxyYColor`
- Python uses context managers (`with` statement) for resource management
- Python uses exceptions instead of boolean return values

## Data Structures

### Spectrum Data
Spectral data is returned as a NumPy array of 36 float values representing reflectance or radiance at wavelengths from 380nm to 730nm in 10nm steps.

```python
spectrum = device.get_spectrum()
wavelengths = device.get_wavelengths()

# wavelengths: [380, 390, 400, ..., 720, 730]
# spectrum: [0.123, 0.145, 0.167, ..., 0.891, 0.912]
```

### Color Data (xyY)
Color coordinates are returned as a tuple of three floats:
- `x`: CIE x chromaticity coordinate (0-1)
- `y`: CIE y chromaticity coordinate (0-1)
- `Y`: Luminance in cd/m² (emission) or % (reflectance)

```python
xyY = device.get_xyY()
x, y, Y = xyY
```

## Troubleshooting

### DLL Not Found
Ensure `i1Pro64.dll` is in:
1. Same directory as `i1pro_wrapper.py`
2. Your Python script's directory
3. System PATH

You can specify the DLL path explicitly:
```python
device = I1Pro(dll_path=r"C:\path\to\i1Pro64.dll")
```

### Device Not Found
- Check USB connection
- Verify device drivers are installed
- Try unplugging and reconnecting

### Calibration Failed
- Ensure device is on white tile
- Check that white tile cover is open
- Verify correct measurement mode

### "Device Not Calibrated" Error
Call `calibrate()` after `set_measurement_mode()` and before measurements.

## Thread Safety

The SDK is not thread-safe. Use locks if accessing from multiple threads.

## Performance Notes

- Spectrum measurements: ~1-2 seconds per measurement
- Scan mode: varies with scan speed and length
- Context manager (`with` statement) ensures proper cleanup

## License

This wrapper is provided for use with the i1Pro SDK. The SDK itself is copyright X-Rite Inc. and subject to their license terms.

## Support

For SDK-specific issues, contact X-Rite: devsupport@xrite.com

## Version History

- **1.0** (2025): Initial release
  - Support for all major measurement modes
  - NumPy integration
  - Python 3.11+ compatibility
