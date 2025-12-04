# Understanding Reflectance Measurements with i1Pro

## What You're Seeing is Correct!

When you measure the white calibration tile and get **89.17% reflectance**, this is **completely normal and expected**. Here's why:

## Why Isn't the White Tile 100%?

### 1. Physical Reality
- **No material is perfectly reflective** in the real world
- The white calibration tile is a **diffuse reflector** (not a mirror)
- Even the best white standards reflect only about **90-98%** of incident light
- Some light is always absorbed by the material

### 2. The White Tile Specification
The i1Pro white calibration tile is typically:
- **~90-95% reflective** across the visible spectrum
- Slightly varies by wavelength
- This is a **known, calibrated reference**
- It's measured and characterized at the factory

### 3. What the i1Pro Does

During calibration:
1. The i1Pro measures the white tile
2. It stores this as the **reference white** (not as 100%)
3. Future measurements are compared to this reference
4. Values are given as **percentage relative to the reference**

So when you measure the white tile itself, you're seeing its **actual reflectance**, not 100% because you're not normalizing to it.

## Understanding the Values

### In Reflectance Mode:

```python
xyY, spectrum = device.measure_xyY_and_spectrum()
# Y = 89.17% means:
# - The sample reflects 89.17% of the light
# - This is typical for a white standard
# - Values are already in percentage (0-100%)
```

### Spectral Values

The spectral reflectance values you get are also in **percentages**:
- Each value represents **% reflectance at that wavelength**
- For the white tile: typically **85-95%** across all wavelengths
- For colored samples: varies significantly by wavelength

### Expected Values for Common Materials:

| Material | Typical Y (%) | Notes |
|----------|---------------|-------|
| White calibration tile | 85-95% | Factory calibrated reference |
| White paper (bright) | 80-90% | Depends on whiteness |
| White paper (standard) | 70-80% | Typical copy paper |
| Light gray | 40-60% | Mid-tone |
| Dark gray | 15-30% | Low reflectance |
| Black paper | 3-8% | Very low reflectance |
| Perfect black (theoretical) | 0% | Does not exist |
| Perfect white (theoretical) | 100% | Does not exist |

## Example: Comparing Measurements

### Measuring the White Tile
```
Reflectance Results:
  x = 0.3488
  y = 0.3622
  Y = 89.17% (reflectance)

Spectral values: 87-92% across 380-730nm
```
**This is correct!** The white tile is ~90% reflective.

### Measuring Bright White Paper
```
Reflectance Results:
  x = 0.3450
  y = 0.3580
  Y = 85.20% (reflectance)

Spectral values: 82-88% across 380-730nm
```
**Also normal.** Bright white paper reflects ~85% of light.

### Measuring Standard White Paper
```
Reflectance Results:
  x = 0.3420
  y = 0.3550
  Y = 75.60% (reflectance)

Spectral values: 72-78% across 380-730nm
```
**Expected.** Standard paper is less reflective than the white tile.

### Measuring a Black Sample
```
Reflectance Results:
  x = 0.3100
  y = 0.3200
  Y = 5.30% (reflectance)

Spectral values: 4-6% across 380-730nm
```
**Black materials** reflect very little light.

## Interpreting Spectral Data

### White Tile Spectrum (what you should see)
```
380nm: 87.2%
430nm: 89.5%
480nm: 90.1%
530nm: 91.3%
580nm: 90.8%
630nm: 89.9%
680nm: 88.5%
730nm: 87.8%
```

The spectrum is relatively **flat** (similar values across all wavelengths) because it's a neutral white.

### Colored Sample Spectrum (example: red paper)
```
380nm: 12.5%   (Low - absorbs blue/violet)
430nm: 15.8%   (Low - absorbs blue)
480nm: 18.2%   (Low - absorbs cyan)
530nm: 22.5%   (Medium - partially absorbs green)
580nm: 45.8%   (High - reflects yellow)
630nm: 65.2%   (High - reflects red)
680nm: 58.9%   (High - reflects red)
730nm: 42.1%   (Medium - reflects far red)
```

The spectrum shows **high values in red region**, low in blue/green - this is what makes it appear red!

## Calculating Relative Reflectance

If you want to express reflectance **relative to your white tile**:

