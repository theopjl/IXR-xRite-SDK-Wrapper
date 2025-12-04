"""
ColorChecker Detection and Color Extraction

This module detects a ColorChecker chart in an image using ArUco markers,
extracts the color values from each patch, and optionally performs light compensation.
"""

import cv2
import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# ColorChecker specifications
COLORCHECKER_LAYOUTS = {
    'classic': {
        'name': 'ColorChecker Classic',
        'rows': 4,
        'cols': 6,
        'total_patches': 24,
        'width_mm': 215.9,
        'height_mm': 139.7,
        'has_gray_scale': True,
        'gray_positions': [19, 20, 21, 22, 23],  # Bottom row (indices in row-major order)
    },
    'digitalsg': {
        'name': 'ColorChecker Digital SG',
        'rows': 10,
        'cols': 14,
        'total_patches': 140,
        'width_mm': 215.9,
        'height_mm': 279.4,
        'has_gray_scale': True,
        # Digital SG has gray patches around the perimeter and in the center
        'peripheral_gray_patches': list(range(0, 14)) + list(range(126, 140)) + \
                                  [i * 14 for i in range(1, 9)] + [i * 14 + 13 for i in range(1, 9)],
        'center_gray_patches': [63, 64, 76, 77],  # 4 center patches
    }
}

# ArUco settings (must match template generation)
ARUCO_DICT = cv2.aruco.DICT_4X4_100
MARKER_IDS = [0, 1, 2, 3]  # Top-Left, Top-Right, Bottom-Right, Bottom-Left


