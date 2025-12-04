# Ambient Light Measurement Guide - i1Pro 3

## Overview

The i1Pro 3 can measure ambient lighting conditions using the **AMBIENT_LIGHT_SPOT** mode. This is useful for:
- **Photography & Videography**: Assess lighting conditions
- **Interior Design**: Evaluate room lighting
- **Workspace Ergonomics**: Ensure adequate lighting
- **Lighting Design**: Verify installations
- **Quality Control**: Check lighting standards compliance

## Quick Start

### Simple Measurement
```python
from i1pro_wrapper import I1Pro, MeasurementMode

with I1Pro() as device:
    device.open()
    device.set_measurement_mode(MeasurementMode.AMBIENT_LIGHT_SPOT)
    device.calibrate()
    
    xyY, spectrum = device.measure_xyY_and_spectrum()
    print(f"Illuminance: {xyY[2]:.1f} lux")
    print(f"CCT: {estimate_cct(xyY[0], xyY[1]):.0f} K")
```

### Run Examples
```bash
# Interactive ambient light tool
python example_ambient_light.py

# Advanced examples (option 4)
python example_advanced.py
```

## Measurement Setup

### 1. Prepare Device
- Attach the **white diffuser** to the i1Pro
- The diffuser must be clean and undamaged

### 2. Calibration
- Place device on **white calibration tile**
- Diffuser should face **upward**
- Follow calibration prompts

### 3. Measurement
- Position device at the **point of interest**
- Point diffuser toward **main light source**
- Can be placed on desk, held at eye level, etc.

## Understanding Results

### Illuminance (lux)

The Y value represents **illuminance** in lux:

| Lux Range | Classification | Examples |
|-----------|----------------|----------|
| < 1 | Darkness | Moonless night |
| 1-10 | Very dark | Moonlight |
| 10-50 | Dark | Candlelight, dimmed home |
| 50-100 | Low light | Home evening lighting |
| 100-300 | Medium-low | Living room |
| 300-500 | Medium | Minimum office lighting |
| 500-1000 | Bright | Good office lighting |
| 1000-2500 | Very bright | Retail, supermarket |
| 2500-10000 | Extremely bright | Studio, operating room |
| 10000-50000 | Outdoor shade | Overcast day |
| 50000+ | Direct sunlight | Full daylight |

### Lighting Standards

**ISO 8995 / EN 12464** recommendations:

| Activity | Recommended Lux |
|----------|-----------------|
| Corridors, hallways | 100 |
| Entrance areas | 100-200 |
| Meeting rooms | 300-500 |
| Office work (general) | 500 |
| Office work (detailed) | 750 |
| Drawing, CAD work | 750-1000 |
| Precision work | 1000-1500 |
| Inspection tasks | 1500-2000 |

### Color Temperature (CCT)

Measured in Kelvin (K):

| CCT Range | Description | Characteristics |
|-----------|-------------|-----------------|
| < 2000 K | Candle flame | Very warm, orange |
| 2000-2700 K | Warm white | Incandescent bulbs, cozy |
| 2700-3500 K | Warm white | Halogen, comfortable |
| 3500-4500 K | Neutral white | Fluorescent, balanced |
| 4500-6000 K | Cool white | Office lighting, alert |
| 6000-7000 K | Daylight | Natural daylight |
| 7000+ K | Cool daylight | Overcast sky, clinical |

**Usage recommendations:**
- **Warm (< 3000K)**: Bedrooms, restaurants, residential
- **Neutral (3000-4500K)**: Versatile, any space
- **Cool (> 4500K)**: Offices, task lighting, retail

### Chromaticity (x, y)

CIE 1931 color space coordinates:
- **x**: Red-green component (typically 0.2-0.5)
- **y**: Yellow-blue component (typically 0.2-0.5)

Used to calculate CCT and assess light quality.

## Measurement Techniques

### Single Point Measurement
Measures light at one location:
```python
device.calibrate()
xyY, spectrum = device.measure_xyY_and_spectrum()
```

### Multiple Point Survey
Measure several locations in a room:
```python
locations = ["Desk", "Window", "Center", "Corner"]
measurements = {}

for location in locations:
    input(f"Position at {location}, press Enter...")
    xyY, _ = device.measure_xyY_and_spectrum()
    measurements[location] = xyY[2]  # Store illuminance

# Analyze distribution
print(f"Average: {np.mean(list(measurements.values())):.1f} lux")
print(f"Min: {min(measurements.values()):.1f} lux")
print(f"Max: {max(measurements.values()):.1f} lux")
```

### Light Source Characterization
Analyze a specific light source:
```python
# Point directly at light source
xyY, spectrum = device.measure_xyY_and_spectrum()
wavelengths = device.get_wavelengths()

# Analyze spectrum
blue = np.mean(spectrum[0:10])   # 380-480nm
green = np.mean(spectrum[10:20]) # 480-580nm
red = np.mean(spectrum[20:36])   # 580-730nm
```