```python
# Measure white tile
white_xyY, white_spectrum = device.measure_xyY_and_spectrum()
# white_xyY[2] = 89.17%

# Measure sample
sample_xyY, sample_spectrum = device.measure_xyY_and_spectrum()
# sample_xyY[2] = 75.60%

# Relative to white tile (as if white tile was 100%)
relative = (sample_xyY[2] / white_xyY[2]) * 100
# relative = (75.60 / 89.17) * 100 = 84.8%

print(f"Sample is {relative:.1f}% as reflective as the white tile")
```

## Normalizing Spectra

If you want spectra normalized to the white tile = 1.0:

```python
import numpy as np

white_xyY, white_spectrum = device.measure_xyY_and_spectrum()
sample_xyY, sample_spectrum = device.measure_xyY_and_spectrum()

# Normalize: divide sample by white tile
normalized_spectrum = sample_spectrum / white_spectrum

# Now normalized_spectrum values are:
# - ~1.0 for wavelengths where sample matches white tile
# - <1.0 for wavelengths where sample is less reflective
# - Could be >1.0 for fluorescent samples (rare)

print(f"Normalized spectrum range: {np.min(normalized_spectrum):.3f} - {np.max(normalized_spectrum):.3f}")
```

## Common Questions

### Q: Why don't I get 100% when measuring the white tile?
**A:** Because you're measuring its actual reflectance (~89%), not normalizing to it. This is the correct behavior.

### Q: Should I normalize my measurements to the white tile?
**A:** It depends on your application:
- **Color measurements (xyY, Lab)**: No normalization needed, use values as-is
- **Comparing materials**: Use actual % values
- **Spectral analysis needing normalized data**: Yes, divide by white tile spectrum
- **Following ISO standards**: Use actual % values

### Q: Is my device broken?
**A:** No! Getting ~85-95% for the white tile is completely normal and indicates proper calibration.

### Q: What if I get values over 100%?
**A:** This can happen with:
- **Fluorescent materials** that emit light (rare)
- **Glossy surfaces** with specular reflection (wrong measurement geometry)
- **Measurement errors** - recalibrate

### Q: What about absolute vs relative measurements?
**A:** The i1Pro in reflectance mode gives you:
- **Absolute reflectance** values in % (0-100%)
- Referenced to a **factory-calibrated white standard**
- This is what you're seeing: actual physical reflectance

## Visualizing the Concept

```
Light Source (100% intensity)
        ↓
        ↓  All light hits the sample
        ↓
    [White Tile]
        ↓
        ↓  ~89% reflects back
        ↓  ~11% absorbed
        ↓
   [i1Pro Sensor]

Result: Y = 89.17%
```

Compare to a less reflective sample:

```
Light Source (100% intensity)
        ↓
        ↓  All light hits the sample
        ↓
   [Gray Paper]
        ↓
        ↓  ~50% reflects back
        ↓  ~50% absorbed
        ↓
   [i1Pro Sensor]

Result: Y = 50.00%
```

## Summary

✅ **White tile at 89% is CORRECT**  
✅ **Spectral values 85-95% across wavelengths is NORMAL**  
✅ **This is absolute reflectance, not relative**  
✅ **Your i1Pro is working properly**  

The i1Pro is giving you physically accurate reflectance values. The white calibration tile is a reference standard, not a 100% reflector.

## Quick Reference

| What You Measure | Expected Y (%) | What It Means |
|------------------|----------------|---------------|
| White tile itself | 85-95% | Physical reflectance of tile |
| Perfect diffuse reflector (BaSO₄) | 98-99% | Lab standard, not your tile |
| Bright white paper | 80-90% | Very white, but not as good as tile |
| Office paper | 70-80% | Typical paper reflectance |
| Light colors | 40-70% | Moderate reflectance |
| Dark colors | 10-40% | Low reflectance |
| Black paper | 3-8% | Very low reflectance |

## Additional Resources

- ISO 13655:2017 - Graphic technology — Spectral measurement and colorimetric computation for graphic arts images
- CIE Technical Report 15:2018 - Colorimetry
- X-Rite white tile specifications (included with your device)

Remember: **The numbers you're seeing are correct!** The white tile is supposed to be around 90% reflective, not 100%.