class ColorCheckerDetector:
    """Detects and extracts colors from ColorChecker charts using ArUco markers."""
    
    def __init__(self, camera_params: Optional[Dict] = None):
        """
        Initialize the detector.
        
        Args:
            camera_params: Optional dictionary with 'camera_matrix' and 'dist_coeffs'
        """
        self.camera_params = camera_params
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
        
    def detect_markers(self, image: np.ndarray) -> Tuple[Optional[np.ndarray], Dict]:
        """
        Detect ArUco markers in the image.
        
        Args:
            image: Input image
            
        Returns:
            Tuple of (corners array, info dict)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        corners, ids, rejected = self.detector.detectMarkers(gray)
        
        if ids is None or len(ids) < 4:
            return None, {'error': f'Only {len(ids) if ids is not None else 0} markers detected, need 4'}
        
        # Check if we have all required marker IDs
        detected_ids = ids.flatten()
        missing_ids = [mid for mid in MARKER_IDS if mid not in detected_ids]
        
        if missing_ids:
            return None, {'error': f'Missing marker IDs: {missing_ids}'}
        
        # Sort corners by marker ID
        marker_corners = {}
        for i, marker_id in enumerate(detected_ids):
            if marker_id in MARKER_IDS:
                marker_corners[marker_id] = corners[i][0]
        
        return marker_corners, {'detected_ids': detected_ids.tolist()}
    
    def order_corners(self, marker_corners: Dict) -> np.ndarray:
        """
        Order the ColorChecker corners from marker positions.
        Markers are: 0=TL, 1=TR, 2=BR, 3=BL (around the ColorChecker)
        
        Args:
            marker_corners: Dictionary mapping marker ID to corner coordinates
            
        Returns:
            Array of 4 corners in order [TL, TR, BR, BL]
        """
        # Get the center of each marker
        corners = []
        for marker_id in MARKER_IDS:
            marker = marker_corners[marker_id]
            center = marker.mean(axis=0)
            corners.append(center)
        
        return np.array(corners, dtype=np.float32)
    
    def get_colorchecker_corners(self, marker_corners_2d: np.ndarray) -> np.ndarray:
        """
        Calculate the actual ColorChecker corners from marker positions.
        The markers are positioned outside the ColorChecker area.
        
        Args:
            marker_corners_2d: 4 marker center points [TL, TR, BR, BL]
            
        Returns:
            4 ColorChecker corners [TL, TR, BR, BL]
        """
        # Calculate the inward offset based on marker positions
        # Estimate the ColorChecker region by moving inward from markers
        
        # Calculate vectors from markers towards the center
        center = marker_corners_2d.mean(axis=0)
        
        cc_corners = []
        for marker_pt in marker_corners_2d:
            direction = center - marker_pt
            direction = direction / np.linalg.norm(direction)
            # Move inward by approximately 15-20% of the distance to center
            offset = direction * np.linalg.norm(center - marker_pt) * 0.3
            cc_corners.append(marker_pt + offset)
        
        return np.array(cc_corners, dtype=np.float32)
    
    def detect_colorchecker_type(self, image: np.ndarray, cc_corners: np.ndarray) -> str:
        """
        Determine the type of ColorChecker (classic or digitalsg) based on aspect ratio.
        
        Args:
            image: Input image
            cc_corners: ColorChecker corners
            
        Returns:
            'classic' or 'digitalsg'
        """
        # Calculate aspect ratio
        width = np.linalg.norm(cc_corners[1] - cc_corners[0])
        height = np.linalg.norm(cc_corners[3] - cc_corners[0])
        aspect_ratio = width / height
        
        # Classic: ~1.54 (215.9/139.7), Digital SG: ~0.77 (215.9/279.4)
        if aspect_ratio > 1.2:
            return 'classic'
        else:
            return 'digitalsg'
    
    def extract_patches(self, image: np.ndarray, cc_corners: np.ndarray, 
                       cc_type: str) -> Tuple[List[np.ndarray], np.ndarray]:
        """
        Extract color patches from the ColorChecker.
        
        Args:
            image: Input image
            cc_corners: ColorChecker corners [TL, TR, BR, BL]
            cc_type: 'classic' or 'digitalsg'
            
        Returns:
            Tuple of (list of RGB values, warped ColorChecker image)
        """
        layout = COLORCHECKER_LAYOUTS[cc_type]
        rows, cols = layout['rows'], layout['cols']
        
        # Define the size of the warped image
        output_width = 1400  # pixels (100 pixels per column for 14 cols)
        output_height = int(output_width * layout['height_mm'] / layout['width_mm'])
        
        # Destination points for perspective transform
        dst_corners = np.array([
            [0, 0],
            [output_width - 1, 0],
            [output_width - 1, output_height - 1],
            [0, output_height - 1]
        ], dtype=np.float32)
        
        # Calculate perspective transform
        matrix = cv2.getPerspectiveTransform(cc_corners, dst_corners)
        
        # Warp the image
        warped = cv2.warpPerspective(image, matrix, (output_width, output_height))
        
        # Calculate patch positions
        patch_colors = []
        
        # Add small margin to avoid edge effects
        margin_ratio = 0.05
        effective_width = output_width * (1 - 2 * margin_ratio)
        effective_height = output_height * (1 - 2 * margin_ratio)
        x_start = output_width * margin_ratio
        y_start = output_height * margin_ratio
        
        patch_width = effective_width / cols
        patch_height = effective_height / rows
        
        # Sample from the center of each patch (avoid edges)
        sample_ratio = 0.4  # Sample from center 40% of each patch
        
        for row in range(rows):
            for col in range(cols):
                # Calculate patch center
                cx = x_start + (col + 0.5) * patch_width
                cy = y_start + (row + 0.5) * patch_height
                
                # Define sampling region
                sample_w = patch_width * sample_ratio
                sample_h = patch_height * sample_ratio
                
                x1 = int(cx - sample_w / 2)
                x2 = int(cx + sample_w / 2)
                y1 = int(cy - sample_h / 2)
                y2 = int(cy + sample_h / 2)
                
                # Extract patch region
                patch = warped[y1:y2, x1:x2]
                
                # Calculate mean color
                mean_color = patch.mean(axis=(0, 1))
                patch_colors.append(mean_color)
        
        return patch_colors, warped
    
    def apply_light_compensation(self, patch_colors: List[np.ndarray], 
                                 cc_type: str) -> List[np.ndarray]:
        """
        Apply light compensation using gray patches (only for Digital SG).
        
        Args:
            patch_colors: List of RGB values for each patch
            cc_type: ColorChecker type
            
        Returns:
            List of compensated RGB values
        """
        if cc_type != 'digitalsg':
            print("Warning: Light compensation only available for Digital SG")
            return patch_colors
        
        layout = COLORCHECKER_LAYOUTS[cc_type]
        
        # Get peripheral gray patches
        peripheral_indices = layout.get('peripheral_gray_patches', [])
        center_indices = layout.get('center_gray_patches', [])
        
        if not peripheral_indices or not center_indices:
            print("Warning: Gray patch positions not defined for light compensation")
            return patch_colors
        
        # Calculate average illumination from peripheral and center gray patches
        peripheral_grays = [patch_colors[i] for i in peripheral_indices if i < len(patch_colors)]
        center_grays = [patch_colors[i] for i in center_indices if i < len(patch_colors)]
        
        if not peripheral_grays or not center_grays:
            print("Warning: Could not find gray patches for compensation")
            return patch_colors
        
        peripheral_avg = np.mean(peripheral_grays, axis=0)
        center_avg = np.mean(center_grays, axis=0)
        
        # Calculate compensation factor
        # Assume center should match peripheral illumination
        compensation = center_avg / (peripheral_avg + 1e-6)
        
        print(f"Light compensation factors (RGB): {compensation}")
        
        # Apply compensation to all patches
        compensated = []
        for color in patch_colors:
            compensated_color = color / compensation
            # Clip to valid range
            compensated_color = np.clip(compensated_color, 0, 255 if color.dtype == np.uint8 else 65535)
            compensated.append(compensated_color)
        
        return compensated
    
    def process_image(self, image_path: str, output_dir: str, 
                     apply_light_comp: bool = False) -> Dict:
        """
        Process an image to detect and extract ColorChecker data.
        
        Args:
            image_path: Path to input image
            output_dir: Directory to save outputs
            apply_light_comp: Whether to apply light compensation
            
        Returns:
            Dictionary with results
        """
        # Load image
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            return {'error': f'Could not load image: {image_path}'}
        
        # Handle 16-bit images
        is_16bit = image.dtype == np.uint16
        bit_depth = 16 if is_16bit else 8
        
        # Convert to BGR if grayscale
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        # Detect ArUco markers
        print("Detecting ArUco markers...")
        marker_corners, marker_info = self.detect_markers(image)
        
        if marker_corners is None:
            return {'error': marker_info.get('error', 'Marker detection failed')}
        
        print(f"Found markers: {marker_info['detected_ids']}")
        
        # Order corners
        ordered_markers = self.order_corners(marker_corners)
        
        # Calculate ColorChecker corners
        cc_corners = self.get_colorchecker_corners(ordered_markers)
        
        # Detect ColorChecker type
        cc_type = self.detect_colorchecker_type(image, cc_corners)
        layout = COLORCHECKER_LAYOUTS[cc_type]
        print(f"Detected ColorChecker type: {layout['name']}")
        
        # Extract patches
        print("Extracting color patches...")
        patch_colors, warped_image = self.extract_patches(image, cc_corners, cc_type)
        
        # Apply light compensation if requested
        if apply_light_comp and cc_type == 'digitalsg':
            print("Applying light compensation...")
            patch_colors_compensated = self.apply_light_compensation(patch_colors, cc_type)
        else:
            patch_colors_compensated = None
        
        # Prepare output
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save warped ColorChecker image
        warped_path = output_path / 'colorchecker_extracted.png'
        if is_16bit:
            cv2.imwrite(str(warped_path), warped_image.astype(np.uint16))
        else:
            cv2.imwrite(str(warped_path), warped_image)
        print(f"Saved extracted ColorChecker: {warped_path}")
        
        # Save visualization with detected markers
        vis_image = image.copy()
        if is_16bit:
            vis_image = (vis_image / 256).astype(np.uint8)
        
        # Draw markers
        cv2.aruco.drawDetectedMarkers(vis_image, 
                                     [marker_corners[mid].reshape(1, 4, 2) for mid in MARKER_IDS],
                                     np.array(MARKER_IDS))
        
        # Draw ColorChecker corners
        cc_corners_int = cc_corners.astype(np.int32)
        cv2.polylines(vis_image, [cc_corners_int], True, (0, 255, 0), 3)
        
        vis_path = output_path / 'detection_visualization.png'
        cv2.imwrite(str(vis_path), vis_image)
        print(f"Saved visualization: {vis_path}")
        
        # Prepare JSON output
        json_data = {
            'colorchecker_type': cc_type,
            'colorchecker_name': layout['name'],
            'layout': {
                'rows': layout['rows'],
                'cols': layout['cols'],
                'total_patches': layout['total_patches']
            },
            'bit_depth': bit_depth,
            'patch_colors': [color.tolist() for color in patch_colors],
        }
        
        if patch_colors_compensated:
            json_data['patch_colors_compensated'] = [color.tolist() for color in patch_colors_compensated]
        
        # Save JSON
        json_path = output_path / 'colorchecker_data.json'
        with open(json_path, 'w') as f:
            json.dump(json_data, f, indent=2)
        print(f"Saved color data: {json_path}")
        
        return {
            'success': True,
            'colorchecker_type': cc_type,
            'total_patches': len(patch_colors),
            'output_files': {
                'extracted_image': str(warped_path),
                'visualization': str(vis_path),
                'data': str(json_path)
            }
        }


def load_camera_params(params_path: str) -> Dict:
    """Load camera intrinsic parameters from JSON file."""
    with open(params_path, 'r') as f:
        params = json.load(f)
    
    return {
        'camera_matrix': np.array(params['camera_matrix']),
        'dist_coeffs': np.array(params['dist_coeffs'])
    }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Detect ColorChecker and extract patch colors using ArUco markers')
    parser.add_argument('--input', '-i', required=True,
                       help='Input image path (8-bit or 16-bit RGB)')
    parser.add_argument('--output', '-o', required=True,
                       help='Output directory for results')
    parser.add_argument('--camera-params', '-c',
                       help='Optional: Camera intrinsic parameters (JSON file)')
    parser.add_argument('--light-compensation', '-l', action='store_true',
                       help='Apply light compensation (Digital SG only)')
    
    args = parser.parse_args()
    
    # Load camera parameters if provided
    camera_params = None
    if args.camera_params:
        try:
            camera_params = load_camera_params(args.camera_params)
            print("Loaded camera parameters")
        except Exception as e:
            print(f"Warning: Could not load camera parameters: {e}")
    
    # Create detector
    detector = ColorCheckerDetector(camera_params)
    
    # Process image
    result = detector.process_image(args.input, args.output, args.light_compensation)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return 1
    
    print("\nProcessing complete!")
    print(f"ColorChecker type: {result['colorchecker_type']}")
    print(f"Total patches: {result['total_patches']}")
    print(f"Output files saved to: {args.output}")
    
    return 0


if __name__ == '__main__':
    exit(main())
