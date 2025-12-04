# ColorChecker Detection with ArUco Markers

This project provides tools to automatically detect and extract color values from X-Rite ColorChecker charts using ArUco markers for precise positioning.

## Overview

The system consists of two main scripts:

1. **`generate_colorchecker_template.py`** - Generates a PDF template with ArUco markers
2. **`detect_colorchecker.py`** - Detects the ColorChecker and extracts patch colors

## Features

- ✅ Supports **ColorChecker Classic** (24 patches) and **ColorChecker Digital SG** (140 patches)
- ✅ Automatic detection using 4 ArUco markers
- ✅ Works with **8-bit and 16-bit** RGB images
- ✅ Optional camera intrinsic parameter support for distortion correction
- ✅ Light compensation for Digital SG (using peripheral and center gray patches)
- ✅ Outputs extracted ColorChecker image, JSON data, and visualization

## Installation

1. Install the required dependencies:

```powershell
pip install -r colorchecker_requirements.txt
```

## Usage

### Step 1: Generate the Template

Generate a PDF template for your ColorChecker type:

**For ColorChecker Classic (24 patches):**
```powershell
python generate_colorchecker_template.py --type classic --output template_classic.pdf
```

**For ColorChecker Digital SG (140 patches):**
```powershell
python generate_colorchecker_template.py --type digitalsg --output template_digitalsg.pdf
```

### Step 2: Print and Setup

1. Print the generated PDF on **A3 white paper**
2. Place your ColorChecker on the marked rectangle
3. Ensure all 4 ArUco markers are visible
4. Keep the setup flat and evenly illuminated

### Step 3: Capture Image

Take a photo of the setup with your camera. Ensure:
- All 4 ArUco markers are visible and in focus
- The ColorChecker is properly placed within the rectangle
- Lighting is even (no strong shadows or reflections)
- Image is sharp (no motion blur)

### Step 4: Detect and Extract Colors

**Basic usage:**
```powershell
python detect_colorchecker.py --input photo.jpg --output results
```

**With camera calibration:**
```powershell
python detect_colorchecker.py --input photo.jpg --output results --camera-params camera_intrinsics.json
```

**With light compensation (Digital SG only):**
```powershell
python detect_colorchecker.py --input photo.tif --output results --light-compensation
```

## Outputs

The detection script generates three files in the output directory:

1. **`colorchecker_extracted.png`** - Warped and straightened ColorChecker image
2. **`detection_visualization.png`** - Original image with detected markers and boundaries
3. **`colorchecker_data.json`** - JSON file with extracted color values

### JSON Format

```json
{
  "colorchecker_type": "classic",
  "colorchecker_name": "ColorChecker Classic",
  "layout": {
    "rows": 4,
    "cols": 6,
    "total_patches": 24
  },
  "bit_depth": 8,
  "patch_colors": [
    [115.2, 82.5, 68.7],
    [194.8, 150.3, 130.1],
    ...
  ],
  "patch_colors_compensated": [  // Only if --light-compensation is used
    [113.5, 81.2, 67.9],
    ...
  ]
}
```

The `patch_colors` array contains RGB values for each patch in row-major order (left to right, top to bottom).

## Camera Intrinsics Format

If you have calibrated your camera, you can provide intrinsic parameters in JSON format:

```json
{
  "camera_matrix": [
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
  ],
  "dist_coeffs": [k1, k2, p1, p2, k3]
}
```

Where:
- `fx`, `fy` = focal lengths
- `cx`, `cy` = principal point
- `k1`, `k2`, `k3` = radial distortion coefficients
- `p1`, `p2` = tangential distortion coefficients

## ColorChecker Specifications

### ColorChecker Classic
- **Patches:** 24 (4 rows × 6 columns)
- **Size:** 215.9 × 139.7 mm
- **Gray scale:** Bottom row (last 6 patches)

### ColorChecker Digital SG
- **Patches:** 140 (10 rows × 14 columns)
- **Size:** 215.9 × 279.4 mm
- **Gray patches:** Around perimeter and 4 center patches
- **Light compensation:** Uses peripheral vs. center gray patches

## ArUco Marker Details

- **Dictionary:** 4×4 (100 markers)
- **Marker IDs:** 0, 1, 2, 3
- **Positions:** Top-Left, Top-Right, Bottom-Right, Bottom-Left (around ColorChecker)
- **Size:** 20 mm

## Troubleshooting

### Markers Not Detected
- Ensure markers are printed clearly (high quality printer)
- Check that all 4 markers are visible and in focus
- Improve lighting conditions
- Ensure markers are not occluded or damaged

### Wrong ColorChecker Type Detected
- The script uses aspect ratio to determine the type
- Ensure the ColorChecker is properly aligned within the rectangle
- Check that perspective distortion is minimal

### Inaccurate Colors
- Use proper lighting (D50 or D65 illuminant recommended)
- Avoid specular reflections on patches
- Ensure camera is in focus
- Consider using camera calibration parameters
- For Digital SG, try the light compensation option

### 16-bit Images
The detector automatically handles 16-bit TIFF or PNG images. RGB values will be in the range [0, 65535].

## Advanced Usage

### Batch Processing

Process multiple images:
```powershell
foreach ($img in Get-ChildItem *.jpg) {
    python detect_colorchecker.py --input $img --output "results/$($img.BaseName)"
}
```

### Integration with Color Management

The extracted RGB values can be used for:
- Camera characterization
- Color profile creation
- White balance adjustment
- Color accuracy testing
- Light source characterization

## Technical Details

### Detection Pipeline

1. **Marker Detection:** Detect 4 ArUco markers
2. **Corner Ordering:** Order markers as TL, TR, BR, BL
3. **ColorChecker Localization:** Calculate CC boundaries from marker positions
4. **Type Detection:** Determine Classic vs. Digital SG from aspect ratio
5. **Perspective Correction:** Warp image to frontal view
6. **Patch Extraction:** Sample color from center 40% of each patch
7. **Light Compensation (optional):** Normalize using gray patches

### Coordinate System

- Patches are indexed in **row-major order** (left to right, top to bottom)
- Marker ID 0 is at the top-left corner
- Color values are in **RGB order** (Red, Green, Blue)

## References

- X-Rite ColorChecker specifications
- OpenCV ArUco module documentation
- Color management best practices

## License

This tool is provided for educational and research purposes.

## Support

For issues or questions, please check:
1. Lighting conditions and image quality
2. Marker visibility and print quality
3. Correct ColorChecker placement
4. Camera calibration accuracy (if used)
