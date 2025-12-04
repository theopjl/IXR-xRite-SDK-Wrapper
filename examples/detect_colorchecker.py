"""
Example script for ColorChecker detection and color extraction

This script detects a ColorChecker in an image using ArUco markers and extracts patch colors.
"""

import sys
import os

# Add src directory to path for importing xRite package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from xRite import ColorCheckerDetector, load_camera_params


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
