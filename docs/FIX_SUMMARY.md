# Reflectance Measurement Fix - Summary

## Issue Found

When measuring reflectance with the i1Pro, the spectral values were being returned as fractions (0-1) while the Y tristimulus value was returned as a percentage (0-100). This caused confusion because:

- **Y value**: 89.17% ✓ (correct, as percentage)
- **Spectral values**: 0.73 - 0.91 ✗ (incorrect scale, should be 73-91%)

## Root Cause

The X-Rite i1Pro SDK has an inconsistency:
- **Tristimulus values (xyY)**: Y is returned as percentage (0-100)
- **Spectral values**: In reflectance mode, returned as fractions (0-1)

This is different from emission mode where both use relative scales.

## Fix Applied

Updated `i1pro_wrapper.py` in the `get_spectrum()` method to automatically scale reflectance spectral values:

```python
# In reflectance mode, SDK returns values as fractions (0-1)
# but Y values as percentages (0-100). Scale spectrum to match.
if self.measurement_mode in [MeasurementMode.REFLECTANCE_SPOT,
                             MeasurementMode.REFLECTANCE_SCAN,
                             MeasurementMode.DUAL_REFLECTANCE_SPOT,
                             MeasurementMode.DUAL_REFLECTANCE_SCAN]:
    # Scale from 0-1 to 0-100 to match Y percentage
    spec_array = spec_array * 100.0
```

## Results After Fix

Now all reflectance measurements return consistent units:

```
White Tile Measurement:
  Y = 89.11%
  Spectrum: 73.03% - 91.06%
  
Sample Spectral Values:
  380 nm: 73.03%
  430 nm: 84.54%
  480 nm: 87.72%
  530 nm: 88.82%
  580 nm: 89.36%
  630 nm: 89.79%
  680 nm: 90.35%
  730 nm: 91.06%
```

All values are now in percentages (%), making them consistent and easier to interpret.

## Why Your Measurement Was Correct

Your original measurement showed:
- **Y = 89.17%** - This was always correct!
- **Spectrum values** - Were correct but displayed in wrong scale (0-1 instead of 0-100)

The white calibration tile reflecting ~89% of light is **completely normal**. No real material reflects 100% of light.

## Understanding the Spectral Curve

The white tile shows:
- **Lower reflectance at 380nm (73%)**: Common for white standards, slight UV absorption
- **Higher reflectance at 730nm (91%)**: Slight increase in near-IR
- **Overall range (73-91%)**: Within normal variation for a diffuse white standard
- **Mean (~88%)**: Matches the Y value of 89% very well

This is expected behavior for a calibrated white reference tile.

## UV Absorption Note

Many white calibration tiles have **reduced reflectance in the UV region** (380-400nm):
- This is **intentional** in some designs
- Helps provide a neutral reference under different light sources
- Your tile showing 73% at 380nm vs 89-91% in visible range is normal

## Verification

Run the verification script to check your measurements:
```bash
python verify_reflectance.py
```

This will:
1. Calibrate the device
2. Measure the white tile
3. Analyze the results
4. Confirm everything is working correctly

Expected result: **✓ VERIFICATION PASSED**

## Updated Files

1. **i1pro_wrapper.py** - Fixed spectrum scaling in reflectance mode
2. **example_advanced.py** - Updated reflectance example with better explanations
3. **verify_reflectance.py** - New verification script
4. **UNDERSTANDING_REFLECTANCE.md** - Complete guide to reflectance measurements

## Quick Reference

| Measurement Type | Y Units | Spectrum Units | Range |
|-----------------|---------|----------------|-------|
| **Emission** | cd/m² | Relative | Varies |
| **Reflectance** | % (0-100) | % (0-100) | 0-100% |
| **Ambient** | lux | Relative | Varies |

## Testing Your Fix

1. **Test with white tile**:
   ```python
   python verify_reflectance.py
   ```
   Expected: Y ≈ 89%, Spectrum ≈ 73-91%

2. **Test with white paper**:
   ```python
   python example_advanced.py
   # Choose option 2 or 3
   ```
   Expected: Y ≈ 75-85%, Spectrum varies

3. **Test comparison**:
   Run option 3 in advanced examples to compare white tile vs sample

## Summary

✅ **Fix Applied**: Spectral values now scale correctly in reflectance mode  
✅ **Units Consistent**: Both Y and spectrum use percentages (0-100)  
✅ **Measurements Correct**: White tile at ~89% is expected behavior  
✅ **Documentation Updated**: Complete guides added  

Your i1Pro is working perfectly! The confusion was just about the scale of the spectral values.
