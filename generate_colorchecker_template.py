"""
ColorChecker Template Generator with ArUco Markers

This script generates an A3 PDF template with ArUco markers positioned at the corners
to facilitate automatic detection of ColorChecker charts (Classic 24-patch or Digital SG).

Usage:
    python generate_colorchecker_template.py --type classic --output template_classic.pdf
    python generate_colorchecker_template.py --type digitalsg --output template_digitalsg.pdf
"""

import cv2
import numpy as np
import argparse
from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO


# ColorChecker dimensions (in mm)
COLORCHECKER_SPECS = {
    'classic': {
        'name': 'ColorChecker Classic (24 patches)',
        'width': 215.9,  # mm
        'height': 279.4,  # mm (standard size with border)
        'patch_area_width': 215.9,
        'patch_area_height': 139.7,
        'description': '4x6 grid of color patches'
    },
    'digitalsg': {
        'name': 'ColorChecker Digital SG (140 patches)',
        'width': 215.9,  # mm
        'height': 279.4,  # mm
        'patch_area_width': 215.9,
        'patch_area_height': 279.4,
        'description': '10x14 grid of color patches'
    }
}

# ArUco marker settings
ARUCO_DICT = cv2.aruco.DICT_4X4_100
MARKER_SIZE_MM = 20  # Size of each ArUco marker in mm
MARKER_IDS = [0, 1, 2, 3]  # IDs for the four corner markers


def generate_aruco_marker(marker_id, marker_size_pixels=200):
    """
    Generate an ArUco marker image.
    
    Args:
        marker_id: ID of the marker to generate
        marker_size_pixels: Size of the marker in pixels
        
    Returns:
        numpy array containing the marker image
    """
    aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size_pixels)
    return marker_img


def create_pdf_template(colorchecker_type, output_path):
    """
    Create a PDF template with ArUco markers for ColorChecker detection.
    
    Args:
        colorchecker_type: Either 'classic' or 'digitalsg'
        output_path: Path where the PDF will be saved
    """
    if colorchecker_type not in COLORCHECKER_SPECS:
        raise ValueError(f"Invalid colorchecker type. Must be 'classic' or 'digitalsg'")
    
    specs = COLORCHECKER_SPECS[colorchecker_type]
    
    # Create PDF canvas (A3 size)
    c = canvas.Canvas(output_path, pagesize=A3)
    page_width, page_height = A3
    
    # Calculate positions
    # Center the ColorChecker on the page
    cc_width = specs['width'] * mm
    cc_height = specs['height'] * mm
    
    # Position ColorChecker in the center
    cc_x = (page_width - cc_width) / 2
    cc_y = (page_height - cc_height) / 2
    
    # Margin around ColorChecker for ArUco markers
    marker_offset = 15 * mm  # Distance from ColorChecker edge to marker center
    marker_size = MARKER_SIZE_MM * mm
    
    # Calculate ArUco marker positions (at corners, outside the ColorChecker area)
    # Order: Top-Left (0), Top-Right (1), Bottom-Right (2), Bottom-Left (3)
    marker_positions = [
        # Top-Left
        (cc_x - marker_offset - marker_size/2, cc_y + cc_height + marker_offset - marker_size/2),
        # Top-Right
        (cc_x + cc_width + marker_offset - marker_size/2, cc_y + cc_height + marker_offset - marker_size/2),
        # Bottom-Right
        (cc_x + cc_width + marker_offset - marker_size/2, cc_y - marker_offset - marker_size/2),
        # Bottom-Left
        (cc_x - marker_offset - marker_size/2, cc_y - marker_offset - marker_size/2),
    ]
    
    # Draw title
    c.setFont("Helvetica-Bold", 16)
    title_y = page_height - 30
    c.drawCentredString(page_width/2, title_y, f"ColorChecker Detection Template")
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_width/2, title_y - 20, specs['name'])
    
    # Draw ColorChecker placement rectangle
    c.setStrokeColorRGB(0.2, 0.2, 0.8)  # Blue color
    c.setLineWidth(2)
    c.rect(cc_x, cc_y, cc_width, cc_height)
    
    # Add label for ColorChecker area
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.2, 0.2, 0.8)
    c.drawCentredString(page_width/2, cc_y + cc_height + 5, 
                       f"Place ColorChecker Here ({specs['width']:.1f} x {specs['height']:.1f} mm)")
    
    # Draw crosshairs at corners to help with alignment
    crosshair_size = 5
    c.setStrokeColorRGB(0.8, 0.2, 0.2)  # Red color
    c.setLineWidth(0.5)
    corners = [
        (cc_x, cc_y), (cc_x + cc_width, cc_y),
        (cc_x + cc_width, cc_y + cc_height), (cc_x, cc_y + cc_height)
    ]
    for cx, cy in corners:
        c.line(cx - crosshair_size, cy, cx + crosshair_size, cy)
        c.line(cx, cy - crosshair_size, cx, cy + crosshair_size)
    
    # Generate and place ArUco markers
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    
    for marker_id, (mx, my) in zip(MARKER_IDS, marker_positions):
        # Generate ArUco marker
        marker_img = generate_aruco_marker(marker_id, marker_size_pixels=400)
        
        # Convert to PIL Image via BytesIO
        marker_pil = BytesIO()
        # Convert to RGB (cv2 generates grayscale)
        marker_rgb = cv2.cvtColor(marker_img, cv2.COLOR_GRAY2RGB)
        from PIL import Image
        pil_img = Image.fromarray(marker_rgb)
        pil_img.save(marker_pil, format='PNG')
        marker_pil.seek(0)
        
        # Draw marker on PDF
        c.drawImage(ImageReader(marker_pil), mx, my, 
                   width=marker_size, height=marker_size)
        
        # Add marker ID label
        c.setFont("Helvetica", 8)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(mx + marker_size/2, my - 10, f"ID: {marker_id}")
    
    # Add instructions at the bottom
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0, 0, 0)
    instructions = [
        "Instructions:",
        "1. Print this template on A3 white paper",
        "2. Place the ColorChecker within the blue rectangle, aligning with corner marks",
        "3. Ensure all four ArUco markers are visible when photographing",
        "4. Keep the setup flat and evenly illuminated",
        f"5. ColorChecker type: {specs['description']}"
    ]
    
    y_pos = 60
    for instruction in instructions:
        c.drawString(50, y_pos, instruction)
        y_pos -= 15
    
    # Add technical information
    c.setFont("Helvetica", 7)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(50, 20, f"ArUco Dictionary: 4x4_100 | Marker IDs: {MARKER_IDS} | Marker Size: {MARKER_SIZE_MM}mm")
    
    # Save PDF
    c.save()
    print(f"PDF template generated successfully: {output_path}")
    print(f"ColorChecker type: {specs['name']}")
    print(f"Page size: A3 ({page_width/mm:.1f} x {page_height/mm:.1f} mm)")


def main():
    parser = argparse.ArgumentParser(
        description='Generate ColorChecker detection template with ArUco markers')
    parser.add_argument('--type', '-t', 
                       choices=['classic', 'digitalsg'],
                       default='classic',
                       help='Type of ColorChecker (classic or digitalsg)')
    parser.add_argument('--output', '-o',
                       default='colorchecker_template.pdf',
                       help='Output PDF file path')
    
    args = parser.parse_args()
    
    create_pdf_template(args.type, args.output)


if __name__ == '__main__':
    main()