## Spectral Analysis

### Spectral Power Distribution
The spectrum shows **relative power** at each wavelength:
- **Continuous spectrum**: Incandescent, sunlight
- **Line spectrum**: Fluorescent, LED (spikes at specific wavelengths)
- **Balanced spectrum**: Good color rendering

### Color Rendering Assessment
Check spectral balance:
```python
blue_pct = (blue_power / total_power) * 100
green_pct = (green_power / total_power) * 100
red_pct = (red_power / total_power) * 100

# Ideal for color rendering:
# Blue: 30-40%, Green: 30-40%, Red: 25-35%
```

### LED vs Incandescent Detection
- **Incandescent**: Smooth, continuous spectrum
- **LED**: Spiky spectrum with distinct peaks
- **Fluorescent**: Multiple sharp peaks

## Practical Applications

### Photography/Videography
```python
# Check lighting consistency
measurements = []
for i in range(5):
    xyY, _ = device.measure_xyY_and_spectrum()
    measurements.append(xyY[2])

cv = (np.std(measurements) / np.mean(measurements)) * 100
if cv < 5:
    print("Stable lighting (good for video)")
else:
    print(f"Lighting varies {cv:.1f}% (use manual exposure)")
```

### Workspace Evaluation
```python
desk_lux = measure_at_desk()
if desk_lux < 500:
    print("Add task lighting")
elif desk_lux > 1000:
    print("Consider reducing glare")
else:
    print("Adequate lighting")
```

### Daylight Analysis
```python
# Measure at different times
times = ["9 AM", "12 PM", "3 PM", "6 PM"]
daylight_data = {}

for time in times:
    input(f"Measure at {time}...")
    xyY, _ = device.measure_xyY_and_spectrum()
    daylight_data[time] = xyY[2]

# Plot variation
```

### Color Temperature Matching
```python
# Match artificial to natural light
natural_xyY, _ = measure_window_light()
natural_cct = estimate_cct(natural_xyY[0], natural_xyY[1])

artificial_xyY, _ = measure_overhead_light()
artificial_cct = estimate_cct(artificial_xyY[0], artificial_xyY[1])

print(f"Natural: {natural_cct:.0f}K")
print(f"Artificial: {artificial_cct:.0f}K")
print(f"Difference: {abs(natural_cct - artificial_cct):.0f}K")
```

## Common Issues

### Low Readings (< expected)
**Causes:**
- Diffuser not properly attached
- Light source too far away
- Obstructed light path

**Solutions:**
- Check diffuser placement
- Move closer to light source
- Remove obstacles

### Inconsistent Readings
**Causes:**
- Flickering lights (AC-powered)
- Variable daylight (clouds)
- Movement during measurement

**Solutions:**
- Use adaptive measurement mode (default)
- Take multiple measurements and average
- Shield from direct sunlight for consistency

### Unexpected Color Temperature
**Causes:**
- Mixed lighting (daylight + artificial)
- Colored surfaces reflecting light
- Measurement angle

**Solutions:**
- Turn off artificial lights for daylight measurement
- Measure in neutral environment
- Ensure diffuser faces dominant light source

## Data Logging

### CSV Export
```python
import csv
from datetime import datetime

with open('lighting_log.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        datetime.now().isoformat(),
        location,
        xyY[2],  # lux
        xyY[0],  # x
        xyY[1],  # y
        estimate_cct(xyY[0], xyY[1])  # CCT
    ])
```

### Visualization
```python
import matplotlib.pyplot as plt

# Plot illuminance over time
times = [...]
lux_values = [...]

plt.plot(times, lux_values)
plt.xlabel('Time')
plt.ylabel('Illuminance (lux)')
plt.axhline(y=500, color='r', linestyle='--', label='Minimum office')
plt.legend()
plt.show()
```

## Tips & Best Practices

1. **Calibration**: Calibrate at the start of each session
2. **Consistent Position**: Keep device in same orientation for comparisons
3. **Multiple Readings**: Take 3-5 measurements and average
4. **Wait Time**: Allow 1-2 seconds for measurement to stabilize
5. **Ambient Only**: Measure ambient light, not direct sources
6. **Documentation**: Record location, time, and conditions

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't calibrate | Check white tile is clean, diffuser attached |
| Very low values | Ensure diffuser faces light source |
| Erratic readings | Check for flickering lights, stabilize device |
| Wrong mode | Verify AMBIENT_LIGHT_SPOT mode is set |

## Additional Resources

- **ISO 8995**: Lighting of work places
- **EN 12464-1**: Light and lighting - Lighting of work places
- **CIE Technical Reports**: Color measurement and rendering
- **IES Lighting Handbook**: Comprehensive lighting guide

## Example Scripts

- `example_ambient_light.py` - Interactive ambient light tool
- `example_advanced.py` - Comprehensive examples (option 4)
