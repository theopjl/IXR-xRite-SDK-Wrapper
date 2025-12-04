# xRite Python SDK Wrapper

Python wrapper for the X-Rite i1Pro SDK and ColorChecker detection tools, compatible with Python 3.11+.

## Project Structure

```
xRite/
├── dlls/                    # xRite SDK DLL files (64-bit)
│   └── i1Pro64.dll
├── include/                 # SDK header files
│   ├── i1Pro.h
│   └── MeasurementConditions.h
├── src/xRite/               # Python package
│   ├── __init__.py
│   ├── i1pro_wrapper.py     # i1Pro SDK wrapper
│   ├── colorchecker_detector.py  # ColorChecker detection
│   └── colorchecker_template.py  # Template generation
├── examples/                # Python examples
│   ├── example_simple.py
│   ├── example_advanced.py
│   ├── example_ambient_light.py
│   ├── detect_colorchecker.py
│   ├── generate_template.py
│   └── verify_reflectance.py
├── tests/                   # Unit tests
│   └── test_wrapper.py
├── docs/                    # Documentation
│   ├── AMBIENT_LIGHT_GUIDE.md
│   ├── COLORCHECKER_README.md
│   ├── FIX_SUMMARY.md
│   ├── SETUP_GUIDE.md
│   └── UNDERSTANDING_REFLECTANCE.md
├── requirements.txt         # Python dependencies
├── colorchecker_requirements.txt  # ColorChecker dependencies
└── README.md
```

## Features

### i1Pro Wrapper
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

### ColorChecker Detection
- ✅ Supports **ColorChecker Classic** (24 patches) and **ColorChecker Digital SG** (140 patches)
- ✅ Automatic detection using 4 ArUco markers
- ✅ Works with **8-bit and 16-bit** RGB images
- ✅ Optional camera intrinsic parameter support for distortion correction
- ✅ Light compensation for Digital SG (using peripheral and center gray patches)
- ✅ Outputs extracted ColorChecker image, JSON data, and visualization

## Requirements

### For i1Pro Wrapper
- Python 3.11+
- NumPy
- i1Pro SDK DLL files:
  - `i1Pro64.dll` (for 64-bit Python)

### For ColorChecker Detection
- Python 3.11+
- OpenCV with ArUco module (`opencv-contrib-python`)
- NumPy
- Pillow
- ReportLab (for PDF generation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/theopjl/IXR-xRite-SDK-Wrapper.git
cd IXR-xRite-SDK-Wrapper
```

2. Install Python dependencies:

For i1Pro wrapper:
```bash
pip install -r requirements.txt
```

For ColorChecker detection:
```bash
pip install -r colorchecker_requirements.txt
```

3. Ensure the i1Pro DLL is in the `dlls/` directory.

## Quick Start

### i1Pro Measurements

```python
import sys
sys.path.insert(0, 'src')

from xRite import I1Pro, MeasurementMode, Observer

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
```

### ColorChecker Template Generation

```bash
python examples/generate_template.py --type classic --output template.pdf
python examples/generate_template.py --type digitalsg --output template_sg.pdf
```

### ColorChecker Detection

```bash
python examples/detect_colorchecker.py --input photo.jpg --output results
python examples/detect_colorchecker.py --input photo.tif --output results --light-compensation
```

## API Reference

### i1Pro Classes

#### `I1Pro`
Main class for interacting with i1Pro devices.

```python
from xRite import I1Pro, MeasurementMode, Observer, Illumination

device = I1Pro()
device.open()
device.set_measurement_mode(MeasurementMode.REFLECTANCE_SPOT)
device.set_illumination(Illumination.D50)
device.set_observer(Observer.TWO_DEGREE)
device.calibrate()
xyY, spectrum = device.measure_xyY_and_spectrum()
device.close()
```

#### Measurement Modes
- `EMISSION_SPOT`: Display/emission spot measurement
- `REFLECTANCE_SPOT`: Reflectance spot measurement
- `DUAL_REFLECTANCE_SPOT`: Dual illumination spot (i1Pro2)
- `REFLECTANCE_SCAN`: Reflectance scan mode
- `AMBIENT_LIGHT_SPOT`: Ambient light spot

#### Illumination Types
- `A`, `B`, `C`: CIE illuminants
- `D50`, `D55`, `D65`, `D75`: CIE daylight illuminants
- `F2`, `F7`, `F11`: Fluorescent illuminants
- `EMISSION`: For emissive measurements

#### Observer Types
- `TWO_DEGREE`: CIE 1931 2° observer
- `TEN_DEGREE`: CIE 1964 10° observer

### ColorChecker Classes

#### `ColorCheckerDetector`
Detects and extracts colors from ColorChecker charts.

```python
from xRite import ColorCheckerDetector

detector = ColorCheckerDetector()
result = detector.process_image('photo.jpg', 'output_dir', apply_light_comp=True)
```

#### Template Generation
```python
from xRite import create_pdf_template

create_pdf_template('classic', 'template_classic.pdf')
create_pdf_template('digitalsg', 'template_digitalsg.pdf')
```

## Running Examples

```bash
# Simple i1Pro measurement
python examples/example_simple.py

# Advanced i1Pro examples (menu-driven)
python examples/example_advanced.py

# Ambient light measurement
python examples/example_ambient_light.py

# Verify reflectance measurements
python examples/verify_reflectance.py

# Generate ColorChecker template
python examples/generate_template.py --type classic --output template.pdf

# Detect ColorChecker in image
python examples/detect_colorchecker.py --input photo.jpg --output results
```

## Running Tests

```bash
python tests/test_wrapper.py
```

## Documentation

Detailed documentation is available in the `docs/` directory:

- [Setup Guide](docs/SETUP_GUIDE.md) - Complete installation and setup instructions
- [Ambient Light Guide](docs/AMBIENT_LIGHT_GUIDE.md) - Guide for ambient light measurements
- [ColorChecker README](docs/COLORCHECKER_README.md) - ColorChecker detection documentation
- [Understanding Reflectance](docs/UNDERSTANDING_REFLECTANCE.md) - Understanding reflectance measurements
- [Fix Summary](docs/FIX_SUMMARY.md) - Summary of measurement fixes

## Data Structures

### Spectrum Data
Spectral data is returned as a NumPy array of 36 float values representing reflectance or radiance at wavelengths from 380nm to 730nm in 10nm steps.

```python
spectrum = device.get_spectrum()
wavelengths = device.get_wavelengths()  # [380, 390, 400, ..., 730]
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
Ensure `i1Pro64.dll` is in the `dlls/` directory or specify the path explicitly:
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

## License

This wrapper is provided for use with the i1Pro SDK. The SDK itself is copyright X-Rite Inc. and subject to their license terms.

## Support

For SDK-specific issues, contact X-Rite: devsupport@xrite.com

## Version History

- **1.0.0** (2025): Initial release
  - Support for all major measurement modes
  - NumPy integration
  - Python 3.11+ compatibility
  - ColorChecker detection with ArUco markers
  - Reorganized project structure
